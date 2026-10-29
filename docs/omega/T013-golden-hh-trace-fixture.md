# Golden Hodgkin–Huxley trace fixture

Run the independent-reference comparison:

```sh
PYTHONPATH=python python -m neurosim.golden_hh tests/fixtures/omega/T013-golden-hh-trace-fixture/valid.json
```

The command simulates the fixture configuration, samples the saved voltage at each requested time, and compares the values in mV against an adaptive DOP853 reference. It reports per-sample and maximum absolute errors plus the simulation manifest. Exit status is 0 when all samples are within tolerance, 1 when the numeric comparison fails, and 2 when the fixture is invalid or cannot be audited.

The fixture uses five times for a single classic HH constant-current trace. Sparse agreement does not certify the full trajectory or biological adequacy of the model. See the [contract](contracts/T013-golden-hh-trace-fixture.md) and [validation evidence](evidence/T013-golden-hh-trace-fixture.md).
