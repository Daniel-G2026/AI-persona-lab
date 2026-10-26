# Experiment 007 — Realism Reconstruction of the B-strong Targets (Proposal)

**Status:** Proposed by Claude 2026-10-25. **Awaiting founder approval. Nothing generated, nothing spent.**

## Goal
Turn the B-strong shape targets into clean, photorealistic full-body photos **without losing the B-strong fullness**, and without changing the face, upper body, waist, bust or outfit.

- Shape targets (Exp 006, selected by the founder):
  - `experiments/006-body-control/warp/front-B-strong.png` (SHA-256 `fb7f48ab…`)
  - `experiments/006-body-control/warp/three-quarter-B-strong.png` (`d1feac3c…`)
- Face anchor: 2002 (`5b5191d0…`). Version A stays untouched and valid. **Nothing here becomes canonical.**

## What has to be fixed
| Problem | Where it comes from | How this plan fixes it |
|---|---|---|
| Bowed forearms and shifted hands | The warp shifts the arms more at the wrist than the elbow, along a curve | **Free re-warp:** move each forearm in a straight line instead (behaves like a slight rotation at the elbow, so the forearm stays straight) |
| Abrupt thigh-to-knee transition | The B-strong taper ends quickly just above the knee | **Free re-warp:** a longer, gentler taper into the knee, with hip and thigh fullness unchanged |
| Stretched legging texture and shading | A warp moves pixels; it can't re-render fabric | **Paid re-render** of the legging area |
| Contour, edge and background artifacts | Slight background compression; draft masks | Re-warp plus the paid re-render; masks rebuilt properly |

Fixing arms and the knee **for free first** means the paid models never have to redraw hands (the hardest thing to regenerate) or change the silhouette.

## 1. Method
### Step 1 (free, local): B-strong-v2 shape target
- The same B-strong fullness at the hips, thighs and glutes, with:
  - **straight forearms** (shift grows evenly from elbow to wrist, then stays constant across the hand)
  - a **gentler knee taper**: front outer keyframes `[1040,0] [1250,40] [1480,42] [1620,32] [1760,14] [1880,0]`, with inner and three-quarter profiles softened the same way
- **Hard check:** hip, thigh and glute measurements stay within ±2% of B-strong. Zero pixels change above the waistband.
- Output: `warp/*-B-strong-v2.png` plus an A | B-strong | B-strong-v2 sheet.

### Step 2 (paid): three reconstruction methods, compared
| ID | Method | Silhouette preserved? | Face and upper body preserved? |
|---|---|---|---|
| **R1** | **Interior re-render.** FLUX.1 Fill [pro] with an **interior mask**: the legging area eroded about 12 px inside the outline. The model redraws fabric inside a locked silhouette. Run on a lower-body crop, composited back. | **Yes, by construction.** The outline band is never redrawn. | **Yes, pixel-identical** (outside the mask) |
| **R2** | **Low-strength re-render.** Z-Image Turbo image-to-image on the lower-body crop at low strength (0.30 and 0.45), composited back through the broad mask. It keeps the input's structure and refreshes texture and shading. | Mostly (lower strength = more faithful); measured | **Yes, pixel-identical** (composited) |
| **R3** | **Global reconstruction.** Nano Banana Pro Edit with references [B-strong-v2 target, 2002 face]: re-render the whole photo, keeping the silhouette. | At risk: the model may slim her back toward its default; measured | Very likely (Nano Banana has held her face throughout); checked on face crops |

**Recommendation:** R1 is the most likely to satisfy every constraint at once:
- the silhouette is locked by the mask edge
- the face and upper body can't change
- the model only does what it's good at: drawing fabric

R2 is a very cheap check of whether a light refresh is enough. R3 is the most natural-looking option, if it holds the shape.

## 2. Broad mask, narrow mask, or both?
- **Narrow mask alone: no.** It only reaches the outline, and can't fix the stretched shading across the thighs.
- **Broad mask over the whole legging area, used directly with FLUX Fill: no.** Fill redraws masked areas from scratch, so it would decide the silhouette itself and could shrink her back toward Version A.
- **Use instead:**
  - an **interior mask** for R1: the broad area *shrunk* about 12 px inside the outline, so all fabric is re-rendered but the silhouette edge stays exactly B-strong-v2
  - the **broad mask** only as the *blend region* when compositing R2 back
  - edges are handled by the free re-warp, so no separate narrow-mask pass is needed
