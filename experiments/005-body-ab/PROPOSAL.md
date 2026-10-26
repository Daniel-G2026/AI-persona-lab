# Experiment 005 — Body Direction A/B Comparison (Proposal)

**Status:** Proposed by Claude 2026-10-25. **Awaiting founder approval. Nothing generated.**

## Purpose
A **comparative branch**, not a replacement. Same woman, two body directions, compared side by side:

- **Version A:** the current direction. Slim feminine upper body, longer torso, narrow waist, flat toned stomach, medium natural bust, lean-curvy lower body with the current moderate hip/glute shape. Best example so far: Exp 004 `front-gen-v2` 4101.
- **Version B:** a fuller lower-body alternative ("gym girl thicker"). Identical face and upper body, with broader, more pronounced hips, noticeably fuller upper thighs, and larger, rounder, more projected glutes. The added shape comes from the lateral hips, upper thighs and glutes, never from a smaller waist or larger bust.

Version B does not replace Version A. Neither becomes canonical until the founder chooses. `PROJECT_SPEC.md` is not changed by this experiment.

## Anchors
| Role | Image | SHA-256 |
|---|---|---|
| Original face baseline | Exp 001 seed 1001 (`experiments/001-portrait/shortlist/seed-1001.png`) | `12bb637b…8b88` |
| Face identity anchor (used in every request) | Exp 002 Nano Banana Pro 2002 (`experiments/002-portrait-refine/shortlist/nanobananapro-seed-2002.png`) | `5b5191d0…8893` |
| Version A front reference / edit base | Exp 004 front-gen-v2 4101 → `experiments/005-body-ab/base/004-front-gen-v2-seed-4101.png` | `24dd9192…a0` |
| Version A three-quarter reference / edit base | Exp 004 3q-gen-v2 4101 → `experiments/005-body-ab/base/004-3q-gen-v2-seed-4101.png` | `3c8eafb4…a5` |

## 1. Design and why
**Model:** Nano Banana Pro Edit (`fal-ai/nano-banana-pro/edit`), 2K, 2:3, PNG, fal default safety settings. It is the only model that has held her face across Experiments 002–004, and changing models now would mix up model effects with body effects.

**Two tracks, both using front and true three-quarter views:**

### Track 1: Paired edits (the core comparison)
- **Version A** = the two existing Exp 004 images (front-gen-v2 and 3q-gen-v2, seed 4101). No new cost.
- **Version B** = edits of exactly those images: same face, pose, lighting, outfit and framing, with only the lower body made fuller. References: the A image first, then 2002 for the face.
- **Why:** this is the most controlled A/B test possible. Each pair differs only in the lower body, so the comparison is pure body direction, and the "two different women" risk is lowest.
- **Risk:** in Exp 004 a cautious edit barely changed anything. The Version B edit prompts are written to demand a clearly visible change. If the edit still under-delivers, Track 2 still produces a Version B.

### Track 2: Matched fresh generations (a fairness check)
- A and B prompts are **word-for-word identical except the body paragraphs**: same face, outfit, pose and framing text, same seeds, **2002 as the only reference**.
- **Why:**
  - Track 1's Version A is a hand-picked best image, which biases the comparison in A's favour. Generating A and B the same way removes that bias.
  - It also shows whether each version can be **reproduced** from text, which future content will need.
- **Why not add 4101 as a body reference:** in Exp 004, a body reference pulled the pose and shape toward itself (3q-gen+003). Here that would drag Version B back toward A.

### Arms and counts
| Arm | Version | View | Method | References | Images |
|---|---|---|---|---|---|
| `B-front-edit` | B | front | edit A front | A-front base, 2002 | 3 |
| `B-3q-edit` | B | three-quarter | edit A three-quarter | A-3q base, 2002 | 3 |
| `A-front-gen` | A | front | generate | 2002 | 2 |
| `B-front-gen` | B | front | generate | 2002 | 2 |
| `A-3q-gen` | A | three-quarter | generate | 2002 | 2 |
| `B-3q-gen` | B | three-quarter | generate | 2002 | 2 |
| **Total** | | | | | **14** |

Seeds: 5001–5003 for edits, 5001–5002 for generations. Identical seeds across matched A/B arms.

### Staged run
1. **Stage 1:** seed 5001 for all 6 arms (6 images, $0.90), then stop for founder + ChatGPT review.
2. **Stage 2:** the remaining 8 images ($1.20), only after approval, possibly with adjusted prompts.

## 2. Prompts
Prompt files in `experiments/005-body-ab/`:
- `prompt_A_front_gen.txt`, `prompt_B_front_gen.txt`
- `prompt_A_3q_gen.txt`, `prompt_B_3q_gen.txt`
- `prompt_B_front_edit.txt`, `prompt_B_3q_edit.txt`

### How the four generation prompts are built
Each is **[FACE] + [BODY A or BODY B] + [WARDROBE + POSE] + [FRAMING]**. Every block except the body is identical across A and B and unchanged from Exp 004 v2.

