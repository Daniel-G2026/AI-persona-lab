# Experiment 011 — Pipeline Benchmark + First Motion Test (Proposal)

> **HISTORICAL PROPOSAL / PARTIALLY COMPLETED.** This document is the original proposal, not the live production plan. **Part A completed** 2026-10-26: two café image-to-video outputs, $1.06, results in `EXPERIMENT_LOG.md` and `partA/`. **Part B's sixteen-image design was replaced by a four-image pilot** (`PILOT_B_PROPOSAL.md`), and the pilot is now **on hold** after the 2026-10-27 shift to **Higgsfield Genjutsu Motion Transfer** with a separate blonde working persona. No re-run, purchase, or training is authorized by this old proposal. See `../../PRODUCTION_PLAYBOOK.md`.


**Status:** Proposed by Claude 2026-10-26. **Awaiting founder approval. Nothing generated, nothing spent.** Context: `STRATEGY_REVIEW.md`.

Fixed and unchanged throughout: 2002 face, 1001 baseline, Version A and Version B body references (neither canonical), all Exp 009/010 images and the sealed blind set.

---

## Part A — Immediate 5-second motion test (technical, not final content)
**Input:** `experiments/010-correction/candidates/S2-A-signfix.png` (café, signage corrected; `6ff697ec…`).
**Purpose:** learn how believable the motion is, and whether her identity holds through movement. Not content approval.

| Clip | Tool (fal) | Settings | Why | Cost |
|---|---|---|---|---|
| **A1** | Gemini Omni Flash 1.1 image-to-video `google/gemini-omni-flash/v1.1/image-to-video` | start frame = S2-A signfix, 9:16, **720p**, 5 s (nearest allowed) | Cheapest baseline; plain start-frame animation | 5 × $0.10 = **$0.50** |
| **A2** | Kling v3 Pro image-to-video `fal-ai/kling-video/v3/pro/image-to-video` | start frame = S2-A signfix, 5 s, audio off; **`elements`: @Element1 = frontal 2002 + reference_image_urls [S2-A face crop, Version A front body ref]** | Tests whether explicit identity binding reduces face drift during motion | ≈ 5 × $0.112 = **≈ $0.56** |

- **The same motion prompt for both:**
  > A short, real smartphone video continuing this exact photo. She stays standing in the same spot outside the café; her small smile becomes a natural relaxed smile, she glances briefly down the street and back to the camera, and lifts the iced coffee slightly as if about to take a sip. Gentle natural handheld camera movement, no cuts, no zoom, no change of angle. Keep her face, hair, body and clothes exactly as in the photo; realistic hair and fabric movement, natural blinking; passers-by and cars move naturally in the background; consistent overcast daylight.
  - Kling's prompt adds "@Element1 is the woman."
- **No 360p draft:** the clips are short and cheap, and the draft would add a decision stop without much saving.
- **Evaluation**, kept separate from stills:
  - frame grabs at 0 / 1.25 / 2.5 / 3.75 / 5 s → face crops vs 2002 (identity 1–5 per frame, min and mean)
  - body and clothing stability
  - motion naturalness (blink, smile, weight, hair, fabric, the cup)
  - camera behaviour (believable handheld, no warping)
  - background (people and cars move plausibly, no "boiling", the sign stays legible and doesn't morph)
  - overall "would pass as a real phone video" 1–5
  - Claude, ChatGPT and blind humans scored separately
- Audio is off for Kling; Omni's audio track is stripped if present.

---

## Part B — Still-image benchmark: two strongest workflows
**Question:** which workflow gives the most **usable, identity-consistent, believable** photos per dollar and per minute of manual work, across **different scenes**?

| Workflow | Description |
|---|---|
| **W1: Nano reference-driven** (current) | Nano Banana Pro Edit; refs [2002, body front, body 3q]; the casual smartphone prompt style from Exp 009, with an added "no readable text except simple real words; avoid signage" rule |
| **W2: Real background + Nano** | Nano Banana Pro Edit; refs [**real background photo**, 2002, body front, body 3q]; prompt: place her naturally into *this exact photo*, matching its light, perspective, camera and grain. The real photo supplies the environment, so there is no invented signage or clutter |

### Design
- **4 scenes × 2 workflows × 2 images = 16 images.** In each scene/workflow cell, one image uses Version A references and one uses Version B. Body is recorded, not optimized.
- **Scenes** (everyday Instagram situations, varied light and angle):
  1. **Kitchen**, morning window light: making coffee, side/three-quarter view
  2. **Park path** or tree-lined street, afternoon: walking toward the camera, friend-shot
  3. **Car passenger seat**, daylight: casual selfie, upper body
  4. **Restaurant or bar table**, warm evening light: seated, friend-shot across the table
- **W2 backgrounds:** 4 photos, **ideally shot by the founder on their phone**:
  - matching the scenes, empty of people, no readable brand logos
  - free, rights-clean, and genuinely phone-camera
  - Alternative: licensed stock (e.g. Unsplash licence) chosen by the founder. Claude won't download images without approval.
  - Each background is hash-recorded and kept unchanged.
- **Same evaluation for both workflows:**
  - **Face consistency** (face crop vs 2002, 1–5)
  - **Body:** reads as the intended A/B? Regression yes/no
  - **Photographic realism:** the Exp 009 sub-scores plus the blind "would a scroller suspect AI" 1–5
  - **Major artifacts** yes/no (text, hands, perspective or lighting mismatch, pasted look)
  - **Usable** = identity ≥ 4 AND realism ≥ 4 AND no major artifacts, **with no manual correction**. A second "usable after ≤ 5 minutes of correction" count is tracked separately.
  - **Manual time** logged per image (review + any fix).
  - **Cost per usable image** = spend ÷ usable count, per workflow.
  - **Repeatability** = usable rate across the 4 scenes; we look for consistency, not one lucky hit.
- **Blind human round:** the 16 images under random codes with a sealed key, using the Exp 009 procedure.
- **Decision rule:**
  - the workflow with the higher usable rate becomes the default (ties go to the lower manual time)
  - **if neither reaches ≥ 50% usable**, the next step is a LoRA built from the approved images, or Runway Gen-4 References as a challenger
  - **if the winner reaches ≥ 50%**, its approved outputs (plus Exp 009/010 approvals) form the seed dataset for an eventual LoRA

### Prompts
Prompts are drafted per scene in `prompts/` at setup, after approval. They reuse Exp 009's smartphone-believability language verbatim, so the only experimental variable is the workflow, not prompt quality.

---

## Costs (estimates; prices re-checked on fal before running)
| Part | Calc | Cost |
|---|---|---|
| A1 Omni Flash 720p 5 s | 5 × $0.10 | $0.50 |
| A2 Kling v3 Pro + Elements 5 s, audio off | 5 × ≈ $0.112 | ≈ $0.56 |
| B 16 stills, Nano Banana Pro 2K | 16 × $0.15 | $2.40 |
| **Total** | | **≈ $3.46** |

- **Recommended caps:** Part A $1.25; Part B $3.00.
- Month-to-date ≈ $5.67 → ≈ $9.13 of $110.

## Execution order and stops
1. **Part A** (can start immediately on approval) → stop for review of motion realism.
2. **Part B** needs the founder's 4 background photos for W2. Then generate all 16 → blind set → stop for review and the workflow decision.
3. Nothing beyond this without approval: no LoRA training, no Runway account, no further correction passes.

## Approval needed
1. Part A: both clips (A1 Omni, A2 Kling + Elements), or A1 only
2. Part B: the 16-image benchmark design, and who supplies the 4 backgrounds (founder's phone photos recommended)
3. Caps
