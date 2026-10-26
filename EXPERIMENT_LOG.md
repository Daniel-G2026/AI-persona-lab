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
Status: Complete. Founder decision recorded 2026-10-25.

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
Founder decision (2026-10-25), after ChatGPT review:
- **Provisional refined canonical portrait reference: Nano Banana Pro seed 2002** → `experiments/002-portrait-refine/shortlist/nanobananapro-seed-2002.png` (SHA-256 `5b5191d0…8893`).
- **Original untouched facial baseline: Exp 001 seed 1001** remains preserved → `experiments/001-portrait/shortlist/seed-1001.png`.
- Nano Banana Pro is the preferred portrait refinement tool. Full-body performance is evaluated separately (Experiment 003).
- Observed in 2002: the beauty mark is on the subject's **left** cheekbone (viewer's right). No visible forehead scar. Irises are warm amber-brown. **The mark side is not yet formally locked in `PROJECT_SPEC.md`** pending founder confirmation.

### Next Experiment
Experiment 003: first full-body identity test. Proposal: `experiments/003-full-body/PROPOSAL.md` (pending founder approval). Options for the mirrored marks:
- adopt the side the model produced and lock that in `PROJECT_SPEC.md`
- re-prompt using only image-side wording
- use a masked edit or inpaint to place the marks exactly

---

## Experiment 003 — First Full-Body Identity Test
Date: 2026-10-25
Status: Complete. Reviewed 2026-10-25.

### Hypothesis
Nano Banana Pro, given the canonical portrait as a reference, can produce a believable head-to-shoes image of the same woman that matches the body brief, and adding the 1001 baseline as a second reference changes identity preservation.

### Setup
- Proposal: `experiments/003-full-body/PROPOSAL.md`. Settings: `experiments/003-full-body/config.json`.
- Model: Nano Banana Pro Edit (`fal-ai/nano-banana-pro/edit`), aspect 2:3, resolution 2K, PNG, fal default safety settings.
- Arms (4 images each, seeds 3001–3004):
  - **ref2002**: reference 2002 only. Prompt: `prompt_ref2002.txt`.
  - **ref2002+1001**: 2002 first, 1001 second. Prompt: `prompt_ref2002+1001.txt` (adds one sentence naming the second image as a supporting reference).
- References: 2002 (SHA-256 `5b5191d0…8893`) and 1001 (`12bb637b…8b88`), hash-checked before and after the run.
- Founder adjustments applied:
  1. Beauty mark locked on the subject's left cheekbone (now in `PROJECT_SPEC.md`); the prompt says so. The scar is deferred and the prompt says "Do not add any scar."
  2. Identity is judged on manually selected face crops. An upscaled crop doesn't add detail, so identity is marked **inconclusive** when the face is too small to judge.
  3. A head-to-height ratio of about 1:7.5 is an approximate reference only.
  4. Prompt line added: "Realistic anatomy, natural proportions and her identity from the reference take priority over the body description: do not exaggerate her curves to match it."
  5. Manual face crops, no OpenCV.
  6. All outputs, references, settings and costs are recorded in `runs.jsonl` and this log.
- Acceptance rules: in `config.json` and `PROPOSAL.md`.
- Cap: $2.00. Estimate: $1.20.

### Results
- Actual cost: **$1.20** by script estimate (8 × $0.15). Each request reported 1 billable unit; the second reference did not change the price. Confirm in the fal dashboard. Month-to-date ≈ $2.13.
- Actual dimensions: 1696×2528 (2:3) for all 8. No seeds returned (Nano Banana Pro limitation). No safety flags. Reference hashes unchanged after the run.
- Files in `experiments/003-full-body/`:
  - `contact_sheet.jpg`: both references, then all 8
  - `face_crops.jpg`: manual face crops next to 2002 and 1001; boxes in `face_crops.json`, sheet built by `scripts/face_crop_sheet.py`
  - `runs.jsonl`
  - `review.csv`: face-crop size prefilled
  - Originals are local and mirrored to OneDrive.
