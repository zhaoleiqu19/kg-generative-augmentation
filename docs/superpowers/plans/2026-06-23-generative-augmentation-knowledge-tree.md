# Knowledge Tree for Diagnosis-Driven Generative Augmentation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up an Obsidian-compatible Markdown knowledge tree in `docs/kg/` with a runnable validator and a repeatable agent ingestion workflow, then drive it through a wide sweep + per-stage deep dives toward a shortlist of 2-3 demonstrable research gaps.

**Architecture:** Atomic paper notes in `90-papers/` link up into synthesized concept nodes in `00/10/20/30`; `MAP.md` is the tree, `GAPS.md` is the payoff. A Python validator enforces frontmatter completeness, link integrity, and the anti-hallucination guardrail (concept nodes may not cite `#unverified` papers). The validator is the test gate for every ingestion batch.

**Tech Stack:** Markdown (Obsidian `[[wikilinks]]`), Python 3.11 stdlib + pytest, git. Web access via deferred `WebSearch`/`WebFetch` tools at execution time.

## Global Constraints

- Knowledge tree root: `docs/kg/`. Plan/spec under `docs/superpowers/`.
- Paper-note filename: `90-papers/authorYEAR-name.md` (kebab-case).
- Paper-note required frontmatter keys (exact): `title, authors, year, url, loop-stage, tags`.
- `url` must start with `http` (a fetched, real source). No paper note without one.
- Anti-hallucination: notes drafted from memory before fetching carry tag `unverified`; concept nodes (`00/10/20/30`) must never `[[link]]` an `unverified` paper.
- Definition of done for the whole effort: `GAPS.md` holds 2-3 gaps that are (a) not already solved in the tree and (b) demonstrable on the elevator e-bike anchor task.
- Every ingestion batch ends green: `python docs/kg/tools/validate_kg.py` exits 0, then commit.

---

### Task 1: Scaffold the knowledge-tree structure

**Files:**
- Create: `docs/kg/MAP.md`, `docs/kg/GAPS.md`, `docs/kg/RUNBOOK.md`
- Create: `docs/kg/_templates/paper-note.md`, `docs/kg/_templates/concept-node.md`
- Create: `.gitkeep` in each leaf dir under `00-foundations 10-landscape 20-loop/{stage1-diagnosis,stage2-spec,stage3-synthesis,stage4-closeloop} 30-anchor-task 90-papers`

**Interfaces:**
- Produces: the directory layout and template files all later tasks/notes follow; `RUNBOOK.md` (the ingestion procedure) consumed by Task 4+.

- [ ] **Step 1: Create the directory tree**

```bash
cd docs/kg 2>/dev/null || mkdir -p docs/kg && cd docs/kg
for d in 00-foundations 10-landscape \
         20-loop/stage1-diagnosis 20-loop/stage2-spec 20-loop/stage3-synthesis 20-loop/stage4-closeloop \
         30-anchor-task 90-papers _templates tools; do
  mkdir -p "$d" && touch "$d/.gitkeep"
done
```

- [ ] **Step 2: Write the paper-note template**

File `docs/kg/_templates/paper-note.md`:

```markdown
---
title:
authors:
year:
venue:
url:
loop-stage:   # foundations | landscape | stage1 | stage2 | stage3 | stage4 | anchor
tags:
---

## TL;DR
(2 lines)

## Method
## Main claim + result
(include the number, with its source)

## Relevance to us
## Links
- [[concept-node]]
```

- [ ] **Step 3: Write the concept-node template**

File `docs/kg/_templates/concept-node.md`:

```markdown
# <Concept>

## What it is
## Why it matters
## Key papers
- [[authorYEAR-name]]

## Open questions
## Our take
```

- [ ] **Step 4: Write MAP, GAPS, RUNBOOK home pages**

File `docs/kg/MAP.md`:

```markdown
# Knowledge Tree — Map

The whole tree as nested links. Updated every ingestion batch.

- 00 Foundations
- 10 Landscape (wide sweep)
- 20 Loop (spine)
  - stage1 diagnosis
  - stage2 spec
  - stage3 synthesis
  - stage4 close-loop
- 30 Anchor task (elevator e-bike detection)
- 90 Papers
```

File `docs/kg/GAPS.md`:

```markdown
# Candidate Research Gaps

One entry per candidate. Append every batch. Each: gap · evidence (links) · why-not-solved · demonstrable-on-anchor? (y/n/unknown).

(none yet)
```

