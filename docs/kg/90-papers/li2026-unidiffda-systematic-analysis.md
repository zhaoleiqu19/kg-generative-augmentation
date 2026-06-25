---
title: "Diffusion-Based Data Augmentation for Image Recognition: A Systematic Analysis and Evaluation"
authors: Zekun Li, Yinghuan Shi, Yang Gao, Dong Xu
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2603.08364
loop-stage: stage3
tags: diffusion, data-augmentation, survey, benchmark, classification, low-data
---

## TL;DR
A unifying analysis (UniDiffDA) of diffusion-based data augmentation: decomposes the whole DiffDA workflow into three components and benchmarks representative methods on a fair, shared protocol.

## Method
Introduces **UniDiffDA**, a framework that decomposes DiffDA methods into three core components — **model fine-tuning, sample generation, and sample utilization** — to expose the design space and the key differences among methods. Builds a unified codebase and a fair evaluation protocol, benchmarking representative DiffDA methods across diverse low-data **classification** tasks (abstract, arXiv:2603.08364).

## Main claim + result
Provides a controlled, apples-to-apples comparison the prior literature lacked (methods previously varied in task config, model choice, and pipeline). Reports relative strengths/limitations of DiffDA strategies and design guidance; per-method numbers sit in the paper body. Code and configs released for reproducibility.

## Relevance to us
A **positioning anchor** for the generation side: its three-component decomposition (fine-tune / generate / utilize) is a clean axis for organizing our generation survey, and its fair-protocol finding warns that DiffDA gains are pipeline-sensitive. Caveat for our scope: it benchmarks **classification**, not detection — so it bounds the field but does not cover the box-level interface we care about. Complements the methods/metrics review [[alimisis2024-diffusion-augmentation-review]].

## Links
- [[generative-augmentation-landscape]]
