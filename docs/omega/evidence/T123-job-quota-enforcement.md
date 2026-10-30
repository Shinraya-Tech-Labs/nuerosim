# T123 — job-quota-enforcement

Reproducible evidence for the T123 contract and implementation.

- Positive fixture: tests/fixtures/omega/T123-job-quota-enforcement/valid.json
- Negative fixture: tests/fixtures/omega/T123-job-quota-enforcement/invalid.json
- Focused checks: tests/test_T123_edge.py and test_T123 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T123_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

