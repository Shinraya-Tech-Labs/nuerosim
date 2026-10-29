import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from neurosim.module_boundaries import parse_project_scripts, summarize_boundaries


def test_T003_legacy_modules_boundary_map_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T003-legacy-modules-boundary-map/valid.json").read_text(
            encoding="utf-8"
        )
    )

    result = summarize_boundaries(
        fixture["paths"], fixture["project_scripts"], fixture["revision"]
    )

    assert result == fixture["expected"]


def test_T003_malformed_pyproject_fixture_has_clear_error():
    fixture = json.loads(
        Path("tests/fixtures/omega/T003-legacy-modules-boundary-map/invalid.json").read_text(
            encoding="utf-8"
        )
    )

    with pytest.raises(ValueError, match=fixture["expected_error"]):
        parse_project_scripts(fixture["pyproject_contents"])


def test_T003_legacy_modules_boundary_map_empty_and_prefix_boundary():
    result = summarize_boundaries(
        [], {"unrelated": "neurosim.workbenchish.cli:main"}, "empty-tree"
    )

    assert result == {
        "revision": "empty-tree",
        "legacy_modules": [],
        "archived_legacy_files": [],
        "entry_points": {
            "neurosim.workbench": {},
            "neurosim.legacy": {},
            "other": {"unrelated": "neurosim.workbenchish.cli:main"},
        },
        "legacy_module_count": 0,
        "archived_file_count": 0,
        "entry_point_count": 1,
    }


def test_T003_legacy_modules_boundary_map_cli_integration():
    root = Path(__file__).resolve().parents[1]
    env = os.environ | {"PYTHONPATH": str(root / "python")}
    run = subprocess.run(
        [sys.executable, "-m", "neurosim.module_boundaries", "HEAD"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr
    result = json.loads(run.stdout)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True
    ).stdout.strip()

    assert result["revision"] == head
    assert result["legacy_modules"] == ["python/neurosim/legacy_cli.py"]
    assert result["archived_file_count"] == len(result["archived_legacy_files"])
    assert result["entry_points"]["neurosim.workbench"]["neurosim"] == (
        "neurosim.workbench.cli:main"
    )
    assert result["entry_points"]["neurosim.legacy"] == {}