File `docs/kg/RUNBOOK.md`:

```markdown
# Ingestion Runbook (one batch)

1. User names a target (survey / subtopic / "fill stage1-diagnosis").
2. Agent loads WebSearch/WebFetch, searches, returns CANDIDATE LIST (title + url) — writes nothing yet.
3. User picks which candidates get full notes.
4. Agent WebFetches each pick; drafts `90-papers/authorYEAR-name.md` from fetched text only.
5. Agent updates the concept node, MAP.md (new [[link]]), appends any gap to GAPS.md.
6. Agent reports: found N, fetched M, couldn't verify K.
7. Run `python docs/kg/tools/validate_kg.py` → must exit 0. Commit.

Guardrails: no note without a fetched http url; memory-only drafts tagged `unverified`; concept nodes never link unverified papers; every number carries its source.
```

- [ ] **Step 5: Verify structure exists**

Run: `find docs/kg -type d | sort && ls docs/kg/_templates`
Expected: all dirs listed; `concept-node.md  paper-note.md` present.

- [ ] **Step 6: Commit**

```bash
git add docs/kg
git commit -m "feat(kg): scaffold knowledge-tree structure and templates"
```

---

### Task 2: Build the KG validator (TDD)

**Files:**
- Create: `docs/kg/tools/validate_kg.py`
- Test: `docs/kg/tools/test_validate_kg.py`

**Interfaces:**
- Produces: `validate(root: pathlib.Path) -> list[str]` (returns error strings, empty = valid) and a CLI `main()` returning an exit code. Consumed as the test gate by every later task.

- [ ] **Step 1: Write the failing tests**

File `docs/kg/tools/test_validate_kg.py`:

```python
import pathlib
from validate_kg import validate

def _scaffold(root):
    (root / "90-papers").mkdir(parents=True)
    (root / "00-foundations").mkdir()
    (root / "MAP.md").write_text("# Map\n")
    (root / "GAPS.md").write_text("# Gaps\n")

def _paper(root, stem, **fm):
    base = {"title": "T", "authors": "A", "year": "2024",
            "url": "http://x", "loop-stage": "stage1", "tags": "x"}
    base.update(fm)
    body = "---\n" + "\n".join(f"{k}: {v}" for k, v in base.items()) + "\n---\nbody\n"
    (root / "90-papers" / f"{stem}.md").write_text(body)

def test_clean_tree_passes(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo")
    assert validate(tmp_path) == []

def test_missing_map_fails(tmp_path):
    _scaffold(tmp_path)
    (tmp_path / "MAP.md").unlink()
    assert any("MAP.md" in e for e in validate(tmp_path))

def test_missing_frontmatter_key_fails(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", url="")
    assert any("url" in e for e in validate(tmp_path))

def test_non_http_url_fails(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", url="arxiv-2401")
    assert any("http" in e for e in validate(tmp_path))

def test_broken_link_fails(tmp_path):
    _scaffold(tmp_path)
    (tmp_path / "00-foundations" / "c.md").write_text("see [[nope]]\n")
    assert any("broken link" in e for e in validate(tmp_path))

def test_concept_cannot_link_unverified(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", tags="unverified")
    (tmp_path / "00-foundations" / "c.md").write_text("[[smith2024-foo]]\n")
    assert any("unverified" in e for e in validate(tmp_path))
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd docs/kg/tools && python -m pytest test_validate_kg.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'validate_kg'`.

- [ ] **Step 3: Implement the validator**

File `docs/kg/tools/validate_kg.py`:

