from neurosim.execution_tools import profile_sections

def test_profile_sections_sums_each_subsystem():
    assert profile_sections({"engine": [0.1, 0.2], "io": [1]})["engine"] == 0.30000000000000004

