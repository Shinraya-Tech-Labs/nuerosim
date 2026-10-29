# AdEx threshold dynamics

Run the production threshold audit:

```sh
PYTHONPATH=python python -m neurosim.adex_threshold_audit tests/fixtures/omega/T025-adex-threshold-dynamics/valid.json --output adex-threshold.json
```

The report includes the numerical cutoff (`threshold + 5*Delta`), actual spike times/count and intervals, and the simulator manifest. It exits 0 when expected spike times pass, 1 for a mismatch, and 2 for invalid input. The cutoff is a numerical device in this implementation; results depend on timestep and parameters.

See the [contract](contracts/T025-adex-threshold-dynamics.md), [validation evidence](evidence/T025-adex-threshold-dynamics.md), and [Day 02 report](DAY_02_REPORT.md).
