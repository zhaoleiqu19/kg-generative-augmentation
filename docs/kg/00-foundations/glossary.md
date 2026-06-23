# Glossary

## What it is
Key terms used across the knowledge tree for the diagnosis-driven synthetic augmentation loop project.

## Terms

**Synthetic data** — Training images (and their annotations) produced by a generative model, renderer, or copy-paste pipeline rather than captured from the real world. Cost ~47x lower per labeled image than human-annotated real images (Yang et al. 2023).

**Domain gap** — The distribution mismatch between synthetic training data and real-world test data, often manifesting as degraded detection accuracy when a model trained on generated images is evaluated on camera footage.

**Data-centric AI** — A methodology that prioritizes the quality and composition of the training dataset over model architecture changes as the primary lever for improving model performance.

**Diffusion model** — A class of generative model that learns to reverse a gradual noise-addition process; produces high-fidelity images from text prompts or geometric conditions, enabling layout-controlled synthetic data generation (e.g., GeoDiffusion).

**Copy-paste synthesis** — A synthetic data technique that extracts foreground objects from labeled source images and composites them onto diverse backgrounds, preserving tight bounding-box annotations with no additional labeling cost.

**Loop-stage** — A project-specific label (`foundations`, `landscape`, `stage1`–`stage4`, `anchor`) indicating where in the diagnosis-driven augmentation pipeline a note's content is most relevant.

## Why it matters
Shared vocabulary ensures consistent use of terms across paper notes, concept nodes, and experiment logs. Ambiguous terms (e.g., "augmentation" covering both classical transforms and generative synthesis) are distinguished here to prevent confusion in literature reviews and method comparisons.

## Key papers
- [[yang2023-ai-generated-images-data-source]]

## Open questions
- Where exactly is the domain gap largest for elevator e-bike detection (texture, lighting, viewpoint)?
- At what synthetic-to-real ratio does diminishing returns set in for detection mAP?

## Our take
Synthetic data is cost-effective and scalable; the main friction is closing the domain gap, which the diagnosis loop is designed to quantify and reduce systematically.
