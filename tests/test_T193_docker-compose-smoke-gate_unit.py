from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T193_docker_compose_smoke_gate_unit():
    result = run_fixture(Path("tests/fixtures/omega/T193-docker-compose-smoke-gate/valid.json"))
    assert result["task"] == "T193"
    assert result["result"]["status"] == "pass"

