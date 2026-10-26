"""Experiment 007 realism reconstruction: masks, paid reconstruction calls, compositing and review sheets.

Usage (from the repo root):
    python scripts/reconstruct.py experiments/007-reconstruction masks          # free: build + verify masks
    python scripts/reconstruct.py experiments/007-reconstruction run --dry-run  # free: show requests and cost
    python scripts/reconstruct.py experiments/007-reconstruction run            # paid: R1/R2/R3 per view
    python scripts/reconstruct.py experiments/007-reconstruction report         # free: sheets + measurements

Methods (recon_config.json):
    R1  FLUX.1 Fill [pro] on a lower-body crop with the INTERIOR mask (legging area eroded inside the outline, so the
        silhouette edge is never redrawn); composited back with a feather that ramps only inside the mask.
    R2  Z-Image Turbo image-to-image on the same crop at one documented strength; composited back through the BROAD
        mask, again ramping only inside the mask.
    R3  Nano Banana Pro Edit on the full image, references [target, 2002]; kept as returned (no compositing).
Every pixel outside an R1/R2 compositing region is copied from the target unchanged, and this is verified. Raw API
outputs (crop or full) are kept in raw/; composites in out/. Targets and references are SHA-256-checked.
"""

import base64
import hashlib
import io
import json
import math
import os
import sys
import urllib.error
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes, distance_transform_edt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from body_warp import masks as colour_masks, measure  # noqa: E402
from generate_fal import call_fal, download, load_env, backup  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_rgb(p):
    return np.asarray(Image.open(REPO / p).convert("RGB"))


def data_uri(arr, mode="RGB"):
    buf = io.BytesIO()
    Image.fromarray(arr, mode).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def build_masks(rgb, view, mcfg):
    leg, skin = colour_masks(rgb)
    rows = np.zeros_like(leg)
    r0, r1 = view["mask_rows"]
    rows[r0:r1] = True
    filled = binary_fill_holes(leg) & rows          # fill seams/specks inside the leggings
    hands = binary_dilation(skin, iterations=mcfg["hand_exclusion_dilate_px"])
    interior = binary_erosion(filled, iterations=mcfg["interior_erode_px"]) & ~hands
    broad = binary_dilation(filled, iterations=mcfg["broad_dilate_px"]) & rows & ~hands
    band = filled & ~binary_erosion(filled, iterations=mcfg["interior_erode_px"]) & ~hands
    return {"interior": interior, "broad": broad, "band": band, "skin": skin, "filled": filled}


def ramp_alpha(mask, feather):
    """1 deep inside the mask, ramping to 0 at its boundary; exactly 0 outside."""
    d = distance_transform_edt(mask)
    return np.clip(d / feather, 0, 1) * mask


def cmd_masks(exp, cfg):
    report = {}
    tiles = []
    for vname, view in cfg["views"].items():
        assert sha(REPO / view["target"]) == view["target_sha256"], f"{vname} target hash mismatch"
        rgb = load_rgb(view["target"])
        M = build_masks(rgb, view, cfg["masks"])
        H = rgb.shape[0]
        skin_core = binary_dilation(M["skin"], iterations=2)
        checks = {}
        for name in ("interior", "broad"):
            m = M[name]
            Image.fromarray((m * 255).astype(np.uint8)).save(exp / "masks" / f"{vname}-{name}.png")
            ys = np.where(m)[0]
            checks[name] = {
                "pixels": int(m.sum()), "frame_pct": round(100 * m.mean(), 2),
                "rows": [int(ys.min()), int(ys.max())],
                "overlap_face_upper_body_rows_lt_1000": int(m[:1000].sum()),
                "overlap_waistband_rows_1000_to_mask_start": int(m[1000:view["mask_rows"][0]].sum()),
                "overlap_hands_arms_skin": int((m & skin_core).sum()),
                "within_crop_rows": bool(ys.min() >= view["crop_rows"][0] and ys.max() < view["crop_rows"][1]),
            }
            tint = rgb.copy()
            tint[m] = (0.45 * tint[m] + 0.55 * np.array([255, 60, 200])).astype(np.uint8)
            tiles.append((tint, f"{vname}: {name} mask ({checks[name]['frame_pct']}%)"))
        report[vname] = checks
    (exp / "masks" / "mask_checks.json").write_text(json.dumps(report, indent=2))
    sheet(tiles, exp / "masks_preview.jpg", cols=4)
    print(json.dumps(report, indent=2))


