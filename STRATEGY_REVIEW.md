# AI Persona Lab — Production Pipeline Review

> **HISTORICAL SNAPSHOT — 2026-10-26.** The review below accurately describes the research-stage strategy at the time. **It is not the current production workflow.** On 2026-10-27 the founder adopted a separate **blonde Higgsfield influencer** as a working production persona, tested real-video Motion Transfer with a new Milan environment, and began creating **fal Nano Banana Pro profile stills**. See [PRODUCTION_PLAYBOOK.md](PRODUCTION_PLAYBOOK.md) and [PRODUCTION_ASSET_REGISTER.md](PRODUCTION_ASSET_REGISTER.md). Experiment 011 Part A was subsequently completed for the *earlier brown-haired* branch (Omni vs Kling; $1.06). Its Part B real-background pilot is **on hold** in the newer platform-led workflow, not silently canceled or run.


**Date:** 2026-10-26 · **Author:** Claude · **Status:** For founder + ChatGPT review. Nothing generated or spent for this review.

## 1. Where we are (honest summary)
- **Spent:** about $5.67 across 10 experiments.
- **Proven:**
  - Nano Banana Pro transfers the **2002 face** into new scenes reliably when the face is reasonably visible (Exp 003, 008, 009, 010).
  - Casual smartphone prompting produces stills that read as **ordinary phone photos at feed scale** (Exp 009).
  - Localized edit + composite fixes a specific flaw with **0 px changed elsewhere** (Exp 010).
- **Not proven:**
  - **Repeatability** across many scenes. Each "good" image so far was selected or corrected by hand.
  - **Video** (none generated).
  - **Body Version B** carrying over into new scenes (regressed in Exp 008 and 009).
- **Lesson:** fixing single images works but doesn't scale. The next step must measure **usable-output rate and cost per usable post** across many scenes, not perfect one picture.

## 2. Options compared
Legend: **D** = documented capability (official docs or provider page) · **T** = tested by us · **C** = third-party or marketing claim, untested by us.

| | 1. Nano Banana Pro reference + local edit (current) | 2. Runway Gen-4 References | 3. Kling Elements (video) | 4. Trained character LoRA | 5. Real photo backgrounds + character generation |
|---|---|---|---|---|---|
| **What it is** | Prompt + reference images (face, body); targeted edits composited back | Image model with up to ~3 tagged reference images (`@tag` in prompt) | Reusable "Element" (frontal + 1–3 angle images, or a 3–8 s clip) bound into video generation | Fine-tune a model on 20–40 curated images of the character | Insert or generate the character into **real** photographs (our own phone photos or licensed stock) |
| **Access** | fal (have key) **D** | Runway Dev API, **new account, $10 minimum top-up** **D** | fal `fal-ai/kling-video/v3/pro/image-to-video` with `elements` (frontal + 1–3 refs; `@Element1` in prompt) **D**; also Kling's own API | fal trainers, e.g. Z-Image trainer **D** | fal (Nano Banana Pro edit with a background image as a reference) **D** |
| **Price** | $0.15/image at 2K **D/T** | gen4_image $0.05 (720p) / $0.08 (1080p); turbo $0.02 **D** | Kling v3 Pro ≈ $0.112/s with audio off on fal, about $0.56 per 5 s (fal guide; re-check) **D** | Z-Image trainer $2.26 per 1,000 steps, about $4.50 for 2,000 steps **D**; inference cheap (Z-Image class) | Same as option 1 ($0.15/image) plus free real photos |
| **Character consistency** | Face: good when visible (**T**, identity 4/5 typical). Body B: regresses (**T**) | Claimed strong for references (**C**); untested on our face | Purpose-built for identity across clips (**D**: design; **C**: quality) | Usually the strongest repeatability once trained (**C**); depends entirely on dataset quality | Same face behaviour as option 1 (**T** for the face) |
| **Photographic realism** | Feed-scale believable in casual prompts (**T**); AI tells: garbled text, slight polish | Unknown for our use (**C**) | Video only | Depends on the base model (Z-Image realism moderate in Exp 001, **T**) | **Background is real by construction**: removes gibberish text and "staged set" tells. Risks: lighting/perspective mismatch, pasted look (untested) |
| **Motion realism** | n/a (stills) | Gen-4.5 video $0.12/s **D**; untested | Kling motion widely rated well (**C**); untested | n/a | n/a |
| **Repeatability across scenes** | Unmeasured; per-image variance high (**T**) | Unmeasured | Unmeasured | Potentially high (**C**) | Unmeasured; bounded by how many real backgrounds we have |
| **Manual correction time** | Medium: review plus occasional local fixes (Exp 010 took an afternoon of engineering, now scripted) | Unknown | Low per clip if identity holds | High up front (curate dataset), low per image after | Medium: need suitable photos; possibly 0 text fixes |
| **Scalability** | Good: API, about $0.15/try | Good: API, cheap | Good: API | Best per-image cost once trained; retraining per look or body version | Good if a background library exists |
| **Key risk** | Text artifacts, polish drift, body regression | New vendor; unproven on our face | Video cost; identity drift through motion | **Chicken-and-egg:** needs 20–40 consistent images we don't yet have | Lighting integration; needs rights-clean photos |

