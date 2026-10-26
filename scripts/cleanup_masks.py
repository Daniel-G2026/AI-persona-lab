"""Draft cleanup masks for warped previews (white = area a fill model may redraw). Free, local.

Usage: python scripts/cleanup_masks.py experiments/006-body-control

For each warp/<view>-<intensity>.png it writes:
    -mask-narrow.png  band of about +/-25 px along the new legging outline (and inner-thigh contours): fixes edges only
    -mask-broad.png   the whole legging area from just below the waistband to just below the knee, plus a margin
                      outside the outline: lets the model re-render fabric tension, folds and shading across the thighs
Hands and arms are excluded from both, and nothing above the waistband is ever included.
Also writes cleanup_masks_preview.jpg (masks tinted over each image).
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import binary_dilation, binary_erosion

sys.path.insert(0, str(Path(__file__).resolve().parent))
from body_warp import masks  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def main():
    exp_dir = (REPO / sys.argv[1]).resolve()
    cfg = json.loads((exp_dir / "warp_config.json").read_text(encoding="utf-8"))
    tiles = []
    for vname, view in cfg["views"].items():
        for inten in view["intensities"]:
            img = np.asarray(Image.open(exp_dir / "warp" / f"{vname}-{inten}.png").convert("RGB"))
            leg, skin = masks(img)
            rows = np.zeros_like(leg)
            rows[view["waistband_y"] + 15: view["knee_y"] + 60] = True
            hands = binary_dilation(skin, iterations=6)
            leg_r = leg & rows
            narrow = (binary_dilation(leg_r, iterations=25) & ~binary_erosion(leg_r, iterations=25)) & rows & ~hands
            broad = binary_dilation(leg_r, iterations=20) & rows & ~hands
            for name, m in (("narrow", narrow), ("broad", broad)):
                Image.fromarray((m * 255).astype(np.uint8)).save(exp_dir / "warp" / f"{vname}-{inten}-mask-{name}.png")
                tint = img.copy()
                tint[m] = (0.45 * tint[m] + 0.55 * np.array([255, 60, 200])).astype(np.uint8)
                tiles.append((tint, f"{vname} {inten}: {name} mask ({m.mean() * 100:.1f}% of frame)"))
    tw, th, lh, cols = 420, 626, 30, 4
    sheet = Image.new("RGB", (cols * tw, -(-len(tiles) // cols) * (th + lh)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    for i, (img, lab) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + lh)
        sheet.paste(Image.fromarray(img).resize((tw, th), Image.LANCZOS), (x, y))
        draw.text((x + 6, y + th + 6), lab, fill="black", font=font)
    sheet.save(exp_dir / "cleanup_masks_preview.jpg", quality=90)
    print("ok")


if __name__ == "__main__":
    main()
