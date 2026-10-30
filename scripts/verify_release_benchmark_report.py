"""Verify captured benchmark evidence against its inputs and raw samples."""

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path


PHASES = ("setup", "simulation", "serialization", "retrieval")
MEMORY_METRICS = (
    "process_baseline_rss_bytes",
    "process_peak_rss_bytes",
    "incremental_peak_rss_bytes",
)


def _reject_constant(value):
    raise ValueError(f"non-finite JSON number: {value}")


def _percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    return float(
        ordered[lower]
        + (ordered[upper] - ordered[lower]) * (position - lower)
    )


def _summary(values):
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "sample_stddev": statistics.stdev(values),
        "p95": _percentile(values, 0.95),
        "min": min(values),
        "max": max(values),
    }


def _assert_summary(actual, values, label):
    expected = _summary(values)
    for key, value in expected.items():
        observed = actual.get(key)
        if key == "count":
            matches = observed == value
        else:
            matches = isinstance(observed, (int, float)) and math.isclose(
                observed, value, rel_tol=1e-12, abs_tol=1e-15
            )
        if not matches:
            raise ValueError(f"{label}.{key} does not match its raw samples")


def validate_report(report_path, config_path, runner_path):
    report_path = Path(report_path)
    config_path = Path(config_path)
    runner_path = Path(runner_path)
    report = json.loads(
        report_path.read_text(encoding="utf-8"), parse_constant=_reject_constant
    )
    config = json.loads(
        config_path.read_text(encoding="utf-8"), parse_constant=_reject_constant
    )
    canonical_config = json.dumps(
        config, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    canonical_runner = runner_path.read_bytes().replace(b"\r\n", b"\n")
    runner_hash = hashlib.sha256(canonical_runner).hexdigest()

    if report.get("schema_version") != 1:
        raise ValueError("unsupported benchmark report schema")
    if report.get("suite") != config.get("suite"):
        raise ValueError("report suite does not match workload config")
    if report.get("config_sha256") != hashlib.sha256(canonical_config).hexdigest():
        raise ValueError("report workload config hash does not match")
    if report.get("runner_sha256") != runner_hash:
        raise ValueError("report runner hash does not match")

    expected_workloads = config.get("workloads", [])
    actual_workloads = report.get("benchmarks", [])
    if len(expected_workloads) != len(actual_workloads):
        raise ValueError("report workload count does not match config")
    repetitions = config.get("repetitions")
    warmups = config.get("warmup_repeats")

    for expected, actual in zip(expected_workloads, actual_workloads):
        workload_id = expected.get("id")
        label = f"workload {workload_id}"
        if actual.get("id") != workload_id or actual.get("config") != expected.get(
            "config"
        ):
            raise ValueError(f"{label} does not match workload config")
        if (
            actual.get("repetitions") != repetitions
            or actual.get("warmup_repeats_discarded") != warmups
        ):
            raise ValueError(f"{label} repetition policy does not match config")

        samples = actual.get("sample_records", [])
        if len(samples) != repetitions or not samples:
            raise ValueError(f"{label} has an unexpected sample count")
        output_hashes = {sample.get("output_sha256") for sample in samples}
        if (
            len(output_hashes) != 1
            or actual.get("repeats_identical") is not True
            or actual.get("identical_output_sha256") not in output_hashes
        ):
            raise ValueError(f"{label} output hashes are not deterministic")

        for phase in PHASES:
            _assert_summary(
                actual.get("phase_summary_seconds", {}).get(phase, {}),
                [sample[f"{phase}_s"] for sample in samples],
                f"{label}.{phase}",
            )
        _assert_summary(
            actual.get("phase_summary_seconds", {}).get("measured_total", {}),
            [sum(sample[f"{phase}_s"] for phase in PHASES) for sample in samples],
            f"{label}.measured_total",
        )
        for metric in MEMORY_METRICS:
            _assert_summary(
                actual.get("memory_summary_bytes", {}).get(metric, {}),
                [float(sample[metric]) for sample in samples],
                f"{label}.{metric}",
            )

        first = samples[0]
        derived = actual.get("derived", {})
        for key in (
            "neuron_count",
            "time_steps",
            "realized_edge_count",
            "spike_count",
            "serialized_result_bytes",
        ):
            sample_key = {
                "realized_edge_count": "realized_edge_count",
                "serialized_result_bytes": "serialized_result_bytes",
            }.get(key, key)
            if derived.get(key) != first.get(sample_key):
                raise ValueError(f"{label}.derived.{key} does not match samples")
        if derived.get("neuron_steps") != first["neuron_count"] * first[
            "time_steps"
        ]:
            raise ValueError(f"{label}.derived.neuron_steps does not match samples")

    return len(actual_workloads), repetitions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report", type=Path, required=True
    )
    parser.add_argument(
        "--config", type=Path, default=Path("benchmarks/v020-workloads.json")
    )
    parser.add_argument(
        "--runner", type=Path, default=Path("scripts/run_release_benchmarks.py")
    )
    args = parser.parse_args(argv)
    workload_count, repetitions = validate_report(
        args.report, args.config, args.runner
    )
    print(
        f"PASS: verified {workload_count} workloads, {repetitions} raw samples each, "
        "summary statistics, deterministic hashes, and input hashes."
    )


if __name__ == "__main__":
    main()