### Assessment
- **Option 1** is our working baseline. Keep it, but measure it properly.
- **Option 5** targets the exact failures we observed: AI-looking environments and gibberish signage. It needs no new vendor and costs the same per image. **It is the strongest challenger for stills.**
- **Option 2** is plausible, but needs a new vendor and is architecturally similar to option 1 (reference-driven generation). Lower priority until option 1 or 5 shows a ceiling.
- **Option 4 is premature now and likely right later.** A LoRA needs 20–40 consistent, approved images in varied scenes and angles. The benchmark below produces exactly that pool. Revisit when we have about 25 approved images.
- **Option 3** is the most relevant **video** option: it binds identity explicitly, using frontal + angle images such as 2002 and the A/B body references. Gemini Omni Flash 1.1 (start-frame image-to-video, $0.03–0.10/s on fal) is the cheap baseline.

## 3. Recommended production system (target)
1. **Character pack** (fixed, versioned): 2002 face, 1001 baseline, Version A and Version B body references (none canonical). Later, a LoRA trained on approved outputs.
2. **Stills:** whichever of **(1) Nano reference-driven** and **(5) real background + Nano** wins the benchmark on **usable rate × cost × correction time**. Local-edit compositing stays a *repair tool*, not the default workflow.
3. **Video:** image-to-video from approved stills. **Omni Flash** (cheap drafts) vs **Kling v3 Elements** (identity-bound), chosen by the motion test.
4. **QA gate per asset:** identity ≥ 4, realism ≥ 4 (blind "would a scroller suspect AI"), no major artifacts, AI label on publish.
5. **Metrics tracked per batch:** usable rate, cost per usable image or clip, minutes of manual work per usable asset.

Rough steady-state budget (**estimate, to be replaced by benchmark data**):
- If ~50% of stills are usable at $0.15 each → about **$0.30 per usable photo**.
- If ~30–50% of 5 s clips are usable at $0.50–0.60 each → about **$1–2 per usable clip**.
- 20 photos + 8 Reels per month ≈ **$6 + $16 ≈ $22/month**, within the $110 cap.

## 4. Next step
See `experiments/011-pipeline-benchmark/PROPOSAL.md`:
- **(A)** an immediate 5 s motion test on the corrected S2-A café photo
- **(B)** a controlled 16-image still benchmark: Nano reference-driven vs real background + Nano

## Sources
- Runway API pricing (official): https://docs.dev.runwayml.com/guides/pricing/ · Runway Gen-4 Images API news: https://runway.com/news/introducing-runway-api-for-gen-4-images · Runway pricing: https://runway.com/pricing
- Runway gen4_image `referenceImages` / `@tag` usage (SDK pattern, third-party skill page): https://mcpservers.org/zh-CN/agent-skills/runwayml/rw-integrate-image · reference count (third-party): https://www.cometapi.com/es/runway-gen4-image-api/
- fal Kling v3 Pro image-to-video API (elements schema): https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api · fal Kling 3 page: https://fal.ai/kling-3 · fal Kling O1 guide: https://fal.ai/learn/devs/kling-o1-developer-guide
- Kling Element Library user guide (official): https://kling.ai/quickstart/klingai-element-library-3-user-guide · Kling character consistency guide: https://kling.ai/quickstart/ai-video-character-consistency
- Kling API pricing (third-party): https://costbench.com/software/ai-media-apis/kling-api/ · https://www.cloudzero.com/blog/kling-ai-pricing/ · https://www.atlascloud.ai/blog/tips/kling-3.0-review-features-pricing-ai-alternatives
- fal Z-Image trainer: https://fal.ai/models/fal-ai/z-image-trainer · fal FLUX Kontext trainer: https://fal.ai/models/fal-ai/flux-kontext-trainer · fal Krea 2 trainer: https://fal.ai/models/fal-ai/krea-2-trainer
- fal Gemini Omni Flash 1.1 image-to-video: https://fal.ai/models/google/gemini-omni-flash/v1.1/image-to-video · fal image-to-video API guide: https://fal.ai/learn/tools/best-image-to-video-apis-2026
