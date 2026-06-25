---
title: "OcclusionFormer: Arranging Z-Order for Layout-Grounded Image Generation"
authors: Ziye Li, Henghui Ding
year: 2026
venue: arXiv (ICML 2026)
url: https://arxiv.org/abs/2605.21343
loop-stage: stage3
tags: diffusion, layout-to-image, occlusion, z-order, bounding-box, controllable-generation, diffusion-transformer
---

## TL;DR
A layout-to-image model that explicitly handles **inter-object occlusion**: it models Z-order (who is in front) so overlapping boxes render with correct layering instead of entangled textures.

## Method
Three parts (abstract, arXiv:2605.21343): (1) **SA-Z dataset** with explicit occlusion ordering + pixel-level annotations; (2) the **OcclusionFormer** Diffusion Transformer that "models Z-order priority by decoupling instances and compositing them via volume rendering" (layer-wise separation then recombination); (3) a **Queried Alignment Loss** supervising each instance for fine-grained spatial precision and semantic consistency.

## Main claim + result
Targets the failure of prior L2I methods in overlap regions (ambiguous textures, wrong layering). Reports "substantial accuracy gains across diverse scenes" via correct occlusion dependencies; specific metrics to be pulled from the paper body. ICML 2026.

## Relevance to us
**Directly addresses the anchor's hardest case**: elevator e-bikes are routinely occluded by doors, walls, and people, and most box-conditioned engines (GeoDiffusion / InstanceDiffusion / MIGC++) lack explicit occlusion ordering. The Z-order interface adds a representation dimension a detection diagnosis could supply ("e-bike behind person"). Strongest candidate for the **occlusion** sub-axis of the box/layout row. Pair with [[wang2024-instancediffusion-instance-control]] (per-instance control) / [[zhu2024-odgen-detection-generation]] (object-wise occlusion via fine-tuning).

## Links
- [[stage3-state-of-the-art]]
