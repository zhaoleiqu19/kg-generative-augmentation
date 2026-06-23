# Stage 3 — Synthesis: State of the Art

> Spine stage 3: actually generate the spec'd images (and annotations). The most *mature* stage — a rich, detection-ready method menu exists. The job here is to pick the right tool, not invent one.

## What it is
The generation toolbox, in four families:
1. **Layout/box-conditional generation** — diffusion conditioned on bboxes/geometry; annotations come for free.
2. **Composition (copy-paste)** — generate/crop isolated objects, filter, paste onto backgrounds with masks.
3. **Personalization** — learn a specific rare subject from few images, re-render in new conditions.
4. **General diffusion augmentation** — semantic edits / class-conditional sampling (mostly classification).

## Why it matters
This is where the elevator/e-bike images get made. Method choice controls fidelity (a proven "helps" lever, [[azizi2023-synthetic-data-improves-imagenet]]) and how well the **small/occluded** domain gap closes (→ G3).

## State of the art

### Layout/box-conditional (detection)
- [[zhu2024-odgen-detection-generation]] — object-wise conditioning (visual patch + per-object text); handles **multi-class + occlusion**; **+25.3% mAP** domain-specific, +5.6% COCO. Strongest fit for the anchor.
- [[chen2023-geodiffusion-geometric-control]] — geometry/bbox → prompt; first L2I diffusion shown to help detectors; 4× faster training.
- [[zhu2025-recon-region-controllable]] — region-controllable made *faithful* via perception-feedback rectification + region-aligned cross-attention (NeurIPS'25 spotlight).
- [[tang2024-aerogen-remote-sensing-generation]] — small-object (remote sensing), horizontal+rotated boxes, **inline filter**, **rare-class +12.6–17.8%**.

### Composition (copy-paste)
- [[zhao2023-xpaste-copy-paste]] — SD-generated/crawled objects + CLIP filter + paste; **+6.8 box AP on long-tail** (LVIS).
- [[ge2023-text2image-for-detection]] — foreground+background+cut-paste with auto boxes/masks.

### Personalization
- [[ruiz2022-dreambooth-subject-driven]] — learn a specific e-bike model from 3–5 images, re-render in new lighting/pose/occlusion.

### General / fidelity
- [[alimisis2024-diffusion-augmentation-review]] — method+metric taxonomy. · [[azizi2023-synthetic-data-improves-imagenet]] — fidelity raises downstream accuracy. · [[yang2023-ai-generated-images-data-source]] — families + 47× cost advantage.

## What's solved vs open
- **Solved:** detection-ready generation is mature. Two strong, complementary recipes for the anchor: (a) **ODGEN-style object-wise layout generation** (occlusion-aware, big mAP), and (b) **DreamBooth-personalized object → CLIP-filtered copy-paste** (rare-class, low-risk). Rare/long-tail gains are consistent (ODGEN, AeroGen, X-Paste) — encouraging for the rare "e-bike-in-elevator" class.
- **Open:** which closes the **small/occluded** gap best is unmeasured for our regime (→ G3); annotation tightness for tiny objects is unaddressed; and crucially these all assume the *spec/layout is given* — none derive it from a diagnosis (→ G4).

## Our take
Stage 3 is not the bottleneck — the menu is rich and the numbers are strong, with ODGEN and DreamBooth+X-Paste as the two front-runner pipelines for the elevator anchor. The leverage is upstream (diagnosis → spec, G2/G4) and in measuring the small-object regime (G3); stage 3 supplies the engine those gaps would drive.
