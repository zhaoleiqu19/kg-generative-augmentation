---
title: "TIDE: A General Toolbox for Identifying Object Detection Errors"
authors: Daniel Bolya, Sean Foley, James Hays, Judy Hoffman
year: 2020
venue: arXiv (ECCV 2020)
url: https://arxiv.org/abs/2008.08115
loop-stage: stage1
tags: object-detection, instance-segmentation, error-analysis, error-taxonomy, diagnosis, representation-source
---

## TL;DR
A dataset-agnostic, drop-in replacement for mAP that splits detection error into six types and — crucially — isolates how much each type costs overall performance.

## Method
Operates directly on prediction files, no knowledge of the underlying system needed (abstract, arXiv:2008.08115). Segments errors into **six types** and introduces the first technique for measuring each error's *isolated* contribution to overall performance. Validated across 4 datasets and 7 recognition models. The six error types (named in the TIDE paper/toolbox): **classification, localization, both (cls+loc), duplicate, background, missed (false negative)**.

## Main claim + result
First to isolate each error type's effect on overall mAP (so two models with the same mAP can be told apart by *why* they fail). No single headline number — it is a diagnostic framework; per-model breakdowns are the output.

## Relevance to us
**The canonical box-level "representation vocabulary" for the diagnosis side**: its six categories (esp. localization / classification / missed) are exactly the kind of failure axis that could be aligned to a generation control interface (size·occlusion·class-confusion → layout spec). Caveat for the alignment thesis: TIDE aggregates errors at the **dataset level**, not per-instance grounded slices — to turn a TIDE category into a *generation spec* you still need instance-level grounding (see [[zhang2026-gh-esd-instance-slice-discovery]] / [[chen2025-hibug2-error-slice-discovery]]). Successor to Hoiem's 2012 detector-error analysis.

## Links
- [[stage1-state-of-the-art]]
