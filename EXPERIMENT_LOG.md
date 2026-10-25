# AI Persona Lab — Experiment Log

## Experiment 001 — Initial Full-Character Generation (Phase A: portrait candidates)
Date: 2026-10-25 (setup approved)
Status: Approved, awaiting fal API key and credits. Batch 1 (3 images) not yet run.

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
- Actual total cost: TBD
- Portrait candidates / usable portraits: TBD
- Full-body candidates / usable full-body images: TBD
- Output file paths and saved settings: TBD
- Realism assessment: TBD
- Face/body cohesion: TBD
- Identity consistency across angles or scenes: Not yet tested

### Problems
Not yet run.

### Decision
Pending.

### Next Experiment
After a face-and-body identity is approved, test the same character across front/side/three-quarter views, different outfits, poses, scenes, and lighting, then perform an early image-to-video consistency test. Do not assemble a large LoRA or Soul ID dataset until these tests justify it.
