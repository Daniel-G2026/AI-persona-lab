# AI Persona Lab — Project Specification

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

## Character Identity
**Status: Creative brief approved for first-round exploration; exact visual identity is not locked until the founder selects and approves a reference set.** These are design targets, not proof that any model can preserve them. Prioritize anatomical plausibility and recognizable identity over maximizing every adjective.

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
- **Distinctive landmarks:** Faint smile line(s), small subtle forehead scar, and a discreet beauty mark along the cheekbone. **Exact side and placement of scar/beauty mark are not yet locked**; these must be decided from the selected canonical face and then preserved in every applicable view, rather than flipping left/right between outputs.

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

## Canonical Reference Set
**Status: Not yet generated or approved.**

Build a cohesive reference set depicting the **same original adult fictional character**, not unrelated independently selected faces and bodies:
1. Close-up facial portrait.
2. Full-body front view.
3. Full-body side view.
4. Full-body three-quarter view.
5. Natural seated or walking pose.

Preserve the selected source image(s), exact prompts, model/version, seeds (if supported), settings, and file paths. The founder must approve **both facial and full-body identity** before any large training dataset is assembled.

Reference sheets are not proof of consistency: the pipeline must subsequently reproduce the same person in controlled tests with altered lighting, outfits, settings, poses, and camera angles, plus an early image-to-video test.

## Technical Constraints
- Hardware: Windows 11, Intel i7-14700F, 32 GB RAM, RTX 5060 (verify available VRAM before local training decisions).
- Monthly spending cap: $110 USD.
- Tool selection: Open pending controlled benchmarks.
- Avoid committing to LoRA training, Soul ID, or a large synthetic dataset before initial identity-consistency tests.

## Current Workflow
- Status: Character design brief complete; generating and evaluating canonical identity is next.
- Approved tools: None yet.
- Canonical face and body references: None yet.
- Execution and review responsibilities: See `WORKFLOW.md`.
- Historical tests and costs: See `EXPERIMENT_LOG.md`.

## Decisions
- Use an original fictional adult identity; do not intentionally copy a real person's likeness.
- Define the face and body as one cohesive character.
- Test facial **and full-body** consistency before creating a large training dataset.
- Test image-to-video consistency early.
- Record repeatability, failures, and cost, not just attractive examples.

## Next Action
Use the character design brief above to run a small controlled first-round portrait and full-body generation experiment. Select and approve a coherent face/body identity, lock the exact locations of the scar and cheekbone beauty mark, and test consistency before any large training dataset.
