# Experiment 011 Part B — 4-Image Pilot: Real Background vs Generated Scene (Proposal)

**Status:** Proposed by Claude 2026-10-26. **Awaiting founder approval and the background photo. Nothing generated.**

## Question
Can **W2 (real background + Nano Banana Pro)** put the same woman into a **real photograph without regenerating it**, keeping its lighting, geometry, perspective, objects and text? And how does it compare with **W1 (Nano fully generated scene)** in the same scene?

## Scene
**Home kitchen, morning window light.** She stands at the counter making coffee in a three-quarter view, upper body to about mid-thigh, a friend-taken phone photo.

## The background (W2)
**Recommended: the founder's own phone photo.** It is rights-clean by ownership and genuinely phone-camera (optics, HDR, noise), which a stock DSLR photo isn't.
- **Shot spec:**
  - your kitchen (or a friend's, with permission), morning light from a window, the phone held vertically at chest height, **portrait 3:4**, default camera, no portrait mode
  - empty of people; no visible brand logos
  - a clear area of counter and floor where a person could stand
  - **include one small piece of real, simple text** as a preservation probe, e.g. a handwritten sticky note on the fridge reading "milk, eggs, coffee", or a wall calendar
  - Send the original file (HEIC/JPG straight from the phone).
- **Fallback:** a vetted, free Unsplash photo with no people or brands, chosen and approved by the founder before Claude downloads it. Licence: commercial use allowed, no attribution required, can't be resold unmodified. It doesn't address AI use or property/trademark releases, which is another reason to prefer your own photo.
  - Candidates seen (not downloaded): [kitchen with a sink and a window](https://unsplash.com/photos/a-kitchen-with-a-sink-and-a-window-siZbxDGY2mA), [kitchen window with sun through the blinds](https://unsplash.com/photos/a-kitchen-window-with-the-sun-shining-through-the-blinds-FH1t3LsPg5c), [kitchen with a sink, dishwasher and a window](https://unsplash.com/photos/a-kitchen-with-a-sink-dishwasher-and-a-window-NQ5OB3vrdOo)
  - Their metadata shows DSLR or mirrorless cameras, not phones, and they have no text probe.
- The background is hash-recorded and never modified. It's used at its native aspect ratio (3:4).

## The 4 images
| ID | Workflow | Body refs | References sent, in order |
|---|---|---|---|
| P-W1-A | W1 generated scene | Version A | 2002, A front, A three-quarter |
| P-W1-B | W1 generated scene | Version B | 2002, B front, B three-quarter |
| P-W2-A | W2 real background | Version A | **background**, 2002, A front, A three-quarter |
| P-W2-B | W2 real background | Version B | **background**, 2002, B front, B three-quarter |

Nano Banana Pro Edit, **3:4, 2K**, PNG, seeds 11101–11104, fal default safety settings. Body is recorded, not optimized.

## Prompts
**Shared identity/body/style block** (same for all 4; body sentence per version), reused verbatim from Exp 009:
> Image [face] is her face: keep her exactly the same person, with the same face shape, eyes, brows, nose, lips, skin tone, the small beauty mark on her left cheekbone, and her deep brown below-shoulder soft 2B waves. Images [body] show her body: keep exactly this body shape and these proportions, [A: a slim, balanced, lean-curvy figure with moderate hips and toned legs] / [B: a slim upper body with a narrow waist and a clearly fuller lower body: broad hips, full upper thighs and rounded, projected glutes]. Take only face and body from those references, not their pose, clothes, lighting or background. She is clearly an adult, around 23–24. No scar. Real, unretouched skin with visible pores and slight natural shine; a few flyaway hairs; minimal everyday makeup. Prioritize ordinary, everyday photographic believability over beauty or polish.
>
> She wears a soft grey oversized t-shirt and fitted black bike shorts, barefoot. She stands at the kitchen counter in a natural three-quarter view, pouring hot water from a kettle into a mug, glancing toward the camera with a small sleepy smile, as if a friend just took a quick phone photo of her.

**W1 scene sentence** (appended):
> Create a real, unedited smartphone photo of her in an ordinary lived-in apartment kitchen on a weekday morning: soft window light from one side, a kettle, a few mugs, a cutting board and a plant on the counter, a fridge with a handwritten sticky note reading "milk, eggs, coffee". Deep focus, phone main-camera perspective, natural phone colour and slight noise, imperfect framing, upper body to mid-thigh.

**W2 scene sentence** (appended; image 1 = background):
> Image 1 is a real photograph of a kitchen. Use it exactly as the scene: do not change, move, add, remove or restyle anything in it. Keep its lighting, colours, perspective, camera angle, framing, objects and any text exactly as they are. Add her into this photograph, standing naturally at the counter, at a correct size for the room and camera distance, lit by the same window light with matching shadows on her and on the counter and floor, and with the same focus, grain and colour as the photograph, so it looks like one real photo taken on the same phone.

## Evaluation
**1. Environment preservation (W2 only; the key question).**
Claude compares each W2 output with the original background:
- **Geometry and perspective:** an edge-map overlay of output vs background, outside her silhouette. Do lines, cabinets, window and counter edges stay in place? Mean edge displacement in px.
- **Pixel preservation:** mean absolute difference outside her silhouette and its shadow. A low value means preserved; a high value means regenerated.
- **Objects:** a checklist of every visible object in the background. Each is present and unchanged / moved / altered / removed. Anything added is listed.
- **Text probe:** is the real note or calendar text **identical** (same words, same handwriting)?
- **Lighting:** same direction and colour temperature; her shadows consistent with the window.
- **Verdict:** *preserved* (output-vs-background difference small, all objects intact, text identical) / *partly regenerated* / *regenerated*.

**2. Face consistency** (all 4): face crop vs 2002, 1–5.

**3. Body consistency** (all 4): reads as intended A/B? regression yes/no. Diagnostic only.

**4. Photographic realism** (all 4): the Exp 009 sub-scores plus the blind "would a scroller suspect AI" 1–5. For W2 specifically: does she look **pasted in** (edge halos, scale, lighting mismatch)?

**5. Usable without correction:** identity ≥ 4, realism ≥ 4, no major artifacts; for W2, also environment *preserved*.

**6. Failure diagnosis** (per founder decision 3): each failure is tagged **face / body / background / posing / general photorealism**, so the next step targets the real bottleneck. No LoRA recommendation unless the diagnosis points to it and a clean, consistent dataset exists.

**Blind human ratings:** the 4 pilot images under new codes with a sealed key (Exp 009 procedure), optionally alongside the real background photo as a control.

**Contingency (free, only if W2 regenerates the scene):** a "W2-composite" variant pastes only her (and her shadow) from the W2 output back into the untouched real photo using a person mask. Environment preservation is then guaranteed; it's evaluated for edge and lighting integration. No extra API cost.

## Cost
- 4 × Nano Banana Pro Edit 2K ($0.15) = **$0.60**. Recommended cap **$0.80**. Price re-checked before running.
- If the pilot succeeds, the next step is the multi-scene expansion to measure usable-output rate, proposed separately.

## Approval needed
1. The background source: your phone photo (recommended, with the shot spec above) or a specific Unsplash photo you pick
2. The 4-image design and prompts
3. The cap
