---
title: "Improving Object Detection by Modifying Synthetic Data with Explainable AI"
authors: Nitish Mital, Simon Malzard, Richard Walters, Celso M. De Melo, Raghuveer Rao, Victoria Nockles
year: 2024
venue: arXiv
url: https://arxiv.org/abs/2412.01477
loop-stage: landscape
tags: object-detection, synthetic-data, explainable-ai, human-in-the-loop, feedback-driven-generation, 3d-rendering
---

## TL;DR
A feedback-driven whole-loop neighbor: uses Explainable-AI saliency to tell a human *how* to edit the 3D mesh models that render synthetic training images, so the synthetic data is modified toward what the detector actually needs.

## Method
Robust XAI (saliency) techniques highlight which aspects of synthetic 3D models drive detection errors; these guide a **human-in-the-loop** process of modifying the 3D mesh models (in Unity) used to render the images — increasing or decreasing realism/abstraction where indicated (abstract, arXiv:2412.01477). The loop is: render → detect → explain → edit mesh → re-render.

## Main claim + result
Synthetic data alone improved vehicle detection in unseen orientations by **+4.6% to mAP50 = 94.6%**; XAI-guided mesh modifications added a further **+1.5% to mAP50 = 96.1%** (per fetched summary of results).

## Relevance to us
A diagnosis→generation loop where the **diagnosis signal is XAI saliency** and the **generation interface is a 3D-renderer's mesh parameters** — a different representation pair than ours (real-image diffusion), and crucially **human-in-the-loop** rather than an automated bridge, on **rendered** (not real) images. Useful as a contrast point: it shows feedback-driven synthetic editing works, but neither end matches our box-level-diagnosis ↔ controllable-real-image-generation alignment. Contrast with [[ouyang2025-safefix-model-repair]] (classification repair loop).

## Links
- [[related-systems-whole-loop]]
