"""Audit classic HH gating rates at removable singularities and nearby voltages."""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

from .workbench.engine import rates


RATE_NAMES = ("alpha_m", "beta_m", "alpha_h", "beta_h", "alpha_n", "beta_n")


def audit_rates(voltages_mV, continuity_tolerance=1e-7):
    if not isinstance(voltages_mV, list) or not voltages_mV:
        raise ValueError("voltages_mV must be a non-empty list")
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in voltages_mV
    ):
        raise ValueError("voltages_mV values must be finite numbers")
    if not isinstance(continuity_tolerance, (int, float)) or not math.isfinite(continuity_tolerance) or continuity_tolerance <= 0:
        raise ValueError("continuity tolerance must be finite and positive")
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        values = rates(np.asarray(voltages_mV, dtype=float))
    if any(not np.isfinite(array).all() or (array < 0).any() for array in values):
        raise ValueError("HH gating rates must be finite and non-negative")
    rows = [
        {"voltage_mV": float(voltage), **{name: float(array[index]) for name, array in zip(RATE_NAMES, values)}}
        for index, voltage in enumerate(voltages_mV)
    ]
    exact = {"alpha_m_at_minus40": None, "alpha_n_at_minus55": None}
    near = {"alpha_m": [], "alpha_n": []}
    for row in rows:
        if row["voltage_mV"] == -40:
            exact["alpha_m_at_minus40"] = row["alpha_m"]
        if row["voltage_mV"] == -55:
            exact["alpha_n_at_minus55"] = row["alpha_n"]
        if 0 < abs(row["voltage_mV"] + 40) <= 2e-6:
            near["alpha_m"].append(abs(row["alpha_m"] - 1))
        if 0 < abs(row["voltage_mV"] + 55) <= 2e-6:
            near["alpha_n"].append(abs(row["alpha_n"] - 0.1))
    checks = {
        "alpha_m_at_minus40": exact["alpha_m_at_minus40"] == 1.0,
        "alpha_n_at_minus55": exact["alpha_n_at_minus55"] == 0.1,
        "near_minus40_continuous": bool(near["alpha_m"]) and max(near["alpha_m"]) <= continuity_tolerance,
        "near_minus55_continuous": bool(near["alpha_n"]) and max(near["alpha_n"]) <= continuity_tolerance,
    }
    return {
        "passed": all(checks.values()),
        "units": {"voltage": "mV", "rate": "ms^-1"},
        "rates": rows,
        "singularity_checks": checks,
        "near_limit_deviation_ms^-1": {
            name: max(deviations) if deviations else None for name, deviations in near.items()
        },
        "continuity_tolerance_ms^-1": continuity_tolerance,
    }


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")
    if fixture.get("units") != {"voltage": "mV", "rate": "ms^-1"}:
        raise ValueError("units must be mV and ms^-1")
    return audit_rates(
        fixture.get("voltages_mV"), fixture.get("continuity_tolerance_ms^-1", 1e-7)
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON HH gating-rate fixture")
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
