---
title: "DiffusionEngine: Diffusion Model is Scalable Data Engine for Object Detection"
authors: Manlin Zhang, Jie Wu, Yuxi Ren, Ming Li, Jie Qin, Xuefeng Xiao, Wei Liu, Rui Wang, Min Zheng, Andy J. Ma
year: 2023
venue: arXiv
url: https://arxiv.org/abs/2309.03893
loop-stage: stage3
tags: object-detection, diffusion, data-engine, detection-adapter, auto-labeling, controllable-generation
---

## TL;DR
A single-stage detection data engine: a frozen pre-trained diffusion model plus a learned Detection-Adapter produce image *and* bounding-box pairs together, no separate generate-then-label pipeline.

## Method
DiffusionEngine (DE) = pre-trained diffusion model + **Detection-Adapter**. The adapter is trained to align the implicit semantic and location knowledge already inside an off-the-shelf diffusion model with **detection-aware signals**, so it predicts bounding boxes for the generated images in a plug-and-play manner (abstract, arXiv:2309.03893). Contributes two scaled benchmarks, **COCO-DE** and **VOC-DE**.

## Main claim + result
Scaling up data via DE (DINO-based adapter) improves **mAP by +3.1% on COCO, +7.6% on VOC, +11.5% on Clipart** (abstract), across detectors and across data-sparse / label-scarce / cross-domain / semi-supervised settings.

## Relevance to us
Belongs to the **generation-engine** row (box/layout): it is a strong, label-free detection data scaler, but it is **not diagnosis-driven** — it scales blanket data, not measured failure slices. The Detection-Adapter (aligning diffusion's latent location knowledge to detection signals) is itself an alignment mechanism worth noting on the generation side. Compare with layout-conditioned engines [[chen2023-geodiffusion-geometric-control]] / [[zhu2024-odgen-detection-generation]].

## Links
- [[stage3-state-of-the-art]]
