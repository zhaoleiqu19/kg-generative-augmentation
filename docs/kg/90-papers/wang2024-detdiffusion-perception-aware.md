---
title: "DetDiffusion: Synergizing Generative and Perceptive Models for Enhanced Data Generation and Perception"
authors: Yibo Wang, Ruiyuan Gao, Kai Chen, Kaiqiang Zhou, Yingjie Cai, Lanqing Hong, Zhenguo Li, Lihui Jiang, Dit-Yan Yeung, Qiang Xu, Kai Zhang
year: 2024
venue: arXiv (CVPR 2024)
url: https://arxiv.org/abs/2403.13304
loop-stage: stage3
tags: object-detection, diffusion, perception-aware, layout-guided, controllable-generation, generation-diagnosis-alignment
---

## TL;DR
First framework to harmonize a generative and a perceptive model in one loop: the detection/segmentation model's signal is fed back into diffusion generation, so the generated data is tailored to the downstream detector.

## Method
Two perception-to-generation couplings (abstract, arXiv:2403.13304): (1) a **perception-aware loss (P.A. loss) through segmentation** that uses a segmentation head to improve generation quality and controllability; (2) **perception-aware attributes (P.A. Attr)** extracted from the perceptive model and used to customize data augmentation during generation. The generator is layout-guided (category + bbox conditioning).

## Main claim + result
Claims a new state-of-the-art in **layout-guided generation on COCO**, and that DetDiffusion syntheses augment training data to improve downstream detection (abstract). Specific mAP / FID numbers to be pulled from the paper body (not in the abstract). CVPR 2024.

## Relevance to us
The cleanest published instance of the **alignment thesis**: the perceptive model's signal *is* the generation control interface (P.A. loss + P.A. Attr), so the diagnosis→generation bridge is internal rather than a hand-built translator. Key questions for our gap: the signal here is a generic perception-aware loss, **not a grounded per-slice failure diagnosis** (no occlusion/size/class-confusion slices), and the loop is one-shot (no re-diagnosis). Compare with [[zhu2024-odgen-detection-generation]] (object-wise, occlusion) and [[chen2023-geodiffusion-geometric-control]] (box-only).

## Links
- [[stage3-state-of-the-art]]
