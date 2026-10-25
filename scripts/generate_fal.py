"""Generate images for an experiment on fal.ai and record everything needed to reproduce them.

Usage (from the repo root):
    python scripts/generate_fal.py experiments/001-portrait --seeds 1001-1003 --dry-run
    python scripts/generate_fal.py experiments/001-portrait --seeds 1001-1003
    python scripts/generate_fal.py experiments/001-portrait --contact-sheet-only

Reads FAL_KEY (and optional BACKUP_DIR) from .env. Only the standard library and Pillow are needed.

Per experiment folder:
    config.json        endpoint, params, price, spend cap (input)
    prompt.txt         exact prompt text sent (input)
    runs.jsonl         one line per request: params sent, returned seed, request id, cost, file hash
    images/            original PNGs + raw API responses (git-ignored, mirrored to BACKUP_DIR)
    contact_sheet.jpg  labelled thumbnails of every successful image
    review.csv         one row per seed for scoring

Safety rails: refuses to start if the batch could push recorded spend past the cap, skips seeds already
generated, and stops at the first failed request instead of retrying. The raw API response is saved before the
image is downloaded, so if a download fails, rerunning the same seeds finishes it without paying for a new generation.
"""

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import shutil
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Python's default CA store on this machine rejects fal's image CDN (v3b.fal.media); certifi's bundle works.
try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()
REVIEW_COLUMNS = [
    "seed", "file", "realism_1to5", "skin_texture_1to5", "eyes_1to5", "hair_hairline_1to5",
    "asymmetry_natural_1to5", "matches_brief_1to5", "scar_visible_side", "beauty_mark_visible_side",
    "artifacts", "usable_yes_no", "shortlist_yes_no", "reviewer", "notes",
]


def load_env(path):
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def parse_seeds(spec):
    seeds = []
    for part in spec.split(","):
        if "-" in part:
            lo, hi = part.split("-")
            seeds.extend(range(int(lo), int(hi) + 1))
        else:
            seeds.append(int(part))
    return seeds


def read_ledger(ledger):
    if not ledger.exists():
        return []
    return [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]


def megapixels(width, height):
    return width * height / 1_000_000


def cap_cost(mp, price):
    # Conservative figure for cap checks, in case fal bills per started megapixel.
    return math.ceil(mp) * price


def call_fal(api_url, key, payload):
    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300, context=SSL_CTX) as resp:
        headers = {k.lower(): v for k, v in resp.headers.items() if k.lower().startswith("x-fal")}
        return json.loads(resp.read()), headers


def download(url, dest):
    with urllib.request.urlopen(url, timeout=300, context=SSL_CTX) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def backup(src, exp_dir, backup_root):
    if not backup_root:
        return None
    dest = Path(backup_root) / exp_dir.relative_to(REPO) / "images" / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return str(dest)


