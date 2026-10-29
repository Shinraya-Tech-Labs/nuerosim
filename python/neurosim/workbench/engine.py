"""Deterministic float64 CPU simulation; see docs/SCIENCE.md for limitations."""

import hashlib
import json
import math
import platform
import time
from pathlib import Path
from collections import defaultdict

import numpy as np

from . import __version__
from .config import Experiment

_SOURCE_HASH = hashlib.sha256(
    b"".join(
        Path(__file__).with_name(name).read_bytes()
        for name in ("engine.py", "config.py")
    )
).hexdigest()


class Cancelled(Exception):
    """Cooperative cancellation at a simulation boundary."""


def effective_delay_steps(delay_ms, dt_ms):
    return max(1, math.ceil(delay_ms / dt_ms - 1e-10))


def rates(v):
    """Classic HH alpha/beta rates, ms^-1 at 6.3 C; removable singularities."""

    def ratio(x):
        out = np.ones_like(x, dtype=float)
        np.divide(x, -np.expm1(-x), out=out, where=np.abs(x) > 1e-8)
        return out

    return (
        ratio((v + 40) / 10),
        4 * np.exp(-(v + 65) / 18),
        0.07 * np.exp(-(v + 65) / 20),
        1 / (1 + np.exp(-(v + 35) / 10)),
        0.1 * ratio((v + 55) / 10),
        0.125 * np.exp(-(v + 65) / 80),
    )


def initial_state(config):
    state = np.zeros((5, config.n))  # V,m,h,n,w
    state[0] = config.initial_voltage
    am, bm, ah, bh, an, bn = rates(state[0])
    state[1:4] = np.array([am / (am + bm), ah / (ah + bh), an / (an + bn)])
    return state


def cable_current(v, coupling):
    """Equal-area sealed chain. Each edge contributes equal/opposite currents."""
    result = np.zeros_like(v)
    flow = coupling * np.diff(v)
    result[:-1] += flow
    result[1:] -= flow
    return result


def derivative(state, current, ge, gi, config):
    p = config.parameters
    v, m, h, n, w = state
    d = np.zeros_like(state)
    drive = current + ge * (0 - v) + gi * (-80 - v)
    if config.model == "hh":
        am, bm, ah, bh, an, bn = rates(v)
        d[0] = (
            drive
            - p.g_na * m**3 * h * (v - p.e_na)
            - p.g_k * n**4 * (v - p.e_k)
            - p.g_leak * (v - p.e_leak)
        ) / p.cm
        d[1:4] = np.array(
            [am * (1 - m) - bm * m, ah * (1 - h) - bh * h, an * (1 - n) - bn * n]
        )
    elif config.model == "cable":
        d[0] = (drive - p.g_leak * (v - p.e_leak) + cable_current(v, p.axial)) / p.cm
    else:
        d[0] = (p.rest - v) / p.tau_m + drive / p.cm
        if config.model == "adex":
            # Numerical spike cutoff is threshold+5*Delta; stages are bounded
            # at cutoff to avoid evaluating the divergent exponential after a spike.
            d[0] += (
                p.delta_t
                / p.tau_m
                * np.exp(np.minimum((v - p.threshold) / p.delta_t, 5))
                - w / p.cm
            )
            d[4] = (p.a * (v - p.rest) - w) / p.tau_w
    return d


def connectivity(config):
    rng = np.random.default_rng(config.seed)
    mask = rng.random((config.n, config.n)) < config.probability
    np.fill_diagonal(mask, False)
    src, tgt = np.nonzero(mask)
    n_exc = config.n - round(config.n * config.inhibitory_fraction)
    return [(int(s), int(t), bool(s >= n_exc)) for s, t in zip(src, tgt)]