**[FACE]**
> Using the reference photo as the only identity source, create a new full-length photograph of the same woman. Keep her face exactly the same person: the same face shape, eyes, eye colour, brows, nose, lips, jawline, skin tone, the small beauty mark on her left cheekbone exactly as in the reference, and her deep brown below-shoulder soft 2B waves. Her face must stay clearly visible and recognizable as the woman in the reference. Do not add any scar. She is clearly an adult, around 23-24.

**[BODY A]** (verbatim from Exp 004 v2, which produced front-gen-v2 4101)
> Body: about 5 ft 7 in (170 cm). Her upper body stays exactly as in her approved look: slim and balanced shoulders, a proportionally longer torso, a flat, lightly toned stomach, a natural medium bust and a naturally narrow waist. Do not narrow the waist any further and do not enlarge the bust.
>
> The defining feature of her figure is the visible contrast between her slender upper body and her naturally fuller hips and glutes: above the waist she is narrow and light-framed, and below it her silhouette widens into distinctly curvy hips and a full, rounded seat. Her shoulders, waist, bust and torso proportions stay exactly as described above; the contrast comes from the lower body, not from making the upper body smaller. Specifically:
> - From the front, her hips curve clearly outward below the waist, so the hip line is visibly wider than the waist and the outline reads as a distinct curve, not a straight line.
> - The extra volume sits in her lateral hips and upper glutes, the sides of the hips and the upper seat, not in thicker thighs.
> - Her glutes are noticeably rounded and lifted, with natural backward projection that is obvious in profile.
> - The outline flows smoothly and anatomically from her narrow waist out to full hips and then into toned, athletic upper thighs and long, toned legs.
>
> She remains slim and athletic overall, like a woman who trains her lower body and does Pilates. The curves come from natural muscle and soft tissue, never a surgically enhanced, BBL-like, cartoonish or generally heavier look.

