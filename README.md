# kg-generative-augmentation

A research workspace on **diagnosis-driven generative data augmentation** for vision models: don't augment blindly — first find where a model fails, then synthesize exactly those cases, then retrain and verify the gap closed.

**Current plan — two steps:** (1) a **literature survey** of the diagnosis + generative-augmentation field, to establish what's achievable today; (2) a **pluggable tool** that wires existing components into a *detect → generate → train-augment* pipeline to measurably improve a detection model. The knowledge tree (`docs/kg/`) + the per-paper atoms (`90-papers/`) are the survey substrate; the **diagnosis↔generation alignment** thesis (`docs/kg/50-alignment/`) is the theory backbone and the tool's plugin interface.

## Layout

- `docs/kg/` — the Obsidian-compatible Markdown note-web
  - `MAP.md` — the tree as nested `[[wikilinks]]`
  - `GAPS.md` — running list of candidate research gaps
  - `RUNBOOK.md` — the per-batch ingestion procedure
  - `00-foundations/` `10-landscape/` `20-loop/` — Phase 0–4 concept nodes (`30-anchor-task/` archived to `_archive/`)
  - `90-papers/` — one atomic note per paper (single source of truth, shared by all views)
  - `50-alignment/` — current direction: the diagnosis↔generation *alignment* thesis (new views that reference the `90-papers/` atoms, never copy them)
  - `tools/validate_kg.py` — the validator / test gate
- `docs/zh/` — Chinese translation of the repo (showcase; English originals are authoritative)
- `docs/superpowers/specs/` — design doc
- `docs/superpowers/plans/` — implementation plan

## Validate

The validator enforces frontmatter completeness, link integrity, and the
anti-hallucination guardrail (concept nodes may not cite `unverified` papers):

```bash
python3 docs/kg/tools/validate_kg.py
cd docs/kg/tools && python3 -m pytest test_validate_kg.py -q
```
