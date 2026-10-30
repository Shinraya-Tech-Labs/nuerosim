from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T208_accessibility_screenshot_audit_unit():
    result = run_fixture(Path("tests/fixtures/omega/T208-accessibility-screenshot-audit/valid.json"))
    assert result["task"] == "T208"
    assert result["result"]["status"] == "pass"

