"""Measured serial baseline, three repeats; no GPU speedup inference."""

import json
import platform
import statistics
from neurosim.workbench.config import Experiment, Pulse
from neurosim.workbench.engine import simulate

rows = []
for model, n, duration in [("hh", 1, 50), ("lif", 128, 100), ("lif", 512, 100)]:
    config = Experiment(
        model=model,
        n=n,
        duration=duration,
        probability=0.02 if n > 1 else 0,
        record_every=10,
        pulses=[Pulse(start=0, stop=duration, amplitude=10)],
    )
    samples = [simulate(config) for _ in range(3)]
    rows.append(
        {
            "model": model,
            "n": n,
            "duration_ms": duration,
            "dt_ms": config.dt,
            "wall_seconds": [r["wall_time_s"] for r in samples],
            "median_seconds": statistics.median(r["wall_time_s"] for r in samples),
            "spikes": sum(map(len, samples[0]["spikes"])),
            "edges": len(samples[0]["edges"]),
            "manifest": samples[0]["manifest"],
            "repeats_identical": all(
                r["voltage"] == samples[0]["voltage"] for r in samples
            ),
        }
    )
print(
    json.dumps(
        {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python": platform.python_version(),
            "benchmarks": rows,
            "cuda": "blocked: nvcc and NVIDIA runtime not found",
            "mpi": "blocked: MPI executable not found",
        },
        indent=2,
    )
)
