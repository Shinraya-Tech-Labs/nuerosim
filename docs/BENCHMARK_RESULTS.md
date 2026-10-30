# NeuroSim v0.2.0 CPU benchmark results

Run `v020-run-001` measured 11 NeuroSim workloads on **2026-10-30 19:52 UTC**.
The report captured five measured repetitions per workload after one discarded
warm-up. Every repeated workload produced the same output hash.

## Host and provenance

- Windows 11 (build 26200), AMD Ryzen 7 7730U with Radeon Graphics, 16 logical
  CPUs, and 15.35 GiB system memory.
- Python 3.14.2, NumPy 2.4.2, SciPy 1.17.1, FastAPI 0.129.0, Pydantic 2.12.5,
  and NeuroSim 0.2.0.dev0.
- Source revision: `60c00909ef07a97f5c0267db52047f68aaaf750e`.
- Workload config SHA-256:
  `4d7ee2eba90479bf8f7a86f329f060e08924dbed24c51b72f1d4d47421999b1c`.
- Runner SHA-256:
  `42aeb03eb1f470a2394cc1d82a2acd459e32a7ea6fe59d9d6aefbafeb7632934`.
- Raw report SHA-256:
  `106367d3ea4ef55dc08d1e16e48c2e3a47bc5dc6159d5dae412fb40153ab4666`.

## Measurements

Simulation durations are in seconds. Standard deviation is the sample standard
deviation across the five measured repetitions. JSON encode/decode are medians
in milliseconds. RSS is median incremental peak resident memory over each
worker's pre-work baseline, in MiB. Result bytes are the encoded JSON payload
size.

| Workload | Cells | Steps | Edges | Spikes | Sim mean | Sim median | Sim SD | Sim p95 | JSON encode | JSON decode | Peak RSS | Result bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hh-single-50ms` | 1 | 2,000 | 0 | 4 | 0.901 | 0.898 | 0.012 | 0.916 | 0.228 | 0.153 | 8.07 | 6,440 |
| `lif-single-500ms` | 1 | 20,000 | 0 | 43 | 2.739 | 2.666 | 0.183 | 2.989 | 0.744 | 0.498 | 8.19 | 26,664 |
| `adex-single-200ms` | 1 | 8,000 | 0 | 10 | 1.557 | 1.564 | 0.039 | 1.591 | 0.536 | 0.342 | 8.14 | 21,168 |
| `lif-network-8-p50-30ms` | 8 | 1,200 | 28 | 15 | 0.246 | 0.244 | 0.013 | 0.264 | 0.386 | 0.265 | 8.00 | 14,830 |
| `lif-network-16-p05-30ms` | 16 | 1,200 | 8 | 4 | 0.243 | 0.240 | 0.005 | 0.250 | 0.179 | 0.128 | 7.93 | 6,185 |
| `lif-network-64-p05-30ms` | 64 | 1,200 | 195 | 8 | 0.250 | 0.244 | 0.012 | 0.267 | 0.491 | 0.389 | 8.05 | 22,796 |
| `lif-network-256-p05-30ms` | 256 | 1,200 | 3,269 | 249 | 0.290 | 0.272 | 0.044 | 0.349 | 2.786 | 2.148 | 9.51 | 153,083 |
| `lif-network-64-p05-50ms` | 64 | 2,000 | 195 | 17 | 0.352 | 0.354 | 0.014 | 0.367 | 0.688 | 0.558 | 8.24 | 33,315 |
| `lif-network-64-p50-50ms` | 64 | 2,000 | 2,041 | 960 | 0.369 | 0.362 | 0.019 | 0.395 | 2.231 | 1.507 | 8.78 | 106,841 |
| `lif-long-1000ms` | 1 | 40,000 | 0 | 87 | 4.701 | 4.665 | 0.058 | 4.778 | 0.694 | 0.477 | 8.12 | 29,472 |
| `lif-result-serialization-64x200ms` | 64 | 8,000 | 403 | 3,607 | 1.130 | 1.109 | 0.037 | 1.178 | 35.837 | 27.977 | 20.67 | 1,501,263 |

## Reproduce

From the repository root, install the project and development dependencies and
run the harness with the committed workload set. Use a new output path for a
new run; the harness refuses to overwrite existing evidence.

```powershell
python -m pip install '.[dev]'
python scripts/run_release_benchmarks.py --config benchmarks/v020-workloads.json --output benchmarks/results/v020-run-002.json
python scripts/verify_release_benchmark_report.py --report benchmarks/results/v020-run-002.json
```

The raw report is `benchmarks/results/v020-run-001.json`. It includes all
sample-level measurements, individual output hashes, phase summaries,
environment metadata, and workload configurations. See
[`BENCHMARK_METHODOLOGY.md`](BENCHMARK_METHODOLOGY.md) for timing and memory
definitions. The verification command independently recomputes summary
statistics from the saved samples and checks that report hashes still match the
workload config and runner.

## Scope

These are serial CPU measurements on one Windows laptop. Host load, thermal
state, power policy, and OS scheduling affect timing. They do not measure GPU
execution, API or queue overhead, concurrent users, database persistence,
network transfer, browser rendering, or cold process imports. Use the exact raw
report and captured environment when comparing another run; do not treat the
values as universal performance guarantees.
