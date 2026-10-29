# Adaptive reference comparisons

Run the fixture comparison:

```sh
PYTHONPATH=python python -m neurosim.adaptive_reference tests/fixtures/omega/T020-adaptive-reference-comparisons/valid.json
```

The audit runs the production HH RK4 config and two independent DOP853 integrations with different tolerances. It reports the difference between adaptive references separately from RK4-to-tight-reference error, both in mV, and returns the actual simulation manifest. Exit status is 0 within both limits, 1 when a numeric limit fails, and 2 for invalid input or solver failure.

See the [contract](contracts/T020-adaptive-reference-comparisons.md) and [validation evidence](evidence/T020-adaptive-reference-comparisons.md).
