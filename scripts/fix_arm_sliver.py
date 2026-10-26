"""Fill thin light slivers trapped between a forearm and the legging edge. Free, local.

Usage: python scripts/fix_arm_sliver.py <input.png> <output.png> [y0 y1] [exclude_x0 exclude_x1]

Light pixels (luma > 170) in rows y0..y1 that vanish under a horizontal morphological opening of width 7 are
"thin": slivers under 7 px wide. Their anti-aliased fringe (luma > 145, horizontally adjacent) is included. Each
thin run on a row is replaced by a linear blend of the pixels just outside it, giving a soft arm/leggings contact; the repaired
strip (plus 2 px) then gets a light vertical blur to remove row-to-row jaggedness.
Wide light areas (background, the real gap between arm and waist) are untouched, as is an optional excluded column
range (e.g. the thigh gap). The input file is never modified. Prints a JSON summary.
"""

import json
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_opening, gaussian_filter


def main():
    src, dst = sys.argv[1], sys.argv[2]
    y0, y1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1000, 1330)
    ex = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (-1, -1)
    img = np.asarray(Image.open(src).convert("RGB")).astype(float)
    luma = img @ np.array([0.299, 0.587, 0.114])
    light = luma > 170
    thin = light & ~binary_opening(light, structure=np.ones((1, 7), bool))
    thin |= binary_dilation(thin, structure=np.ones((1, 3), bool)) & (luma > 145)
    region = np.zeros_like(thin)
    region[y0:y1] = True
    if ex[0] >= 0:
        region[:, ex[0]:ex[1] + 1] = False
    thin &= region
    out = img.copy()
    rows = set()
    for y in np.unique(np.where(thin)[0]):
        xs = np.where(thin[y])[0]
        for run in np.split(xs, np.where(np.diff(xs) > 1)[0] + 1):
            a, b = img[y, run[0] - 1], img[y, run[-1] + 1]
            g = len(run)
            for i, x in enumerate(run):
                t = (i + 1) / (g + 1)
                out[y, x] = (1 - t) * a + t * b
        rows.add(int(y))
    # smooth row-to-row jaggedness inside the repaired strip only
    strip = binary_dilation(thin, iterations=2) & region  # never spill outside the scanned rows/columns
    blurred = gaussian_filter(out, sigma=(1.6, 0.8, 0))
    out[strip] = blurred[strip]
    Image.fromarray(out.round().astype(np.uint8)).save(dst)
    print(json.dumps({"input": src, "output": dst, "rows_scanned": [y0, y1], "excluded_columns": list(ex),
                      "pixels_filled": int(thin.sum()), "pixels_in_smoothed_strip": int((binary_dilation(thin, iterations=2) & region).sum()), "rows_changed": len(rows),
                      "row_range_changed": [min(rows), max(rows)] if rows else None}))


if __name__ == "__main__":
    main()
