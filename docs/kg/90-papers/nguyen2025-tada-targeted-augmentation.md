---
title: "Do We Need All the Synthetic Data? Targeted Image Augmentation via Diffusion Models"
authors: Dang Nguyen, Jiping Li, Jinghao Zheng, Baharan Mirzasoleiman
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2505.21574
loop-stage: stage2
tags: targeted-augmentation, sample-selection, diffusion, efficiency, classification
---

## TL;DR
TADA augments only the *hard-to-learn* subset (examples not learned early in training) with faithful synthetic variants — and beats augmenting the whole dataset.

## Method
TArgeted Diffusion Augmentation: select examples "not learned early in training," generate "faithful synthetic images that preserve semantic features while varying noise," and augment only that subset (abstract, arXiv:2505.21574). Backed by theory on a two-layer CNN: improves generalization by homogenizing feature-learning speed without amplifying noise.

## Main claim + result
"Augmenting only this targeted subset consistently outperforms augmenting the entire dataset." Augmenting only **30–40%** of data yields **up to +2.8%** generalization across ResNet/ViT/ConvNeXt/Swin on CIFAR-10/100, TinyImageNet, ImageNet; TADA+SGD even beats the SAM optimizer on CIFAR-100/TinyImageNet (abstract).

## Relevance to us
Strong "**targeted beats blanket**" evidence with numbers — the quantitative backbone for why our loop should spec a *subset*, not flood. The selection criterion (not-learned-early) is a candidate diagnosis signal. Caveat: classification, image-level; for detection the "hard subset" must be defined at object/slice level (→ G2) and the gain re-measured on size-specific AP (→ G3).

## Links
- [[stage2-state-of-the-art]]
