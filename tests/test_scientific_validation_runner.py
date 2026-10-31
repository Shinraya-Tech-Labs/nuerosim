import json
from pathlib import Path

import pytest

from scripts.run_scientific_validation import run_suite


SUITE = Path("scientific/experiments/v020-core.json")


def test_core_science_suite_is_reproducible_and_preserves_raw_traces(tmp_path):
    first = run_suite(SUITE, tmp_path / "first")
    second = run_suite(SUITE, tmp_path / "second")
    assert [item["experiment_id"] for item in first["experiments"]] == [
        item["experiment_id"] for item in second["experiments"]
    ]
    assert [item["scientific_outputs_sha256"] for item in first["experiments"]] == [
        item["scientific_outputs_sha256"] for item in second["experiments"]
    ]
    record = json.loads((tmp_path / "first" / "network_seeded.json").read_text())
    assert record["manifest"]["config"]["seed"] == 42
    assert record["scientific_outputs"]["edges"]
    assert len(record["scientific_outputs"]["voltage"]) == 8
    assert record["scientific_outputs_sha256"]


def test_runner_refuses_to_overwrite_existing_evidence(tmp_path):
    output = tmp_path / "existing"
    output.mkdir()
    (output / "keep.txt").write_text("prior evidence")
    with pytest.raises(FileExistsError):
        run_suite(SUITE, output)
    assert (output / "keep.txt").read_text() == "prior evidence"


def test_runner_rejects_ids_that_escape_the_output_directory(tmp_path):
    suite = json.loads(SUITE.read_text())
    suite["experiments"][0]["id"] = "../outside"
    config = tmp_path / "unsafe.json"
    config.write_text(json.dumps(suite))
    output = tmp_path / "results"

    with pytest.raises(ValueError, match="filename-safe"):
        run_suite(config, output)

    assert not output.exists()
