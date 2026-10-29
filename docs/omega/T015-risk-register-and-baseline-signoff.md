# Risk register and baseline signoff

Validate a baseline record with the local signoff command:

```sh
PYTHONPATH=python python -m neurosim.baseline_signoff .omega/day01-signoff.json
```

The record names the tested 40-character Git revision, evidence for the required Python/web checks, and each residual risk with severity, disposition, rationale, and evidence. A valid record with failed or missing checks returns `baseline_gate_passed: false` and exit status 1; malformed records exit 2. An accepted risk remains visible in the output and does not imply release approval.

See the [contract](contracts/T015-risk-register-and-baseline-signoff.md), [signoff evidence](evidence/T015-risk-register-and-baseline-signoff.md), and [Day 01 report](DAY_01_REPORT.md).
