"""Compare a subthreshold LIF run with its piecewise constant-current solution."""

import argparse
import json
import math
import sys
from pathlib import Path

from .workbench.config import Experiment
from .workbench.engine import simulate

UNITS = {"time": "ms", "voltage": "mV", "current_density": "uA/cm^2", "capacitance_density": "uF/cm^2"}


def exact_voltage(config, time_ms):
    p = config.parameters
    boundaries = sorted({0.0, float(time_ms), *(float(v) for pulse in config.pulses for v in (pulse.start, pulse.stop) if 0 < v < time_ms)})
    voltage = config.initial_voltage
    for start, stop in zip(boundaries, boundaries[1:]):
        midpoint = (start + stop) / 2
        current = sum(pulse.amplitude for pulse in config.pulses if pulse.start <= midpoint < pulse.stop)
        equilibrium = p.rest + current * p.tau_m / p.cm
        voltage = equilibrium + (voltage - equilibrium) * math.exp(-(stop - start) / p.tau_m)
    return voltage


def compare_experiment(experiment_data, tolerance_mV):
    if isinstance(tolerance_mV, bool) or not isinstance(tolerance_mV, (int, float)) or not math.isfinite(tolerance_mV) or tolerance_mV <= 0:
        raise ValueError("tolerance_mV must be finite and positive")
    try:
        config = Experiment.model_validate(experiment_data)
    except Exception as exc:
        raise ValueError(f"invalid experiment: {exc}") from exc
    if config.model != "lif":
        raise ValueError("exact reference requires model='lif'")
    if config.n != 1 or config.probability != 0:
        raise ValueError("exact reference requires one neuron and no connectivity")
    if any(pulse.target != 0 for pulse in config.pulses):
        raise ValueError("pulse target must be neuron 0")

    result = simulate(config)
    times = result["t"]
    reference = [exact_voltage(config, time_ms) for time_ms in times]
    # LIF resets are discontinuities; only subthreshold trajectories are in scope.
    boundaries = set(times)
    boundaries.update(v for pulse in config.pulses for v in (pulse.start, pulse.stop))
    if any(exact_voltage(config, t) >= config.parameters.threshold for t in boundaries):
        raise ValueError("exact reference is limited to trajectories without threshold crossing")
    actual = result["voltage"][0]
    errors = [abs(a - b) for a, b in zip(actual, reference)]
    maximum_error = max(errors, default=0.0)
    return {
        "passed": maximum_error <= tolerance_mV,
        "units": UNITS,
        "times_ms": times,
        "exact_voltage_mV": reference,
        "production_voltage_mV": actual,
        "max_abs_error_mV": maximum_error,
        "tolerance_mV": float(tolerance_mV),
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
        raise ValueError("units must be ms, mV, uA/cm^2, and uF/cm^2")
    report = compare_experiment(fixture.get("experiment"), fixture.get("tolerance_mV"))
    expected = fixture.get("expected_exact_voltage_mV")
    if not isinstance(expected, dict):
        raise ValueError("expected_exact_voltage_mV must be an object")
    expected_errors = {}
    for time_text, value in expected.items():
        try:
            index = report["times_ms"].index(float(time_text))
        except (ValueError, TypeError):
            raise ValueError(f"expected time {time_text} is not a recorded sample") from None
        expected_errors[time_text] = abs(report["exact_voltage_mV"][index] - float(value))
    report["fixture_reference_errors_mV"] = expected_errors
    report["passed"] = report["passed"] and max(expected_errors.values(), default=0) <= fixture["tolerance_mV"]
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON LIF exact-reference fixture")
    parser.add_argument("--output", help="write the full report to this JSON file")
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
