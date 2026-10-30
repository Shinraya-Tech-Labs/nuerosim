from neurosim.interop_tools import loss_report

def test_loss_report_defaults_to_empty_losses():
    assert loss_report("a", "b")["losses"] == []

