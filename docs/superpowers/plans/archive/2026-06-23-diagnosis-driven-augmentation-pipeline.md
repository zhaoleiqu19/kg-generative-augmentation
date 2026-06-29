# Diagnosis-Driven Generative Augmentation Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimal, end-to-end diagnosis-driven generative augmentation pipeline (diagnose → spec → generate → filter+retrain → measure) with swappable module interfaces, prove the skeleton on fake data, lock the demo task + components via a focused survey, then run one real round and report whether the metric moved.

**Architecture:** Four single-responsibility modules (Diagnose, Spec, Generate, CloseLoop) communicate only through four frozen dataclass contracts (`Slice`, `GenSpec`, `SyntheticDataset`, `Report`); an Orchestrator runs them in sequence with a round/stop loop. The skeleton ships first with dummy implementations (fully end-to-end green on tiny fake data), proving the module boundaries, before any heavy ML component is integrated. Real components are adapters that honor the same contracts; swapping a method or task touches only one module's implementation (or just data loading + metric).

**Tech Stack:** Python 3.11, pytest, stdlib dataclasses (skeleton). Real-integration tasks add PyTorch + `ultralytics` (YOLO baseline, COCO-format annotations) and external diagnosis/generation repos chosen during the survey.

## Global Constraints

- Project root for pipeline code: repo-root `pipeline/` (realizes the spec's "40-pipeline/" as a top-level project dir; keeps the `docs/kg/` Obsidian vault free of code). Decision docs in `pipeline/decisions/`.
- Reuse published, validated components only — no novel diagnosis/generation algorithms.
- First version: **no elevator data** (use a public detection set); **single round** (no forced multi-round iteration).
- Accumulation rule: real + synthetic **accumulate, never replace real**.
- Eval set contains **no synthetic images**; report the targeted slice's delta, not only the overall average.
- Success = the loop closes end-to-end and the result is interpretable; **up / flat / down all count**.
- Run the skeleton test gate with `python3 -m pytest pipeline/tests -q` (default `python` here is 2.7.5).
- Contract field names are frozen across all tasks: `Slice(description, members, metric, severity)`, `GenItem(target, conditions, count)`, `GenSpec(items)`, `SyntheticDataset(images_dir, annotations_path)`, `Report(baseline_metric, augmented_metric, per_slice_delta, iterate)`.

---

### Task 1: Scaffold + data contracts

**Files:**
- Create: `pipeline/pipeline/__init__.py`, `pipeline/pipeline/contracts.py`
- Create: `pipeline/tests/__init__.py`, `pipeline/tests/test_contracts.py`
- Create: `pipeline/requirements.txt`, `pipeline/README.md`

**Interfaces:**
- Produces: the four frozen dataclasses every later task imports — `Slice`, `GenItem`, `GenSpec`, `SyntheticDataset`, `Report` (field names per Global Constraints).

- [ ] **Step 1: Write the failing test**

`pipeline/tests/test_contracts.py`:
```python
from pipeline.contracts import Slice, GenItem, GenSpec, SyntheticDataset, Report

def test_slice_fields():
    s = Slice(description="small+occluded", members=["a", "b"], metric=0.12, severity=0.9)
    assert s.members == ["a", "b"] and s.metric == 0.12

def test_genspec_holds_items():
    spec = GenSpec(items=[GenItem(target="small+occluded", conditions="prompt: small ebike, occluded", count=50)])
    assert spec.items[0].count == 50

def test_report_fields():
    r = Report(baseline_metric=0.30, augmented_metric=0.34, per_slice_delta={"small+occluded": 0.06}, iterate=False)
    assert r.augmented_metric - r.baseline_metric == 0.04
    assert r.per_slice_delta["small+occluded"] == 0.06

def test_synthetic_dataset_paths():
    d = SyntheticDataset(images_dir="/tmp/x", annotations_path="/tmp/x/ann.json")
    assert d.annotations_path.endswith(".json")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest pipeline/tests/test_contracts.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.contracts'`.

- [ ] **Step 3: Write minimal implementation**

`pipeline/pipeline/__init__.py`: empty file.
`pipeline/pipeline/contracts.py`:
```python
"""Data contracts — the only coupling points between pipeline modules."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Slice:
    description: str          # human-readable, e.g. "small + occluded"
    members: list[str]        # sample ids locating the failing examples
    metric: float             # AP/acc on this slice
    severity: float           # higher = worse / more urgent to fix


@dataclass(frozen=True)
class GenItem:
    target: str               # the slice description this item addresses
    conditions: str           # free field: prompt / layout / region spec
    count: int                # how many to generate


@dataclass(frozen=True)
class GenSpec:
    items: list[GenItem]


@dataclass(frozen=True)
class SyntheticDataset:
    images_dir: str           # directory of generated images
    annotations_path: str     # COCO-format json, same schema as the real set


@dataclass(frozen=True)
class Report:
    baseline_metric: float
    augmented_metric: float
    per_slice_delta: dict      # slice description -> metric delta
    iterate: bool              # whether the orchestrator should run another round
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest pipeline/tests/test_contracts.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Add requirements + README, then commit**

`pipeline/requirements.txt`:
```
pytest
```
`pipeline/README.md`:
```markdown
# Pipeline — diagnosis-driven generative augmentation

Vertical-slice pipeline with swappable modules. See
`docs/superpowers/specs/2026-06-23-diagnosis-driven-augmentation-pipeline-design.md`.

Test gate: `python3 -m pytest pipeline/tests -q`
```
```bash
git add pipeline
git commit -m "feat(pipeline): data contracts + scaffold"
```

---

### Task 2: Module interfaces, dummy implementations, orchestrator (end-to-end on fake data)

**Files:**
- Create: `pipeline/pipeline/interfaces.py`, `pipeline/pipeline/dummies.py`, `pipeline/pipeline/orchestrator.py`
- Create: `pipeline/tests/test_dummies.py`, `pipeline/tests/test_orchestrator.py`

**Interfaces:**
- Consumes: `Slice, GenItem, GenSpec, SyntheticDataset, Report` from Task 1.
- Produces: ABCs `Diagnoser.diagnose(model, dataset) -> list[Slice]`, `Specifier.make_spec(slices, budget) -> GenSpec`, `Generator.generate(spec) -> SyntheticDataset`, `CloseLooper.close_loop(model, real, synth) -> Report`; and `run_loop(model, real, diagnoser, specifier, generator, closelooper, budget, max_rounds=1) -> list[Report]`. Later real-component tasks subclass these ABCs.

- [ ] **Step 1: Write the failing tests**

`pipeline/tests/test_dummies.py`:
```python
from pipeline.contracts import GenSpec, SyntheticDataset, Report
from pipeline.dummies import DummyDiagnoser, DummySpecifier, DummyGenerator, DummyCloseLooper

def test_dummy_diagnoser_returns_slices():
    slices = DummyDiagnoser().diagnose(model=None, dataset=["x"])
    assert slices and all(s.description for s in slices)

def test_dummy_specifier_targets_worst_slice():
    slices = DummyDiagnoser().diagnose(model=None, dataset=["x"])
    spec = DummySpecifier().make_spec(slices, budget=10)
    assert isinstance(spec, GenSpec) and spec.items[0].count <= 10

def test_dummy_generator_returns_dataset(tmp_path):
    spec = DummySpecifier().make_spec(DummyDiagnoser().diagnose(None, ["x"]), budget=10)
    out = DummyGenerator(out_dir=str(tmp_path)).generate(spec)
    assert isinstance(out, SyntheticDataset)

def test_dummy_closelooper_returns_report(tmp_path):
    out = DummyGenerator(out_dir=str(tmp_path)).generate(
        DummySpecifier().make_spec(DummyDiagnoser().diagnose(None, ["x"]), budget=10))
    rep = DummyCloseLooper().close_loop(model=None, real=["x"], synth=out)
    assert isinstance(rep, Report) and rep.iterate is False
```

`pipeline/tests/test_orchestrator.py`:
```python
from pipeline.contracts import Report
from pipeline.dummies import DummyDiagnoser, DummySpecifier, DummyGenerator, DummyCloseLooper
from pipeline.orchestrator import run_loop

def test_run_loop_end_to_end(tmp_path):
    reports = run_loop(
        model=None, real=["x"],
        diagnoser=DummyDiagnoser(), specifier=DummySpecifier(),
        generator=DummyGenerator(out_dir=str(tmp_path)), closelooper=DummyCloseLooper(),
        budget=10, max_rounds=1)
    assert len(reports) == 1 and isinstance(reports[0], Report)

def test_boundary_swap_diagnoser(tmp_path):
    # Swapping one module's impl must not require touching others.
    class OneSliceDiagnoser(DummyDiagnoser):
        def diagnose(self, model, dataset):
            base = super().diagnose(model, dataset)
            return base[:1]
    reports = run_loop(
        model=None, real=["x"],
        diagnoser=OneSliceDiagnoser(), specifier=DummySpecifier(),
        generator=DummyGenerator(out_dir=str(tmp_path)), closelooper=DummyCloseLooper(),
        budget=10, max_rounds=1)
    assert len(reports) == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest pipeline/tests/test_dummies.py pipeline/tests/test_orchestrator.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.interfaces'` / `pipeline.dummies`.

- [ ] **Step 3: Write the interfaces**

`pipeline/pipeline/interfaces.py`:
```python
"""Abstract module interfaces. Real components and dummies both subclass these."""
import abc
from .contracts import Slice, GenSpec, SyntheticDataset, Report


class Diagnoser(abc.ABC):
    @abc.abstractmethod
    def diagnose(self, model, dataset) -> list[Slice]: ...


class Specifier(abc.ABC):
    @abc.abstractmethod
    def make_spec(self, slices: list[Slice], budget: int) -> GenSpec: ...


class Generator(abc.ABC):
    @abc.abstractmethod
    def generate(self, spec: GenSpec) -> SyntheticDataset: ...


class CloseLooper(abc.ABC):
    @abc.abstractmethod
    def close_loop(self, model, real, synth: SyntheticDataset) -> Report: ...
```

- [ ] **Step 4: Write the dummies**

`pipeline/pipeline/dummies.py`:
```python
"""Trivial implementations so the whole loop runs end-to-end on fake data."""
import json
import os
from .contracts import Slice, GenItem, GenSpec, SyntheticDataset, Report
from .interfaces import Diagnoser, Specifier, Generator, CloseLooper


class DummyDiagnoser(Diagnoser):
    def diagnose(self, model, dataset):
        return [
            Slice(description="small+occluded", members=["s1", "s2"], metric=0.10, severity=0.9),
            Slice(description="low-light", members=["s3"], metric=0.20, severity=0.5),
        ]


class DummySpecifier(Specifier):
    def make_spec(self, slices, budget):
        worst = max(slices, key=lambda s: s.severity)
        return GenSpec(items=[GenItem(target=worst.description,
                                      conditions=f"prompt: {worst.description}",
                                      count=min(budget, 10))])


class DummyGenerator(Generator):
    def __init__(self, out_dir):
        self.out_dir = out_dir

    def generate(self, spec):
        os.makedirs(self.out_dir, exist_ok=True)
        ann = os.path.join(self.out_dir, "ann.json")
        with open(ann, "w") as f:
            json.dump({"images": [], "annotations": [], "spec_items": len(spec.items)}, f)
        return SyntheticDataset(images_dir=self.out_dir, annotations_path=ann)


class DummyCloseLooper(CloseLooper):
    def close_loop(self, model, real, synth):
        return Report(baseline_metric=0.30, augmented_metric=0.30,
                      per_slice_delta={"small+occluded": 0.0}, iterate=False)
```

- [ ] **Step 5: Write the orchestrator**

`pipeline/pipeline/orchestrator.py`:
```python
"""Runs diagnose -> spec -> generate -> close_loop, with a round/stop loop."""
from .interfaces import Diagnoser, Specifier, Generator, CloseLooper


def run_loop(model, real, diagnoser: Diagnoser, specifier: Specifier,
             generator: Generator, closelooper: CloseLooper,
             budget: int, max_rounds: int = 1):
    reports = []
    for _ in range(max_rounds):
        slices = diagnoser.diagnose(model, real)
        spec = specifier.make_spec(slices, budget)
        synth = generator.generate(spec)
        report = closelooper.close_loop(model, real, synth)
        reports.append(report)
        if not report.iterate:
            break
    return reports
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 -m pytest pipeline/tests -q`
Expected: PASS (all contract + dummy + orchestrator tests).

- [ ] **Step 7: Commit**

```bash
git add pipeline
git commit -m "feat(pipeline): module interfaces, dummies, orchestrator (end-to-end on fake data)"
```

---

### Task 3: Survey — select the demo task (decision deliverable)

> Research/decision task: produces two markdown decision docs, no pipeline code. Follows the `docs/kg/RUNBOOK.md` ingestion discipline (candidate list → fetch `/abs/` → cite numbers; MDPI 403 → arXiv substitute).

**Files:**
- Create: `pipeline/decisions/generality-map.md`
- Create: `pipeline/decisions/demo-task-selection.md`

**Interfaces:**
- Consumes: `docs/kg/90-papers/*` and `docs/kg/20-loop/stage*-state-of-the-art.md` as the evidence base.
- Produces: a locked `(model, task, dataset)` choice and a per-module component choice that Tasks 5–8 implement.

- [ ] **Step 1: Build the detection-first generality map**

Search (WebSearch/WebFetch) detection sub-scenarios where diagnosis-driven / generative augmentation has reported gains. For each row record: scenario, representative paper `[[link]]` (already in the tree where possible), reported gain + source, public-dataset availability, generation-tool fit. Write to `pipeline/decisions/generality-map.md` as a table; include an **"elevator e-bike — target, pending data"** row.

- [ ] **Step 2: Apply the selection checklist and choose the demo task**

Choose the one `(model, task, dataset)` meeting all of: public + single-GPU-sized dataset; detection with clear diagnosable failure modes (small/occluded/long-tail); someone reported generative-augmentation gains on this kind of task; generation coverable by ODGEN or DreamBooth+X-Paste. Write `pipeline/decisions/demo-task-selection.md` with: chosen dataset + why; baseline detector (a pretrained model to fine-tune); and a provisional per-module component choice (Diagnose: HiBug2 or GH-ESD; Generate: ODGEN or DreamBooth+X-Paste; CloseLoop filter: CLIP or detector self-agreement).

- [ ] **Step 3: Exit check + commit**

Exit criteria: both files exist; `demo-task-selection.md` names an exact dataset, an exact baseline model, and one component per module, each with a cited reason. Every number carries its source.
```bash
git add pipeline/decisions
git commit -m "docs(pipeline): generality map + demo-task selection"
```

---

### Task 4: Flux capability probe (decision deliverable)

> Decides who fills the Generate module. The spec mandates this as the first concrete action before real generation.

**Files:**
- Create: `pipeline/decisions/flux-capability-probe.md`
- Modify: `pipeline/decisions/demo-task-selection.md` (record the final Generate choice)

**Interfaces:**
- Consumes: the local Flux generation scripts (`generate.py`, `batch_generate.py`, `gen_prom/` — untracked, local-only).
- Produces: a yes/no on whether Flux can (a) control layout/region and (b) personalize a specific object, and the final Generate-module decision.

- [ ] **Step 1: Probe layout/region control**

Using the existing local Flux scripts, attempt to generate an image where an object is placed in a specified region / under a specified condition. Record: works / partially / no, with an example prompt and the observed result. (If Flux only does free text-to-image, note that.)

- [ ] **Step 2: Probe object personalization**

Attempt to render a specific recurring object across varied scenes (DreamBooth-style few-shot, if supported by the local setup). Record outcome.

- [ ] **Step 3: Decide the Generate component**

If Flux gives usable layout/region control → Generate adapter wraps Flux. Else → fall back to the survey's off-the-shelf choice (ODGEN or DreamBooth+X-Paste / SD). Write findings to `flux-capability-probe.md` and update the Generate line in `demo-task-selection.md`.

- [ ] **Step 4: Commit**

```bash
git add pipeline/decisions
git commit -m "docs(pipeline): Flux capability probe + final Generate choice"
```

---

### Task 5: Rule-based Specifier (real, fully coded)

> The Specifier is pure logic over the contracts, so it is implemented concretely now (independent of the survey choices).

**Files:**
- Create: `pipeline/pipeline/specifier.py`
- Create: `pipeline/tests/test_specifier.py`

**Interfaces:**
- Consumes: `list[Slice]`, `GenSpec`, `GenItem` from Task 1; subclasses `Specifier` from Task 2.
- Produces: `RuleSpecifier(per_slice_cap: int).make_spec(slices, budget) -> GenSpec` — allocates the budget across slices in proportion to severity (worst first), capping per slice, emitting one `GenItem` per addressed slice.

- [ ] **Step 1: Write the failing test**

`pipeline/tests/test_specifier.py`:
```python
from pipeline.contracts import Slice
from pipeline.specifier import RuleSpecifier

def _slices():
    return [
        Slice(description="small+occluded", members=["a", "b", "c"], metric=0.10, severity=0.9),
        Slice(description="low-light", members=["d"], metric=0.25, severity=0.3),
    ]

def test_worst_slice_gets_most_budget():
    spec = RuleSpecifier(per_slice_cap=1000).make_spec(_slices(), budget=100)
    by_target = {i.target: i.count for i in spec.items}
    assert by_target["small+occluded"] > by_target["low-light"]
    assert sum(by_target.values()) <= 100

def test_per_slice_cap_respected():
    spec = RuleSpecifier(per_slice_cap=5).make_spec(_slices(), budget=100)
    assert all(i.count <= 5 for i in spec.items)

def test_conditions_carry_slice_description():
    spec = RuleSpecifier(per_slice_cap=1000).make_spec(_slices(), budget=10)
    assert any("small+occluded" in i.conditions for i in spec.items)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest pipeline/tests/test_specifier.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.specifier'`.

- [ ] **Step 3: Write the implementation**

`pipeline/pipeline/specifier.py`:
```python
"""Rule-based Specifier: allocate generation budget by slice severity."""
from .contracts import GenItem, GenSpec
from .interfaces import Specifier


class RuleSpecifier(Specifier):
    def __init__(self, per_slice_cap: int = 1000):
        self.per_slice_cap = per_slice_cap

    def make_spec(self, slices, budget):
        if not slices:
            return GenSpec(items=[])
        total_sev = sum(s.severity for s in slices) or 1.0
        items = []
        for s in sorted(slices, key=lambda x: x.severity, reverse=True):
            share = int(budget * (s.severity / total_sev))
            count = min(share, self.per_slice_cap)
            if count > 0:
                items.append(GenItem(target=s.description,
                                     conditions=f"prompt: {s.description}",
                                     count=count))
        return GenSpec(items=items)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest pipeline/tests/test_specifier.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/pipeline/specifier.py pipeline/tests/test_specifier.py
git commit -m "feat(pipeline): rule-based Specifier (severity-proportional budget)"
```

---

### Task 6: Real Diagnoser adapter (chosen tool, on the demo dataset)

> Adapter wrapping the diagnosis tool selected in Task 3. The contract-conformance test is fully specified; the internal call uses the chosen repo's API (read its README; cite the exact entrypoint in a code comment).

**Files:**
- Create: `pipeline/pipeline/diagnose_real.py`
- Create: `pipeline/tests/test_diagnose_real.py`
- Modify: `pipeline/requirements.txt` (add the chosen tool's deps + `torch`, `ultralytics`)

**Interfaces:**
- Consumes: a fine-tuned baseline detector + the demo dataset (paths from `demo-task-selection.md`); subclasses `Diagnoser`.
- Produces: `RealDiagnoser(...).diagnose(model, dataset) -> list[Slice]` where each `Slice.members` are real dataset sample ids and `Slice.metric` is the slice's AP from the detector's eval.

- [ ] **Step 1: Write the conformance test (with a small real/fixture eval)**

`pipeline/tests/test_diagnose_real.py`:
```python
import pytest
from pipeline.contracts import Slice

ru = pytest.importorskip("pipeline.diagnose_real")

def test_diagnose_returns_valid_slices(tiny_demo_model, tiny_demo_dataset):
    # tiny_demo_model / tiny_demo_dataset: fixtures pointing at a few-image
    # subset of the chosen demo dataset (paths from demo-task-selection.md).
    slices = ru.RealDiagnoser().diagnose(tiny_demo_model, tiny_demo_dataset)
    assert slices, "diagnoser must surface at least one slice"
    for s in slices:
        assert isinstance(s, Slice)
        assert s.description and isinstance(s.members, list)
        assert 0.0 <= s.metric <= 1.0
```

Add the two fixtures to `pipeline/tests/conftest.py` pointing at the few-image subset named in `demo-task-selection.md`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest pipeline/tests/test_diagnose_real.py -q`
Expected: FAIL — module/fixtures not defined.

- [ ] **Step 3: Implement the adapter**

`pipeline/pipeline/diagnose_real.py`: subclass `Diagnoser`; inside `diagnose`, (a) run the detector over `dataset`, (b) call the chosen slice-discovery tool (HiBug2 or GH-ESD — exact entrypoint per its README, cited in a comment) to get error slices, (c) map each tool slice to a `Slice(description=<tool label>, members=<sample ids>, metric=<slice AP>, severity=1 - slice AP)`. Keep all tool-specific code inside this file so no other module imports the tool.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest pipeline/tests/test_diagnose_real.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pipeline/pipeline/diagnose_real.py pipeline/tests/test_diagnose_real.py pipeline/tests/conftest.py pipeline/requirements.txt
git commit -m "feat(pipeline): real Diagnoser adapter on demo dataset"
```

---

### Task 7: Real Generator adapter (chosen component)

> Adapter wrapping the Generate component decided in Task 4 (Flux, or ODGEN, or DreamBooth+X-Paste). Conformance test fully specified; generation call per the chosen tool.

**Files:**
- Create: `pipeline/pipeline/generate_real.py`
- Create: `pipeline/tests/test_generate_real.py`

**Interfaces:**
- Consumes: `GenSpec` from Task 1; subclasses `Generator`.
- Produces: `RealGenerator(out_dir, ...).generate(spec) -> SyntheticDataset` writing real images to `out_dir` and a COCO-format `annotations_path` matching the demo dataset's schema.

- [ ] **Step 1: Write the conformance test**

`pipeline/tests/test_generate_real.py`:
```python
import json, os, pytest
from pipeline.contracts import GenSpec, GenItem

gr = pytest.importorskip("pipeline.generate_real")

def test_generate_produces_images_and_coco_annotations(tmp_path):
    spec = GenSpec(items=[GenItem(target="small+occluded",
                                  conditions="prompt: small ebike, occluded", count=2)])
    out = gr.RealGenerator(out_dir=str(tmp_path)).generate(spec)
    assert os.path.isdir(out.images_dir)
    with open(out.annotations_path) as f:
        ann = json.load(f)
    assert "images" in ann and "annotations" in ann
    assert len(ann["images"]) >= 1  # produced at least one image for the spec
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest pipeline/tests/test_generate_real.py -q`
Expected: FAIL — module not defined.

- [ ] **Step 3: Implement the adapter**

`pipeline/pipeline/generate_real.py`: subclass `Generator`; for each `GenItem`, call the chosen generator `count` times with `conditions` (exact API per the tool's README / the local Flux scripts, cited in a comment), save images to `out_dir`, and build COCO `images`/`annotations` entries (boxes from layout-conditioned generation, or from copy-paste masks). Return `SyntheticDataset(images_dir=out_dir, annotations_path=<coco json>)`. Keep all generator-specific code in this file.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest pipeline/tests/test_generate_real.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pipeline/pipeline/generate_real.py pipeline/tests/test_generate_real.py
git commit -m "feat(pipeline): real Generator adapter (chosen component)"
```

---

### Task 8: Real CloseLooper (filter + accumulate + retrain + evaluate)

**Files:**
- Create: `pipeline/pipeline/closeloop_real.py`
- Create: `pipeline/tests/test_closeloop_real.py`

**Interfaces:**
- Consumes: a model handle + real dataset + `SyntheticDataset`; subclasses `CloseLooper`.
- Produces: `RealCloseLooper(filter_fn, eval_slices).close_loop(model, real, synth) -> Report` — filters `synth`, builds an accumulated (real + filtered synth) training set, retrains from the baseline weights, evaluates on the **synthetic-free** eval set, and fills `Report` including `per_slice_delta`.

- [ ] **Step 1: Write the tests (filter + accumulation logic, mockable)**

`pipeline/tests/test_closeloop_real.py`:
```python
import json, pytest
from pipeline.contracts import SyntheticDataset, Report

cl = pytest.importorskip("pipeline.closeloop_real")

def test_filter_drops_low_score(tmp_path):
    looper = cl.RealCloseLooper(filter_fn=lambda img, cond: False, eval_slices=[])
    kept = looper._filter(SyntheticDataset(images_dir=str(tmp_path), annotations_path="x"))
    assert kept == []  # everything filtered out -> empty

def test_too_few_survivors_skips_round(tmp_path, monkeypatch):
    looper = cl.RealCloseLooper(filter_fn=lambda img, cond: False, eval_slices=[],
                                min_survivors=1)
    rep = looper.close_loop(model="m", real=["r"],
                            synth=SyntheticDataset(images_dir=str(tmp_path), annotations_path="x"))
    assert isinstance(rep, Report) and rep.iterate is False
    assert rep.augmented_metric == rep.baseline_metric  # skipped: no change

def test_accumulation_never_drops_real(tmp_path):
    looper = cl.RealCloseLooper(filter_fn=lambda img, cond: True, eval_slices=[])
    train = looper._build_training_set(real=["r1", "r2"], kept_synth=["s1"])
    assert "r1" in train and "r2" in train and "s1" in train
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest pipeline/tests/test_closeloop_real.py -q`
Expected: FAIL — module not defined.

- [ ] **Step 3: Implement the CloseLooper**

`pipeline/pipeline/closeloop_real.py`: subclass `CloseLooper`. Implement `_filter` (apply `filter_fn` per generated image; return survivors), `_build_training_set` (real + kept synth, **never dropping real**), and `close_loop` (if survivors < `min_survivors`: return a no-change `Report(iterate=False)` with a warning; else retrain from baseline weights via `ultralytics` on the accumulated set, evaluate on the synthetic-free eval set, compute overall + `per_slice_delta` against `eval_slices`, set `iterate=False` for the single-round v1). External calls (ultralytics train/val) per its docs, cited in comments.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest pipeline/tests/test_closeloop_real.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pipeline/pipeline/closeloop_real.py pipeline/tests/test_closeloop_real.py
git commit -m "feat(pipeline): real CloseLooper (filter/accumulate/retrain/eval)"
```

---

### Task 9: Run the vertical slice + write the result report

**Files:**
- Create: `pipeline/run_vertical_slice.py`
- Create: `pipeline/decisions/vertical-slice-result.md`

**Interfaces:**
- Consumes: `run_loop` (Task 2), `RealDiagnoser` (6), `RealGenerator` (7), `RuleSpecifier` (5), `RealCloseLooper` (8), and the choices in `demo-task-selection.md`.
- Produces: a CLI entrypoint that runs one real round and a written result.

- [ ] **Step 1: Write the runner**

`pipeline/run_vertical_slice.py`: load the baseline detector (pretrained → fine-tuned per `demo-task-selection.md`), build `RealDiagnoser`, `RuleSpecifier`, `RealGenerator`, `RealCloseLooper` (with the chosen `filter_fn`), call `run_loop(..., budget=<from decision doc>, max_rounds=1)`, and print + save the returned `Report`(s) as JSON next to the result doc.

- [ ] **Step 2: Run the vertical slice**

Run: `python3 pipeline/run_vertical_slice.py`
Expected: completes one round end-to-end, prints baseline vs augmented + `per_slice_delta`, writes the JSON.

- [ ] **Step 3: Write the result report**

`pipeline/decisions/vertical-slice-result.md`: record baseline metric, augmented metric, per-slice delta (esp. the targeted slice), the components used, and an honest interpretation (up/flat/down + likely why). Link back to GAPS G1/G4 — did the end-to-end detection loop + slice→spec bridge work in practice.

- [ ] **Step 4: Commit**

```bash
git add pipeline/run_vertical_slice.py pipeline/decisions/vertical-slice-result.md
git commit -m "feat(pipeline): run vertical slice + result report"
```

---

## Self-Review

**Spec coverage:**
- §1 goal/scope/DoD → Tasks 1–9 deliver the end-to-end run; success "up/flat/down all valid" encoded in Task 9 Step 3 + Global Constraints. ✅
- §2 four modules + four contracts + interface principles → Task 1 (contracts), Task 2 (interfaces/dummies/orchestrator + boundary-swap test), Tasks 5–8 (real impls). ✅
- §3 Step A survey/demo selection → Task 3; Flux probe (first concrete action) → Task 4; vertical-slice run → Task 9; integration with kg/GAPS → Tasks 3 & 9. ✅
- §4 testing layers → unit (1,2,5,6,7,8), integration smoke on fake data (Task 2), boundary check (Task 2); scientific rigor (synthetic-free eval, per-slice delta) → Task 8/9; error handling (skip round on too-few survivors, accumulate-not-replace) → Task 8; risk mitigations → Tasks 3 (public set, checklist), 4 (Flux fallback). ✅
- §5 open questions → resolved in Tasks 3 (task/dataset, Diagnose impl) and 4 (Generate component). ✅

**Placeholder scan:** Tasks 1, 2, 5 are fully coded (no placeholders). Tasks 6–8 are *adapter* tasks whose contract-conformance tests and adapter responsibilities are fully specified; the single irreducible deferral is the external repo's exact API call, which is unknowable until Task 3/4 lock the component — flagged explicitly in each task, not hidden as "TODO". This mirrors the prior knowledge-tree plan's treatment of necessarily-procedural research tasks. Tasks 3–4 are decision deliverables with concrete exit criteria and doc structure.

**Type consistency:** contract field names are frozen in Global Constraints and used identically across Tasks 1–9. Method signatures `diagnose/make_spec/generate/close_loop` and `run_loop(...)` match between Task 2 ABCs, Task 2 dummies, and Tasks 5–9 real impls.
