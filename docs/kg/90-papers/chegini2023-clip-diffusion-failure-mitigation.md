---
title: "Identifying and Mitigating Model Failures through Few-shot CLIP-aided Diffusion Generation"
authors: Atoosa Chegini, Soheil Feizi
year: 2023
venue: arXiv
url: https://arxiv.org/abs/2312.05464
loop-stage: stage1
tags: failure-attribution, diffusion-generation, spurious-correlation, diagnosis-to-generation, classification
---

## TL;DR
End-to-end diagnosis→generation: use LLMs/VLMs to describe a model's failure modes (e.g. spurious background correlations) in natural language with no human labels, then diffusion-generate targeted data to fix them.

## Method
Leverage LLMs + vision-language models to produce interpretable descriptions of spurious correlations / failure scenarios automatically; use those descriptions to guide diffusion-model synthesis of targeted training data; retrain few-shot to remediate (abstract, arXiv:2312.05464). Focus on incorrect background associations.

## Main claim + result
Tested across **40 models** (ResNets, EfficientNets, ViTs, CLIP variants) on ImageNet-1000, CIFAR-10/100, with "**remarkable improvements in accuracy (~21%) on hard sub-populations**," especially background-related failures (abstract).

## Relevance to us
The cleanest published instance of the stage1→stage3 bridge: automatic failure *description* directly becomes the generation *spec*. The ~21% gain on hard sub-populations is a strong "diagnosis-driven generation works" data point. Caveat: classification + background spurious-correlation; G1 asks whether this transfers to detection of small/occluded objects.

## Links
- [[stage1-state-of-the-art]]
