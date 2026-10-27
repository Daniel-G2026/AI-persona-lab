"""Composite an edited image back into the original only inside a mask, and verify nothing else changed. Free, local.

Usage: python scripts/local_composite.py <original.png> <edited.png> <mask.png> <out.png> [feather_px]

- Sizes must match exactly (no rescaling); otherwise the script stops.
- Alpha = 1 deep inside the mask, ramping to 0 at its edge over feather_px; exactly 0 outside, so every pixel outside
  the mask is copied from the original.
- Prints JSON: changed pixels outside the mask (must be 0), and the mean absolute difference between edited and
  original outside the mask (how much the edit model shifted/re-rendered the rest of the frame; large values mean the
  model did not keep the frame aligned, which makes compositing edges risky).
"""

import json
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt


def main():
    o_p, e_p, m_p, out_p = sys.argv[1:5]
    feather = float(sys.argv[5]) if len(sys.argv) > 5 else 6
    o = np.asarray(Image.open(o_p).convert("RGB")).astype(float)
    e = np.asarray(Image.open(e_p).convert("RGB")).astype(float)
    m = np.asarray(Image.open(m_p).convert("L")) > 127
    if o.shape != e.shape or o.shape[:2] != m.shape:
        sys.exit(json.dumps({"error": "size mismatch", "original": o.shape, "edited": e.shape, "mask": m.shape}))
    alpha = (np.clip(distance_transform_edt(m) / feather, 0, 1) * m)[..., None]
    out = (alpha * e + (1 - alpha) * o).round().astype(np.uint8)
    Image.fromarray(out).save(out_p)
    outside = ~m
    changed_outside = int((np.abs(out.astype(int) - o.astype(int)).max(axis=2)[outside] > 0).sum())
    drift = float(np.abs(e - o).mean(axis=2)[outside].mean())
    inside = float(np.abs(e - o).mean(axis=2)[m].mean())
    print(json.dumps({"out": out_p, "mask_pixels": int(m.sum()), "changed_pixels_outside_mask": changed_outside,
                      "edit_drift_outside_mask_mean_abs": round(drift, 2), "edit_change_inside_mask_mean_abs": round(inside, 2),
                      "feather_px": feather}))


if __name__ == "__main__":
    main()
