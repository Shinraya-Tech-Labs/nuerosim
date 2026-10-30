from neurosim.ui_contracts import picker_options

def test_picker_options_humanizes_underscores():
    assert picker_options(["two_run"])[0] == {"value": "two_run", "label": "Two Run"}

