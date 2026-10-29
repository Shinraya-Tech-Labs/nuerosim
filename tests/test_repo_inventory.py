import json
import os
from pathlib import Path
import subprocess
import sys

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


def test_T001_repo_tree_provenance_inventory_cli_integration():
    root = Path(__file__).resolve().parents[1]
    env = os.environ | {"PYTHONPATH": str(root / "python")}
    valid = subprocess.run(
        [sys.executable, "-m", "neurosim.repo_inventory", "HEAD"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert valid.returncode == 0, valid.stderr
    output = json.loads(valid.stdout)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert output["revision"] == head
    assert output["tracked_files"] == len(output["paths"])

    fixture = json.loads(
        (root / "tests/fixtures/omega/T001-repo-tree-provenance-inventory/invalid.json").read_text(
            encoding="utf-8"
        )
    )
    invalid = subprocess.run(
        [sys.executable, "-m", "neurosim.repo_inventory", fixture["revision"]],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert invalid.returncode == 2
    assert fixture["expected_error"] in invalid.stderr
