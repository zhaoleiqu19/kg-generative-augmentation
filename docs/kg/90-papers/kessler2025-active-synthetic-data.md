---
title: "Towards Active Synthetic Data Generation for Finetuning Language Models"
authors: Samuel Kessler, Menglin Xia, Daniel Madrigal Diaz, Dongge Han, Helia Heshemi, Saravan Rajmohan, Victor Ruehle, Jordan T. Ash
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2512.00884
loop-stage: stage4
tags: closed-loop, active-learning, synthetic-data-curation, student-state-feedback, selection
---

## TL;DR
Generate synthetic finetuning data in an iterative closed loop steered by the student model's current state, and curate it with simple active-learning selection — beating static one-shot generation.

## Method
"Data are generated in an iterative, closed-loop fashion that is guided by the current state of the student model" (abstract, arXiv:2512.00884). Rather than LLM-specific tricks, uses "simple, inexpensive selection criteria from the active learning literature." Validated on math/logic reasoning across four small LMs.

## Main claim + result
For fixed compute, closed-loop curation "delivers improved student performance over static generation" (abstract). The contribution is the *loop + cheap active-learning selection*, not a single benchmark number.

## Relevance to us
The control-loop blueprint for our spine: regenerate based on the *current* detector's weaknesses (= re-diagnose each round), and use cheap active-learning selection rather than bespoke heuristics. Connects stage 4 back to stage 1 (re-diagnosis) and stage 2 (what to select). Caveat: NLP reasoning, not detection — the selection criterion must be redefined at object/slice level for us.

## Links
- [[stage4-state-of-the-art]]
