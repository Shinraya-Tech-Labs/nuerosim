from neurosim.interop_tools import example

def test_example_preserves_config():
    config = {"dt_ms": 0.1}
    assert example("lif", config)["config"] == config

