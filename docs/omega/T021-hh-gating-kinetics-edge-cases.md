# HH gating kinetics edge audit

Run the fixture-based rate audit:

```sh
PYTHONPATH=python python -m neurosim.hh_rates_audit tests/fixtures/omega/T021-hh-gating-kinetics-edge-cases/valid.json
```

The audit reports all six classic HH gating rates in ms⁻¹ for each voltage, checks the exact removable-singularity limits at −40 and −55 mV, and checks nearby continuity. It exits 0 when the rates are finite/nonnegative and the limits pass, 1 when a numeric edge check fails, and 2 for invalid input.

The equations use the classic 6.3°C parameterization. See the [contract](contracts/T021-hh-gating-kinetics-edge-cases.md) and [validation evidence](evidence/T021-hh-gating-kinetics-edge-cases.md).
