# Stage 2 — Spec: State of the Art

> Spine stage 2: translate a diagnosis into a *generation specification* — what to synthesize (which examples, how many, under what conditions) to fix the diagnosed gap.

## What it is
The bridge between diagnosis (stage 1) and synthesis (stage 3). It has two halves:
- **Decision** — *which* examples to augment and *how many* (the targeting / selection problem).
- **Encoding** — expressing the target as conditions a generator can consume (prompt, layout, geometry, region).

## Why it matters
A good spec is what makes generation *targeted*, which is the only regime that reliably helps ([[does-synthetic-data-help]]); blanket generation is wasteful and can hurt. The spec also sets the synthetic-to-real ratio the diagnosis demanded.

## State of the art

### Decision: what / how much to generate
- [[huang2024-actgen-active-generation]] — use the model's **misclassified samples** as the signal; generate harder look-alikes; better results with far fewer images. The clearest diagnosis→spec link (classification).
- [[nguyen2025-tada-targeted-augmentation]] — augment only the **hard-to-learn subset** (~30–40%) → **up to +2.8%**, beating full-dataset augmentation; theory says targeting homogenizes feature-learning speed without amplifying noise. Quantitative case for "targeted > blanket."

### Encoding: spec format the generator can consume
- [[chen2023-geodiffusion-geometric-control]] — spec = **geometric/layout** conditions (bboxes, camera views) turned into prompts; first to show L2I diffusion data helps detectors. Defines the executable spec language for detection.
- [[zhu2025-recon-region-controllable]] — **region-controllable** generation made *faithful* via perception-feedback rectification + region-aligned cross-attention. State of the art for honoring a region spec (NeurIPS'25 spotlight).

## What's solved vs open
- **Solved:** for *classification*, the decision half is demonstrated — targeting the hard/misclassified subset beats blanket, with numbers (ActGen, TADA). For *detection*, the encoding half exists — layout/region conditions are an executable, beneficial spec format (GeoDiffusion, ReCon).
- **Open (the wedge):** **nobody connects the two for detection.** A diagnosed *detection* failure slice (stage 1; GH-ESD/HiBug2) → an automatic *layout/region* spec (GeoDiffusion/ReCon format) is essentially unaddressed. The selection criteria are all classification image-level (misclassified / not-learned-early), not object/slice-level. (→ GAPS G4)

## Our take
The pieces flank the gap on both sides: detection diagnosis is emerging (stage 1) and controllable detection generation is mature (encoding here). The unbuilt bridge — *auto-translate a grounded detection slice into a region/layout generation spec, with a principled count* — is the most "gap-shaped" opening in the whole loop, and it lands directly on the anchor.
