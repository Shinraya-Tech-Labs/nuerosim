"""Audit AdEx numerical cutoff and spike timing with the production solver."""

import argparse
import json
import math
import sys
from pathlib import Path

from .workbench.config import Experiment
from .workbench.engine import simulate

UNITS = {"time": "ms", "voltage": "mV", "current_density": "uA/cm^2"}


def audit_experiment(experiment_data, expected_spike_times_ms, tolerance_ms):
    if isinstance(tolerance_ms, bool) or not isinstance(tolerance_ms, (int, float)) or not math.isfinite(tolerance_ms) or tolerance_ms <= 0:
        raise ValueError("spike_time_tolerance_ms must be finite and positive")
    if not isinstance(expected_spike_times_ms, list) or any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in expected_spike_times_ms):
        raise ValueError("expected_spike_times_ms must be a list of finite numbers")
    try:
        config = Experiment.model_validate(experiment_data)
    except Exception as exc:
        raise ValueError(f"invalid experiment: {exc}") from exc
    if config.model != "adex":
        raise ValueError("threshold audit requires model='adex'")
    if config.n != 1 or config.probability != 0:
        raise ValueError("threshold audit requires one neuron and no connectivity")
    if config.duration * config.n / config.dt > 2_000_000:
        raise ValueError("experiment exceeds two million neuron-steps")
    result = simulate(config)
    spike_times = result["spikes"][0]
    if len(spike_times) != len(expected_spike_times_ms):
        passed = False
        errors = None
    else:
        errors = [abs(actual - expected) for actual, expected in zip(spike_times, expected_spike_times_ms)]
        passed = max(errors, default=0.0) <= tolerance_ms
    p = config.parameters
    return {
        "passed": passed,
        "units": UNITS,
        "numerical_cutoff_voltage_mV": p.threshold + 5 * p.delta_t,
        "spike_times_ms": spike_times,
        "spike_count": len(spike_times),
        "spike_intervals_ms": [b - a for a, b in zip(spike_times, spike_times[1:])],
        "expected_spike_times_ms": expected_spike_times_ms,
        "spike_time_errors_ms": errors,
        "spike_time_tolerance_ms": float(tolerance_ms),
        "final_voltage_mV": result["final_state"][0][0],
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
    return audit_experiment(fixture.get("experiment"), fixture.get("expected_spike_times_ms"), fixture.get("spike_time_tolerance_ms"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON AdEx threshold fixture")
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
