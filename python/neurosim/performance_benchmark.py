"""Run repeatable serial CPU benchmarks for built-in NeuroSim profiles."""

import argparse
import json
import math
import platform
import statistics
import sys

from .workbench.config import Experiment, Pulse
from .workbench.engine import simulate


PROFILES = {
    "hh": ("hh", 1, 50, 0.0),
    "lif-128": ("lif", 128, 100, 0.02),
    "lif-512": ("lif", 512, 100, 0.02),
}


def median_seconds(samples):
    values = list(samples)
    if not values or any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("samples must contain finite non-negative seconds")
    return statistics.median(values)


def profile_config(name):
    if name not in PROFILES:
        raise ValueError(f"unknown benchmark profile: {name}")
    model, n, duration, probability = PROFILES[name]
    return Experiment(
        model=model,
        n=n,
        duration=duration,
        dt=0.025,
        record_every=10,
        seed=42,
        probability=probability,
        pulses=[Pulse(start=0, stop=duration, amplitude=10)],
    )


def run_profile(name, repeats=3, simulate_fn=simulate):
    if not isinstance(repeats, int) or not 1 <= repeats <= 20:
        raise ValueError("repeats must be between 1 and 20")
    config = profile_config(name)
    samples = [simulate_fn(config) for _ in range(repeats)]
    wall_seconds = [float(result["wall_time_s"]) for result in samples]
    if any(not math.isfinite(value) or value < 0 for value in wall_seconds):
        raise ValueError("simulation returned invalid wall time")
    first = samples[0]
    return {
        "profile": name,
        "config": config.model_dump(mode="json"),
        "wall_seconds": wall_seconds,
        "median_seconds": median_seconds(wall_seconds),
        "spikes": sum(map(len, first["spikes"])),
        "edges": len(first["edges"]),
        "manifest": first["manifest"],
        "repeats_identical": all(
            result["voltage"] == first["voltage"]
            and result["spikes"] == first["spikes"]
            and result["edges"] == first["edges"]
            for result in samples[1:]
        ),
    }


def run_benchmarks(profiles=None, repeats=3):
    selected = list(profiles or PROFILES)
    if not selected:
        raise ValueError("at least one benchmark profile is required")
    if len(selected) != len(set(selected)):
        raise ValueError("benchmark profiles must not repeat")
    rows = [run_profile(name, repeats) for name in selected]
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "repeats": repeats,
        "benchmarks": rows,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", action="append", choices=PROFILES)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        report = run_benchmarks(args.profile, args.repeats)
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
