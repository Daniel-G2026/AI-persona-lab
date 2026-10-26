# Experiment 009 — Smartphone Believability + Early Video Proof of Concept (Proposal)

**Status:** Proposed by Claude 2026-10-25. **Awaiting founder approval. Nothing generated, nothing spent.**

## The question
Not "can we make her attractive?", but **"can we produce believable, casual social-media content of the same woman, repeatedly?"** Exp 008's photos were technically photorealistic but read as AI: too clean, too evenly lit, too posed, stock-photo framing.

## Fixed anchors (unchanged; hash-checked)
- Face: **2002** (`experiments/002-portrait-refine/shortlist/nanobananapro-seed-2002.png`)
- Body, **Version A** (neither version is canonical): `experiments/005-body-ab/base/004-front-gen-v2-seed-4101.png`, `…/004-3q-gen-v2-seed-4101.png`
- Body, **Version B**: `experiments/007-reconstruction/shortlist/B/front-R2-s035.png`, `…/three-quarter-R2-s035.png`

## Part 1 — Casual smartphone stills

### What usually makes AI photos read as AI, and how this test counters it
| AI tell | Counter-measure in the prompts / pipeline |
|---|---|
| Studio-even, flattering light | One real light source plus spill: window daylight mixed with a warm lamp, or flat overcast; hard shadows allowed |
| Shallow "portrait-lens" bokeh, perfect composition | **Phone optics**: deep depth of field, slightly wide main-camera perspective, imperfect off-centre framing, horizon slightly tilted |
| Over-clean, empty sets | **Lived-in environments**: everyday clutter, ordinary objects, imperfect surfaces |
| Posed model stance, camera-aware expression | Candid moments: mid-movement, mid-laugh, glancing at the phone; a mirror selfie where she is looking at her phone screen |
| Airbrushed skin, perfect hair | Unretouched skin with pores, slight shine, flyaway hairs, natural under-eye texture |
| Pristine 2K render | **Free local "phone pass"** (variant b): slight sensor noise, mild phone-style sharpening, smartphone-typical JPEG compression, resized to 1080×1920. No paid calls. |

### Design: 4 paid stills, plus 4 free processed variants
**2 scenarios × 2 body references (A, B).** Same face anchor and scenario text within each pair, so body consistency can be compared directly, while realism is judged across two very different everyday situations.

| ID | Scenario | Body refs | Why this scenario |
|---|---|---|---|
| 9-S1-A / 9-S1-B | **Mirror selfie** in a lived-in apartment hallway or bedroom | A / B | Influencer staple; naturally full-body; the phone in hand explains the framing |
| 9-S2-A / 9-S2-B | **Friend-taken candid** outside a neighbourhood coffee shop, holding an iced coffee, mid-laugh | A / B | Tests real-world environment, people and street detail, and candid posing |

- **Model:** Nano Banana Pro Edit (fal), **9:16, 2K**, PNG, seeds 9101–9104.
  - 9:16 matches phone photos, Stories and Reels, and gives the video stage a vertical start frame.
- **References in order:**
  1. 2002 (face)
  2. body front (A or B)
  3. body three-quarter (A or B)
- **Variant b** for each still: the free local phone pass (`scripts/phone_pass.py`). Identical content; only camera and processing character differ. Reviewers rate a and b **without being told which is which**.

### Still prompts
**Shared opening** (body sentence chosen per version):
> Use the reference images as follows. Image 1 is her face: keep her exactly the same person, with the same face shape, eyes, brows, nose, lips, skin tone, the small beauty mark on her left cheekbone, and her deep brown below-shoulder soft 2B waves. Images 2 and 3 show her body: keep exactly this body shape and these proportions, [**A:** a slim, balanced, lean-curvy figure with moderate hips and toned legs] / [**B:** a slim upper body with a narrow waist and a clearly fuller lower body: broad hips, full upper thighs and rounded, projected glutes]. Take only face and body from the references, not their pose, clothes, lighting or background. She is clearly an adult, around 23–24. No scar.
>
> This must look like a real, unedited photo taken on a smartphone and posted casually to Instagram: not a fashion shoot, not stock photography, not a studio. Deep focus with everything reasonably sharp (no portrait-mode blur), the slightly wide perspective of a phone's main camera, natural smartphone colour and dynamic range, a little digital noise in the shadows. Real, unretouched skin with visible pores, slight natural shine and tiny imperfections; a few flyaway hairs; minimal everyday makeup. Ordinary, imperfect framing.

