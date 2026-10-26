# Experiment 006 — Controllable Lower-Body Shaping (Proposal)

**Status:** Stage 0 approved and complete 2026-10-25 (free; no paid calls). Stage 1 not approved.

## Why a new method
Exp 004–005 showed that text prompts change hip, thigh and glute volume only a little. Front-view edits barely move, and the one successful change (B-3q-edit 5001) still lacks fuller upper thighs. We need a method where **we decide the shape and its size**, and the model only has to make it look real.

## Baselines (Version A, unchanged and still a valid option)
- Front: `experiments/005-body-ab/base/004-front-gen-v2-seed-4101.png` (SHA-256 `24dd9192…a0`)
- Three-quarter: `experiments/005-body-ab/base/004-3q-gen-v2-seed-4101.png` (`3c8eafb4…a5`)
- Face anchor where a model needs one: 2002 (`5b5191d0…8893`)
- Strongest Version B so far, for comparison only: `experiments/005-body-ab/shortlist/B/B-3q-edit-seed-5001.png` (`7bf900c2…a5`)

Nothing here becomes canonical; outputs are Version B candidates.

## The options compared

### 1. Localized / masked editing (inpainting)
Paint a mask over the hips, glutes and thighs. Only that area is redrawn; everything outside it stays pixel-for-pixel identical.
- **Tool:** FLUX.1 Fill [pro] on fal (`fal-ai/flux-pro/v1/fill`). $0.05/MP rounded up, so about **$0.25 per image** at 1696×2528. Takes `image_url`, `mask_url` (white = redraw), `prompt`, `seed` (returned).
- **Strengths:**
  - Face, upper body, waist and background are **guaranteed unchanged** outside the mask.
  - The mask can extend past her current outline, giving the model room to draw wider thighs.
- **Weaknesses:**
  - The model still decides *how much* fuller, and fill models tend to redraw something close to what was there. That is the same weakness that limited the text-only edits.
  - Risk of visible seams in fabric, shading or lighting at the mask edge.
  - In the front image her hands overlap the outer thighs, so they must be kept out of the mask.
  - A different model than Nano Banana, so a style mismatch inside the mask is possible.

### 2. Dedicated body-shape reference
Give Nano Banana a second image that **shows** the target silhouette, alongside the face reference.
- **Evidence it works:** in Exp 004, a body reference overrode the text: 3q-gen+003 copied the reference's stance. Nano Banana follows reference images far more strongly than body text.
- **Problem:** where the reference comes from. We should not use photos of real people: that would copy a real person's body and raises rights and likeness issues. A 3D mannequin would mean installing and learning new software. **The reference must be made by us.**
- **Weakness:** Nano Banana regenerates the whole image, so the face or upper body could drift slightly (it has held identity well so far).

### 3. Geometric warp ("liquify"), our own silhouette author
A small local Python script (numpy/scipy, already installed, **free**) pushes the outline of the hips, thighs and glutes outward by an exact, chosen number of pixels. It tapers to zero at the waistband and the knees, and keeps the hands fixed.
- **Strengths:**
  - **Exact, measurable size**, for example +11% hip width.
  - The face, upper body and **waist width cannot change**, because displacement is zero there.
  - Free, instant, and repeatable at several sizes so you can pick visually before any spending.
  - The image remains our own woman, so there's no likeness issue.
- **Weakness:** a raw warp can look slightly stretched. Fabric shading and seams don't update physically. Plain leggings and a plain background reduce this, but a realism pass is still needed.

## Recommendation
**Use the warp to define the shape, then a model to make it photoreal.** This combines option 3's control with option 1 or 2's realism, and turns option 2 into something feasible: the warped image *is* our body-shape reference, of the same woman. Pure masked inpainting (option 1 alone) runs as the control, to test whether the warp step is needed.

The approach **most likely** to give a clearly noticeable thigh and glute increase while keeping face, upper body, waist and realism is **warp + masked cleanup** (Method M2 below):
- the warp guarantees the size of the change
- the mask guarantees nothing else moves
- the model only fixes fabric and shading, the task fill models do best

Warp + Nano Banana (M3) is the runner-up. It probably gives the most natural fabric, but it can slightly revert the shape or shift the face.

## Test design
Both views, front and three-quarter, starting from the Version A baselines.

### Stage 0: warp previews (free, no API calls)
- For each view, two sizes:
  - **Front (A 4101: hips ~465, thighs ~442, waist ~310 px):**
    - *B-mid*: outer hip and outer upper-thigh lines about +25 px per side (about +11% hip width); inner thigh contours about 10 px inward per side.
    - *B-strong*: about +40 px per side and 15 px inward.
    - Zero change at and above the waistband; taper to zero at the knees.
  - **Three-quarter (A 4101: glute depth ~377, waist depth ~259 px):**
    - *B-mid*: seat back contour about +25 px; back of upper thigh about +15; front of thigh about +10.
    - *B-strong*: about +40 / +25 / +15.
    - Zero at the waistband; taper to the knees.
