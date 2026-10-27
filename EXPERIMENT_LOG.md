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
Founder + ChatGPT assessment (2026-10-25):
- Track 1 front edit: insufficient A/B difference.
- **Track 1 three-quarter edit: a successful directional improvement.** B has more rounded, projected glutes with the face, waist, lighting and pose preserved.
- Track 2 front generation: insufficient difference in hip and thigh fullness.
- Track 2 three-quarter generation: some improvement, but possibly partly from a narrower waist depth or a slight pose difference.
- **B-3q-edit 5001 is the strongest fuller-body result so far, but Version B still doesn't fully meet the brief, especially the noticeably fuller upper thighs.**

Decisions:
1. **Version A preserved** as a valid alternative (references in `experiments/005-body-ab/base/`; see `shortlist/A/README.md`).
2. **B-3q-edit seed 5001 shortlisted** as the strongest Version B candidate → `experiments/005-body-ab/shortlist/B/B-3q-edit-seed-5001.png` (SHA-256 `7bf900c2…a5`).
3. **Neither physique is canonical.**
4. **The original Stage 2 is cancelled** (do not run it unchanged).

### Next Experiment
Experiment 006: a more controllable method for lower-body shaping (masked editing vs a body-shape reference, plus a geometric warp). Proposal: `experiments/006-body-control/PROPOSAL.md` (Stage 0 approved 2026-10-25).

---

## Experiment 006 — Controllable Lower-Body Shaping
Date: 2026-10-25
Status: **Stage 0 only** (free local warp previews) approved by founder after ChatGPT review, and complete. **No paid calls made.** Paused for the founder to choose a shape intensity.

### Hypothesis
A local geometric warp can produce a clearly fuller lower body (hips, inner and outer upper thighs, glutes) at an exact, measurable size, with the face, upper body and waist provably unchanged. It can then serve as the shape target for a later realism pass.

### Setup
- Proposal: `experiments/006-body-control/PROPOSAL.md`. Warp settings: `warp_config.json`. Scripts: `scripts/body_warp.py`, `scripts/cleanup_masks.py`.
- Sources: Version A front and three-quarter (`experiments/005-body-ab/base/…4101.png`). **Unchanged after the run:** hashes re-verified (`24dd9192…`, `3c8eafb4…`), and the originals in Exp 004 are read-only.
- Method:
  - Each image row gets a smooth 1-D mapping built from the legging outline (detected by colour).
  - Displacement is zero at and above the waistband (y≈1000) and tapers to zero at the knees (y≈1830).
  - Front: outer contours pushed out, inner-thigh contours pushed toward each other (fills the thigh gap).
  - Three-quarter: back contour (glutes, back of thigh) pushed out, plus a small front-thigh push.
  - **Arms and hands move rigidly with the body surface beside them** (translated, never stretched). An earlier attempt pasted the original arms back on top; it left light halos, then streaks and background-coloured chunks in the three-quarter view, so it was replaced.
- Intensities: **B-mid** (about 25 px per side) and **B-strong** (about 40 px per side), per the proposal.
- Cost: **$0.00.**

### Results
- Files in `experiments/006-body-control/`:
  - **`warp_previews.jpg`**: A | B-mid | B-strong per view, same scale
  - `warp/*.png`: full-resolution previews (hashes in `warp_measurements.json`)
  - `warp_diff_sheet.jpg`: changed pixels in red
  - `warp_measurements.json`
  - `cleanup_masks_preview.jpg` plus `warp/*-mask-narrow.png` / `*-mask-broad.png` (drafts)
- **Measured** (automatic, from the legging outline in the same 1696×2528 frame; outer span = legging edge to legging edge; arms excluded):

| Front | A | B-mid | B-strong |
|---|---|---|---|
| Hips (outer span) | 466 | 516 (**+10.7%**) | 539 (**+15.7%**) |
| Upper thigh (outer span) | 430 | 477 (+10.9%) | 506 (+17.7%) |
| Upper thigh, single leg | 201 | 232 (+15%) | 249 (+24%) |
| Mid thigh, single leg | 181 | 208 (+15%) | 225 (+24%) |
| Knee (outer span) | 368 | 368 (0%) | 368 (0%) |
| Pixels changed above waistband / below knee | n/a | 0 / 0 | 0 / 0 |
| Max hand/arm shift | n/a | 25 px | 40 px |

| Three-quarter | A | B-mid | B-strong |
|---|---|---|---|
| Glute-level depth | 387 | 414 (**+7.0%**) | 430 (**+11.1%**) |
| Upper thigh depth | 296 | 321 (+8.4%) | 334 (+12.8%) |
| Waistband depth | 229 | 229 (0%) | 229 (0%) |
| Knee | 216 | 216 | 216 |
| Pixels changed above waistband / below knee | n/a | 0 / 0 | 0 / 0 |
| Max hand/arm shift | n/a | 9 px | 14 px |

- **Waist width is unchanged by construction:** zero changed pixels at or above the waistband in all four previews. The face and upper body are pixel-identical to Version A.
- Claude's **subjective** look (separate from the measurements):
  - Front B-mid: reads as noticeably fuller hips and thighs, with the upper thigh gap mostly closed. Still natural-looking.
  - Front B-strong: clearly "thicker" lower body. The thigh-to-knee taper is somewhat abrupt just above the knee.
  - Three-quarter B-mid: rounder, more lifted, more projected glutes; looks natural.
  - Three-quarter B-strong: strongly projected glutes; still plausible to me, but reviewers should judge.
- **Artifacts (reported honestly):**
  1. **Front hands and forearms are shifted outward** (up to 25 px mid / 40 px strong), and at B-strong the forearms **bow slightly**, because the shift grows from elbow to wrist. This was the trade-off to avoid the halos and streaks of pasting the arms back. Three-quarter hand shifts are small (9 / 14 px).
  2. **Legging shading is stretched, not re-rendered:** side-shading bands are wider and fold or tension detail doesn't update physically. Most visible across the front thighs at B-strong. This is what a realism pass must fix.
  3. Background beside the legs is slightly compressed; invisible on the plain backdrop at normal viewing size.
  4. Knees, calves, shoes, floor and everything above the waistband are untouched.
- **Cleanup masks (founder point 4), for a future paid stage:**
  - **Narrow** (about ±25 px around the new outline, 2.6–3.6% of the frame): fixes edges only. **It cannot fix the stretched shading across the thighs** (artifact 2).
  - **Broad** (the whole legging area from waistband to knee plus margin, 6.3–9.8% of the frame): lets the model re-render fabric tension, folds and shading throughout, at a higher risk of the model shrinking the shape back.
  - Draft limitation: the front narrow mask wrongly includes the waistband seam line (lighter than the fabric). Both masks need a manual touch-up before any paid use.
  - Likely best: the broad mask for fabric, combined with a prompt that holds the outline.

### Decision
Founder decision (2026-10-25):
- **B-strong is the correct Version B lower-body fullness target** for both views (`warp/front-B-strong.png`, `warp/three-quarter-B-strong.png`).
- B-strong is the **selected shape target, not a finished image**. Realism reconstruction comes next.
- **Version A remains preserved** as a valid alternative. **Version B is not canonical.**

### Next Experiment
Experiment 007: realism reconstruction of the B-strong targets. Proposal: `experiments/007-reconstruction/PROPOSAL.md` (approved in principle 2026-10-25; staged).

---

## Experiment 007 — Realism Reconstruction of the B-strong Target
Date: 2026-10-25
Status: Approach approved in principle by founder (after ChatGPT review), **staged**. Step 1 (free B-strong-v2 re-warp) approved; step 1b fixes done; **6-image paid checkpoint complete 2026-10-25. Paused for founder + ChatGPT review.**

