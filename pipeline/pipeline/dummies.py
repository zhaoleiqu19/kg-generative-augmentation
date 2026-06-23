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
