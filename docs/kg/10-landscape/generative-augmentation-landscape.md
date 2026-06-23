# Generative Augmentation Landscape

## What it is
The wide-sweep map of how generated/synthetic images are used to augment training data for vision models, and the emerging move from *blanket* augmentation toward *diagnosis-driven, targeted* augmentation. This node anchors the Phase 0 landscape and feeds the loop spine in `20-loop/`.

## Why it matters
It frames the project's central bet: that generating data to fix *specific, diagnosed* model weaknesses beats generating data indiscriminately. The landscape splits into (a) what to generate with (diffusion methods), (b) why it works/when it fails (data-centric framing, domain gap), (c) how to target it (failure attribution + repair), and (d) where it must land (small-object detection / the anchor task).

## Key papers
- [[yang2023-ai-generated-images-data-source]] — synthetic data as a source; ~47x cheaper per labeled image; copy-paste / layout-to-image / annotation-free pipelines.
- [[zha2023-data-centric-ai-survey]] — the data-centric AI frame; training-data development as the lever.
- [[alimisis2024-diffusion-augmentation-review]] — taxonomy of diffusion-based augmentation methods + evaluation metrics (stage 3 menu).
- [[nikouei2025-small-object-detection-survey]] — small-object detection challenges (occlusion, class imbalance) + size-specific AP; closest to the anchor.
- [[ouyang2025-safefix-model-repair]] — diagnosis→targeted-generation→VLM-filter→retrain closed loop; the spine's published template.

## Open questions
- Does targeted/diagnosis-driven augmentation (SafeFix-style) generalize from classification to **detection**? Most repair work is classification-centric.
- How to diagnose failures at the granularity of detection (per-object, per-attribute) rather than per-image class?
- Which diffusion augmentation method (semantic edit vs. layout-conditional vs. personalization) best closes the domain gap for small/occluded objects?
- What synthetic-to-real ratio and what filtering (VLM-based?) actually help vs. hurt detection mAP?

## Our take
The field has the pieces — cheap synthetic data, a diffusion method menu, a data-centric rationale, and one closed-loop repair template (SafeFix) — but the closed loop is demonstrated mostly on classification. The unexploited seam is **diagnosis-driven targeted generation for small-object detection**, which is exactly the anchor task. That seam is where GAPS should concentrate.
