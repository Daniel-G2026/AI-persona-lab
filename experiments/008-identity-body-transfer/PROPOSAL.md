# Experiment 008 — Identity and Body-Shape Transfer (Proposal)

**Status:** Proposed by Claude 2026-10-25. **Awaiting founder approval. Nothing generated, nothing spent.**

## Question
Can Nano Banana Pro produce the **same fictional adult woman** (portrait 2002's face, plus Version B's fuller hips, thighs and glutes) in **new outfits, poses and real environments**? Or does it keep her face but **slide back to its default slimmer body**?

The test scores **face** and **body** separately, so a good face can't hide a lost body, or vice versa.

## References (all unchanged; hash-checked before and after the run)
| Order | Role | File | SHA-256 |
|---|---|---|---|
| Image 1 | **Face identity** | `experiments/002-portrait-refine/shortlist/nanobananapro-seed-2002.png` | `5b5191d0…` |
| Image 2 | **Body shape, front** (Version B) | `experiments/007-reconstruction/shortlist/B/front-R2-s035.png` | `5eae9d12…` |
| Image 3 | **Body shape, three-quarter** (Version B) | `experiments/007-reconstruction/shortlist/B/three-quarter-R2-s035.png` | `f8d1cddf…` |

- Version A (`experiments/005-body-ab/base/…4101.png`) is **not sent**. It's used only as the slim comparison point in evaluation.
- The prompt states each image's role explicitly. In Exp 004, a body reference also dragged in its pose and studio, so the prompt tells the model to take **shape only** from images 2–3, not their pose, outfit, lighting or background.

## Design: 2 images
| # | Setting | Pose and view | Outfit (fitted enough to judge shape) | Body evidence it gives |
|---|---|---|---|---|
| **8-1** | Sunlit city sidewalk, late afternoon | Standing, **facing the camera**, weight on one leg | Fitted high-waisted mid-blue straight-leg jeans, fitted white ribbed tank top, white sneakers | Hip width and upper-thigh fullness from the front |
| **8-2** | Bright modern apartment kitchen, window light | **True three-quarter view**, left side toward the camera, one hand on the counter | Fitted ankle-length ribbed knit dress in warm oatmeal, flat sandals | Hip curve and glute projection in profile |

- Settings: Nano Banana Pro Edit (`fal-ai/nano-banana-pro/edit`), aspect ratio 2:3, resolution 2K, PNG, seeds 8001 and 8002, fal default safety settings.
- The outfits and settings are deliberately different from the studio references, which tests real transfer rather than copying.

## Prompts
**Shared reference paragraph** (opens both prompts):
> Use the three reference images as follows. Image 1 is the identity reference for her face: keep her exactly the same person, with the same face shape, eyes, eye colour, brows, nose, lips, skin tone, the small beauty mark on her left cheekbone, and her deep brown below-shoulder soft 2B waves. Images 2 and 3 show her body from the front and from a three-quarter view: reproduce exactly this body shape and these proportions, with a slim upper body, a proportionally longer torso, a narrow waist, a flat toned stomach and a medium natural bust, and a clearly fuller lower body with broad hips, full inner and outer upper thighs and rounded, projected glutes. Take only her body shape from images 2 and 3. Do not copy their pose, outfit, lighting or studio background, and do not slim her lower body toward a typical slim model figure. She is clearly an adult, around 23–24. Do not add any scar.

**8-1, front, city** (after the shared paragraph):
> Create a new photorealistic full-length photograph. She stands on a sunlit city sidewalk in warm late-afternoon light, facing the camera with her weight on one leg, one hand loosely holding the strap of a small shoulder bag and the other arm relaxed, so neither arm covers her hips. She wears fitted high-waisted mid-blue straight-leg jeans, a fitted white ribbed tank top and simple white sneakers. Relaxed, natural expression. Her entire body is visible from head to shoes; camera at about waist height from a moderate distance, natural perspective, no wide-angle distortion. Realistic skin, denim and fabric texture, natural shadows, an everyday social-media photo feel. One person in focus, no text.

