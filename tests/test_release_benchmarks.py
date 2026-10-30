import json

import pytest

from scripts.run_release_benchmarks import run_benchmarks


def _config(tmp_path, repetitions=3):
    config = {
        "schema_version": 1,
        "suite": "benchmark-runner-test",
        "warmup_repeats": 0,
        "repetitions": repetitions,
        "workloads": [
            {
                "id": "lif-fast-smoke",
                "category": "test",
                "config": {
                    "model": "lif",
                    "n": 1,
                    "duration": 1,
                    "dt": 0.025,
                    "record_every": 1,
                    "seed": 7,
                    "probability": 0,
                    "pulses": [],
                },
            }
        ],
    }
    path = tmp_path / "benchmark.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def test_release_benchmark_measures_isolated_run_phases_and_peak_rss(tmp_path):
    output = tmp_path / "report.json"
    report = run_benchmarks(_config(tmp_path), output)

    assert report["protocol"]["measured_repetitions"] == 3
    workload = report["benchmarks"][0]
    assert workload["repeats_identical"] is True
    assert workload["derived"]["time_steps"] == 40
    assert len(workload["sample_records"]) == 3
    assert workload["phase_summary_seconds"]["simulation"]["count"] == 3
    assert workload["phase_summary_seconds"]["simulation"]["p95"] >= 0
    assert workload["memory_summary_bytes"]["process_peak_rss_bytes"]["median"] > 0
    assert all(
        sample["process_peak_rss_bytes"] >= sample["process_baseline_rss_bytes"]
        for sample in workload["sample_records"]
    )
    assert json.loads(output.read_text(encoding="utf-8")) == report


def test_release_benchmark_refuses_to_overwrite_existing_report(tmp_path):
    output = tmp_path / "existing.json"
    output.write_text("preserve", encoding="utf-8")

    with pytest.raises(FileExistsError):
        run_benchmarks(_config(tmp_path), output)

    assert output.read_text(encoding="utf-8") == "preserve"


def test_release_benchmark_rejects_too_few_repetitions(tmp_path):
    with pytest.raises(ValueError, match="repetitions must be"):
        run_benchmarks(_config(tmp_path, repetitions=2), tmp_path / "report.json")
