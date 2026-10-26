"""Build a blind review set for Experiment 009: originals vs phone-pass variants under random codes.

Usage: python scripts/blind_set.py experiments/009-realism-video

For every generated still (images/*.png) it writes:
    variants/original/<stem>.png    the original, centre-cropped/resized to 1080x1920 only (same display size as
                                    the phone pass; no other processing)
    variants/phone/<stem>.png       scripts/phone_pass.py output
Then it shuffles all variants with a fixed random seed, gives each a code (e.g. K7), and writes:
    blind/<code>.png                identical-looking files, same size and format
    blind_sheet.jpg                 all codes in shuffled order, labels = code only
    blind_key.json                  code -> still + variant (git-ignored; only its SHA-256 is committed, in
                                    blind_key.sha256, so the key can't be peeked at in the repo or changed later)
Originals at full resolution stay untouched in images/.
"""

import hashlib
import json
import random
import string
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phone_pass import fit_9x16, phone_pass, SETTINGS  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def main():
    exp = (REPO / sys.argv[1]).resolve()
    stills = sorted(p for p in (exp / "images").glob("*.png"))
    for d in ("variants/original", "variants/phone", "blind"):
        (exp / d).mkdir(parents=True, exist_ok=True)
    items = []
    for i, p in enumerate(stills):
        im = Image.open(p)
        o = exp / "variants/original" / p.name
        f = exp / "variants/phone" / p.name
        fit_9x16(im.convert("RGB")).save(o)
        phone_pass(im, seed=1000 + i).save(f)
        items += [(p.stem, "original", o), (p.stem, "phone", f)]
    rng = random.Random(90091)
    rng.shuffle(items)
    codes = set()
    key = {}
    tiles = []
    for stem, var, path in items:
        while True:
            c = rng.choice(string.ascii_uppercase.replace("O", "").replace("I", "")) + str(rng.randint(2, 9))
            if c not in codes:
                codes.add(c)
                break
        Image.open(path).save(exp / "blind" / f"{c}.png")
        key[c] = {"still": stem, "variant": var}
        tiles.append((exp / "blind" / f"{c}.png", c))
    key_bytes = json.dumps({"phone_pass_settings": SETTINGS, "codes": key}, indent=2).encode()
    (exp / "blind_key.json").write_bytes(key_bytes)
    (exp / "blind_key.sha256").write_text(hashlib.sha256(key_bytes).hexdigest() + "  blind_key.json\n")
    tw, th, lh, cols = 405, 720, 40, 4
    sheet = Image.new("RGB", (cols * tw, -(-len(tiles) // cols) * (th + lh)), "white")
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arialbd.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    for i, (p, c) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + lh)
        sheet.paste(Image.open(p).resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + 10, y + th + 6), c, fill="black", font=font)
    sheet.save(exp / "blind_sheet.jpg", quality=95)
    print("codes:", [c for _, c in tiles])


if __name__ == "__main__":
    main()
