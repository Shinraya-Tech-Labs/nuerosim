from neurosim.ui_contracts import keyboard_order

def test_keyboard_order_is_deterministic():
    labels = ("Run", "Stop")
    assert keyboard_order(labels) == ["Run", "Stop"]