def cost_of(method, mp):
    c = method["cost"]
    return c["usd"] if c["type"] == "per_image" else math.ceil(mp) * c["usd_per_mp"]


def cmd_run(exp, cfg, dry):
    ref = cfg["face_reference"]
    assert sha(REPO / ref["path"]) == ref["sha256"], "2002 hash mismatch"
    ledger = exp / "runs.jsonl"
    rows = [json.loads(l) for l in ledger.read_text().splitlines()] if ledger.exists() else []
    done = {(r["view"], r["method"]) for r in rows if r["status"] == "ok"}
    spent = sum(r.get("cost_usd", 0) for r in rows if r.get("billed"))
    jobs = [(v, m) for v in cfg["views"] for m, meth in cfg["methods"].items()
            if (v, m) not in done and meth.get("enabled", True)]
    est = 0.0
    for v, m in jobs:
        view, meth = cfg["views"][v], cfg["methods"][m]
        mp = (1696 * (view["crop_rows"][1] - view["crop_rows"][0]) / 1e6) if meth["on"] == "crop" else 1696 * 2528 / 1e6
        est += cost_of(meth, mp)
    print(f"Jobs: {jobs}\nEstimated ${est:.2f}; recorded ${spent:.2f}; cap ${cfg['spend_cap_usd']:.2f}")
    if spent + est > cfg["spend_cap_usd"]:
        sys.exit("Refusing: would exceed cap")
    if dry or not jobs:
        return
    env = load_env(REPO / ".env")
    key = os.environ.get("FAL_KEY") or env.get("FAL_KEY")
    backup_root = os.environ.get("BACKUP_DIR") or env.get("BACKUP_DIR")
    face_uri = data_uri(load_rgb(ref["path"]))
    for v, m in jobs:
        view, meth = cfg["views"][v], cfg["methods"][m]
        assert sha(REPO / view["target"]) == view["target_sha256"]
        target = load_rgb(view["target"])
        prompt = (exp / meth["prompt_files"][v]).read_text(encoding="utf-8").strip()
        c0, c1 = view["crop_rows"]
        payload = {"prompt": prompt, **meth["params"], "seed": meth["seed"]}
        if meth["on"] == "crop":
            crop = np.ascontiguousarray(target[c0:c1])
            payload["image_url"] = data_uri(crop)
            if m == "R1":
                mk = np.asarray(Image.open(exp / "masks" / f"{v}-{meth['mask']}.png"))[c0:c1]
                payload["mask_url"] = data_uri(np.ascontiguousarray(mk), "L")
            if m.startswith("R2"):
                payload["image_size"] = {"width": crop.shape[1], "height": crop.shape[0]}
            mp = crop.shape[0] * crop.shape[1] / 1e6
        else:
            payload["image_urls"] = [data_uri(target), face_uri]
            mp = target.shape[0] * target.shape[1] / 1e6
        stem = f"{v}-{m}"
        row = {"view": v, "method": m, "endpoint": meth["endpoint"], "seed_sent": meth["seed"],
               "params_sent": {k: x for k, x in payload.items() if k not in ("prompt", "image_url", "mask_url", "image_urls")},
               "prompt_file": meth["prompt_files"][v], "target_sha256": view["target_sha256"],
               "input": "crop rows %d-%d" % (c0, c1) if meth["on"] == "crop" else "full image + 2002"}
        try:
            result, headers = call_fal(meth["api_url"], key, payload)
        except urllib.error.HTTPError as e:
            row |= {"status": "error", "billed": False, "error": f"HTTP {e.code}: {e.read().decode(errors='replace')[:400]}"}
            with ledger.open("a") as f:
                f.write(json.dumps(row) + "\n")
            sys.exit(f"{stem} failed: {row['error']}")
        (exp / "raw" / f"{stem}.response.json").write_text(json.dumps({"headers": headers, "body": result}, indent=2))
        raw = exp / "raw" / f"{stem}.png"
        download(result["images"][0]["url"], raw)
        with Image.open(raw) as im:
            w, h = im.size
        row |= {"status": "ok", "billed": True, "cost_usd": round(cost_of(meth, mp), 4),
                "returned_seed": result.get("seed"), "request_id": headers.get("x-fal-request-id"),
                "fal_headers": headers, "raw_file": f"raw/{stem}.png", "raw_size": [w, h], "raw_sha256": sha(raw),
                "has_nsfw_concepts": any(result.get("has_nsfw_concepts") or []),
                "backup": backup(raw, exp, backup_root)}
        with ledger.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"{stem}: ok raw {w}x{h} ~${row['cost_usd']}")


