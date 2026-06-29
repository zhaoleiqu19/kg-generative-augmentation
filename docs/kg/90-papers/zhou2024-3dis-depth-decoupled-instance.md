---
title: "3DIS: Depth-Driven Decoupled Instance Synthesis for Text-to-Image Generation (+ 3DIS-FLUX)"
authors: Dewei Zhou, Ji Xie, Zongxin Yang, Yi Yang
year: 2024
venue: arXiv:2410.12669 (ICLR 2025); 3DIS-FLUX = arXiv:2501.05131 (2025)
url: https://arxiv.org/abs/2410.12669
loop-stage: stage3
tags: object-detection, diffusion, multi-instance-generation, layout-control, depth, occlusion, training-free, flux, controllable-generation
---

## TL;DR
3DIS splits multi-instance generation into (1) a coarse **scene depth map** for instance positioning, then (2) **training-free attribute rendering** via pre-trained ControlNet on any base model — so the same layout control transfers to SD2/SDXL/Flux without retraining a renderer.

## Method
Two decoupled stages (abstract, arXiv:2410.12669): (i) generate a **coarse scene depth map** for accurate instance positioning + scene composition, via a custom adapter integrated into **LDM3D**; (ii) render fine-grained per-instance attributes using a **pre-trained ControlNet on any foundational model, without additional training**. Only the scene-construction (depth) stage needs adapter training; detail rendering is finetuning-free, which is what lets it port across base models. **3DIS-FLUX** (arXiv:2501.05131) swaps the renderer to **FLUX.1-Depth-dev** and manipulates the **Attention Mask in FLUX's Joint Attention** for detail rendering — higher image quality via a DiT base.

## Main claim + result
"Extensive experiments on **COCO-Position** and **COCO-MIG** benchmarks demonstrate that 3DIS significantly outperforms existing methods" in layout precision + attribute rendering (abstract); specific metric values **to be pulled from the paper body** (not in the abstract). 3DIS-FLUX reports surpassing the original 3DIS and current SOTA adapter-based methods in performance + image quality, **no numbers in the abstract**.

## Relevance to us
A high-alignment, **open-source** ([github.com/limuloo/3DIS](https://github.com/limuloo/3DIS), ICLR 2025 spotlight) peer/upgrade to InstanceDiffusion for the generation end: depth decoupling **handles occlusion natively** (the anchor's e-bike-behind-person axis) and the training-free renderer rides **Flux** for a higher quality ceiling than SD1.5 — the same niche as [[zhu2024-odgen-detection-generation]] (occlusion + multi-class) but with code and no per-domain finetuning. Same group as [[zhou2024-migcpp-multi-instance]]. Candidate generator for the MVP; being benchmarked against InstanceDiffusion / MIGC++ / GeoDiffusion in a separate cross-comparison.

## Links
- [[stage3-state-of-the-art]]
