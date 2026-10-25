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
**Status: Not yet defined or approved.** Do not treat placeholder traits as final.

### Face and Appearance
- Adult age:
- Ethnicity / general appearance:
- Face shape and features:
- Eye colour / shape:
- Hair texture, colour, length, and hairline:
- Complexion / skin undertone:
- Distinctive marks or features:

### Body and Movement
- Height / height impression:
- Body build:
- Shoulder, waist, and hip proportions:
- Leg and arm proportions:
- Overall silhouette:
- Typical posture and movement:
- Distinctive physical features:

### Personality and Positioning
- Personality:
- Lifestyle:
- Visual aesthetic:
- Target audience:

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
- Status: Discovery and full-character design.
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
Define and approve the character's facial appearance, body morphology, and positioning; then run a small controlled generation experiment producing initial portrait and full-body candidates. Do not begin large-scale dataset generation yet.
