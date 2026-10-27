# AI Persona Lab — Project Specification

> **Current production direction (2026-10-27):** see [PRODUCTION_PLAYBOOK.md](PRODUCTION_PLAYBOOK.md). This document retains the original **brown-haired research character brief**; it must not silently override the founder-selected **blonde Higgsfield working persona**. New platform work is tracked in [PRODUCTION_ASSET_REGISTER.md](PRODUCTION_ASSET_REGISTER.md).

## Objective
Create an original fictional adult AI influencer who remains photorealistic and visually consistent across still images and videos. The product is a coherent **full digital human**, not a face alone: facial identity, body shape, proportions, skin tone, hair, and distinctive features must persist across different poses, clothes, scenes, camera angles, and motion.

## Budget
- **Monthly spending cap: $110 USD**, including generation credits, API calls, GPU rentals, subscriptions, and unsuccessful attempts.
- Paid experiments require the founder's approval in advance, with a cost estimate recorded before execution.
- Record actual spend and results in `EXPERIMENT_LOG.md`.

## Success Criteria
- Stable facial identity across expressions, lighting, angles, outfits, and environments.
- Stable **full-body identity**: build, shoulder-to-waist-to-hip proportions, limb-length impression, height impression relative to the scene, skin tone, and any distinctive physical features.
- Realistic skin texture, hair, hands, anatomy, posture, and clothing interaction.
- Believable everyday social-media photographs rather than only polished portraits.
- Consistency across front, side, and three-quarter views and natural seated, standing, or walking poses.
- Convincing video with minimal facial or body-identity drift throughout motion.
- A repeatable workflow with measurable usable-output rate and cost per usable photo/video.

## Identity Branches and Current Character Status

### Active blonde Higgsfield production persona
- Founder elected on 2026-10-27 to **keep** the blonde woman produced in Higgsfield's AI Influencer Studio, with long honey-blonde hair and tinted aviator glasses. She is the **current production test identity** for short-form videos and profile photography.
- Her initial e-commerce-style beige-coat/burgundy-trouser appearance is a **look/outfit**, not a permanently locked wardrobe. Later blouse and selfie variations are allowed.
- The successful Milan-location Motion Transfer established **promising motion and location compositing**, not a fully repeatable identity model.
- A ChatGPT-generated low-angle G63 selfie was approved for **camera angle/composition**; that approval does **not** lock its exact face or make it the definitive profile photograph.
- Only founder approval can formally lock a production master identity. The new blonde master and newer session exports are **not yet imported into this repository**.

### Original brown-haired research brief (preserved)
**Status: Archived reference direction, not silently replaced or converted to the current blonde look.** These design targets explain Experiments 001–011 and must be preserved for traceability. Prioritize anatomical plausibility and recognizable identity over maximizing every adjective.

### Core Profile and Visual Impression
- **Age:** Clearly adult woman in her early 20s; working visual target around 23–24.
- **General appearance:** Hard-to-place, racially ambiguous beauty with a subtly Middle Eastern-leaning impression. Avoid making her appearance an exact copy of any real individual.
- **Overall appeal:** Elegant, refined, luxury/model-like, softly sensual and approachable enough to appear believable in everyday photography; not a hyper-stylized 'AI influencer' or exaggerated body ideal.
- **Complexion:** Warm golden-beige, sun-kissed with a golden undertone. User describes her as roughly Fitzpatrick type III (a sun-reactivity classification, *not* an exact skin-colour specification). Maintain visually stable colour across lighting scenarios.
- **Skin finish:** Clear, healthy, naturally luminous skin with subtle pores, realistic skin texture, and small irregularities. Avoid airbrushed/plastic or excessively filtered skin.

