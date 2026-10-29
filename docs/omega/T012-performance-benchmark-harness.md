# Performance benchmark harness

Run selected CPU profiles and choose the repeat count:

```sh
PYTHONPATH=python python -m neurosim.performance_benchmark --profile hh --profile lif-128 --repeats 3
```

Available profiles are `hh`, `lif-128`, and `lif-512`. Omitting `--profile` runs all three; repeats default to 3 and must be between 1 and 20. Output JSON includes the exact validated config and manifest, wall times, median, spike/edge counts, and whether repeated voltage/spike/connectivity outputs match. `python scripts/benchmark_cpu.py` remains a compatibility entry point.

Timing is host/load dependent and does not cover GPU, API, storage, browser, or cold-start performance. See the [contract](contracts/T012-performance-benchmark-harness.md) and [validation evidence](evidence/T012-performance-benchmark-harness.md).
