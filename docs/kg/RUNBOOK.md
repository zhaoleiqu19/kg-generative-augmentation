# Ingestion Runbook (one batch)

1. User names a target (survey / subtopic / "fill stage1-diagnosis").
2. Agent loads WebSearch/WebFetch, searches, returns CANDIDATE LIST (title + url) — writes nothing yet.
3. User picks which candidates get full notes.
4. Agent WebFetches each pick; drafts `90-papers/authorYEAR-name.md` from fetched text only.
5. Agent wires the atom into the **current views**: register it in `MAP.md` (global atom list), reference it from the relevant `50-alignment/` view (`survey-*` / `representation-map`) and tag its **representation** (box / region / attribute-text / instance-mask); append any new gap to the current gaps file (`GAPS.md` until `50-alignment/alignment-gaps.md` takes over). For Phase 0–4 concept nodes (`00–30`), still wire there if relevant.
6. Agent reports: found N, fetched M, couldn't verify K.
7. Run `python3 docs/kg/tools/validate_kg.py` → must exit 0. Commit.

Guardrails: no note without a fetched http url; memory-only drafts tagged `unverified`; concept nodes never link unverified papers; every number carries its source.
