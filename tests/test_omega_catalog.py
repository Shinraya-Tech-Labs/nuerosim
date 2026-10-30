"""Shared coverage for the fixture-backed T151-T210 task catalog.

The catalog keeps one unit, CLI, and malformed-input contract per task while
avoiding one nearly-identical Python module for every fixture.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.omega_final import run_fixture, run_task


FIXTURES = sorted(
    path
    for path in Path("tests/fixtures/omega").glob("T*/valid.json")
    if 151 <= int(path.parent.name[1:4]) <= 210
)


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda path: path.parent.name)
def test_catalog_fixture(fixture):
    result = run_fixture(fixture)
    assert result["task"] == json.loads(fixture.read_text(encoding="utf-8"))["task"]
    assert result["result"]["status"] == "pass"


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda path: path.parent.name)
def test_catalog_cli(fixture):
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.omega_final", "--fixture", str(fixture)],
        env={**os.environ, "PYTHONPATH": str(Path("python").resolve())},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["task"]


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda path: path.parent.name)
def test_catalog_empty_input_is_controlled(fixture):
    task = json.loads(fixture.read_text(encoding="utf-8"))["task"]
    with pytest.raises(ValueError):
        run_task(task, {"input": {}})