- **Face resolution:** each face is about 300–340 px in the source (references: 2002 about 900 px, 1001 about 600 px). That is enough to judge overall identity and the beauty mark, but not pores or fine iris detail. Reviewers should mark identity inconclusive where they can't decide.
- Claude's technical first look (the acceptance calls are for founder + ChatGPT):
  - **Identity:** all 8 faces read as close to 2002 at this resolution: face shape, brows, nose, lips and hair. No obvious lookalike substitutions. Some (ref2002 3003/3004, ref2002+1001 3004) have a mauve or purple eye-makeup tint and a slightly more polished look than 2002.
  - **Beauty mark:** visible on the subject's **left** cheekbone (correct, locked side) in most images and never mirrored. No scar in any image (as instructed).
  - **Anatomy:** hands, fingers and feet look clean in all 8. Natural standing poses, full head-to-shoes framing, no obvious wide-angle distortion.
  - **Body vs brief:** consistently slim and athletic, with a flat toned stomach and long legs. Bust and hips read toward the lean, modest end of the brief rather than "lean-curvy", which errs on the side of founder adjustment 4 (no exaggeration).
  - **Wardrobe compliance:** 6 of 8 wear the requested sports top and leggings. ref2002 3003 has a long-sleeve top, ref2002+1001 3004 has a t-shirt, and ref2002+1001 3002 is an olive/green set rather than a neutral tone.
  - **Reference arms:** no clear difference between 2002 only and 2002 + 1001 at this resolution. This needs the founder/ChatGPT scores.

### Problems
- Faces are only about 300–340 px in a full-length 2K frame, which limits identity judgment. A 4K run ($0.30 per image) or a separate three-quarter-length frame would give more facial detail.
- Some outfit drift from the prompt (2 of 8 tops, 1 of 8 colours).

### Decision
ChatGPT review, relayed by the founder (2026-10-25):
- Full-body generation is **promising**: identity and realism are good enough to continue.
- **The lower body is too slim and too straight for the brief.** Missing: (1) more outward hip curve from the front; (2) more glute projection and roundness from the side and three-quarter angle.
- Preserve: 2002 facial identity, slim balanced upper body, longer torso, flat lightly toned stomach, natural medium bust, long toned legs, realistic athletic look.
- Do not: make her generally thicker, shrink the waist, enlarge the bust, or create a BBL-like, surgically enhanced or cartoonish shape.
- No per-image scores recorded. The 2002-only vs 2002 + 1001 question was not decided.

### Next Experiment
Experiment 004: lower-body shape refinement. Proposal: `experiments/004-body-shape/PROPOSAL.md` (approved 2026-10-25 with adjustments).

---

## Experiment 004 — Lower-Body Shape Refinement
Date: 2026-10-25
Status: Batch 1 and revised Batch 2 (seed 4101, front-gen-v2 + 3q-gen-v2) complete 2026-10-25. Paused for founder + ChatGPT review.

### Hypothesis
Nano Banana Pro can add more lateral hip curvature and rounded, lifted glutes without changing the 2002 face, upper body, longer torso, waist width, bust or slim athletic build. Editing an Exp 003 image may control a front view better than generating fresh. For three-quarter views, an Exp 003 body reference may help or hinder.

### Setup
- Proposal: `experiments/004-body-shape/PROPOSAL.md`. Settings: `experiments/004-body-shape/config.json`.
- Model: Nano Banana Pro Edit, 2K, 2:3, PNG, fal default safety settings.
- References:
  - 2002 face (SHA-256 `5b5191d0…8893`)
  - **Exp 003 `ref2002-seed-3001` as a temporary editing base**, copied to `experiments/004-body-shape/base/003-ref2002-seed-3001.png` (SHA-256 `6da8e656…768d`). **Its physique is not canonical** (founder).