### Face and Appearance
- **Face outline:** Oval and slightly elongated, elegant proportions rather than a round/baby face.
- **Bone structure:** Softly defined cheekbones, gentle tapered jaw, refined softly rounded chin; balanced and feminine rather than sharply hollow or heavily contoured.
- **Eyes:** Noticeably large, captivating hazel eyes; slightly elongated almond shape, subtly lifted outer corners, luxury/editorial gaze rather than exaggerated doe eyes.
- **Brows:** Medium-full, natural-looking, softly arched, groomed without a drawn-on appearance.
- **Nose:** Narrow, elegant, refined bridge and naturally proportionate tip; straight or gently straight profile, not an implausibly pinched surgical look.
- **Mouth:** Medium-full, soft naturally shaped lips, slightly fuller lower lip, gentle Cupid's bow; no conspicuously overfilled appearance.
- **Expression:** Calm and subtly alluring at rest, with a genuine relaxed smile in appropriate shots.
- **Hair:** Deep brown; thick density; mostly type 2B loose S-shaped waves (not tight ringlets); length below shoulders; naturally soft hairline. Glossy, high-maintenance-but-effortless 'rich-girl' waves with natural volume and a little irregularity.
- **Distinctive landmarks:** Faint smile line(s) and a discreet beauty mark along the cheekbone.
  - **Beauty mark: LOCKED (founder, 2026-10-25) on the subject's LEFT cheekbone** (the right side of a front-facing image as the viewer sees it), as in reference 2002. Preserve it in every view where that cheek is visible; never mirror it to the right cheek.
  - **Forehead scar: DEFERRED.** Not established in the canonical references; do not add it until the founder decides otherwise.

### Body and Movement
- **Height:** Approx. 5 ft 7 in (170 cm); maintain believable relative scale using environment/camera cues rather than treating an isolated photo as a precise height measurement.
- **Frame:** Slim, athletic, softly curvy, with a balanced upper body and a proportionally **longer torso**.
- **Silhouette:** Gym-trained lean-curvy with some natural softness. Noticeably narrow-but-realistic waist, flat lightly toned abdomen, proportionately fuller hips and lifted glutes that remain natural for her frame.
- **Shoulders:** Balanced to softly narrower than hips; avoid extremely narrow shoulders or exaggerated hip ratios.
- **Bust:** Medium-sized, naturally rounded with plausible anatomy and subtle asymmetry; fitted clothing may show natural bust contours or moderate cleavage without an augmented/spherical appearance.
- **Hips and glutes:** Gentle but evident curves from front and side, proportionately fuller for a slim build; neither an extreme hourglass nor overtly surgically enhanced proportions.
- **Legs:** Long-looking, toned, feminine legs; slim-to-athletic thighs, gently defined calves, and at most a subtle natural upper-thigh gap when stance and anatomy allow. Do not force a gap in every pose.
- **Posture and movement:** Relaxed, poised, natural weight distribution; believable gait and body mechanics. Not stiff or doll-like.
- **Visual analogy:** A woman who plausibly practices Pilates and trains her lower body, without bodybuilding definition or unrealistically dramatic proportions.
- **Consistency note:** Hold torso-to-leg ratio, shoulder/waist/hip relationship, bust impression, hairstyle, and physical landmarks reasonably stable across outfits and angles. Camera perspective and clothing can change their appearance but should not rewrite anatomy.

### Personality and Positioning
- **Personality:** Not yet selected. Do not infer a full backstory from physical appearance.
- **Lifestyle:** Contemporary, aspirational, stylish; specifics not yet selected.
- **Visual aesthetic:** Soft sensuality, clean luxury, believable everyday model-off-duty presentation.
- **Wardrobe:** Body-skimming/fitted dresses, coordinated activewear sets, occasional tasteful swimwear. Prefer realistic styling rather than exaggerated glamour or constant lingerie-like presentation.
- **Intended appeal:** Primarily male-attractive presentation, while still maintaining credible personal style and everyday realism.
- **Target audience:** Not yet formally defined.

### Visual Guardrails
- Do not produce an underage-looking character; consistently depict a clearly adult woman.
- Avoid extreme BBL-like hips, conspicuously oversized glutes or bust, impossibly tiny waist, or excessively thin runway proportions.
- Avoid generic face drift, porcelain/plastic skin, excessive cosmetic filler look, conspicuous beauty filters, unnatural symmetry, overly heavy makeup, and tightly coiled hair inconsistent with the specified 2B waves.
- Avoid independently constructing an attractive face and unrelated body: every reference view must depict a coherent, single fictional human.
- Show realistic asymmetry and physical variation *without* moving, duplicating, or erasing her distinguishing facial features.

## Preserved Research References (brown-haired branch)

**The portrait and body variants below remain valid historical research references, separate from the new working blonde production persona. Neither body A nor body B has been selected as canonical.**

