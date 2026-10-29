import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.baseline_signoff import audit_file, validate_signoff


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/omega/T015-risk-register-and-baseline-signoff"


def test_T015_risk_register_and_baseline_signoff_unit():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    report = audit_file(FIXTURES / "valid.json")
    assert report["baseline_gate_passed"] is fixture["expected"]["baseline_gate_passed"] is True
    assert report["required_check_count"] == fixture["expected"]["required_check_count"] == 4
    assert report["risk_count"] == fixture["expected"]["risk_count"] == 1
    assert report["accepted_risks"] == ["webgpu"]


def test_invalid_fixture_is_rejected():
    with pytest.raises(ValueError, match="full 40-character Git SHA"):
        audit_file(FIXTURES / "invalid.json")


def test_failed_required_check_blocks_signoff():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["checks"][0]["status"] = "failed"
    report = validate_signoff(fixture)
    assert report["baseline_gate_passed"] is False
    assert report["failed_checks"] == ["python"]


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda data: data.update(risks=[]), "risks must be a non-empty list"),
        (lambda data: data["risks"][0].update(disposition="open"), "invalid disposition"),
        (lambda data: data["checks"].append(copy.deepcopy(data["checks"][0])), "IDs must be unique"),
    ],
)
def test_invalid_risk_or_duplicate_check_rejected(mutate, message):
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    mutate(fixture)
    with pytest.raises(ValueError, match=message):
        validate_signoff(fixture)


def test_missing_required_check_leaves_gate_failed():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["checks"] = fixture["checks"][:-1]
    report = validate_signoff(fixture)
    assert report["baseline_gate_passed"] is False
    assert report["missing_checks"] == ["web-e2e"]


def test_invalid_risk_severity_or_empty_evidence_is_rejected():
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["risks"][0]["severity"] = "urgent"
    with pytest.raises(ValueError, match="invalid severity"):
        validate_signoff(fixture)
    fixture = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    fixture["checks"][0]["evidence"] = " "
    with pytest.raises(ValueError, match="non-empty evidence"):
        validate_signoff(fixture)


def test_cli_emits_signoff_json():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.baseline_signoff", str(FIXTURES / "valid.json")],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["baseline_gate_passed"] is True
