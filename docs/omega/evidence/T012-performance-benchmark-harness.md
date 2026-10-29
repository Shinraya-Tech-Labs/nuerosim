# T012 validation evidence

## Real simulation benchmark

At code revision `4a9ca30`, `python -m neurosim.performance_benchmark --profile hh --repeats 2` ran the real one-neuron HH profile on Windows 11 / Python 3.14.2. Wall times were **0.821412 s** and **0.738805 s**, median **0.780109 s**. The result recorded 4 spikes, 0 edges, and identical voltage, spike, and connectivity outputs across repeats. The manifest reported the configured 50 ms duration, 0.025 ms timestep, and CPU float64 backend.

The focused harness tests passed (9 passed). The compatibility entry point `python scripts/benchmark_cpu.py --profile hh --repeats 1` also emitted valid JSON with the real HH manifest.

## Limits

These timings depend on host load and are not performance guarantees. The measurement includes simulation and result construction, but not API queuing, storage, browser rendering, cold imports, GPU execution, or comparative speedup.
