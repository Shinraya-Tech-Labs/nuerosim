from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T183_auth_mode_design_for_public_demo_unit():
    result = run_fixture(Path("tests/fixtures/omega/T183-auth-mode-design-for-public-demo/valid.json"))
    assert result["task"] == "T183"
    assert result["result"]["status"] == "pass"

