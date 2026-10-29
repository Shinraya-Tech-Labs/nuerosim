# HH 6.3°C reference audit

Run the fixed-temperature reference audit:

```sh
PYTHONPATH=python python -m neurosim.hh_reference tests/fixtures/omega/T022-hh-6-3-celsius-reference/valid.json
```

The audit reports the six classic HH gating rates at the fixture voltage, derives the three steady-state gates, and compares them with both the fixture's reference values and the production HH initializer. It exits 0 when all values meet tolerance, 1 when a numeric comparison fails, and 2 for invalid input. Only the fixed 6.3°C parameterization is supported; other temperatures are rejected because this model has no temperature scaling.

See the [contract](contracts/T022-hh-6-3-celsius-reference.md), [validation evidence](evidence/T022-hh-6-3-celsius-reference.md), and [scientific model limits](../SCIENCE.md).
