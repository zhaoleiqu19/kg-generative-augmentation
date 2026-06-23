---
title: "Synthetic Data from Diffusion Models Improves ImageNet Classification"
authors: Shekoofeh Azizi, Simon Kornblith, Chitwan Saharia, Mohammad Norouzi, David J. Fleet
year: 2023
venue: arXiv (TMLR)
url: https://arxiv.org/abs/2304.08466
loop-stage: stage3
tags: diffusion-models, synthetic-data, classification, helps, imagenet
---

## TL;DR
Fine-tuned (Imagen) class-conditional diffusion models generate synthetic ImageNet data that, added to real data, measurably raises classification accuracy over strong ResNet/ViT baselines.

## Method
Fine-tune a large text-to-image diffusion model into a class-conditional generator, sample class-balanced synthetic images, and augment the real ImageNet training set with them. Evaluate both generative quality (FID/IS) and downstream classification accuracy.

## Main claim + result
Reports "significant improvements in ImageNet classification accuracy over strong ResNet and Vision Transformer baselines" (abstract, arXiv:2304.08466). Concrete numbers from the abstract: FID 1.76 and Inception Score 239 at 256×256; downstream classification accuracy 64.96% at 256×256, rising to 69.24% at 1024×1024 — i.e. **higher-resolution / higher-fidelity synthetic samples help more**.

## Relevance to us
A canonical "synthetic data HELPS" data point with real numbers, and evidence that generation *fidelity/resolution* is the lever (69.24% vs 64.96%). Supports the helps-vs-hurts node and motivates fidelity control in our pipeline. Caveat: classification, not detection — does not settle the detection case (see [[ge2023-text2image-for-detection]]).

## Links
- [[does-synthetic-data-help]]
