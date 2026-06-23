# Knowledge Tree — Map

The whole tree as nested links. Updated every ingestion batch.

- 00 Foundations
  - [[glossary]]
- 10 Landscape (wide sweep)
  - [[generative-augmentation-landscape]]
  - [[does-synthetic-data-help]]
- 20 Loop (spine)
  - stage1 diagnosis — [[stage1-state-of-the-art]] ✅ filled (Phase 1)
  - stage2 spec — [[stage2-state-of-the-art]] ✅ filled (Phase 2)
  - stage3 synthesis — [[stage3-state-of-the-art]] ✅ filled (Phase 3)
  - stage4 close-loop — [[stage4-state-of-the-art]] ✅ filled (Phase 4)
- 30 Anchor task (elevator e-bike detection) — [[task-sota]] (stub)
- 90 Papers
  - [[yang2023-ai-generated-images-data-source]]
  - [[zha2023-data-centric-ai-survey]]
  - [[alimisis2024-diffusion-augmentation-review]]
  - [[nikouei2025-small-object-detection-survey]]
  - [[ouyang2025-safefix-model-repair]]
  - [[azizi2023-synthetic-data-improves-imagenet]]
  - [[ge2023-text2image-for-detection]]
  - [[zhang2024-generated-data-amplify-bias]]
  - [[eyuboglu2022-domino-slice-discovery]]
  - [[zhang2026-gh-esd-instance-slice-discovery]]
  - [[chen2025-hibug2-error-slice-discovery]]
  - [[chegini2023-clip-diffusion-failure-mitigation]]
  - [[huang2024-actgen-active-generation]]
  - [[nguyen2025-tada-targeted-augmentation]]
  - [[chen2023-geodiffusion-geometric-control]]
  - [[zhu2025-recon-region-controllable]]
  - [[zhu2024-odgen-detection-generation]]
  - [[tang2024-aerogen-remote-sensing-generation]]
  - [[zhao2023-xpaste-copy-paste]]
  - [[ruiz2022-dreambooth-subject-driven]]
  - [[gerstgrasser2024-accumulate-avoid-collapse]]
  - [[yi2025-escaping-collapse-verification]]
  - [[kessler2025-active-synthetic-data]]
  - [[liu2024-synthvlm-clipscore-filtering]]

> **Weakest links (confirmed after Phases 1–4):** the upstream/integrative ones, not synthesis.
> - **stage 3 synthesis is NOT the bottleneck** — mature, detection-ready, strong rare-class numbers.
> - **stage 1 diagnosis** at *detection granularity* (per-object, grounded) is only just emerging (GH-ESD, HiBug2), unproven for small/occluded objects (→ G2).
> - **stage 2 spec** — translating a diagnosed detection slice into a layout/region generation spec is essentially unbuilt (→ G4).
> - **stage 4** safeguards exist but are non-detection; no end-to-end *detection* loop is published (→ G1), and the detection *verifier* + safe ratio/stop params are undefined (→ G3).
>
> Net: the contribution surface is the **diagnosis→spec bridge (G2+G4)** and **proving the whole loop end-to-end on the anchor (G1)**, with G3 supplying the measurements.
