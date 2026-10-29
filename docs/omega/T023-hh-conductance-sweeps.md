# HH conductance sweeps

Run a bounded sodium-conductance sweep with the production HH workbench engine:

```sh
PYTHONPATH=python python -m neurosim.hh_conductance_sweep tests/fixtures/omega/T023-hh-conductance-sweeps/valid.json --output sweep.json
```

The report contains one result and simulator manifest per conductance. The command exits 0 when the reference counts and final voltages pass, 1 for a numeric mismatch, and 2 for invalid input. Sweeps support 2–12 strictly increasing `g_na` values from 0–240 mS/cm² and cap total simulated work at two million neuron-steps.

See the [contract](contracts/T023-hh-conductance-sweeps.md), [validation evidence](evidence/T023-hh-conductance-sweeps.md), and [Day 02 report](DAY_02_REPORT.md). The example is a parameter sensitivity check, not a biological validation or universal conductance response claim.
