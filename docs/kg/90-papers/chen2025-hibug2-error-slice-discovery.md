---
title: "HiBug2: Efficient and Interpretable Error Slice Discovery for Comprehensive Model Debugging"
authors: Muxi Chen, Chenchen Zhao, Qiang Xu
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2501.16751
loop-stage: stage1
tags: slice-discovery, model-debugging, object-detection, pose-estimation, tag-then-slice, diagnosis
---

## TL;DR
A tag-then-slice debugging framework that generates task-specific visual attributes, enumerates error slices efficiently, and — crucially — predicts error slices *beyond* the validation set.

## Method
Generates task-specific visual attributes to flag error-prone instances, then runs an efficient slice-enumeration algorithm to systematically find error slices, combining interpretable attribute generation with structured exploration to beat the combinatorial blow-up (abstract, arXiv:2501.16751). Covers image classification, pose estimation, and object detection.

## Main claim + result
Key novelty: "predicting error slices beyond the validation set," addressing a major limitation of prior methods; improves coherence + precision of slices and "significantly enhances model repair capabilities." The abstract gives no specific numbers — pull from the paper's tables in a follow-up read.

## Relevance to us
Multi-task (incl. detection) and explicitly links discovery → repair, matching our loop. The "predict slices beyond validation" idea matters for the anchor: elevator footage will have failure modes not present in any held-out split. Compare its attribute-based slicing against GH-ESD's grounded/relational slicing for detection.

## Links
- [[stage1-state-of-the-art]]