**[BODY B]** (from the founder's Version B brief)
> Body: about 5 ft 7 in (170 cm). Her upper body stays exactly as in her approved look: slim, feminine and balanced shoulders, a proportionally longer torso, a flat, toned stomach, a natural medium bust and a naturally narrow waist. Do not narrow the waist any further and do not enlarge the bust.
>
> Her lower body is clearly fuller and more developed than a slim athletic figure, so the contrast between her slim upper body and her fuller lower body is immediately visible. Specifically:
> - Her hips are broader and more pronounced, with a strong, visible outward curve from the waist into the lateral hips.
> - Her thighs are noticeably fuller and shapelier, especially the upper thighs, while staying toned and feminine.
> - Her glutes are larger, rounder and more projected, with an obvious curve and strong backward and side projection from the side and three-quarter angle.
> - The outline runs in one strong, smooth line from her narrow waist out to broad hips and down into full upper thighs and toned lower legs.
>
> She reads as a fit, strong "gym girl" with a thicker, developed lower body: attractive, believable and proportionate. The added shape comes from fuller lateral hips, fuller upper thighs and larger glutes, never from a smaller waist or a larger bust. Real muscle and soft tissue, not surgically enhanced, not cartoonish, not distorted.

**[WARDROBE]** (both views)
> She wears a short, fitted sports top (not a t-shirt, not long-sleeved) and full-length high-waisted leggings in the same muted taupe-grey neutral tone, with plain low-profile neutral sneakers. The leggings fit closely enough to show her real shape, with realistic fabric tension and folds.

**[POSE — front]**
> She stands front-facing in a relaxed, natural pose with her weight shifted slightly onto one leg, her arms hanging loosely a little away from her sides so they do not cover her waist or hips, and a calm, quietly alluring expression.

**[POSE — three-quarter]**
> She stands in a true three-quarter view: her whole body is rotated about 45 degrees from the camera so that the front of her torso and her left side are both visible, with her left hip nearest the camera. Her back is NOT toward the camera, and she is not looking over her shoulder; her chest and stomach are still partly visible. Her head turns only slightly toward the camera so her face is seen in a natural three-quarter angle. Her weight rests on her back leg in a realistic, relaxed posture, and her arms hang naturally slightly forward of her body so they do not cover her hips or seat. The outward curve of her hip and the rounded backward projection of her glutes are clearly visible in her silhouette.

**[FRAMING]**
> The entire body is visible from the top of her head to her shoes, with no cropping. Neutral, uncluttered studio background; soft, even, natural daylight; camera at about waist height from a moderate distance, with natural portrait-lens perspective and no wide-angle distortion. Photorealistic anatomy, hands, feet and skin texture. One person only, no text.

### Version B edit prompts (Track 1)
**`prompt_B_front_edit.txt`**
> Edit the first image, a full-length photograph of this woman; the second image is her face reference. Keep everything else exactly the same: her face and identity (match the second image), hair, the beauty mark on her left cheekbone, shoulders, arms, hands, bust size, waist width, stomach, torso length, pose, outfit, shoes, lighting, background and camera framing. Do not add any scar.
>
> Change only her lower body into a clearly fuller, more developed version: broader, more pronounced hips with a strong outward curve from the waist into the lateral hips; noticeably fuller, shapelier upper thighs that stay toned; and larger, rounder glutes. The outline should run in one strong, smooth line from her narrow waist out to broad hips and full upper thighs.
>
> The difference from the original image must be clearly visible, but she must stay attractive, believable and proportionate: a fit, strong "gym girl" with a thicker, developed lower body. The added shape comes from fuller lateral hips, fuller upper thighs and larger glutes, never from a smaller waist or a larger bust. Real muscle and soft tissue with realistic fabric tension and folds on the leggings; not surgically enhanced, not cartoonish, not distorted.

**`prompt_B_3q_edit.txt`**: the same, but the first sentence describes "a full-length three-quarter-view photograph", and the change paragraph reads:
> Change only her lower body into a clearly fuller, more developed version: broader, more pronounced hips with stronger side projection; noticeably fuller, shapelier upper thighs that stay toned; and larger, rounder, more projected glutes whose curve is clearly visible in profile. The outline should run in one strong, smooth line from her narrow waist out to broad hips, a rounded seat and full upper thighs.

## 3. Evaluation framework
**Review materials** (all committed):
- **`ab_pairs.jpg`**: one row per matched pair, **A on the left, B on the right**, at identical scale, labelled with version, view, method and seed. Rows:
  - Track 1 front (A base vs each B edit)
  - Track 1 three-quarter
  - Track 2 front (A vs B, same seed)
  - Track 2 three-quarter
- **`face_crops.jpg`**: every output's face next to 2002 and 1001.
- **Approximate measurements** on front images (manual, ±10 px; supporting evidence only): shoulder, waist, hip and upper-thigh widths, plus hip ÷ waist and thigh ÷ waist ratios.

### A. Per image (`review.csv`)
| Criterion | Scale | Mandatory? |
|---|---|---|
| Identity vs 2002 (face crop) | 1–5 or inconclusive | **≥ 4** |
| Same woman as its paired image | yes / no | **yes** |
| Photorealism (anatomy, hands, feet, fabric) | 1–5 | **≥ 4** |
| Upper body preserved (waist not narrower, bust not larger, torso, shoulders) | yes / no | **yes** |
| Not distorted / cartoonish / surgical-looking | yes / no | **yes** |
| Matches its intended version (A = moderate lean-curvy; B = clearly fuller hips, thighs, glutes) | 1–5 | target ≥ 3.5 |
| Hip width / curve | 1–5 | |
| Upper-thigh fullness | 1–5 | |
| Glute size and projection (three-quarter) | 1–5 | |
| Body appeal | 1–5 | |
| Outfit and pose on brief | yes / no | |

### B. Per pair (`review_pairs.csv`)
- **Same woman in A and B?** (yes / no). If no, the pair is invalid for preference.
- **Is the A/B difference clearly visible?** (yes / no)
- **More attractive:** A / B / tie
- **More believable:** A / B / tie
- Notes

### C. Overall verdict (founder; ChatGPT separately)
- Which version is more attractive overall?
- Which is more believable?
- **Which direction do you prefer:** A, B, or undecided?
- Is Version B reliably reproducible (Track 2), or did it only work as an edit (Track 1)?

**A valid outcome needs**, for each version, at least one front and one three-quarter image passing every mandatory criterion. Otherwise the comparison is inconclusive, and that version gets fixed before preferences count.

## 4. Cost
- Stage 1: 6 × $0.15 = **$0.90**. Stage 2: 8 × $0.15 = **$1.20**. Total **$2.10**.
- **Recommended cap: $3.00** (headroom for one failed or re-run image).
- Month-to-date before this experiment: about $3.03. After: about $5.13 of $110.

## 5. Storage and documentation
- **Folder:** `experiments/005-body-ab/`, same structure as before.
- **Arm names carry the version:** `A-…` or `B-…`. Each arm in `config.json` also records `"version"`, `"view"`, `"method"` and its references. File names start with the arm name (e.g. `B-front-edit-seed-5001.png`), so version membership is visible everywhere: files, `runs.jsonl`, `review.csv`.
- **References:** the 2002 face anchor (and 1001 for the face-crop sheet) plus the two Version A bases in `base/`. All are hash-checked before and after each run. Each `runs.jsonl` row lists the exact references sent, in order.
- **Side-by-side sheet:** a small new script (`scripts/ab_sheet.py`) reads the pair definitions from `config.json` and builds `ab_pairs.jpg`.
- **Log:** `EXPERIMENT_LOG.md` gets the approval, each stage's results, and the A/B verdict. Originals are local and mirrored to OneDrive.
- **Shortlist:** `shortlist/A/` and `shortlist/B/` keep the versions physically separate. Version A stays a live option whatever happens.

## Approval needed
1. The design: Track 1 paired edits + Track 2 matched generations, 14 images, staged 6 + 8
2. $3.00 cap
3. The prompts (or ChatGPT's revisions)
