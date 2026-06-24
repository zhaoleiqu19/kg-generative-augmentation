---
title: "Scene-Aware Location Modeling for Data Augmentation in Automotive Object Detection"
authors: Jens Petersen, Davide Abati, Amirhossein Habibian, Auke Wiggers
year: 2025
venue: arXiv (cs.CV)
url: https://arxiv.org/abs/2504.17076
loop-stage: stage2
tags: object-detection, placement, location-model, inpainting, scene-aware, occlusion, automotive, spec-bridge
---

## TL;DR
Learns a probabilistic model of *where* a new object can realistically go in an existing scene, then inpaints it there — replacing the usual "reuse the frame layout" or "place at random" with realistic, scene-conditioned placement.

## Method
A "scene-aware probabilistic location model that predicts where new objects can realistically be placed in an existing scene" (abstract, arXiv:2504.17076), paired with a generative inpainting model that renders the object at the sampled location. Diagnoses two failure modes of prior aug: layouts are either copied with little change (no diversity) or random (no realism).

## Main claim + result
Up to **+1.4 mAP** on automotive detection, **2.8× the +0.5 mAP** of competing placement methods; also improves instance segmentation (abstract). Benchmark/dataset names and per-class numbers to be pulled from the paper body.

## Relevance to us
Directly on the **G4 slice→spec bridge**: the novel piece is a *placement spec* (a learned distribution over where an object should appear), which is exactly the "where" half of turning a diagnosed slice into a generation spec. Its **inpaint-at-location** engine also serves occlusion/truncation better than copy-paste (the reconsidered T4 choice) because the object is composited *into* scene context. The gap it leaves open for us: placement is learned from the *scene prior*, **not derived from a measured detector failure** — coupling such a location model to a diagnosis is unaddressed. Compare placement-from-layout in [[chen2023-geodiffusion-geometric-control]] and region rectification in [[zhu2025-recon-region-controllable]].

## Links
- [[related-systems-whole-loop]]
- [[stage2-state-of-the-art]]
