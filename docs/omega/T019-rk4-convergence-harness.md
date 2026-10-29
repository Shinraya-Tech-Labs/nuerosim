# RK4 convergence harness

Run the fixture-driven HH refinement comparison:

```sh
PYTHONPATH=python python -m neurosim.rk4_convergence tests/fixtures/omega/T019-rk4-convergence-harness/valid.json
```

The harness shares the independent HH/DOP853 reference with the Euler check, runs two actual RK4 experiments, and reports voltage errors in mV, error ratio, observed order, and manifests. It returns 0 when error decreases with observed order in the declared range, 1 when convergence fails, and 2 for invalid inputs.

The reference is one 20 ms constant-current HH trajectory. See the [contract](contracts/T019-rk4-convergence-harness.md) and [validation evidence](evidence/T019-rk4-convergence-harness.md).