- Arms:
  - **front-edit**: edits the 003 base; references 003 base + 2002
  - **front-gen**: new image from 2002
  - **3q-gen**: new image from 2002
  - **3q-gen+003**: new image from 2002 + 003 base
  - Prompts are in `prompt_*.txt`.
- Founder adjustments applied:
  1. The body description now stresses moderate fullness at the sides of the hips and in the upper glutes, with the curve coming from there, "not from heavier thighs or an extra-narrow waist". The front-edit prompt says the same.
  2. Three-quarter pose: realistic posture; arms relaxed and slightly away from the body so neither overlaps the hips or seat; lateral hip curve and glute profile "clearly visible in silhouette".
  3. **Staged run: seed 4001 for each of the 4 arms (4 images), then stop for founder + ChatGPT review.** Seeds 4002–4003 need separate approval.
  4. The 003 base is temporary and not canonical (as above).
  5. Prompts explicitly preserve facial identity, upper-body anatomy, longer torso, waist width, bust size and the slim athletic build.
- Wardrobe line tightened: a short fitted sports top, not a t-shirt or long-sleeved, in a single taupe-grey tone.
- Cap: $2.50 for the whole experiment. Estimate: $0.60 for batch 1, $1.80 for all 12.

### Results — Batch 1 (seed 4001, 4 images)
- Actual cost: **$0.60** by script estimate (4 × $0.15, 1 billable unit each, including the two-reference arms). Experiment total so far: $0.60 of the $2.50 cap. Month-to-date ≈ $2.73.
- All images 1696×2528. No seeds returned, no safety flags. Reference hashes unchanged.
- Files in `experiments/004-body-shape/`:
  - `contact_sheet.jpg`
  - `before_after.jpg`: the 003 base and all 4 at identical scale
  - `face_crops.jpg` (boxes in `face_crops.json`)
  - `runs.jsonl`
  - `review.csv`: face-crop sizes prefilled
- **Approximate front-view widths** (manual, ±10 px, same 1696×2528 frame; front-gen has slightly different framing):

| Image | Shoulders | Waist (narrowest) | Hips (widest) | Hip ÷ waist |
|---|---|---|---|---|
| 003 base | ~540 | ~322 | ~432 | ~1.34 |
| front-edit 4001 | ~542 | ~318 | ~438 | ~1.38 |
| front-gen 4001 | ~570 | ~324 | ~444 | ~1.37 |

- Claude's technical first look (the acceptance calls are for founder + ChatGPT):
  - **front-edit:** nearly identical to the base. Face, upper body, outfit and pose are preserved, but the hip change is within measurement error and is hard to see side by side. The edit was too conservative.
  - **front-gen:** a good match to the brief's upper body and a clean anatomy. The hip line is only marginally curvier than the base; it reads about the same.
  - **3q-gen:** the **only image showing the target shape**: a clear lateral hip curve and rounded, lifted glute projection in profile, while the waist and upper body stay slim. It doesn't look BBL-like to me, but reviewers should judge. **The pose overshot:** she is turned well past 45°, closer to a rear three-quarter view, looking back over her shoulder. One hand sits near the side of her thigh, but the silhouette stays readable.
  - **3q-gen+003:** **the pose failed.** She is only slightly turned, close to front-facing, so the glute profile isn't visible. The 003 reference appears to have pulled her back into its front-facing stance.
  - **Identity:** all 4 faces are plausible matches to 2002 at about 320–340 px. Wherever the beauty mark is visible, it's on her left cheek. No scar. Hands and feet look clean.
  - **Outfit:** all 4 wear the tightened wardrobe (short sports top, taupe-grey leggings, neutral sneakers). That fixes the Exp 003 drift.

### Problems
- The front edit made almost no visible change (the hip shift is within measurement error).
- The 003 body reference overrode the three-quarter pose instruction.
- The 3q-gen angle overshot 45°.

