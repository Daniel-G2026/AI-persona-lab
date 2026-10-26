"""Build an A/B side-by-side sheet from the "pairs" in an experiment's config.json.

Usage: python scripts/ab_sheet.py experiments/005-body-ab

Each pair names its A and B side as an arm name or "ref:<reference name>". A reference side is one fixed image,
shown next to every generated image of the other side. Two arm sides are matched by seed, one row per seed.
All images are shown at the same scale, A on the left, labelled with version, view, method and seed.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
W, H, LABEL_H, TITLE_H = 420, 626, 30, 34


def main():
    exp_dir = (REPO / sys.argv[1]).resolve()
    config = json.loads((exp_dir / "config.json").read_text(encoding="utf-8"))
    arms = {a["name"]: a for a in config["arms"]}
    rows = [json.loads(l) for l in (exp_dir / "runs.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    ok = {}
    for r in rows:
        if r["status"] == "ok":
            ok.setdefault(r["arm"], {})[r["seed"]] = exp_dir / r["file"]

    def label(side, seed=None):
        if side.startswith("ref:"):
            ref = config["references"][side[4:]]
            return f"A  {ref.get('label', side[4:])}"
        a = arms[side]
        return f"{a['version']}  {a['view']}  {a['method']}  seed {seed}"

    lines = []  # (title, [(path, label), ...])
    for pair in config["pairs"]:
        A, B = pair["A"], pair["B"]
        if A.startswith("ref:"):
            tiles = [(REPO / config["references"][A[4:]]["path"], label(A))]
            tiles += [(p, label(B, s)) for s, p in sorted(ok.get(B, {}).items())]
            if len(tiles) > 1:
                lines.append((pair["name"], tiles))
        else:
            for s in sorted(set(ok.get(A, {})) & set(ok.get(B, {}))):
                lines.append((f"{pair['name']} (seed {s})", [(ok[A][s], label(A, s)), (ok[B][s], label(B, s))]))
    if not lines:
        sys.exit("No complete pairs yet.")

    cols = max(len(t) for _, t in lines)
    sheet = Image.new("RGB", (cols * W, len(lines) * (TITLE_H + H + LABEL_H)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font, bold = ImageFont.truetype("arial.ttf", 18), ImageFont.truetype("arialbd.ttf", 22)
    except OSError:
        font = bold = ImageFont.load_default()
    y = 0
    for title, tiles in lines:
        draw.text((10, y + 6), title, fill="black", font=bold)
        y += TITLE_H
        for i, (path, lab) in enumerate(tiles):
            img = Image.open(path).convert("RGB")
            img.thumbnail((W, H), Image.LANCZOS)
            sheet.paste(img, (i * W + (W - img.width) // 2, y))
            draw.text((i * W + 8, y + H + 5), lab, fill="black", font=font)
        y += H + LABEL_H
    out = exp_dir / "ab_pairs.jpg"
    sheet.save(out, quality=90)
    print(f"A/B sheet: {out.relative_to(REPO)} ({len(lines)} rows)")


if __name__ == "__main__":
    main()
