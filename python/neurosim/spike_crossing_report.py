"""Report HH spike-time endpoint quantization using sampled upward crossings."""

import argparse
import json
import math
import sys
from pathlib import Path

from .workbench.config import Experiment
from .workbench.engine import simulate

UNITS = {"time": "ms", "voltage": "mV", "current_density": "uA/cm^2"}


def crossing_report(experiment_data, expected_spike_times_ms, expected_crossings_ms, maximum_crossing_offset_ms):
    if isinstance(maximum_crossing_offset_ms, bool) or not isinstance(maximum_crossing_offset_ms, (int, float)) or not math.isfinite(maximum_crossing_offset_ms) or maximum_crossing_offset_ms <= 0:
        raise ValueError("maximum_crossing_offset_ms must be finite and positive")
    try:
        config = Experiment.model_validate(experiment_data)
    except Exception as exc:
        raise ValueError(f"invalid experiment: {exc}") from exc
    if config.model != "hh":
        raise ValueError("crossing report requires model='hh'")
    if config.n != 1 or config.probability != 0:
        raise ValueError("crossing report requires one neuron and no connectivity")
    if config.record_every != 1:
        raise ValueError("crossing report requires record_every=1")
    result = simulate(config)
    times = result["t"]
    voltage = result["voltage"][0]
    rows = []
    for spike_time in result["spikes"][0]:
        indices = [i for i, t in enumerate(times) if abs(t - spike_time) <= 1e-12]
        if not indices or indices[0] == 0:
            raise ValueError("spike time is missing its previous voltage sample")
        index = indices[0]
        t0, t1 = times[index - 1], times[index]
        v0, v1 = voltage[index - 1], voltage[index]
        if not (v0 < 0 <= v1):
            raise ValueError("trace does not bracket an upward 0 mV crossing")
        crossing = t0 + (0 - v0) * (t1 - t0) / (v1 - v0)
        offset = spike_time - crossing
        rows.append({"spike_time_ms": spike_time, "interpolated_crossing_ms": crossing, "endpoint_offset_ms": offset})
    expected = expected_spike_times_ms
    if not isinstance(expected, list) or any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in expected):
        raise ValueError("expected_spike_times_ms must be a list of finite numbers")
    match = len(expected) == len(rows) and all(abs(row["spike_time_ms"] - value) <= 1e-12 for row, value in zip(rows, expected))
    if not isinstance(expected_crossings_ms, list) or len(expected_crossings_ms) != len(rows) or any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in expected_crossings_ms):
        raise ValueError("expected_interpolated_crossings_ms must match the spike count")
    crossing_errors = [abs(row["interpolated_crossing_ms"] - value) for row, value in zip(rows, expected_crossings_ms)]
    match = match and max(crossing_errors, default=0.0) <= 1e-12
    bound_ok = all(-1e-12 <= row["endpoint_offset_ms"] <= min(config.dt, maximum_crossing_offset_ms) + 1e-12 for row in rows)
    return {
        "passed": match and bound_ok,
        "units": UNITS,
        "dt_ms": config.dt,
        "maximum_crossing_offset_ms": min(config.dt, float(maximum_crossing_offset_ms)),
        "crossings": rows,
        "interpolated_crossing_errors_ms": crossing_errors,
        "manifest": result["manifest"],
    }


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")
    if fixture.get("units") != UNITS:
        raise ValueError("units must be ms, mV, and uA/cm^2")
    return crossing_report(fixture.get("experiment"), fixture.get("expected_spike_times_ms"), fixture.get("expected_interpolated_crossings_ms"), fixture.get("maximum_crossing_offset_ms"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON HH spike-crossing fixture")
    parser.add_argument("--output", help="write the report to this JSON file")
    args = parser.parse_args(argv)
    try:
        report = audit_fixture(args.fixture)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    output = json.dumps(report, sort_keys=True, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
