"""Audit absolute refractory scheduling in production LIF/AdEx simulations."""

import argparse
import json
import math
import sys
from pathlib import Path

from .workbench.config import Experiment
from .workbench.engine import simulate

UNITS = {"time": "ms", "voltage": "mV", "current_density": "uA/cm^2"}


def audit_experiment(experiment_data, tolerance_ms, expected_first=None, expected_minimum_interval=None):
    if isinstance(tolerance_ms, bool) or not isinstance(tolerance_ms, (int, float)) or not math.isfinite(tolerance_ms) or tolerance_ms <= 0:
        raise ValueError("minimum_interval_tolerance_ms must be finite and positive")
    try:
        config = Experiment.model_validate(experiment_data)
    except Exception as exc:
        raise ValueError(f"invalid experiment: {exc}") from exc
    if config.model not in ("lif", "adex"):
        raise ValueError("refractory audit requires model='lif' or model='adex'")
    if config.n != 1 or config.probability != 0:
        raise ValueError("refractory audit requires one neuron and no connectivity")
    if config.duration / config.dt > 2_000_000:
        raise ValueError("experiment exceeds two million neuron-steps")
    result = simulate(config)
    spike_times = result["spikes"][0]
    if len(spike_times) < 2:
        raise ValueError("experiment must produce at least two spikes to audit refractory scheduling")
    intervals = [b - a for a, b in zip(spike_times, spike_times[1:])]
    refractory = config.parameters.refractory
    passed = min(intervals) + tolerance_ms >= refractory
    if expected_first is not None:
        passed = passed and abs(spike_times[0] - expected_first) <= tolerance_ms
    if expected_minimum_interval is not None:
        passed = passed and abs(min(intervals) - expected_minimum_interval) <= tolerance_ms
    return {
        "passed": passed,
        "units": UNITS,
        "spike_times_ms": spike_times,
        "interspike_intervals_ms": intervals,
        "minimum_interspike_interval_ms": min(intervals),
        "configured_refractory_ms": refractory,
        "minimum_interval_satisfied": min(intervals) + tolerance_ms >= refractory,
        "refractory_steps_at_dt": math.ceil(refractory / config.dt - 1e-10),
        "minimum_interval_tolerance_ms": float(tolerance_ms),
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
    return audit_experiment(fixture.get("experiment"), fixture.get("minimum_interval_tolerance_ms"), fixture.get("expected_first_spike_ms"), fixture.get("expected_minimum_interspike_interval_ms"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON refractory scheduling fixture")
    parser.add_argument("--output", help="write the audit report to this JSON file")
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
