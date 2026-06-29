# Diagnosis-Driven Generative Augmentation Pipeline — Design

**Date:** 2026-06-23
**Status:** Approved (brainstorm), pending implementation plan
**Supersedes:** the original Phase 5 idea (anchor-only gap shortlist) in
`docs/superpowers/plans/2026-06-23-generative-augmentation-knowledge-tree.md`.

## 1. Goal & Scope

Build a **diagnosis-driven generative data-augmentation pipeline**: given a
(vision model, task, dataset), automatically **diagnose** where the data is
weak, **generate** targeted augmentation data, **filter + retrain**, and
**measure** the change. Prove it on one easy public detection task as a
vertical slice, but design module interfaces so tasks and per-stage methods can
be swapped later. Elevator-CCTV e-bike detection remains the eventual target,
not the first demonstration.

This is **not a pivot** from prior work: the `20-loop/` four stages
(diagnose → spec → synthesize → close-loop) are exactly this pipeline; the
`90-papers/` survey is the "how others do each step" library we borrow from.
What changed is a clarification: the elevator task becomes the *first intended
application*, and "**which (vision model, task) pairs are amenable to this
method**" becomes an explicit, detection-first survey axis.

**Approach (decided):** Approach A "vertical slice" with Approach B "module
interface boundaries" — build a minimal end-to-end run for one demo task, but
define clean, swappable module contracts from day one.

### Deliverables (this round)
1. Survey wrap-up: a **detection-first generality map** + a chosen **public
   demo task** (model + task + dataset) + a chosen off-the-shelf component for
   each of the four stages.
2. A **minimal end-to-end pipeline** (four modules wired by the contracts).
3. A **result**: did the metric improve on the demo task, and why.

### Success criteria (Definition of Done)
- Pipeline runs one full round end-to-end (diagnose → spec → generate →
  filter → retrain → evaluate) and emits a comparison report.
- Reports **baseline vs augmented** metric on the demo task. **Up / flat / down
  all count as valid** — success = the loop closes and the result is
  interpretable, not that it must improve.
- Module boundaries hold: swapping the task or one stage's method does not
  require changing other modules.

### Out of scope (YAGNI)
- No support for all vision tasks at once (detection-first; others = adjacent
  evidence only).
- No novel diagnosis/generation algorithms — reuse published, validated ones.
- First version uses **no elevator data** (none available); no large-scale
  multi-task empirical study (that is later generality validation).
- No GUI/service; a CLI run is sufficient.

## 2. Module Architecture & Data Contracts

Four modules = the four loop stages, each single-responsibility and
communicating only through data contracts; internal implementations are
swappable.

```
            Real (model, labeled data)
                     │
   1. Diagnose   diagnose(model, dataset) -> list[Slice]
                     │  list[Slice]
   2. Spec       make_spec(slices, budget) -> GenSpec
                     │  GenSpec
   3. Generate   generate(spec) -> SyntheticDataset
                     │  SyntheticDataset
   4. CloseLoop  close_loop(model, real, synth) -> Report
                     │  (filter → accumulate real+synth → retrain → eval)
                     ▼
              Report (baseline vs augmented + decision)

   Orchestrator: runs 1→2→3→4, manages rounds + stopping criterion.
```

### Data contracts (the only coupling points)
| Type | Key fields | Producer → Consumer |
|---|---|---|
| `Slice` | `description` (human-readable, e.g. "small + occluded"), `members` (sample id list), `metric` (AP/acc on the slice), `severity` | Diagnose → Spec |
| `GenSpec` | `items`: each = {target slice, generation conditions (free field: prompt/layout/region), count} | Spec → Generate |
| `SyntheticDataset` | `images` + `annotations` (same format as the real set, e.g. COCO json) | Generate → CloseLoop |
| `Report` | `baseline_metric`, `augmented_metric`, `per_slice_delta`, `iterate?` | CloseLoop → human/Orchestrator |

### Interface principles (the B boundaries)
- Each module is a replaceable implementation that only honors the contracts
  above (e.g. `Diagnose` = HiBug2 impl or GH-ESD impl).
- **Swapping task** touches only data loading + the eval metric (detection =
  mAP / size-specific AP; classification = acc); module code is unchanged.
- **Swapping a method** changes only that one module's implementation; contracts
  unchanged — which is why a vertical slice can still validate the boundaries.
- `Slice` uses a dual representation: **sample-id list + human-readable
  description** (locate samples *and* feed a prompt).
- `GenSpec` generation conditions are a **free field** (prompt/layout/region all
  fit), not a rigid schema, in the first version.

