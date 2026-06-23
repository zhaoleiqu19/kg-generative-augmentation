---
title: "ODGEN: Domain-specific Object Detection Data Generation with Diffusion Models"
authors: Jingyuan Zhu, Shiyu Li, Yuxuan Liu, Ping Huang, Jiulong Shan, Huimin Ma, Jian Yuan
year: 2024
venue: arXiv (NeurIPS 2024)
url: https://arxiv.org/abs/2405.15199
loop-stage: stage3
tags: object-detection, diffusion, domain-specific, object-wise-conditioning, occlusion, controllable-generation
---

## TL;DR
ODGEN fine-tunes a diffusion model on domain data and conditions generation object-wise (visual foreground patches + per-object text), producing multi-class, occluded detection scenes that boost detectors.

## Method
Dual conditioning: "synthesized visual prompts with spatial constraints and object-wise textual descriptions" (abstract, arXiv:2405.15199). Fine-tunes on both cropped foreground objects and entire images from the domain. The object-wise strategy is what lets it render multi-class scenes *with occlusions* — a known failure of prior layout-to-image methods.

## Main claim + result
Up to **+25.3% mAP@.50:.95** training YOLOv5/v7 on domain-specific data with ODGEN-generated images; **+5.6% mAP@.50:.95** over prior methods on COCO-2014 (abstract). NeurIPS 2024.

## Relevance to us
The strongest detection-generation result in the tree and the best fit for the anchor: it explicitly targets **domain-specific, occluded, multi-class** scenes (= elevator interiors with partly-hidden e-bikes). Object-wise conditioning is a candidate execution engine for a G4 slice→spec pipeline. Compare against [[chen2023-geodiffusion-geometric-control]] (box-only) and [[zhu2025-recon-region-controllable]] (region rectification).

## Links
- [[stage3-state-of-the-art]]
