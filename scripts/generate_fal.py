"""Generate images for an experiment on fal.ai and record everything needed to reproduce them.

Usage (from the repo root):
    python scripts/generate_fal.py experiments/002-portrait-refine --seeds 2001-2004 --dry-run
    python scripts/generate_fal.py experiments/002-portrait-refine --seeds 2001-2004 [--arms flux2pro]
    python scripts/generate_fal.py experiments/001-portrait --contact-sheet-only

Reads FAL_KEY (and optional BACKUP_DIR) from .env. Needs the standard library, Pillow and certifi.

Per experiment folder:
    config.json        model arm(s), params, prices, spend cap, optional reference image (input)
    prompt.txt         exact prompt text sent (input)
    runs.jsonl         one line per request: params sent, returned seed, request id, actual size, cost, file hash
    images/            original PNGs + raw API responses (git-ignored, mirrored to BACKUP_DIR)
    contact_sheet.jpg  reference (if any) then labelled thumbnails of every successful image
    review.csv         one row per image for scoring

A config either has one model (top-level "endpoint"/"api_url"/"params", as in 001) or several under "arms".
Each seed is run once per arm. Reference images are declared under "references" (name -> path, sha256, label) and
each edit arm lists the ones it sends, in order, as data URIs in image_urls ("reference_image" + "uses_reference"
is the older single-reference form). Every reference's SHA-256 is checked before and after the run so baselines are
provably unchanged. An arm may set its own "prompt_file"; otherwise prompt.txt is used.

Safety rails: refuses to start if the batch could push recorded spend past the cap, skips images already
generated, and stops at the first failed request instead of retrying. The raw API response is saved before the
image is downloaded, so if a download fails, rerunning the same seeds finishes it without paying for a new generation.
"""

import argparse
import base64
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
DEFAULT_REVIEW_COLUMNS = [
    "arm", "seed", "file", "width", "height", "realism_1to5", "skin_texture_1to5", "eyes_1to5",
    "hair_hairline_1to5", "asymmetry_natural_1to5", "matches_brief_1to5", "scar_visible_side",
    "beauty_mark_visible_side", "artifacts", "usable_yes_no", "shortlist_yes_no", "reviewer", "notes",
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


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def megapixels(width, height):
    return width * height / 1_000_000


def arms_of(config):
    if "arms" in config:
        return config["arms"]
    # Single-model config (Experiment 001 layout): one unnamed arm billed per megapixel.
    return [{
        "name": "", "endpoint": config["endpoint"], "api_url": config["api_url"], "params": config["params"],
        "cost": {"type": "per_megapixel", "usd_per_mp": config["price_per_megapixel_usd"]},
    }]


def arm_cost(arm, out_mp, in_mp=0.0, billable_units=None):
    """Conservative cost of one image, rounding megapixels up as fal does."""
    c = arm["cost"]
    if c["type"] == "per_image":
        return c["usd"]
    if c["type"] == "per_megapixel":
        units = billable_units if billable_units is not None else math.ceil(out_mp)
        return units * c["usd_per_mp"]
    if c["type"] == "first_mp_plus_extra":
        # FLUX.2 [pro] edit: first output MP, then each extra MP of output and of input, each rounded up.
        return c["first_mp_usd"] + c["extra_mp_usd"] * (max(math.ceil(out_mp) - 1, 0) + math.ceil(in_mp))
    raise ValueError(f"unknown cost type {c['type']}")


def expected_out_mp(arm):
    if "expected_output" in arm:
        return megapixels(arm["expected_output"]["width"], arm["expected_output"]["height"])
    size = arm["params"].get("image_size")
    return megapixels(size["width"], size["height"]) if isinstance(size, dict) else 1.0


def references_of(config):
    if "references" in config:
        return config["references"]
    if "reference_image" in config:
        return {"ref": config["reference_image"]}
    return {}


def arm_refs(arm, config):
    if "references" in arm:
        return arm["references"]
    return ["ref"] if arm.get("uses_reference") and "reference_image" in config else []


def stem_for(arm_name, seed):
    return f"{arm_name}-seed-{seed}" if arm_name else f"seed-{seed}"


def call_fal(api_url, key, payload):
    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600, context=SSL_CTX) as resp:
        headers = {k.lower(): v for k, v in resp.headers.items() if k.lower().startswith("x-fal")}
        return json.loads(resp.read()), headers


