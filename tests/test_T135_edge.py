from neurosim.ui_contracts import status_label

def test_status_label_unknown_is_humanized():
    assert status_label("paused") == "Paused"

