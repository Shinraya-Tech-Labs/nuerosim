import pytest
from neurosim.omega_final import run_task


def test_T156_render_fps_telemetry_reproducibility_edge():
    with pytest.raises(ValueError):
        run_task("T156", {"input": {}})

