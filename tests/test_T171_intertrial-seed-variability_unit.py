from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T171_intertrial_seed_variability_unit():
    result = run_fixture(Path("tests/fixtures/omega/T171-intertrial-seed-variability/valid.json"))
    assert result["task"] == "T171"
    assert result["result"]["status"] == "pass"

