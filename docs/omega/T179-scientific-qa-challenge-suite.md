# T179 — scientific-qa-challenge-suite

Run:

`PYTHONPATH=python python -m neurosim.omega_final --fixture tests/fixtures/omega/T179-scientific-qa-challenge-suite/valid.json`

The audit validates the fixture boundary and reports a deterministic metric. Missing, non-finite, or mismatched units are rejected; the helper does not generalize beyond the supplied experiment.

