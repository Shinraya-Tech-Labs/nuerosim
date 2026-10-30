from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T154_viewport_lod_policy_unit():
    result = run_fixture(Path("tests/fixtures/omega/T154-viewport-lod-policy/valid.json"))
    assert result["task"] == "T154"
    assert result["result"]["status"] == "pass"

