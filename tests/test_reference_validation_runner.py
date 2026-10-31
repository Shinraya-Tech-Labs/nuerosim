import json

import pytest

from scripts.run_reference_validation import run_validation


def test_reference_comparison_suite_passes_and_persists_metrics(tmp_path):
    output = tmp_path / "reference-report.json"
    report = run_validation(output)

    assert report["passed"] is True
    assert len(report["comparisons"]) == 7
    by_name = {item["reference"]: item for item in report["comparisons"]}
    assert by_name["Leaky integrate-and-fire analytic trajectory"]["metrics"][
        "max_abs_error_mV"
    ] <= by_name["Leaky integrate-and-fire analytic trajectory"]["metrics"][
        "tolerance_mV"
    ]
    cable = by_name["independently integrated sealed-chain cable ODE with SciPy DOP853"]
    assert cable["metrics"]["max_abs_voltage_error_mV"] < 1e-7
    adex = by_name["independently coded AdEx ODE with SciPy DOP853"]
    assert adex["metrics"]["max_abs_voltage_error_mV"] <= adex["metrics"][
        "voltage_tolerance_mV"
    ]
    assert adex["metrics"]["max_abs_adaptation_error_uA_cm2"] <= adex["metrics"][
        "adaptation_tolerance_uA_cm2"
    ]
    assert all(item["fixture_sha256"] for item in report["comparisons"] if "fixture_sha256" in item)
    assert json.loads(output.read_text(encoding="utf-8")) == report


def test_reference_runner_does_not_overwrite_evidence(tmp_path):
    output = tmp_path / "existing.json"
    output.write_text("keep", encoding="utf-8")

    with pytest.raises(FileExistsError):
        run_validation(output)

    assert output.read_text(encoding="utf-8") == "keep"
