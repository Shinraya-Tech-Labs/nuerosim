import copy
import json
from pathlib import Path

import pytest

from scripts.run_release_benchmarks import run_benchmarks
from scripts.verify_release_benchmark_report import validate_report


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_release_benchmarks.py"
CAPTURED_REPORT = ROOT / "benchmarks/results/v020-run-004.json"
CAPTURED_CONFIG = ROOT / "benchmarks/v020-workloads.json"


def test_captured_release_benchmark_report_matches_raw_samples():
    assert validate_report(CAPTURED_REPORT, CAPTURED_CONFIG, RUNNER) == (11, 5)


def _create_report(tmp_path):
    config = {
        "schema_version": 1,
        "suite": "benchmark-report-test",
        "warmup_repeats": 0,
        "repetitions": 3,
        "workloads": [
            {
                "id": "lif-report-smoke",
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
    config_path = tmp_path / "workloads.json"
    config_path.write_text(json.dumps(config) + "\n", encoding="utf-8")
    report_path = tmp_path / "report.json"
    report = run_benchmarks(config_path, report_path)
    return config_path, report_path, report


def test_report_validation_accepts_platform_line_endings(tmp_path):
    config_path, report_path, _ = _create_report(tmp_path)
    config_crlf = tmp_path / "workloads-crlf.json"
    config_bytes = config_path.read_bytes().replace(b"\r\n", b"\n")
    config_crlf.write_bytes(config_bytes.replace(b"\n", b"\r\n"))
    runner_crlf = tmp_path / "runner-crlf.py"
    runner_bytes = RUNNER.read_bytes().replace(b"\r\n", b"\n")
    runner_crlf.write_bytes(runner_bytes.replace(b"\n", b"\r\n"))

    assert validate_report(report_path, config_crlf, runner_crlf) == (1, 3)


def test_report_validator_rejects_changed_repeat_hash(tmp_path):
    config_path, report_path, report = _create_report(tmp_path)
    report["benchmarks"][0]["sample_records"][0]["output_sha256"] = "changed"
    changed_report = tmp_path / "changed-report.json"
    changed_report.write_text(json.dumps(copy.deepcopy(report)), encoding="utf-8")

    with pytest.raises(ValueError, match="output hashes are not deterministic"):
        validate_report(changed_report, config_path, RUNNER)
