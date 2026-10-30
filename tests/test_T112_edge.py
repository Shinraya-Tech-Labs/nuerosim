import pytest
from neurosim.interop_tools import discrepancy

def test_hh_comparison_can_report_negative_delta():
    assert discrepancy("hh", 1.1, 1.0)["delta"] == pytest.approx(-0.1)

