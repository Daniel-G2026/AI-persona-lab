# Production Playbook — AI Persona Lab

**Current working direction: 2026-10-27**  
**Purpose:** produce believable, repeatable photos and short-form videos of an original **adult fictional AI influencer**, with identity consistency and a credible everyday social-media aesthetic. This document describes the live production workflow; the older experiments and proposals remain historical evidence.

## 1. Current decisions (do not silently overwrite)

- **Primary short-form video workflow: Higgsfield Genjutsu → Motion Transfer.** Use one performance video for movement and camera timing, a character image for identity, and optionally a separate environment photo for the new location. This user-tested approach is more promising than reconstructing every aspect of a character through a bespoke training pipeline.
- **Primary still-image workflow: Nano Banana Pro Edit via fal.ai** (pay-per-generation), for profile photos, outfit changes, and identity-controlled lifestyle stills. Image generation in ChatGPT may serve as a reference/prototype, but do not assume results are the same identity as an upstream reference.
- **Object Swap is secondary:** use it when deliberately retaining the original footage and background; it is **not** the default for creating a substantially different setting. One actual test leaked the source's watermark and showed the source performer's facial appearance bleeding into the intended character.
- **The new working production character is the founder-selected blonde Higgsfield influencer**, with long honey-blonde hair, hazel eyes, aviator-style lightly tinted sunglasses and a polished but believable look. The founder chose to **keep** this result as a working character. This is **not** an instruction to replace or delete the separately approved brown-haired portrait 2002 from Experiments 001–011.
- **Character identity is not the same as wardrobe:** the beige coat/burgundy trousers and later Gucci-style white blouse are outfits, not permanently attached character features. Glasses are part of the current blonde styling, but can vary intentionally if the founder requests it.
- **Do not start LoRA, Soul ID training, 3D/warp-body reconstruction, or another large custom pipeline without a demonstrated unmet need and an approved, costed experiment.**
- Preserve original research references: Exp 002 portrait 2002, Exp 001 seed 1001, Version A front/three-quarter and Version B R2-s035 front/three-quarter. Both body versions remain **unselected**, and apply to the older brown-haired design exploration unless explicitly repurposed by the founder.
- **Transparency and rights:** label or disclose AI-generated photorealistic content as required by the target platform; use performances, location photos, logos and music only with rights suitable for intended publication. Downloading an Instagram Reel does not grant permission to republish or transform it commercially.

## 2. Video: motion + character + new location

### Choose the correct mode
| Mode | Reference behavior | Use it when | Known issue |
|---|---|---|---|
| **Motion Transfer** (default) | Extracts temporal motion from a video, synthesizes the selected character/scene | Same choreographed movements, **new person and new location** | Background may be regenerated, softened or inconsistent |
| **Object Swap** | Replaces a person/object while generally retaining more of the source scene | Preserving **the original filmed environment** is intentional and licensed | Our Instagram test preserved the watermark/source scene and exhibited facial identity bleed |

### Inputs and preparation
1. **Performance source video (one video in the Genjutsu interface)**: prefer **original or properly licensed** 4–30 s footage (confirm current UI). Favor a continuous 9:16 clip with simple movement, consistent camera position, good exposure and a clearly visible person. Trim a closing Instagram-logo bumper *if present in material you are authorized to transform*; never treat watermark removal as a substitute for licensing.
2. **Character reference image**: the founder-approved blonde Higgsfield output, preferably a reasonably clear face plus full body for whole-body content. This image determines **who** appears, not the actions or location.
3. **Location reference image (optional)**: a clean photo or generated reference of the **new** environment. If a person dominates the location image, an AI model may confuse subjects; favor an unoccupied scene or remove distracting foreground figures when editing is permitted. Avoid screenshot carousel arrows, dots, UI and unwanted captions. **A cleaned/re-generated reference may not be pixel-identical to a real location photo.**
4. Keep the scene camera view/perspective compatible with the performance; a reference still can guide architecture/lighting but does **not** lock every background pixel.
5. Where Genjutsu lets you type **@-mentions**, select actual attached media from the application's autocomplete; do **not** merely type fake `@Name` strings. Name the source video, character image and location image distinctly, and assign a single role to each.

### Recommended concise prompt structure
Use the **actual media mentions inserted by the UI** in place of the placeholders:

