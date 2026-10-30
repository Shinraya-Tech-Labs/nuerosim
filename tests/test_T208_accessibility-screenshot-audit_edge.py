import pytest
from neurosim.omega_final import run_task


def test_T208_accessibility_screenshot_audit_edge():
    with pytest.raises(ValueError):
        run_task("T208", {"input": {}})