### Decision (Batch 1 review)
Founder + ChatGPT assessment (2026-10-25):
- front-edit 4001: insufficient change.
- front-gen 4001: insufficient outward hip curvature.
- 3q-gen 4001: closest lower-body shape to the target, but the pose is too rear-facing and **the face has drifted**.
- 3q-gen+003 4001: inadequate three-quarter angle.
- **Do not run seeds 4002–4003 with the original prompts** (cancelled).
- Wanted: a **noticeably more pronounced lower-body silhouette**, visually apparent compared with Exp 003, while preserving the approved upper body and facial identity.

### Revised Batch 2 (approved 2026-10-25)
- Two new generations, **2002 as the only identity reference**, seed 4101:
  - `front-gen-v2`: front-facing. Prompt: `experiments/004-body-shape/prompt_front_gen_v2.txt`
  - `3q-gen-v2`: true three-quarter view. Prompt: `experiments/004-body-shape/prompt_3q_gen_v2.txt`
- Prompt changes vs batch 1:
  - The lower-body description is rewritten around the founder/ChatGPT points:
    1. clearly visible outward hip curve from the front
    2. volume in the lateral hips and upper glutes, not thicker thighs
    3. noticeably rounded, lifted glutes with natural backward projection
    4. a smooth narrow waist → full hips → toned upper thighs transition
    5. no narrowing of the waist or enlarging of the bust
  - The hedged wording ("slightly fuller", "gently", "subtle") is removed. The no-BBL / no-surgical / no-cartoonish / not-heavier guardrails are kept.
  - The upper body is explicitly held as approved.
  - **Face drift:** the prompts add "Her face must stay clearly visible and recognizable as the woman in the reference." The three-quarter head turn is limited to "only slightly toward the camera" (3q-gen 4001 drifted while looking back over its shoulder).
  - **True three-quarter pose:** body rotated about 45° with the front of the torso and her left side both visible, left hip nearest the camera. "Her back is NOT toward the camera, and she is not looking over her shoulder." Chest and stomach partly visible; arms slightly forward so the hips and seat stay unobscured.
  - Front pose: weight on one leg, arms a little away from her sides so they don't cover her waist or hips.
  - The wardrobe line now notes the leggings "fit closely enough to show her real shape".
  - Camera at about waist height (was waist-to-chest) to avoid shortening the legs and hips.
- ChatGPT's full anatomical description was not received verbatim; the prompts were written from its five emphasis points.
- Estimate: 2 × $0.15 = **$0.30**. Experiment 004 total would be $0.90 of the $2.50 cap; month-to-date about $3.03.
- Same success criteria as Experiment 004, plus: the front image must show a hip curve **visibly** more outward than the 003 base (side by side and by approximate width ratio); the three-quarter image must be a true 45° view with an unobscured hip and glute silhouette and identity ≥ 4/5.
- **Approval (founder, after ChatGPT review, 2026-10-25):** two images, seed 4101, $0.30 estimate within the $2.50 cap. Before generating, the lower-body introduction was strengthened in both prompts to stress the **visible contrast between her slender upper body and naturally fuller hips and glutes**, with shoulders, waist, bust and torso proportions explicitly unchanged.
- **Founder stopping rule:** if the hip shape still doesn't noticeably improve, stop revising the text and investigate a dedicated body-shape reference or a more controllable editing approach.

### Results — Revised Batch 2 (seed 4101, 2 images)
- Actual cost: **$0.30** by script estimate (2 × $0.15). Experiment 004 total: **$0.90** of the $2.50 cap. Month-to-date ≈ $3.03.
- Both images 1696×2528. No seeds returned, no safety flags. References unchanged.
- Files: `before_after_v2.jpg` (003 base, front-gen v1, front-gen-v2, 3q-gen v1, 3q-gen-v2 at identical scale), updated `face_crops.jpg`, `contact_sheet.jpg`, `runs.jsonl`, `review.csv`.
- **Approximate front-view widths** (manual, ±10 px):

