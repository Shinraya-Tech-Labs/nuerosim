"""Validate declared workbench units and mean-rate dimensional arithmetic."""

import json
import math
import sys
from pathlib import Path

from .units import Quantity, Unit, mean_population_rate

EXPECTED_UNITS = {
    "time": "ms",
    "voltage": "mV",
    "current": "uA/cm^2",
    "conductance": "mS/cm^2",
    "capacitance": "uF/cm^2",
}
RATE_REL_TOL = 1e-12
RATE_ABS_TOL = 1e-12


def _finite_number(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = float(value)
    except OverflowError:
        raise ValueError(f"{name} must be a finite number") from None
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number")
    return number


def audit_units(result: dict) -> dict[str, object]:
    if not isinstance(result, dict):
        raise ValueError("result must be an object")
    manifest = result.get("manifest")
    config = manifest.get("config") if isinstance(manifest, dict) else None
    units = manifest.get("units") if isinstance(manifest, dict) else None
    if units != EXPECTED_UNITS:
        raise ValueError("manifest units do not match workbench contract")
    if not isinstance(config, dict):
        raise ValueError("manifest config must be an object")

    duration_ms = _finite_number(config.get("duration"), "duration_ms")
    neurons = config.get("n")
    duration = Quantity(duration_ms, Unit.MILLISECOND)
    if duration_ms <= 0 or duration.to(Unit.SECOND).value <= 0:
        raise ValueError("duration_ms must be positive")
    if isinstance(neurons, bool) or not isinstance(neurons, int) or neurons <= 0:
        raise ValueError("n must be a positive integer")

    spikes = result.get("spikes")
    if not isinstance(spikes, list) or len(spikes) != neurons:
        raise ValueError("spikes must contain one train per neuron")
    spike_count = 0
    for train in spikes:
        if not isinstance(train, list):
            raise ValueError("each spike train must be a list")
        for spike_ms in train:
            spike_ms = _finite_number(spike_ms, "spike_time_ms")
            if not 0 <= spike_ms <= duration_ms:
                raise ValueError("spike_time_ms must be within the simulation duration")
            spike_count += 1

    computed_rate_hz = mean_population_rate(spike_count, neurons, duration).value
    stored_rate_hz = _finite_number(result.get("mean_rate_hz"), "mean_rate_hz")
    if not math.isclose(
        stored_rate_hz,
        computed_rate_hz,
        rel_tol=RATE_REL_TOL,
        abs_tol=RATE_ABS_TOL,
    ):
        raise ValueError("mean_rate_hz does not match spike count and duration")
    return {
        "status": "pass",
        "units": dict(EXPECTED_UNITS),
        "duration_ms": duration_ms,
        "neurons": neurons,
        "spike_count": spike_count,
        "mean_rate_hz": computed_rate_hz,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python -m neurosim.units_audit RESULT.json", file=sys.stderr)
        raise SystemExit(2)
    try:
        result = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        report = audit_units(result)
        output = json.dumps(report, indent=2, sort_keys=True, allow_nan=False)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        print(f"units audit: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
