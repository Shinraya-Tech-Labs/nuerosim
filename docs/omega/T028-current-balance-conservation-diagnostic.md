# Current balance conservation diagnostic

Run the cable axial-current diagnostic:

```sh
PYTHONPATH=python python -m neurosim.current_balance tests/fixtures/omega/T028-current-balance-conservation-diagnostic/valid.json --output balance.json
```

It reports the per-compartment axial currents and their net. Exit codes are 0 for a passing reference, 1 for a reference mismatch, and 2 for invalid input. The check applies to the equal-and-opposite axial cable term only.

See the [contract](contracts/T028-current-balance-conservation-diagnostic.md), [validation evidence](evidence/T028-current-balance-conservation-diagnostic.md), and [Day 02 report](DAY_02_REPORT.md).
