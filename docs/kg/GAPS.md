# Candidate Research Gaps

One entry per candidate. Append every batch. Each: gap · evidence (links) · why-not-solved · demonstrable-on-anchor? (y/n/unknown).

## G1 — Diagnosis-driven targeted augmentation for *detection* (not just classification)
- **Gap:** The closed loop "diagnose failures → generate targeted data → filter → retrain" is demonstrated mainly on image **classification**; its transfer to **object detection** (per-object, per-attribute failures) is open.
- **Evidence:** [[chegini2023-clip-diffusion-failure-mitigation]] (diagnose→diffusion-generate, ~21% on hard sub-pops, **classification**), [[ouyang2025-safefix-model-repair]] (classification-centric repair loop), [[generative-augmentation-landscape]] open questions.
- **Why not solved:** The strongest end-to-end diagnose→generate→repair results (Chegini ~21%; SafeFix) are classification + spurious-correlation. Detection failures are localized (box-level, attribute-level), so failure attribution and the success metric (size-specific AP, not accuracy) differ from classification repair — the transfer is unproven.
- **Demonstrable on anchor?** likely y — elevator e-bike detection is a detection task with clear failure modes (occlusion at door, small scale).

## G2 — Detection-granularity, spatially-grounded failure diagnosis for small/occluded objects
- **Gap:** Slice discovery is mature for classification but only *just emerging* for instance-level detection, and not validated for the small/occluded regime. Two specific holes: (a) does grounded instance-level slicing work for *small* objects? (b) can a discovered detection slice be turned into a generation **spec** (stage 2), instead of triggering blanket retrain?
- **Evidence:** [[eyuboglu2022-domino-slice-discovery]] (mature but classification-only), [[zhang2026-gh-esd-instance-slice-discovery]] (instance-level, P@10 0.73 vs 0.63 — newest, untested on small objects), [[chen2025-hibug2-error-slice-discovery]] (multi-task incl. detection; predicts slices beyond val set), [[nikouei2025-small-object-detection-survey]] (small-object challenges), [[stage1-state-of-the-art]] synthesis.
- **Why not solved:** Diagnosis (stage 1) is the least-developed loop link for detection; per-image attribute slicing is too coarse for box-level failures, and the slice→spec handoff (stage 2) is essentially unaddressed.
- **Demonstrable on anchor?** likely y — run GH-ESD/HiBug2-style instance slicing on an elevator detector; measure whether slices map to interpretable hard cases (door occlusion, low light, small scale).

## G3 — Does generation close the *small/occluded* domain gap, and at what ratio/filtering?
- **Gap:** Unclear which diffusion augmentation type + synthetic-to-real ratio + filtering (VLM-based?) actually improves mAP for small/occluded objects vs. hurts via artifacts.
- **Evidence:** [[does-synthetic-data-help]] (helps: Azizi 64.96%→69.24% by fidelity, Ge detection ≈ real; hurts: Zhang bias amplification), [[alimisis2024-diffusion-augmentation-review]] (method menu, metrics), [[yang2023-ai-generated-images-data-source]] (cost/benefit), domain-gap term in [[glossary]].
- **Why not solved:** "Helps" results isolate classification (Azizi) or generic VOC/COCO detection (Ge); none isolate the **small/occluded** detection regime. Helps-vs-hurts is dataset- and ratio-specific and the small-object regime is under-studied.
- **Demonstrable on anchor?** y — directly measurable with the existing Flux pipeline + an elevator dataset (sweep synthetic-to-real ratio, measure size-specific AP).