def composite(exp, cfg, v, m):
    view, meth = cfg["views"][v], cfg["methods"][m]
    target = load_rgb(view["target"]).astype(float)
    raw = np.asarray(Image.open(exp / "raw" / f"{v}-{m}.png").convert("RGB")).astype(float)
    info = {"raw_size": [raw.shape[1], raw.shape[0]]}
    if meth["on"] == "full":
        info["aligned"] = list(raw.shape[:2]) == list(target.shape[:2])
        return raw.astype(np.uint8), None, info
    c0, c1 = view["crop_rows"]
    want = (c1 - c0, target.shape[1])
    info["expected_crop_size"] = [want[1], want[0]]
    info["aligned"] = raw.shape[:2] == want
    if not info["aligned"]:
        raw = np.asarray(Image.fromarray(raw.astype(np.uint8)).resize((want[1], want[0]), Image.LANCZOS)).astype(float)
        info["resized_to_crop"] = True
    mask = np.asarray(Image.open(exp / "masks" / f"{v}-{meth['mask']}.png")) > 127
    feather = cfg["masks"]["r1_feather_px" if m == "R1" else "r2_feather_px"]
    alpha = ramp_alpha(mask, feather)[..., None]
    full = target.copy()
    full[c0:c1] = raw
    out = alpha * full + (1 - alpha) * target
    return out.round().astype(np.uint8), alpha[..., 0] > 0, info


def font(n):
    try:
        return ImageFont.truetype("arial.ttf", n)
    except OSError:
        return ImageFont.load_default()


