import json
from pathlib import Path

from neurosim.repo_inventory import summarize_paths


def test_T001_repo_tree_provenance_inventory_unit():
    fixture = json.loads(
        Path(
            "tests/fixtures/omega/T001-repo-tree-provenance-inventory/valid.json"
        ).read_text(encoding="utf-8")
    )

    result = summarize_paths(fixture["paths"], "fixture-revision")

    assert result["tracked_files"] == fixture["expected"]["tracked_files"]
    assert result["by_top_level"] == fixture["expected"]["by_top_level"]
    assert result["by_extension"] == fixture["expected"]["by_extension"]
    assert result["paths"] == sorted(fixture["paths"])


def test_T001_repo_tree_provenance_inventory_empty_tree_boundary():
    assert summarize_paths([], "empty-tree") == {
        "revision": "empty-tree",
        "tracked_files": 0,
        "by_top_level": {},
        "by_extension": {},
        "paths": [],
    }