```text
@MOTION_REFERENCE — MOTION ONLY: faithfully reproduce the original walking,
gestures, head turns, posture changes, timing, pacing and source camera
movement. Do not invent new actions, new camera moves or a new performance.

@CHARACTER_REFERENCE — CHARACTER ONLY: replace the source performer with
this same adult blonde woman. Keep her face, hairstyle, sunglasses (if used),
body proportions and selected outfit consistent in every frame and angle.
Do not blend her face with the source performer's identity.

@LOCATION_REFERENCE — ENVIRONMENT ONLY: set the performance in this new
location. Follow the reference's architecture, perspective, street details
and lighting; place the character at a natural scale with correct shadows.

Final: source video's motion + character reference's identity + location
reference's setting. Natural smartphone optics, coherent sharp environmental
detail and believable skin, hair and fabric. No imported overlays, unwanted
watermarks, artificial bokeh, facial morphing or abrupt scene changes.
```

**Important:** role-specific prompt language **reduces ambiguity**; it cannot guarantee that the model isolates every source, removes all artifacts, or exactly recreates a location.

### Source quality and cropping
- **Prefer an original vertical MP4** over a Windows desktop Snipping Tool screen recording. Avoid multiple lossy exports.
- A download may be 1920×1080 landscape while containing a **narrow vertical video with black side bars**. Crop *the bars only*, preserving the entire actual vertical picture. Do not enlarge an already-small crop and assume pixels become sharper.
- In Higgsfield's `Edit reference` crop panel, pull horizontal crop handles to the video edges; retain the top/bottom unless trimming a real overlay is authorized and does not cut out the performance.
- **Higgsfield on-screen preview sharpness is not proof of downloaded-file sharpness.** Compare playback at the *same displayed size* and inspect actual output width/height and compression. Past exports were ~720×1280 and could look softer maximized. Select higher export quality if offered and affordable; upscaling cannot recreate missing detail reliably.
- Avoid significant source-video lettering, social-app watermarks and closing logo bumpers; a generative video may reproduce them (especially Object Swap).

### Result evaluation and save procedure
- Watch from beginning to end at normal speed, *then* inspect frames around large head turns, hair movement, profile-to-front transitions and hand contact.
- Separately rate: **(a) face/identity stability; (b) motion fidelity; (c) body/garment consistency; (d) environmental sharpness and stability; (e) overall smartphone believability; (f) originality compared with licensed performance; (g) rights/readiness for publication.**
- Check for source-performer identity leakage, watermark/caption carryover, sudden face morphs, unnatural arms/legs, repeated/frozen pedestrians, invented background features and garbled signage.
- Record platform, mode, model, all input reference identifiers, selected @ tags, output dimensions/duration, estimated and actual credit use, human observations, and output location. Preserve the original media, exported video and any edited version separately. A good-looking single clip **does not establish** repeatable production quality.

## 3. What actual tests taught us (2026-10-27)

| Test | Source/mode | Observed result | Operational takeaway |
|---|---|---|---|
| First Genjutsu test | Desktop screen-recorded/cropped Instagram reference; Motion Transfer | Roughly tracked walking, turns and gestures; original blonde character remained broadly recognizable; background quality was a concern | Motion-driven video is technically viable; source quality and export require checking |
| Second Genjutsu test | Phone-downloaded Instagram copy; apparently **Object Swap** (founder not fully certain) | Original scene and Instagram watermark carried over; character face became inconsistent and resembled source creator | Cleaner source alone cannot solve **mode/identity** errors; avoid Object Swap as default |
| **Milan location test** | Motion Transfer + blonde character + clean Milan-street location reference, with explicit @ roles | 9 s vertical output followed reference gestures, retained new street environment, and reduced severe face drift; **not flawless** (some synthetic movement, face softness/variation, quieter background) | Best current practical proof-of-concept; **keep, but do not treat as perfect or fully repeatable** |

The Milan street picture supplied in chat was reconstructed as a *new generated clean scene reference* after identifying a foreground pedestrian and carousel controls. It should not be labeled a pixel-preserving edit or a real untouched background photograph.

The historical fal Experiment 011 Part A also generated **two distinct café image-to-video tests** using Omni Flash and Kling + Elements. Those tests belong to the earlier **brown-haired** reference branch; do not confuse them with the **blonde Higgsfield** workflow. See `EXPERIMENT_LOG.md`.

## 4. Stills: profile photos and lifestyle images

### Workflow
1. Use **Nano Banana Pro Edit on fal.ai** when Higgsfield image features require an additional subscription/upgrade. The multi-reference **Image URLs** inputs hold the character photo, wardrobe/product photo, and location/interior photo. Do not misuse `context` as image-reference storage.
2. Give explicit roles: `@Character` = identity, `@Outfit` = clothing, `@Interior` = environment; **only use @ mention syntax if that particular UI actually resolves attached references**. On fal, describe reference images by numbered order when there is no supported tagging.
3. Initial output setting for a social profile image: **1:1 square, 2K, one image** when supported. Compose for **circular cropping**; leave safe room around hair/glasses.
4. For natural social-media stills, use believable smartphone optical character, normal exposure and credible environments, not a perfectly polished commercial image.
5. Keep generated prototypes separate from **identity-locked** references. A new face in a flattering still may drift even when the overall styling matches.

