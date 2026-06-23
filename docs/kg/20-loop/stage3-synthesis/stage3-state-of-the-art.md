# Stage 3 — Synthesis (STUB)

> Spine stage 3: actually generate the spec'd images (and annotations). The most mature stage — a rich method menu already exists.

## What it is
The generation toolbox: diffusion-based semantic editing, layout/geometry-conditional generation, personalization, and copy-paste composition that yields images plus boxes/masks.

## Why it matters
This is where the elevator/e-bike images get made. Method choice controls fidelity and domain-gap closure — and fidelity is a proven lever for "helps" ([[azizi2023-synthetic-data-improves-imagenet]]).

## Key papers
- [[alimisis2024-diffusion-augmentation-review]] — taxonomy of diffusion augmentation methods + evaluation metrics.
- [[ge2023-text2image-for-detection]] — compositional foreground+background+cut-paste for detection with auto annotations.
- [[azizi2023-synthetic-data-improves-imagenet]] — fidelity/resolution raises downstream accuracy.
- [[yang2023-ai-generated-images-data-source]] — copy-paste / layout-to-image / annotation-free families.

## Open questions
- Which method best closes the **small/occluded** domain gap? (→ GAPS G3)
- How to guarantee annotation quality (tight boxes) for small objects?

## Our take
Stub but well-stocked. Phase 3 narrows the menu to the methods viable for small-object elevator detection with the existing Flux pipeline.
