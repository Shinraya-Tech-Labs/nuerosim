"""Run a machine-readable set of bounded workbench scientific experiments."""

import argparse
import hashlib
import json
import platform
import re
import sys
from pathlib import Path

import numpy as np

from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import simulate
from neurosim.workbench import __version__


TRACE_FIELDS = (
    "t",
    "voltage",
    "spikes",
    "edges",
    "rate_time",
    "rate_hz",
    "mean_rate_hz",
    "final_state",
    "effective_delay_ms",
    "activity_events",
)


def _json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def run_suite(config_path, output_dir):
    suite_bytes = Path(config_path).read_bytes()
    document = json.loads(suite_bytes)
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("suite must be an object with schema_version=1")
    suite = document.get("suite")
    experiments = document.get("experiments")
    if not isinstance(suite, str) or not isinstance(experiments, list) or not experiments:
        raise ValueError("suite name and non-empty experiments list are required")
    ids = [item.get("id") for item in experiments if isinstance(item, dict)]
    if len(ids) != len(experiments) or any(not isinstance(item_id, str) or not item_id for item_id in ids):
        raise ValueError("each experiment must have a string id")
    if any(re.fullmatch(r"[a-z0-9][a-z0-9_-]*", item_id) is None for item_id in ids):
        raise ValueError("experiment ids must be lowercase filename-safe slugs")
    if len(set(ids)) != len(ids):
        raise ValueError("experiment ids must be unique")
    output_dir = Path(output_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for case in experiments:
        if not isinstance(case.get("config"), dict):
            raise ValueError(f"{case['id']}: config must be an object")
        if not isinstance(case.get("validation_refs", []), list):
            raise ValueError(f"{case['id']}: validation_refs must be a list")
        config = Experiment.model_validate(case["config"])
        result = simulate(config)
        traces = {field: result[field] for field in TRACE_FIELDS}
        trace_digest = hashlib.sha256(_json_bytes(traces)).hexdigest()
        artifact = {
            "experiment_id": case["id"],
            "purpose": case.get("purpose", ""),
            "validation_refs": case.get("validation_refs", []),
            "manifest": result["manifest"],
            "scientific_outputs": traces,
            "scientific_outputs_sha256": trace_digest,
            "measured_wall_time_s": result["wall_time_s"],
        }
        filename = f"{case['id']}.json"
        (output_dir / filename).write_text(
            json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        records.append(
            {
                "experiment_id": case["id"],
                "file": filename,
                "config_sha256": result["manifest"]["config_sha256"],
                "scientific_outputs_sha256": trace_digest,
                "wall_time_s": result["wall_time_s"],
            }
        )

    summary = {
        "schema_version": 1,
        "suite": suite,
        "suite_sha256": hashlib.sha256(suite_bytes).hexdigest(),
        "software_version": __version__,
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "units": document.get("units", {}),
        "experiments": records,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", default="scientific/experiments/v020-core.json", type=Path
    )
    parser.add_argument(
        "--output-dir", default="scientific/results/v020-core-reproduction-003", type=Path
    )
    args = parser.parse_args(argv)
    try:
        summary = run_suite(args.config, args.output_dir)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
