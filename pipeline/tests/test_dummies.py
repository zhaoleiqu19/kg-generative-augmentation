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
