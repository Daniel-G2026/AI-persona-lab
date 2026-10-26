"""Free, local "phone pass": make a generated still look like it went through a phone camera + Instagram upload.

Usage: python scripts/phone_pass.py <input.png> <output.png> [seed]

Steps (fixed, documented settings; deterministic for a given seed):
  1. centre-crop to 9:16 and resize to 1080x1920 (Instagram's vertical size), Lanczos
  2. mild phone-style sharpening (unsharp mask radius 1.2, 60 %, threshold 2)
  3. luminance sensor noise, stronger in shadows (sigma 1.0 in highlights rising to 4.0 in deep shadows)
  4. JPEG round-trip at quality 82 with 4:2:0 chroma subsampling (typical phone/Instagram compression)
The result is saved as PNG (lossless container) so blind reviewers can't tell variants apart by file type.
This is an experimental variant only; it is not assumed to improve realism.
"""

import io
import sys

import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1920
SETTINGS = {"size": [W, H], "unsharp": {"radius": 1.2, "percent": 60, "threshold": 2},
            "noise_sigma_highlight": 1.0, "noise_sigma_shadow": 4.0, "jpeg_quality": 82, "subsampling": "4:2:0"}


def fit_9x16(im, w=W, h=H):
    sw, sh = im.size
    target = w / h
    if sw / sh > target:
        nw = round(sh * target)
        im = im.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else:
        nh = round(sw / target)
        im = im.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


def phone_pass(im, seed=0):
    im = fit_9x16(im.convert("RGB"))
    u = SETTINGS["unsharp"]
    im = im.filter(ImageFilter.UnsharpMask(radius=u["radius"], percent=u["percent"], threshold=u["threshold"]))
    a = np.asarray(im).astype(float)
    luma = a @ np.array([0.299, 0.587, 0.114])
    sig = SETTINGS["noise_sigma_highlight"] + (SETTINGS["noise_sigma_shadow"] - SETTINGS["noise_sigma_highlight"]) * (1 - luma / 255.0) ** 1.5
    rng = np.random.default_rng(seed)
    a = np.clip(a + (rng.standard_normal(luma.shape) * sig)[..., None], 0, 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, format="JPEG", quality=SETTINGS["jpeg_quality"], subsampling=2)
    return Image.open(io.BytesIO(buf.getvalue())).convert("RGB")


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    phone_pass(Image.open(src), seed).save(dst)
