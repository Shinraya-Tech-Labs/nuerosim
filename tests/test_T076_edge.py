from neurosim.morphology_tools import parse_swc
def test_T076_edge():
 try: parse_swc('bad')
 except ValueError: assert True
