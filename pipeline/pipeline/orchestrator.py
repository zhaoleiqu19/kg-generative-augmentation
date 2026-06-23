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
