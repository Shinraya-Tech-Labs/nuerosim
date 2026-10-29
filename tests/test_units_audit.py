import json
from pathlib import Path

import pytest

from neurosim.units_audit import audit_units


def test_T005_scientific_units_audit_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T005-scientific-units-audit/valid.json").read_text(
            encoding="utf-8"
        )
    )

    assert audit_units(fixture["result"]) == fixture["expected"]


def test_T005_scientific_units_audit_rejects_wrong_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T005-scientific-units-audit/invalid.json").read_text(
            encoding="utf-8"
        )
    )

    with pytest.raises(ValueError, match=fixture["expected_error"]):
        audit_units(fixture["result"])
