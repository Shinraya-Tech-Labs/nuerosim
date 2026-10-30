from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T174_isi_coefficient_of_variation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T174-isi-coefficient-of-variation/valid.json"))
    assert result["task"] == "T174"
    assert result["result"]["status"] == "pass"