- Approved/refined brown-haired face: Exp 002 Nano Banana Pro seed 2002 — `experiments/002-portrait-refine/shortlist/nanobananapro-seed-2002.png`.
- Original baseline: Exp 001 seed 1001 — `experiments/001-portrait/shortlist/seed-1001.png`.
- **Body Version A**: `experiments/005-body-ab/base/004-front-gen-v2-seed-4101.png` and `experiments/005-body-ab/base/004-3q-gen-v2-seed-4101.png`.
- **Body Version B** (preferred **provisional** R2 s0.35 reconstruction): `experiments/007-reconstruction/shortlist/B/front-R2-s035.png` and `experiments/007-reconstruction/shortlist/B/three-quarter-R2-s035.png`.
- Brown-haired branch results and identity/body limitations are recorded in Experiments 001–011 in `EXPERIMENT_LOG.md`. Notably, fuller Version B proportions frequently regress when transferred into new settings.

Do not overwrite, repurpose or describe these assets as references for the new blonde production character without founder approval. Keep reference hashes, prompts and source media separated by identity branch.

## Technical Constraints
- Hardware: Windows 11, Intel i7-14700F, 32 GB RAM, RTX 5060 (verify available VRAM before local training decisions).
- Monthly spending cap: $110 USD.
- Tool selection: Open pending controlled benchmarks.
- Avoid committing to LoRA training, Soul ID, or a large synthetic dataset before initial identity-consistency tests.

## Current Workflow (2026-10-27)

- **Videos:** Higgsfield Genjutsu **Motion Transfer** is the active working method: source performance video controls movement and timing; the **blonde character reference** controls identity; a distinct location image controls the new scene. Select actual **@-tagged references** in Higgsfield where supported. Do not treat Object Swap as the default: a user test retained the Instagram watermark and drifted toward the reference performer's face.
- **Stills:** fal.ai **Nano Banana Pro Edit** is used for reference-driven profile images and lifestyle photography without an additional Higgsfield stills upgrade. The G63 project uses the blonde character, supplied white Gucci polo-style blouse, and black/ivory G63 cabin references. Working target is a **1:1, 2K selfie**, photographed from **directly in front at belly/lap height and angled upward**, with sunglasses and kissing/pout lips.
- **External media:** originals and newly generated Higgsfield photos/videos supplied in chat **have not been imported to the repo** by this doc update. Check `PRODUCTION_ASSET_REGISTER.md` before assuming availability.
- **Research tools:** original Nano Banana, Omni/Kling video comparison and A/B silhouette work remain documented, but new bespoke model training is **paused** pending a specific demonstrated blocker.
- **Budget:** initial **$110/month total** remains. Repository API spend through Experiment 011 Part A is about **$6.73**. Additional purchased Higgsfield subscription, user-run generations and manual fal playground charges have **not been reconciled**; do not claim the rest is unspent.
- **Quality:** measure full-motion face stability, correct choreography, sharpness, original scene replacement, no watermark contamination and rights to motion/background materials. Naturalistic quality alone does not establish rights to Instagram source performances.

## Decisions and Guardrails

- Continue creating an original, clearly adult fictional influencer; do not copy the identity of the human performer in a motion source.
- Maintain **identity branch separation**: blonde working production persona vs preserved brown-haired research face/body variants.
- Use real or licensed performance footage for any content intended for publication. Downloadability does not grant commercial rights.
- Preserve all original experiments and pending proposals as **historical records**, not as current run instructions.
- Require costed approval for new paid tests; no automatic LoRA/Soul ID adoption.
- Disclose generated photorealistic content where platforms require it; do not claim invented events/locations or endorsements as real.
- Keep outfit, environment and camera instructions separate from identity and choreography.

## Next Action

1. With a source performance that has appropriate usage rights, generate another **blonde Higgsfield Motion Transfer** clip in a distinctly different, clean environment. Verify continuity, face stability, setting realism, watermarks, actual export resolution and cost.
2. For profile photos, build on the **founder-approved low front-facing belly-height selfie angle** with the blonde identity, white blouse and G63 cabin references. Do not promote an angled or identity-drifting still to final profile status.
3. Record durable asset links, rights, user/platform expenses and comparative quality in the production register/log before making content at scale.
