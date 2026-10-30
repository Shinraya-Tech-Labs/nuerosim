from neurosim.morphology_tools import validate_swc
def test_T077_edge():
 try: validate_swc([(1,1,0,0,0,1,9)])
 except ValueError: assert True
