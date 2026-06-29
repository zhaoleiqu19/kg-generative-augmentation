# One-Month Plan — Survey-to-Gap + Working MVP Pipeline — Design

**Date:** 2026-06-29
**Status:** Brainstorm approved, pending implementation plan
**Relation to prior specs:** Re-scopes `archive/2026-06-23-diagnosis-driven-augmentation-pipeline-design.md`
(now archived) for a **fixed one-month, no-novel-method** budget. The 4-module architecture
and data contracts from that spec are reused as-is; what changes is scope
(two parallel deliverables, off-the-shelf components only) and the explicit
**survey-driven component selection** step. The 2026-06-23 spec and other
pre-pivot material will be archived separately.

## 1. Goal & Scope

Within **one month**, ship **two independent deliverables**:

1. **Survey-to-gap** — a defensible literature survey that (a) names the
   research gap (the diagnosis→generation "bridge"), and (b) **selects the most
   suitable off-the-shelf components** (one diagnosis method + one generation
   model) for the pipeline.
2. **Working MVP pipeline** — a minimal end-to-end run that **closes the loop**
   (diagnose → spec → generate → filter → retrain → evaluate) once on a public
   detection task, assembled entirely from the components the survey selected.

**Hard constraint (decided):** **No novel methods, no new architectures, no
self-improved algorithms** — time does not allow research. We *design our own
pipeline* but *use others' validated tools as its parts*. Because the pipeline
must be usable, the survey must choose the **best-fit** existing components, not
arbitrary ones.

### Success criteria (Definition of Done)
- **Deliverable 1:** `alignment-gaps.md` states the gap; `demo-task-selection.md`
  records the chosen diagnosis method + generation model + rationale; inclusion
  criteria locked in `alignment-thesis.md`.
- **Deliverable 2:** the pipeline runs one full round end-to-end and emits a
  comparison `Report` (baseline vs augmented). **Up / flat / down all count as
  valid** — success = the loop closes and the result is interpretable, *not*
  that the metric must improve.
- Module boundaries hold: swapping a stage's component does not require changing
  other modules.

### Out of scope (YAGNI)
- No novel diagnosis/generation algorithms; no architecture design.
- No elevator data (none available); elevator stays as the "target, pending
  data" row in the generality map.
- No multi-round forced iteration in v1 (single round); no GUI/service (CLI).
- No large-scale multi-task empirical study.

### Coupling between the two deliverables
Loosely coupled with a **one-way dependency**: the survey's *component-selection*
output feeds the MVP; the survey's *gap-finding* output is fully independent.
The MVP does **not** claim to fill the gap — it is a working pipeline built from
the best available parts. The shared backbone is the **alignment lens**: the
"most suitable" diagnosis↔generation pair is the one whose diagnosis output
representation best aligns with the generation control interface (lightest
bridge). The same lens both *measures* the gap and *selects* the components.

## 2. MVP Architecture & Data Contracts

Four single-responsibility modules forming a loop; modules communicate **only**
through fixed data contracts, so any component is swappable without touching the
others.

```
   Real data (COCO subset) + a detector model
            │
  1. Diagnose   diagnose(model, data)        -> list[Slice]
            │  list[Slice]
  2. Spec       make_spec(slices, budget)     -> GenSpec
            │  GenSpec
  3. Generate   generate(spec)                -> SyntheticDataset
            │  SyntheticDataset
  4. CloseLoop  close_loop(model, real, synth)-> Report
            │   (filter -> accumulate real+synth -> retrain -> eval)
            ▼
       Report (baseline vs augmented metric + decision)

   Orchestrator: runs 1->2->3->4 for a single round in v1.
```

### Data contracts (the only coupling points)
| Type | Key fields | Producer → Consumer |
|---|---|---|
| `Slice` | `description` (human-readable, e.g. "small objects"), `members` (sample id list), `metric` (AP on the slice), `severity` | Diagnose → Spec |
| `GenSpec` | `items`: each = {target slice, generation conditions (free field: prompt/layout/region), count} | Spec → Generate |
| `SyntheticDataset` | `images` + `annotations` (same format as real, COCO json) | Generate → CloseLoop |
| `Report` | `baseline_metric`, `augmented_metric`, `per_slice_delta`, `iterate?` | CloseLoop → human/Orchestrator |

`Slice` uses a **dual representation** on purpose: a sample-id list (to *locate*
the failing images) plus a human-readable description (to *feed* the generator
as a prompt). This dual form is the simplest concrete instance of the
diagnosis→generation bridge.

### Component choices (resolved by the survey, not pre-locked)
- **Diagnose:** a real slice-discovery tool selected by the survey (candidates:
  HiBug2, GH-ESD, others surfaced in survey). **Spike first** (time-boxed); if
  none reproduce in the box, fall back to a **metric-based slicer** (per-size AP
  → worst slice) behind the same interface so the loop still closes.
- **Spec:** simple rules (slice description → prompt/layout conditions; counts
  allocated worst-slice-first).
- **Generate:** a generation model selected by the survey (candidates:
  GeoDiffusion, InstanceDiffusion [downloaded], SDXL-inpaint, ODGEN). **Not
  pre-locked.** All candidates are COCO-capable, so the demo task is robust to
  the choice.