def manifest(config):
    cfg = config.model_dump()
    digest = hashlib.sha256(
        json.dumps(cfg, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "schema_version": 1,
        "config": cfg,
        "config_sha256": digest,
        "engine_sha256": _SOURCE_HASH,
        "software_version": __version__,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
        "backend": "cpu-float64",
        "units": {
            "time": "ms",
            "voltage": "mV",
            "current": "uA/cm^2",
            "conductance": "mS/cm^2",
            "capacitance": "uF/cm^2",
        },
    }


def simulate(config: Experiment, progress=None, cancelled=None):
    start = time.perf_counter()
    state = initial_state(config)
    edges = connectivity(config)
    if len(edges) > 32768:
        raise ValueError("limit: 32768 realized synapses; reduce connectivity")
    outgoing = defaultdict(list)
    for src, tgt, inhibitory in edges:
        outgoing[src].append((tgt, inhibitory))
    pending = defaultdict(list)
    pending_count = 0
    ge, gi = np.zeros(config.n), np.zeros(config.n)
    refractory_until = np.zeros(config.n)
    times, voltages = [0.0], [state[0].copy()]
    spikes = [[] for _ in range(config.n)]
    steps = round(config.duration / config.dt)
    delay_steps = effective_delay_steps(config.delay, config.dt)
    p = config.parameters
    for step in range(steps):
        if step % 20 == 0:
            if cancelled and cancelled():
                raise Cancelled()
            if progress:
                progress(step / steps)
        arrivals = pending.pop(step, [])
        pending_count -= len(arrivals)
        for target, inhibitory in arrivals:
            (gi if inhibitory else ge)[target] += config.weight
        current = np.zeros(config.n)
        for pulse in config.pulses:
            if round(pulse.start / config.dt) <= step < round(pulse.stop / config.dt):
                current[pulse.target] += pulse.amplitude
        t = step * config.dt
        old_v = state[0].copy()
        active = t + 1e-10 >= refractory_until

        def f(s, offset):
            decay = np.exp(-offset / config.tau_syn)
            ds = derivative(s, current, ge * decay, gi * decay, config)
            if config.model in ("lif", "adex"):
                ds[0, ~active] = 0
            return ds

        with np.errstate(over="raise", invalid="raise", divide="raise"):
            h = config.dt
            k1 = f(state, 0)
            if config.solver == "rk4":
                k2 = f(state + h * k1 / 2, h / 2)
                k3 = f(state + h * k2 / 2, h / 2)
                k4 = f(state + h * k3, h)
                state += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            else:
                state += h * k1
        ge *= np.exp(-config.dt / config.tau_syn)
        gi *= np.exp(-config.dt / config.tau_syn)
        if not np.isfinite(state).all() or np.max(np.abs(state[0])) > 1000:
            raise FloatingPointError("unstable integration; reduce dt or input")
        if config.model == "hh" and (
            np.min(state[1:4]) < -1e-6 or np.max(state[1:4]) > 1 + 1e-6
        ):
            raise FloatingPointError("HH gates left [0,1]; reduce dt")
        end = (step + 1) * h
        if config.model == "hh":
            fired = np.flatnonzero((old_v < 0) & (state[0] >= 0))
        elif config.model in ("lif", "adex"):
            threshold = p.threshold + (5 * p.delta_t if config.model == "adex" else 0)
            fired = np.flatnonzero(active & (state[0] >= threshold))
            state[0, fired] = p.reset
            if config.model == "adex":
                state[4, fired] += p.b
            refractory_until[fired] = end + p.refractory
        else:
            fired = []
        for source in fired:
            spikes[source].append(end)
            pending_count += len(outgoing[source])
            if pending_count > 1_000_000:
                raise ValueError("limit: one million pending synaptic events")
            pending[step + 1 + delay_steps].extend(outgoing[source])
        if (step + 1) % config.record_every == 0 or step + 1 == steps:
            times.append(end)
            voltages.append(state[0].copy())
    if cancelled and cancelled():
        raise Cancelled()
    if progress:
        progress(1.0)
    bin_edges = np.linspace(
        0, config.duration, max(2, math.ceil(config.duration / 10) + 1)
    )
    counts, _ = np.histogram([t for train in spikes for t in train], bin_edges)
    return {
        "t": times,
        "voltage": np.array(voltages).T.tolist(),
        "spikes": spikes,
        "edges": edges,
        "rate_time": ((bin_edges[1:] + bin_edges[:-1]) / 2).tolist(),
        "rate_hz": (counts / config.n / (np.diff(bin_edges) / 1000)).tolist(),
        "mean_rate_hz": sum(map(len, spikes)) / config.n / (config.duration / 1000),
        "final_state": state.tolist(),
        "manifest": manifest(config),
        "effective_delay_ms": delay_steps * config.dt,
        "wall_time_s": time.perf_counter() - start,
    }
