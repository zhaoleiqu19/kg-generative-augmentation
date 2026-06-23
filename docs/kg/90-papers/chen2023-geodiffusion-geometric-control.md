---
title: "GeoDiffusion: Text-Prompted Geometric Control for Object Detection Data Generation"
authors: Kai Chen, Enze Xie, Zhe Chen, Yibo Wang, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung
year: 2023
venue: arXiv (ICLR 2024)
url: https://arxiv.org/abs/2306.04607
loop-stage: stage3
tags: layout-to-image, geometric-control, object-detection, controllable-generation, spec-format
---

## TL;DR
GeoDiffusion turns geometric conditions (bounding boxes, even camera views) into text prompts, so a pre-trained diffusion model generates detection data that obeys a specified layout.

## Method
"Flexibly translate[s] various geometric conditions into text prompts" (abstract, arXiv:2306.04607), encoding not just bounding boxes but extra geometry such as camera views in self-driving scenes, then conditions a pre-trained T2I diffusion model. Layout-to-image (L2I) generation with annotations coming for free from the input layout.

## Main claim + result
First to validate that diffusion-based L2I generated images improve object detector performance; "outperforms previous L2I methods while maintaining 4x faster training" (abstract). Abstract omits the exact FID/mAP deltas (reported elsewhere as large gains vs LostGAN/ControlNet) — pull exact numbers from the paper tables in a follow-up.

## Relevance to us
Defines the **spec format** the synthesis side can consume: a *layout/geometry* spec → annotated detection image. This is the executable target of our slice→spec handoff — a diagnosed detection failure ("e-bike small, bottom-left, occluded") can in principle be written as a GeoDiffusion-style layout condition. Belongs to stage 3 mechanism but anchors stage 2's spec language.

## Links
- [[stage2-state-of-the-art]]