### Founder conditions for later stages
- After v2 approval, propose a **6-image checkpoint**: R1 (FLUX Fill, interior mask), R2 (Z-Image i2i, **one documented strength**) and R3 (Nano Banana Pro), each 1 front + 1 three-quarter. About $0.52.
- Checks required at that stage:
  1. the 12 px protected silhouette band keeps no visible stretching and creates no boundary seams
  2. crop dimensions, output alignment and compositing accuracy verified
  3. R1/R2 preserve every pixel outside the compositing region
  4. R3: face independently checked against 2002, and the lower-body silhouette measured for any reduction
  5. all raw outputs kept

### Step 1 — B-strong-v2 (free)
- Settings: `experiments/006-body-control/warp_config.json`, intensity `B-strong-v2`. Script `scripts/body_warp.py` gains `arm_mode: linear`: each forearm's shift grows evenly from the elbow row (y=1000) to the wrist row (front y=1320, three-quarter y=1300), then stays constant across the hand. The forearm stays straight, pivoting at the elbow, instead of bowing.
- Knee taper lengthened: outer/back profiles now step down at about 1620/1600 → 1760/1740 → 0 at 1880 (B-strong reached 0 at 1830). Hip and upper-thigh keyframes are unchanged.
- Outputs:
  - `experiments/006-body-control/warp/front-B-strong-v2.png` (`ca6539a2…`)
  - `…/three-quarter-B-strong-v2.png` (`160b8969…`)
  - Review sheets in `experiments/007-reconstruction/`: `v2_compare.jpg` (equal scale), `v2_zoom.jpg` (1:1 forearm, hand and knee crops) and `v2_vs_bstrong_diff.jpg`.
- B-mid and B-strong re-rendered byte-identical (hashes unchanged), so the warp is reproducible.
- **Measured vs B-strong** (automatic legging outline):

| | B-strong | B-strong-v2 | Δ |
|---|---|---|---|
| Front hips (outer span) | 539 | 531 | −1.5% |
| Front upper thigh (outer / single leg) | 506 / 249 | 499 / 245 | −1.4% / −1.6% |
| Front mid thigh (outer / single leg) | 472 / 225 | 480 / 229 | +1.7% / +1.8% |
| Front knee | 368 | 374 | +1.6% |
| Three-quarter glutes | 430 | 430 | 0% |
| Three-quarter upper thigh | 334 | 336 | +0.6% |
| Three-quarter waistband | 229 | 230 | +1 px |
| Pixels changed above waistband / below knee+60 | 0 / 0 | 0 / 0 | n/a |
| Max hand/arm shift (vs Version A) | 40.5 / 14.2 | 36.5 / 10.9 | n/a |

- All within ±2% of B-strong. **The small front-hip drop is a measuring effect:** the straightened forearms sit slightly closer to the body and hide a little more of the hip edge. The hip displacement profile is identical. **Versus Version A, front hips remain +13.9%** (531 vs 466) by this occlusion-limited measure.
- **Where v2 differs from B-strong:** only the forearms and hands, and the outer thigh-to-knee edge band (rows 1000–1899). No background, face, upper-body or shoe changes.
- Claude's subjective look:
  - The forearms read straighter, with natural elbow-to-wrist alignment.
  - The thigh-to-knee transition is visibly smoother and longer, with no loss of upper-thigh fullness.
  - Three-quarter: glutes unchanged, slightly smaller hand shift.
- **Artifacts still present (honest):**
  1. A **thin light line where the front forearms meet the hip edge**, inherited from B-strong (background pixels squeezed between arm and hip). It sits in the outline band, which R1's interior mask leaves untouched, so it would need R2's broad blend, R3, or a small manual touch.
  2. **Legging shading is still warp-stretched** across the front thighs. This is the paid reconstruction's job.
  3. Front hands remain shifted outward (up to 36 px vs Version A) because they follow the widened thighs. Their shape is not distorted.
- No new background, fabric or contour artifacts seen at 1:1 in the zoom crops.

### Decision (Step 1)
Founder (after ChatGPT review, 2026-10-25): **B-strong-v2 approved** as the reconstruction starting point for both views. Forearms and knee transitions are improved, and B-strong fullness is adequately preserved.

### Step 1b — pre-checkpoint fixes (free)
- **Arm/hip light-line fix** (founder item 1): `scripts/fix_arm_sliver.py`.
  - Light runs under 7 px wide (found by a horizontal morphological opening of luma > 170, plus their anti-aliased fringe) in rows 1000–1330 are filled with a blend of their neighbours, then lightly smoothed vertically **inside the repaired strip only**.
  - The real arm-to-waist background gap is wider and left untouched. Front thigh-gap columns 780–920 are excluded.
  - Two earlier versions were rejected after 1:1 inspection: one used a colour classifier that missed the shadowed arm edge; one used a per-row fill that left a dashed line.
  - Outputs: `experiments/007-reconstruction/front-B-strong-v2-fixed.png` (`4588c038…`) changes 3,775 px; `three-quarter-B-strong-v2-fixed.png` (`de2c74e8…`) changes 3,293 px.
  - All changes are in rows 1000–1329 at the forearm/hip contact. **0 px above y=1000, 0 below y=1330.** Silhouette unchanged. Summary: `sliver_fix.json`.
  - A first run spilled 13 px above y=1000 in the three-quarter view through the smoothing margin; it was clamped and re-run.
