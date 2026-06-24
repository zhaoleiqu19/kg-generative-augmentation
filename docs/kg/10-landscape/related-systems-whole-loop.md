# Related Systems — Whole-Loop & Closest Neighbors

## What it is
A prior-art node for the *systems* that come closest to the project's full diagnose→generate→filter→retrain loop, so we can name precisely what is already built and where the open seam is. Where the loop spine (`20-loop/`) maps the field stage-by-stage, this node maps the **end-to-end neighbors** that combine several stages, and checks each against the four things that make detection the hard case: free labels, per-object diagnosis, slice-wise metric, cheap retrain.

## Why it matters
The deliverable is `GAPS.md`. Its credibility rests on showing the closest existing systems and where each falls short of *diagnosis-driven, real-image, occlusion-capable, detection* augmentation. This node is the evidence that the seam is genuinely open rather than already filled by a neighbor we missed.

## Key papers

### Closest whole-loop neighbors (detection / generation steered by some signal)
- [[yurt2025-ltda-drive-longtail]] — generate→insert→**LLM-filter** for long-tail 3D detection; **+34.75% rare-class** on KITTI. Missing piece: steered by *blanket long-tail*, not a measured per-slice diagnosis.
- [[hong2024-galot-generative-active-learning]] — explicit **AL-criterion → generate** closed loop; **classification**, fully synthetic, text-pseudo-labels (no boxes).
- [[ouyang2025-safefix-model-repair]] — diagnose→targeted-gen→VLM-filter→retrain; the published loop template, but **classification**-centric.
- [[chegini2023-clip-diffusion-failure-mitigation]] — diagnose→diffusion-generate, ~21% on hard sub-populations; **classification**.

### Placement / spec neighbors (the "where", relevant to G4)
- [[petersen2025-scene-aware-location]] — learned **probabilistic location model** + inpainting; **+1.4 mAP** (2.8× a random-placement baseline). Placement from a scene prior, not from a diagnosis.
- [[girella2024-diag-indistribution-defect]] — **human marks the region**, training-free in-distribution defect gen; **+18–28% AP** on KSDD2. The manual version of the slice→spec marker.

### Engines already in the tree (steered-by-given-layout detection generation)
- [[zhu2024-odgen-detection-generation]] · [[chen2023-geodiffusion-geometric-control]] · [[zhu2025-recon-region-controllable]] · [[tang2024-aerogen-remote-sensing-generation]] · [[zhao2023-xpaste-copy-paste]]

### Calibrating skeptics
- [[voetman2023-big-data-myth-detection]] — fully-synthetic detection reaches *near-parity* (AP dev 0.09–0.12) on an easy task — replacement, not amplifier.

## Open questions
- Does any neighbor steer generation from a **grounded, per-object detection diagnosis** (vs. blanket tail / generic AL uncertainty / a human marker)? — none found.
- Does any produce **correct boxes under occlusion** on **real images**? ODGEN/Scene-Aware get closest (object-wise / inpaint-in-context); GALOT/Big-Data-Myth sidestep boxes (synthetic-only / manual).
- Which neighbor's **filter** (LLM agent, VLM, CLIP) transfers to a detection verifier with a defined safe ratio/stop (→ G3)?

## Our take
The loop exists *in pieces*: long-tail detection gen with an LLM filter (LTDA-Drive), a true AL→generate closed loop (GALOT), scene-aware placement + inpainting (Scene-Aware), human-region in-distribution gen (DIAG), and a classification repair template (SafeFix). **None couples a grounded per-object detection diagnosis to a controllable, occlusion-capable, real-image generator with a defined verifier.** That intersection is the seam — exactly the sharpened [[generative-augmentation-landscape]] G1 (whole loop for detection) feeding on G2/G4 (diagnosis→spec) and G3 (safe ratio/filter).
