"""Audit reported synaptic delay scheduling in a workbench result JSON."""

import json
import math
import sys
from pathlib import Path

from pydantic import ValidationError

from neurosim.workbench.config import Experiment
from neurosim.workbench.engine import effective_delay_steps


def audit_schedule(result: dict) -> dict[str, object]:
    manifest = result.get("manifest") if isinstance(result, dict) else None
    units = manifest.get("units") if isinstance(manifest, dict) else None
    if not isinstance(units, dict) or units.get("time") != "ms":
        raise ValueError('manifest time unit must be "ms"')
    config = manifest.get("config")
    if not isinstance(config, dict) or not {"delay", "dt"} <= config.keys():
        raise ValueError("manifest config must include delay and dt")
    try:
        experiment = Experiment.model_validate(config)
    except ValidationError as error:
        raise ValueError(f"invalid experiment config: {error}") from None

    steps = effective_delay_steps(experiment.delay, experiment.dt)
    effective_ms = steps * experiment.dt
    reported_ms = result.get("effective_delay_ms")
    if isinstance(reported_ms, bool) or not isinstance(reported_ms, (int, float)):
        raise ValueError("effective_delay_ms does not match timestep scheduling")
    try:
        reported_ms = float(reported_ms)
    except OverflowError:
        raise ValueError("effective_delay_ms does not match timestep scheduling") from None
    if not math.isfinite(reported_ms) or not math.isclose(
        reported_ms, effective_ms, rel_tol=1e-12, abs_tol=1e-12
    ):
        raise ValueError("effective_delay_ms does not match timestep scheduling")
    return {
        "status": "pass",
        "requested_delay_ms": experiment.delay,
        "dt_ms": experiment.dt,
        "delay_steps": steps,
        "effective_delay_ms": round(effective_ms, 12),
        "rounding_ms": round(effective_ms - experiment.delay, 12),
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python -m neurosim.event_schedule RESULT.json", file=sys.stderr)
        raise SystemExit(2)
    try:
        result = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        report = audit_schedule(result)
        output = json.dumps(report, indent=2, sort_keys=True, allow_nan=False)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        print(f"event schedule audit: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
