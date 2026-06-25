---
title: "InstanceDiffusion: Instance-level Control for Image Generation"
authors: Xudong Wang, Trevor Darrell, Sai Saketh Rambhatla, Rohit Girdhar, Ishan Misra
year: 2024
venue: arXiv (CVPR 2024)
url: https://arxiv.org/abs/2402.03290
loop-stage: stage3
tags: object-detection, diffusion, instance-level-control, layout-to-image, bounding-box, instance-mask, controllable-generation
---

## TL;DR
Adds precise per-instance control to text-to-image diffusion: each instance gets its own free-form text + a location given as a point, scribble, **bounding box**, or **segmentation mask** (or combinations).

## Method
Three additions to a T2I model (abstract + project page, arXiv:2402.03290): **UniFusion** (injects instance-level conditions), **ScaleU** (improves image fidelity), and a **Multi-instance Sampler** (better generations when many instances are present). Location can be specified as single points, scribbles, boxes, masks, or mixes thereof, with per-instance language.

## Main claim + result
Reports large gains over the prior instance/layout SOTA on COCO for both box and mask inputs (figures vary by source — on the order of ~2.0× AP50_box and ~1.7× IoU reported; exact numbers to be pulled from the paper body).

## Relevance to us
**The strongest generation-side fit for an aligned per-instance diagnosis spec.** Its control interface (per-instance box/mask + free-form text) is exactly the language a grounded detection diagnosis (size·occlusion·class per instance) would emit — so a GH-ESD-style slice could map near-directly onto InstanceDiffusion inputs. The Multi-instance Sampler suits crowded elevator scenes. Already chosen in our toolkit but **not yet built** (see decisions/gen-toolkit). Compare with box-only [[chen2023-geodiffusion-geometric-control]] and object-wise [[zhu2024-odgen-detection-generation]]; weaker on explicit occlusion ordering than [[li2026-occlusionformer-zorder]].

## Links
- [[stage3-state-of-the-art]]
