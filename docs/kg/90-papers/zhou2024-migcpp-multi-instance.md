---
title: "MIGC++: Advanced Multi-Instance Generation Controller for Image Synthesis"
authors: Dewei Zhou, You Li, Fan Ma, Zongxin Yang, Yi Yang
year: 2024
venue: arXiv (revised 2025; extends MIGC, CVPR 2024)
url: https://arxiv.org/abs/2407.02329
loop-stage: stage3
tags: diffusion, multi-instance-generation, layout-to-image, bounding-box, instance-mask, attribute-control, controllable-generation
---

## TL;DR
A multi-instance generation controller: place multiple objects at predefined positions with specified attributes, using a divide-and-conquer "shade each instance, then compose" strategy to stop attribute leakage between instances.

## Method
Introduces the Multi-Instance Generation (MIG) task; MIGC breaks multi-instance shading into **single-instance subtasks** ("divide-and-conquer") to avoid attribute leakage; **MIGC++** adds multimodal control (**position via boxes & masks**, **attributes via text & images**) and a **Consistent-MIG** algorithm for consistency under iterative edits (abstract, arXiv:2407.02329).

## Main claim + result
Claims to substantially outperform existing techniques on COCO-MIG, Multimodal-MIG, COCO-Position, and DrawBench (abstract). A secondary source reports ~+16% ISR over InstanceDiffusion on COCO-MIG-MASK; exact numbers to be pulled from the paper body.

## Relevance to us
Same alignment value as InstanceDiffusion (box/mask + attribute = the diagnosis-spec language), with an explicit fix for **attribute leakage** — important when an elevator scene has several similar instances (e.g. multiple e-bikes/people) that must keep distinct attributes (occluded vs not). Candidate engine for the "framed multi-instance spec → image" step. Compare [[wang2024-instancediffusion-instance-control]]; neither models occlusion Z-order like [[li2026-occlusionformer-zorder]].

## Links
- [[stage3-state-of-the-art]]
