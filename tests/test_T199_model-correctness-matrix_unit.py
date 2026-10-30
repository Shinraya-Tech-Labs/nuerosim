from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T199_model_correctness_matrix_unit():
    result = run_fixture(Path("tests/fixtures/omega/T199-model-correctness-matrix/valid.json"))
    assert result["task"] == "T199"
    assert result["result"]["status"] == "pass"