### Decided first-version components (final choice from survey)
- **Diagnose:** HiBug2 or GH-ESD (detection-granularity slicing).
- **Spec:** simple rules (slice description → prompt/layout conditions; counts
  set TADA-style on the worst slice).
- **Generate:** ODGEN *or* DreamBooth + X-Paste (chosen with the demo task and
  the Flux capability probe).
- **CloseLoop:** CLIP / detector self-agreement filter + accumulate real+synth +
  retrain + evaluate.

## 3. Vertical Slice Realization

### Step A — survey selects the demo task
Targeted (not broad) literature/dataset search against a selection checklist:

| Criterion | Why |
|---|---|
| Public dataset, ready to use, small enough for single-GPU training | resolves "no data" + caps compute |
| Detection task with clear, diagnosable failure modes (small / occluded / long-tail) | gives Diagnose something to slice |
| Someone has reported generative-augmentation gains on such a task | borrow others' conclusions, avoid known-dead scenarios |
| Generation coverable by an off-the-shelf component (ODGEN or DreamBooth+X-Paste) | no self-built generation |

Outputs (new `40-pipeline/` dir): **`generality-map.md`** (detection
sub-scenarios × method applicability × evidence; elevator included as the
"target, pending data" row) and **`demo-task-selection.md`** (chosen
model+task+dataset + the component choice per module + rationale).

### Step B — run the vertical slice (one round)
1. Fine-tune a baseline detector from **pretrained weights** on the public set →
   record baseline metric.
2. `diagnose` → a few failure slices (e.g. "small objects, lowest AP").
3. `make_spec` → conditions + count for the worst slice.
4. `generate` → synthetic images + annotations.
5. `close_loop` → filter → accumulate real+synth → retrain → evaluate → `Report`.
6. Read `per_slice_delta`: did the targeted slice / overall metric move.

**First version runs a single round** (no forced multi-round iteration) as the
minimal validation. **The first concrete action is a Flux capability probe**
(can it control layout / personalize an object?), written into
`demo-task-selection.md`, since it decides who fills Generate.

### Step C — integration with existing work
- This spec replaces the old "anchor-only" Phase 5 idea.
- writing-plans then produces the implementation plan (survey selection → build
  four modules → run vertical slice → report).
- `90-papers/` + `stage*-state-of-the-art.md` are the component-choice evidence
  base; GAPS **G1** (end-to-end detection loop) and **G4** (slice→spec bridge)
  are exactly what the vertical slice hands-on validates.

## 4. Validation, Testing, Error Handling, Risks

### Testing (layered, by contract)
- **Unit:** each module tested with fabricated contracts (feed constructed
  `Slice`/`GenSpec`, assert output format + edge cases); no real model/generation.
- **Integration smoke test:** tiny data (~tens of images) runs the full four
  modules once; asserts "end-to-end no error, `Report` produced", not gains —
  CI-level gate.
- **Boundary check:** swap Diagnose for a dummy impl and still run end-to-end →
  proves decoupling.

### Validating "usefulness" (scientific rigor)
- Fixed random seed; same baseline + same eval set.
- Compare baseline vs augmented; report `per_slice_delta` + overall.
- Anti-self-deception: **eval set contains no synthetic images**; focus on the
  targeted slice's delta, not a diluted overall average.

### Error handling (pipeline robustness)
- Poor generation → CloseLoop filter (CLIP / detector self-agreement) catches it;
  if too few survive, **skip the round with a warning** rather than pollute the
  training set.
- Retrain diverges / drops → `Report` records "down", `iterate?=false`; no forced
  extra rounds.
- Accumulation default: **real + synthetic accumulate, never replace real**
  (collapse avoidance; Gerstgrasser et al. 2024).

### Risk mitigations
| Risk | Mitigation |
|---|---|
| No elevator data | vertical slice uses a public set; elevator stays in generality-map as the target row, pending data |
| Flux capability unknown | Generate module is swappable; fall back to ODGEN / Stable Diffusion + X-Paste; run a Flux capability probe first |
| Insufficient compute | small dataset + pretrained fine-tune + single-round start |
| Wrong demo task (inherently hard to improve) | selection checklist requires "someone reported gains," borrowing others' conclusions |

## 5. Open Questions (resolved in plan / survey)
- Exact demo task + dataset — decided in Step A.
- ODGEN vs DreamBooth+X-Paste for Generate — decided after the Flux probe.
- Diagnose impl (HiBug2 vs GH-ESD) — decided by which is reproducible/available.
