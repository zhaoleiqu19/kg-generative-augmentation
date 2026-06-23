---
title: "GH-ESD: Grounded Hypothesis-Driven Error Slice Discovery for Instance-Level Vision Tasks"
authors: Wei Zhang, Chaoqun Wang, Zixuan Guan, Sam Kao, Pengfei Zhao, Peng Wu, Sifeng He
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2512.24592
loop-stage: stage1
tags: slice-discovery, object-detection, segmentation, instance-level, vlm, diagnosis
---

## TL;DR
Error slice discovery pushed to instance-level tasks (object detection, segmentation): finds failure slices grounded in spatial/relational visual patterns, not just attribute combinations.

## Method
A generate-and-verify framework: (1) construct failure hypotheses from LLM priors + visual evidence; (2) discover slices at the instance level via Vision-Language Models; (3) verify slices through statistical trend analysis (abstract, arXiv:2512.24592). "Grounded" = failures arise from "contextual relational and spatially grounded visual patterns" rather than simple attribute combos.

## Main claim + result
Targets detection/segmentation where per-image attribute slicing (Domino-style) is too coarse. Reports **improving Precision@10 by 0.10 (0.73 vs. 0.63)** on the GESD benchmark for detection (abstract).

## Relevance to us
The closest published work to **G2** (detection-granularity diagnosis). Demonstrates instance-level, spatially-grounded failure slicing — exactly what the anchor needs (e.g. "e-bike occluded by door, low light"). Key questions for our gap: does its hypothesis-verify loop handle small objects, and can its slices be turned into generation specs (stage 2)?

## Links
- [[stage1-state-of-the-art]]
