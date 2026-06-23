---
title: "AI-Generated Images as Data Source: The Dawn of Synthetic Era"
authors: Zuhao Yang, Fangneng Zhan, Kunhao Liu, Muyu Xu, Shijian Lu
year: 2023
venue: arXiv
url: https://arxiv.org/abs/2310.01830
loop-stage: landscape
tags: synthetic-data, object-detection, generative-ai, data-augmentation, survey
---

## TL;DR
Comprehensive survey examining how AI-generated images can replace or augment real data for visual intelligence tasks, covering generative models, neural rendering, and downstream applications including object detection, segmentation, and autonomous driving.

## Method
The survey organizes AI-generated data sources into two technological foundations — generative models (GANs, diffusion models, text-to-image) and neural rendering — then maps them onto downstream applications. For object detection specifically, the authors identify three mainstream synthetic data generation approaches: (1) copy-paste synthesis with bounding box annotations, (2) layout-to-image generation using geometric conditions (e.g., GeoDiffusion), and (3) imaginary-supervised learning that eliminates human annotation entirely (e.g., ImaginaryNet).

## Main claim + result
AI-generated images can match or exceed real-data performance on downstream vision tasks while being ~47x cheaper to produce. Generative images cost approximately $2.54×10⁻⁴ per image versus $1.20×10⁻² for human-labeled real images (Table III of the paper). For object detection, the cut-and-paste foreground synthesis approach yielded the greatest per-image performance enhancement in controlled comparisons (Table VI).

## Relevance to us
Directly relevant to the diagnosis-driven augmentation loop. The survey maps the full landscape of techniques we may draw from at stage 3 (synthesis): copy-paste pipelines, diffusion-based layout-conditional generation, and annotation-free training. The 47x cost figure is a useful baseline for justifying the synthetic-augmentation route over human re-labeling.

## Links
- [[glossary]]
