# Golden leaky integrate-and-fire trace fixture

Run the closed-form comparison:

```sh
PYTHONPATH=python python -m neurosim.golden_lif tests/fixtures/omega/T014-golden-lif-trace-fixture/valid.json
```

The tool runs the configured single-neuron LIF experiment, samples voltage at the requested millisecond times, and compares it with the analytic constant-current RC response. The JSON output includes per-sample errors and the actual experiment manifest. Exit status is 0 within tolerance, 1 when the comparison or no-spike requirement fails, and 2 for invalid fixtures.

The reference only applies to the documented subthreshold case. See the [contract](contracts/T014-golden-lif-trace-fixture.md) and [validation evidence](evidence/T014-golden-lif-trace-fixture.md).
