from neurosim.ui_contracts import reduced_motion

def test_reduced_motion_false_is_disabled():
    assert reduced_motion(False) is False