- **Approved B-strong-v2 files preserved untouched** (founder item 3): `experiments/006-body-control/warp/*-B-strong-v2.png`, hashes re-verified (`ca6539a2…`, `160b8969…`). The fixed copies are new files.
- **Cleanup masks** (founder item 2): `scripts/reconstruct.py masks` → `experiments/007-reconstruction/masks/`, `masks_preview.jpg`, `masks/mask_checks.json`.
  - Built from the filled legging area (fixes the draft's waistband-seam false positive).
  - Rows start below the waistband seam: front 1160, three-quarter 1185, to 1900.
  - Hands and arms excluded with a 10 px margin.
  - Interior mask = legging area eroded 12 px; broad mask = dilated 20 px.
  - **Verified 0 px overlap with the face and upper body (rows < 1000), the waistband, and hands/arms**, for both masks in both views. All masks sit inside the crop.

### Checkpoint (paid) — approved 2026-10-25
- 6 images, estimate **$0.52**, Exp 007 cap $1.50. Endpoints, prices and parameters re-verified on fal before running:
  - FLUX.1 Fill [pro]: $0.05/MP rounded up; `image_url`, `mask_url`, `seed` returned
  - Z-Image Turbo image-to-image: `strength`, custom `image_size`, `seed` returned
  - Nano Banana Pro Edit: $0.15/image at 2K
- **R1:** FLUX Fill, interior mask, lower-body crop rows 1008–2000 (1696×992), seed 7001. Composited with a 4 px feather that ramps only inside the mask.
- **R2:** Z-Image Turbo image-to-image on the same crop, **strength 0.35** (single documented strength: the midpoint of the proposed 0.30/0.45, low enough to keep the silhouette and hands, high enough to re-render fabric), 8 steps, acceleration none, seed 7001. Composited through the broad mask with an 8 px inside feather.
- **R3:** Nano Banana Pro Edit on the full image, references [fixed target, 2002], 2:3, 2K, seed 7001 (not returned by this model). No compositing.
- Prompts: `experiments/007-reconstruction/prompt_R*.txt` (as proposed). Settings: `recon_config.json`.
- Raw outputs kept in `raw/` and mirrored to OneDrive; composites in `out/`.

### Checkpoint results (6 images)
- **Cost: $0.52** by estimate. R1 2 × $0.10 (no billable-units header returned), R2 2 × $0.01 (2 units each), R3 2 × $0.15 (1 unit each). Exp 007 total $0.52 of the $1.50 cap. Month-to-date ≈ $4.45. No safety flags.
- **Raw outputs kept** (founder item 5): `experiments/007-reconstruction/raw/` (crop or full PNGs plus API responses, mirrored to OneDrive under `…/007-reconstruction/images/`). Composites in `out/` (also mirrored). Both are git-ignored; hashes are in `runs.jsonl`.
- Review files:
  - `recon_compare.jpg`: Version A | target | R1 | R2 | R3, equal scale
  - `recon_face_crops.jpg`
  - `recon_closeups.jpg` plus 1:1 strips `closeup_front_thigh.png`, `closeup_front_armhip.png`, `closeup_3q_glute_armhip.png`
  - `recon_report.json`: measurements, retention, alignment, outside-region and boundary checks

**Technical checks (founder items 1–4)**
| Check | front R1 | front R2 | front R3 | 3q R1 | 3q R2 | 3q R3 |
|---|---|---|---|---|---|---|
| Output size as sent / aligned | **1440×832 returned for a 1696×992 crop: NOT aligned**, rescaled into place | 1696×992 ✓ | 1696×2528 ✓ | **1440×832: NOT aligned**, rescaled | 1696×992 ✓ | 1696×2528 ✓ |
| Pixels changed outside the compositing region | **0** | **0** | n/a (whole image re-rendered) | **0** | **0** | n/a |
| Luma step across the 12 px band boundary (out vs target) | 1.64 vs 1.34 | n/a | n/a | 1.12 vs 0.42 | n/a | n/a |

- **FLUX Fill [pro] appears to cap output at about 1.2 MP**, and returned a slightly different aspect ratio (1.731 vs 1.710). R1 had to be rescaled about 1.18× back into the crop, so the redrawn region is softer and may sit a pixel or two off its surroundings. **Fix for any re-run:** send a narrower lower-body crop of at most about 1.2 MP with 32-multiple sides (e.g. 896×992), so no rescale is needed.
- R1 band boundary: a slightly larger tonal step than in the target (small in absolute terms, about 1 luma level). No visible stretch remains in the 12 px band at 1:1, but see the R1 defects below.

**Fullness retention** (automatic legging outline; vs Version A, and vs the target)
| | Target vs A | R1 | R2 | R3 |
|---|---|---|---|---|
| Front hips | +14.4% | +14.4% (0.0%) | +14.4% (0.0%) | **+11.8% (−2.3%)** |
| Front upper thigh, single leg | +21.9% | +19.4% (−2.0%) | +21.9% (0.0%) | +22.4% (+0.4%) |
| Front mid thigh, single leg | +26.5% | +26.5% | +26.5% | +26.0% (−0.4%) |
| 3q glutes | +11.1% | +11.1% | +11.1% | +11.6% (+0.5%) |
| 3q upper thigh | +13.5% | +13.5% | +13.5% | +13.9% (+0.3%) |
| 3q waistband | +0.4% | same | same | +0.0% |

- Proposal thresholds were front hips ≥ +14%, thighs ≥ +20%, glutes ≥ +10%.
  - **R2 meets all** in both views.
  - R1 meets all except the front upper-thigh single leg (+19.4%, just under +20%, a measurement edge case from the redrawn inner-thigh contour).
  - **R3 misses the front hips** (+11.8%: its silhouette was slightly reduced at the hips). It meets the rest.

**Face (R3 checked independently against 2002, founder item 4)**
- R1 and R2 faces are pixel-identical to the target (outside their masks by construction).
- R3 re-rendered the face. Still recognizably the same woman; beauty mark on the left cheekbone in both views. **But it has drifted:** warmer/redder skin, slightly bolder brows, a more contrasted, more made-up look than 2002.

**Photorealism and defects (Claude's 1:1 inspection; subjective)**
- **R1 (FLUX Fill, interior mask): defects.**
  - A doubled inner-thigh contour with a reddish line near the crotch (front).
  - A dark notch/fold at the front right wrist-to-hip contact.
  - A small dark spot under the three-quarter fingers.
  - Fabric slightly darker than the surrounding original.
  - Plus the resolution/alignment issue above. **Not usable as-is.**
- **R2 (Z-Image i2i, strength 0.35, broad mask): clean.**
  - Smooth, natural fabric.
  - Natural arm/hip contacts (no light line, no notch).
  - No visible seams at the 8 px composite feather.
  - Silhouette exactly preserved.
  - The change from the target is **subtle**: shading is refreshed and smoothed, but it is not a dramatic re-render. Some warp-era shading character may remain.
- **R3 (Nano Banana Pro, full image): the most natural fabric and lighting overall.**
  - Hands redrawn but intact.
  - Background and upper body re-rendered (not pixel-identical).
  - Front hips reduced 2.3% vs the target, and the face drifted as above.
- No method shows new background warping. Knees look smooth in all three.

### Technical summary at checkpoint
- R2 best satisfies the constraints (shape and identity exact, clean, cheap) but is a light-touch refresh.
- R3 looks most natural but slightly slims the front hips and drifts the face.
- R1 needs a re-run at ≤ 1.2 MP crop size and still showed contour defects.

### Decision (checkpoint review)
Founder + ChatGPT (2026-10-25):
- **R1 rejected:** visible contour and contact-point artifacts.
- **R2 (strength 0.35) is the preferred reconstruction method so far.**
- R3: polished, but facial styling drift and reduced front hip fullness.
- **R2 front and three-quarter shortlisted as provisional Version B reconstructed candidates:**
  - `experiments/007-reconstruction/shortlist/B/front-R2-s035.png` (`5eae9d12…`)
  - `…/three-quarter-R2-s035.png` (`f8d1cddf…`)
- Version A preserved as a valid alternative. **Neither physique is canonical.**
- No further FLUX Fill or global Nano Banana spend this checkpoint. R1 and R3 are disabled in `recon_config.json` (`enabled: false`), and `scripts/reconstruct.py` skips disabled methods.

### R2 strength comparison (approved by founder 2026-10-25)
- New method `R2-s045` in `recon_config.json`: **identical to R2 except strength 0.45**. Verified programmatically:
  - same endpoint (`fal-ai/z-image/turbo/image-to-image`)
  - same B-strong-v2-fixed inputs, prompts (`prompt_R2_front.txt`, `prompt_R2_3q.txt`), crop rows 1008–2000 (1696×992, custom `image_size` = crop) and broad masks with 8 px inside feather
  - same 8 steps, acceleration none, PNG, seed 7001
  - Keeping the same seed isolates the effect of strength.
- 2 images (front, three-quarter). **Dry-run estimate $0.02** (2 MP × $0.005 each, matching the 2 billable units observed on the R2 0.35 calls). Exp 007 total would be $0.54 of the $1.50 cap.
- Comparison vs R2 0.35, at equal scale and 1:1, on:
  1. fabric texture, tension and shading
  2. retention of B-strong hip, thigh and glute fullness (automatic measurements)
  3. inner-thigh contours and arm/hip contact
  4. compositing seams
  5. exact face and upper-body preservation (changed pixels outside the mask must be 0)
- Rule: **if 0.45 gives no meaningful realism improvement, 0.35 stays the preferred setting.**

### Results — R2 strength 0.45 vs 0.35 (2 images)
- Cost **$0.02** (2 billable units × $0.005 each). Exp 007 total **$0.54** of the $1.50 cap. Month-to-date ≈ $4.47. Seed 7001 returned for both; no safety flags.
- Both outputs 1696×992, **aligned**. **0 pixels changed outside the broad mask** in both views, so the face and upper body are exactly preserved.
- Raw outputs: `raw/*-R2-s045.png` (+ responses), mirrored to OneDrive. Composites: `out/*-R2-s045.png`.
- Review sheets:
  - `s045_compare.jpg` (target | 0.35 | 0.45, equal scale)
  - 1:1 strips: `s045_closeup_front_thigh.png`, `s045_closeup_front_armhip.png`, `s045_closeup_front_knees.png`, `s045_closeup_3q_glute_armhip.png`, `s045_closeup_3q_thigh_knee.png`
- How much the image changed inside the mask (mean absolute difference from the target): front 3.67 → 5.13, three-quarter 3.90 → 5.57. So 0.45 alters more, as expected.

| Retention vs Version A (vs target) | R2 0.35 | R2 0.45 |
|---|---|---|
| Front hips | +14.4% (0.0%) | +14.4% (0.0%) |
| Front upper thigh, single leg | +21.9% (0.0%) | +21.9% (0.0%) |
| Front mid thigh, single leg | +26.5% (0.0%) | +25.4% (−0.9%) |
| **3q glutes** | +11.1% (0.0%) | **+6.2% (−4.4%)**: fails the ≥ +10% threshold |
| 3q upper thigh | +13.5% (0.0%) | +11.5% (−1.8%) |

- Comparison on the founder's five points (Claude, 1:1):
  1. **Fabric texture, tension and shading:** no meaningful realism gain at 0.45. The fabric looks about the same, just more altered.
  2. **Fullness:** front held. **The three-quarter glute contour was pulled in** (−4.4% depth; visibly smaller curve).
  3. **Contours and contacts: worse at 0.45.**
     - An odd fabric "tab" at the top of the front thigh gap.
     - **The light streak at the front wrist/hip contact reappeared** (the artifact fixed before the checkpoint).
  4. **Seams: worse at 0.45.** In the three-quarter view, a pale **ghost band** remains where the original glute outline was, inside the broad mask (the model redrew a smaller glute and left the vacated area light). Visible even at full-length scale.
  5. Face and upper body: exactly preserved in both (0 px outside the mask).

### Decision (strength comparison)
Per the founder's rule (if 0.45 brings no meaningful realism improvement, keep 0.35): **0.45 brings no improvement and adds defects, so R2 at strength 0.35 remains the preferred setting.** The R2 0.35 outputs remain the shortlisted provisional Version B reconstructed candidates. R2-s045 is disabled in the config. Version A untouched; nothing canonical.

### Final decision (Experiment 007 closed)
Founder + ChatGPT (2026-10-25):
- **R2 at strength 0.35 confirmed** as the preferred reconstruction setting. **Strength 0.45 rejected** (reduced glute projection, ghost contours, contact artifacts).
- **R2 0.35 front and three-quarter outputs kept as provisional Version B body references** (`experiments/007-reconstruction/shortlist/B/`).
- Version A preserved as a valid alternative. **Neither body direction is canonical.**
- **Reconstruction testing complete.** No further tuning of the same studio photographs.

### Next Experiment
Experiment 008: identity and body-shape transfer to new outfits, poses and environments. Proposal: `experiments/008-identity-body-transfer/PROPOSAL.md` (approved 2026-10-25 with adjustments).

---

## Experiment 008 — Identity and Body-Shape Transfer
Date: 2026-10-25
Status: Approved 2026-10-25 for **2 images**, $0.50 cap. **Run complete; paused for founder + ChatGPT review.**

### Hypothesis
Nano Banana Pro, given 2002 (face) and the Version B R2 0.35 front and three-quarter images (body), can produce the same woman with Version B fullness in new outfits, poses and real environments, rather than reverting to a default slimmer body.

### Setup
- Settings: `experiments/008-identity-body-transfer/config.json`. Prompts: `prompt_8-1.txt`, `prompt_8-2.txt`.
- Nano Banana Pro Edit, 2:3, 2K, PNG, fal default safety settings. **Price and parameters re-verified on fal before running:** $0.15/image (4K would be double); up to 14 references; 2:3 and 2K supported.
- References in order:
  1. 2002 (face)
  2. Version B front R2 0.35 (body)
  3. Version B three-quarter R2 0.35 (body)
  - All hash-checked. Version A is not sent; it is the slim comparison point only.
- **8-1** (seed 8001): city sidewalk, facing the camera. **Adjustment 1:** realistically fitted, slim-cut, high-waisted stretch-denim jeans that clearly show the hip and upper-thigh silhouette (replacing straight-leg jeans), white ribbed tank top, white sneakers.
- **8-2** (seed 8002): apartment kitchen, true three-quarter view. **Adjustment 2:** fitted oatmeal knit dress. She stands in front of the counter with fingertips on its edge; the counter, arms and fabric explicitly must not hide the waist, hips, glutes or upper thighs, and there are no loose folds over the lower body.
- **Adjustment 3:** the B-retention index is **supporting evidence only** (clothing, stance, rotation and perspective affect the ratios). A **separate qualitative judgement** of whether Version B fullness is still visually recognizable is required.
- Estimate $0.30.

### Results (2 images)
- Cost **$0.30** (2 × $0.15). Exp 008 total $0.30 of the $0.50 cap. Month-to-date ≈ $4.77. Both 1696×2528; no safety flags; no seed returned (Nano Banana Pro). Reference hashes verified before the run (generate_fal check).
- Files in `experiments/008-identity-body-transfer/`:
  - `contact_sheet.jpg`
  - **`body_comparison.jpg`**: each output | Version A | Version B, equal scale
  - **`face_crops.jpg`**: 2002, both B references, both outputs
  - `measurements.json`, `runs.jsonl`, `review.csv`
  - Originals are local and mirrored to OneDrive.

**Transfer quality**
- Both outputs used the requested new outfit, pose and environment. **No copying** of the studio, taupe set or reference poses.
  - 8-1: sunlit city sidewalk, slim-cut stretch jeans, white ribbed tank, white sneakers.
  - 8-2: kitchen, fitted oatmeal ribbed knit dress.
- Photorealism looks high in both (natural light, believable skin and fabric, hands fine).
- **8-2 pose deviation:** rendered near side-on (about 80–90°) with her body turned toward the counter, not the requested true 45° three-quarter view. The counter and arms do not hide the hips or glutes.

**A. Facial identity (scored separately)**
- 8-1: a strong match to 2002 (face shape, brows, eyes, nose, lips, hair). **Beauty mark on the left side, but it sits lower, toward the jaw near the mouth, instead of on the cheekbone:** a position drift.
- 8-2: the same woman; a natural open smile changes the expression. Beauty mark on the left cheekbone ✓. Slight styling difference from the smile and warm light; no strong "polished" drift.
- No scar in either. Face crops about 340 px: identity judgeable, fine detail limited.

**B. Body shape (measurements = supporting evidence; qualitative judgement separate)**
| 8-1 front (manual, ±10 px) | Version A | Version B | 8-1 |
|---|---|---|---|
| Shoulders | 560 | 560 | 560 |
| Waist | 315 | 315 | **355** |
| Hips | 467 | 528 | 510 |
| Upper thigh, single leg | ~211 | ~242 | ~242 |
| B-retention index: hip ÷ shoulder | 0 | 1 | **0.7** |
| B-retention index: thigh ÷ shoulder | 0 | 1 | **1.0** |
| B-retention index: hip ÷ waist (curve contrast) | 0 | 1 | **-0.24** |

- 8-1 caveats: the waist is measured over a fitted ribbed tank (fabric may add width); denim adds thickness at the hips and thighs.
- 8-2: **pose-limited, no index.** Output depth ratio 1.40 (glute 350 / waist 250 px) vs about 1.46 (A) and 1.62 (B) in the 45° references. Not comparable because of the side-on rotation.
- **Qualitative (Claude), the deciding judgement per founder adjustment 3:**
  - **8-1: Version B fullness is NOT clearly recognizable.** Despite near-B widths at the hips and thighs, the figure reads as a slim, straight, athletic body. The waist reads wider and the waist-to-hip curve is weaker than even Version A, and the legs look slim in the jeans. Visually closer to Version A than to Version B. **Verdict: face transfers; body partly regresses toward the default slimmer figure.**
  - **8-2: partially recognizable.** The glutes are clearly rounded and projected in profile (the strongest Version B trait carried over). The hips and upper thighs read slim, the overall silhouette is slimmer than B, and the side-on pose prevents a like-for-like comparison. **Verdict: face transfers; body partly preserved (glutes), partly regressed (hips/thighs); pose deviated.**

**C. Waist and bust**
- Bust natural and not enlarged in either. 8-1's waist did not narrow (it reads wider).

### Interpretation (technical, for review)
Nano Banana Pro transfers the **face** reliably into new scenes, but **body references alone do not reliably carry Version B's fuller lower body**. The model drifts toward a slimmer, straighter default, most visibly in the front view. Two images is a small sample.

### Decision / direction change
Founder reassessment (2026-10-25):
- The real goal is **believable, high-quality social-media content** (Instagram photos, Reels, short videos) featuring the fictional adult character.
- Exp 008 showed the main problem: the photos are attractive and technically photorealistic but still **look obviously AI-generated and overly staged**.
- **Stop optimizing body proportions in isolation.** The key question is now whether believable content can be produced **repeatedly**.
- Keep 2002 as the face anchor. Keep **both** Version A and Version B body references; neither is canonical.

### Next Experiment
Experiment 009: smartphone-style photographic believability and an early image-to-video proof of concept. Proposal: `experiments/009-realism-video/PROPOSAL.md` (direction approved 2026-10-25; Part 1 only).

---

## Experiment 009 — Smartphone Believability (Part 1: stills)
Date: 2026-10-25
Status: Direction approved by founder (after ChatGPT review). **Part 1 only authorized: 4 stills + free phone-pass variants, about $0.60.** Video NOT approved. **Part 1 complete 2026-10-25; paused for founder, ChatGPT and blind human review.**

### Hypothesis
With prompts aimed at ordinary smartphone photography (phone optics, real light, lived-in settings, candid posing, unretouched skin), Nano Banana Pro can produce stills of the same woman that ordinary viewers would not immediately identify as AI.

### Setup
- Settings: `experiments/009-realism-video/config.json`. Prompts: `prompt_S{1,2}-{A,B}.txt`. Nano Banana Pro Edit, **9:16, 2K**, PNG, fal default safety settings, $0.15/image (re-verified on fal earlier today).
- References in order: 2002 (face), then the body front and three-quarter for **Version A or Version B**. Both versions are kept; neither is canonical. All hash-checked.
- Arms:
  - **S1** mirror selfie in a lived-in hallway (A seed 9101, B seed 9102)
  - **S2** friend-taken photo outside a coffee shop (A seed 9103, B seed 9104)
- Founder adjustments applied:
  1. **S2 simplified:** iced coffee in one hand, the other hand relaxed at her side, a small candid smile, standing naturally. No laughing or hair movement.
  2. Prompts now say: "Prioritize ordinary, everyday photographic believability over beauty or polish… not a fashion shoot, not a campaign, not stock photography."
  3. **Originals and phone-pass variants are kept separately.**
     - `scripts/phone_pass.py`: 1080×1920 crop/resize, unsharp mask 1.2/60%/2, shadow-weighted luminance noise σ 1–4, JPEG q82 4:2:0, saved as PNG.
     - The originals' blind copies get the same 1080×1920 crop/resize and nothing else.
     - `scripts/blind_set.py` shuffles all 8 under random codes. The key `blind_key.json` is git-ignored; only its SHA-256 is committed.
     - **The phone pass is not assumed to improve realism.**
  4. Face, body and photographic realism are assessed separately.
  5. **Blind human evaluation procedure:** `BLIND_REVIEW.md`, with the form `human_ratings.csv`, kept separate from `claude_assessment.csv` (and ChatGPT's).
  6. **Mandatory video gate:** no image-to-video unless at least one still passes identity (≥ 4/5) and realism (overall ≥ 4/5) with no major artifacts, **and** the founder separately approves video.
  7. **Fallback rule:** if the stills remain obviously AI-generated, stop and propose a different still-image approach, e.g. a real photographic background as the base.
- Cap $0.75 (estimate $0.60).

### Results — Part 1 (4 stills)
- Cost **$0.60** (4 × $0.15). Exp 009 total $0.60 of the $0.75 cap. Month-to-date ≈ $5.37. All 1536×2752 (9:16); no safety flags; no seeds returned.
- Files in `experiments/009-realism-video/`:
  - `contact_sheet.jpg` (references + 4 originals)
  - `face_crops.jpg`
  - **`blind_sheet.jpg`**: 8 coded images, originals and phone pass shuffled
  - `blind_key.sha256`
  - `claude_assessment.csv`, `claude_blind_variant_ratings.csv`, empty `chatgpt_assessment.csv` and `human_ratings.csv` templates
  - `BLIND_REVIEW.md`
- Originals: local `images/` plus OneDrive. Blind PNGs for reviewers: OneDrive `…/009-realism-video/blind_for_reviewers/` (8 × 1080×1920 PNG plus instructions). The sealed key is backed up as `SEALED_blind_key.json`.

**Claude's assessment** (not blind to scenario or body version; separate from ChatGPT and humans)
| Still | Face (vs 2002) | Body reads as intended? | Realism sub-scores (skin/camera/env/light/pose) | Overall "would a scroller suspect AI" | Video gate |
|---|---|---|---|---|---|
| S1-A mirror selfie, A | **3/5**: looking down at the phone, face rounder and younger-looking; mark not clearly visible | 4 (A) | 4/4/4/4/4 | **4** | no: identity < 4 |
| S1-B mirror selfie, B | **3/5**: same rounder, younger look; mark on left cheek, **mirror-correct side** | **2: reads like A (regressed)** | 4/4/4/4/4 | **4** | no: identity < 4 |
| S2-A coffee shop, A | **4/5**; mark left cheek | 4 (A) | 4/4/4/4/4 | **3**: gibberish chalkboard text | no: realism < 4 |
| S2-B coffee shop, B | **4/5**: best match; mark left cheek | **2: reads slim (regressed)** | 4/4/4/4/4 | **3**: gibberish chalkboard/window/awning text | no: realism < 4 |

- **Big improvement over Exp 008.** At feed size these read like ordinary phone photos:
  - phone optics: deep focus, wide perspective, tilted framing
  - mixed real light
  - lived-in clutter, lint on the leggings, mirror smudges
  - passers-by and reflections
  - candid expressions
- By Claude's judgement they are **not "obviously AI-generated"**, so the fallback rule (real-photo backgrounds) is not triggered.
- **Remaining AI tells:**
  - **gibberish text** on the chalkboards and signage (S2, the main giveaway on a closer look)
  - an overly uniform dust/speck pattern on the mirror (S1)
  - a real-brand logo on sneakers (S1-B), a publishing concern rather than a realism one
- **Face consistency is weaker in the mirror selfies** (downward gaze, phone partly covering the face, rounder/younger read) than in the friend-taken photos.
- **Body:** consistent with Exp 008. **Version B references do not produce a recognizably fuller body.** Both B stills read like Version A. Version A stills match A.
- **Phone pass (rated blind, without the key):** original and processed variants are **indistinguishable at feed scale**. At 2× one of each pair is slightly crisper and grainier. No realism preference from Claude; human ratings will decide. Not assumed to help.

### Video gate status
**Not met by Claude's assessment:** no still has identity ≥ 4 **and** realism ≥ 4 with no notable artifacts.
- S1 stills fail on identity.
- S2 stills fail on garbled text.
- Pending ChatGPT and blind human review. **No video generated. Video requires separate founder approval anyway.**

### Decision
Founder + ChatGPT assessment (2026-10-26):
- **S1-A and S1-B are the most promising for everyday smartphone realism**, but both show noticeable facial drift vs 2002.
- S2-A and S2-B have stronger facial consistency, but background signage and lettering remain obvious AI artifacts.
- Both Version B outputs regress toward Version A's slimmer body.
- The phone-processing pass shows no realism advantage yet.

Decisions:
1. **Video generation not authorized.**
2. **All four originals and their processed variants preserved.** Originals are set read-only; `variants/`, `blind/` and the sealed key are kept.
3. **Blind human ratings to be collected** with the existing procedure (`BLIND_REVIEW.md`), without revealing the original/processed mapping.
4. A minimal correction experiment (face consistency for the mirror image, realistic signage for the café image) to be proposed.
5. Keep the casual smartphone style. 6. No further body-shape refinement unless a specific shot needs it. 7. Version A and Version B stay separate and provisional.
- **Priority:** one convincing, identity-consistent photo to serve as the first video-test input.

### Next Experiment
Experiment 010: minimal image correction. Proposal: `experiments/010-correction/PROPOSAL.md` (2-image checkpoint approved 2026-10-26).

---

## Experiment 010 — Minimal Image Correction (2-image checkpoint)
Date: 2026-10-26
Status: Approved by founder (after ChatGPT review): **one face correction (S1-A) and one signage correction (S2-A)**, about $0.30. Remaining variants and video not approved. **Checkpoint complete 2026-10-26; paused for review.**

### Setup
- Bases copied from Exp 009, hash-verified against Exp 009 `runs.jsonl`:
  - `experiments/010-correction/base/009-S1-A-seed-9101.png` (`392ee08f…`)
  - `…/009-S2-A-seed-9103.png` (`0452a0f1…`)
  - **The Exp 009 originals stay read-only, and the sealed blind key is unchanged** (SHA-256 still `6db95176…`).
- Method: Nano Banana Pro Edit (9:16, 2K) on the whole photo, then `scripts/local_composite.py` pastes the edit back **only inside a hand-drawn mask** (alpha ramps up inside the mask; exactly 0 outside). It checks that sizes match (no rescaling), counts changed pixels outside the mask (must be 0), and reports how much the edit drifted elsewhere.
- Masks (`experiments/010-correction/masks/`, `masks.json`, previews `mask_preview_S1-A.jpg` / `mask_preview_S2-A.jpg`):
  - **S1-A face:** face and ear, hairline to chin. It stops at x=733, so the phone, its camera reflection and the fingers are excluded. 6 px inside feather.
  - **S2-A signage:** the visible chalkboard face, cut around her strap, bag and jeans (widened once after a preview showed garbled fragments left uncovered beside the bag), plus the reflected board above the window sill. 4 px inside feather.
- Prompts (`prompt_C1-face.txt`, `prompt_C2-signage.txt`), with founder adjustments:
  1. C1 keeps her original downward gaze, expression, head angle, lighting, skin texture and the phone reflection. The face must resemble 2002 without looking pasted in. **Mirror check:** the beauty mark is on the left side of the picture (the cheek nearer her visible ear), the anatomically correct side in a reflection.
  2. C2 uses minimal readable lettering ("COFFEE" / "& PASTRIES" only, no other words or drawings). The window reflection is soft, low-contrast and unreadable, not artificially sharp. The rest of the photo is preserved.
  3. Localized compositing, 1:1 edge checks, zero changed pixels outside the masks.
  4. Exp 009 photos and the sealed blind set preserved.
- Seeds 10001 (C1), 10002 (C2). Cap $0.40.

### Results (2 edits)
- Cost **$0.30** (2 × $0.15). Exp 010 total $0.30 of the $0.40 cap. Month-to-date ≈ $5.67. Both edits returned at 1536×2752, the same size as the bases (no rescaling). No safety flags.
- Raw edits: `experiments/010-correction/images/` (local and OneDrive).
- **Corrected candidates (composited):**
  - `experiments/010-correction/candidates/S1-A-facefix.png` (`dcb83338…`)
  - `…/S2-A-signfix.png` (`6ff697ec…`)
- Review files:
  - `compare_S1-A.jpg`, `compare_S2-A.jpg` (original | corrected, full frame)
  - `closeup_S1-A_face.jpg`, `closeup_S2-A_sign.jpg` (1:1)
  - `face_crops.jpg` (2002 | S1-A original | S1-A corrected | S2-A)
  - `mask_preview_*.jpg`

| Check | S1-A face fix | S2-A signage fix |
|---|---|---|
| Changed pixels outside mask | **0** | **0** |
| Edit drift outside mask (how much the model altered the rest of the frame) | 3.81, well aligned | 13.73, re-rendered more, so the mask edges were checked closely |
| Mask edges at 1:1 / 2× | No visible seam at hairline, chin or phone boundary; grain and light continuous | No visible seam at bag, jeans or window sill |

**Claude's assessment** (separate from ChatGPT and humans)
- **S1-A face fix:**
  - Identity **improved from 3 to 4/5**: brow shape, eye shape, nose and lips now read as the 2002 woman.
  - Beauty mark visible on the **left of the picture (cheek nearer her visible ear), correct for a mirror reflection**.
  - Downward glance, smile, head angle and phone reflection kept. The gaze is slightly less downcast than the original.
  - **Drift: the face is more groomed than the original** (bolder, shaped brows, more defined lips and contour, smoother and more matte skin). At 1:1 it is slightly smoother than the surrounding photo. At feed scale it sits naturally.
  - Realism **4/5**, no major artifacts. **Video gate: borderline pass (polish flagged).**
- **S2-A signage fix:**
  - Board reads "COFFEE" / "& PASTRIES", with her jeans naturally hiding part of "PASTRIES"; real chalk texture and an erased smudge.
  - **No gibberish remains anywhere in the frame** (the licence plate is too small to read, which is normal).
  - The window reflection shows the sign **mirror-reversed (physically correct) but more legible than requested** (asked for soft and unreadable). Plausible, not artificially sharp.
  - Face unchanged (identity 4/5).
  - Realism **4/5**, no major artifacts. **Video gate: pass.**
- **Technical recommendation:** S2-A signfix is the safer first video input (no face edit, strong identity, the main giveaway removed). S1-A facefix is the alternative if the founder prefers the mirror selfie's realism and accepts the slightly polished face.

### Decision
Founder (2026-10-26): reassess the technical and commercial direction.
- After 10 experiments (≈ $5.67), believable, repeatable social video is not yet proven.
- **Stop proposing incremental corrections to the same photographs as the default workflow.**
- A strategic pipeline review was requested, comparing:
  1. Nano Banana Pro reference + local edit
  2. Runway Gen-4 References
  3. Kling Elements
  4. a trained character LoRA
  5. real photographic backgrounds + character generation
- Plus a two-workflow still benchmark and an immediate 5 s image-to-video test on S2-A signfix.
- All references and both body versions retained; nothing canonical.

### Next
- Strategy review: `STRATEGY_REVIEW.md`.
- Proposed Experiment 011 (pipeline benchmark + first motion test): `experiments/011-pipeline-benchmark/PROPOSAL.md` (direction approved 2026-10-26; Part A approved; Part B replaced by a 4-image pilot proposal).

---

## Experiment 011 — Pipeline Benchmark
Date: 2026-10-26
Founder decisions (after ChatGPT review of `STRATEGY_REVIEW.md`):
1. **Part A approved:** the first video comparison on the corrected S2-A café photo. A1 Gemini Omni Flash 1.1 (5 s, 720p) and A2 Kling v3 Pro with Elements (5 s, audio off). About $1.06, cap $1.25. **Simplified motion prompt** (founder text, used for both). Verify schemas and prices first; keep raw videos; extract frames; stop after the two videos.
2. **Part B modified:** no 16-image run yet. First a **4-image pilot in one scene** (W1-A, W1-B, W2-A, W2-B), with W2 on a **rights-clean real background**, explicitly testing whether W2 *preserves* the photograph's environment (lighting, geometry, perspective, objects, text) instead of regenerating it. The background, prompts, costs and evaluation are to be presented for approval first.
3. **No automatic LoRA recommendation from a pass threshold.** Diagnose the bottleneck (face identity, body identity, backgrounds, posing, general photorealism) and recommend training only if it addresses the demonstrated bottleneck and a clean, consistent dataset exists.

### Part A — setup (verified 2026-10-26 before spending)
- Settings: `experiments/011-pipeline-benchmark/partA/video_config.json`. Prompts: `prompt_A1_omni.txt`, `prompt_A2_kling.txt` (the same founder text; Kling adds "@Element1 is the woman."). Script: `scripts/video_gen.py` (fal queue API, ledger, cap check).
- **Start frame:** `experiments/010-correction/candidates/S2-A-signfix.png` (`6ff697ec…`), sent as JPEG q95 at 1072×1920 to keep the request small (outputs are 720p).
- **A1 Omni Flash 1.1** (`google/gemini-omni-flash/v1.1/image-to-video`): schema verified (`image_url`, `aspect_ratio` 16:9/9:16, `resolution` 360p–4k, `duration` integer seconds). $0.10/s at 720p. **No audio parameter exposed**, so any audio is stripped before review. Sent: 9:16, 720p, 5 s.
- **A2 Kling v3 Pro** (`fal-ai/kling-video/v3/pro/image-to-video`): schema verified (`start_image_url`, `duration` 3–15, `generate_audio`, `elements` [frontal_image_url + reference_image_urls]). **$0.112/s audio off** ($0.56 / 5 s). Aspect follows the start image.
  - Element @Element1: frontal = 2002 face crop; references = S2-A face crop + Version A front body reference. Kling's page says references are optional and the API schema says at least one, so sending them satisfies both.

### Part A — results (2 clips)
- Cost **$1.06** (A1 $0.50 + A2 $0.56). Within the $1.25 cap. Month-to-date ≈ $6.73.
- **Outputs:**
  - A1 Omni: 720×1280, 24 fps, 5.03 s, with an AAC audio track (stripped for review); generated in 47 s.
  - A2 Kling: 1076×1924 (follows the start frame), 24 fps, 5.04 s, no audio; generated in about 5 min.
- Raw videos: `partA/raw/` (local; mirrored to OneDrive `…/partA/images/`). Silent review copies on OneDrive `…/partA/review/`. Videos are git-ignored; hashes are in `runs.jsonl`.
- Review sheets (committed): `frames_sheet.jpg` (full frames at 0 / 1.25 / 2.5 / 3.75 / 4.95 s) and `face_frames.jpg` (2002 + upper-body/face crops per frame). Extra frames at 0.6 / 1.9 / 3.1 / 4.4 s are local.
- **Limitation:** Claude judges from extracted frames, not playback. Temporal smoothness, flicker and motion feel need the founder, ChatGPT and human viewers to watch the clips.

**Claude's frame-based assessment** (separate from ChatGPT and humans; `partA/claude_assessment.csv`)
| | A1 Omni Flash | A2 Kling + Elements |
|---|---|---|
| Face consistency across frames | Same woman throughout (4/5). Late frames straighten her head; the face reads slightly smoother and more symmetric | Same woman throughout (4/5). More natural head tilt; a natural blink at about 4.4 s; holds detail better |
| Body stability | Stable; jeans, top and bag consistent | Stable |
| Background stability | Passer-by walks naturally; cars, bike and reflections coherent; **sign stays legible ("COFFEE / & PASTRIES")** | Same: plausible passer-by, legible sign, coherent reflections |
| Camera | **Drifts and reframes more than "very gentle"** (a noticeable pan) | Similar drift, slightly less |
| Motion naturalness | Small smile and posture shift; somewhat calm and "settled" | Smile, head tilt and blink read more lifelike |
| Overall "real phone video?" | 3/5 | **4/5** |
| Resolution | 720p | about 1080×1920 |

- **Technical read:** both preserve identity and environment far better than expected for a first test, with no morphing, background boiling or sign corruption visible in the frames.
- Kling + Elements looks more lifelike and sharper, at about the same cost ($0.56 vs $0.50). Omni is about 6× faster and allows cheap 360p drafts.
- Both camera motions overshoot the prompt. A future prompt might specify "locked-off, almost static handheld".

### Part A — decision
Pending founder + ChatGPT review (and optional blind human viewing). No further video without approval.

### Part B — pilot proposal
`experiments/011-pipeline-benchmark/PILOT_B_PROPOSAL.md`: kitchen scene, W1 vs W2 × Version A/B, 4 images ($0.60). Background: the founder's own phone photo (recommended, with a text probe) or a founder-approved Unsplash photo. Environment-preservation tests: edge overlay, outside-silhouette pixel difference, object checklist, text probe. **Pending founder approval and the background.**

---

## Production Platform Pivot — Higgsfield + fal Nano Banana (2026-10-27)

**Status:** Real user-run platform tests reviewed in chat; operational direction changed. This is **not** an additional paid GitHub/Claude Code experiment and does **not** replace the existing research-branch character references. See `PRODUCTION_PLAYBOOK.md` for live procedures and `PRODUCTION_ASSET_REGISTER.md` for asset provenance.

### Direction and identity
- The founder determined that the initial custom face/body reconstruction and iterative patching were **not an efficient direct route to believable, repeated Instagram/TikTok content**.
- Ready-made platform workflows now take precedence over model training: **Higgsfield Genjutsu Motion Transfer for videos**, and **Nano Banana Pro Edit on fal.ai for still photos**.
- The founder created a paid Higgsfield account, generated a **blonde** adult character with long blonde hair, hazel eyes, lightly tinted aviator-style glasses, beige coat and burgundy trousers, and explicitly decided to **keep that character look**.
- This **working blonde production persona** must stay **separate** from prior **brown-haired portrait 2002** and unselected Version A/B body experiments, which remain preserved and useful historical research. No portrait/body references are promoted or overwritten without specific founder approval.
- Avoid repeated bespoke body warps, unnecessary training or open-ended still-image corrections as the default path. Measure believable results, workflow effort, reference fidelity and post-ready quality instead.

### Video workflow learned from hands-on tests
- **One uploaded motion-reference video** supplies the real performer's movement, timing, posture transitions and camera behavior. Higgsfield allows **additional image references** for the **working blonde character** and a **new location** in its Genjutsu interface. When the UI offers `@` autocomplete, select actual media tags and explicitly assign **VIDEO = motion only, CHARACTER IMAGE = identity only, LOCATION IMAGE = environment only**. Free-text placeholder tags without actual media associations are insufficient.
- The **initial Motion Transfer video** used an Instagram source captured via Windows Snipping Tool and cropped on desktop. Movement generally followed the reference, but background/export sharpness was an unresolved concern.
- A **phone-downloaded version** of the Instagram motion reference was tried with **apparently Object Swap** (the founder was not completely certain about the selected mode). **Failure:** the original street scene/Instagram watermark remained, and the new character's face drifted toward the source performer's appearance. A higher-quality source did not fix mode-specific identity/background leakage.
- The source video was discovered to be a landscape video with **black sidebars around a narrower vertical image**. Correct media prep: crop sidebars *without cropping into or needlessly enlarging the actual vertical footage*; trim any terminal Instagram-logo bumper when working with authorized footage. A raw 1920×1080 container does **not** mean the embedded vertical video has 1080p width.
- **Best user-reviewed Motion Transfer:** source movement + blonde character + **clean Milan street image** as a location reference, with explicit role-specific tags/prompt. Result was approximately **9 seconds, 720×1280 at 24 fps**, and successfully recreated a different environment with closely matched gestures, significantly reduced face bleed and no Instagram watermark. Remaining defects included some artificial smoothing of movement, softer facial details at close distance, and slightly static/less dynamic scene behavior. **Promising proof-of-concept; not yet demonstrated scalable or foolproof.**
- The Milan location photo supplied in chat originally had a prominent foreground person and social carousel controls. A **new cleaned/generated image** was created for use as a scene reference. This was a generated reconstruction and must **not** be presented as a pixel-preserving edit of an original real photograph.
- **Current mode choice:** use **Motion Transfer** to move existing authorized choreography into a **different** location; reserve **Object Swap** for cases where retaining the source's real filmed location is actually desired. Real location-photo guidance is beneficial but does not guarantee exactly preserved background pixels.

### Photo/profile-picture workflow learned from hands-on tests
- Higgsfield requested an upgrade for additional photo capabilities; the founder instead tried **fal.ai Nano Banana Pro Edit** using multiple reference images.
- Photo concept: working blonde influencer takes a **G63 driver-seat selfie** wearing the founder-supplied **white Gucci short-sleeve collared blouse with a fitted smocked waist**, in a black-and-ivory **G63 cabin** with white quilted seats, circular vents and premium dashboard. She wears tinted sunglasses and makes a soft **kissing/pout** expression.
- Initial Nano Banana image used these references but had the **wrong camera placement** (off-center / upper-side angle). An additional **ChatGPT-generated composition reference** showed exactly the desired camera geometry: phone **directly in front of her at belly/lap level**, tilted **upward**, with her face pointing forward. The founder explicitly accepted **this angle**. This approval does **not** select a final canonical face or profile-photo file.
- Profile-photo working settings: **1:1 aspect ratio, 2K, one output**; keep face and sunglasses inside a future circular avatar crop. Preserve plausible driver-side steering-wheel layout, cabin reflections and daylight.
- An actual fal playground validation error occurred because optional `context` contained `[{"type":"","text":""}]` (and `history` was also initially malformed). Clearing it to `[]` or assigning a valid typed text context resolves **input-structure** issues; changing resolution does not.
- For stills, explicitly distinguish **face reference vs blouse reference vs cabin reference** and use model-supported reference URLs/ordering. Higgsfield `@` media tagging should not be assumed to apply to fal's separate playground.

### Evidence, costs and unresolved questions
- Earlier repository-controlled **Exp 011 Part A** was **completed separately** on the **brown-haired research branch**: Omni Flash image-to-video and Kling v3 + Elements made two café clips costing **$1.06**, increasing historically documented API experiment spending from **~$5.67 to ~$6.73**. Their frame review favored Kling, but full playback and founder acceptance were pending in the recorded log. **Do not mislabel these as blonde Higgsfield clips.**
- **The founder bought a Higgsfield plan** and made several paid/free? Higgsfield generations and manual fal image calls. The actual subscription price, credits consumed and manual playground charges have **not been provided or verified in-repo**; thus `$6.73` is **not** an all-inclusive monthly total. Existing **$110/month ceiling includes subscriptions**.
- All newest photos, screenshots, Reel references, generated images and exported videos were shared via **chat**, **not** committed to this GitHub repository. The register records their chat filenames, status and provenance; durable original files/rights records need founder-approved import. Do not invent links, SHA hashes or assert backups.
- Rights of reused Instagram motion footage are **not established**. The download capability, watermark removal or AI setting change does **not** grant a licence for public/commercial derivative publishing. Use original/self-shot or appropriately licensed performances for final social posts. Disclose AI-generated photorealistic assets where required.

### Decision and next action
1. **Active pipeline is documented in `PRODUCTION_PLAYBOOK.md`.** Higgsfield Motion Transfer and fal Nano Banana are practical defaults for the working blonde persona; keep the previous research tools/experiments archived and intact.
2. The Exp 011 Part B four-image **brown-haired** kitchen pilot is **on hold**, not executed; no automatic LoRA training.
3. Next useful controlled run: **one rights-cleared vertical performance, working blonde character, and an intentionally different clean location**; assess motion fidelity, full-speed facial stability, generated scene sharpness and cost.
4. For profile pictures, use the accepted front-facing **belly-level upward** selfie camera angle and verify facial identity against the blonde working reference before publication.
5. Reconcile Higgsfield subscription and platform usage, actual fal playground spend, approved assets and licence status before reporting total spend or launching a production batch.

---

## Experiment 012 — Niche Test for AI Content Services (proposed 2026-10-27)

**Status:** Approved by founder 2026-10-27, spend cap $20. Nothing generated yet. Business-direction test, separate from the persona branches.

- **Why:** The founder is stepping back from the AI-influencer goal to test selling AI product and listing content to small businesses.
- **Design:** 30 personalised pitches across three niches, 10 each: small product brands, real estate agents, clothing boutiques. Each prospect gets 2 private sample images. One demo clip per niche.
- **Tools:** fal Nano Banana Pro Edit ($0.15/image at 2K) and Kling v3 Pro image-to-video ($0.56 per 5 s, audio off). Re-verify prices before running.
- **Budget:** estimate ≈ $16.86, cap $20. Fits within the $84.22 remaining under the $110 monthly cap (see Budget reconciliation below).
- **Gate:** product/room/garment fidelity is checked at 100% zoom before anything is sent.
- **Decision rule:** positive-reply rate × price quoted ÷ minutes per sample, with at least 2 positive replies required.
- **Files:** `experiments/012-niche-test/` (PROPOSAL, OUTREACH, prompts, pitch tracker, review sheet, config template). Prospect photos are git-ignored.

---

## Budget reconciliation (2026-10-27)

- **Higgsfield plan:** $19/month (270 credits/month).
- **fal.ai total to date:** $6.78, founder-reported from the fal dashboard (the repo ledger was ~$6.73).
- **Month-to-date spend:** $25.78 of the $110 cap.
- **Remaining:** $84.22.

---

## Experiment 012 — Portfolio batch, run 1 (2026-10-27)

**Status:** 5 of 7 arms generated; the 2 quarter-zip arms are held. Within the approved $20 Exp 012 cap (batch cap $3.00). No video.

- **Inputs:** the founder's own photos (git-ignored, `portfolio/inputs/`). Each one was made upright (EXIF), cropped to the founder's boxes, downscaled to a long edge of at most 3072 px and saved as JPEG q95. The config hashes both the originals and the copies that were sent.
- **Model:** `fal-ai/nano-banana-pro/edit`, 2K PNG, seed 12001. Price re-checked 2026-10-27: $0.15/image (4K is charged 2x). Products are 4:5 (1856×2304); the room is 4:3 (2400×1792).
- **Arms run:** cologne-bathroom, cologne-dresser, watch-desk, watch-wrist, room-restyle. Prompts are in `portfolio/prompts/`, filled in from the shared templates. `prompts/prompt_realestate_restyle.txt` was drafted from the staging template because the founder-supplied file was not found.
- **Held:** quarterzip-flatlay and quarterzip-model. The crop box (0.000, 0.068, 0.940, 0.778) cuts off the waistband and both cuffs (the garment ends at about y 0.84, and the right cuff reaches the photo edge). Needs a corrected box.
- **Cost:** est. $0.75 (5 × $0.15). Month-to-date ≈ $26.53 of $110 (confirm in the fal dashboard).
- **First look (not a gate verdict):** the room output appears to change the window (blinds raised, wider city view) and the framing of the right wall, so it likely fails G4. Product outputs need the 100% zoom check on logo and label text.
- **Files:** `portfolio/config.json`, `runs.jsonl`, `contact_sheet.jpg`, `pairs_sheet.jpg` (input vs output), `review.csv` (quality-gate columns, unscored). Full-size outputs are git-ignored and mirrored to BACKUP_DIR.
