---
title: "Active Generation for Image Classification"
authors: Tao Huang, Jiaqi Liu, Shan You, Chang Xu
year: 2024
venue: arXiv (ECCV 2024)
url: https://arxiv.org/abs/2403.06517
loop-stage: stage2
tags: active-generation, targeted-augmentation, misclassification-signal, diagnosis-to-spec, classification
---

## TL;DR
ActGen makes generation *training-aware*: use the model's own misclassified samples as the signal for what to synthesize, generating images akin to the hard cases instead of bulk data.

## Method
Identifies "challenging or misclassified samples encountered by the current model" (abstract, arXiv:2403.06517) and generates similar-but-harder images via two guidance techniques: (1) attentive image guidance — real images as references during denoising, attention on class prompts to keep foreground while diversifying background; (2) gradient-based generation guidance — losses that make samples more challenging and avoid over-similarity.

## Main claim + result
"Achieves better performance with a significantly reduced number of generated images" vs methods that demand disproportionately large generation volumes (abstract). Tested on CIFAR and ImageNet. The abstract gives no single headline number — the contribution is the misclassification-driven *targeting*, not a volume record.

## Relevance to us
The cleanest stage-2 statement: **diagnosis signal (misclassification) → generation spec**. This is exactly the slice→spec handoff our loop needs, demonstrated for classification. Open for us: replace "misclassified image" with a *detection failure slice* (per-object), and "similar image" with a controllable layout spec (cf. [[chen2023-geodiffusion-geometric-control]]).

## Links
- [[stage2-state-of-the-art]]
