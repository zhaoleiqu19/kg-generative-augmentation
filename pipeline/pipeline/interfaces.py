"""Abstract module interfaces. Real components and dummies both subclass these."""
import abc
from typing import List
from .contracts import Slice, GenSpec, SyntheticDataset, Report


class Diagnoser(abc.ABC):
    @abc.abstractmethod
    def diagnose(self, model, dataset) -> List[Slice]: ...


class Specifier(abc.ABC):
    @abc.abstractmethod
    def make_spec(self, slices: List[Slice], budget: int) -> GenSpec: ...


class Generator(abc.ABC):
    @abc.abstractmethod
    def generate(self, spec: GenSpec) -> SyntheticDataset: ...


class CloseLooper(abc.ABC):
    @abc.abstractmethod
    def close_loop(self, model, real, synth: SyntheticDataset) -> Report: ...
