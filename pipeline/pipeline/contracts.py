"""Data contracts — the only coupling points between pipeline modules."""
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Slice:
    description: str          # human-readable, e.g. "small + occluded"
    members: List[str]        # sample ids locating the failing examples
    metric: float             # AP/acc on this slice
    severity: float           # higher = worse / more urgent to fix


@dataclass(frozen=True)
class GenItem:
    target: str               # the slice description this item addresses
    conditions: str           # free field: prompt / layout / region spec
    count: int                # how many to generate


@dataclass(frozen=True)
class GenSpec:
    items: List[GenItem]


@dataclass(frozen=True)
class SyntheticDataset:
    images_dir: str           # directory of generated images
    annotations_path: str     # COCO-format json, same schema as the real set


@dataclass(frozen=True)
class Report:
    baseline_metric: float
    augmented_metric: float
    per_slice_delta: Dict      # slice description -> metric delta
    iterate: bool              # whether the orchestrator should run another round
