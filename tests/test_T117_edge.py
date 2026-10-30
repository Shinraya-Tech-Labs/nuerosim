from neurosim.interop_tools import rms_error

def test_rms_error_empty_trace_is_zero():
    assert rms_error([], []) == 0

