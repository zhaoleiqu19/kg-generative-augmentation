---
title: "Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data"
authors: Matthias Gerstgrasser, Rylan Schaeffer, Apratim Dey, Rafael Rafailov, Henry Sleight, John Hughes, Tomasz Korbak, Rajashree Agrawal, Dhruv Pai, Andrey Gromov, Daniel A. Roberts, Diyi Yang, David L. Donoho, Sanmi Koyejo
year: 2024
venue: arXiv
url: https://arxiv.org/abs/2404.01413
loop-stage: stage4
tags: model-collapse, data-accumulation, self-consuming-loop, closed-loop-safety, theory
---

## TL;DR
Model collapse comes from *replacing* real data with synthetic across generations; if instead you *accumulate* real + all synthetic generations, collapse is provably avoided.

## Method
Compares "replace" vs "accumulate" data regimes across language models (text), diffusion models (molecular generation), and VAEs (image generation). In a linear-models framework, proves an accumulation bound (abstract, arXiv:2404.01413).

## Main claim + result
"Accumulating the successive generations of synthetic data alongside the original real data avoids model collapse" (abstract). Theory: with accumulation "the test error has a finite upper bound independent of the number of iterations," so collapse no longer occurs; replacement instead degrades "until fitted models become useless."

## Relevance to us
The foundational safety rule for our closed loop: **never discard the real data — accumulate.** Directly counters the bias-amplification risk of [[zhang2024-generated-data-amplify-bias]]. Caveat: shown on text/molecules/VAEs, not detection — the *principle* transfers, the exact synthetic:real ratio for detection is unverified (→ G3).

## Links
- [[stage4-state-of-the-art]]
