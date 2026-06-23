# Candidate Research Gaps

One entry per candidate. Append every batch. Each: gap · evidence (links) · why-not-solved · demonstrable-on-anchor? (y/n/unknown).

## G1 — Diagnosis-driven targeted augmentation for *detection* (not just classification)
- **Gap:** The closed loop "diagnose failures → generate targeted data → filter → retrain" is demonstrated mainly on image **classification**; its transfer to **object detection** (per-object, per-attribute failures) is open.
- **Evidence:** [[ouyang2025-safefix-model-repair]] (classification-centric repair loop), [[generative-augmentation-landscape]] open questions.
- **Why not solved:** Detection failures are localized (box-level, attribute-level), so failure attribution and the success metric (size-specific AP, not accuracy) differ from classification repair.
- **Demonstrable on anchor?** likely y — elevator e-bike detection is a detection task with clear failure modes (occlusion at door, small scale).

## G2 — Detection-granularity failure diagnosis as the bottleneck
- **Gap:** No standard way to attribute detection failures to specific semantic attributes (viewpoint, occlusion-by-door, lighting) to *drive* what to generate.
- **Evidence:** [[nikouei2025-small-object-detection-survey]] (challenges: occlusion, class imbalance), [[ouyang2025-safefix-model-repair]] (attribution exists but at class level), MAP weakest-stage note.
- **Why not solved:** Diagnosis (stage 1) is the least-developed loop link; most work jumps straight to synthesis (stage 3).
- **Demonstrable on anchor?** unknown — needs an anchor dataset with attribute labels or a way to mine them.

## G3 — Does generation close the *small/occluded* domain gap, and at what ratio/filtering?
- **Gap:** Unclear which diffusion augmentation type + synthetic-to-real ratio + filtering (VLM-based?) actually improves mAP for small/occluded objects vs. hurts via artifacts.
- **Evidence:** [[does-synthetic-data-help]] (helps: Azizi 64.96%→69.24% by fidelity, Ge detection ≈ real; hurts: Zhang bias amplification), [[alimisis2024-diffusion-augmentation-review]] (method menu, metrics), [[yang2023-ai-generated-images-data-source]] (cost/benefit), domain-gap term in [[glossary]].
- **Why not solved:** "Helps" results isolate classification (Azizi) or generic VOC/COCO detection (Ge); none isolate the **small/occluded** detection regime. Helps-vs-hurts is dataset- and ratio-specific and the small-object regime is under-studied.
- **Demonstrable on anchor?** y — directly measurable with the existing Flux pipeline + an elevator dataset (sweep synthetic-to-real ratio, measure size-specific AP).