### Specific tested concept: G63 low-angle profile selfie
- Character: the working blonde woman with oversized warm-tinted sunglasses and hazel eyes.
- Wardrobe reference: short-sleeved **white collared Gucci blouse**, button placket and fitted smocked waist; the user supplied the garment photo.
- Interior reference: **Mercedes-AMG G63-style black dashboard**, circular/turbine vents, steering wheel, center console and quilted ivory leather seats. The supplied interior photo is photographed from the passenger side and may require carefully specified driver-seat positioning.
- Expression: playful soft **kissing/pout** lips, sunglasses on; neutral-natural skin texture.
- **Correct camera angle is essential:** phone is **directly in front of her at belly/lap level**, pointed **upward toward her centered, forward-facing face**. NOT held at arm's length from the upper left/right, not a three-quarter photo taken by another person. Arms may extend toward the bottom edge to indicate a real selfie.
- Frame: head, sunglasses and lips prominent, upper torso and enough cabin context to register G63 luxury interior. A square 1:1 composition needs to withstand a tight Instagram/TikTok circular profile crop.
- First Nano Banana result successfully combined the references but placed the camera off to the side / too high. A subsequent **image prototype in ChatGPT** demonstrated the desired centered, low-angle perspective; the founder explicitly approved **that angle**. It is a **composition reference**, not automatically a verified identity-matched final profile photo.

**Camera-angle correction prompt:**

```text
Use the same adult blonde character and the supplied white collared,
smocked-waist blouse, inside the driver's seat of a black-and-ivory G63.
Make this a genuine SELFIE: the phone is held straight in front of her
body at belly/lap height and pitched upward toward her face, not off
to either side. She looks directly at the lens and makes a gentle
kissing-lips expression, wearing warm-tinted oversized sunglasses.
Low-angle perspective shows her face, underside of sunglasses,
upper torso, roofline and recognizable ivory seats / G63 dash.
Physically plausible driver-side steering wheel placement, window
light, dashboard geometry and reflections. Natural skin texture;
no distorted hands or synthetic glamour lighting. Square 1:1,
centered for a circular profile crop.
```

### fal Nano Banana Pro playground validation issue (observed)
The optional `context` field exposed an invalid placeholder array `[{"type":"","text":""}]`, causing a type-tag validation error (`text|image|document|signature` expected). If the UI permits it, use `[]` or supply a valid entry such as `[{"type":"text","text":"Use the uploaded image references as described in the prompt."}]`. Same principle for empty `history`. Do not change generation resolution in response to this input-structure error.

## 5. Production guardrails and next actionable milestone

- **Current scope is validation, not training.** Make a small number of varied authorized-content tests. Do not infer production scalability from one successful Milan clip.
- For the next **video**, record or license a short, clear vertical performance, pair it with the working blonde identity and a clearly distinct location reference, and test one Motion Transfer output. Ask founder approval before spending credits.
- For the next **profile still**, use the founder-approved *low-angle* prototype as **camera/composition guidance** along with the blonde identity, blouse and G63 interior; verify that the face remains the same working character. Do not silently adopt the prototype's facial details as canonical.
- After three substantially different videos and three stills, review usable-output rate, manual corrections per post, stability of identity and cost per usable asset.
- **Budget:** reconciled 2026-10-27: Higgsfield plan **$19/month** (270 credits/month) + fal.ai **$6.78** to date (founder-reported from the fal dashboard) = **$25.78 month-to-date, $84.22 remaining** of the **$110 USD** monthly cap (subscriptions included).
- **Ownership/permission:** only use licensed or self-shot performances and backgrounds for public content. A generative model's ability to erase a watermark does not clear the original creator's rights. Don't misrepresent synthetic scenes as evidence of real events or undisclosed real-world endorsements.

## 6. Files, responsibility and recordkeeping

- `PROJECT_SPEC.md` defines original research identity and creative guardrails.
- `EXPERIMENT_LOG.md` records original experiments and the 2026-10-27 platform pivot.
- `STRATEGY_REVIEW.md` and Exp 011 proposals are historical snapshots unless specifically reapproved.
- `PRODUCTION_ASSET_REGISTER.md` lists new character/video/still reference assets and whether actually imported into this repository.
- Founder selects character/look, authorizes payments, approves publication; Claude Code can implement documentation/automation; ChatGPT reviews prompts, image/video quality and source provenance.
- **Do not claim a new character or asset is committed in GitHub merely because it appeared in a chat attachment.** Import user-authorized, rights-cleared masters to agreed local storage first, then record durable, truthful paths and hashes; avoid storing externally sourced copyrighted video in Git by default.
