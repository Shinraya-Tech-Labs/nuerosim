from neurosim.ui_contracts import channel_chart

def test_channel_chart_projects_multiple_channels():
    assert channel_chart([0], {"m": [0.5], "h": [0.2]})[0]["h"] == 0.2