- **CloseLoop:** detector self-agreement / CLIP-score filter → accumulate
  real+synth → retrain → evaluate on a synth-free eval set.

### Demo task (decided)
A small **COCO subset**; diagnose the classic **small-object** failure slice
(COCO already standardizes small/medium/large AP). Single-GPU feasible; lowest
generation risk.

## 3. Survey Track (two jobs)

### Job (a) — find the gap (near-complete, finish it)
- Write `50-alignment/alignment-gaps.md` (currently a stub): formalize the
  filled box-level survey verdict — both ends are mature and share per-instance
  box/mask/occlusion language, but no bridge turns a grounded, measured
  detection slice into a per-instance generation spec.
- Lock inclusion criteria (time window etc., marked TBD) in `alignment-thesis.md`.
- Optional: ingest 1–2 diagnosis candidates (e.g. Manifold-Compactness, CB-SLICE)
  via RUNBOOK into `90-papers/`.

### Job (b) — component selection (new comparison work)
Pick one diagnosis method + one generation model from off-the-shelf candidates,
judged by explicit criteria written into `40-pipeline/demo-task-selection.md`:

| Criterion | Diagnosis | Generation |
|---|---|---|
| Granularity | outputs per-instance, locatable slices | controllable at that granularity (layout/box/mask) |
| **Alignment (core)** | output can serve directly as a generation condition | control interface can directly consume the diagnosis output → lightest bridge |
| Detection-ready | slices carry sample ids + metric | emits images + annotations (COCO json) |
| Handles the failure mode | can slice small/occluded objects | can render small/occluded with correct annotations |
| **Reproducible / runnable locally** | repo runs (verified by spike) | weights in place, locally verified |

Outputs (new `40-pipeline/` dir): `generality-map.md` (detection sub-scenarios ×
method applicability × evidence; elevator included as the "target, pending
data" row) and `demo-task-selection.md` (chosen components + rationale).

## 4. Timeline (4 weeks, survey-first / Approach A)

| Week | Survey track | MVP track |
|---|---|---|
| **1** | Finish gap (`alignment-gaps.md`, lock criteria) → **bank deliverable 1**; run component selection (incl. diagnosis spike). | Rebase `feat/pipeline-skeleton` onto master; prepare COCO subset; fine-tune baseline detector + record baseline; start diagnosis spike. |
| **2** | Light polish; finalize `demo-task-selection.md`. | Diagnose worst slice → `make_spec` → generate targeted synthetic images+labels with the chosen generator. |
| **3** | — | CloseLoop: filter → accumulate real+synth → retrain → eval on synth-free set → `Report`. Run one full round. |
| **4** | Final read-through. | Analyze `per_slice_delta`; write up. **Buffer** for repro/compute slippage. Stretch: stronger diagnosis tool, or a 2nd round. |

The diagnosis spike and component selection sit in week 1 so the MVP build
(weeks 2–4) consumes a settled choice. If selection slips, start with the
highest-alignment pair that is confirmed runnable.

## 5. Validation, Testing, Error Handling, Risks

### Testing (layered, by contract)
- **Unit:** each module tested with fabricated contracts (feed a constructed
  `Slice`/`GenSpec`, assert output format + edge cases); no real model/generation.
- **Integration smoke test:** tiny data (~tens of images) runs all four modules
  once; asserts "end-to-end no error, `Report` produced" — CI-level gate.
- **Boundary check:** swap Diagnose for a dummy impl and still run end-to-end →
  proves decoupling.

### Validating usefulness (anti-self-deception)
- Fixed seed; same baseline + same eval set for baseline vs augmented.
- Report `per_slice_delta` + overall.
- Three red lines: (1) **eval set contains no synthetic images**; (2) focus on
  the **targeted slice's** delta, not a diluted overall average; (3) up/flat/down
  all recorded honestly — **down is a valid result**.

### Error handling
- Poor generation → CloseLoop filter catches it; if too few survive, **skip the
  round with a warning** rather than pollute training data.
- Retrain diverges/drops → `Report` records "down", `iterate?=false`; no forced
  extra rounds.
- Accumulation default: **real + synthetic accumulate, never replace real**
  (collapse avoidance; Gerstgrasser et al. 2024).

### Risks
| Risk | Mitigation |
|---|---|
| Diagnosis repo won't reproduce | time-boxed spike + metric-slicer fallback (loop still closes) |
| Chosen generator underperforms | Generate module is swappable; COCO task friendly to all candidates |
| Insufficient compute | small dataset + pretrained fine-tune + single round |
| Demo task hard to improve | improvement not required for success; "down" still a valid deliverable |
| Survey selection delays MVP start | selection time-boxed to week 1; if it slips, start with the highest-alignment confirmed-runnable pair |
| No elevator data | public set for v1; elevator stays as "target, pending data" row in generality-map |

## 6. Open Questions (resolved in plan / survey)
- Exact COCO subset size + baseline detector choice — decided at start of MVP build.
- Diagnosis tool (HiBug2 vs GH-ESD vs other) — decided by the spike.
- Generation model (GeoDiffusion vs InstanceDiffusion vs SDXL-inpaint vs ODGEN)
  — decided by component selection against the criteria table.