- Output: a sheet with A | B-mid | B-strong for each view, plus measurements. The numbers are starting points, tuned by eye so nothing looks unnatural.
- **Founder picks one size per view, or both, before any paid step.**

### Stage 1: realism methods (paid, at the chosen size)
| Method | What | Images | Cost |
|---|---|---|---|
| **M1: masked inpaint only** (control) | FLUX Fill on the *original* A image. Mask over hips, glutes and thighs, expanded about 10% beyond the outline; hands and everything above the waistband excluded. | 2 per view = 4 | 4 × $0.25 = $1.00 |
| **M2: warp + masked cleanup** (recommended) | FLUX Fill on the *warped* image. Narrow mask band (about ±25 px) along the new outline and inner-thigh area, so only fabric and shading are repaired. | 1 per view = 2 | 2 × $0.25 = $0.50 |
| **M3: warp as body-shape reference** | Nano Banana Pro Edit. References: warped image (body, pose, outfit) + 2002 (face). | 1 per view = 2 | 2 × $0.15 = $0.30 |
| **Total** | | **8** | **$1.80** |

- **Recommended cap: $2.50.**
- Month-to-date ≈ $3.93 → ≈ $5.73 of $110.
- If you want to save money: drop to one M1 image per view (6 images, $1.30).

### Prompts
**M1 front (FLUX Fill)**
> Full-length photograph of a slim, fit young woman in fitted taupe-grey high-waisted leggings, standing front-facing in a neutral studio. In the filled area her lower body is clearly fuller and more developed: broader hips with a strong outward curve below the waist, and visibly fuller upper thighs through both the inner and outer thigh contours, with natural quadriceps fullness and athletic definition, tapering gradually toward the knees. The leggings stretch realistically over the fuller shape with natural folds and the same fabric colour, texture and lighting as the rest of the photo. Photorealistic and seamless.

**M1 three-quarter (FLUX Fill)**: as above, "standing in a three-quarter view", plus:
> …and larger, rounder, more projected glutes whose curve is clearly visible in profile.

**M2 (FLUX Fill cleanup, both views)**
> Photorealistic fitted taupe-grey leggings on a fit woman's hips, glutes and thighs. Keep this exact body shape and outline. Natural fabric tension, folds, seams and shading, seamless with the surrounding photo and the same lighting.

**M3 (Nano Banana Pro Edit, both views)**
> The first image shows this woman's exact pose, outfit, framing and body silhouette; the second image is her face reference. Recreate the first image as a clean, natural photograph. Keep the pose, outfit, background, lighting and camera framing, and above all keep her exact body silhouette and proportions from the first image, including the fuller hips, upper thighs and glutes, unchanged. Keep her face exactly as in the second image, with the beauty mark on her left cheekbone. Fix any unnatural stretching so the leggings' fabric, seams, folds and shading look physically real. Do not slim her lower body back down, do not narrow her waist and do not change her upper body. Do not add any scar.

## Evaluation
**Review materials:**
- **`ab_pairs.jpg`**: Version A baseline on the left, each method's B on the right, same scale and same pose.
- **Difference overlay**: highlights where pixels changed, to prove the face and upper body are untouched.
- Face crops.
- Measurements: hips, upper thighs, waist and glute depth versus A.

**Mandatory:**
- Identity ≥ 4/5 (it should be unchanged in M1/M2 by construction)
- Photorealism ≥ 4/5, with particular attention to seams, fabric, shading, the thigh gap and the hands
- **Waist width within about ±3% of A**
- Bust and upper body unchanged
- Not distorted or cartoonish

**Target:**
- **Clearly noticeable thigh and glute increase versus A**, by eye side by side and in measurement:
  - hip and thigh width or glute depth at least about +8% (mid) or +12% (strong)
- Scored 1–5 for thigh fullness (inner and outer), hip curve, glute projection and appeal

**Decision this answers:**
- which realism method (M1, M2 or M3) to use for Version B from now on
- whether masked editing alone is enough

**No winner between Version A and Version B is implied.**

## Considered and not proposed now
- **Local open-source pipeline with pose and depth control** (SDXL/FLUX ControlNet on the RTX 5060): the most control in the long run, but a much larger setup effort. Revisit if Version B is chosen and needs to work at scale (many outfits and poses).
- **Photos of real people as body references:** excluded on rights and likeness grounds.

## Approval needed
1. Stage 0 warp previews (free), then your choice of size per view
2. Stage 1 methods (M1 ×4, M2 ×2, M3 ×2 = $1.80) with a $2.50 cap, or the reduced 6-image option
3. The prompts (or ChatGPT's revisions)