- Masks are rebuilt from the filled legging area, which fixes the draft's waistband-seam false positive. Hands are excluded with an 8 px margin. Mask files are committed and shown on a preview sheet.

## 3. Number of images
| Method | Per view | Total |
|---|---|---|
| R1 interior re-render (FLUX Fill) | 2 seeds | 4 |
| R2 low-strength re-render (Z-Image i2i), strengths 0.30 and 0.45 | 2 | 4 |
| R3 global reconstruction (Nano Banana Pro) | 2 | 4 |
| **Total** | | **12** |

## 4. Prompts
**R1: FLUX.1 Fill [pro], interior mask** (front; three-quarter adds the bracketed part)
> Photorealistic close-fitting high-waisted leggings in a muted taupe-grey, worn by a fit young woman with a full, curvy lower body: broad hips and full inner and outer upper thighs [, and rounded, lifted, projected glutes]. Natural fabric tension, smooth stretch, soft folds, seams and soft studio shading that follow the curves of her hips and thighs and match the rest of the photo exactly. Even, soft daylight. Photorealistic.

**R2: Z-Image Turbo image-to-image, lower-body crop** (front; three-quarter adds the bracketed part)
> Photorealistic photograph of a fit young woman's hips and legs in close-fitting taupe-grey high-waisted leggings and plain neutral sneakers, standing [in a three-quarter view] in a neutral studio with soft, even daylight. Full, curvy lower body with broad hips, full upper thighs that taper smoothly into the knees [, and rounded, projected glutes]. Natural fabric tension, folds and shading, realistic hands and forearms, clean edges against the plain light background.

**R3: Nano Banana Pro Edit, references [B-strong-v2 target, 2002]** (both views)
> The first image is the target photograph of this woman. Keep its exact pose, framing, background, lighting and outfit, and above all keep her exact body silhouette and proportions: the full hips, full inner and outer upper thighs and rounded, projected glutes, the narrow waist, the slim upper body and the medium natural bust. Do not slim or enlarge anything. The second image is her face reference: keep her face exactly the same person, with the small beauty mark on her left cheekbone. Re-render the photo as a single clean, natural photograph: realistic legging fabric with natural tension, folds, seams and shading across the hips and thighs; straight, natural forearms and relaxed hands; a smooth, anatomical transition from the full thighs into the knees; clean edges against the plain background. Do not add any scar. One person only, no text.

## 5. Cost
- R1: FLUX Fill on a lower-body crop of about 1696×1104 (1.9 MP, billed as 2 MP × $0.05) ≈ **$0.10** each × 4 = **$0.40**
- R2: Z-Image Turbo i2i on the same crop (2 MP × $0.005) ≈ **$0.01** each × 4 = **$0.04**
- R3: Nano Banana Pro $0.15 × 4 = **$0.60**
- Step 1: free
- **Total ≈ $1.04. Recommended cap: $1.50.**
- Month-to-date ≈ $3.93 → ≈ $4.97 of $110.
- Prices will be re-checked on fal before running, as before.

## 6. Success criteria
**Review materials:**
- **`recon_pairs.jpg`**: B-strong-v2 target | each reconstruction | Version A, same scale
- face crops
- a changed-pixel overlay (R1/R2 must show zero change outside their masks)
- automatic legging-outline measurements against the target

**Mandatory for each image:**
- **Identity ≥ 4/5** (R1/R2 are pixel-identical above the waistband by construction; R3 is judged on face crops)
- **Photorealism ≥ 4/5:**
  - leggings read as real fabric, with no stretched shading bands
  - forearms straight and natural; hands intact
  - smooth thigh-to-knee transition
  - no contour halos, seams at the mask edge, or background distortion
- **Fullness retained:**
  - front hips ≥ **+14%** vs Version A (B-strong is +15.7%)
  - single-leg upper and mid thigh ≥ **+20%** (B-strong is +24%)
  - three-quarter glute depth ≥ **+10%** (B-strong is +11.1%)
- **Waist within ±2%** of Version A. Bust and upper body unchanged.
- Not distorted or cartoonish. Outfit unchanged (same taupe-grey set and sneakers).

**Experiment passes** if at least one front and one three-quarter image meet everything. Those become **"Version B reconstructed candidates"**: shortlisted, not canonical. The results also tell us which reconstruction method to use for future Version B images.

## Approval needed
1. Step 1 free re-warp (B-strong-v2)
2. Step 2: R1 ×4, R2 ×4, R3 ×4 (≈ $1.04) with a $1.50 cap
3. The prompts (or ChatGPT's revisions)
