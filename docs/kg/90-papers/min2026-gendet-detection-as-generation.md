---
title: "GenDet: Painting Colored Bounding Boxes on Images via Diffusion Model for Object Detection"
authors: Chen Min, Chengyang Li, Fanjie Kong, Qi Zhu, Dawei Zhao, Liang Xiao
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2601.07273
loop-stage: landscape
tags: object-detection, diffusion, detection-as-generation, generative-discriminative, not-a-data-engine
---

## TL;DR
Reframes **object detection itself** as image generation: conditioned on the input image, a Stable-Diffusion-based model *paints* colored bounding boxes with category labels directly in image space. It is a detector, not a training-data generator.

## Method
A conditional generation architecture on pre-trained Stable Diffusion that formulates detection as **semantic constraints in latent space**, giving precise control over box positions and category attributes while keeping generative flexibility (abstract, arXiv:2601.07273). Input = image; output = boxes painted on it.

## Main claim + result
Claims accuracy "competitive with discriminative detectors" while retaining generative flexibility (abstract; no specific mAP given). Positions itself as bridging generative and discriminative tasks.

## Relevance to us
**Off-target for the generation-side data row** — despite the name it does *image → boxes* (detection / auto-labeling), not *boxes → image* (data synthesis), so it does **not** fill the box/layout data-generation interface we surveyed. Kept as a datapoint that generative and discriminative detection can share one latent space (a weak alignment-thesis echo). For actual box→image engines see [[wang2024-instancediffusion-instance-control]] / [[zhang2023-diffusionengine-data-engine]] / [[chen2023-geodiffusion-geometric-control]].

## Links
- [[generative-augmentation-landscape]]