def build_contact_sheet(exp_dir, rows):
    from PIL import Image, ImageDraw, ImageFont

    ok = [r for r in rows if r["status"] == "ok" and (exp_dir / r["file"]).exists()]
    if not ok:
        print("No images yet; contact sheet skipped.")
        return
    ok.sort(key=lambda r: r["seed"])
    tw, th, label_h, cols = 384, 512, 36, min(5, len(ok))
    grid_rows = math.ceil(len(ok) / cols)
    sheet = Image.new("RGB", (cols * tw, grid_rows * (th + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for i, r in enumerate(ok):
        x, y = (i % cols) * tw, (i // cols) * (th + label_h)
        img = Image.open(exp_dir / r["file"]).convert("RGB")
        img.thumbnail((tw, th))
        sheet.paste(img, (x + (tw - img.width) // 2, y))
        label = f"seed {r['seed']}" + ("  [SAFETY FLAG]" if r.get("has_nsfw_concepts") else "")
        draw.text((x + 10, y + th + 6), label, fill="black", font=font)
    out = exp_dir / "contact_sheet.jpg"
    sheet.save(out, quality=90)
    print(f"Contact sheet: {out.relative_to(REPO)}")


def update_review_csv(exp_dir, rows):
    path = exp_dir / "review.csv"
    existing = {}
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            existing = {row["seed"]: row for row in csv.DictReader(f)}
    for r in rows:
        if r["status"] == "ok" and str(r["seed"]) not in existing:
            existing[str(r["seed"])] = {c: "" for c in REVIEW_COLUMNS} | {"seed": r["seed"], "file": r["file"]}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        for seed in sorted(existing, key=int):
            writer.writerow(existing[seed])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment", help="experiment folder, e.g. experiments/001-portrait")
    ap.add_argument("--seeds", help="e.g. 1001-1003 or 1001,1005")
    ap.add_argument("--dry-run", action="store_true", help="print requests and costs; send nothing")
    ap.add_argument("--contact-sheet-only", action="store_true")
    args = ap.parse_args()

    exp_dir = (REPO / args.experiment).resolve()
    config = json.loads((exp_dir / "config.json").read_text(encoding="utf-8"))
    prompt = (exp_dir / "prompt.txt").read_text(encoding="utf-8").strip()
    ledger = exp_dir / "runs.jsonl"
    images_dir = exp_dir / "images"
    rows = read_ledger(ledger)

    if args.contact_sheet_only:
        build_contact_sheet(exp_dir, rows)
        update_review_csv(exp_dir, rows)
        return
    if not args.seeds:
        sys.exit("--seeds is required")

    params = config["params"]
    price = config["price_per_megapixel_usd"]
    cap = config["spend_cap_usd"]
    size = params["image_size"]
    mp = megapixels(size["width"], size["height"])

    done = {r["seed"] for r in rows if r["status"] == "ok"}
    todo = [s for s in parse_seeds(args.seeds) if s not in done]
    skipped = sorted(set(parse_seeds(args.seeds)) & done)
    if skipped:
        print(f"Skipping seeds already generated: {skipped}")
    if not todo:
        print("Nothing to generate.")
        return

    spent = sum(r.get("cap_cost_usd", 0) for r in rows if r.get("billed", True))
    # Seeds with a saved response were already billed but never recorded; finishing them costs nothing new.
    pending = [s for s in todo if (images_dir / f"seed-{s}.response.json").exists()]
    spent += len(pending) * cap_cost(mp, price)
    new_requests = [s for s in todo if s not in pending]
    projected = spent + len(new_requests) * cap_cost(mp, price)
    print(f"Endpoint: {config['endpoint']}  size {size['width']}x{size['height']} ({mp:.2f} MP)")
    print(f"Seeds: {todo}" + (f" (finishing already-paid {pending} from saved responses)" if pending else ""))
    print(f"Estimated cost: ${len(new_requests) * mp * price:.4f} "
          f"(conservative ${len(new_requests) * cap_cost(mp, price):.4f}); "
          f"recorded so far ${spent:.4f}; cap ${cap:.2f}")
    if projected > cap:
        sys.exit(f"Refusing: projected spend ${projected:.4f} exceeds cap ${cap:.2f}.")

    if args.dry_run:
        example = {"prompt": prompt[:60] + "...", **params, "seed": todo[0]}
        print("Dry run. First request would be:\n" + json.dumps(example, indent=2))
        return

    env = load_env(REPO / ".env")
    key = os.environ.get("FAL_KEY") or env.get("FAL_KEY")
    if not key:
        sys.exit("FAL_KEY is not set in .env")
    backup_root = os.environ.get("BACKUP_DIR") or env.get("BACKUP_DIR")
    images_dir.mkdir(parents=True, exist_ok=True)

    new_rows = []
    for seed in todo:
        payload = {"prompt": prompt, **params, "seed": seed}
        stem = f"seed-{seed}"
        response_path = images_dir / f"{stem}.response.json"
        recovered = response_path.exists()
        started = (dt.datetime.fromtimestamp(response_path.stat().st_mtime, dt.timezone.utc) if recovered
                   else dt.datetime.now(dt.timezone.utc))
        row = {
            "experiment": config["experiment"], "seed": seed, "endpoint": config["endpoint"],
            "requested_at_utc": started.isoformat(timespec="seconds"),
            "params_sent": {k: v for k, v in payload.items() if k != "prompt"},
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "recovered_from_saved_response": recovered,
        }
        if recovered:
            saved = json.loads(response_path.read_text(encoding="utf-8"))
            result, headers = saved["body"], saved["headers"]
        else:
            try:
                result, headers = call_fal(config["api_url"], key, payload)
            except urllib.error.HTTPError as e:
                row |= {"status": "error", "billed": False, "error": f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}"}
                with ledger.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row) + "\n")
                sys.exit(f"Seed {seed} failed, stopping. {row['error']}")
            response_path.write_text(json.dumps({"headers": headers, "body": result}, indent=2), encoding="utf-8")

        image = result["images"][0]
        w, h = image.get("width") or size["width"], image.get("height") or size["height"]
        out_mp = megapixels(w, h)
        units = headers.get("x-fal-billable-units")
        png = images_dir / f"{stem}.png"
        try:
            if not png.exists():
                download(image["url"], png)
        except urllib.error.URLError as e:
            sys.exit(f"Seed {seed} was generated (and billed) but the download failed: {e}. "
                     "Rerun the same seeds to finish it from the saved response at no extra cost.")
        digest = hashlib.sha256(png.read_bytes()).hexdigest()
        row |= {
            "status": "ok", "billed": True,
            "returned_seed": result.get("seed"),
            "request_id": headers.get("x-fal-request-id"),
            "fal_headers": headers,
            "width": w, "height": h, "megapixels": round(out_mp, 4),
            "billable_units": float(units) if units else None,
            "est_cost_usd": round((float(units) if units else out_mp) * price, 5),
            "cap_cost_usd": round(float(units) * price, 5) if units else cap_cost(out_mp, price),
            "timings": result.get("timings"),
            "has_nsfw_concepts": any(result.get("has_nsfw_concepts") or []),
            "file": f"images/{png.name}", "sha256": digest, "bytes": png.stat().st_size,
            "backup": backup(png, exp_dir, backup_root),
            "seconds_elapsed": None if recovered else round((dt.datetime.now(dt.timezone.utc) - started).total_seconds(), 1),
        }
        with ledger.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
        flag = "  SAFETY FLAG (likely black image)" if row["has_nsfw_concepts"] else ""
        how = " (recovered, no new charge)" if recovered else ""
        print(f"seed {seed}: ok{how}, returned seed {row['returned_seed']}, {w}x{h}, ~${row['est_cost_usd']}{flag}")
        new_rows.append(row)

    all_rows = rows + new_rows
    build_contact_sheet(exp_dir, all_rows)
    update_review_csv(exp_dir, all_rows)
    total = sum(r.get("est_cost_usd", 0) for r in all_rows if r["status"] == "ok")
    print(f"Done. Estimated total spend for this experiment: ${total:.4f}. Confirm actual charges in the fal dashboard.")
    if not backup_root:
        print("WARNING: BACKUP_DIR not set; originals exist only in this folder.")


if __name__ == "__main__":
    main()
