# AI Persona Lab — Experiment Log

## Experiment 001 — Initial Full-Character Generation (Phase A: portrait candidates)
Date: 2026-10-25 (setup approved)
Status: Batch 1 (seeds 1001–1003) generated 2026-10-25. Founder decision: seed 1001 is the provisional canonical face (see Experiment 002). Batch 2 not run.

### Hypothesis
A low-cost image-generation workflow can produce a promising, photorealistic **adult fictional person** with a coherent face **and full body**, suitable for later identity-consistency testing.

### Setup
- Model / provider: Z-Image Turbo on fal.ai, endpoint `fal-ai/z-image/turbo` (being evaluated, not yet approved as a tool). fal exposes no model version number; the endpoint, date, seed, params and fal request ids are recorded instead.
- Pricing checked 2026-10-25: $0.005 per megapixel. Prompt expansion (+$0.0025/request) is off.
- Approved character specification: `PROJECT_SPEC.md` creative brief (exploration only, identity not locked).
- Reference images: None. Text-to-image only.
- Portrait prompt: `PROMPTS.md` Prompt 1, verbatim → `experiments/001-portrait/prompt.txt`
- Full-body prompt: Not in this phase (Prompt 2 follows once a face is shortlisted).
- Settings (`experiments/001-portrait/config.json`): 1152×1536 (3:4, 1.77 MP), 8 steps, acceleration `none`, 1 image per request, PNG, safety checker on. Z-Image Turbo has no negative prompt or guidance scale.
- Acceleration `none` is the baseline choice only; it is not assumed better than `regular`. That needs a same-seed comparison.
- Seeds: fixed, 1001–1020. Each image's seed is also read back from the API response.
- Number of generations: 20 planned, run in stages. **Batch 1 = seeds 1001–1003, then stop for founder + ChatGPT review.** Batch 2 (1004–1020) needs separate approval.
- Estimated cost: about $0.009/image; $0.027 for batch 1, about $0.18 for all 20 (conservatively $0.20 if billed per whole megapixel).
- Founder approval: 2026-10-25, spending cap **$1.00 USD** for Experiment 001.
- Script: `scripts/generate_fal.py`. Per-request records: `experiments/001-portrait/runs.jsonl`. Storage and backup: `experiments/README.md`.

