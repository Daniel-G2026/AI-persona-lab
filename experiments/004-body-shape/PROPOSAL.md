# Experiment 004 — Lower-Body Shape Refinement (Proposal)

**Status:** Proposed by Claude 2026-10-25. **Awaiting founder approval. Nothing generated.**

## Objective
Keep everything that worked in Experiment 003 (2002 face, slim balanced upper body, longer torso, flat stomach, medium bust, long legs, realism) and refine **only the lower body**:
- slightly more pronounced outer hip flare
- a smoother, more feminine waist-to-hip transition
- slightly fuller upper thighs
- a more rounded, lifted glute shape

The result should stay slim and lean-curvy. It must not be generally thicker, narrower-waisted, larger-busted, BBL-like, surgically enhanced or cartoonish.

## 1. Model / tool
**Nano Banana Pro Edit** (`fal-ai/nano-banana-pro/edit`), 2K, 2:3, PNG, fal default safety settings.
- It kept the face in Experiments 002 and 003 and produced clean anatomy.
- It can do two different jobs, which this experiment compares:
  - **edit an existing Exp 003 image** (change only the lower body, keep everything else fixed)
  - **generate a new image** from references

## 2. References: Exp 003 outputs, or the portrait only?
It depends on the view, so test both:
- **Front view:** an Exp 003 image is the most controlled starting point. Editing it keeps her face, upper body, outfit, pose and lighting fixed, so any change is the lower body alone.
- **Three-quarter view:** no Exp 003 image shows this angle, so it must be generated. An Exp 003 image as a second reference could anchor her upper body, outfit and scale. But it could also anchor the straight lower body we're trying to fix. Unknown, so one arm uses it and one doesn't.

**Proposed Exp 003 base image:** `ref2002-seed-3001`. Neutral sports top and leggings, front-facing, clean hands and feet, beauty mark visible. **Founder/ChatGPT to confirm or pick another.** No Exp 003 image has been formally approved.

The 1001 baseline is not used: Exp 003 showed no benefit from it at full-body resolution.

| Arm | View | Method | References (in order) | Prompt file |
|---|---|---|---|---|
| **front-edit** | front | edit the Exp 003 base | 003 base, 2002 | `prompt_front_edit.txt` |
| **front-gen** | front | new generation | 2002 | `prompt_front_gen.txt` |
| **3q-gen** | three-quarter | new generation | 2002 | `prompt_3q_gen.txt` |
| **3q-gen+003** | three-quarter | new generation | 2002, 003 base | `prompt_3q_gen_003.txt` |

## 3. Prompts
**Shared wardrobe line**, tightened after the outfit drift in Exp 003:
> a short, fitted sports top (not a t-shirt, not long-sleeved) and full-length high-waisted leggings in the same muted taupe-grey neutral tone, with plain low-profile neutral sneakers

**Shared refined body description** (replaces the Exp 003 body paragraph):
> Body: about 5 ft 7 in (170 cm) with natural proportions; a slim, balanced upper body with a proportionally longer torso, a flat, lightly toned stomach and a natural medium bust. Her lower body is softly curvy while staying slim: a gently but clearly outward-curving hip line visible from the front, a smooth feminine waist-to-hip transition created by her hips (not by an extra-narrow waist), slightly fuller upper thighs, and rounded, lifted glutes with visible natural projection in profile. Long, toned, feminine legs. She looks like a woman who does Pilates and lower-body strength training: lean and athletic, never thick, surgically enhanced, BBL-like or exaggerated.
>
> Realistic anatomy, natural proportions and her identity from the reference take priority over this description. Do not narrow her waist, enlarge her bust, or make her generally heavier.

### front-edit (`prompt_front_edit.txt`)
> Edit the first image, a full-length photograph of this woman; the second image is her face reference. Keep everything exactly the same: her face and identity, hair, beauty mark on her left cheekbone, shoulders, arms, hands, bust size, waist width, stomach, torso length, leg length, pose, outfit, shoes, lighting, background and camera framing.
>
> Change only the shape of her lower body, subtly and realistically: a slightly more pronounced outward hip curve visible from the front, a smoother and more feminine waist-to-hip transition created by the hips rather than by narrowing the waist, and slightly fuller upper thighs. Keep her slim and athletic, like a woman who does Pilates and lower-body strength training. Keep natural fabric tension and folds on the leggings.
>
> Do not make her generally thicker, do not narrow her waist, do not enlarge her bust, and do not create a surgically enhanced, BBL-like or cartoonish shape. Do not add any scar.

