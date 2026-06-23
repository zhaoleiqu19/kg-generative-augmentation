---
title: "AeroGen: Enhancing Remote Sensing Object Detection with Diffusion-Driven Data Generation"
authors: Datao Tang, Xiangyong Cao, Xuan Wu, Jialin Li, Jing Yao, Xueru Bai, Dongsheng Jiang, Yin Li, Deyu Meng
year: 2024
venue: arXiv
url: https://arxiv.org/abs/2411.15497
loop-stage: stage3
tags: remote-sensing, small-object, object-detection, diffusion, layout-control, filtering, rare-class
---

## TL;DR
AeroGen generates remote-sensing detection data from layout conditions (horizontal AND rotated boxes), with a diversity-conditioned generator plus a filtering step — giving big gains on rare classes.

## Method
A layout-controllable diffusion model supporting both horizontal and rotated bounding-box conditions, combined with "a diversity-conditioned generator and a filtering mechanism" (abstract, arXiv:2411.15497). First to support rotated-box conditional generation for synthetic remote-sensing imagery.

## Main claim + result
mAP **+3.7% (DIOR), +4.3% (DIOR-R), +2.43% (HRSC)**; crucially, **rare-class gains reach +12.6–17.8%** (abstract). The built-in filter is an in-pipeline quality gate.

## Relevance to us
Remote-sensing objects are **small** — the closest published regime to elevator small-object detection, with the standout result that gains concentrate on *rare* classes (e-bike-in-elevator is exactly a rare, hard class). The integrated **filtering** step is a stage-4 idea applied inline; worth borrowing. Demonstrates the "layout-cond + filter" template that G3/G4 would instantiate on the anchor.

## Links
- [[stage3-state-of-the-art]]
