import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from neurosim.parameter_bounds import audit_schema
from neurosim.workbench.config import Experiment


def test_T006_model_parameter_bounds_audit_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T006-model-parameter-bounds-audit/valid.json").read_text(
            encoding="utf-8"
        )
    )

    assert audit_schema(fixture["schema"]) == fixture["expected"]


def test_T006_model_parameter_bounds_audit_rejects_out_of_range_default():
    fixture = json.loads(
        Path("tests/fixtures/omega/T006-model-parameter-bounds-audit/invalid.json").read_text(
            encoding="utf-8"
        )
    )

    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_schema(fixture["schema"])


def test_T006_model_parameter_bounds_audit_exclusive_boundary():
    schema = {
        "properties": {
            "stop": {"type": "number", "default": 0, "exclusiveMinimum": 0}
        }
    }

    with pytest.raises(ValueError, match="default is outside declared bounds"):
        audit_schema(schema)


def test_T006_model_parameter_bounds_audit_workbench_integration():
    report = audit_schema(Experiment.model_json_schema())
    dt = next(
        item
        for item in report["bounds"]
        if item["model"] == "Experiment" and item["field"] == "dt"
    )

    assert report["status"] == "pass"
    assert report["field_count"] == 40
    assert (dt["default"], dt["minimum"], dt["maximum"]) == (0.025, 0.001, 0.025)


def test_T006_model_parameter_bounds_audit_cli():
    root = Path(__file__).resolve().parents[1]
    env = os.environ | {"PYTHONPATH": str(root / "python")}
    run = subprocess.run(
        [sys.executable, "-m", "neurosim.parameter_bounds"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout) == audit_schema(Experiment.model_json_schema())
