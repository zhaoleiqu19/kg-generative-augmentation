# Design: Knowledge Tree for Diagnosis-Driven Generative Data Augmentation

**Date:** 2026-06-23
**Status:** Approved (design); pending implementation plan
**Owner:** kushyido@gmail.com

## 1. Goal

Build a maintainable, agent-assisted **knowledge tree** (Obsidian-compatible Markdown
note-web inside this repo) while surveying the vertical field of **using generative
models to augment vision models**. The tree is a byproduct; the real deliverable is a
**shortlist of 2-3 candidate research gaps** that are (a) not already solved in the
surveyed literature and (b) demonstrable on a concrete anchor task.

### Research spine

The conceptual spine is the **diagnosis -> generation closed loop**:

> Don't augment blindly. First find where the dataset/model fails, then synthesize
> exactly those cases, then verify the gap closed without harming the rest.

A fast **level-0 wide sweep** of the broader "generative augmentation for vision" field
precedes the deep dive, to build vocabulary and reveal which loop stage the field is
weakest at.

### Anchor task

**Elevator CCTV detection of electric mopeds / e-bikes** (fire-safety "no e-bike in
elevator" use case). Already explored in this workspace via Flux prompts targeting hard
cases: occlusion by people, moped-vs-bicycle confusion, the "entering the elevator"
boundary state. Used as the validation testbed in the final phase, not the spine.

## 2. Knowledge-tree structure

Lives in `docs/kg/`. Two node types:

- **Paper note** (`90-papers/authorYEAR-name.md`) — atomic, one per paper.
- **Concept node** (`00/10/20/30/*.md`) — synthesized, links to paper notes.

```
docs/kg/
  MAP.md                      # home node: the whole tree as nested [[links]]
  GAPS.md                     # running list of candidate research gaps (the payoff)
  00-foundations/             # terminology & basics (vocab grounding)
    glossary.md
    data-augmentation-basics.md
    synthetic-vs-real-data.md
    domain-gap-and-sim2real.md
    diffusion-models-primer.md
    detection-eval-metrics.md
  10-landscape/               # LEVEL-0 wide sweep of generative augmentation
    techniques-overview.md
    does-synthetic-data-help.md     # the "when it helps vs hurts" debate
    evaluating-synthetic-data.md
    surveys-and-benchmarks.md
  20-loop/                    # THE SPINE: one folder per stage
    stage1-diagnosis/         # finding weaknesses: slice discovery, error analysis,
                              #   hard-case mining
    stage2-spec/              # weakness -> generation spec (failure -> prompt/condition)
    stage3-synthesis/         # targeted controllable generation
                              #   (layout / occlusion / rare-case)
    stage4-closeloop/         # did the gap close? targeted eval, no-regression,
                              #   end-to-end loop systems
  30-anchor-task/             # elevator e-bike detection as validation testbed
    task-sota.md
    public-datasets.md
    known-hard-cases.md       # links to existing occlusion / "entering elevator" prompts
  90-papers/                  # one atomic note per paper (authorYEAR-name.md)
  _templates/                 # paper-note.md, concept-node.md
```

Principle: `90-papers/` holds raw atomic notes; `00/10/20/30` hold synthesized concept
nodes that link to them; `MAP.md` is the tree; `GAPS.md` is where the thesis emerges.

### Node templates

**Paper note** frontmatter: `title, authors, year, venue, url/arxiv-id, loop-stage, tags`.
Body: TL;DR (2 lines) · method · main claim + result (with the number) ·
**relevance-to-us** · `[[links]]` to concept nodes.

**Concept node** body: what it is · why it matters · key papers `[[...]]` ·
**open questions** · **our-take**.

Optional: a master comparison **table node** auto-derived from paper-note frontmatter
(method / scenario / result / link) for at-a-glance comparison.

## 3. Build method

Chosen approach: **agent-assisted curated note-web** (with a borrowed master table node).
Rejected alternatives: bulk-summarize-first (too shallow, hallucination-prone);
depth-first skipping the wide sweep (risk of missing prior art).

### The ingestion loop (one unit of work)

1. **User** names a target (a survey, a subtopic, or "fill stage1-diagnosis").
2. **Agent searches** (WebSearch -> arxiv / Semantic Scholar) and returns a *candidate
   list* with title + url **before writing anything**.
3. **User picks** which candidates get a full note.
4. **Agent WebFetches each chosen paper** and drafts the atomic note **only from fetched
   text** — never from memory.
5. **Agent updates** the relevant concept node, `MAP.md` (new `[[link]]`), and appends any
   noticed gap to `GAPS.md`.
6. **User reviews**, corrects "our-take," promotes/demotes.

Division of labor: agent does the dredging (search, fetch, draft, link maintenance); user
keeps the two judgment calls — **what's worth reading** (step 3) and **what it means for
us** (step 6).

### Anti-hallucination guardrails (non-negotiable)

- **No paper note without a working fetched URL.** Un-fetchable -> no node.
- Every quantitative claim carries its source number, not a memory paraphrase.
- Anything drafted from memory before fetching is tagged `#unverified` and **cannot** be
  cited in a concept node until fetched.
- Each batch the agent reports "found N, fetched M, couldn't verify K."

### Practical notes

- Web access via deferred tools (`WebSearch` / `WebFetch`), loaded at start.
- Some paper sites block fetching; arxiv abstract/HTML and Semantic Scholar usually work,
  PDFs sometimes do not.

## 4. Cadence

- **Phase 0 — Wide sweep.** Target `00-foundations/` + `10-landscape/`. Start from 2-3
  recent surveys (synthetic data for object detection; data-centric AI; diffusion models
  for data augmentation), harvest their reference lists. Coverage + vocabulary over depth;
  first read on which loop stage is weakest. *Exit when:* glossary populated, the "does
  synthetic data help?" debate mapped, `MAP.md` skeleton complete with stubs everywhere.
- **Phases 1-4 — Deep dive, one loop stage at a time** (`stage1` -> `stage2` -> `stage3`
  -> `stage4`). Each ends with a "state-of-the-art + open problems" synthesis node and
  fresh `GAPS.md` entries. Hypothesis: `stage1` (diagnosis) and `stage4` (verifying the
  gap closed) are thinnest — likely where the bet lives; the wide sweep confirms.
- **Phase 5 — Project gaps onto the anchor task.** Take top 2-3 from `GAPS.md`, write them
  against `30-anchor-task/`: is each gap real *and* feasible to demonstrate on the elevator
  task with the existing Flux pipeline + a public/own dataset?

### Definition of done

Not "read everything." Done when `GAPS.md` holds **2-3 gaps that are (a) not already
solved in the tree and (b) demonstrable on the anchor task** — the research-point
shortlist.

### Running discipline

Every batch appends to `GAPS.md` and updates `MAP.md`. The tree is never stale; the thesis
accumulates in one watchable file.

## 5. Out of scope (for now)

- Actually running detection training / generation experiments (that is Phase 5+ follow-on
  work, a separate spec).
- Choosing a final research gap to pursue (output of this work, not part of it).
- Any change to the existing Flux generation scripts.