### front-gen (`prompt_front_gen.txt`)
> Using the reference photo as the identity source, create a new full-length photograph of the same woman. Keep her face exactly the same person: the same face shape, eyes, eye colour, brows, nose, lips, jawline, skin tone, the small beauty mark on her left cheekbone exactly as in the reference, and her deep brown below-shoulder soft 2B waves. Do not add any scar. She is clearly an adult, around 23–24.
>
> [shared refined body description]
>
> She wears [shared wardrobe line]. She stands relaxed and front-facing with a slight natural hip shift and her arms at ease, with a calm, quietly alluring expression.
>
> The entire body is visible from the top of her head to her shoes, with no cropping. Neutral, uncluttered studio background; soft, even, natural daylight; camera at about waist-to-chest height from a moderate distance, with natural portrait-lens perspective and no wide-angle distortion. Photorealistic, with natural skin texture and realistic fabric stretch and folds. One person only, no text.

### 3q-gen (`prompt_3q_gen.txt`)
The same as front-gen, except the pose sentence is replaced with:
> She stands relaxed in a three-quarter view: her body is turned about 45 degrees so her left side is toward the camera, her head turns to look at the camera, her weight rests on her back leg, and her arms hang naturally without covering her hips. Her hip curve and the rounded, lifted shape of her glutes are visible in profile.

### 3q-gen+003 (`prompt_3q_gen_003.txt`)
The same as 3q-gen, with this added after the first sentence:
> The second image shows the same woman full-length; use it only for her upper body, outfit and overall scale, not for her lower-body shape.

## 4. Variants
**12 images:** 4 arms × 3 seeds (4001–4003). That's enough to see whether a method works reliably, not just once, while staying small.

## 5. Estimated cost
- 12 × $0.15 = **$1.80**. In Exp 003, a second reference did not change the price; I'll confirm again on the first image.
- **Proposed cap: $2.50.**
- Month-to-date before this experiment: about $2.13. After: about $3.93 of $110.

## 6. Success criteria
**Review materials:**
- contact sheet
- face-crop sheet
- a **before/after sheet** placing each front image next to the Exp 003 base at the same scale
- **approximate width measurements** on front images: shoulder, waist and hip widths in pixels, taken manually by Claude. They're supporting evidence only and inexact, because pose and clothing affect them.

**Mandatory for each image:**
- **Identity vs 2002 ≥ 4/5** on the face crop. Inconclusive if the face is too small to judge. Inconclusive doesn't pass automatically; reviewers decide.
- **Photorealism ≥ 4/5:** anatomy, hands, feet, joints, fabric.
- **Not exaggerated:** no BBL-like, surgical, cartoonish or generally heavier look. Any of these fails the image.
- **Upper body preserved:** waist no narrower, bust no larger, torso length, stomach and shoulders unchanged. For front-edit, compare directly with the Exp 003 base. For generated images, compare by eye with Exp 003.

**Shape goals:**
- **Front views:**
  - the hip curve is visibly more outward than in the Exp 003 base, side by side
  - the waist-to-hip transition is smoother
  - the upper thighs are slightly fuller
  - supporting measurement: hip-to-waist width ratio higher than in the base, mainly through wider hips, while waist width stays about the same
- **Three-quarter views:**
  - rounded, lifted glute projection visible in profile
  - the hip curve is visible
  - the overall figure still reads slim and athletic
- Scored 1–5 each; target **≥ 3.5 average**.

**Secondary:**
- outfit matches the wardrobe line
- beauty mark on her left cheekbone where visible
- no scar
- hair matches

**An arm passes if** at least 2 of its 3 images meet every mandatory criterion and reach the shape target. The results decide:
- the front-view method: edit an existing image, or generate fresh
- whether the three-quarter view benefits from an Exp 003 body reference

**Not proved by this test:** consistency across outfits, scenes or motion.

## Approval needed
1. Nano Banana Pro, 4 arms × 3 images = 12
2. $2.50 cap
3. The prompts (or ChatGPT's revisions)
4. The Exp 003 base image: `ref2002-seed-3001`, or another