### Results
**Batch 1: seeds 1001–1003 (2026-10-25)**
- Actual total cost: $0.03 by script estimate (fal's `x-fal-billable-units: 2` per image × $0.005). fal bills **whole megapixels**: 1.77 MP is charged as 2 MP, so about $0.01/image. Confirm in the fal dashboard.
- Portrait candidates: 3. Usable: pending review.
- Returned seeds matched requested seeds (1001, 1002, 1003). No safety flags. Inference took 1.6–2.3 s per image.
- Files: `experiments/001-portrait/contact_sheet.jpg`, `runs.jsonl` (params, request ids, hashes), `review.csv` (empty scoring sheet). Originals are local in `images/` and mirrored to OneDrive (`AI-persona-lab-originals`).
- Claude's technical first look (not the quality review):
  - Realism is strong in all three: believable skin with pores and some sheen, natural hairlines, no hand/text/extra-person artifacts.
  - **Eye colour drifted to brown in all three**; the brief asks for hazel.
  - **No visible forehead scar or cheekbone beauty mark in any image**; the small landmarks were not rendered.
  - Hair: 1001 has the closest match to 2B waves. 1002 and 1003 are mostly straight or slicked back.
  - Neckline: 1002 is a crew neck as prompted; 1001 and 1003 are scoop necks.
  - The three seeds give **very similar faces** (low variation between seeds). That suits consistency but limits casting variety from seed changes alone.
- Face/body cohesion: Not tested in this phase.
- Identity consistency across angles or scenes: Not yet tested.

### Problems
- First run: seed 1001 generated (and was billed), but downloading the image failed with an SSL certificate error. Python's default certificate store rejects fal's image host. The image was recovered from the saved API response at no extra charge. The script now uses the certifi bundle and recovers saved-but-undownloaded seeds automatically.

### Decision
Pending.

### Next Experiment
After a face-and-body identity is approved, test the same character across front/side/three-quarter views, different outfits, poses, scenes, and lighting, then perform an early image-to-video consistency test. Do not assemble a large LoRA or Soul ID dataset until these tests justify it.

---

## Experiment 002 — Reference-Based Portrait Refinement of Seed 1001
Date: 2026-10-25
Status: Run complete (8/8). Paused for founder + ChatGPT review.

### Hypothesis
An instruction-based edit model can keep the provisional canonical face (Exp 001 seed 1001) recognizably the same person while changing the irises to hazel and adding a right-cheekbone beauty mark and a left-forehead scar.

### Setup
- Reference: `experiments/001-portrait/shortlist/seed-1001.png` (SHA-256 `12bb637b…8b88`, unchanged; hash checked before and after the run). The local original is set read-only.
- Prompt: `experiments/002-portrait-refine/prompt.txt`. This is the approved edit prompt, plus one line making identity and realism the priority over the marks (founder adjustment 3).
- Arms (4 images each, seeds 2001–2004), settings in `experiments/002-portrait-refine/config.json`:
  - **flux2pro**: `fal-ai/flux-2-pro/edit`, custom 1152×1536 (3:4, same as the reference), PNG.
  - **nanobananapro**: `fal-ai/nano-banana-pro/edit`, aspect 3:4, resolution 2K, PNG. It has no custom pixel size. 2K was chosen over 1K at the same price because 1K is below the reference's 1.77 MP.
  - Safety settings: fal defaults for both.
- Acceptance (founder): identity vs 1001 **≥ 4/5** and photorealism **≥ 4/5** are both mandatory. Identity outranks cosmetic changes. Hazel eyes, mark and scar are secondary. Reject anything more artificial or glamorous than 1001. The winner becomes the preferred *portrait refinement* tool only; full-body is evaluated separately.
- Cap: $1.50. Estimate: $0.90.

### Results
- Actual cost: **$0.90** by script estimate. FLUX.2: 4 × $0.075 (fal billable units 2.5 × $0.03). Nano Banana Pro: 4 × $0.15. Confirm in the fal dashboard. Month-to-date ≈ $0.93.
- Actual dimensions: flux2pro 1152×1536; nanobananapro 1792×2400 (both 3:4).
- Seeds: FLUX.2 returned the requested seeds. Nano Banana Pro accepts a seed but returns none, so its outputs may not be exactly reproducible.
- Speed: FLUX.2 19–23 s per image; Nano Banana Pro 27–37 s.
- Files: `contact_sheet.jpg` (1001 reference first, then all 8), `runs.jsonl`, `review.csv` (empty scoring sheet with the acceptance columns). Originals are local and mirrored to OneDrive.
- Claude's technical first look (founder + ChatGPT make the acceptance call):
  - **Mark placement failed in both models: the beauty mark landed on the subject's *left* cheek (viewer's right), the opposite of the request.** Where a forehead scar appeared, it was on the subject's *right* (viewer's left), also mirrored. The prompt named both her side and the viewer's side, and both models still mirrored them.
  - **nanobananapro:** the face looks essentially unchanged from 1001, with a believable skin texture. Irises are lighter, warm amber-golden; more hazel than 1001 but little green. Beauty marks are small and natural. The scar is absent or very faint in the images inspected closely. Hair and top are preserved.
  - **flux2pro:** the face is broadly similar, but skin looks slightly shinier and more retouched. Irises in 2002–2004 are a saturated yellow-green that looks artificial. Scars are overt cuts or wounds, not subtle, and 2001 added an extra cheek mark. On the realism and "not more artificial" rules, these look likely to fail.

### Problems
- Left/right instructions were mirrored by both models despite stating both the subject's side and the image side.
- Nano Banana Pro does not return a seed (reproducibility gap).

### Decision
Pending founder + ChatGPT review.

### Next Experiment
To be decided after review. Options for the mirrored marks:
- adopt the side the model produced and lock that in `PROJECT_SPEC.md`
- re-prompt using only image-side wording
- use a masked edit or inpaint to place the marks exactly

