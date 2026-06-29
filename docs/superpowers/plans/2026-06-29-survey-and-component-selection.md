# Survey-to-Gap & Component Selection — Implementation Plan (Plan 1 of 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** In Week 1, ship Deliverable 1 (a defensible survey-to-gap) and decide
the MVP's two off-the-shelf components (one diagnosis method + one generation
model), so the Week 2–4 MVP build (Plan 2) starts from a settled choice.

**Architecture:** This is research + documentation work, not application code.
The "test" gate is therefore **not pytest** — it is the KG validator
(`python3 docs/kg/tools/validate_kg.py` exits 0) plus, for the empirical spike
tasks, "the external repo actually runs and the outcome is recorded." All
literature additions follow the RUNBOOK (candidate list → user picks → fetch →
draft from fetched text only). Deliverable docs live in `docs/kg/50-alignment/`.

**Tech Stack:** Markdown (KG notes), `docs/kg/tools/validate_kg.py` (gate),
WebFetch (RUNBOOK literature), conda envs `geodiff` / `flux2` + local model
weights under `/data1/qushiduo/models/` (spikes), `python3` (default `python`
is 2.7.5 — never use it).

## Global Constraints

- **Validator gate, every commit touching `docs/kg/`:** `python3 docs/kg/tools/validate_kg.py` must exit 0 (prints `KG validation passed.`) before committing.
- **Anti-hallucination:** no paper note without a real fetched `http(s)` url; arXiv → fetch the `/abs/` page, never `/pdf/`. MDPI returns 403 (skip, substitute). Notes drafted from memory carry tag `unverified`; concept dirs `00/10/20/30` must never `[[link]]` an `unverified` paper (`50-alignment/` may).
- **Paper-note frontmatter keys (exact):** `title, authors, year, url, loop-stage, tags`. `loop-stage` ∈ `foundations | landscape | stage1 | stage2 | stage3 | stage4 | anchor`. Filenames `90-papers/authorYEAR-name.md`, kebab-case.
- **No literal `[[...]]` in prose/examples** — the validator treats any `[[x]]` as a wikilink. Write illustrative examples without double brackets.
- **Every number carries its source** (paper + abstract / Table N). If the abstract lacks it, write "to be pulled from the paper body."
- **Local-only, never commit:** `generate.py`, `batch_generate.py`, `gen_prom/`, `setup_env/`, `handoff.md`. External repos cloned for spikes live under `~/gen_tools/` (not in this repo).
- **HF downloads:** drop proxy + `HF_ENDPOINT=https://hf-mirror.com` + `HF_HUB_DISABLE_XET=1`; pip via `-i https://pypi.tuna.tsinghua.edu.cn/simple`; `git clone` from github still needs the proxy. (See memory `hf-download-recipe`.)
- **Placement decision:** selection docs go in `docs/kg/50-alignment/` (current-direction home per CLAUDE.md), not the "40-pipeline/" the spec mentioned.
- **Commit messages:** prefix `kg(50-alignment): ...`; end with the Co-Authored-By trailer. Commit only the intended doc files (never the local-only paths above).

---

### Task 1: Lock inclusion criteria in `alignment-thesis.md`

**Files:**
- Modify: `docs/kg/50-alignment/alignment-thesis.md` (the section currently marked 待定 / TBD)

**Interfaces:**
- Consumes: nothing.
- Produces: a settled "inclusion criteria" subsection that Tasks 2–8 cite when deciding what to survey and how to weight picks.

- [ ] **Step 1: Read the current thesis to find the TBD criteria block**

Run: `grep -n "待定\|TBD\|纳入\|inclusion" docs/kg/50-alignment/alignment-thesis.md`
Read the surrounding section so the new text matches the doc's voice and the 5 positioning axes already there.

- [ ] **Step 2: Replace the TBD block with concrete criteria**

