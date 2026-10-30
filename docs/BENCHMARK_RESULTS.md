# NeuroSim v0.2.0 CPU benchmark results

Run `v020-run-004` measured 11 NeuroSim workloads on **2026-10-30 20:16 UTC**.
The report captured five measured repetitions per workload after one discarded
warm-up. Every repeated workload produced the same output hash.

## Host and provenance

- Windows 11 (build 26200), AMD Ryzen 7 7730U with Radeon Graphics, 16 logical
  CPUs, and 15.35 GiB system memory.
- Python 3.14.2, NumPy 2.4.2, SciPy 1.17.1, FastAPI 0.129.0, Pydantic 2.12.5,
  and NeuroSim 0.2.0.dev0.
- Source revision: `89f9745a87dd01bf54f554d739cec74175becddc`.
- Workload config SHA-256:
  `7b009521a3b95d838d8cb93a9301424f67d6251448ab24a53c77acd873776429`.
- Runner SHA-256:
  `a17b49db4f8b8c1ac6ed57df8d92726d1fbbfde9aa7e357e87504297452914d0`.
- Raw report SHA-256:
  `72b27b56508b92e8aefd072375b928170e9f4b2b3315ad29afa8d93655a040bf`.

## Measurements

Simulation durations are in seconds. Standard deviation is the sample standard
deviation across the five measured repetitions. JSON encode/decode are medians
in milliseconds. RSS is median incremental peak resident memory over each
worker's pre-work baseline, in MiB. Result bytes are the encoded JSON payload
size.

| Workload | Cells | Steps | Edges | Spikes | Sim mean | Sim median | Sim SD | Sim p95 | JSON encode | JSON decode | Peak RSS | Result bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `hh-single-50ms` | 1 | 2,000 | 0 | 4 | 0.861 | 0.860 | 0.027 | 0.891 | 0.210 | 0.148 | 7.95 | 6,440 |
| `lif-single-500ms` | 1 | 20,000 | 0 | 43 | 2.474 | 2.463 | 0.029 | 2.512 | 0.645 | 0.427 | 8.07 | 26,664 |
| `adex-single-200ms` | 1 | 8,000 | 0 | 10 | 1.492 | 1.492 | 0.021 | 1.516 | 0.536 | 0.346 | 8.00 | 21,168 |
| `lif-network-8-p50-30ms` | 8 | 1,200 | 28 | 15 | 0.241 | 0.237 | 0.010 | 0.253 | 0.375 | 0.265 | 7.96 | 14,830 |
| `lif-network-16-p05-30ms` | 16 | 1,200 | 8 | 4 | 0.242 | 0.242 | 0.006 | 0.249 | 0.180 | 0.139 | 8.05 | 6,185 |
| `lif-network-64-p05-30ms` | 64 | 1,200 | 195 | 8 | 0.266 | 0.261 | 0.016 | 0.285 | 0.489 | 0.413 | 8.09 | 22,796 |
| `lif-network-256-p05-30ms` | 256 | 1,200 | 3,269 | 249 | 0.273 | 0.271 | 0.012 | 0.290 | 2.779 | 2.167 | 9.46 | 153,083 |
| `lif-network-64-p05-50ms` | 64 | 2,000 | 195 | 17 | 0.356 | 0.350 | 0.014 | 0.373 | 0.693 | 0.571 | 8.23 | 33,315 |
| `lif-network-64-p50-50ms` | 64 | 2,000 | 2,041 | 960 | 0.384 | 0.377 | 0.026 | 0.419 | 2.190 | 1.509 | 8.77 | 106,841 |
| `lif-long-1000ms` | 1 | 40,000 | 0 | 87 | 4.756 | 4.727 | 0.068 | 4.849 | 0.720 | 0.478 | 8.12 | 29,472 |
| `lif-result-serialization-64x200ms` | 64 | 8,000 | 403 | 3,607 | 1.103 | 1.097 | 0.015 | 1.124 | 35.424 | 26.921 | 20.82 | 1,501,263 |

## Reproduce

From the repository root, install the project and development dependencies and
run the harness with the committed workload set. Use a new output path for a
new run; the harness refuses to overwrite existing evidence.

```powershell
python -m pip install '.[dev]'
python scripts/run_release_benchmarks.py --config benchmarks/v020-workloads.json --output benchmarks/results/v020-run-005.json
python scripts/verify_release_benchmark_report.py --report benchmarks/results/v020-run-005.json
```

The raw report is `benchmarks/results/v020-run-004.json`. It includes all
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
