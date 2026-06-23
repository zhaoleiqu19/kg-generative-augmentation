# Stage 4 — Close the Loop: State of the Art

> Spine stage 4: filter the generated data, retrain, re-measure on the diagnosed slice, and decide whether to iterate — closing diagnosis → spec → synthesis → diagnosis without self-consuming degradation.

## What it is
The orchestration with three jobs: (1) **filter/verify** generations for quality + semantic consistency; (2) **iterate safely** (manage the real:synthetic mix across rounds); (3) **decide when to stop** (re-diagnose, detect plateau).

## Why it matters
This is where the loop either compounds gains or collapses. The three jobs map onto three well-established results — accumulation, verification, and active re-generation — so stage 4 is about *assembling known safeguards*, not inventing them.

## State of the art

### Iterate safely (avoid model collapse)
- [[gerstgrasser2024-accumulate-avoid-collapse]] — **accumulate** real + all synthetic generations (don't replace) → provable finite error bound; collapse avoided. The core safety rule.
- [[zhang2024-generated-data-amplify-bias]] — caution: unfiltered self-consuming iteration amplifies *subgroup bias*, not just accuracy loss. Monitor fairness, not only mAP.

### Filter / verify (make iteration trustworthy)
- [[yi2025-escaping-collapse-verification]] — an external **verifier** escapes collapse, but "unless the verifier is perfectly reliable, early gains will plateau and may even reverse" → implies a stopping criterion.
- [[liu2024-synthvlm-clipscore-filtering]] — **CLIPScore filter**: 18% curated synthetic beats a full raw baseline ("less is more").
- Inline filters already in the tree: [[ouyang2025-safefix-model-repair]] (LVLM), [[zhao2023-xpaste-copy-paste]] (CLIP), [[tang2024-aerogen-remote-sensing-generation]] (filtering mechanism).

### Close the loop (re-diagnose, select, stop)
- [[kessler2025-active-synthetic-data]] — iterative closed-loop generation **guided by the current student model**, with cheap active-learning selection beating static generation. The control blueprint linking stage 4 back to stages 1–2.
- [[ouyang2025-safefix-model-repair]] — the published end-to-end vision template (attribute → generate → VLM filter → retrain).

## What's solved vs open
- **Solved (in principle, mostly non-detection):** how to iterate safely (accumulate), how to make iteration trustworthy (verify/filter — with numbers), and how to drive the loop by the model's current state (active closed-loop). The safeguards exist.
- **Open:**
  1. Almost all of it is shown on **LM/VLM/VAE**, not detection + diffusion — the safeguards' *parameters* (real:synthetic ratio, verifier choice, stop threshold) are unverified for detection (→ G3).
  2. The **verifier for detection** is undefined — detector self-agreement? a separate VLM judging the box? An unreliable one plateaus/reverses (Yi et al.).
  3. **No end-to-end detection loop** wires diagnosis (stage 1) → spec (stage 2) → synthesis (stage 3) → filtered retrain (here) for the small/occluded regime (→ G1, G4).

## Our take
Stage 4 is an assembly problem, not a research void: **accumulate (don't replace), verify with a good filter, re-diagnose each round, stop on plateau.** The genuine openings are upstream and integrative — defining a reliable *detection* verifier and proving the *whole* loop end-to-end on the anchor (G1/G4), plus pinning the safe ratio/stop parameters for small objects (G3).
