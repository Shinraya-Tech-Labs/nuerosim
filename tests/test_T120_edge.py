from neurosim.interop_tools import benchmark_report

def test_benchmark_report_empty_results():
    assert benchmark_report("empty", {})["count"] == 0

