"""Free, local geometric warp ("liquify") of the lower-body silhouette, for shape previews.

Usage: python scripts/body_warp.py experiments/006-body-control

Reads <experiment>/warp_config.json. For each view and intensity it pushes the legging outline outward (and, for
front views, the inner-thigh contours toward each other) by the configured pixel profiles, then writes:
    warp/<view>-<intensity>.png       warped preview (originals are never modified)
    warp/<view>-<intensity>-diff.png  changed pixels in red over a grey copy of the original
    warp_previews.jpg                 A | B-mid | B-strong per view, same scale
    warp_measurements.json            legging-mask widths before/after and changed-pixel checks

Method: each image row gets a smooth monotonic 1-D mapping built from outline landmarks (outer edges, leg centres,
inner-thigh edges, body midline) detected from the leggings' colour. Displacement is zero at and above the
waistband and tapers to zero at the knees, so the waist, upper body and face are untouched by construction. Arms
and hands move rigidly with the body surface beside them (translated, never stretched); the maximum shift is
reported in warp_measurements.json.
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import (binary_closing, binary_dilation, gaussian_filter, gaussian_filter1d, label,
                           map_coordinates, median_filter)

REPO = Path(__file__).resolve().parent.parent


def masks(rgb):
    R, G, B = (rgb[..., i].astype(float) for i in range(3))
    luma = 0.299 * R + 0.587 * G + 0.114 * B
    leggings = (luma < 172) & ((R - B) < 45)
    skin = ((R - B) > 40) & (R > 120) & ~leggings
    return leggings, skin


def runs_in_row(row, x0, x1, min_len=15):
    xs = np.where(row[x0:x1])[0] + x0
    if len(xs) == 0:
        return []
    parts = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1)
    return [(p[0], p[-1]) for p in parts if len(p) >= min_len]


def profile(keys, ys):
    """Linear keyframes [[y, value], ...] -> values at ys, smoothed; zero outside the keyframe range."""
    k = np.array(keys, dtype=float)
    v = np.interp(ys, k[:, 0], k[:, 1], left=0.0, right=0.0)
    return gaussian_filter1d(v, 12)


def landmarks(leggings, view, y0, y1, x0, x1):
    H = leggings.shape[0]
    n = y1 - y0
    L = {k: np.full(n, np.nan) for k in ("oL", "oR", "iL", "iR")}
    for j, y in enumerate(range(y0, y1)):
        runs = runs_in_row(leggings[y], x0, x1)
        if not runs:
            continue
        L["oL"][j], L["oR"][j] = runs[0][0], runs[-1][1]
        if view["type"] == "front":
            big = sorted(sorted(runs, key=lambda r: r[1] - r[0])[-2:])
            if len(big) == 2 and big[1][0] - big[0][1] > 2 and y > view["crotch_y"]:
                L["iL"][j], L["iR"][j] = big[0][1], big[1][0]
    for k in L:
        a = L[k]
        idx = np.arange(n)
        ok = ~np.isnan(a)
        if ok.sum() == 0:
            continue
        a = np.interp(idx, idx[ok], a[ok])
        L[k] = gaussian_filter1d(median_filter(a, 31), 6)
    return L


def arm_runs(skin, view):
    """Cleaned arm/hand skin runs per row inside view["arm_rows"]."""
    a0, a1 = view["arm_rows"]
    S = np.zeros_like(skin)
    S[a0:a1] = skin[a0:a1]
    S = binary_closing(S, iterations=2)
    lab, n = label(S)
    if n:
        sizes = np.bincount(lab.ravel())
        S = np.isin(lab, np.where(sizes >= 80)[0][1:])
    return {y: runs_in_row(S[y], 0, S.shape[1], min_len=6) for y in range(a0, a1)}


def rigid_interp(xs, src, dst, runs, shifts=None):
    """Piecewise-linear map through (src, dst); each arm run moves rigidly, by the base displacement at its centre
    or by the given per-run shift."""
    src, dst = list(src), list(dst)
    for i, (a, b) in enumerate(runs):
        c = (a + b) / 2
        dc = shifts[i] if shifts is not None else np.interp(c, src, dst) - c
        lo, hi = a - 4, b + 4
        keep = [(s_, d_) for s_, d_ in zip(src, dst) if not (lo <= s_ <= hi)]
        keep += [(lo, lo + dc), (hi, hi + dc)]
        keep.sort()
        src, dst = [k[0] for k in keep], [k[1] for k in keep]
    dst = np.maximum.accumulate(np.array(dst, dtype=float))
    return np.interp(xs, src, dst)


def build_forward_map(view, intensity, L, y0, y1, W, arms):
    """Per-row forward displacement (target - source) for x in [0, W)."""
    ys = np.arange(y0, y1)
    prof = view["intensities"][intensity]
    xs = np.arange(W, dtype=float)
    disp = np.zeros((y1 - y0, W))
    rows_sd = []
    margin = view.get("anchor_margin", 220)
    if view["type"] == "front":
        d_out = profile(prof["outer"], ys)
        d_in = profile(prof["inner"], ys)
        xm = view["midline_x"]
        for j in range(len(ys)):
            oL, oR = L["oL"][j], L["oR"][j]
            iL, iR = L["iL"][j], L["iR"][j]
            if np.isnan(iL) or ys[j] <= view["crotch_y"]:
                iL, iR, din = xm - 2, xm + 2, 0.0
            else:
                gap = iR - iL
                din = min(d_in[j], max(gap / 2 - 3, 0))
            cL, cR = (oL + iL) / 2, (iR + oR) / 2
            src = [0, oL - margin, oL, cL, iL, xm, iR, cR, oR, oR + margin, W - 1]
            dst = [0, oL - margin, oL - d_out[j], cL - (d_out[j] - din) / 2, iL + din, xm,
                   iR - din, cR + (d_out[j] - din) / 2, oR + d_out[j], oR + margin, W - 1]
            rows_sd.append((src, dst, xm))
    else:  # three-quarter: front edge = leftmost legging pixel, back edge = rightmost
        d_back = profile(prof["back"], ys)
        d_front = profile(prof["front"], ys)
        for j in range(len(ys)):
            F, Bk = L["oL"][j], L["oR"][j]
            M = (F + Bk) / 2
            src = [0, F - margin, F, M, Bk, Bk + margin, W - 1]
            dst = [0, F - margin, F - d_front[j], M, Bk + d_back[j], Bk + margin, W - 1]
            rows_sd.append((src, dst, M))
    linear = prof.get("arm_mode") == "linear"
    if linear:
        # Straight forearms: per side, shift grows linearly from the elbow row to the wrist row, then stays constant.
        e_y, w_y = view["arm_linear"]["elbow_y"], view["arm_linear"]["wrist_y"]
        ref = {"L": [], "R": []}
        for j, y in enumerate(ys):
            if w_y <= y < w_y + 150:
                src, dst, mid = rows_sd[j]
                for a, b in arms.get(y, []):
                    c = (a + b) / 2
                    ref["L" if c < mid else "R"].append(np.interp(c, src, dst) - c)
        ref = {k: float(np.median(v)) if v else 0.0 for k, v in ref.items()}
    for j, y in enumerate(ys):
        src, dst, mid = rows_sd[j]
        runs = arms.get(y, [])
        shifts = None
        if linear:
            f = float(np.clip((y - e_y) / (w_y - e_y), 0, 1))
            shifts = [ref["L" if (a + b) / 2 < mid else "R"] * f for a, b in runs]
        disp[j] = rigid_interp(xs, src, dst, runs, shifts) - xs
    disp = gaussian_filter(disp, sigma=(6, 2))
    return disp


def warp_image(rgb, disp, y0):
    H, W, _ = rgb.shape
    src_x = np.tile(np.arange(W, dtype=float), (H, 1))
    xs = np.arange(W, dtype=float)
    for j in range(disp.shape[0]):
        fwd = xs + disp[j]
        fwd = np.maximum.accumulate(fwd)  # keep monotonic
        src_x[y0 + j] = np.interp(xs, fwd, xs)
    src_y = np.tile(np.arange(H, dtype=float)[:, None], (1, W))
    out = np.stack([map_coordinates(rgb[..., c].astype(float), [src_y, src_x], order=1, mode="nearest")
                    for c in range(3)], axis=-1)
    return np.clip(out, 0, 255).astype(np.uint8)


def measure(rgb, view):
    leg, _ = masks(rgb)
    x0, x1 = view["search_x"]
    m = {}
    for name, (ya, yb) in view["measure_rows"].items():
        widths, legs = [], []
        for y in range(ya, yb):
            runs = runs_in_row(leg[y], x0, x1)
            if runs:
                widths.append(runs[-1][1] - runs[0][0])
                if view["type"] == "front" and len(runs) >= 2:
                    big = sorted(runs, key=lambda r: r[1] - r[0])[-2:]
                    legs.append(np.mean([b - a for a, b in big]))
        m[name] = {"outer_span_px": int(np.median(widths)) if widths else None}
        if legs:
            m[name]["single_leg_px"] = int(np.median(legs))
    return m


def main():
    exp_dir = (REPO / sys.argv[1]).resolve()
    cfg = json.loads((exp_dir / "warp_config.json").read_text(encoding="utf-8"))
    out_dir = exp_dir / "warp"
    out_dir.mkdir(exist_ok=True)
    report, rows = {}, []
    for vname, view in cfg["views"].items():
        orig = np.asarray(Image.open(REPO / view["source"]).convert("RGB"))
        H, W, _ = orig.shape
        leggings, skin = masks(orig)
        y0, y1 = view["warp_rows"]
        L = landmarks(leggings, view, y0, y1, *view["search_x"])
        arms = arm_runs(skin, view)
        report[vname] = {"source": view["source"], "A": measure(orig, view)}
        tiles = [(orig, f"{vname}: A (original, unchanged)")]
        for inten in view["intensities"]:
            disp = build_forward_map(view, inten, L, y0, y1, W, arms)
            warped = warp_image(orig, disp, y0)
            shifts = [abs(disp[y - y0, int((a + b) / 2)]) for y, rs in arms.items() if y0 <= y < y1 for a, b in rs]
            Image.fromarray(warped).save(out_dir / f"{vname}-{inten}.png")
            changed = np.abs(warped.astype(int) - orig.astype(int)).max(axis=2) > 6
            grey = np.repeat(orig.mean(axis=2, keepdims=True), 3, axis=2).astype(np.uint8)
            grey[changed] = [230, 40, 40]
            Image.fromarray(grey).save(out_dir / f"{vname}-{inten}-diff.png")
            above = changed[: view["waistband_y"]].sum()
            below = changed[view["knee_y"] + 60:].sum()
            report[vname][inten] = measure(warped, view) | {
                "changed_pixels_above_waistband": int(above),
                "changed_pixels_below_knee_plus_60": int(below),
                "max_displacement_px": round(float(np.abs(disp).max()), 1),
                "max_arm_hand_shift_px": round(float(max(shifts)) if shifts else 0.0, 1),
            }
            tiles.append((warped, f"{vname}: {inten}"))
        rows.append(tiles)
    (exp_dir / "warp_measurements.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    tw, th, lh = 560, 835, 34
    ncol = max(len(t) for t in rows)
    sheet = Image.new("RGB", (ncol * tw, len(rows) * (th + lh)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for r, tiles in enumerate(rows):
        for c, (img, lab) in enumerate(tiles):
            sheet.paste(Image.fromarray(img).resize((tw, th), Image.LANCZOS), (c * tw, r * (th + lh)))
            draw.text((c * tw + 10, r * (th + lh) + th + 6), lab, fill="black", font=font)
    sheet.save(exp_dir / "warp_previews.jpg", quality=92)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
