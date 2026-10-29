"""Compare DOP853 tolerance sensitivity with the production HH RK4 solver."""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from .hh_convergence import hh_rhs
from .workbench.config import Experiment, Pulse
from .workbench.engine import simulate


def compare_fixture(fixture):
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")
    if fixture.get("units") != {"time": "ms", "current": "uA/cm^2", "voltage": "mV"}:
        raise ValueError("units must be ms, uA/cm^2, and mV")
    keys = (
        "duration_ms", "current_uA_cm2", "dt_ms", "loose_rtol", "loose_atol_mV",
        "tight_rtol", "tight_atol_mV", "reference_limit_mV", "rk4_limit_mV",
    )
    values = {key: fixture.get(key) for key in keys}
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values.values()):
        raise ValueError("duration, current, dt, and tolerances must be finite numbers")
    if values["duration_ms"] <= 0 or values["dt_ms"] <= 0:
        raise ValueError("duration_ms and dt_ms must be positive")
    if values["loose_rtol"] <= values["tight_rtol"] or values["loose_atol_mV"] <= values["tight_atol_mV"]:
        raise ValueError("loose DOP853 tolerances must be looser than tight tolerances")
    if values["tight_rtol"] <= 0 or values["tight_atol_mV"] <= 0:
        raise ValueError("DOP853 tolerances must be positive")
    if values["reference_limit_mV"] <= 0 or values["rk4_limit_mV"] <= 0:
        raise ValueError("error limits must be positive")

    config = Experiment(
        model="hh",
        solver="rk4",
        duration=values["duration_ms"],
        dt=values["dt_ms"],
        record_every=fixture.get("record_every", 1),
        pulses=[Pulse(start=0, stop=values["duration_ms"], amplitude=values["current_uA_cm2"])],
    )
    result = simulate(config)
    times = np.asarray(result["t"])
    initial = [-65, 0.052932485257, 0.596120753508, 0.317676914061]
    references = []
    for rtol, atol in (
        (values["loose_rtol"], values["loose_atol_mV"]),
        (values["tight_rtol"], values["tight_atol_mV"]),
    ):
        solution = solve_ivp(
            lambda t, y: hh_rhs(t, y, values["current_uA_cm2"]),
            (0, values["duration_ms"]),
            initial,
            method="DOP853",
            rtol=rtol,
            atol=[atol, 1e-12, 1e-12, 1e-12],
            dense_output=True,
        )
        if not solution.success:
            raise ValueError(f"DOP853 failed: {solution.message}")
        references.append(solution.sol(times)[0])
    reference_delta = float(np.max(np.abs(references[0] - references[1])))
    rk4_error = float(np.max(np.abs(np.asarray(result["voltage"])[0] - references[1])))
    return {
        "passed": reference_delta <= values["reference_limit_mV"] and rk4_error <= values["rk4_limit_mV"],
        "reference_delta_max_mV": reference_delta,
        "reference_limit_mV": values["reference_limit_mV"],
        "rk4_error_max_mV": rk4_error,
        "rk4_limit_mV": values["rk4_limit_mV"],
        "sample_count": len(times),
        "reference_tolerances": {
            "loose": [values["loose_rtol"], values["loose_atol_mV"]],
            "tight": [values["tight_rtol"], values["tight_atol_mV"]],
        },
        "manifest": result["manifest"],
    }


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    return compare_fixture(fixture)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON adaptive reference comparison fixture")
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
