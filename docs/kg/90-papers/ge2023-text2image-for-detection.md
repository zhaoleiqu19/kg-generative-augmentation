---
title: "Beyond Generation: Harnessing Text to Image Models for Object Detection and Segmentation"
authors: Yunhao Ge, Jiashu Xu, Brian Nlong Zhao, Neel Joshi, Laurent Itti, Vibhav Vineet
year: 2023
venue: arXiv
url: https://arxiv.org/abs/2309.05956
loop-stage: stage3
tags: text-to-image, object-detection, segmentation, synthetic-data, helps, copy-paste
---

## TL;DR
A text-to-image pipeline that generates foregrounds and backgrounds separately, then cut-and-pastes them with masks, producing detection/segmentation training data good enough to rival real-data training.

## Method
Three steps: (1) foreground generation — class-name prompts produce isolated objects; (2) background generation — real-image captions become diverse context scenes; (3) composition — cut-and-paste foregrounds onto backgrounds, auto-deriving bounding boxes and segmentation masks (no manual labeling). Evaluated on Pascal VOC and COCO.

## Main claim + result
"Detectors trained solely on synthetic data produced by our method achieve performance comparable to those trained on real data" (abstract, arXiv:2309.05956); synthetic+real combinations do better still. The abstract gives no specific mAP/AP numbers — to be pulled from the paper's tables in a follow-up read. Code: github.com/gyhandy/Text2Image-for-Detection.

## Relevance to us
The "synthetic HELPS for **detection**" anchor of the helps-vs-hurts node, and a concrete recipe close to our pipeline (controllable foreground + diverse background + automatic boxes). The compositional/cut-and-paste route is directly portable to generating elevator e-bike instances against varied elevator interiors.

## Links
- [[does-synthetic-data-help]]