**8-2, three-quarter, kitchen** (after the shared paragraph):
> Create a new photorealistic full-length photograph. She stands in a bright, modern apartment kitchen with soft window light, in a natural three-quarter view: her body is turned about 45 degrees so her left side is toward the camera and the front of her torso is partly visible, her head turned toward the camera with a relaxed smile. One hand rests on the edge of the counter and the other hangs relaxed, neither covering her hips. She wears a fitted, ankle-length ribbed knit dress in warm oatmeal and simple flat sandals; the dress follows her shape so the curve of her hips and the rounded projection of her glutes are visible in profile. Her entire body is visible from head to feet; natural perspective, no wide-angle distortion. Realistic skin, knit texture and soft natural light, an everyday lifestyle photo feel. One person, no text.

## Evaluation: face and body scored separately
### A. Facial identity (face crop vs 2002 and 1001)
- Identity ≥ **4/5**, or "inconclusive" if the face is too small to judge
- Beauty mark on her **left** cheekbone where visible; no scar
- **Styling drift** flagged separately: skin tone, brow weight, makeup, or a more "polished" look than 2002 (the R3 problem in Exp 007)

### B. Body shape: did it keep Version B, or slide back toward Version A or slimmer?
New photos have different clothing, distance and framing, so raw pixels can't be compared. Claude measures **scale-free ratios** on each output, and on the A and B references with the **same manual gridded method**:
- **8-1 (front):** hip width ÷ shoulder width, and upper thigh (single leg) ÷ shoulder width. Shoulders are the same in A and B, so they serve as the ruler.
- **8-2 (three-quarter):** glute-level depth ÷ waist depth.

**B-retention index** = (output ratio − A ratio) ÷ (B ratio − A ratio):
- **1.0** = Version B fullness kept
- **0** = back to Version A
- **< 0** = slimmer than Version A (full regression to a default figure)

Also judged by eye: an equal-height side-by-side of each output next to the Version A and Version B references.

Measurement caveat: pose, stance and camera angle change apparent widths. Each reading is marked "reliable" or "pose-limited", and differences explained by pose are not counted as body changes (as in Exp 005).

### C. Transfer quality
- New outfit, pose and environment actually used, with **no copying** of the studio, pose or taupe set from the references
- Photorealism ≥ 4/5 (anatomy, hands, fabric, lighting, a believable real-world photo)
- Waist not narrowed and bust not enlarged vs the references

### Outcome categories (per image)
| Face | Body index | Verdict |
|---|---|---|
| ≥ 4 | ≥ 0.7 | **Transfer works**: same woman, Version B body |
| ≥ 4 | 0.3–0.7 | Face transfers; **body partly regresses** |
| ≥ 4 | < 0.3 | Face transfers; **body regresses to the default slimmer figure** |
| < 4 | any | **Identity fails**; body result noted but not counted |

The two results tell us whether Nano Banana Pro can carry Version B into real content as-is, or whether body shape needs a stronger mechanism, such as more body references, pose control, or the Exp 006–007 warp-and-reconstruct pipeline applied after generation.

## Cost
- 2 × $0.15 = **$0.30**. **Recommended cap: $0.50.** The price will be re-checked on fal before running.
- Month-to-date ≈ $4.47 → ≈ $4.77 of $110.

## Storage
- `experiments/008-identity-body-transfer/`: `config.json` (arms 8-1 and 8-2, references in order), prompt files, `runs.jsonl`, contact sheet, face crops, **body comparison sheet** (output | Version A | Version B, equal height), `measurements.json` (ratios and retention index), `review.csv`.
- Originals are local and mirrored to OneDrive. Reference hashes are verified before and after the run.

## Approval needed
1. The 2-image design and reference configuration
2. The prompts (or ChatGPT's revisions)
3. $0.50 cap
