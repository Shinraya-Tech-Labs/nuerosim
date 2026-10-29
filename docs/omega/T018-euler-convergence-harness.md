# Euler convergence harness

Run the fixture-driven HH refinement comparison:

```sh
PYTHONPATH=python python -m neurosim.euler_convergence tests/fixtures/omega/T018-euler-convergence-harness/valid.json
```

The harness compares two forward-Euler timesteps with an independent DOP853 trace, reports sampled voltage errors in mV, error ratio, observed order, and experiment manifests. It returns status 0 when refinement is first-order within the declared range, 1 when the measured convergence fails, and 2 for invalid inputs.

The reference covers one 20 ms smooth constant-current HH response. Do not treat it as a general solver guarantee. See the [contract](contracts/T018-euler-convergence-harness.md) and [validation evidence](evidence/T018-euler-convergence-harness.md).
