from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T157_vectorized_lif_path_prototype_unit():
    result = run_fixture(Path("tests/fixtures/omega/T157-vectorized-lif-path-prototype/valid.json"))
    assert result["task"] == "T157"
    assert result["result"]["status"] == "pass"

