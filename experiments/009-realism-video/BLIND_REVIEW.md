# Experiment 009 — Blind Human Review Procedure

Purpose: find out whether ordinary people perceive the stills as real smartphone photos, **independently** of
Claude's and ChatGPT's assessments. Human ratings live only in `human_ratings.csv`; Claude's are in
`claude_assessment.csv`, and ChatGPT's should go in `chatgpt_assessment.csv`. They are never merged before analysis.

## What reviewers see
- 8 images named by random codes (e.g. `K7.png`), all 1080×1920 PNG: the 4 stills × {original, phone-processed}.
  Nothing in the file name, size or format reveals which is which.
- Share the folder `blind_for_reviewers/` (OneDrive: `AI-persona-lab-originals/experiments/009-realism-video/blind_for_reviewers/`),
  or the overview `blind_sheet.jpg` if necessary (the sheet is JPEG-compressed, so prefer the individual PNGs).
- **The key (`blind_key.json`) is not in the repo.** Only its fingerprint (`blind_key.sha256`) is, so nobody, including
  ChatGPT reading the repo, can peek, and the key can be shown to be unchanged when it is opened.

## Who
- 3–5 reviewers, ideally people who regularly use Instagram and **haven't seen this project's images before**.
- Tell them honestly: "Some or all of these images may be AI-generated. Rate each on first impression." Do not say
  how many, or which ones.

## How (about 5 minutes per reviewer)
1. Reviewer opens each image **full-screen on their own phone**, in the code order given (already random).
2. Look at it for about 5 seconds, as if scrolling, then answer:
   - **Q1 Real or AI?** 1 = definitely AI · 2 = probably AI · 3 = can't tell · 4 = probably real · 5 = definitely real
   - **Q2 Giveaway:** what, if anything, made it look AI or fake? (free text, or "nothing")
   - **Q3 Scroll test:** would you scroll past this on Instagram without noticing anything odd? yes / no
3. No going back to change answers; no comparing images side by side. Reviewers don't discuss with each other until all are done.

## Recording
Fill one row per reviewer per image in `human_ratings.csv`:
`reviewer_id, code, q1_real_1to5, q2_giveaway, q3_scroll_pass_yes_no, device, date`
Use anonymous IDs (R1, R2 …); no names.

## Analysis (after all ratings are in)
Claude opens the key, checks its SHA-256 against `blind_key.sha256`, and reports per still and per variant:
mean Q1, the % of "scroll pass", and the common giveaways. Original vs phone pass is compared directly; **the phone pass
is not assumed to help**. Human results are reported separately from Claude and ChatGPT.
