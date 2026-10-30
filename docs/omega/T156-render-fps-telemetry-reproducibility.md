# T156 — render-fps-telemetry-reproducibility

Run the reproducible audit with:

`PYTHONPATH=python python -m neurosim.omega_final --fixture tests/fixtures/omega/T156-render-fps-telemetry-reproducibility/valid.json`

The fixture records the accepted input and expected result. Invalid or resource-bound inputs return exit code 2. This scoped helper reports deterministic supplied measurements and does not claim hardware-specific performance.

