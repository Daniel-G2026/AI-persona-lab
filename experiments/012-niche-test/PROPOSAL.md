# Experiment 012 — Niche Test for AI Content Services

**Status:** Approved by founder 2026-10-27, spend cap $20. Nothing generated yet.
**Branch:** Business test. Separate from the persona work (Exp 001–011, blonde persona).

## Question
Which small-business niche gives the best **replies × price × effort** for AI-made product and listing content?

## Hypothesis
Small product brands will reply most often. Real estate agents will reply less often, but at higher prices. Boutiques sit in the middle, with the hardest accuracy problems (garment fit and fabric).

## Design
| Niche | Prospects | Personalised sample per prospect | Demo clip |
|---|---|---|---|
| A. Small product brands (skincare, candles, jewellery, accessories) | 10 | 2 lifestyle images of *their* product | 1 for the niche (portfolio) |
| B. Real estate agents | 10 | 1 virtual-staging image + 1 styled exterior/interior | 1 photo-to-walkthrough clip |
| C. Clothing boutiques | 10 | 2 styled images of *their* garment (flat-lay / on-model) | 1 for the niche |

- **Pitches:** 30 total, sent over 2 weeks (about 15 a week). One follow-up after 4–5 days, then stop.
- **Samples are private.** Send them only to that business. Never post them publicly without written permission. Prospect input photos stay in `prospects/` (git-ignored) and are never committed.

## Tools (prices verified in earlier experiments; re-check before running)
- **Stills:** fal `fal-ai/nano-banana-pro/edit`, 2K, $0.15/image (verified Exp 008–010, 2026-10-25).
- **Clips:** fal `fal-ai/kling-video/v3/pro/image-to-video`, audio off, $0.112/s, so $0.56 per 5 s (verified Exp 011, 2026-10-26).
- Existing scripts: `scripts/generate_fal.py` (stills) and `scripts/video_gen.py` (clips).

## Budget (estimate)
| Item | Calculation | USD |
|---|---|---|
| Personalised stills | 30 prospects × 2 images × $0.15 | 9.00 |
| Re-rolls (assume 50%) | 30 extra images × $0.15 | 4.50 |
| Demo clips | 3 × $0.56, plus 3 re-rolls | 3.36 |
| **Total estimate** | | **≈ 16.86** |
| **Spend cap** | | **20.00** |

**Monthly budget:** reconciled 2026-10-27. Month-to-date spend is $25.78 of the $110 cap ($84.22 remaining), so the $20 cap fits. See "Budget reconciliation (2026-10-27)" in `EXPERIMENT_LOG.md`.

## Per-sample quality gate (all must pass before sending)
1. **Product fidelity:** logo, label text, colours, shape and proportions match the real product. Zoom to 100%. *This is the #1 deal-killer.*
2. Believable lighting, shadows and reflections; the product sits at a plausible scale.
3. No garbled text, extra fingers or warped objects in the scene.
4. Real estate only: walls, windows, floors and fixed features unchanged; staged furniture fits the room's scale.
5. Boutique only: garment colour, pattern, cut and length match the original.

## Metrics (log in `pitch_tracker.csv` and `samples_review.csv`)
- Reply rate per niche (any reply / pitches sent)
- Positive reply rate (interested or asked for a price)
- Paid conversions, and price accepted
- Sample cost per prospect (including re-rolls)
- Minutes per sample (generation + fixing + sending)
- Pass rate of the first generation on the quality gate

## Decision rule (after 2 weeks or 30 pitches)
Score each niche:
`score = positive_reply_rate × typical_price_quoted ÷ minutes_per_sample`

- **Winner:** the highest score, *provided* it has at least 2 positive replies.
- **No niche reaches 2 positive replies:** review the pitch message and samples before blaming the niche. Run one more round of 10 with a revised message.
- **Any paid job:** deliver it, collect a testimonial and permission to use the work in a portfolio, then offer a monthly retainer.
