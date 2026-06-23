import pathlib
from validate_kg import validate

def _scaffold(root):
    (root / "90-papers").mkdir(parents=True)
    (root / "00-foundations").mkdir()
    (root / "MAP.md").write_text("# Map\n")
    (root / "GAPS.md").write_text("# Gaps\n")

def _paper(root, stem, **fm):
    base = {"title": "T", "authors": "A", "year": "2024",
            "url": "http://x", "loop-stage": "stage1", "tags": "x"}
    base.update(fm)
    body = "---\n" + "\n".join(f"{k}: {v}" for k, v in base.items()) + "\n---\nbody\n"
    (root / "90-papers" / f"{stem}.md").write_text(body)

def test_clean_tree_passes(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo")
    assert validate(tmp_path) == []

def test_missing_map_fails(tmp_path):
    _scaffold(tmp_path)
    (tmp_path / "MAP.md").unlink()
    assert any("MAP.md" in e for e in validate(tmp_path))

def test_missing_frontmatter_key_fails(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", url="")
    assert any("url" in e for e in validate(tmp_path))

def test_non_http_url_fails(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", url="arxiv-2401")
    assert any("http" in e for e in validate(tmp_path))

def test_broken_link_fails(tmp_path):
    _scaffold(tmp_path)
    (tmp_path / "00-foundations" / "c.md").write_text("see [[nope]]\n")
    assert any("broken link" in e for e in validate(tmp_path))

def test_concept_cannot_link_unverified(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", tags="unverified")
    (tmp_path / "00-foundations" / "c.md").write_text("[[smith2024-foo]]\n")
    assert any("unverified" in e for e in validate(tmp_path))

def test_missing_title_fails(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo", title="")
    assert any("title" in e for e in validate(tmp_path))

def test_missing_gaps_fails(tmp_path):
    _scaffold(tmp_path)
    (tmp_path / "GAPS.md").unlink()
    assert any("GAPS.md" in e for e in validate(tmp_path))

def test_body_unverified_mention_does_not_block(tmp_path):
    _scaffold(tmp_path)
    _paper(tmp_path, "smith2024-foo")
    note = tmp_path / "90-papers" / "smith2024-foo.md"
    note.write_text(note.read_text() + "\nmentions #unverified in prose\n")
    (tmp_path / "00-foundations" / "c.md").write_text("[[smith2024-foo]]\n")
    assert validate(tmp_path) == []

def test_template_placeholder_links_ignored(tmp_path):
    _scaffold(tmp_path)
    (tmp_path / "_templates").mkdir()
    (tmp_path / "_templates" / "concept-node.md").write_text("[[authorYEAR-name]]\n")
    assert validate(tmp_path) == []
