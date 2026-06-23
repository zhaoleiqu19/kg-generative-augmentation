# Stage 1 — Diagnosis (STUB)

> Spine stage 1: detect *where and why* a vision model fails, at a granularity that can drive targeted generation. Provisionally the **weakest loop stage** (see MAP).

## What it is
Failure attribution: turning a model's errors into actionable, semantic descriptions of *what kind* of input it fails on (attributes, subpopulations, conditions) — the signal that tells the rest of the loop what to generate.

## Why it matters
Without diagnosis at the right granularity, generation is blanket, not targeted; blanket+iterative generation is the regime that hurts ([[does-synthetic-data-help]]). Diagnosis is the lever that makes the whole loop safe and efficient.

## Key papers
- [[ouyang2025-safefix-model-repair]] — attributes failures to underrepresented semantic subpopulations (class-level; detection-granularity is open).

## Open questions
- How to attribute *detection* failures (box-level, attribute-level), not just per-image class? (→ GAPS G2)
- What automated signals expose the failure attributes (clustering on embeddings, slice discovery, VLM captioning of misses)?

## Our take
Stub. Phase 1 fills this: survey slice-discovery / failure-attribution methods and assess which transfer to small-object detection.
