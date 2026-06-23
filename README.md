# kg-generative-augmentation

A knowledge tree for researching **diagnosis-driven generative data augmentation** for vision models: don't augment blindly — first find where a dataset/model fails, then synthesize exactly those cases, then verify the gap closed.

The tree is a byproduct; the real deliverable is [`docs/kg/GAPS.md`](docs/kg/GAPS.md) — a shortlist of research gaps that are (a) not already solved in the surveyed literature and (b) demonstrable on a concrete anchor task (elevator CCTV detection of electric mopeds/e-bikes).

## Layout

- `docs/kg/` — the Obsidian-compatible Markdown note-web
  - `MAP.md` — the tree as nested `[[wikilinks]]`
  - `GAPS.md` — running list of candidate research gaps
  - `RUNBOOK.md` — the per-batch ingestion procedure
  - `00-foundations/` `10-landscape/` `20-loop/` `30-anchor-task/` — concept nodes
  - `90-papers/` — one atomic note per paper
  - `tools/validate_kg.py` — the validator / test gate
- `docs/superpowers/specs/` — design doc
- `docs/superpowers/plans/` — implementation plan

## Validate

The validator enforces frontmatter completeness, link integrity, and the
anti-hallucination guardrail (concept nodes may not cite `unverified` papers):

```bash
python3 docs/kg/tools/validate_kg.py
cd docs/kg/tools && python3 -m pytest test_validate_kg.py -q
```
