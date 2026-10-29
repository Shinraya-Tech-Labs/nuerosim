"""Audit classic HH rates and resting gates at the fixed 6.3 C parameterization."""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

from .workbench.config import Experiment
from .workbench.engine import initial_state, rates

RATE_NAMES = ("alpha_m", "beta_m", "alpha_h", "beta_h", "alpha_n", "beta_n")
GATE_NAMES = ("m", "h", "n")


def audit_reference(temperature_c, voltage_mV, tolerance, expected_rates, expected_gates):
    if isinstance(temperature_c, bool) or not isinstance(temperature_c, (int, float)) or temperature_c != 6.3:
        raise ValueError("only the fixed 6.3 C parameterization is implemented")
    if isinstance(voltage_mV, bool) or not isinstance(voltage_mV, (int, float)) or not math.isfinite(voltage_mV) or not -80 <= voltage_mV <= -55:
        raise ValueError("voltage_mV must be finite and within -80..-55 mV")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if not isinstance(expected_rates, dict) or set(expected_rates) != set(RATE_NAMES):
        raise ValueError("expected rates must contain all six HH rates")
    if not isinstance(expected_gates, dict) or set(expected_gates) != set(GATE_NAMES):
        raise ValueError("expected gates must contain m, h, and n")

    actual = [float(value[0]) for value in rates(np.array([voltage_mV], dtype=float))]
    rate_values = dict(zip(RATE_NAMES, actual))
    if any(not math.isfinite(v) or v < 0 for v in actual):
        raise ValueError("HH rates must be finite and non-negative")
    gates = {
        name: rate_values[f"alpha_{name}"] / (rate_values[f"alpha_{name}"] + rate_values[f"beta_{name}"])
        for name in GATE_NAMES
    }
    production = initial_state(Experiment(model="hh", initial_voltage=voltage_mV, pulses=[]))
    initial_gates = dict(zip(GATE_NAMES, map(float, production[1:4, 0])))
    rate_error = max(abs(rate_values[k] - float(expected_rates[k])) for k in RATE_NAMES)
    gate_error = max(abs(gates[k] - float(expected_gates[k])) for k in GATE_NAMES)
    initialization_error = max(abs(gates[k] - initial_gates[k]) for k in GATE_NAMES)
    return {
        "passed": rate_error <= tolerance and gate_error <= tolerance and initialization_error <= tolerance,
        "units": {"temperature": "C", "voltage": "mV", "rate": "ms^-1", "gate": "1"},
        "temperature_c": float(temperature_c), "voltage_mV": float(voltage_mV),
        "rates_ms^-1": rate_values, "steady_state_gates": gates,
        "production_initial_gates": initial_gates,
        "max_rate_error_ms^-1": rate_error, "max_gate_error": gate_error,
        "max_initialization_error": initialization_error, "tolerance": float(tolerance),
    }


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")
    if fixture.get("units") != {"temperature": "C", "voltage": "mV", "rate": "ms^-1", "gate": "1"}:
        raise ValueError("units must be C, mV, ms^-1, and dimensionless gates")
    return audit_reference(fixture.get("temperature_c"), fixture.get("voltage_mV"), fixture.get("tolerance"), fixture.get("expected_rates_ms^-1"), fixture.get("expected_gates"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON HH reference fixture")
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