| Image | Shoulders | Waist | Hips | Hip ÷ waist |
|---|---|---|---|---|
| 003 base | ~540 | ~322 | ~432 | ~1.34 |
| front-gen 4001 (v1) | ~570 | ~324 | ~444 | ~1.37 |
| **front-gen-v2 4101** | ~558 | ~320 | ~469 | **~1.47** |

- Claude's technical first look (the acceptance calls are for founder + ChatGPT):
  - **front-gen-v2:** a **measurable improvement**. Hip-to-waist ratio is about 1.47 vs about 1.34 for the base (roughly +10%), from wider hips while the waist stays about the same. The outward hip curve is visible side by side. The upper body, flat stomach and bust read as unchanged. Still clearly slim and realistic, not exaggerated. Whether the change is *enough* is the reviewers' call; it is noticeable but moderate.
  - **3q-gen-v2:** **pose fixed**. A true front-left three-quarter view, left hip nearest the camera, front of the torso visible, arms clear of the hips. **The face is the closest to 2002 of any Exp 004 image**: same orientation, beauty mark on the left cheek. The glute projection and hip curve are visible but **clearly less pronounced than 3q-gen 4001**, so the rear-leaning v1 pose showed more shape than the true three-quarter view.
  - Hands, feet and outfit look clean and on-brief in both.
- **Against the founder's stopping rule:** the front view improved noticeably; the three-quarter view improved in pose and face but not in shape. Two text revisions have now moved the hip ratio by about 10% at most.

### Decision
Founder direction (2026-10-25):
- **Exp 004 front-gen-v2 4101 is the strongest current front-body reference** for improved hip shape.
- The current slimmer lean-curvy body is kept as **Version A**, a valid option that is not discarded.
- A fuller lower-body **Version B** ("gym girl thicker": broader hips, fuller upper thighs, larger, rounder, more projected glutes; same face, waist, bust and upper body) will be explored **as a comparison branch, not a replacement**.
- Both must be the same woman, and are compared side by side before any direction is chosen. `PROJECT_SPEC.md` is not rewritten around Version B.

### Next Experiment
Experiment 005: Version A vs Version B comparison. Proposal: `experiments/005-body-ab/PROPOSAL.md` (approved 2026-10-25, Stage 1 only).

---

## Experiment 005 — Body Direction A/B Comparison
Date: 2026-10-25
Status: Design approved by founder (after ChatGPT review) 2026-10-25. **Stage 1 only (6 images) authorized** and complete 2026-10-25. Paused for founder + ChatGPT review. Stage 2 not approved.

### Hypothesis
The same woman can be shown in two body directions: **Version A** (current lean-curvy) and **Version B** (fuller hips, upper thighs and glutes, same face and upper body). These can be compared side by side without the identity drifting into a different woman.

### Setup
- Proposal: `experiments/005-body-ab/PROPOSAL.md`. Settings: `experiments/005-body-ab/config.json`.
- Model: Nano Banana Pro Edit, 2K, 2:3, PNG, fal default safety settings.
- References (hash-checked):
  - 2002 face anchor
  - Version A bases (preserved, read-only originals): `base/004-front-gen-v2-seed-4101.png` (`24dd9192…`) and `base/004-3q-gen-v2-seed-4101.png` (`3c8eafb4…`)
- Arms:
  - **Track 1 (paired edits):** `B-front-edit` and `B-3q-edit` edit the Version A bases (A image first, then 2002).
  - **Track 2 (matched generations, 2002 only):** `A-front-gen`, `B-front-gen`, `A-3q-gen`, `B-3q-gen`. A and B prompts are identical except the body paragraphs.
- Stage 1: seed 5001 for all 6 arms. Estimate **$0.90**. Experiment cap **$3.00**.
- Founder adjustments on approval:
  1. **Version B thighs strengthened** (all 4 B prompts): visibly fuller upper thighs through both inner and outer thigh contours, natural quadriceps and hamstring fullness, athletic definition, gradual taper toward the knees; the A/B thigh difference should be clearly noticeable. **Version A prompts unchanged.**
  2. **Evaluation:** separate real anatomical differences from apparent ones caused by camera angle, perspective, stance or pose. Matched seeds don't guarantee identical compositions. A pair-level review (`review_pairs.csv`) records composition differences and discounts differences they explain.
