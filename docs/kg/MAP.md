# Knowledge Tree — Map

The whole tree as nested links. Updated every ingestion batch.

> **Status:** this MAP is the **global index** of the whole tree and the complete list of `90-papers/` atoms. Sections **00–20** are the **Phase 0–4 record** (kept as history, still-valid analysis; the former `30-anchor-task/` is archived under `_archive/` — the elevator e-bike anchor is no longer the focus). The **current direction** is a two-step plan: **(1)** a literature survey of diagnosis-driven generative augmentation (what's achievable today), **(2)** a pluggable *detect → generate → retrain* augmentation tool. Theory backbone + working notes live in **`50-alignment/`** — start at `50-alignment/README.md`.

- 00 Foundations
  - [[glossary]]
- 10 Landscape (wide sweep)
  - [[generative-augmentation-landscape]]
  - [[does-synthetic-data-help]]
  - [[related-systems-whole-loop]] — prior-art whole-loop neighbors; the seam is open
- 20 Loop (spine)
  - stage1 diagnosis — [[stage1-state-of-the-art]] ✅ filled (Phase 1)
  - stage2 spec — [[stage2-state-of-the-art]] ✅ filled (Phase 2)
  - stage3 synthesis — [[stage3-state-of-the-art]] ✅ filled (Phase 3)
  - stage4 close-loop — [[stage4-state-of-the-art]] ✅ filled (Phase 4)
- 30 Anchor task — *archived* (`_archive/kg/30-anchor-task/`; elevator e-bike anchor dropped)
- 50 Alignment (current direction: diagnosis↔generation alignment) — see `50-alignment/README.md`; new views over the shared `90-papers/` atoms (Phase 0–4 views above are kept as history)
  - applicability table — `50-alignment/generality-map.md` (detection sub-scenarios × where diagnosis-driven aug applies; reads off COCO small-object as the MVP demo row)
  - diagnosis→generation bridge design — `50-alignment/decisions/diagnosis-bridge.md` (TIDE + pycocotools + HiBug2 → per-instance {box, caption}; HiBug2 attribute→caption routing)
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
  - [[zhou2024-3dis-depth-decoupled-instance]]
  - [[tang2024-aerogen-remote-sensing-generation]]
  - [[zhao2023-xpaste-copy-paste]]
  - [[ruiz2022-dreambooth-subject-driven]]
  - [[gerstgrasser2024-accumulate-avoid-collapse]]
  - [[yi2025-escaping-collapse-verification]]
  - [[kessler2025-active-synthetic-data]]
  - [[liu2024-synthvlm-clipscore-filtering]]
  - [[yurt2025-ltda-drive-longtail]]
  - [[petersen2025-scene-aware-location]]
  - [[hong2024-galot-generative-active-learning]]
  - [[girella2024-diag-indistribution-defect]]
  - [[voetman2023-big-data-myth-detection]]

> **Weakest links (confirmed after Phases 1–4):** the upstream/integrative ones, not synthesis.
> - **stage 3 synthesis is NOT the bottleneck** — mature, detection-ready, strong rare-class numbers.
> - **stage 1 diagnosis** at *detection granularity* (per-object, grounded) is only just emerging (GH-ESD, HiBug2), unproven for small/occluded objects (→ G2).
> - **stage 2 spec** — translating a diagnosed detection slice into a layout/region generation spec is essentially unbuilt (→ G4).
> - **stage 4** safeguards exist but are non-detection; no end-to-end *detection* loop is published (→ G1), and the detection *verifier* + safe ratio/stop params are undefined (→ G3).
>
> Net: the contribution surface is the **diagnosis→spec bridge (G2+G4)** and **proving the whole loop end-to-end on a detection task (G1)**, with G3 supplying the measurements.
>
> *(This conclusion evolved into the **alignment thesis** — see `50-alignment/alignment-thesis.md`.)*
