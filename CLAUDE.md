# CLAUDE.md

Operating rules for working in this repo. See `README.md` for the public overview.

## What this repo is

A research workspace on *diagnosis-driven generative data augmentation* for vision models (find where a detector fails → synthesize exactly those cases → retrain → verify the gap closed). **Current plan = two steps:**

1. **Literature survey** — map the diagnosis + generative-augmentation field and establish *what is achievable today* (built on the `docs/kg/` tree + the `90-papers/` atoms).
2. **A pluggable tool** — assemble existing components into a *detect → generate → train-augment* pipeline that measurably improves a detection model. The plugin interface = the **shared diagnosis↔generation representation** (the alignment thesis below).

> **The elevator-CCTV e-bike anchor is dropped** (archived under `_archive/`). Don't scope new work to it. COCO / standard detection benchmarks are the working ground now.

The repo began as a knowledge tree (Phases 0–4: wide sweep + the four loop stages, in `docs/kg/MAP.md` / `GAPS.md` / `00–20`; kept as history). The theoretical backbone is the **diagnosis↔generation alignment** thesis, worked in **`docs/kg/50-alignment/`** (see its `README.md`): if a diagnosis method's output representation matches a generation method's control interface, the bridge between them stays lightweight — which is exactly what makes the Step-2 tool pluggable. `GAPS.md` is now an **input** (open problems found while surveying), not the sole deliverable.

## The ingestion workflow (RUNBOOK)

All literature goes in one batch at a time, following `docs/kg/RUNBOOK.md`:

1. User names a target → 2. agent searches, returns a **candidate list (title + url), writes nothing** → 3. user picks → 4. agent fetches each pick and drafts `90-papers/authorYEAR-name.md` **from fetched text only** → 5. wire into concept nodes + `MAP.md`, append gaps to `GAPS.md` → 6. report found N / fetched M / unverified K → 7. validate, then commit.

## Hard rules (non-negotiable)

- **Validator gate, every batch:** `python3 docs/kg/tools/validate_kg.py` must exit 0 before committing. **Use `python3`** — default `python` here is 2.7.5.
- **Anti-hallucination:** no paper note without a real fetched `http(s)` url. If a source can't be fetched, do **not** write it from memory — substitute a fetchable equivalent or report it as unverified. Notes drafted from memory carry tag `unverified`.
- **Concept nodes** (`00/10/20/30`) must **never** `[[link]]` an `unverified`-tagged paper. The validator enforces this. (`50-alignment/` is *not* a concept dir — it may link any paper, but every `[[stem]]` must still resolve.)
- **No literal `[[...]]` in prose/examples:** the validator treats any `[[x]]` as a wikilink, so an illustrative `[[example]]` becomes a false "broken link" — and the error print can crash on non-ASCII (e.g. Chinese). Write examples without double brackets.
- **Paper-note frontmatter keys (exact):** `title, authors, year, url, loop-stage, tags`. `loop-stage` ∈ `foundations | landscape | stage1 | stage2 | stage3 | stage4 | anchor`.
- **Every number carries its source** (cite the paper + where: abstract / Table N). Don't invent numbers; if the abstract lacks them, say "to be pulled from the paper body."
- Filenames: `90-papers/authorYEAR-name.md`, kebab-case.

## Web-research conventions (learned the hard way)

- **arXiv:** fetch the `/abs/` page, **not** `/pdf/` — the PDF comes back as binary garble or exceeds the fetch size limit. `/abs/` gives clean title + authors + abstract.
- **MDPI (`www.mdpi.com`): returns HTTP 403 to WebFetch.** Don't retry it — substitute an arXiv / other fetchable source on the same topic.
- **HuggingFace model/weight downloads on this server:** the local proxy passes HF API + small files but **blocks large LFS/Xet bodies** (0-byte downloads). Download with the proxy env vars unset + `HF_ENDPOINT=https://hf-mirror.com` + `HF_HUB_DISABLE_XET=1`; pip via `-i https://pypi.tuna.tsinghua.edu.cn/simple`; `git clone` from github **still needs the proxy**. (Mirror can time out mid-file — re-run `snapshot_download` to fetch missing files; verify ALL weight files landed.)

## Repo conventions

- **Archived (local-only, never commit/push):** the early Flux generation scripts (`generate.py`, `batch_generate.py`, `gen_prom/`, `setup_env/`, outputs/logs) now live under `_archive/flux-experiments/` (gitignored); `组会分享.md` (e-bike org-meeting slides) stays untracked at root. The repo is public; keep these untracked.
- `handoff.md` is volatile session state — untracked, never committed.
- Work happens on `master`; commit each batch directly. Commit-message prefix: `kg(phaseN): ...` or `kg(stageN): ...`.
- Commit/push only when the user asks.

## Where things live

- `docs/kg/MAP.md` — tree index (nested `[[wikilinks]]`); records the suspected weakest loop stage. Update every batch.
- `docs/kg/GAPS.md` — the deliverable; running candidate-gap list.
- `docs/kg/00-foundations/` `10-landscape/` `20-loop/` — Phase 0–4 concept nodes (kept as history). (`30-anchor-task/` archived to `_archive/kg/`.)
- `docs/kg/90-papers/` — one atomic note per paper; **single source of truth**, shared by every view. New papers always land here (via RUNBOOK); other areas only `[[link]]` them.
- `docs/kg/50-alignment/` — **current direction** (diagnosis↔generation alignment): new *view* docs (thesis, representation-map, surveys, gaps) + `decisions/gen-toolkit.md` (local GeoDiffusion/SDXL/Flux toolkit). References `90-papers/` atoms; never copies them.
- `docs/zh/` — Chinese translation of the repo (showcase); English is authoritative, so update English first.
- `docs/kg/_templates/` — `paper-note.md`, `concept-node.md`.
- `docs/kg/tools/validate_kg.py` + `test_validate_kg.py` — the gate (run tests with `python3 -m pytest`).
