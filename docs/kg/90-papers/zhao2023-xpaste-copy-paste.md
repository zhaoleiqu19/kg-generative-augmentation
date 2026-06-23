---
title: "X-Paste: Revisiting Scalable Copy-Paste for Instance Segmentation using CLIP and StableDiffusion"
authors: Hanqing Zhao, Dianmo Sheng, Jianmin Bao, Dongdong Chen, Dong Chen, Fang Wen, Lu Yuan, Ce Liu, Wenbo Zhou, Qi Chu, Weiming Zhang, Nenghai Yu
year: 2023
venue: arXiv (ICML 2023)
url: https://arxiv.org/abs/2212.03863
loop-stage: stage3
tags: copy-paste, instance-segmentation, long-tail, stable-diffusion, clip-filtering, composition
---

## TL;DR
X-Paste scales copy-paste augmentation by sourcing foreground objects from Stable Diffusion (and web crawl) and filtering them with CLIP, then compositing — strong gains on long-tail classes.

## Method
A data acquisition + processing framework: generate objects with a text-to-image model (or crawl the web), filter the noisy set with a zero-shot CLIP recognizer, then composite onto backgrounds with masks (abstract, arXiv:2212.03863). Four modules: acquisition, mask generation, filtering, composition.

## Main claim + result
On LVIS instance segmentation: **+2.6 box AP / +2.1 mask AP** overall, and **+6.8 box AP / +6.5 mask AP on long-tail / rare categories** (abstract). Scales without manual annotation or 3D rendering.

## Relevance to us
The canonical **composition (copy-paste)** route — an alternative to layout-conditional generation, with automatic masks and an explicit **CLIP filter** (again a stage-4 idea inline). Rare-class gains echo AeroGen. For the anchor, generate isolated e-bike instances (DreamBooth-personalized) → CLIP-filter → paste into elevator backgrounds is a concrete, low-risk pipeline. Cf. [[ge2023-text2image-for-detection]] (same family).

## Links
- [[stage3-state-of-the-art]]
