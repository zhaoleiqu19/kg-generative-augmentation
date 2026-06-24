---
title: "Leveraging Latent Diffusion Models for Training-Free In-Distribution Data Augmentation for Surface Defect Detection"
authors: Federico Girella, Ziyue Liu, Franco Fummi, Francesco Setti, Marco Cristani, Luigi Capogrosso
year: 2024
venue: CBMI 2024 (21st Int. Conf. on Content-Based Multimedia Indexing)
url: https://arxiv.org/abs/2407.03961
tags: training-free, in-distribution, human-in-loop, region-conditioning, surface-defect, anomaly-generation, latent-diffusion
loop-stage: stage3
---

## TL;DR
DIAG generates *in-distribution* synthetic defects training-free: a domain expert gives a text description + a region where the anomaly should go, and a latent diffusion model paints it there — no fine-tuning.

## Method
A "training-free Diffusion-based In-distribution Anomaly Generation pipeline" with a **human-in-the-loop**: experts provide "multimodal guidance ... through text descriptions and region localization of the possible anomalies" (abstract, arXiv:2407.03961). Operates **zero-shot** (no fine-tuning). The framing critique it fixes: conventional artifact-superimposition augmentation produces **out-of-distribution** images, so the model learns "what is not normal" but not what a defect *looks like*.

## Main claim + result
On **KSDD2** surface-defect detection: AP improvement of **≈18% when positive samples are available** and **≈28% when they are missing**, vs. SOTA augmentation (abstract). Code: github.com/intelligolabs/DIAG.

## Relevance to us
Two transferable ideas, one caveat. Ideas: (1) **in-distribution** generation as the explicit objective — the same risk the anchor faces if Flux outputs drift off the CCTV manifold (ties to G3 helps-vs-hurts); (2) **region localization as the spec** — a human marks *where*, which is the manual version of the G4 slice→spec bridge (automate that marker from a diagnosis and you have the missing link). Caveat: it is **anomaly/defect detection** (per-pixel-ish, single-object, expert-in-loop), not multi-object boxed detection, and targeting is **human**, not diagnosed. Compare the human region-spec here with the learned placement of [[petersen2025-scene-aware-location]].

## Links
- [[related-systems-whole-loop]]
- [[stage3-state-of-the-art]]
