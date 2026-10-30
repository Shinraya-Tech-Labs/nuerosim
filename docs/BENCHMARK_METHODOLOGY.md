# CPU benchmark methodology

The release harness is `scripts/run_release_benchmarks.py`, driven by
`benchmarks/v020-workloads.json`. It measures actual NeuroSim simulations and
JSON result handling. It does not estimate times from operation counts.

## Reproduce

Install the project and development dependencies, then run from the repository
root. Each output path must be new; the harness refuses to overwrite previous
evidence.

```powershell
python -m pip install '.[dev]'
python scripts/run_release_benchmarks.py --config benchmarks/v020-workloads.json --output benchmarks/results/v020-run-005.json
python scripts/verify_release_benchmark_report.py --report benchmarks/results/v020-run-005.json
```

The committed workload file selects five measured repetitions and one
discarded warm-up for each case. To repeat a run, supply a new output path and
keep the workload file unchanged. The report stores its canonical JSON config
SHA-256, an LF-normalized harness SHA-256, the source Git revision, and the
complete configuration for every case. Canonical config JSON and normalized
source line endings make the input hashes stable across Windows and Unix. The
`.gitattributes` rule preserves raw benchmark JSON bytes so the report file
SHA-256 remains the same after checkout.

## Workloads

The suite includes a 50 ms single-cell HH run, 500 ms and 1000 ms LIF runs, a
200 ms AdEx run, an eight-cell seeded network, 16/64/256-cell scaling, 64-cell
connectivity at probabilities 0.05 and 0.5, and a 64-cell 200 ms result
serialization/retrieval case. Each model run uses the recorded fixed timestep,
seed, pulse, connectivity, and recording interval in the JSON config. The
serialization case materializes the simulation result, encodes it with the
Python standard-library JSON encoder, then decodes the payload in memory.

## Measurements

Each warm-up and sample runs in a fresh Python subprocess with the same
workload. Import and process-launch time are excluded from phase timings; the
worker records configuration validation (`setup`), simulation, JSON encoding,
and JSON decoding separately with `time.perf_counter`. It records neuron and
time-step counts, realized edges, spikes, serialized payload size, and a hash of
the deterministic simulation outputs. Repeated samples must produce the same
output hash or the run fails.

For every timed phase and the total of measured phases, the report gives count,
mean, median, sample standard deviation, p95, minimum, and maximum. The p95 uses
linear interpolation over the measured repetitions. Raw per-sample timings are
retained in the report.

Every sample also records baseline working-set size, peak working-set/RSS, and
incremental peak over baseline. On Windows these come from
`GetProcessMemoryInfo`; on Unix they come from the process high-water RSS and,
where available, `/proc/self/statm`. RSS includes interpreter and imported
libraries; the report keeps the baseline and incremental peak visible so the
scope is clear. Hardware metadata includes CPU model, logical CPU count, total
system memory, OS, Python and dependency versions, thread-related environment
variables, and the source/config hashes.

## Limits

These are serial CPU measurements on the recorded host, not universal speed
claims. Host load, power policy, thermal state, and OS scheduling can change
results. No CUDA, GPU, WebGPU, MPI, distributed execution, storage service,
API queuing, browser rendering, cold import, or concurrent-user performance is
measured. JSON retrieval here means decoding the serialized result in memory;
the database/API lifecycle is tested separately. Benchmark result artifacts
must be interpreted with their captured environment and raw samples.
