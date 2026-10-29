"""Audit a saved Hodgkin–Huxley reference trace fixture."""

import argparse
import json
import math
import sys
from pathlib import Path

from .workbench.config import Experiment
from .workbench.engine import simulate


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be a JSON object")
    if fixture.get("units") != {"time": "ms", "voltage": "mV"}:
        raise ValueError("fixture units must be ms and mV")
    try:
        config = Experiment(**fixture["config"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid experiment config: {exc}") from exc
    if config.model != "hh" or config.n != 1:
        raise ValueError("golden trace requires a single-neuron HH config")
    times = fixture.get("sample_times_ms")
    expected = fixture.get("reference_voltage_mV")
    tolerance = fixture.get("tolerance_mV")
    if not isinstance(times, list) or len(times) < 1 or not isinstance(expected, list):
        raise ValueError("sample time and reference voltage arrays are required")
    if len(times) != len(expected):
        raise ValueError("sample time and reference voltage arrays must have equal length")
    if any(not isinstance(value, (int, float)) or not math.isfinite(value) for value in [*times, *expected]):
        raise ValueError("sample times and reference voltages must be finite numbers")
    if any(right <= left for left, right in zip(times, times[1:])):
        raise ValueError("sample times must be strictly increasing")
    if not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance_mV must be a finite positive number")

    result = simulate(config)
    actual = []
    for requested in times:
        index = min(range(len(result["t"])), key=lambda i: abs(result["t"][i] - requested))
        if abs(result["t"][index] - requested) > 1e-9:
            raise ValueError(f"sample time {requested} ms is absent from the saved trace grid")
        actual.append(result["voltage"][0][index])
    errors = [abs(found - reference) for found, reference in zip(actual, expected)]
    max_error = max(errors)
    return {
        "passed": max_error <= tolerance,
        "reference": fixture.get("reference", "unspecified"),
        "sample_count": len(times),
        "max_abs_error_mV": max_error,
        "tolerance_mV": tolerance,
        "errors_mV": errors,
        "spike_count": len(result["spikes"][0]),
        "manifest": result["manifest"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON golden HH trace fixture")
    args = parser.parse_args(argv)
    try:
        report = audit_fixture(args.fixture)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