```python
#!/usr/bin/env python3
"""Validate the docs/kg knowledge tree: frontmatter, links, guardrails."""
import re
import sys
import pathlib

CONCEPT_DIRS = ("00-foundations", "10-landscape", "20-loop", "30-anchor-task")
REQUIRED = ("title", "authors", "year", "url", "loop-stage", "tags")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def _frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def validate(root):
    root = pathlib.Path(root)
    errors = []
    for home in ("MAP.md", "GAPS.md"):
        if not (root / home).exists():
            errors.append(f"{home} missing")

    md = list(root.rglob("*.md"))
    stems = {p.stem for p in md}
    unverified = set()

    papers = root / "90-papers"
    for p in papers.rglob("*.md") if papers.exists() else []:
        text = p.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        if fm is None:
            errors.append(f"{p.name}: missing frontmatter")
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{p.name}: frontmatter missing '{key}'")
        url = fm.get("url", "")
        if url and not url.startswith("http"):
            errors.append(f"{p.name}: url must start with http (got '{url}')")
        if "unverified" in fm.get("tags", "") or "#unverified" in text:
            unverified.add(p.stem)

    for p in md:
        text = p.read_text(encoding="utf-8")
        is_concept = any(part in CONCEPT_DIRS for part in p.parts)
        for raw in LINK_RE.findall(text):
            target = raw.split("|")[0].split("#")[0].strip()
            if not target:
                continue
            if target not in stems:
                errors.append(f"{p.name}: broken link [[{target}]]")
            elif is_concept and target in unverified:
                errors.append(f"{p.name}: concept node links unverified paper [[{target}]]")
    return errors


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    errors = validate(root)
    if errors:
        print("KG VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    print("KG validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd docs/kg/tools && python -m pytest test_validate_kg.py -q`
Expected: PASS (6 passed).

- [ ] **Step 5: Commit**

```bash
git add docs/kg/tools/validate_kg.py docs/kg/tools/test_validate_kg.py
git commit -m "feat(kg): add knowledge-tree validator with tests"
```

---

### Task 3: Establish green baseline on the real tree

**Files:**
- Modify: `docs/kg/90-papers/` (add one seed paper note end-to-end as a smoke test)
- Modify: `docs/kg/00-foundations/glossary.md` (create, link the seed)

**Interfaces:**
- Consumes: `validate(root)` from Task 2, templates from Task 1.
- Produces: a proven end-to-end example note + passing validator on the actual `docs/kg/`.

- [ ] **Step 1: Run validator on the real (empty) tree**

Run: `python docs/kg/tools/validate_kg.py`
Expected: PASS (no papers yet, MAP/GAPS exist).

- [ ] **Step 2: Add one real seed paper note**

Pick one well-known survey, fetch it (`WebFetch`), and write `docs/kg/90-papers/<authorYEAR-name>.md` from the template with all required frontmatter filled from the fetched page (real `http` url). This is the smoke test of the whole note format.

- [ ] **Step 3: Create glossary concept node linking the seed**

File `docs/kg/00-foundations/glossary.md`: start the glossary, add a `## Key papers` section with `[[<authorYEAR-name>]]` pointing at the seed.

- [ ] **Step 4: Update MAP.md**

Add the glossary and the seed paper under their branches in `docs/kg/MAP.md` as `[[links]]`.

- [ ] **Step 5: Run validator, verify green**

Run: `python docs/kg/tools/validate_kg.py`
Expected: `KG validation passed.`

- [ ] **Step 6: Commit**

```bash
git add docs/kg
git commit -m "feat(kg): seed glossary + first paper note, green baseline"
```

---

### Task 4: Phase 0 — wide sweep (recurring ingestion batches)

**Files:**
- Modify: `docs/kg/00-foundations/*`, `docs/kg/10-landscape/*`, `docs/kg/90-papers/*`, `docs/kg/MAP.md`, `docs/kg/GAPS.md`

**Interfaces:**
- Consumes: `RUNBOOK.md` procedure, validator gate.
- Produces: populated foundations + landscape, full MAP skeleton with stubs everywhere, first read on the weakest loop stage.

This task repeats the RUNBOOK batch (Task 1, RUNBOOK.md) until the exit criteria below are met. Each batch is one reviewable unit.

- [ ] **Step 1 (per batch): Pick a target & gather candidates**

Targets in order: a recent survey on (1) synthetic/generated data for object detection, (2) data-centric AI, (3) diffusion models for data augmentation. Agent loads `WebSearch`/`WebFetch`, returns a CANDIDATE LIST (title + url), writes nothing.

- [ ] **Step 2 (per batch): User picks; agent fetches & drafts notes**

For each pick: `WebFetch` the source, write `90-papers/authorYEAR-name.md` from fetched text only, fill all required frontmatter.

- [ ] **Step 3 (per batch): Synthesize + wire up**

Update/create the matching `00-foundations` / `10-landscape` concept node, add `[[links]]` to MAP.md, append any noticed gap to GAPS.md. Report found N / fetched M / unverified K.

- [ ] **Step 4 (per batch): Validate & commit**

