from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T184_read_only_demo_mode_unit():
    result = run_fixture(Path("tests/fixtures/omega/T184-read-only-demo-mode/valid.json"))
    assert result["task"] == "T184"
    assert result["result"]["status"] == "pass"

