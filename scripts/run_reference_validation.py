"""Reproduce the independent reference and convergence checks for v0.2.0."""

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

from neurosim.adaptive_reference import audit_fixture as audit_hh_adaptive
from neurosim.euler_convergence import audit_fixture as audit_hh_euler
from neurosim.hh_reference import audit_fixture as audit_hh_rates
from neurosim.lif_exact_reference import audit_fixture as audit_lif_exact
from neurosim.rk4_convergence import audit_fixture as audit_hh_rk4
from neurosim.workbench.config import Experiment, Parameters, Pulse
from neurosim.workbench.engine import cable_current, simulate


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "omega"


def _fixture_comparison(name, fixture, audit, method, metric_names):
    path = FIXTURES / fixture
    result = audit(path)
    return {
        "reference": name,
        "method": method,
        "fixture": path.relative_to(ROOT).as_posix(),
        "fixture_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "passed": result["passed"],
        "metrics": {key: result[key] for key in metric_names},
    }


def _adex_comparison():
    config = Experiment(
        model="adex",
        duration=20,
        dt=0.025,
        record_every=1,
        pulses=[Pulse(start=0, stop=20, amplitude=0.3)],
    )
    actual = np.asarray(simulate(config)["final_state"])[[0, 4], 0]

    def rhs(time_ms, state):
        voltage, adaptation = state
        return [
            (-65 - voltage) / 20
            + 0.3
            + 2 / 20 * np.exp((voltage + 50) / 2)
            - adaptation,
            (0.02 * (voltage + 65) - adaptation) / 100,
        ]

    reference = solve_ivp(
        rhs,
        (0, 20),
        [-65, 0],
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
    )
    if not reference.success:
        raise RuntimeError(f"AdEx DOP853 reference failed: {reference.message}")
    errors = np.abs(actual - reference.y[:, -1])
    voltage_error, adaptation_error = map(float, errors)
    voltage_tolerance = 1e-7
    adaptation_tolerance = 1e-7
    return {
        "reference": "independently coded AdEx ODE with SciPy DOP853",
        "method": "endpoint comparison; subthreshold constant-current trajectory",
        "passed": voltage_error <= voltage_tolerance
        and adaptation_error <= adaptation_tolerance,
        "metrics": {
            "duration_ms": 20,
            "current_uA_cm2": 0.3,
            "dt_ms": 0.025,
            "rtol": 1e-10,
            "atol": 1e-12,
            "max_abs_voltage_error_mV": voltage_error,
            "voltage_tolerance_mV": voltage_tolerance,
            "max_abs_adaptation_error_uA_cm2": adaptation_error,
            "adaptation_tolerance_uA_cm2": adaptation_tolerance,
            "state": ["voltage_mV", "adaptation_uA_cm2"],
        },
    }


def _cable_comparison():
    config = Experiment(
        model="cable",
        n=3,
        duration=10,
        dt=0.025,
        record_every=1,
        parameters=Parameters(g_leak=0, axial=0.1),
        pulses=[Pulse(start=0, stop=10, amplitude=1)],
    )
    result = simulate(config)
    reference = solve_ivp(
        lambda time_ms, voltage: np.array([1.0, 0.0, 0.0])
        + cable_current(voltage, 0.1),
        (0, 10),
        [-65.0, -65.0, -65.0],
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
        dense_output=True,
    )
    if not reference.success:
        raise RuntimeError(f"cable DOP853 reference failed: {reference.message}")
    error = float(
        np.max(
            np.abs(
                np.asarray(result["voltage"])
                - reference.sol(np.asarray(result["t"]))
            )
        )
    )
    return {
        "reference": "independently integrated sealed-chain cable ODE with SciPy DOP853",
        "method": "full trajectory comparison at production sample times",
        "passed": error < 1e-7,
        "metrics": {
            "compartments": 3,
            "duration_ms": 10,
            "current_uA_cm2": 1,
            "dt_ms": 0.025,
            "rtol": 1e-11,
            "atol": 1e-12,
            "max_abs_voltage_error_mV": error,
            "tolerance_mV": 1e-7,
        },
    }


def build_report():
    comparisons = [
        _fixture_comparison(
            "Hodgkin-Huxley published 6.3 C rates and steady-state gates",
            "T022-hh-6-3-celsius-reference/valid.json",
            audit_hh_rates,
            "published rate equations and expected gate values; production initialization checked",
            [
                "temperature_c",
                "voltage_mV",
                "max_rate_error_ms^-1",
                "max_gate_error",
                "max_initialization_error",
                "tolerance",
            ],
        ),
        _fixture_comparison(
            "Leaky integrate-and-fire analytic trajectory",
            "T024-lif-exact-reference-solution/valid.json",
            audit_lif_exact,
            "piecewise constant-current closed-form voltage solution",
            ["max_abs_error_mV", "tolerance_mV", "fixture_reference_errors_mV"],
        ),
        _fixture_comparison(
            "Hodgkin-Huxley adaptive reference sensitivity",
            "T020-adaptive-reference-comparisons/valid.json",
            audit_hh_adaptive,
            "two DOP853 tolerance settings compared with production RK4",
            [
                "reference_delta_max_mV",
                "reference_limit_mV",
                "rk4_error_max_mV",
                "rk4_limit_mV",
                "sample_count",
            ],
        ),
        _fixture_comparison(
            "Hodgkin-Huxley RK4 convergence order",
            "T019-rk4-convergence-harness/valid.json",
            audit_hh_rk4,
            "two fixed-step solutions compared with independent DOP853",
            ["dt_ms", "max_abs_error_mV", "coarse_to_fine_error_ratio", "observed_order"],
        ),
        _fixture_comparison(
            "Hodgkin-Huxley Euler convergence order",
            "T018-euler-convergence-harness/valid.json",
            audit_hh_euler,
            "two forward-Euler solutions compared with independent DOP853",
            ["dt_ms", "max_abs_error_mV", "coarse_to_fine_error_ratio", "observed_order"],
        ),
        _adex_comparison(),
        _cable_comparison(),
    ]
    return {
        "schema_version": 1,
        "suite": "neurosim-v020-reference-comparisons",
        "passed": all(item["passed"] for item in comparisons),
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "comparisons": comparisons,
    }


def run_validation(output_path):
    output_path = Path(output_path)
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite reference evidence: {output_path}")
    report = build_report()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("scientific/results/v020-reference-reproduction-003.json"),
    )
    args = parser.parse_args(argv)
    try:
        report = run_validation(args.output)
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
