from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T207_linux_clean_install_validation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T207-linux-clean-install-validation/valid.json"))
    assert result["task"] == "T207"
    assert result["result"]["status"] == "pass"

