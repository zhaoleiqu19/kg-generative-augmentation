# Stage 4 — Close the Loop (STUB)

> Spine stage 4: retrain on the generated data, filter for quality, re-measure, and iterate — closing diagnosis → spec → synthesis → diagnosis.

## What it is
The orchestration: quality/consistency filtering of generations, retraining, evaluation on the diagnosed slice, and deciding whether to iterate — without triggering self-consuming degradation.

## Why it matters
This is where the loop either compounds gains or collapses. Filtering and subgroup monitoring are what separate the safe regime from the harmful one ([[zhang2024-generated-data-amplify-bias]]).

## Key papers
- [[ouyang2025-safefix-model-repair]] — full closed loop with LVLM filtering and retrain; the published template.
- [[zhang2024-generated-data-amplify-bias]] — caution: unfiltered iteration amplifies bias across generations.

## Open questions
- What filter (VLM-based?) keeps gains while preventing the bias/collapse Zhang reports?
- Stopping criterion: when has the loop closed the diagnosed gap "enough"?

## Our take
Stub. SafeFix gives the template; the open work is making the loop robust for detection and proving it on the anchor. Fill in Phase 4.
