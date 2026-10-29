import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from neurosim.performance_benchmark import median_seconds, profile_config, run_benchmarks


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/omega/T012-performance-benchmark-harness/valid.json"
INVALID = ROOT / "tests/fixtures/omega/T012-performance-benchmark-harness/invalid.json"


def test_fixture_median_and_profile_configuration():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert median_seconds(fixture["sample_wall_seconds"]) == fixture["expected_median_seconds"]
    config = profile_config(fixture["profile"])
    assert (config.model, config.n, config.duration, config.dt) == (
        "hh",
        1,
        50,
        0.025,
    )


def test_invalid_fixture_rejects_repeat_bound():
    from neurosim.performance_benchmark import run_profile

    fixture = json.loads(INVALID.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match=fixture["expected_error"]):
        run_profile("hh", fixture["repeats"])


@pytest.mark.parametrize("samples", [[], [-1], [float("nan")], [float("inf")]])
def test_invalid_timing_samples_are_rejected(samples):
    with pytest.raises(ValueError, match="finite non-negative seconds"):
        median_seconds(samples)


def test_unknown_profile_is_rejected():
    with pytest.raises(ValueError, match="unknown benchmark profile"):
        profile_config("not-a-profile")


def test_duplicate_profiles_and_repeat_limit_are_rejected():
    from neurosim.performance_benchmark import run_profile

    with pytest.raises(ValueError, match="profiles must not repeat"):
        run_benchmarks(["hh", "hh"])
    with pytest.raises(ValueError, match="repeats must be between 1 and 20"):
        run_profile("hh", 21)


def test_cli_runs_real_seeded_hh_simulation():
    result = subprocess.run(
        [sys.executable, "-m", "neurosim.performance_benchmark", "--profile", "hh", "--repeats", "1"],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": "python"},
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    run = report["benchmarks"][0]
    assert run["profile"] == "hh"
    assert run["config"]["model"] == run["manifest"]["config"]["model"] == "hh"
    assert len(run["wall_seconds"]) == 1
    assert run["wall_seconds"][0] >= 0
