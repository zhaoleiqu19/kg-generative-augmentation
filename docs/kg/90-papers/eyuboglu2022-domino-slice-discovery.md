---
title: "Domino: Discovering Systematic Errors with Cross-Modal Embeddings"
authors: Sabri Eyuboglu, Maya Varma, Khaled Saab, Jean-Benoit Delbrouck, Christopher Lee-Messer, Jared Dunnmon, James Zou, Christopher Ré
year: 2022
venue: arXiv (ICLR 2022)
url: https://arxiv.org/abs/2203.14960
loop-stage: stage1
tags: slice-discovery, failure-attribution, cross-modal, classification, diagnosis
---

## TL;DR
The foundational slice-discovery method: find coherent subsets where a classifier systematically errs, using CLIP-style cross-modal embeddings, and auto-describe each slice in natural language.

## Method
Three steps — embed, slice, describe. Embed inputs and text in a shared cross-modal (CLIP) space; an "error-aware mixture model" clusters data by embedding + class label + model prediction to surface underperforming regions; then generate a natural-language name for each discovered slice (abstract, arXiv:2203.14960). Evaluated on natural images, medical images, and time-series.

## Main claim + result
First slice-discovery method to give natural-language slice descriptions. Identifies **36% of 1,235 tested slices — a 12-point improvement over prior methods**, and "correctly generat[es] the exact name of the slice in 35% of settings" (abstract).

## Relevance to us
The vocabulary anchor for stage 1: defines "slice discovery" and the embed→slice→describe template. But it is **classification-only** (per-image label), exactly the granularity our anchor (detection) must go beyond — it frames G2 rather than solving it.

## Links
- [[stage1-state-of-the-art]]
