---
title: "AUTHENTICATION: Identifying Rare Failure Modes in Autonomous Vehicle Perception Systems using Adversarially Guided Diffusion Models"
authors: Mohammad Zarei, Melanie A. Jutras, Eliana Evans, Mike Tan, Omid Aaramoon
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2504.17179
loop-stage: landscape
tags: object-detection, failure-modes, long-tail, adversarial, diffusion, inpainting, diagnosis-driven-generation
---

## TL;DR
A whole-loop neighbor for autonomous-vehicle perception: surfaces rare failure modes (RFMs) of a detector, then uses an adversarially guided inpainting diffusion model to *generate* images that expose those failures.

## Method
Extract segmentation masks for objects of interest (e.g. cars) and invert them into **environmental masks**; combine with crafted text prompts; feed into a **Stable Diffusion inpainting** model guided by **adversarial noise optimization** to synthesize environments that evade the object detector. Finally produce **natural-language descriptions** of the generated RFMs (abstract, arXiv:2504.17179).

## Main claim + result
Generates diverse, detection-evading scenes to understand and stress the long-tail of AV perception; positioned to feed both downstream training and testing. No benchmark mAP numbers are reported in the abstract (numbers to be pulled from the paper body).

## Relevance to us
A **diagnosis→generation** loop in spirit, but the "diagnosis" is **adversarial failure-induction**, not a measured per-object slice from real operating data — generation is steered by adversarial noise rather than by an aligned representation of *which real slices fail*. The region-inpaint + inverted-mask interface (environment held, object region controlled) is exactly the "region inpaint" row of our representation-map. Contrast with measured-diagnosis approaches [[chen2025-hibug2-error-slice-discovery]] / [[zhang2026-gh-esd-instance-slice-discovery]], and with placement-from-prior [[petersen2025-scene-aware-location]].

## Links
- [[related-systems-whole-loop]]
