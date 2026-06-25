---
title: "Knowledge-Guided Failure Prediction: Detecting When Object Detectors Miss Safety-Critical Objects"
authors: Jakob Paul Zimmermann, Gerrit Holzbach, David Lerch
year: 2026
venue: arXiv (CVPR 2026 SAIAD Workshop)
url: https://arxiv.org/abs/2603.25499
loop-stage: stage1
tags: object-detection, failure-prediction, false-negative, foundation-model, runtime-monitoring, safety-critical, diagnosis
---

## TL;DR
A runtime gate (KGFP) that predicts when a detector is about to miss a safety-critical object, by measuring how far the detector's internal features drift from a visual foundation model's embeddings.

## Method
Dual-encoder architecture monitoring the detector at runtime: measures **semantic misalignment between the detector's internal features and visual-foundation-model embeddings via an angular-distance metric**. When the detector operates outside its competence (or the foundation model sees novel input), the embeddings diverge — flagging a potentially unsafe image (per fetched summary, arXiv:2603.25499).

## Main claim + result
As a selective-prediction gate on COCO person detection: **person recall rises 64.3% → 84.5% among accepted images at a fixed 5% FPR**, and stays strong across six COCO-O visual domains, substantially beating OOD baselines.

## Relevance to us
A **per-image failure predictor** ("will this frame be missed?"), so it fits the loop best as a **trigger / verifier** (stage 3 filter or re-diagnosis gate) rather than as a box-level slice spec — it says *whether* a frame is unsafe, not *what configuration* (size/occlusion) to generate. The foundation-model-misalignment signal is a candidate stop/quality check for the anchor. Contrast with spec-producing diagnosis [[zhang2026-gh-esd-instance-slice-discovery]].

## Links
- [[stage1-state-of-the-art]]
