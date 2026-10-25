# Experiment 003 — First Full-Body Identity Test (Proposal)

**Status:** Proposed by Claude 2026-10-25. **Awaiting founder approval. Nothing generated.**
**Identity references:**
- Primary: Exp 002 Nano Banana Pro seed 2002, `experiments/002-portrait-refine/shortlist/nanobananapro-seed-2002.png`
- Untouched baseline: Exp 001 seed 1001, `experiments/001-portrait/shortlist/seed-1001.png`

## Objective
Generate a believable full-body image of the same woman, preserving the identity from 1001 / 2002 while matching the approved body brief in `PROJECT_SPEC.md`.

## Open question for the founder first
In 2002 the beauty mark is on her **left** cheekbone (the right side of the image as we look at it), and there is no visible scar. Choosing 2002 effectively makes left the canonical side.
**Proposal:** lock "beauty mark on her left cheekbone; forehead scar not yet established" in `PROJECT_SPEC.md`. Needs founder confirmation.

## 1. Model to test first
**Nano Banana Pro Edit** (`fal-ai/nano-banana-pro/edit`), used to generate a new image from reference images.
- It kept her face best in Experiment 002 by a clear margin.
- It accepts several reference images at once, and the price is per output image regardless of how many references are sent.
- FLUX.2 [pro] Edit is a fallback only, given its realism problems in Experiment 002.

## 2. References: 2002 only, or 2002 plus 1001?
Unknown, so test both:

| Arm | Reference images |
|---|---|
| **A: `ref2002`** | 2002 only |
| **B: `ref2002+1001`** | 2002 (primary) + 1001 (supporting view of the same person) |

Two images could anchor identity more firmly. They could also pull the eyes back toward 1001's plain brown. The answer applies to every later experiment.

## 3. Variants and settings
- **8 images:** 4 per arm, seeds 3001–3004.
- Aspect ratio **2:3**, resolution **2K**, PNG. That's about 1664×2496; the actual size will be recorded.
- Safety settings: fal defaults.
- Limitation: in a head-to-shoes frame the face is only about 150–200 px tall, so identity is judged on enlarged face crops (see success criteria).

## 4. Prompt
Arm B adds this to the end of the first sentence: "The second image shows the same woman and is supporting reference only."

> Using the reference photo as the identity source, create a new full-length photograph of the same woman. Keep her face exactly the same person: the same face shape, eyes, eye colour, brows, nose, lips, jawline, skin tone, the small beauty mark on her cheekbone, and her deep brown below-shoulder soft 2B waves. She is clearly an adult, around 23–24.
>
> Body: about 5 ft 7 in (170 cm) tall with natural proportions; a slim, athletic, lean-curvy build with a proportionally longer torso; a flat, lightly toned stomach and a naturally narrow waist; a medium, natural, clearly feminine bust; noticeable but not exaggerated hips; rounded, lifted glutes that are shapely but not oversized; long, toned, feminine legs. Realistic anatomy, joints, hands and feet. Her shape looks like a woman who does Pilates and lower-body training, not surgically enhanced or exaggerated.
>
> She wears a simple, opaque, fitted activewear set in a muted neutral tone: a supportive sports top and full-length leggings, with plain low-profile sneakers. She stands relaxed in a natural pose, front-facing with a slight hip shift and her arms at ease, with a calm, quietly alluring expression.
>
> The entire body is visible from the top of her head to her shoes, with no cropping. Neutral, uncluttered studio background; soft, even, natural daylight; camera at about chest height from a moderate distance, with natural portrait-lens perspective and no wide-angle distortion. Photorealistic, with natural skin texture, realistic fabric stretch and folds, and believable, softly sensual, luxury model-off-duty appeal. One person only, no text.

## 5. Estimated cost
- 8 × $0.15 = **$1.20**. The per-image price with multiple references will be confirmed on the first image before the rest run.
- **Proposed cap: $2.00.**
- Month-to-date before this experiment: about $0.93. After: about $2.13 of $110.

## 6. Success criteria: does the body match the chosen face?
Outputs: the usual contact sheet, plus a **face-crop sheet** showing each image's face enlarged next to 2002 and 1001.
- Proposed: Claude marks the face boxes by eye; no new software.
- Alternative: install OpenCV to crop faces automatically. Needs founder approval.

**Mandatory for each image:**
- **Identity vs 2002 ≥ 4/5**, judged on the face crop: obviously the same woman, not a lookalike.
- **Photorealism ≥ 4/5**: anatomy, hands, feet, joints, fabric, skin.
- **Full frame**: head to shoes, nothing cropped.
- **Natural perspective**: no wide-angle stretching; a plausible head-to-height ratio of roughly 1:7.5.
- **Face–body cohesion**: same skin tone from face to body; believable head, neck and shoulder scale. Not her head on a different person's body.
- **Not exaggerated**: no surgical-looking, BBL-like or doll-like proportions; nothing more artificial than 2002.

**Body brief, scored 1–5 each** (target average **≥ 3.5** in this first test):
- longer torso
- narrow waist / flat stomach
- medium bust
- hips
- glutes (only partly judgeable from the front; fully assessed in the side and three-quarter tests)
- legs
- 5'7" impression

**Secondary:** hair matches the 2B waves; eye colour matches 2002; beauty mark on the correct side if visible (expected to be invisible at this distance).

**Experiment passes if** at least 2 of an arm's 4 images meet every mandatory criterion. The arm with more passes decides whether future work uses 2002 alone or 2002 + 1001.

**Not proved by this test:** consistency across angles and outfits. That comes in the next experiment (side and three-quarter views).

## Approval needed
1. Nano Banana Pro, 2 reference arms × 4 images
2. $2.00 cap
3. The prompt (or ChatGPT's revisions)
4. Face crops marked by eye, or OpenCV
5. Beauty mark side to lock in `PROJECT_SPEC.md`
