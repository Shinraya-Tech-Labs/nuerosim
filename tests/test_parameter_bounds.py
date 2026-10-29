import json
from pathlib import Path

import pytest

from neurosim.parameter_bounds import audit_schema


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