**S1 — mirror selfie:**
> She takes a mirror selfie in the full-length mirror of a lived-in apartment hallway on a weekday afternoon, holding her phone at chest height in one hand so her face stays visible, glancing at the phone screen with a small relaxed smile. She wears a fitted grey ribbed tank top, high-waisted black leggings and white socks, with no shoes. Behind her: a coat rack with a jacket, a tote bag on the floor, a pair of sneakers, a small side table with keys and a plant; a slightly scuffed wall and a doorframe. Light comes from a window out of frame on one side, plus a warm ceiling light, so there are mixed colour temperatures and soft real shadows. The mirror has a few faint smudges. Her full body is visible in the mirror, and the phone and her hand are visible.

**S2 — friend-taken candid:**
> A friend snaps a quick candid photo of her on a phone outside a small neighbourhood coffee shop on an overcast late-morning day. She is mid-laugh, looking slightly off-camera as if reacting to something the friend said, holding an iced coffee in a plastic cup in one hand, her other hand pushing her hair back. She wears fitted high-waisted light-wash jeans, a cropped white t-shirt and worn white sneakers; a small crossbody bag. Behind her: the café's window with reflections, a chalkboard sign, a bicycle locked to a rack, a parked car and a couple of passers-by at ordinary distance. Flat, diffuse daylight with soft shadows under her chin. She is shown from head to about the shins, framed slightly off-centre and a little tilted, as a friend would quickly take it.

## Part 2 — Early video proof of concept
### Research summary (checked 2026-10-25)
| Option | Access | Price | Character consistency | Notes |
|---|---|---|---|---|
| **Gemini Omni Flash 1.1** (Google) | **fal** `google/gemini-omni-flash/v1.1/image-to-video` (**existing account/key**); also Gemini API (`gemini-omni-1.1-flash`), AI Studio, and Flow (Google AI Plus/Pro/Ultra) | **$0.03/s at 360p (draft)**, $0.10/s at 720p, $0.15/s at 1080p, $0.30/s at 4K | Image-to-video from a start frame (optional end frame). A separate reference-to-video endpoint accepts reference images plus up to 3 reference videos (≤ 10 s each), 3–10 s output, 16:9 or 9:16. Scene extension to 40 s. | Generates synchronized audio. Cheap 360p drafts suit iteration. Regional limits apply to *uploaded-video* editing (EEA, CH, UK, some US states); image-to-video not affected per sources. |
| **Runway Gen-4.5** | **Runway** web app or Runway API ("Runway Dev"): **needs a new Runway account and key, which the founder must create**. No fal endpoint found. | **12 credits/s = $0.12/s** on the API ($0.01/credit). Web free tier: 125 one-time credits ≈ 10 s of Gen-4.5. | Image-to-video from a start frame; third-party reports of single-reference character consistency (not confirmed in primary docs) | 2–10 s clips, 720p. Strong motion quality reputation. |
| Alternatives on fal (not proposed now) | fal | Kling v3 Pro $0.112/s; Veo 3.1 Fast $0.10/s (no audio); Seedance 2.0 ≈ $0.30/s | Kling has "element" references for characters | Fallbacks if the two above disappoint |

### Proposed video test: 1 clip, plus an optional comparison
- **Input:** the **strongest still** from Part 1, chosen by the founder and ChatGPT at a stop point after the stills.
- **Primary: Gemini Omni Flash 1.1 on fal,** 9:16, 5 s (or the nearest allowed duration):
  1. **360p draft** (≈ $0.15) to check motion and identity cheaply
  2. if acceptable, **one 720p clip** (≈ $0.50)
  - Audio is ignored or stripped; this is a silent, motion-only test.
- **Optional:** the same still and prompt on **Runway Gen-4.5** (5 s, 720p, ≈ $0.60), only if the founder creates a Runway account and key. Alternatively, the founder can run it manually in the Runway web app on the free 125 credits; Claude can't create accounts.
- **Motion prompt** (simple, natural, no complex action; adapted to the chosen still):
  > Continue this exact photo as a short, real smartphone video. She stays in the same place and makes small, natural movements: [S1: she glances from the phone screen to her reflection, smiles slightly and shifts her weight from one leg to the other] / [S2: her laugh settles into a smile, she tucks her hair behind her ear and takes a small sip of her iced coffee]. Slight natural handheld camera movement, no cuts, no zoom, no change of angle. Keep her face, hair, body shape and clothes exactly as in the photo. Realistic motion of hair and fabric, natural blinking, consistent lighting and background.

## Evaluation: four separate scores (never averaged together)
**1. Face consistency** (vs 2002 and 1001; face crops)
- identity 1–5
- beauty mark on the left cheekbone
- styling drift flagged separately

