from pytest import approx
from pipeline.contracts import Slice, GenItem, GenSpec, SyntheticDataset, Report

def test_slice_fields():
    s = Slice(description="small+occluded", members=["a", "b"], metric=0.12, severity=0.9)
    assert s.members == ["a", "b"] and s.metric == 0.12

def test_genspec_holds_items():
    spec = GenSpec(items=[GenItem(target="small+occluded", conditions="prompt: small ebike, occluded", count=50)])
    assert spec.items[0].count == 50

def test_report_fields():
    r = Report(baseline_metric=0.30, augmented_metric=0.34, per_slice_delta={"small+occluded": 0.06}, iterate=False)
    assert r.augmented_metric - r.baseline_metric == approx(0.04)
    assert r.per_slice_delta["small+occluded"] == 0.06

def test_synthetic_dataset_paths():
    d = SyntheticDataset(images_dir="/tmp/x", annotations_path="/tmp/x/ann.json")
    assert d.annotations_path.endswith(".json")