Write a subsection stating these decisions (verbatim intent — adapt wording to the doc's bilingual style):
- **No hard time cutoff.** Weight picks by *reproducibility (code/weights available) → empirical validation → citation/adoption*, **not** pure recency.
- **Foundational papers are admitted as representation/taxonomy sources, not SOTA baselines** (e.g. TIDE, Hoiem-style error taxonomies define the *language* of detection errors; they are cited for vocabulary, not as methods to beat).
- **Scope = detection-first**; classification/other-task papers admitted only as adjacent evidence.
- **A paper enters via RUNBOOK** (real fetched url) before any view links it.

- [ ] **Step 3: Run the validator**

Run: `python3 docs/kg/tools/validate_kg.py`
Expected: `KG validation passed.` (exit 0)

- [ ] **Step 4: Commit**

```bash
git add docs/kg/50-alignment/alignment-thesis.md
git commit -m "kg(50-alignment): lock survey inclusion criteria (reproducibility-weighted, detection-first)"
```

---

### Task 2: Write `alignment-gaps.md` — the gap deliverable

**Files:**
- Modify: `docs/kg/50-alignment/alignment-gaps.md` (currently a stub)
- Read (sources, do not edit): `docs/kg/50-alignment/survey-diagnosis.md`, `survey-generation.md`, `representation-map.md`

**Interfaces:**
- Consumes: the box-level cross-verdict already filled in `representation-map.md` ("可交叉/gap").
- Produces: the formal gap statement (Deliverable 1's core), referenced by `demo-task-selection.md` (Task 5) as the selection rationale.

- [ ] **Step 1: Re-read the three source views**

Run: `sed -n '1,200p' docs/kg/50-alignment/representation-map.md` and likewise skim `survey-diagnosis.md`, `survey-generation.md`. Note every concrete claim + its `90-papers/` atom (citations must trace to real atoms — anti-hallucination).

- [ ] **Step 2: Write the gap doc with this structure**

Required sections (prose authored from the sources read in Step 1 — do not invent numbers):
1. **One-sentence gap:** both ends are mature and *share the per-instance box/mask/occlusion language*, yet no published method turns a **measured, grounded detection slice** (diagnosis output) into a **per-instance generation spec** (generator input) — the bridge is missing, not the endpoints.
2. **Evidence — diagnosis side:** what detection-granularity slice discovery produces today (cite atoms, e.g. GH-ESD, HiBug2, TIDE), and what representation it outputs.
3. **Evidence — generation side:** what controllable per-instance generation consumes today (cite atoms, e.g. GeoDiffusion, InstanceDiffusion), and the interface it expects.
4. **The seam:** why the two representations almost-but-don't align, with the closest near-neighbors (DetDiffusion, AUTHENTICATION) and exactly which axis each only partially covers.
5. **Relation to old G1–G4:** refine, do not overwrite, the historical gaps (reference `GAPS.md` by name in prose, no double brackets).

- [ ] **Step 3: Cross-link**

Add `[[wikilinks]]` only to atoms that actually exist in `90-papers/` (verify each stem resolves). Do not link any `unverified`-tagged atom from a concept dir — this file is in `50-alignment/`, so links are allowed, but every stem must still resolve.

- [ ] **Step 4: Run the validator**

Run: `python3 docs/kg/tools/validate_kg.py`
Expected: `KG validation passed.` (exit 0). If it reports a broken link, fix the stem (typo or missing atom) — do not delete the gate.

- [ ] **Step 5: Commit**

```bash
git add docs/kg/50-alignment/alignment-gaps.md
git commit -m "kg(50-alignment): write alignment-gaps — diagnosis->generation bridge is the seam"
```

---

### Task 3 (optional): Ingest 1–2 diagnosis candidates via RUNBOOK

Skip if Task 2 already cites enough diagnosis-side atoms. Do this only to strengthen the diagnosis evidence (candidates noted in the spec: Manifold-Compactness `2501.19032`, CB-SLICE `2605.29836`).

**Files:**
- Create: `docs/kg/90-papers/authorYEAR-name.md` (one per accepted paper, kebab-case)
- Modify: `docs/kg/MAP.md` (add atom to the 90-papers list), `docs/kg/50-alignment/survey-diagnosis.md` (link the new atom in the right row)

**Interfaces:**
- Consumes: inclusion criteria (Task 1).
- Produces: new `90-papers/` atoms that `survey-diagnosis.md` and `alignment-gaps.md` may link.

- [ ] **Step 1: Search + present a candidate list (write nothing yet)**

Per RUNBOOK: search, return a candidate list of **title + url only** to the user. Wait for the user to pick.

- [ ] **Step 2: Fetch each pick from its `/abs/` page**

Run WebFetch on the arXiv `/abs/` url (never `/pdf/`). If a source can't be fetched, do not write it from memory — report it unverified and substitute a fetchable equivalent.

- [ ] **Step 3: Draft the atom from fetched text only**

Use `docs/kg/_templates/paper-note.md`. Frontmatter keys exactly `title, authors, year, url, loop-stage, tags`; `loop-stage: stage1` for diagnosis. Every number cites abstract / Table N or says "to be pulled from the paper body."

- [ ] **Step 4: Wire into MAP + survey**

Add the `[[stem]]` to `MAP.md`'s 90-papers list and to the matching row in `survey-diagnosis.md`.

- [ ] **Step 5: Validate + report + commit**

Run: `python3 docs/kg/tools/validate_kg.py` → `KG validation passed.`
Report found N / fetched M / unverified K.
```bash
git add docs/kg/90-papers/ docs/kg/MAP.md docs/kg/50-alignment/survey-diagnosis.md
git commit -m "kg(50-alignment): ingest diagnosis candidate(s) via RUNBOOK"
```

---

### Task 4: Write `generality-map.md` — where this method applies

**Files:**
- Create: `docs/kg/50-alignment/generality-map.md`
- Modify: `docs/kg/MAP.md` (add a link to the new doc under the 50-alignment area)

**Interfaces:**
- Consumes: the surveys + `alignment-gaps.md`.
- Produces: the detection-sub-scenario applicability table that frames *why* the chosen demo task is representative; referenced by `demo-task-selection.md`.

- [ ] **Step 1: Build the applicability table**

A table with rows = detection sub-scenarios (general COCO-style, small-object, occlusion/crowding, long-tail/rare-class, domain-shift, **elevator-CCTV e-bike**) and columns = (failure mode it stresses · does diagnosis-driven aug have reported gains here? cite atom · which generator covers it · evidence strength). Fill cells only from existing `90-papers/` atoms (cite each); leave the **elevator row** explicitly as "target, pending data."

- [ ] **Step 2: Add a one-paragraph read-off**

State which sub-scenario the MVP should demo (small-object on COCO) and why it is the lowest-risk representative row.

- [ ] **Step 3: Link from MAP + validate**

Add the doc to `MAP.md`. Run `python3 docs/kg/tools/validate_kg.py` → `KG validation passed.`

- [ ] **Step 4: Commit**

```bash
git add docs/kg/50-alignment/generality-map.md docs/kg/MAP.md
git commit -m "kg(50-alignment): generality-map — detection sub-scenarios x applicability"
```

---

### Task 5: Write selection criteria + candidate inventory in `demo-task-selection.md`

**Files:**
- Create: `docs/kg/50-alignment/decisions/demo-task-selection.md`

**Interfaces:**
- Consumes: `alignment-gaps.md` (the alignment criterion), `generality-map.md` (the demo task).
- Produces: the criteria table + candidate inventory that Tasks 6–8 fill with a decision; the final output Plan 2 consumes.

- [ ] **Step 1: Record the fixed decisions**

Write: demo task = small COCO subset, small-object slice (from Task 4); success = loop closes (up/flat/down all valid); no novel methods.

- [ ] **Step 2: Write the selection-criteria table (verbatim from the spec)**

| Criterion | Diagnosis | Generation |
|---|---|---|
| Granularity | per-instance, locatable slices | controllable at that granularity (layout/box/mask) |
| **Alignment (core)** | output usable directly as a generation condition | control interface consumes the diagnosis output → lightest bridge |
| Detection-ready | slices carry sample ids + metric | emits images + COCO-json annotations |
| Handles failure mode | can slice small/occluded | can render small/occluded with correct annotations |
| **Reproducible / runnable** | repo runs (verified by spike) | weights in place, locally verified |

- [ ] **Step 3: Write the candidate inventory with current known status**

- Diagnosis candidates: **HiBug2** (`90-papers/chen2025-hibug2-error-slice-discovery.md`), **GH-ESD** (`90-papers/zhang2026-gh-esd-instance-slice-discovery.md`) — both *not yet spiked*; status filled by Task 6.
- Generation candidates with current status (from memory `gen-model-toolkit`): **GeoDiffusion** COCO-512 — *verified working* (`geodiff` env); **SDXL-Inpaint** — *verified working* (`flux2` env); **InstanceDiffusion** — *downloaded, NOT built*; **ODGEN** — *not set up*. Status finalized by Task 7.

- [ ] **Step 4: Validate + commit**

Run: `python3 docs/kg/tools/validate_kg.py` → `KG validation passed.`
```bash
git add docs/kg/50-alignment/decisions/demo-task-selection.md
git commit -m "kg(50-alignment): demo-task-selection — criteria + candidate inventory"
```

---

### Task 6: Diagnosis spike (time-boxed) → record decision

**Files:**
- Modify: `docs/kg/50-alignment/decisions/demo-task-selection.md` (fill the diagnosis status + decision)
- External (not committed): clone repos under `~/gen_tools/`

**Interfaces:**
- Consumes: candidate list (Task 5).
- Produces: the **diagnosis decision** — a runnable real tool, or "fallback to metric-based slicer" — consumed by Plan 2's Diagnose task.

- [ ] **Step 1: Set a hard time-box**

Record a time-box (recommended **2–3 working days total** across both repos) in the doc before starting. When it expires, stop and take the fallback.

- [ ] **Step 2: Attempt HiBug2, then GH-ESD**

For each: `git clone` (proxy on for github), create/activate its env, run the repo's own example/quickstart on its sample data. Record per repo: cloned? deps install? example runs? output is a per-instance slice with sample ids? (yes/no + the blocking error if no).

- [ ] **Step 3: Decide**

If exactly one runs → choose it. If both run → choose the one whose output better matches the alignment criterion (slice description + sample ids closest to a generation condition). If neither runs within the box → **decision = metric-based slicer fallback** (per-size AP → worst slice; built in Plan 2). Write the decision + evidence (what ran / what blocked) into `demo-task-selection.md`.

- [ ] **Step 4: Validate + commit**

Run: `python3 docs/kg/tools/validate_kg.py` → `KG validation passed.`
```bash
git add docs/kg/50-alignment/decisions/demo-task-selection.md
git commit -m "kg(50-alignment): diagnosis spike outcome + decision"
```

---

### Task 7: Generation selection → record decision

**Files:**
- Modify: `docs/kg/50-alignment/decisions/demo-task-selection.md` (fill generation status + decision)
- Reference: `docs/kg/50-alignment/decisions/gen-toolkit.md` (existing verified-toolkit notes)

**Interfaces:**
- Consumes: candidate inventory (Task 5), criteria table (Task 5).
- Produces: the **generation decision** (one model) consumed by Plan 2's Generate task.

- [ ] **Step 1: Score each candidate against the criteria table**

For the COCO small-object demo, judge each candidate on the five criteria. Key known facts to weigh (from `gen-toolkit.md` + memory): GeoDiffusion = COCO-layout-controlled, verified, but SD1.5-based (weak on foregrounded faces; fine for small background objects); SDXL-Inpaint = region edits on real images, verified; InstanceDiffusion = per-instance mask/point control (closest alignment) **but not built**; ODGEN = detection-oriented but not set up.

- [ ] **Step 2: Decide, with the alignment criterion as tie-breaker**

Pick the model that best satisfies *detection-ready + handles small objects + runnable now*, using **alignment** (does its control interface directly consume the diagnosis output from Task 6?) as the tie-breaker. If the top choice on alignment (e.g. InstanceDiffusion) is not built, record either (a) a small build-probe as a Plan 2 prerequisite, or (b) fall back to a verified model (GeoDiffusion/SDXL-Inpaint). State the call explicitly.

- [ ] **Step 3: Record decision + rationale in the doc, validate, commit**

Run: `python3 docs/kg/tools/validate_kg.py` → `KG validation passed.`
```bash
git add docs/kg/50-alignment/decisions/demo-task-selection.md
git commit -m "kg(50-alignment): generation selection + decision"
```

---

### Task 8: Finalize selection + close Week 1

**Files:**
- Modify: `docs/kg/50-alignment/decisions/demo-task-selection.md` (final summary block), `docs/kg/MAP.md` (ensure new docs are indexed), `docs/kg/50-alignment/README.md` (mark statuses done)

**Interfaces:**
- Consumes: all prior tasks.
- Produces: the settled inputs for Plan 2 (chosen diagnosis impl + chosen generator + demo task), and the banked Deliverable 1.

- [ ] **Step 1: Add a "Decision summary" block at the top of `demo-task-selection.md`**

Three lines an outside reader can act on: chosen diagnosis impl (real tool name **or** "metric-based slicer fallback"), chosen generator (+ "needs build probe" flag if any), demo task + dataset subset.

- [ ] **Step 2: Update the 50-alignment README file table**

Flip `alignment-gaps.md`, `generality-map.md`, `demo-task-selection.md` statuses from stub/待填 to done; ensure `MAP.md` links all three.

- [ ] **Step 3: Final validate**

Run: `python3 docs/kg/tools/validate_kg.py`
Expected: `KG validation passed.` (exit 0)

- [ ] **Step 4: Commit + report**

```bash
git add docs/kg/50-alignment/ docs/kg/MAP.md
git commit -m "kg(50-alignment): finalize Week-1 survey + component selection"
```
Report to the user: Deliverable 1 done (gap + criteria locked); chosen diagnosis impl + generator; what Plan 2 will build on.

---

## Self-Review

**Spec coverage** (against `docs/superpowers/specs/2026-06-29-one-month-survey-and-mvp-design.md` §3 + §1 Deliverable 1):
- Find gap → Tasks 1 (criteria), 2 (gap doc), 3 (optional atoms). ✓
- Component selection → Tasks 4 (generality-map), 5 (criteria+inventory), 6 (diagnosis spike), 7 (generation), 8 (finalize). ✓
- Alignment lens as selection criterion → encoded in Tasks 5/6/7 tie-breakers. ✓
- Deliverable 1 banked in Week 1 → Tasks 1–2 are front-loaded and independently committable. ✓

**Placeholder scan:** Empirical/research tasks (3, 6, 7) intentionally end in a *recorded decision* gated by the validator rather than fabricated code/commands — this is the honest gate for research work, not a placeholder. Prose content for Tasks 1/2/4/5 is specified by required sections + sourced-from-atoms rule (anti-hallucination), not pre-written fiction. No "TBD/handle edge cases" left.

**Consistency:** Output file paths are stable across tasks (`50-alignment/decisions/demo-task-selection.md` written in T5, appended in T6/T7/T8). Candidate names and atom stems match memory/handoff (HiBug2 = `chen2025-...`, GH-ESD = `zhang2026-...`). Decision artifacts (diagnosis impl, generator, demo task) are exactly the three inputs Plan 2 needs.
