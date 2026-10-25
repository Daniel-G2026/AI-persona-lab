"""Build a face-crop comparison sheet from manually chosen boxes.

Usage: python scripts/face_crop_sheet.py experiments/003-full-body

Reads <experiment>/face_crops.json ({"references": {name: box}, "images": {file: box}}, boxes as x0,y0,x1,y1 in
original pixels) and the reference paths from config.json, then writes face_crops.jpg: references first, then each
image's face, all shown at the same size and labelled with the true crop size. Upscaling is for viewing only.
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
TILE, LABEL_H, COLS = 420, 52, 5


def main():
    exp_dir = (REPO / sys.argv[1]).resolve()
    config = json.loads((exp_dir / "config.json").read_text(encoding="utf-8"))
    crops = json.loads((exp_dir / "face_crops.json").read_text(encoding="utf-8"))
    tiles = []
    for name, box in crops.get("references", {}).items():
        ref = config["references"][name]
        tiles.append((REPO / ref["path"], box, ref.get("label", name)))
    for file, box in crops["images"].items():
        tiles.append((exp_dir / "images" / file, box, Path(file).stem))
    sheet = Image.new("RGB", (COLS * TILE, math.ceil(len(tiles) / COLS) * (TILE + LABEL_H)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (path, box, label) in enumerate(tiles):
        x, y = (i % COLS) * TILE, (i // COLS) * (TILE + LABEL_H)
        crop = Image.open(path).convert("RGB").crop(tuple(box))
        sheet.paste(crop.resize((TILE, TILE), Image.LANCZOS), (x, y))
        draw.text((x + 8, y + TILE + 4), label, fill="black", font=font)
        draw.text((x + 8, y + TILE + 26), f"source {box[2] - box[0]}x{box[3] - box[1]} px", fill="gray", font=font)
    out = exp_dir / "face_crops.jpg"
    sheet.save(out, quality=92)
    print(f"Face-crop sheet: {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
