from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T177_repeated_network_reproducibility_unit():
    result = run_fixture(Path("tests/fixtures/omega/T177-repeated-network-reproducibility/valid.json"))
    assert result["task"] == "T177"
    assert result["result"]["status"] == "pass"

