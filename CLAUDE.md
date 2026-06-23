# CLAUDE.md

Operating rules for working in this repo. See `README.md` for the public overview.

## What this repo is

A **knowledge tree** for researching *diagnosis-driven generative data augmentation* for vision models. The tree (`docs/kg/`) is a byproduct; the real deliverable is **`docs/kg/GAPS.md`** — a shortlist of 2-3 research gaps that are (a) not already solved in the surveyed literature and (b) demonstrable on the **anchor task**: elevator CCTV detection of electric mopeds / e-bikes.

The work is driven by an implementation plan: `docs/superpowers/plans/2026-06-23-generative-augmentation-knowledge-tree.md` (Phases 0-5). Phase 0 (wide sweep) is complete; Phase 1 = stage1-diagnosis deep dive is next.

## The ingestion workflow (RUNBOOK)

All literature goes in one batch at a time, following `docs/kg/RUNBOOK.md`:

1. User names a target → 2. agent searches, returns a **candidate list (title + url), writes nothing** → 3. user picks → 4. agent fetches each pick and drafts `90-papers/authorYEAR-name.md` **from fetched text only** → 5. wire into concept nodes + `MAP.md`, append gaps to `GAPS.md` → 6. report found N / fetched M / unverified K → 7. validate, then commit.

## Hard rules (non-negotiable)

- **Validator gate, every batch:** `python3 docs/kg/tools/validate_kg.py` must exit 0 before committing. **Use `python3`** — default `python` here is 2.7.5.
- **Anti-hallucination:** no paper note without a real fetched `http(s)` url. If a source can't be fetched, do **not** write it from memory — substitute a fetchable equivalent or report it as unverified. Notes drafted from memory carry tag `unverified`.
- **Concept nodes** (`00/10/20/30`) must **never** `[[link]]` an `unverified`-tagged paper. The validator enforces this.
- **Paper-note frontmatter keys (exact):** `title, authors, year, url, loop-stage, tags`. `loop-stage` ∈ `foundations | landscape | stage1 | stage2 | stage3 | stage4 | anchor`.
- **Every number carries its source** (cite the paper + where: abstract / Table N). Don't invent numbers; if the abstract lacks them, say "to be pulled from the paper body."
- Filenames: `90-papers/authorYEAR-name.md`, kebab-case.

## Web-research conventions (learned the hard way)

- **arXiv:** fetch the `/abs/` page, **not** `/pdf/` — the PDF comes back as binary garble or exceeds the fetch size limit. `/abs/` gives clean title + authors + abstract.
- **MDPI (`www.mdpi.com`): returns HTTP 403 to WebFetch.** Don't retry it — substitute an arXiv / other fetchable source on the same topic.

## Repo conventions

- **Local-only, never commit/push:** `generate.py`, `batch_generate.py`, `gen_prom/`, `setup_env/` (Flux generation scripts). The repo is public; keep these untracked.
- `handoff.md` is volatile session state — untracked, never committed.
- Work happens on `master`; commit each batch directly. Commit-message prefix: `kg(phaseN): ...` or `kg(stageN): ...`.
- Commit/push only when the user asks.

## Where things live

- `docs/kg/MAP.md` — tree index (nested `[[wikilinks]]`); records the suspected weakest loop stage. Update every batch.
- `docs/kg/GAPS.md` — the deliverable; running candidate-gap list.
- `docs/kg/00-foundations/` `10-landscape/` `20-loop/` `30-anchor-task/` — concept nodes.
- `docs/kg/90-papers/` — one atomic note per paper.
- `docs/kg/_templates/` — `paper-note.md`, `concept-node.md`.
- `docs/kg/tools/validate_kg.py` + `test_validate_kg.py` — the gate (run tests with `python3 -m pytest`).
