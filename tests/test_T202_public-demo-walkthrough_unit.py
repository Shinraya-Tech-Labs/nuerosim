from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T202_public_demo_walkthrough_unit():
    result = run_fixture(Path("tests/fixtures/omega/T202-public-demo-walkthrough/valid.json"))
    assert result["task"] == "T202"
    assert result["result"]["status"] == "pass"

