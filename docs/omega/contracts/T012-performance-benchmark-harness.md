# T012 — performance benchmark harness

## Purpose

Measure serial CPU execution time for fixed, seeded NeuroSim experiment profiles and report the corresponding real result metadata.

## Contract

- **Input:** one or more named built-in profiles (`hh`, `lif-128`, `lif-512`) and repeat count from 1 to 20. Defaults are all profiles and 3 repeats.
- **Output:** JSON with environment metadata and, per profile, exact input configuration, per-run simulation wall seconds, median seconds, spike/edge counts, manifest, and equality of repeated voltage/spike/connectivity outputs.
- **Units:** simulation durations and wall times are seconds; biological experiment durations remain milliseconds; sizes/counts are integers.
- **Determinism:** fixed seed and profile configuration; timing is measured and intentionally variable. Repeated scientific outputs are compared exactly.
- **Acceptance examples:** 3 samples `[1.0, 2.0, 3.0]` have median `2.0`; the default `hh` profile runs a real one-neuron Hodgkin–Huxley simulation.
- **Errors:** reject unknown profiles, repeat counts outside 1–20, or simulation failures with nonzero CLI status.
- **Exclusions:** results are host/load dependent and are not performance guarantees. This CPU harness does not measure GPU, API queue, database, browser, or cold-start performance.
