"""Paste the real product's label/dial back over a generated image, so logos and text are real pixels. Free, local.

Usage (from the repo root):
    python scripts/product_composite.py <reference.jpg> <generated.png> <out.png> --region ellipse:cx,cy,rx,ry
    python scripts/product_composite.py ref.jpg gen.png out.png --region rect:x0,y0,x1,y1 --region rect:...:text
    python scripts/product_composite.py ref.jpg gen.png out.png --region ellipse:... --points rx,ry,gx,gy ... (4+)

Regions are fractions of the reference image's width/height and mark what to transplant (e.g. the cologne label, the
watch dial). A region ending in ":text" transplants only lettering darker than its surroundings (for text printed on
clear glass, where the reference's studio background shows through). Steps:
1. SIFT features of the product (the regions, enlarged) are matched to the generated image (ratio test), and a
   homography is fitted with RANSAC. Too few inliers -> stop: the generated product is at a different angle and a
   flat warp cannot place it, so nothing is written. With --points (pairs of reference/generated positions, as
   fractions of each image), the homography comes from those hand-marked points instead, e.g. four dial index tips.
2. The reference and region mask are warped into the generated frame; the reference colours inside the region are
   shifted toward the generated image's (LAB mean/std, partially) so the paste takes on the new scene's light.
3. The region is blended in with a feathered edge. Every pixel outside the warped region is the generated image's.

Prints JSON: matches, inliers, inlier ratio, warped region area and its share of the frame. Optional --preview writes
generated | composite | 1:1 zooms of the region from both, for review.
"""

import argparse
import json
import sys

import cv2
import numpy as np
from scipy.ndimage import distance_transform_edt


def region_masks(img, regions):
    """Full-paste mask and lettering-only alpha (0..1), both in reference pixels."""
    h, w = img.shape[:2]
    full = np.zeros((h, w), np.uint8)
    text = np.zeros((h, w), np.float32)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    k = max(w // 30, 3) | 1
    # Lettering = pixels clearly darker than the local background (median over a window much wider than a stroke).
    darkness = np.clip((cv2.medianBlur(gray.astype(np.uint8), k).astype(np.float32) - gray - 8) / 40, 0, 1)
    for spec in regions:
        kind, vals, *mode = spec.split(":")
        v = [float(x) for x in vals.split(",")]
        m = np.zeros((h, w), np.uint8)
        if kind == "ellipse":
            cv2.ellipse(m, (round(v[0] * w), round(v[1] * h)), (round(v[2] * w), round(v[3] * h)), 0, 0, 360, 255, -1)
        elif kind == "rect":
            cv2.rectangle(m, (round(v[0] * w), round(v[1] * h)), (round(v[2] * w), round(v[3] * h)), 255, -1)
        else:
            sys.exit(f"unknown region kind {kind}")
        if mode == ["text"]:
            text = np.maximum(text, darkness * (m > 0))
        else:
            full = np.maximum(full, m)
    return full, text


def color_match(src, dst, mask, strength):
    """Shift src's LAB mean/std inside mask toward dst's, by strength (0 = unchanged, 1 = full match)."""
    s = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32)
    d = cv2.cvtColor(dst, cv2.COLOR_BGR2LAB).astype(np.float32)
    sel = mask > 0
    out = s.copy()
    for c in range(3):
        sm, ss = s[..., c][sel].mean(), s[..., c][sel].std() + 1e-6
        dm, ds = d[..., c][sel].mean(), d[..., c][sel].std() + 1e-6
        matched = (s[..., c] - sm) * (ds / ss) + dm
        out[..., c] = s[..., c] + strength * (matched - s[..., c])
    return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("generated")
    ap.add_argument("out")
    ap.add_argument("--region", action="append", required=True)
    ap.add_argument("--feather-px", type=float, default=10)
    ap.add_argument("--color-strength", type=float, default=0.6)
    ap.add_argument("--text-darkness", type=float, default=0.35, help="lettering brightness as a share of the scene's")
    ap.add_argument("--min-inliers", type=int, default=30)
    ap.add_argument("--points", nargs="+", help="rx,ry,gx,gy pairs (fractions); at least 4")
    ap.add_argument("--preview")
    args = ap.parse_args()

    ref = cv2.imread(args.reference)
    gen = cv2.imread(args.generated)
    full, text = region_masks(ref, args.region)
    mask = np.maximum(full, (text > 0).astype(np.uint8) * 255)
    # Match on the product around the region too (case, bezel, bottle edges), not just inside it.
    feat_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=max(ref.shape[:2]) // 25)

    h, w = gen.shape[:2]
    report = {"reference": args.reference, "generated": args.generated}
    if args.points:
        if len(args.points) < 4:
            sys.exit("--points needs at least 4 pairs")
        pts = [[float(x) for x in p.split(",")] for p in args.points]
        rh, rw = ref.shape[:2]
        src = np.float32([[p[0] * rw, p[1] * rh] for p in pts])
        dst = np.float32([[p[2] * w, p[3] * h] for p in pts])
        H, _ = cv2.findHomography(src, dst, 0)
        report |= {"alignment": "manual points", "points": len(pts)}
    else:
        H = match_homography(ref, gen, feat_mask, args.min_inliers, report)
    composite(ref, gen, full, text, H, args, report)


