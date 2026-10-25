# AI Persona Lab — Generation Prompt Library

**Status:** Draft v1, for controlled exploration. The character's *visual identity is not yet approved*. Use `PROJECT_SPEC.md` as the authority; do not turn text-only descriptions into claims of stable identity.

**Operational notes**
- Start with a small portrait batch. Once a portrait is shortlisted, use that image as an identity reference for full-body and multi-view generation *if the chosen model supports image conditioning*.
- Prompts are model-agnostic natural language. Claude should adapt syntax, reference strength, and image aspect ratios to the chosen provider; never assume unsupported controls.
- Save model/version, prompt, reference images, seed (if exposed), image dimensions, settings, and cost in `EXPERIMENT_LOG.md`.
- After selecting a canonical face, explicitly identify which *side* of the forehead scar and cheekbone beauty mark should remain consistent in all views.
- Multi-panel character sheets are a **consistency test**, not proof of a stable identity; panels may drift and should be inspected individually.
- Character must clearly appear adult. Use ordinary non-explicit, non-transparent clothing for initial full-body anatomy and identity tests.

## Prompt 1 — Portrait / Face Candidate

Photorealistic editorial casting portrait of an original, clearly adult woman approximately 23–24 years old, with an intriguingly hard-to-place, racially ambiguous appearance and a subtle Middle Eastern-leaning facial impression. Her face is an elegant, slightly elongated oval with softly defined cheekbones, a feminine tapered jaw, and a gently rounded chin. She has large, striking hazel almond-shaped eyes with subtly lifted outer corners, natural medium-full softly arched eyebrows, an elegant narrow straight-looking nose with a proportionate natural tip, and medium-full softly shaped lips with a subtly fuller lower lip. Her complexion is warm golden-beige, lightly sun-kissed, with realistic pores, delicate variations in skin tone, and healthy skin that is clear but not digitally smoothed. A faint natural smile line, a very small subtle forehead scar, and a discreet beauty mark on a cheekbone add individualized character. Her hair is deep brown, thick, below the shoulders, with naturally imperfect 2B S-shaped waves, a soft hairline, and a polished but effortless texture.

Calm, confident, quietly alluring expression; understated everyday makeup; neutral fitted crew-neck top; minimal jewelry. Head and shoulders fully visible, face near front-facing with slight three-quarter turn, direct believable gaze. Shot as a high-end but natural casting photograph with a portrait lens perspective, diffused daylight, soft shadow detail, neutral uncluttered background, and lifelike color science. Realistic facial asymmetry and microtexture, no overt retouching. One person, one photograph.

## Prompt 2 — Full Body / Silhouette Test

Full-length photorealistic fashion casting photograph of **the same original adult woman as the approved portrait reference** [attach portrait reference if available; otherwise treat this as exploratory, not identity-locked]. She appears approximately 23–24, has warm golden-beige naturally textured skin, elegant elongated oval facial structure, striking hazel almond-shaped eyes, a narrow refined nose, medium-full natural lips, and thick deep-brown below-shoulder 2B waves. Preserve the forehead scar and cheekbone beauty mark from the approved reference rather than inventing or mirroring new marks.

She is approximately 5 feet 7 inches (170 cm) tall, with a slim athletic but softly curvy build and a proportionally longer torso. Her shoulders and ribcage appear balanced, waist naturally narrow, abdomen flat and lightly toned. Hips are softly prominent relative to her slim frame; glutes are rounded and lifted with realistic lower-body muscle and natural softness, not enlarged or surgically exaggerated. Medium natural bust, long toned feminine legs, slim athletic thighs, and softly defined calves. Anatomically plausible proportions in the full-body view, with natural standing weight distribution, gentle asymmetry, and believable joints and hands; a slight inner-thigh separation may occur naturally with stance but must not be forced.

She is wearing a tasteful, opaque, fitted coordinated activewear set with a supportive top and full-length leggings, in a muted neutral color, with simple low-profile sneakers. Standing relaxed in a neutral studio setting, front-facing with a slight natural hip shift, arms at ease. Entire body visible from head to shoes, no cropping, camera held around torso level at a moderate distance with natural perspective (not exaggerated wide-angle legs). Even soft daylight, realistic fabric stretch and folds, no posing that obscures body proportions. Single person, photographic reality.

## Prompt 3 — Multi-View Canonical Reference Sheet

Produce a coherent photorealistic **five-view reference sheet of the exact same original, clearly adult fictional woman**, using the attached approved portrait and full-body reference images as the identity anchors where supported. Do **not** redesign or idealize her between panels. She appears approximately 23–24 with a warm golden-beige complexion, slightly elongated oval face, large hazel almond eyes, softly arched medium-full brows, a refined narrow nose, naturally full soft lips, and thick below-shoulder deep-brown 2B loose waves. Keep the location of her subtle forehead scar and discreet cheekbone beauty mark anatomically consistent with the reference; show them only where the angle makes them visible. Her height impression is about 5 feet 7 inches, with a longer torso, slim lean-athletic frame, naturally narrow waist, proportionate medium bust, softly full hips, rounded but restrained glutes, and long gently toned legs.

Lay out five clearly separated photographic panels:
1. Straight-on head-and-shoulders portrait with a neutral relaxed expression.
2. Full-body standing front view, head to shoes.
3. Full-body true side-profile view, head to shoes.
4. Full-body three-quarter standing view, head to shoes.
5. Natural full-body walking pose or relaxed seated pose, entire person visible.

Use the **same opaque, simple fitted neutral outfit** and the same hairstyle across all five panels to make proportions comparable. Neutral uncluttered background, consistent soft studio illumination, natural camera perspective, skin detail and fabric physics. The face and body must stay recognizably identical; distinguish changes caused by view angle from changes in identity. Clean contact-sheet layout with no decorative graphics, logos, captions, or extra people. No extreme body proportions or smoothing.

## Universal Quality Guardrails

Where supported by the generator, discourage: CGI/3D-render appearance, doll-like skin, oversmoothing, face reshaping between views, beauty-mark/scar relocation, forced thigh gap, unnatural hourglass anatomy, exaggerated bust or glutes, malformed hands, warped limbs, stiff posing, aggressive wide-angle distortion, overdone makeup, inconsistent hair texture, multiple people, text artifacts, and cropped feet in full-body images.

## First Experiment Acceptance Checks
- Portrait realism: believable pores, hairline, eyes, teeth (when visible), facial asymmetry, and small landmarks.
- Portrait-to-body match: same facial identity, complexion, and hair; plausible torso-to-leg and upper-to-lower body proportions.
- Sheet consistency: same individual across all angles; same distinguishing marks (allowing angle-dependent visibility).
- Log the **usable** output rate, not just the best image. Do not claim repeatable identity until separate generations with changed scenes and outfits pass review.
