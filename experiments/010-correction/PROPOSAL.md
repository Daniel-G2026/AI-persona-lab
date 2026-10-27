# Experiment 010 — Minimal Image Correction (Proposal)

**Status:** Proposed by Claude 2026-10-26. **Awaiting founder approval. Nothing generated, nothing spent.**

## Goal
Produce **one convincing, identity-consistent casual photo** to serve as the first video-test input, by fixing only what Exp 009's review flagged and **keeping everything else pixel-identical**:
- **Mirror selfie:** facial drift vs portrait 2002.
- **Café photo:** gibberish signage and lettering.

No body-shape work. Version A and Version B stay separate and provisional. All Exp 009 originals and phone-pass variants stay untouched (read-only; hashes recorded).

## Method: edit, then composite back only the corrected region
Exp 007 showed that a full re-render (R3) improves one thing but quietly changes others (face styling, body). So:
1. **Nano Banana Pro Edit** makes the targeted correction on the whole photo.
2. Claude **composites back only the corrected region** (a hand-drawn mask with an inside-only feather, as in Exp 007 R2) into the **original** photo.
3. **Verified:** zero changed pixels outside the mask. Everything else (smartphone look, light, clutter, body) is exactly the original.

### Correction 1 — mirror selfie face (base: **S1-A**)
- **Why S1-A:** the strongest everyday realism (4/5) in review. Its weakness is identity only. S1-B is kept unchanged as an alternative; Version B regressed toward A there anyway.
- **References:** [S1-A (base), 2002 (face)].
- **Prompt:**
  > Edit the first image, a casual mirror selfie, changing only her face so that she is clearly the same woman as in the second image: the same face shape and proportions, eyes and eye shape, brows, nose, lips, jawline and adult age (around 23–24), and the same small beauty mark on her cheekbone. This is a mirror reflection, so the beauty mark appears on the left side of the picture as we look at it. Keep everything else exactly as it is: the same head angle and downward glance at her phone, the same small relaxed smile, her hair, the phone and the hand holding it, her body, clothes, the hallway, the light and the smartphone photo quality. Keep the face natural and unretouched, with real skin texture and no added makeup. Do not make it more polished or glamorous.
- **Composite mask:** face plus hairline, drawn by Claude. It **excludes the phone and the hand** and is feathered inside only. The mask is shown on the results sheet.

### Correction 2 — café signage (base: **S2-A**)
- **Why S2-A:** strong face match (4/5), and fewer lettered surfaces than S2-B (whose awnings and street signs are also garbled). S2-B is kept unchanged as an alternative.
- **Regions:**
  - the A-frame chalkboard, about x 880–1240, y 1320–1980
  - its reflection in the shop window, about x 1320–1536, y 1260–1700
- **Approach:** short, **specified, ordinary text**, which Nano Banana Pro usually renders legibly. A version where the reflection mostly hides the text is equally believable.
- **References:** [S2-A (base)].
- **Prompt:**
  > Edit this photo, changing only the chalkboard A-frame sign beside her and its reflection in the shop window. Make the sign look like a real café sandwich board with plain, legible, slightly uneven hand-written white chalk lettering that reads exactly: "COFFEE" on the first line, "Iced latte  5.50" on the second line, "Pastries · Open 7–3" on the third line, with a small chalk-drawn coffee cup, some faint smudges and erased chalk marks. In the window reflection, the same sign should appear mirrored, softer and partly obscured by reflections so its words are not readable. Keep everything else exactly as it is: the woman, her face, hair, clothes, iced coffee and pose, the street, people, bicycle, cars, light and smartphone photo quality.
- **Composite mask:** the two sign regions only, inside-feathered. The woman (including her arm and bag strap next to the board) is excluded.

### Variants
**2 per correction** (different seeds), so we can pick the better one. **4 paid edits in total.**

## Evaluation
**Kept separate:**
- **Face:** face crop vs 2002 and vs the uncorrected original. Identity 1–5, beauty-mark position, no styling drift.
- **Realism:** the corrected region must not stand out. Checked at 1:1:
  - mask edge
  - skin texture continuity
  - lighting and colour match
  - legible, plausible lettering with correct spelling and no gibberish anywhere in the frame
  - an overall "would a scroller suspect AI" score of 1–5
- **Preservation:** changed pixels outside the mask must be 0. Body, clothes and background identical to the original.

### Video-gate check (from Exp 009, unchanged)
A corrected image becomes the video input candidate **only if** identity ≥ 4/5 **and** overall realism ≥ 4/5 with **no major artifacts**, judged by Claude and ChatGPT separately. If both corrected images pass, the founder picks one. **Video still needs separate founder approval** (Gemini Omni Flash 1.1 remains the proposed first tool).

## Blind human ratings (in parallel, free)
- The Exp 009 blind set and procedure are unchanged. The original/processed mapping stays sealed.
- The corrected images can be added later as a second blind round, under new codes and a new sealed key, if useful.

## Cost
- 4 × Nano Banana Pro Edit at 2K, 9:16 ($0.15 each) = **$0.60**. Masks, compositing and checks are free.
- **Recommended cap: $0.90.**
- Month-to-date ≈ $5.37 → ≈ $5.97 of $110.
- Price re-checked on fal before running.
- A cheaper option: 1 variant per correction ($0.30).

## Approval needed
1. The two corrections (S1-A face, S2-A signage), 2 variants each, with the prompts above (or ChatGPT's revisions)
2. $0.90 cap (or the $0.30 single-variant option)
