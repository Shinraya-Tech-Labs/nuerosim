from neurosim.ui_contracts import raster_limit

def test_raster_limit_zero_is_empty():
    assert raster_limit([1, 2], 0) == []

