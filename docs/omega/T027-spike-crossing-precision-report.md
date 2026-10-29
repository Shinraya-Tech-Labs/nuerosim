# Spike crossing precision report

Run with `PYTHONPATH=python python -m neurosim.spike_crossing_report tests/fixtures/omega/T027-spike-crossing-precision-report/valid.json`. The report compares the solver's endpoint spike times with linear interpolation across the recorded voltage samples and includes the production manifest. `record_every=1` is required. See the [contract](contracts/T027-spike-crossing-precision-report.md), [evidence](evidence/T027-spike-crossing-precision-report.md), and [Day 02 report](DAY_02_REPORT.md).
