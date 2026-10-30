from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T187_sbom_generation_unit():
    result = run_fixture(Path("tests/fixtures/omega/T187-sbom-generation/valid.json"))
    assert result["task"] == "T187"
    assert result["result"]["status"] == "pass"

