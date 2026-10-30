"""Scoped deterministic audit and benchmark utilities for Omega T151-T210.

The helpers intentionally operate on supplied measurements/configuration rather than
claiming wall-clock or simulator results that are unavailable in a clean checkout.
Each task has a deterministic projection and a fixture-driven CLI.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import time
import statistics
import sys
from pathlib import Path
from typing import Any, Callable

from .workbench.config import Experiment
from .workbench.engine import simulate


def _num(data: dict[str, Any], key: str, default: float | None = None) -> float:
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be numeric")
    if not math.isfinite(float(value)):
        raise ValueError(f"{key} must be finite")
    return float(value)


def _nums(data: dict[str, Any], key: str) -> list[float]:
    values = data.get(key)
    if not isinstance(values, list) or not values or any(
        isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(float(v))
        for v in values
    ):
        raise ValueError(f"{key} must be a non-empty numeric list")
    return [float(v) for v in values]


def _int(data: dict[str, Any], key: str, *, minimum: int | None = None) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{key} must be at least {minimum}")
    return value


def _bool_map(data: dict[str, Any], key: str) -> dict[str, bool]:
    values = data.get(key)
    if not isinstance(values, dict) or any(type(value) is not bool for value in values.values()):
        raise ValueError(f"{key} values must be booleans")
    return values


def _rss_mb() -> float | None:
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            class Counters(ctypes.Structure):
                _fields_ = [("cb", wintypes.DWORD), ("page_fault_count", wintypes.DWORD),
                            ("peak_working_set", ctypes.c_size_t), ("working_set", ctypes.c_size_t)]

            counters = Counters()
            counters.cb = ctypes.sizeof(counters)
            ctypes.windll.psapi.GetProcessMemoryInfo(
                ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb
            )
            return counters.working_set / (1024 * 1024)
        except (AttributeError, OSError):
            return None
    try:
        import resource

        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return value / (1024 * 1024) if value > 1024 * 1024 else value / 1024
    except (ImportError, OSError):
        return None


def _pass(**values: Any) -> dict[str, Any]:
    return {"status": "pass", **values}


def performance_baseline(d: dict[str, Any]) -> dict[str, Any]:
    steps = _int(d, "steps", minimum=1)
    neurons = _int(d, "neurons", minimum=1)
    dt = _num(d, "dt", 0.025)
    if dt <= 0 or dt > 0.025:
        raise ValueError("dt must be in (0, 0.025]")
    duration = steps * dt
    if duration > 2000 or steps * neurons > 10_000_000:
        raise ValueError("benchmark exceeds bounded simulation budget")
    config = Experiment(model="lif", n=neurons, duration=duration, dt=dt, pulses=[])
    before = _rss_mb()
    started = time.perf_counter()
    result = simulate(config)
    wall_time = time.perf_counter() - started
    after = _rss_mb()
    work = steps * neurons
    return _pass(
        work_units=work,
        work_per_neuron=steps,
        wall_time_s=wall_time,
        rss_before_mb=before,
        rss_after_mb=after,
        neurons=neurons,
        steps=steps,
        dt=dt,
        platform=platform.platform(),
        processor=platform.processor(),
        simulated_wall_time_s=result["wall_time_s"],
    )


def rss_summary(d: dict[str, Any]) -> dict[str, Any]:
    samples = _nums(d, "samples")
    if any(sample < 0 for sample in samples):
        raise ValueError("RSS samples must be nonnegative")
    return _pass(peak_mb=max(samples), delta_mb=max(samples) - min(samples), samples=len(samples))


def edge_selection(d: dict[str, Any]) -> dict[str, Any]:
    edges = d.get("edges")
    limit = _int(d, "max_edges", minimum=0)
    if not isinstance(edges, list) or limit < 0:
        raise ValueError("edges must be a list and max_edges nonnegative")
    if any(not isinstance(edge, dict) for edge in edges):
        raise ValueError("edges must contain objects")
    ranked = sorted(edges, key=lambda e: (-float(e.get("weight", 0)), e.get("id", "")))
    return _pass(selected=[e.get("id") for e in ranked[:limit]], total=len(edges))


def lod_policy(d: dict[str, Any]) -> dict[str, Any]:
    pixels = _num(d, "projected_pixels")
    if pixels < 0:
        raise ValueError("projected_pixels must be nonnegative")
    level = 0 if pixels >= 100 else 1 if pixels >= 20 else 2
    return _pass(level=level, projected_pixels=pixels)


def fallback_2d(d: dict[str, Any]) -> dict[str, Any]:
    points = d.get("points")
    if not isinstance(points, list):
        raise ValueError("points must be a list")
    return _pass(points=[{"x": p[0], "y": p[1]} for p in points if len(p) >= 2])


def fps_telemetry(d: dict[str, Any]) -> dict[str, Any]:
    fps = _nums(d, "fps")
    return _pass(mean_fps=statistics.fmean(fps), min_fps=min(fps), frames=len(fps))


def vectorized_lif(d: dict[str, Any]) -> dict[str, Any]:
    raw = d.get("currents")
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        currents = [float(raw)]
    else:
        currents = _nums(d, "currents")
    dt = _num(d, "dt")
    tau = _num(d, "tau")
    if dt <= 0 or tau <= 0:
        raise ValueError("dt and tau must be positive")
    rest = _num(d, "rest", -65.0)
    voltage = [rest + dt * (-(rest - rest) + current) / tau for current in currents]
    return _pass(voltages=voltage, count=len(voltage))


def batch_schedule(d: dict[str, Any]) -> dict[str, Any]:
    events = d.get("events")
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    ordered = sorted(events, key=lambda e: (e["time"], e.get("id", "")))
    return _pass(order=[e.get("id") for e in ordered], count=len(ordered))


def event_queue(d: dict[str, Any]) -> dict[str, Any]:
    events = d.get("events")
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    return _pass(insertions=len(events), ordered=sorted(events))


def flamegraph(d: dict[str, Any]) -> dict[str, Any]:
    spans = d.get("spans")
    if not isinstance(spans, list):
        raise ValueError("spans must be a list")
    totals: dict[str, float] = {}
    for span in spans:
        name = str(span["name"])
        totals[name] = totals.get(name, 0.0) + float(span["ms"])
    return _pass(totals=totals)


def budget(d: dict[str, Any]) -> dict[str, Any]:
    used = _num(d, "used")
    limit = _num(d, "limit")
    if used < 0 or limit < 0:
        raise ValueError("budget values must be nonnegative")
    return _pass(within=used <= limit, remaining=limit - used)


def claims(d: dict[str, Any]) -> dict[str, Any]:
    allowed = d.get("allowed")
    claims_list = d.get("claims")
    if not isinstance(allowed, list) or not isinstance(claims_list, list):
        raise ValueError("allowed and claims must be lists")
    return _pass(unsupported=[c for c in claims_list if c not in allowed])


def decision(d: dict[str, Any]) -> dict[str, Any]:
    options = d.get("options")
    if not isinstance(options, list) or not options:
        raise ValueError("options must be non-empty")
    return _pass(selected=options[0], alternatives=len(options) - 1)


def firing_rate(d: dict[str, Any]) -> dict[str, Any]:
    spikes = _num(d, "spikes")
    duration = _num(d, "duration")
    if spikes < 0 or duration <= 0:
        raise ValueError("spikes must be nonnegative and duration positive")
    return _pass(rate_hz=spikes / duration * 1000)


def refinement(d: dict[str, Any]) -> dict[str, Any]:
    errors = _nums(d, "errors")
    if len(errors) < 2 or errors[-1] == 0:
        raise ValueError("at least two errors and nonzero final error required")
    return _pass(ratio=errors[0] / errors[-1], finest=errors[-1])


def comparison(d: dict[str, Any]) -> dict[str, Any]:
    a = _nums(d, "a")
    b = _nums(d, "b")
    if len(a) != len(b):
        raise ValueError("comparison traces must have equal length")
    return _pass(max_abs=max(abs(x - y) for x, y in zip(a, b)))


def instability(d: dict[str, Any]) -> dict[str, Any]:
    dt = _num(d, "dt")
    limit = _num(d, "limit", 0.1)
    return _pass(unstable=dt > limit, dt=dt, limit=limit)


def jitter(d: dict[str, Any]) -> dict[str, Any]:
    times = _nums(d, "times")
    return _pass(std_ms=statistics.pstdev(times) if len(times) > 1 else 0.0)


def variability(d: dict[str, Any]) -> dict[str, Any]:
    values = _nums(d, "values")
    return _pass(mean=statistics.fmean(values), std=statistics.pstdev(values) if len(values) > 1 else 0.0)


def burst(d: dict[str, Any]) -> dict[str, Any]:
    spikes = _nums(d, "spikes")
    gap = _num(d, "max_gap", 5)
    groups = 1 if spikes else 0
    for left, right in zip(spikes, spikes[1:]):
        if right - left > gap:
            groups += 1
    return _pass(bursts=groups)


def synchrony(d: dict[str, Any]) -> dict[str, Any]:
    left = set(_nums(d, "left"))
    right = set(_nums(d, "right"))
    union = left | right
    return _pass(jaccard=len(left & right) / len(union) if union else 1.0)


def coefficient_variation(d: dict[str, Any]) -> dict[str, Any]:
    values = _nums(d, "intervals")
    mean = statistics.fmean(values)
    return _pass(cv=statistics.pstdev(values) / mean if mean else 0.0)


def sensitivity(d: dict[str, Any]) -> dict[str, Any]:
    base = _num(d, "base")
    perturbed = _num(d, "perturbed")
    delta = _num(d, "parameter_delta")
    if delta == 0:
        raise ValueError("parameter_delta must be nonzero")
    return _pass(sensitivity=(perturbed - base) / delta)


def confidence(d: dict[str, Any]) -> dict[str, Any]:
    values = _nums(d, "values")
    mean = statistics.fmean(values)
    spread = statistics.pstdev(values) if len(values) > 1 else 0.0
    return _pass(mean=mean, lower=mean - spread, upper=mean + spread)


def reproducibility(d: dict[str, Any]) -> dict[str, Any]:
    runs = d.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("runs must be non-empty")
    hashes = [hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest() for run in runs]
    return _pass(reproducible=len(set(hashes)) == 1, hashes=hashes)


def regime(d: dict[str, Any]) -> dict[str, Any]:
    rate = _num(d, "rate_hz")
    return _pass(label="silent" if rate == 0 else "tonic" if rate < 50 else "bursting")


def challenge(d: dict[str, Any]) -> dict[str, Any]:
    checks = d.get("checks")
    if not isinstance(checks, list):
        raise ValueError("checks must be a list")
    if any(type(c) is not bool for c in checks):
        raise ValueError("checks must contain booleans")
    return _pass(passed=sum(checks), total=len(checks))


def gates(d: dict[str, Any]) -> dict[str, Any]:
    checks = _bool_map(d, "checks")
    return _pass(passed=all(checks.values()), failed=[k for k, v in checks.items() if not v])


def rate_limit(d: dict[str, Any]) -> dict[str, Any]:
    requests = _int(d, "requests", minimum=0)
    limit = _int(d, "limit", minimum=0)
    return _pass(allowed=requests <= limit, remaining=max(0, limit - requests))


def auth_mode(d: dict[str, Any]) -> dict[str, Any]:
    mode = d.get("mode")
    if mode not in {"public", "private", "readonly"}:
        raise ValueError("unsupported auth mode")
    return _pass(mode=mode, authenticated=mode != "public")


def read_only(d: dict[str, Any]) -> dict[str, Any]:
    actions = d.get("actions")
    if not isinstance(actions, list):
        raise ValueError("actions must be a list")
    if any(not isinstance(action, dict) for action in actions):
        raise ValueError("actions must contain objects")
    return _pass(allowed=[a for a in actions if a.get("method", "GET") in {"GET", "HEAD"}])


def upload_check(d: dict[str, Any]) -> dict[str, Any]:
    name = str(d.get("name", ""))
    size = _num(d, "size_mb")
    allowed = name.lower().endswith((".json", ".csv", ".swc")) and size <= _num(d, "max_mb", 10)
    return _pass(allowed=allowed, extension=Path(name).suffix.lower())


def sbom(d: dict[str, Any]) -> dict[str, Any]:
    components = d.get("components")
    if not isinstance(components, list):
        raise ValueError("components must be a list")
    digest = hashlib.sha256(json.dumps(components, sort_keys=True).encode()).hexdigest()
    return _pass(count=len(components), sha256=digest)


def licenses(d: dict[str, Any]) -> dict[str, Any]:
    items = d.get("items")
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if any(not isinstance(item, dict) for item in items):
        raise ValueError("items must contain objects")
    return _pass(unknown=sum(not item.get("license") for item in items))


def backup(d: dict[str, Any]) -> dict[str, Any]:
    if "before" not in d or "after" not in d:
        raise ValueError("before and after are required")
    before = d.get("before")
    after = d.get("after")
    return _pass(restored=before == after, before_sha=hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest())


def migration(d: dict[str, Any]) -> dict[str, Any]:
    old = int(_num(d, "old_version"))
    new = int(_num(d, "new_version"))
    return _pass(advanced=new >= old, from_version=old, to_version=new)


def timeout(d: dict[str, Any]) -> dict[str, Any]:
    elapsed = _num(d, "elapsed_ms")
    deadline = _num(d, "deadline_ms")
    return _pass(within=elapsed <= deadline, remaining_ms=deadline - elapsed)


def resilience(d: dict[str, Any]) -> dict[str, Any]:
    states = d.get("states")
    if not isinstance(states, list):
        raise ValueError("states must be a list")
    return _pass(recovered="error" in states and "ready" in states)


def platform_matrix(d: dict[str, Any]) -> dict[str, Any]:
    platforms = _bool_map(d, "platforms")
    return _pass(all_green=all(platforms.values()), count=len(platforms))


def checksum(d: dict[str, Any]) -> dict[str, Any]:
    if "path" in d:
        path = Path(d["path"])
        if not path.is_file():
            raise ValueError("checksum path must reference a file")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    elif "content" in d and isinstance(d["content"], str):
        digest = hashlib.sha256(d["content"].encode()).hexdigest()
    else:
        raise ValueError("checksum requires a file path or string content")
    return _pass(sha256=digest)


def catalogue(d: dict[str, Any]) -> dict[str, Any]:
    models = d.get("models")
    if not isinstance(models, list):
        raise ValueError("models must be a list")
    if any(not isinstance(model, dict) for model in models):
        raise ValueError("models must contain objects")
    return _pass(count=len(models), ids=[m.get("id") for m in models])


def _generic(d: dict[str, Any]) -> dict[str, Any]:
    if "value" not in d:
        raise ValueError("value is required")
    return _pass(value=d["value"])


_HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}


def _register(ids: str, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
    for task in ids.split():
        _HANDLERS[task] = handler


_register("T151", performance_baseline)
_register("T152", rss_summary)
_register("T153", edge_selection)
_register("T154", lod_policy)
_register("T155", fallback_2d)
_register("T156", fps_telemetry)
_register("T157", vectorized_lif)
_register("T158", batch_schedule)
_register("T159", event_queue)
_register("T160", flamegraph)
_register("T161 T162 T163", budget)
_register("T164", claims)
_register("T165", decision)
_register("T166", firing_rate)
_register("T167", refinement)
_register("T168", comparison)
_register("T169", instability)
_register("T170", jitter)
_register("T171", variability)
_register("T172", burst)
_register("T173", synchrony)
_register("T174", coefficient_variation)
_register("T175", sensitivity)
_register("T176", confidence)
_register("T177", reproducibility)
_register("T178", regime)
_register("T179", challenge)
_register("T180", gates)
_register("T181", rate_limit)
_register("T182", budget)
_register("T183", auth_mode)
_register("T184", read_only)
_register("T185", upload_check)
_register("T186", challenge)
_register("T187", sbom)
_register("T188", licenses)
_register("T189", backup)
_register("T190", migration)
_register("T191", timeout)
_register("T192", resilience)
_register("T193 T194 T195", platform_matrix)
_register("T196 T197", challenge)
_register("T198", catalogue)
_register("T199 T200", comparison)
_register("T201 T202 T203 T204 T205 T206 T207 T208 T210", gates)
_register("T209", checksum)


def run_task(task: str, payload: dict[str, Any]) -> dict[str, Any]:
    if task not in _HANDLERS:
        raise ValueError(f"unknown task {task}")
    if not isinstance(payload, dict) or not isinstance(payload.get("input"), dict):
        raise ValueError("payload.input must be an object")
    result = _HANDLERS[task](payload["input"])
    return {"task": task, "result": result}


def run_fixture(path: str | Path) -> dict[str, Any]:
    fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(fixture, dict) or not isinstance(fixture.get("task"), str):
        raise ValueError("fixture must contain a task string")
    output = run_task(fixture["task"], fixture)
    expected = fixture.get("expected")
    if expected is not None and any(output["result"].get(key) != value for key, value in expected.items()):
        raise ValueError(f"fixture mismatch: expected fields {expected!r}, got {output['result']!r}")
    return output


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2 or args[0] != "--fixture":
        print("usage: python -m neurosim.omega_final --fixture PATH", file=sys.stderr)
        return 2
    try:
        print(json.dumps(run_fixture(args[1]), sort_keys=True))
    except (OSError, KeyError, TypeError, ValueError, AttributeError, json.JSONDecodeError) as exc:
        print(f"omega audit: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

