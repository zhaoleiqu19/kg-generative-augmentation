---
title: "The Big Data Myth: Using Diffusion Models for Dataset Generation to Train Deep Detection Models"
authors: Roy Voetman, Maya Aghaei, Klaas Dijkstra
year: 2023
venue: arXiv (cs.CV)
url: https://arxiv.org/abs/2306.09762
loop-stage: landscape
tags: object-detection, synthetic-data, skeptic, fine-tuned-stable-diffusion, manual-annotation, helps-vs-hurts
---

## TL;DR
Fine-tune Stable Diffusion to generate a detection dataset, **manually annotate** it, train detectors on it, and test on real images: detectors trained on synthetic data perform *similarly* to a real-data baseline.

## Method
Framework (abstract, arXiv:2306.09762): fine-tune pretrained Stable Diffusion on the domain → generate images → **manually annotate** them → train "various object detection models" → evaluate on a real test set of **331 images** vs. a real-data baseline. Note the honest cost caveat: annotations here are *manual*, so this is not a free-label result.

## Main claim + result
Synthetic-trained detectors "perform similarly to the baseline model"; for **apple detection in orchards** the AP deviation from the real-data baseline is **0.09–0.12** (abstract). Which detectors / which AP threshold to be pulled from the paper body.

## Relevance to us
A **calibrating skeptic** for the helps-vs-hurts ledger: even *fully synthetic* training reaches near-parity for detection — but on an *easy, low-occlusion, single-class* task (apples in orchards), with **manual** boxes. It bounds expectations two ways: (1) "near-parity, not better" warns that *blanket* synthetic data is a replacement, not an amplifier — gains need *targeting* (the project's bet); (2) the easy regime means it says nothing about small/occluded indoor CCTV (→ G3). Sits opposite the optimistic [[ge2023-text2image-for-detection]] in [[does-synthetic-data-help]].

## Links
- [[does-synthetic-data-help]]
- [[related-systems-whole-loop]]
