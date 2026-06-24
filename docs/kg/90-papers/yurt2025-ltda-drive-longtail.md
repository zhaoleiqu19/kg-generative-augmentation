---
title: "LTDA-Drive: LLMs-guided Generative Models based Long-tail Data Augmentation for Autonomous Driving"
authors: Mahmut Yurt, Xin Ye, Yunsheng Ma, Jingru Luo, Abhirup Mallik, John Pauly, Burhaneddin Yaman, Liu Ren
year: 2025
venue: arXiv (cs.RO)
url: https://arxiv.org/abs/2505.18198
loop-stage: stage3
tags: object-detection, long-tail, diffusion, llm-filter, autonomous-driving, generate-then-filter, closed-loop-adjacent
---

## TL;DR
A three-stage augment-by-replacement pipeline for rare classes in driving scenes: diffusion removes a head-class object, a generative model inserts a tail-class instance in its place, and an LLM agent filters low-quality results.

## Method
Three stages (abstract, arXiv:2505.18198): (1) text-guided diffusion **removes head-class objects**, (2) generative models **insert tail-class instances** (e.g. pedestrians/cyclists), (3) an **LLM agent filters** low-quality syntheses. Targets the failure of reweighting/resampling under genuine tail-class scarcity by *manufacturing* tail samples rather than reusing the few that exist.

## Main claim + result
"34.75% improvement for rare classes over counterpart methods" on **KITTI** tail-class 3D detection (abstract). Per-class breakdown and absolute AP to be pulled from the paper body.

## Relevance to us
The **closest recent whole-loop neighbor**: it chains generate→insert→LLM-filter for *detection* and aims squarely at the long-tail/rare-event axis the anchor shares (rare "e-bike-in-elevator"). But it is **not diagnosis-driven** — it augments the tail *by definition* (blanket long-tail), not from a measured per-slice failure — and it is 3D AV, not 2D indoor CCTV. So it sharpens, rather than closes, G1: the loop exists in pieces but isn't *steered by a diagnosis*. The LLM-as-filter is a concrete stage-4 verifier candidate. Contrast the detection-side engine with [[zhu2024-odgen-detection-generation]]; the filter idea echoes [[ouyang2025-safefix-model-repair]].

## Links
- [[related-systems-whole-loop]]
- [[stage3-state-of-the-art]]
