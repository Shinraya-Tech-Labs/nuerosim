# Refractory period scheduling

Run the scheduling audit against the production simulator:

```sh
PYTHONPATH=python python -m neurosim.refractory_audit tests/fixtures/omega/T026-refractory-period-scheduling/valid.json --output refractory.json
```

The report contains production spike times, interspike intervals, the configured refractory interval, its number of dt steps, and the experiment manifest. It exits 0 when observed intervals respect the refractory lower bound and fixture values, 1 for a mismatch, and 2 for invalid input. At least two spikes are needed to evaluate intervals.

See the [contract](contracts/T026-refractory-period-scheduling.md), [validation evidence](evidence/T026-refractory-period-scheduling.md), and [Day 02 report](DAY_02_REPORT.md).
