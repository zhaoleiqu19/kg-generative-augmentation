---
title: "Data-centric Artificial Intelligence: A Survey"
authors: Daochen Zha, Zaid Pervaiz Bhat, Kwei-Herng Lai, Fan Yang, Zhimeng Jiang, Shaochen Zhong, Xia Hu
year: 2023
venue: arXiv
url: https://arxiv.org/abs/2303.10158
loop-stage: foundations
tags: data-centric-ai, survey, data-quality, taxonomy
---

## TL;DR
Foundational survey of the shift from model-centric to data-centric AI: improving the quality and quantity of data, rather than the model architecture, as the primary lever for performance.

## Method
Organizes the data-centric literature around three general goals across the data lifecycle: (1) training data development, (2) inference data development, and (3) data maintenance. Cross-cuts these with two perspectives — automation (systematic data-engineering techniques) and collaboration (human involvement) — and collects methods, benchmarks, and resources for each.

## Main claim + result
Central thesis: "the attention of researchers and practitioners has gradually shifted from advancing model design to enhancing the quality and quantity of the data" (abstract, arXiv:2303.10158). No single headline metric — it is a taxonomy/position survey rather than an empirical study; specific numbers live in the cited primary works, not the abstract.

## Relevance to us
This is the conceptual frame for the whole project: the diagnosis-driven augmentation loop is a concrete instance of training-data development under data-centric AI. Its three-goal taxonomy gives us vocabulary to place each loop stage (diagnosis = data maintenance/quality auditing; synthesis = training-data development).

## Links
- [[glossary]]
- [[generative-augmentation-landscape]]
