"""Measure HH forward-Euler convergence against an independent DOP853 trace."""

import argparse
import json
import sys
from pathlib import Path

from .hh_convergence import run_convergence

def run_euler_convergence(duration_ms, current_uA_cm2, coarse_dt_ms, fine_dt_ms):
    return run_convergence(
        "euler", duration_ms, current_uA_cm2, coarse_dt_ms, fine_dt_ms, (0.7, 1.3)
    )


def audit_fixture(path):
    try:
        fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read fixture: {exc}") from exc
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be an object")
    return run_euler_convergence(
        fixture.get("duration_ms"),
        fixture.get("current_uA_cm2"),
        fixture.get("coarse_dt_ms"),
        fixture.get("fine_dt_ms"),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", help="JSON convergence input fixture")
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
