---
title: "DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation"
authors: Nataniel Ruiz, Yuanzhen Li, Varun Jampani, Yael Pritch, Michael Rubinstein, Kfir Aberman
year: 2022
venue: arXiv (CVPR 2023)
url: https://arxiv.org/abs/2208.12242
loop-stage: stage3
tags: personalization, subject-driven, dreambooth, few-shot, prior-preservation, generation
---

## TL;DR
DreamBooth personalizes a text-to-image model from just 3–5 images of a specific subject, binding it to a unique token so the subject can be re-rendered in new scenes, poses, and lighting.

## Method
Fine-tune a pretrained T2I diffusion model with "a few images of a subject" (typically 3–5), a "unique identifier" token to represent it, and a "class-specific prior preservation loss" to keep the model's general class knowledge while learning the new subject (abstract, arXiv:2208.12242).

## Main claim + result
Enables synthesis of "the subject in diverse scenes, poses, views and lighting conditions that do not appear in the reference images." Demonstrated on recontextualization, text-guided view synthesis, and artistic rendering. Qualitative/foundational — no detection benchmark number (it's a generation method, not a detection study).

## Relevance to us
The personalization primitive for **rare, specific objects**: a particular e-bike/moped model can be learned from a handful of frames and then re-rendered in varied elevator conditions (lighting, pose, occlusion) that the real data lacks. Pairs with X-Paste composition or ODGEN conditioning to produce the exact hard cases a diagnosis demands (G4). Caveat: identity drift / overfitting on few shots; needs the prior-preservation loss + filtering.

## Links
- [[stage3-state-of-the-art]]