def sheet(tiles, path, cols, tw=420, th=626, lh=30):
    n = len(tiles)
    s = Image.new("RGB", (cols * tw, math.ceil(n / cols) * (th + lh)), "white")
    d = ImageDraw.Draw(s)
    for i, (img, lab) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + lh)
        im = Image.fromarray(img) if isinstance(img, np.ndarray) else img
        im = im.copy()
        im.thumbnail((tw, th), Image.LANCZOS)
        s.paste(im, (x + (tw - im.width) // 2, y))
        d.text((x + 6, y + th + 6), lab, fill="black", font=font(16))
    s.save(path, quality=90)


def cmd_report(exp, cfg):
    wcfg = json.loads((REPO / cfg["warp_config"]).read_text())
    ledger = [json.loads(l) for l in (exp / "runs.jsonl").read_text().splitlines()]
    ok = {(r["view"], r["method"]) for r in ledger if r["status"] == "ok"}
    rep, comp_tiles, face_tiles, close_tiles = {}, [], [], []
    face_tiles.append((load_rgb(cfg["face_reference"]["path"])[380:1280, 430:1330], "REF 2002 face"))
    for v, view in cfg["views"].items():
        vw = wcfg["views"][v]
        target = load_rgb(view["target"])
        A = load_rgb(view["version_a"])
        mA, mT = measure(A, vw), measure(target, vw)
        rep[v] = {"version_A": mA, "target": mT}
        comp_tiles += [(A, f"{v}: Version A"), (target, f"{v}: target (B-strong-v2-fixed)")]
        fb = view["face_box"]
        face_tiles.append((target[fb[1]:fb[3], fb[0]:fb[2]], f"{v}: target face"))
        M = build_masks(target, view, cfg["masks"])
        for m in ("R1", "R2", "R2-s045", "R3"):
            if (v, m) not in ok:
                continue
            out, region, info = composite(exp, cfg, v, m)
            Image.fromarray(out).save(exp / "out" / f"{v}-{m}.png")
            r = {"composite_info": info, "measure": measure(out, vw)}
            if region is not None:
                outside = ~region
                r["changed_pixels_outside_region"] = int((np.abs(out.astype(int) - target.astype(int)).max(axis=2)[outside] > 0).sum())
                # seam / band check (R1): luma step across the interior-mask boundary vs the same step in the target
                if m == "R1":
                    inner = M["interior"] & ~binary_erosion(M["interior"], iterations=3)
                    outer = binary_dilation(M["interior"], iterations=3) & ~M["interior"] & M["filled"]
                    lum = lambda x: x.astype(float) @ np.array([0.299, 0.587, 0.114])
                    lo, lt = lum(out), lum(target)
                    r["boundary_luma_step_out"] = round(float(abs(lo[inner].mean() - lo[outer].mean())), 2)
                    r["boundary_luma_step_target"] = round(float(abs(lt[inner].mean() - lt[outer].mean())), 2)
            # retention vs Version A and vs target
            ret = {}
            for k, mv in r["measure"].items():
                for sub in ("outer_span_px", "single_leg_px"):
                    if sub in mv and mv[sub] and mA[k].get(sub):
                        ret[f"{k}.{sub}"] = {"A": mA[k][sub], "target": mT[k].get(sub), "out": mv[sub],
                                             "vs_A_pct": round(100 * (mv[sub] / mA[k][sub] - 1), 1),
                                             "vs_target_pct": round(100 * (mv[sub] / mT[k][sub] - 1), 1) if mT[k].get(sub) else None}
            r["retention"] = ret
            rep[v][m] = r
            comp_tiles.append((out, f"{v}: {m}"))
            face_tiles.append((out[fb[1]:fb[3], fb[0]:fb[2]], f"{v}: {m} face"))
            for cname, (x0, y0, x1, y1) in view["closeups"].items():
                pair = np.concatenate([target[y0:y1, x0:x1], np.full((y1 - y0, 8, 3), 255, np.uint8), out[y0:y1, x0:x1]], axis=1)
                close_tiles.append((pair, f"{v} {cname}: target | {m} (1:1)"))
    (exp / "recon_report.json").write_text(json.dumps(rep, indent=2))
    sheet(comp_tiles, exp / "recon_compare.jpg", cols=5, tw=448, th=668)
    sheet(face_tiles, exp / "recon_face_crops.jpg", cols=5, tw=340, th=340)
    sheet(close_tiles, exp / "recon_closeups.jpg", cols=3, tw=860, th=500)
    print(json.dumps(rep, indent=2))


def main():
    exp = (REPO / sys.argv[1]).resolve()
    cfg = json.loads((exp / "recon_config.json").read_text())
    for d in ("masks", "raw", "out"):
        (exp / d).mkdir(exist_ok=True)
    cmd = sys.argv[2]
    if cmd == "masks":
        cmd_masks(exp, cfg)
    elif cmd == "run":
        cmd_run(exp, cfg, "--dry-run" in sys.argv)
    elif cmd == "report":
        cmd_report(exp, cfg)


if __name__ == "__main__":
    main()
