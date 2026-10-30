from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T178_model_regime_classification_unit():
    result = run_fixture(Path("tests/fixtures/omega/T178-model-regime-classification/valid.json"))
    assert result["task"] == "T178"
    assert result["result"]["status"] == "pass"

