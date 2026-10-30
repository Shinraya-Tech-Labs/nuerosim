from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T206_windows_clean_install_validation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T206-windows-clean-install-validation/valid.json"))
    assert result["task"] == "T206"
    assert result["result"]["status"] == "pass"

