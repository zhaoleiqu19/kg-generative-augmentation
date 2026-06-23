# Does Synthetic Data Help (or Hurt)?

## What it is
The helps-vs-hurts debate: when does adding generated/synthetic images improve a downstream vision model, and when does it degrade it? This node collects the evidence on both sides with cited numbers, so later stages can set design rules.

## Why it matters
The whole project bets on generation improving a detector. That bet is only safe under specific conditions; this node pins down what they are, so the diagnosis-driven loop generates *the helpful kind* of data and avoids the harmful kind.

## Key papers

### HELPS
- [[azizi2023-synthetic-data-improves-imagenet]] — classification: augmenting ImageNet with diffusion samples beats strong ResNet/ViT baselines; accuracy **64.96% → 69.24%** as sample resolution rises 256→1024 (FID 1.76). Fidelity is the lever.
- [[ge2023-text2image-for-detection]] — **detection/segmentation**: detectors trained *solely* on composed synthetic data reach performance "comparable to real data" on VOC/COCO; synthetic+real does better. Cut-and-paste with auto boxes.
- [[yang2023-ai-generated-images-data-source]] — synthetic ~47x cheaper per labeled image; cut-and-paste foreground synthesis gave the largest per-image detection gain in its comparison.

### HURTS / LIMITS
- [[zhang2024-generated-data-amplify-bias]] — feeding generated data back across generations (self-consuming loop) **amplifies subgroup bias**; fairness degrades even when accuracy may not. Argues against blanket/iterative augmentation.

## Synthesis (provisional rules)
1. **Fidelity matters** — higher-quality/resolution samples help more (Azizi: +4.3pts from resolution alone).
2. **Targeted + combined beats pure + blanket** — synthetic *with* real, and aimed at specific gaps, is the reliable regime (Ge; cf. SafeFix targeting).
3. **Iterating unfiltered hurts** — repeated self-consumption amplifies bias (Zhang); a filter step (VLM, cf. [[ouyang2025-safefix-model-repair]]) and subgroup monitoring are needed.
4. **Open for our regime:** none of the "helps" results isolate the **small/occluded detection** case — the anchor's regime is unverified (feeds [[generative-augmentation-landscape]] G3).

## Open questions
- At what synthetic-to-real ratio does help turn to hurt for *detection* (not classification)?
- Does fidelity (Azizi's lever) matter as much for detection as for classification?
- Can a VLM/quality filter prevent the bias amplification Zhang reports while keeping the gains?

## Our take
Synthetic data reliably helps when it is **high-fidelity, combined with real data, targeted at a real gap, and filtered** — and reliably risks harm when it is blanket, iterative, and unfiltered. The diagnosis-driven loop is, by construction, on the safe side of every one of these axes; the unproven axis is small-object detection specifically.