def match_homography(ref, gen, feat_mask, min_inliers, report):
    sift = cv2.SIFT_create(nfeatures=8000)
    kr, dr = sift.detectAndCompute(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY), feat_mask)
    kg, dg = sift.detectAndCompute(cv2.cvtColor(gen, cv2.COLOR_BGR2GRAY), None)
    pairs = cv2.BFMatcher().knnMatch(dr, dg, k=2) if dr is not None and dg is not None else []
    good = [m for m, n in (p for p in pairs if len(p) == 2) if m.distance < 0.75 * n.distance]
    report |= {"alignment": "SIFT + RANSAC", "matches": len(good)}
    if len(good) < 4:
        sys.exit(json.dumps(report | {"status": "failed", "reason": "too few matches"}))
    src = np.float32([kr[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kg[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    H, inl = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    inliers = int(inl.sum()) if inl is not None else 0
    report |= {"inliers": inliers, "inlier_ratio": round(inliers / len(good), 3)}
    if H is None or inliers < min_inliers:
        sys.exit(json.dumps(report | {"status": "failed", "reason": f"fewer than {min_inliers} inliers"}))
    return H


def composite(ref, gen, full, text, H, args, report):
    h, w = gen.shape[:2]
    warped = cv2.warpPerspective(ref, H, (w, h), flags=cv2.INTER_LANCZOS4)
    wmask = cv2.warpPerspective(full, H, (w, h), flags=cv2.INTER_NEAREST)
    wtext = cv2.warpPerspective(text, H, (w, h), flags=cv2.INTER_LINEAR)
    area = int((wmask > 0).sum()) + int((wtext > 0.05).sum())
    report |= {"region_pixels": area, "region_share_of_frame": round(area / (w * h), 4)}
    if area == 0:
        sys.exit(json.dumps(report | {"status": "failed", "reason": "region warped outside the frame"}))

    if (wmask > 0).any():
        warped = color_match(warped, gen, wmask, args.color_strength)
    alpha = (np.clip(distance_transform_edt(wmask > 0) / args.feather_px, 0, 1) * (wmask > 0))[..., None]
    out = alpha * warped + (1 - alpha) * gen
    # Lettering on clear glass: darken the generated pixels in the letter shapes rather than copying the reference's
    # pixels, which carry its studio background's colour.
    t = wtext[..., None]
    out = out * (1 - t * (1 - args.text_darkness))
    inside = (alpha[..., 0] > 0) | (wtext > 0)
    out = out.round().clip(0, 255).astype(np.uint8)
    cv2.imwrite(args.out, out)
    report |= {"status": "ok", "out": args.out, "changed_pixels_outside_region": int(
        (np.abs(out.astype(int) - gen.astype(int)).max(axis=2)[~inside] > 0).sum())}

    if args.preview:
        ys, xs = np.where(inside)
        pad = 40
        y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad, h), max(xs.min() - pad, 0), min(xs.max() + pad, w)
        zg, zo = gen[y0:y1, x0:x1], out[y0:y1, x0:x1]
        th = 900
        def fit(im):
            return cv2.resize(im, (round(im.shape[1] * th / im.shape[0]), th), interpolation=cv2.INTER_AREA)
        sep = np.full((th, 12, 3), 255, np.uint8)
        cv2.imwrite(args.preview, np.hstack([fit(gen), sep, fit(out), sep, fit(zg), sep, fit(zo)]),
                    [cv2.IMWRITE_JPEG_QUALITY, 88])
        report["preview"] = args.preview
    print(json.dumps(report))


if __name__ == "__main__":
    main()
