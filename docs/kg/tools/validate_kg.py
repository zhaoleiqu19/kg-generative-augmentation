#!/usr/bin/env python3
"""Validate the docs/kg knowledge tree: frontmatter, links, guardrails."""
import re
import sys
import pathlib

CONCEPT_DIRS = ("00-foundations", "10-landscape", "20-loop", "30-anchor-task")
REQUIRED = ("title", "authors", "year", "url", "loop-stage", "tags")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def _frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def validate(root):
    root = pathlib.Path(root)
    errors = []
    for home in ("MAP.md", "GAPS.md"):
        if not (root / home).exists():
            errors.append(f"{home} missing")

    md = list(root.rglob("*.md"))
    stems = {p.stem for p in md}
    unverified = set()

    papers = root / "90-papers"
    for p in papers.rglob("*.md") if papers.exists() else []:
        text = p.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        if fm is None:
            errors.append(f"{p.name}: missing frontmatter")
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{p.name}: frontmatter missing '{key}'")
        url = fm.get("url", "")
        if url and not url.startswith("http"):
            errors.append(f"{p.name}: url must start with http (got '{url}')")
        if "unverified" in fm.get("tags", ""):
            unverified.add(p.stem)

    for p in md:
        text = p.read_text(encoding="utf-8")
        is_concept = any(part in CONCEPT_DIRS for part in p.parts)
        for raw in LINK_RE.findall(text):
            target = raw.split("|")[0].split("#")[0].strip()
            if not target:
                continue
            if target not in stems:
                errors.append(f"{p.name}: broken link [[{target}]]")
            elif is_concept and target in unverified:
                errors.append(f"{p.name}: concept node links unverified paper [[{target}]]")
    return errors


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    errors = validate(root)
    if errors:
        print("KG VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    print("KG validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
