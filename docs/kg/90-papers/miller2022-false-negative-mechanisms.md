---
title: "What's in the Black Box? The False Negative Mechanisms Inside Object Detectors"
authors: Dimity Miller, Peyman Moghadam, Mark Cox, Matt Wildie, Raja Jurdak
year: 2022
venue: IEEE Robotics and Automation Letters (RA-L), vol. 7(3), pp. 8510-8517
url: https://arxiv.org/abs/2203.07662
loop-stage: stage1
tags: object-detection, false-negative, missed-detection, failure-mechanisms, diagnosis, robotics, domain-shift
---

## TL;DR
Opens the detector black box to name **five false-negative mechanisms** — each describing which internal component caused a target to be missed — and a framework to quantify them.

## Method
Identifies five "false negative mechanisms," each describing how a specific component inside the architecture failed, for **two-stage and one-stage anchor-box** detectors; introduces a framework to quantify them (abstract, arXiv:2203.07662). Applies it to Faster R-CNN and RetinaNet on benchmark vision vs. robotics datasets.

## Main claim + result
Shows a detector's FN-mechanism distribution **differs significantly between benchmark and robotics-deployment data** — implying benchmark-tuned detectors translate poorly to deployment. No single headline metric; the contribution is the mechanism taxonomy + quantification.

## Relevance to us
Maps to the **"missed / occlusion" representation** on the diagnosis side, and explains *why* boxes get missed at the architecture level. Caveat for alignment: the mechanisms are **internal** (anchor matching, score thresholding, etc.), not a scene-level description — so the bridge from "mechanism X fired" to "generate this kind of image" is indirect. The benchmark≠deployment finding is directly relevant to the anchor (elevator CCTV ≠ COCO). Complements scene-level slice methods [[zhang2026-gh-esd-instance-slice-discovery]].

## Links
- [[stage1-state-of-the-art]]