**2. Body consistency** (vs the matching A or B reference)
- does the image read as the intended version (A or B)? 1–5, a qualitative judgement
- does it regress toward a default slimmer figure? yes/no
- supporting ratios only where the pose allows

**3. Still-image realism**, scored 1–5 each:
- **skin texture** (pores, shine, imperfection; not airbrushed)
- **camera characteristics** (phone depth of field, perspective, noise, dynamic range, framing)
- **environmental realism** (lived-in detail, physical plausibility, no garbled text or warped objects)
- **physical lighting** (single, coherent light sources; shadows and colour temperatures consistent)
- **posing and expression** (candid, not modelled)
- **AI-tell checklist:** hands, teeth, background people, reflections in the mirror and window, text and signage, symmetry, hair edges
- **Overall: "would a typical Instagram viewer scrolling past suspect this is AI?"** 1 = obviously AI … 5 = passes. Rated **blind to variant a/b**.

**4. Video realism**
- temporal face consistency (frame grabs at 0 / 2.5 / 5 s vs 2002)
- body consistency through motion
- motion naturalness (weight shift, blink, hair, fabric)
- camera behaviour (believable handheld, no warping)
- artifacts (morphing hands, background boiling, flicker)
- overall "would pass as a real phone video" 1–5

**Repeatability** (the real question): the share of the 4 stills that pass identity ≥ 4 **and** the overall realism score ≥ 4. This is a first data point, not proof. If promising, the next step is a larger batch of the best scenario type to measure the usable-output rate properly.

## Costs (estimated; prices re-checked on fal before running)
| Item | Calc | Cost |
|---|---|---|
| 4 stills, Nano Banana Pro 2K | 4 × $0.15 | $0.60 |
| Phone-pass variants | local | $0.00 |
| Video draft, Omni Flash 1.1 360p | 5 s × $0.03 | $0.15 |
| Video final, Omni Flash 1.1 720p | 5 s × $0.10 | $0.50 |
| **Subtotal (recommended scope)** | | **$1.25** |
| Optional: Runway Gen-4.5, 5 s 720p (needs the founder's Runway account) | 5 s × $0.12 | $0.60 |

- **Recommended cap: $2.00** (or $2.50 including the Runway option).
- Month-to-date ≈ $4.77 → ≈ $6.02–6.62 of $110.

## Execution stops
1. Generate 4 stills plus the free phone-pass variants → **stop** for blind review and choice of the strongest still.
2. Video 360p draft → quick check (Claude reports; continue to 720p only if motion and identity are acceptable, otherwise stop).
3. Video 720p (and optional Runway) → **stop** for review.

## Storage
- `experiments/009-realism-video/`: `config.json`, prompt files, `scripts/phone_pass.py` settings, `runs.jsonl`, contact sheets (raw vs phone pass, labelled only after review), face crops, body comparison, realism score sheet, video files (originals local and mirrored), frame-grab sheet, `review.csv`.

## Platform note
Instagram and Meta require AI-generated, photorealistic content to carry an AI label. "Believable" here means natural-looking content quality, not hiding that the character is AI-generated.

## Approval needed
1. Part 1: 4 stills (2 scenarios × A/B) plus free phone-pass variants, and the prompts
2. Part 2: Omni Flash 1.1 video (draft, then 720p) on the chosen still; Runway yes or no
3. Cap ($2.00, or $2.50 with Runway)

## Sources
- [Google: Gemini Omni 1.1 Flash developer post](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/)
- [fal: Gemini Omni Flash 1.1 image-to-video](https://fal.ai/models/google/gemini-omni-flash/v1.1/image-to-video) · [reference-to-video](https://fal.ai/models/google/gemini-omni-flash/v1.1/reference-to-video/llms.txt) · [fal how-to](https://fal.ai/learn/tools/how-to-use-gemini-omni-flash-1-1)
- [Runway API pricing docs](https://docs.dev.runwayml.com/guides/pricing/)
- [Atlas Cloud: Omni Flash availability and costs](https://www.atlascloud.ai/blog/tips/gemini-omni-flash-1.1-availability)
- [fal: best image-to-video APIs 2026](https://fal.ai/learn/tools/best-image-to-video-apis-2026)
- Runway Gen-4.5 overviews: [The Rundown](https://www.therundown.ai/tools/runway-gen-4-5), [eesel](https://www.eesel.ai/blog/runway-ai-pricing), [ModelsLab](https://modelslab.com/blog/api/runway-gen-45-image-to-video-api-developers-2026)
- Omni Flash overviews: [MindStudio](https://www.mindstudio.ai/blog/gemini-omni-1-1-flash-video-model), [eesel](https://www.eesel.ai/blog/gemini-omni-1-1-flash)
