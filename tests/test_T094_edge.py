from neurosim.schema_tools import migrate
def test_T094_edge(): assert migrate({},1,2)['schema_version']==2
