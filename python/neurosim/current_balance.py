"""Check conservation of the production equal-and-opposite cable axial currents."""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

from .workbench.engine import cable_current

UNITS = {"voltage": "mV", "axial": "mS/cm^2", "current": "uA/cm^2"}


def diagnose(voltages_mV, axial_mS_cm2):
    if not isinstance(voltages_mV, list) or len(voltages_mV) < 2:
        raise ValueError("voltages_mV must contain at least two compartments")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in voltages_mV):
        raise ValueError("voltages_mV must contain finite numbers")
    if isinstance(axial_mS_cm2, bool) or not isinstance(axial_mS_cm2, (int, float)) or not math.isfinite(axial_mS_cm2) or axial_mS_cm2 < 0:
        raise ValueError("axial_mS_cm2 must be finite and non-negative")
    currents = cable_current(np.asarray(voltages_mV, dtype=float), axial_mS_cm2).tolist()
    net = math.fsum(currents)
    return {"units": UNITS, "axial_currents_uA_cm2": currents, "net_current_uA_cm2": net, "max_abs_balance_residual_uA_cm2": abs(net)}


def audit_fixture(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("fixture must be an object")
    if data.get("units") != UNITS:
        raise ValueError("units must be mV, mS/cm^2, and uA/cm^2")
    report = diagnose(data.get("voltages_mV"), data.get("axial_mS_cm2"))
    if "expected_axial_currents_uA_cm2" in data:
        currents_ok = np.allclose(report["axial_currents_uA_cm2"], data["expected_axial_currents_uA_cm2"], rtol=0, atol=1e-12)
        net_ok = math.isclose(report["net_current_uA_cm2"], data["expected_net_current_uA_cm2"], abs_tol=1e-12)
        report["passed"] = bool(currents_ok and net_ok)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture")
    parser.add_argument("--output")
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
    return 0 if report.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
