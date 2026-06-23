---
title: "ReCon: Region-Controllable Data Augmentation with Rectification and Alignment for Object Detection"
authors: Haowei Zhu, Tianxiang Pan, Rui Qin, Jun-Hai Yong, Bin Wang
year: 2025
venue: arXiv (NeurIPS 2025 spotlight)
url: https://arxiv.org/abs/2510.15783
loop-stage: stage3
tags: region-controllable, object-detection, diffusion, rectification, alignment, spec-format
---

## TL;DR
ReCon makes structure-controllable detection generation actually faithful: it corrects misgenerated regions during sampling and aligns each region to its text description.

## Method
Two components on top of structure-controllable diffusion (abstract, arXiv:2510.15783): (1) **region-guided rectification** — uses feedback from pre-trained perception models to fix misgenerated regions during the diffusion sampling process; (2) **region-aligned cross-attention** — enforces correspondence between image regions and their textual descriptions for spatial-semantic alignment.

## Main claim + result
Reports "consistent performance gains across various datasets, backbone architectures, and data scales." Exact mAP/AP deltas not in the abstract — pull from tables later. NeurIPS 2025 spotlight; code released.

## Relevance to us
The state-of-the-art on *faithful* region-controlled detection generation — directly relevant once a spec exists. Its perception-model-feedback rectification is itself a mini diagnosis→correction loop, echoing our spine. For the anchor, region control + rectification is what would keep small/occluded e-bike instances correctly rendered and labeled.

## Links
- [[stage2-state-of-the-art]]
