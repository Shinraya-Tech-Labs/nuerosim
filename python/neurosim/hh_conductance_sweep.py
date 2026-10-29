"""Run a bounded sodium-conductance sweep through the production HH engine."""

import argparse
import json
import math
import sys
from pathlib import Path

from .workbench.config import Experiment
from .workbench.engine import simulate

UNITS = {"conductance": "mS/cm^2", "time": "ms", "voltage": "mV", "current_density": "uA/cm^2"}


def run_sweep(experiment_data, conductances):
    if not isinstance(conductances, list) or not 2 <= len(conductances) <= 12:
        raise ValueError("g_na sweep must contain 2..12 values")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in conductances):
        raise ValueError("g_na values must be finite numbers")
    if any(a >= b for a, b in zip(conductances, conductances[1:])):
        raise ValueError("g_na values must be strictly increasing")
    if any(not 0 <= x <= 240 for x in conductances):
        raise ValueError("g_na values must be within 0..240 mS/cm^2")
    try:
        config = Experiment.model_validate(experiment_data)
    except Exception as exc:
        raise ValueError(f"invalid experiment: {exc}") from exc
    if config.model != "hh":
        raise ValueError("conductance sweeps require model='hh'")
    if config.duration * config.n / config.dt * len(conductances) > 2_000_000:
        raise ValueError("sweep exceeds two million neuron-steps per run")
    rows = []
    for conductance in conductances:
        run_config = config.model_copy(update={"parameters": config.parameters.model_copy(update={"g_na": conductance})})
        result = simulate(run_config)
        rows.append({
            "g_na_mS_cm2": float(conductance),
            "spike_times_ms": result["spikes"][0],
            "spike_count": len(result["spikes"][0]),
            "final_voltage_mV": float(result["final_state"][0][0]),
            "manifest": result["manifest"],
        })
    return {"units": UNITS, "sweep_parameter": "g_na", "fixed_experiment": config.model_dump(mode="json"), "runs": rows}


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")
    if fixture.get("units") != UNITS:
        raise ValueError("units must be mS/cm^2, ms, mV, and uA/cm^2")
    result = run_sweep(fixture.get("experiment"), fixture.get("g_na_mS_cm2"))
    expected_counts = fixture.get("expected_spike_counts")
    expected_voltage = fixture.get("expected_final_voltage_mV")
    tolerance = fixture.get("voltage_tolerance_mV")
    if expected_counts is None and expected_voltage is None:
        result["passed"] = None
        return result
    if not isinstance(expected_counts, list) or not isinstance(expected_voltage, list) or len(expected_counts) != len(result["runs"]) or len(expected_voltage) != len(result["runs"]):
        raise ValueError("expected outputs must match sweep length")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("voltage_tolerance_mV must be finite and positive")
    count_match = [row["spike_count"] == expected for row, expected in zip(result["runs"], expected_counts)]
    voltage_errors = [abs(row["final_voltage_mV"] - expected) for row, expected in zip(result["runs"], expected_voltage)]
    result["acceptance"] = {"spike_counts_match": count_match, "final_voltage_errors_mV": voltage_errors, "tolerance_mV": tolerance}
    result["passed"] = all(count_match) and max(voltage_errors, default=0) <= tolerance
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON HH conductance sweep fixture")
    parser.add_argument("--output", help="write the full sweep report to this JSON file")
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
    return 0 if report["passed"] is not False else 1


if __name__ == "__main__":
    raise SystemExit(main())
