"""Build an input-vs-output sheet: one row per arm, the arm's reference inputs then its output(s).

Usage (from the repo root):
    python scripts/pair_sheet.py experiments/012-niche-test/portfolio

Reads config.json and runs.jsonl from the experiment folder and writes pairs_sheet.jpg there. Needs Pillow.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
TILE, LABEL_H, GAP = 480, 34, 12


def main():
    exp_dir = (REPO / sys.argv[1]).resolve()
    config = json.loads((exp_dir / "config.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in (exp_dir / "runs.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    refs = config["references"]
    sheet_rows = []
    for arm in config["arms"]:
        outs = [r for r in rows if r.get("arm") == arm["name"] and r["status"] == "ok" and (exp_dir / r["file"]).exists()]
        if not outs:
            continue
        tiles = [(REPO / refs[n]["path"], f"INPUT {n}") for n in arm["references"]]
        tiles += [(exp_dir / r["file"], f"OUTPUT {arm['name']} seed {r['seed']}") for r in outs]
        sheet_rows.append(tiles)
    if not sheet_rows:
        sys.exit("No outputs yet.")
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    cols = max(len(t) for t in sheet_rows)
    row_h = TILE + LABEL_H
    sheet = Image.new("RGB", (cols * (TILE + GAP) + GAP, len(sheet_rows) * (row_h + GAP) + GAP), "white")
    draw = ImageDraw.Draw(sheet)
    for i, tiles in enumerate(sheet_rows):
        y = GAP + i * (row_h + GAP)
        # Outputs are right-aligned so every arm's output sits in the same last column.
        start = cols - len(tiles)
        for j, (path, label) in enumerate(tiles):
            col = j if label.startswith("INPUT") else start + j
            x = GAP + col * (TILE + GAP)
            img = Image.open(path).convert("RGB")
            img.thumbnail((TILE, TILE))
            sheet.paste(img, (x + (TILE - img.width) // 2, y + (TILE - img.height) // 2))
            draw.text((x + 6, y + TILE + 6), label, fill="black", font=font)
        if i:
            draw.line((0, y - GAP // 2, sheet.width, y - GAP // 2), fill="#bbbbbb", width=2)
    out = exp_dir / "pairs_sheet.jpg"
    sheet.save(out, quality=90)
    print(f"Pairs sheet: {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
