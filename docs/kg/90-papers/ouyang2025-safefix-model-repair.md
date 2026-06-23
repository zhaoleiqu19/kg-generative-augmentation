---
title: "SafeFix: Targeted Model Repair via Controlled Image Generation"
authors: Ouyang Xu, Baoming Zhang, Ruiyu Mao, Yunhui Guo
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2508.08701
loop-stage: stage4
tags: model-repair, failure-attribution, controlled-generation, closed-loop, vlm-filtering
---

## TL;DR
A diagnosis-driven closed loop: attribute a vision model's systematic failures to underrepresented semantic subpopulations, then generate targeted synthetic images to repair exactly those weaknesses and retrain.

## Method
Pipeline: (1) an interpretable failure-attribution stage identifies "key failure attributes" — rare semantic subpopulations where the model systematically errs; (2) a conditional text-to-image model generates semantically accurate images targeting those failure cases; (3) a large vision-language model (LVLM) filters the generated set to keep alignment with the original data distribution and semantic consistency; (4) the model is retrained on the augmented synthetic dataset (abstract, arXiv:2508.08701).

## Main claim + result
Claims it "significantly reduce[s] errors associated with rare cases" and "improves model robustness without introducing new bugs" (abstract). Specific numeric gains are not in the abstract — to be extracted from the paper body / tables in a follow-up read. Code is released (GitHub link in paper).

## Relevance to us
This is the closest published template for our entire spine — the diagnosis→spec→synthesis→close-loop cycle in one system. The "failure attribution → targeted generation → VLM filtering → retrain" structure is almost exactly our intended loop. Key questions for us: what is their diagnosis granularity, and does targeted (vs. blanket) augmentation generalize to detection (they appear classification-centric)? This gap is what may differentiate our anchor-task contribution.

## Links
- [[generative-augmentation-landscape]]
