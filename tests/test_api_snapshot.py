import json
from pathlib import Path

import pytest

from neurosim.api_snapshot import build_snapshot


def test_T004_api_endpoint_contract_snapshot_unit():
    fixture = json.loads(
        Path("tests/fixtures/omega/T004-api-endpoint-contract-snapshot/valid.json").read_text(
            encoding="utf-8"
        )
    )

    result = build_snapshot(fixture["schema"])

    assert result["schema"] == fixture["schema"]
    assert result["operation_count"] == fixture["expected"]["operation_count"]
    assert result["sha256"] == fixture["expected"]["sha256"]


def test_T004_api_endpoint_contract_snapshot_rejects_invalid_paths():
    fixture = json.loads(
        Path("tests/fixtures/omega/T004-api-endpoint-contract-snapshot/invalid.json").read_text(
            encoding="utf-8"
        )
    )

    with pytest.raises(ValueError, match=fixture["expected_error"]):
        build_snapshot(fixture["schema"])


def test_T004_api_endpoint_contract_snapshot_empty_paths_boundary():
    first = build_snapshot({"openapi": "3.1.0", "paths": {}})
    second = build_snapshot({"paths": {}, "openapi": "3.1.0"})

    assert first["operation_count"] == 0
    assert first["sha256"] == second["sha256"]
