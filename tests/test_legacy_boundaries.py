import json
from pathlib import Path

import pytest

from neurosim.legacy_boundaries import parse_project_scripts, summarize_boundaries


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
