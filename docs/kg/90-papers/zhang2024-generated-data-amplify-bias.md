---
title: "Will the Inclusion of Generated Data Amplify Bias Across Generations in Future Image Classification Models?"
authors: Zeliang Zhang, Xin Liang, Mingqian Feng, Susan Liang, Chenliang Xu
year: 2024
venue: arXiv
url: https://arxiv.org/abs/2410.10160
loop-stage: stage4
tags: self-consuming-loop, model-collapse, bias, synthetic-data, hurts
---

## TL;DR
When generated data is fed back into training across generations (a self-consuming loop), it can amplify subgroup bias — a "hurts" caution for any closed-loop augmentation system.

## Method
Builds a simulation environment with a self-consuming loop where the generative model and the classifier are trained synergistically across generations, then tracks fairness metrics over time. Run across Colorized MNIST, CIFAR-20/100, and Hard ImageNet over "hundreds of experiments" (abstract, arXiv:2410.10160).

## Main claim + result
Finds measurable "changes in fairness metrics across generations" and offers a conjecture for the bias dynamics when models train on continuously augmented datasets. No single headline number in the abstract; the contribution is the bias-amplification phenomenon + explanatory conjecture, not a benchmark score.

## Relevance to us
The key "HURTS / be careful" data point: indiscriminate, repeated synthetic augmentation can degrade *fairness*, not just accuracy. Argues that our loop must be **targeted and filtered** (cf. [[ouyang2025-safefix-model-repair]] VLM filtering) rather than blanket-iterative — and that we should monitor subgroup metrics, not only mAP.

## Links
- [[does-synthetic-data-help]]