def download(url, dest):
    with urllib.request.urlopen(url, timeout=300, context=SSL_CTX) as resp:
        dest.write_bytes(resp.read())


def backup(src, exp_dir, backup_root):
    if not backup_root:
        return None
    dest = Path(backup_root) / exp_dir.relative_to(REPO) / "images" / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return str(dest)


def build_contact_sheet(exp_dir, config, rows):
    from PIL import Image, ImageDraw, ImageFont

    tiles = []
    for ref in references_of(config).values():
        tiles.append((REPO / ref["path"], ref.get("label", "REFERENCE")))
    ok = sorted((r for r in rows if r["status"] == "ok" and (exp_dir / r["file"]).exists()),
                key=lambda r: (r.get("arm", ""), r["seed"]))
    for r in ok:
        label = (f"{r['arm']} " if r.get("arm") else "") + f"seed {r['seed']}"
        if r.get("has_nsfw_concepts"):
            label += "  [SAFETY FLAG]"
        tiles.append((exp_dir / r["file"], label))
    if not ok:
        print("No images yet; contact sheet skipped.")
        return
    tw, th, label_h = 384, 512, 36
    cols = min(len(tiles), 5)
    grid_rows = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * tw, grid_rows * (th + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for i, (path, label) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + label_h)
        img = Image.open(path).convert("RGB")
        img.thumbnail((tw, th))
        sheet.paste(img, (x + (tw - img.width) // 2, y))
        draw.text((x + 10, y + th + 6), label, fill="black", font=font)
    out = exp_dir / "contact_sheet.jpg"
    sheet.save(out, quality=90)
    print(f"Contact sheet: {out.relative_to(REPO)}")


def update_review_csv(exp_dir, config, rows):
    columns = config.get("review_columns", DEFAULT_REVIEW_COLUMNS)
    path = exp_dir / "review.csv"
    existing = {}
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            existing = {(row.get("arm", ""), row["seed"]): row for row in csv.DictReader(f)}
    for r in rows:
        k = (r.get("arm", ""), str(r["seed"]))
        if r["status"] == "ok" and k not in existing:
            prefill = {"arm": r.get("arm", ""), "seed": r["seed"], "file": r["file"],
                       "width": r.get("width"), "height": r.get("height")}
            existing[k] = {c: prefill.get(c, "") for c in columns}
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for k in sorted(existing, key=lambda k: (k[0], int(k[1]))):
            writer.writerow(existing[k])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment", help="experiment folder, e.g. experiments/002-portrait-refine")
    ap.add_argument("--seeds", help="e.g. 2001-2004 or 2001,2003")
    ap.add_argument("--arms", help="comma-separated arm names to run (default: all)")
    ap.add_argument("--dry-run", action="store_true", help="print requests and costs; send nothing")
    ap.add_argument("--contact-sheet-only", action="store_true")
    args = ap.parse_args()

    exp_dir = (REPO / args.experiment).resolve()
    config = json.loads((exp_dir / "config.json").read_text(encoding="utf-8"))
    default_prompt_file = config.get("prompt_file", "prompt.txt")
    ledger = exp_dir / "runs.jsonl"
    images_dir = exp_dir / "images"
    rows = read_ledger(ledger)

    if args.contact_sheet_only:
        build_contact_sheet(exp_dir, config, rows)
        update_review_csv(exp_dir, config, rows)
        return
    if not args.seeds:
        sys.exit("--seeds is required")

    arms = arms_of(config)
    if args.arms:
        wanted = args.arms.split(",")
        arms = [a for a in arms if a["name"] in wanted]
        if not arms:
            sys.exit(f"No arms named {wanted}")

    refs = references_of(config)
    ref_mp = {}
    for name, ref in refs.items():
        if sha256_file(REPO / ref["path"]) != ref["sha256"]:
            sys.exit(f"Reference image {ref['path']} does not match its recorded SHA-256; refusing to run.")
        from PIL import Image
        with Image.open(REPO / ref["path"]) as im:
            ref_mp[name] = megapixels(*im.size)
    prompts = {a["name"]: (exp_dir / a.get("prompt_file", default_prompt_file)).read_text(encoding="utf-8").strip()
               for a in arms}

    def in_mp_for(a):
        return sum(ref_mp[n] for n in arm_refs(a, config))

    cap = config["spend_cap_usd"]
    done = {(r.get("arm", ""), r["seed"]) for r in rows if r["status"] == "ok"}
    jobs = [(a, s) for a in arms for s in parse_seeds(args.seeds) if (a["name"], s) not in done]
    skipped = [(a["name"], s) for a in arms for s in parse_seeds(args.seeds) if (a["name"], s) in done]
    if skipped:
        print(f"Skipping images already generated: {skipped}")
    if not jobs:
        print("Nothing to generate.")
        return

    def job_cost(a):
        return arm_cost(a, expected_out_mp(a), in_mp_for(a))

    spent = sum(r.get("cap_cost_usd", 0) for r in rows if r.get("billed", True))
    # Images with a saved response were already billed but never recorded; finishing them costs nothing new.
    pending = [(a, s) for a, s in jobs if (images_dir / f"{stem_for(a['name'], s)}.response.json").exists()]
    spent += sum(job_cost(a) for a, _ in pending)
    new_jobs = [j for j in jobs if j not in pending]
    projected = spent + sum(job_cost(a) for a, _ in new_jobs)
    for a in arms:
        n = sum(1 for j in new_jobs if j[0] is a)
        print(f"[{a['name'] or 'default'}] {a['endpoint']}: {n} new image(s) x ~${job_cost(a):.3f}")
    if pending:
        print(f"Finishing already-paid images from saved responses: {[(a['name'], s) for a, s in pending]}")
    print(f"Conservative new cost ${projected - spent:.3f}; recorded so far ${spent:.3f}; "
          f"projected ${projected:.3f}; cap ${cap:.2f}")
    if projected > cap:
        sys.exit(f"Refusing: projected spend ${projected:.4f} exceeds cap ${cap:.2f}.")

    ref_uri = {n: "data:image/png;base64," + base64.b64encode((REPO / r["path"]).read_bytes()).decode()
               for n, r in refs.items()}

    def payload_for(arm, seed):
        p = {"prompt": prompts[arm["name"]], **arm["params"], "seed": seed}
        if arm_refs(arm, config):
            p["image_urls"] = [ref_uri[n] for n in arm_refs(arm, config)]
        return p

    def loggable(payload, arm):
        return {k: ([f"<reference:{n}>" for n in arm_refs(arm, config)] if k == "image_urls" else v)
                for k, v in payload.items() if k != "prompt"}

    if args.dry_run:
        a, s = jobs[0]
        example = {"prompt": prompts[a["name"]][:60] + "...", **loggable(payload_for(a, s), a)}
        print(f"Dry run. First request ({a['api_url']}) would be:\n" + json.dumps(example, indent=2))
        return

    env = load_env(REPO / ".env")
    key = os.environ.get("FAL_KEY") or env.get("FAL_KEY")
    if not key:
        sys.exit("FAL_KEY is not set in .env")
    backup_root = os.environ.get("BACKUP_DIR") or env.get("BACKUP_DIR")
    images_dir.mkdir(parents=True, exist_ok=True)

    from PIL import Image
    new_rows = []
    for arm, seed in jobs:
        payload = payload_for(arm, seed)
        stem = stem_for(arm["name"], seed)
        response_path = images_dir / f"{stem}.response.json"
        recovered = response_path.exists()
        started = (dt.datetime.fromtimestamp(response_path.stat().st_mtime, dt.timezone.utc) if recovered
                   else dt.datetime.now(dt.timezone.utc))
        row = {
            "experiment": config["experiment"], "arm": arm["name"], "seed": seed, "endpoint": arm["endpoint"],
            "requested_at_utc": started.isoformat(timespec="seconds"),
            "params_sent": loggable(payload, arm),
            "prompt_file": arm.get("prompt_file", default_prompt_file),
            "prompt_sha256": hashlib.sha256(prompts[arm["name"]].encode()).hexdigest(),
            "references": [{"name": n, "path": refs[n]["path"], "sha256": refs[n]["sha256"]} for n in arm_refs(arm, config)],
            "recovered_from_saved_response": recovered,
        }
        if recovered:
            saved = json.loads(response_path.read_text(encoding="utf-8"))
            result, headers = saved["body"], saved["headers"]
        else:
            try:
                result, headers = call_fal(arm["api_url"], key, payload)
            except urllib.error.HTTPError as e:
                row |= {"status": "error", "billed": False, "error": f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}"}
                with ledger.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row) + "\n")
                sys.exit(f"{stem} failed, stopping. {row['error']}")
            response_path.write_text(json.dumps({"headers": headers, "body": result}, indent=2), encoding="utf-8")

        image = result["images"][0]
        ext = {"image/jpeg": "jpg", "image/webp": "webp"}.get(image.get("content_type"), "png")
        out = images_dir / f"{stem}.{ext}"
        try:
            if not out.exists():
                download(image["url"], out)
        except urllib.error.URLError as e:
            sys.exit(f"{stem} was generated (and billed) but the download failed: {e}. "
                     "Rerun the same seeds to finish it from the saved response at no extra cost.")
        with Image.open(out) as im:
            w, h = im.size  # actual pixels, not what was requested
        units = headers.get("x-fal-billable-units")
        units = float(units) if units else None
        cost = arm_cost(arm, megapixels(w, h), in_mp_for(arm),
                        units if arm["cost"]["type"] == "per_megapixel" else None)
        row |= {
            "status": "ok", "billed": True,
            "returned_seed": result.get("seed"),
            "request_id": headers.get("x-fal-request-id"),
            "fal_headers": headers,
            "width": w, "height": h, "megapixels": round(megapixels(w, h), 4),
            "billable_units": units,
            "est_cost_usd": round(cost, 5),
            "cap_cost_usd": round(cost, 5),
            "timings": result.get("timings"),
            "has_nsfw_concepts": any(result.get("has_nsfw_concepts") or []),
            "model_description": result.get("description"),
            "file": f"images/{out.name}", "sha256": sha256_file(out), "bytes": out.stat().st_size,
            "backup": backup(out, exp_dir, backup_root),
            "seconds_elapsed": None if recovered else round((dt.datetime.now(dt.timezone.utc) - started).total_seconds(), 1),
        }
        with ledger.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
        how = " (recovered, no new charge)" if recovered else ""
        flag = "  SAFETY FLAG (likely black image)" if row["has_nsfw_concepts"] else ""
        print(f"{stem}: ok{how}, returned seed {row['returned_seed']}, {w}x{h}, ~${row['est_cost_usd']}{flag}")
        new_rows.append(row)

    for ref in refs.values():
        if sha256_file(REPO / ref["path"]) != ref["sha256"]:
            print(f"WARNING: reference image {ref['path']} changed during the run!")
    all_rows = rows + new_rows
    build_contact_sheet(exp_dir, config, all_rows)
    update_review_csv(exp_dir, config, all_rows)
    total = sum(r.get("est_cost_usd", 0) for r in all_rows if r["status"] == "ok")
    print(f"Done. Estimated total spend for this experiment: ${total:.4f}. Confirm actual charges in the fal dashboard.")
    if not backup_root:
        print("WARNING: BACKUP_DIR not set; originals exist only in this folder.")


if __name__ == "__main__":
    main()
