# Anchor Task — Elevator E-bike Detection (STUB)

> The testbed: detecting electric mopeds / e-bikes entering elevators from CCTV, used to make every gap *demonstrable*.

## What it is
A small-object, often-occluded detection task on elevator surveillance footage: flag when an e-bike is brought into the cabin (a fire-safety violation in many jurisdictions).

## Why it matters
It is the concrete yardstick for the whole project: a candidate gap only counts if it can be shown on this task. Its regime (small, occluded, cluttered, variable lighting) is exactly the one the landscape's "helps" results do *not* yet cover.

## Key papers
- [[nikouei2025-small-object-detection-survey]] — characterizes the small-object regime (occlusion, class imbalance, size-specific AP) this task lives in.

## Open questions
- What public datasets exist for elevator/e-bike/indoor-surveillance detection? (Phase 5: `public-datasets.md`)
- What are the dominant failure modes here — door occlusion, scale, motion blur, low light? (Phase 5: `known-hard-cases.md`)
- Does the existing local Flux generation pipeline already target these hard cases?

## Our take
Stub. Phase 5 fills datasets + hard cases and scores the 3 GAPS for feasibility here. Hard cases should link to the local elevator/e-bike prompt work in this workspace.
