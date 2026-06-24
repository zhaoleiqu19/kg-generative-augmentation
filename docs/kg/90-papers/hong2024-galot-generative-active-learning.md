---
title: "GALOT: Generative Active Learning via Optimizable Zero-shot Text-to-image Generation"
authors: Hanbin Hong, Shenao Yan, Shuya Feng, Yan Yan, Yuan Hong
year: 2024
venue: arXiv (cs.CV)
url: https://arxiv.org/abs/2412.16227
loop-stage: stage4
tags: active-learning, text-to-image, generative-active-learning, pseudo-label, closed-loop, classification, zero-shot
---

## TL;DR
Closes an active-learning loop with no real data: AL criteria optimize the *text prompts* of a zero-shot T2I model to synthesize informative, diverse samples, which are pseudo-labeled from the text and used to train a vision model.

## Method
Integrates active learning with zero-shot T2I synthesis (abstract, arXiv:2412.16227): "leverage the AL criteria to optimize the text inputs for generating more informative and diverse data samples, annotated by the pseudo-label crafted from text," yielding a synthetic dataset — an "end-to-end ML task from text description to vision models." The AL criterion (informativeness/diversity) is the *steering signal* that drives what gets generated.

## Main claim + result
"Consistent and significant improvements over traditional AL methods" (abstract) — no numbers in the abstract; metrics, datasets, and AL baselines to be pulled from the paper body.

## Relevance to us
The **clearest closed-loop neighbor on the targeting axis**: an explicit *selection criterion → generate* loop, which is structurally what G1/G4 demand. Two reasons it doesn't pre-empt our seam: (1) it is **classification** with text-derived pseudo-labels — detection needs *correct boxes*, which a text prompt cannot pseudo-label; (2) it is **fully synthetic** (no real images, no per-object failure diagnosis) — the criterion is generic AL uncertainty, not a grounded detection slice. So it shows the loop is buildable but not in the regime that blocks detection (free labels + box correctness, cf. the post-handoff analysis). Compare image-level targeting in [[huang2024-actgen-active-generation]] and [[nguyen2025-tada-targeted-augmentation]].

## Links
- [[related-systems-whole-loop]]
- [[stage4-state-of-the-art]]
