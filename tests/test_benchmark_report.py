import copy
import json
from pathlib import Path

import pytest

from scripts.verify_release_benchmark_report import validate_report


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmarks/results/v020-run-001.json"
CONFIG = ROOT / "benchmarks/v020-workloads.json"
RUNNER = ROOT / "scripts/run_release_benchmarks.py"


def test_captured_release_benchmark_report_matches_raw_samples():
    assert validate_report(REPORT, CONFIG, RUNNER) == (11, 5)


def test_report_validator_rejects_changed_repeat_hash(tmp_path):
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report = copy.deepcopy(report)
    report["benchmarks"][0]["sample_records"][0]["output_sha256"] = "changed"
    changed_report = tmp_path / "changed-report.json"
    changed_report.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(ValueError, match="output hashes are not deterministic"):
        validate_report(changed_report, CONFIG, RUNNER)
