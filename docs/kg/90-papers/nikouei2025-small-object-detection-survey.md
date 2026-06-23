---
title: "Small Object Detection: A Comprehensive Survey on Challenges, Techniques and Real-World Applications"
authors: Mahya Nikouei, Bita Baroutian, Shahabedin Nabavi, Fateme Taraghi, Atefe Aghaei, Ayoob Sajedi, Mohsen Ebrahimi Moghaddam
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2503.20516
loop-stage: anchor
tags: small-object-detection, survey, surveillance, data-augmentation, domain-adaptation
---

## TL;DR
Comprehensive survey of small-object detection: the challenges that make small objects hard, the deep-learning technique families that address them, and the datasets/metrics/applications of the field.

## Method
Surveys four core technique categories — multi-scale feature extraction, super-resolution, attention mechanisms, and transformer architectures — plus auxiliary solutions including data augmentation, synthetic data generation, transfer learning, lightweight networks, knowledge distillation, and self-supervised learning. Reviews widely-used datasets and standard metrics (mAP and size-specific AP).

## Main claim + result
Names the defining challenges as "low resolution, occlusion, background interference, and class imbalance" (abstract, arXiv:2503.20516), spanning surveillance, autonomous systems, medical imaging, and remote sensing. Future priorities: robust domain adaptation, better feature-fusion, and real-time/edge performance. No single headline number — it is a survey; size-specific AP is the recommended evaluation lens.

## Relevance to us
Closest survey to the anchor task: elevator-CCTV e-bikes are small, often occluded objects against cluttered backgrounds — exactly the regime this survey characterizes. Its challenge list (occlusion, class imbalance) and its call for domain adaptation + synthetic data align precisely with what our diagnosis-driven loop is meant to fix. Provides the evaluation lens (size-specific AP) for measuring whether augmentation helps the small/occluded case.

## Links
- [[generative-augmentation-landscape]]
