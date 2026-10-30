# T163 — duration-memory-bound-stress

Run the reproducible audit with:

`PYTHONPATH=python python -m neurosim.omega_final --fixture tests/fixtures/omega/T163-duration-memory-bound-stress/valid.json`

The fixture records the accepted input and expected result. Invalid or resource-bound inputs return exit code 2. This scoped helper reports deterministic supplied measurements and does not claim hardware-specific performance.

