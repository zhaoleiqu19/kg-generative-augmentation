# Stage 1 — Diagnosis: State of the Art

> Spine stage 1: detect *where and why* a vision model fails, at a granularity that can drive targeted generation. Provisionally the **weakest loop stage** for our regime (see MAP).

## What it is
**Error slice discovery / failure attribution**: turning a model's mistakes into coherent, named subgroups ("slices") described in human terms — the signal that tells stage 2/3 *what* to generate. The field splits into two paradigms:
- **slice-then-tag** — cluster failures in an embedding space, then describe (Domino, Spotlight, FACTS).
- **tag-then-slice** — first generate task attributes/tags (via humans or VLM/LLM), then group data into slices (HiBug2, GH-ESD, LADDER).

## Why it matters
Without diagnosis at the right granularity, generation is blanket — and blanket/iterative generation is the regime that *hurts* ([[does-synthetic-data-help]], [[zhang2024-generated-data-amplify-bias]]). Diagnosis is the lever that makes the whole loop targeted, safe, and efficient.

## State of the art

### Foundational (classification)
- [[eyuboglu2022-domino-slice-discovery]] — defines slice discovery; embed→slice→describe with NL names. 36% of 1,235 slices found (+12pts); per-image classification only.

### Diagnosis → generation bridge
- [[chegini2023-clip-diffusion-failure-mitigation]] — auto-describe failures (LLM/VLM) → diffusion-generate targeted fixes; **~21% accuracy gain on hard sub-populations** across 40 models. Classification / background spurious correlations.
- [[ouyang2025-safefix-model-repair]] — full closed loop: attribute failures → conditional T2I generation → VLM filter → retrain. Class-level.

### Toward detection granularity (the gap)
- [[zhang2026-gh-esd-instance-slice-discovery]] — **instance-level** slice discovery for detection/segmentation; grounded/relational slices; Precision@10 0.73 vs 0.63. Closest to G2.
- [[chen2025-hibug2-error-slice-discovery]] — tag-then-slice across classification/pose/**detection**; predicts error slices *beyond* the validation set.

## What's solved vs open
- **Solved:** for *classification*, automatic slice discovery + NL description is mature, and the diagnosis→generation bridge is demonstrated (Chegini ~21%).
- **Open (our wedge):**
  1. Detection-granularity diagnosis (per-object, spatially-grounded) is just emerging (GH-ESD, HiBug2) and unproven for **small/occluded** objects. (→ G2)
  2. Turning a discovered detection slice into a generation *spec* (stage 2) is largely unaddressed — most work goes slice → blanket retrain, not slice → controlled synthesis.
  3. Diagnosis on *deployment* footage with no labeled held-out set (elevator CCTV) — HiBug2's "beyond validation set" idea is the only lead.

## Our take
The diagnosis machinery exists but is classification-shaped. Pushing grounded, instance-level slice discovery onto small-object elevator detection — and wiring its output into a controlled generation spec — is the concrete, under-served opening that GAPS G1/G2 target.
