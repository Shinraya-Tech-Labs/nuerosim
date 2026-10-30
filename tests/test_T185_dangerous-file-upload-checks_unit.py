from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T185_dangerous_file_upload_checks_unit():
    result = run_fixture(Path("tests/fixtures/omega/T185-dangerous-file-upload-checks/valid.json"))
    assert result["task"] == "T185"
    assert result["result"]["status"] == "pass"

