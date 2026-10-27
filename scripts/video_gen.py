"""Image-to-video generation on fal via the queue API, with a ledger. Paid; use --dry-run first.

Usage: python scripts/video_gen.py experiments/011-pipeline-benchmark/partA [--only A1] [--dry-run]

Reads <dir>/video_config.json: inputs (start frame and element images, each hash-checked), and clips (endpoint,
params, prompt file, cost). Images are sent as data URIs (JPEG q95 for size). Each clip is submitted to
https://queue.fal.run/<endpoint>, polled until done, and the raw MP4 plus the API response are saved to <dir>/raw/.
Ledger: <dir>/runs.jsonl. Refuses to run if the estimated cost would exceed the cap. Raw videos are mirrored to BACKUP_DIR.
"""

import base64
import hashlib
import io
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_fal import SSL_CTX, load_env, backup  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jpeg_uri(path, box=None, max_side=None):
    im = Image.open(REPO / path).convert("RGB")
    if box:
        im = im.crop(tuple(box))
    if max_side and max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=95)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), list(im.size)


def http(url, key, data=None, method="GET"):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, method=method,
                                 headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        return json.loads(r.read())


def main():
    d = (REPO / sys.argv[1]).resolve()
    cfg = json.loads((d / "video_config.json").read_text(encoding="utf-8"))
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    dry = "--dry-run" in sys.argv
    for name, inp in cfg["inputs"].items():
        assert sha(REPO / inp["path"]) == inp["sha256"], f"input {name} hash mismatch"
    ledger = d / "runs.jsonl"
    rows = [json.loads(l) for l in ledger.read_text().splitlines()] if ledger.exists() else []
    done = {r["clip"] for r in rows if r["status"] == "ok"}
    spent = sum(r.get("cost_usd", 0) for r in rows if r.get("billed"))
    clips = [c for c in cfg["clips"] if (only is None or c["name"] == only) and c["name"] not in done]
    est = sum(c["cost"]["usd_per_s"] * c["params"]["duration_s"] for c in clips)
    print(f"Clips: {[c['name'] for c in clips]} | est ${est:.2f} | recorded ${spent:.2f} | cap ${cfg['spend_cap_usd']:.2f}")
    if spent + est > cfg["spend_cap_usd"]:
        sys.exit("Refusing: would exceed cap")
    env = load_env(REPO / ".env")
    key = os.environ.get("FAL_KEY") or env.get("FAL_KEY")
    (d / "raw").mkdir(exist_ok=True)
    for c in clips:
        prompt = (d / c["prompt_file"]).read_text(encoding="utf-8").strip()
        start_uri, start_size = jpeg_uri(cfg["inputs"][c["start"]]["path"], max_side=cfg.get("start_max_side", 1920))
        payload = {"prompt": prompt, c["start_param"]: start_uri, **c["api_params"]}
        sent = {k: v for k, v in payload.items() if k not in ("prompt", c["start_param"])}
        if c.get("elements"):
            els = []
            for e in c["elements"]:
                fu, _ = jpeg_uri(cfg["inputs"][e["frontal"]]["path"], e.get("frontal_box"), 1536)
                refs = [jpeg_uri(cfg["inputs"][r["input"]]["path"], r.get("box"), 1536)[0] for r in e["references"]]
                els.append({"frontal_image_url": fu, "reference_image_urls": refs})
            payload["elements"] = els
            sent["elements"] = [{"frontal": e["frontal"], "references": [r["input"] + (f" crop {r['box']}" if r.get("box") else "") for r in e["references"]]} for e in c["elements"]]
        print(f"[{c['name']}] {c['endpoint']} start {start_size} params {json.dumps(sent)}")
        if dry:
            continue
        sub = http(f"https://queue.fal.run/{c['endpoint']}", key, payload, "POST")
        rid, status_url, resp_url = sub["request_id"], sub["status_url"], sub["response_url"]
        t0 = time.time()
        while True:
            st = http(status_url, key)
            if st.get("status") == "COMPLETED":
                break
            if time.time() - t0 > 1500:
                sys.exit(f"{c['name']}: timed out waiting (request {rid}); result can be fetched later from {resp_url}")
            time.sleep(10)
        res = http(resp_url, key)
        (d / "raw" / f"{c['name']}.response.json").write_text(json.dumps(res, indent=2))
        url = res["video"]["url"]
        out = d / "raw" / f"{c['name']}.mp4"
        with urllib.request.urlopen(url, timeout=300, context=SSL_CTX) as r:
            out.write_bytes(r.read())
        row = {"clip": c["name"], "endpoint": c["endpoint"], "request_id": rid, "status": "ok", "billed": True,
               "cost_usd": round(c["cost"]["usd_per_s"] * c["params"]["duration_s"], 3), "params_sent": sent,
               "start_input": c["start"], "start_sent_size": start_size, "prompt_file": c["prompt_file"],
               "seconds_waited": round(time.time() - t0), "file": f"raw/{out.name}", "sha256": sha(out),
               "bytes": out.stat().st_size, "backup": backup(out, d, env.get("BACKUP_DIR"))}
        with ledger.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"[{c['name']}] ok -> {out.name} ({row['bytes']} bytes, {row['seconds_waited']} s)")


if __name__ == "__main__":
    main()
