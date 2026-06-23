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
