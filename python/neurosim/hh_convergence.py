"""Shared HH solver convergence calculation against an independent reference."""

import math

import numpy as np
from scipy.integrate import solve_ivp

from .workbench.config import Experiment, Pulse
from .workbench.engine import simulate


def hh_rhs(t, y, current):
    v, m, h, n = y
    am = 1 if abs(v + 40) < 1e-8 else 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))
    an = 0.1 if abs(v + 55) < 1e-8 else 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))
    return [
        current - 120 * m**3 * h * (v - 50) - 36 * n**4 * (v + 77) - 0.3 * (v + 54.387),
        am * (1 - m) - 4 * np.exp(-(v + 65) / 18) * m,
        0.07 * np.exp(-(v + 65) / 20) * (1 - h) - h / (1 + np.exp(-(v + 35) / 10)),
        an * (1 - n) - 0.125 * np.exp(-(v + 65) / 80) * n,
    ]


def run_convergence(solver, duration_ms, current_uA_cm2, coarse_dt_ms, fine_dt_ms, order_range):
    if solver not in {"euler", "rk4"}:
        raise ValueError("solver must be euler or rk4")
    values = (duration_ms, current_uA_cm2, coarse_dt_ms, fine_dt_ms)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError("duration, current, and timesteps must be finite numbers")
    if duration_ms <= 0 or not 0 < fine_dt_ms < coarse_dt_ms:
        raise ValueError("duration must be positive and fine_dt_ms < coarse_dt_ms")
    max_dt = 0.005 if solver == "euler" else 0.025
    if coarse_dt_ms > max_dt:
        if solver == "euler":
            raise ValueError("HH Euler requires dt <= .005 ms")
        raise ValueError("coarse_dt_ms must be <= 0.025 ms")
    initial = [-65, 0.052932485257, 0.596120753508, 0.317676914061]
    reference = solve_ivp(
        lambda t, y: hh_rhs(t, y, current_uA_cm2),
        (0, duration_ms),
        initial,
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
        dense_output=True,
    )
    if not reference.success:
        raise ValueError(f"DOP853 reference failed: {reference.message}")
    errors, manifests = [], []
    for dt in (coarse_dt_ms, fine_dt_ms):
        config = Experiment(
            model="hh",
            solver=solver,
            duration=duration_ms,
            dt=dt,
            record_every=1,
            pulses=[Pulse(start=0, stop=duration_ms, amplitude=current_uA_cm2)],
        )
        result = simulate(config)
        times = np.asarray(result["t"])
        voltage = np.asarray(result["voltage"])[0]
        errors.append(float(np.max(np.abs(voltage - reference.sol(times)[0]))))
        manifests.append(result["manifest"])
    if errors[0] <= 0 or errors[1] <= 0:
        raise ValueError("convergence order cannot be estimated from zero error")
    ratio = errors[0] / errors[1]
    order = math.log2(ratio)
    return {
        "passed": errors[1] < errors[0] and order_range[0] <= order <= order_range[1],
        "solver": solver,
        "duration_ms": duration_ms,
        "current_uA_cm2": current_uA_cm2,
        "dt_ms": [coarse_dt_ms, fine_dt_ms],
        "max_abs_error_mV": errors,
        "coarse_to_fine_error_ratio": ratio,
        "observed_order": order,
        "reference": "DOP853 rtol=1e-11 atol=1e-12",
        "manifests": manifests,
    }