- Preserved for both versions: 2002 facial identity, beauty mark on the left cheekbone, slim upper body, same waist width and medium natural bust, longer torso, realistic anatomy and skin.
- **Version A stays a fully valid alternative. No winner is designated until the founder compares the images.**

### Results — Stage 1 (seed 5001, 6 images)
- Actual cost: **$0.90** by script estimate (6 × $0.15). Experiment 005 total $0.90 of the $3.00 cap. Month-to-date ≈ $3.93.
- All 1696×2528, no seeds returned, no safety flags, reference hashes unchanged.
- Files in `experiments/005-body-ab/`:
  - **`ab_pairs.jpg`**: 4 rows, A left / B right, same scale. Built by `scripts/ab_sheet.py` from `config.json` pairs.
  - `face_crops.jpg`: 2002, 1001, both A bases and all 6 outputs.
  - `contact_sheet.jpg`
  - `review.csv`: per image, with version, view and method prefilled.
  - `review_pairs.csv`: per pair, including composition-difference columns.
  - `runs.jsonl`
- **Identity:** all 6 faces read as the same woman as 2002 and as each other, at about 340 px face crops. The beauty mark is on the left cheekbone in all 6. No scar. Hands and feet look clean.
- **Composition:** Track 2's matched seeds produced **very similar compositions** for A and B in both views (same pose, framing and lighting), so those pairs compare well. Track 1 pairs share the base image by design.
- **Approximate measurements** (manual, ±10 px; ratios matter more than raw pixels because framing differs between tracks):

| Front | Waist | Hips | Upper thighs (outer) | Hip ÷ waist | Thigh ÷ waist |
|---|---|---|---|---|---|
| A base 4101 | ~310 | ~465 | ~442 | ~1.50 | ~1.43 |
| B edit 5001 | ~315 | ~472 | ~445 | ~1.50 | ~1.41 |
| A gen 5001 | ~350 | ~505 | ~510 | ~1.44 | ~1.46 |
| B gen 5001 | ~355 | ~515 | ~520 | ~1.45 | ~1.46 |

| Three-quarter (body depth) | Waist | Glute level | Glute ÷ waist |
|---|---|---|---|
| A base 4101 | ~259 | ~377 | ~1.46 |
| B edit 5001 | ~255 | ~398 | ~1.56 |
| A gen 5001 | ~275 | ~395 | ~1.44 |
| B gen 5001 | ~252 | ~395 | ~1.57 |

- Claude's technical first look (**no winner designated**; founder + ChatGPT decide):
  - **Front, both tracks:** the A/B difference is **small**. Width ratios are within measurement error. Visually, B's thighs may read a touch fuller in places, but not the "clearly noticeable" difference intended. The front edit repeated Exp 004's pattern of barely changing the base.
  - **Three-quarter, Track 1 (edit):** a **visible, real difference**. B has a rounder, more projected seat (back contour about 28 px further out at glute level) and fuller-looking thighs, while the waist depth, upper body, face, pose and lighting are unchanged. Because the pose is identical, this is anatomical, not a camera effect.
  - **Three-quarter, Track 2 (generation):** B looks rounder and more projected, but **part of the higher ratio comes from a smaller waist depth** (about 252 vs 275 px), against the "do not narrow the waist" rule. It could be a slight rotation difference or real waist narrowing; reviewers should check.
  - Neither version looks exaggerated or distorted. Both remain realistic.

### Problems
- Version B's front-view difference is far smaller than intended in both edit and generation.
- B 3q gen 5001 may narrow the waist (or be slightly rotated).

### Decision
Pending founder + ChatGPT review. **No version designated as the winner. Version A remains a fully valid alternative.** Stage 2 not approved.

