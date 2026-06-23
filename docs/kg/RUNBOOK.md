# Ingestion Runbook (one batch)

1. User names a target (survey / subtopic / "fill stage1-diagnosis").
2. Agent loads WebSearch/WebFetch, searches, returns CANDIDATE LIST (title + url) — writes nothing yet.
3. User picks which candidates get full notes.
4. Agent WebFetches each pick; drafts `90-papers/authorYEAR-name.md` from fetched text only.
5. Agent updates the concept node, MAP.md (new wikilink), appends any gap to GAPS.md.
6. Agent reports: found N, fetched M, couldn't verify K.
7. Run `python docs/kg/tools/validate_kg.py` → must exit 0. Commit.

Guardrails: no note without a fetched http url; memory-only drafts tagged `unverified`; concept nodes never link unverified papers; every number carries its source.
