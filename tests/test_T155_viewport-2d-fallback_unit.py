from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T155_viewport_2d_fallback_unit():
    result = run_fixture(Path("tests/fixtures/omega/T155-viewport-2d-fallback/valid.json"))
    assert result["task"] == "T155"
    assert result["result"]["status"] == "pass"

