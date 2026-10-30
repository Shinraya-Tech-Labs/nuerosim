from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T198_scientific_model_catalogue_final_unit():
    result = run_fixture(Path("tests/fixtures/omega/T198-scientific-model-catalogue-final/valid.json"))
    assert result["task"] == "T198"
    assert result["result"]["status"] == "pass"