Run: `python docs/kg/tools/validate_kg.py` → expect PASS.
```bash
git add docs/kg && git commit -m "kg(phase0): ingest <target> batch"
```

- [ ] **Step 5: Phase 0 exit check**

Done when: `00-foundations/glossary.md` populated; `10-landscape/does-synthetic-data-help.md` maps the helps-vs-hurts debate with cited numbers; `MAP.md` has every branch with at least a stub node; a note in `MAP.md` records the suspected weakest loop stage. Validator green.

---

### Task 5: Phases 1-4 — per-stage deep dives

**Files:**
- Modify: `docs/kg/20-loop/stage{1,2,3,4}-*/*`, `90-papers/*`, `MAP.md`, `GAPS.md`

**Interfaces:**
- Consumes: RUNBOOK, validator, Phase 0 vocabulary.
- Produces: per-stage "state-of-the-art + open problems" node and fresh GAPS entries.

Run the RUNBOOK batches stage by stage, in order: `stage1-diagnosis` → `stage2-spec` → `stage3-synthesis` → `stage4-closeloop`. Each stage is one reviewable sub-milestone.

- [ ] **Step 1 (per stage): Ingest batches for the stage** (same 4 batch steps as Task 4).

- [ ] **Step 2 (per stage): Write the stage synthesis node**

In the stage folder, create `state-of-the-art.md`: what's solved, what's open, key papers `[[...]]`, our-take. Append concrete gaps to GAPS.md.

- [ ] **Step 3 (per stage): Validate & commit**

Run: `python docs/kg/tools/validate_kg.py` → PASS.
```bash
git add docs/kg && git commit -m "kg(stageN): deep-dive synthesis + gaps"
```

- [ ] **Step 4: Phases 1-4 exit check**

Done when each of the four stages has a `state-of-the-art.md` with cited papers and at least one GAPS entry traceable to it. Validator green.

---

### Task 6: Phase 5 — project gaps onto the anchor task

**Files:**
- Modify: `docs/kg/30-anchor-task/{task-sota.md,public-datasets.md,known-hard-cases.md}`, `docs/kg/GAPS.md`

**Interfaces:**
- Consumes: GAPS.md shortlist, anchor-task notes.
- Produces: the final 2-3 gap shortlist scored for feasibility on the elevator e-bike task.

- [ ] **Step 1: Fill anchor-task notes**

Ingest (RUNBOOK) the elevator/e-bike/surveillance-detection SOTA and any public datasets into `30-anchor-task/`. `known-hard-cases.md` links to the existing occlusion / "entering elevator" prompt work in this workspace.

- [ ] **Step 2: Score each top gap against the anchor**

For each top candidate in GAPS.md, add: real? (not solved in tree) · demonstrable on elevator task with existing Flux pipeline + a dataset? (y/n + why) · rough effort.

- [ ] **Step 3: Cut to the shortlist**

Edit GAPS.md so the top section is exactly 2-3 gaps meeting both done-criteria. Move the rest to a "parked" section.

- [ ] **Step 4: Validate & commit**

Run: `python docs/kg/tools/validate_kg.py` → PASS.
```bash
git add docs/kg && git commit -m "kg(phase5): anchor-task gap shortlist"
```

- [ ] **Step 5: Definition-of-done check**

`GAPS.md` top section holds 2-3 gaps that are (a) not solved in the tree and (b) demonstrable on the elevator task. Stop here — choosing which gap to pursue is follow-on work (separate spec).

---

## Self-Review

**Spec coverage:** spine = loop (Tasks 4-5), wide sweep first (Task 4), foundations + frontier (Task 4 covers both `00` and `10`), anchor task as testbed (Task 6), note-web form + templates (Task 1), anti-hallucination guardrails (encoded in validator Task 2 + RUNBOOK Task 1), GAPS as payoff + definition of done (Task 6). Master comparison table is optional in the spec and omitted from the plan as YAGNI until paper volume justifies it — noted here intentionally.

**Placeholder scan:** research-content tasks (4-6) are intentionally procedural because the specific papers cannot be known before fetching; the *procedure*, exit criteria, and the validator gate are concrete. No code step lacks code.

**Type consistency:** `validate(root) -> list[str]` and `main() -> int` used consistently across Task 2 tests, implementation, and Tasks 3-6 gates. Frontmatter key list `REQUIRED` matches the Global Constraints and the paper-note template.
