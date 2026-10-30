from neurosim.ui_contracts import model_explainer

def test_model_explainer_keeps_model_id():
    assert model_explainer("lif_model")["model"] == "lif_model"

