---
title: "SynthVLM: Towards High-Quality and Efficient Synthesis of Image-Caption Datasets for Vision-Language Models"
authors: Zheng Liu, Hao Liang, Bozhou Li, Wentao Xiong, Chong Chen, Conghui He, Wentao Zhang, Bin Cui
year: 2024
venue: arXiv
url: https://arxiv.org/abs/2407.20756
loop-stage: stage4
tags: clipscore-filtering, quality-selection, synthetic-data, efficiency, less-is-more
---

## TL;DR
Generate images from high-quality captions with diffusion, then CLIPScore-filter the pairs — 18% curated synthetic data beats a full-dataset baseline.

## Method
Reverses the usual pipeline: synthesize images *from* high-quality captions via diffusion, then use "CLIPScore-based filtering to curate synthesized image-text pairs," keeping only well-aligned ones (abstract, arXiv:2407.20756). Releases SynthVLM-100K.

## Main claim + result
SynthVLM "outperform[s] LLaVA across most metrics with only **18% pretrain data**" (abstract); curated synthetic pairs beat web-sourced data in automated + human eval.

## Relevance to us
Concrete "**less-is-more via quality filter**" evidence: a CLIPScore gate lets a small curated set outperform a large raw one — the quantitative case for the filter step in our loop (echoes verification, [[yi2025-escaping-collapse-verification]]). Caveat: VLM caption pretraining, not detection; for us the gate is detector/VLM agreement on the generated box, and the metric is size-specific AP, not VLM benchmarks.

## Links
- [[stage4-state-of-the-art]]
