from pathlib import Path
from neurosim.omega_final import run_fixture


def test_T156_render_fps_telemetry_reproducibility_unit():
    result = run_fixture(Path("tests/fixtures/omega/T156-render-fps-telemetry-reproducibility/valid.json"))
    assert result["task"] == "T156"
    assert result["result"]["status"] == "pass"

