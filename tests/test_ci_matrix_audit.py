import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.ci_matrix_audit import audit_workflow, audit_workflows


FIXTURES = Path("tests/fixtures/omega/T010-ci-platform-matrix-audit")


def test_valid_matrix_fixture_reports_eight_combinations():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_workflow(FIXTURES / "valid.json")
    expected = fixture["expected"]
    job = report["jobs"][0]
    assert report["job_count"] == expected["job_count"] == 1
    assert report["matrix_combinations"] == expected["matrix_combinations"] == 8
    assert job["platforms"] == expected["platforms"]
    assert job["runtime_axes"] == expected["runtime_axes"]


def test_invalid_matrix_axis_is_rejected():
    with pytest.raises(ValueError, match="matrix axis python must be a non-empty list"):
        audit_workflow(FIXTURES / "invalid.json")


def test_empty_matrix_axis_is_rejected(tmp_path):
    path = tmp_path / "empty-matrix.json"
    path.write_text('{"jobs":{"job":{"strategy":{"matrix":{"os":[]}}}}}', encoding="utf-8")
    with pytest.raises(ValueError, match="non-empty scalar list"):
        audit_workflow(path)


def test_missing_runner_is_reported_without_inference(tmp_path):
    path = tmp_path / "unknown-runner.json"
    path.write_text('{"jobs":{"job":{"steps":[]}}}', encoding="utf-8")
    job = audit_workflow(path)["jobs"][0]
    assert job["platforms"] == []
    assert job["matrix_combinations"] == 1


def test_repository_workflows_report_declared_coverage():
    report = audit_workflows(
        [".github/workflows/web.yml", ".github/workflows/cpu.yml"]
    )
    cpu, web = report["workflows"]
    tests_job = next(job for job in cpu["jobs"] if job["job"] == "tests")
    web_job = web["jobs"][0]
    assert (report["job_count"], report["matrix_combinations"]) == (4, 11)
    assert tests_job["matrix_combinations"] == 8
    assert tests_job["platforms"] == ["ubuntu-latest", "windows-latest"]
    assert tests_job["runtime_axes"]["python"] == ["3.11", "3.12", "3.13", "3.14"]
    assert web_job["runtime_axes"] == {"node": ["22.23.0"], "python": ["3.12"]}


def test_cli_emits_json_for_repository_workflows():
    env = {**os.environ, "PYTHONPATH": "python"}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "neurosim.ci_matrix_audit",
            ".github/workflows/cpu.yml",
        ],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    assert json.loads(result.stdout)["matrix_combinations"] == 10
