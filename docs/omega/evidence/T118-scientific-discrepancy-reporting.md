# T118 — scientific-discrepancy-reporting

Reproducible evidence for the T118 contract and implementation.

- Positive fixture: tests/fixtures/omega/T118-scientific-discrepancy-reporting/valid.json
- Negative fixture: tests/fixtures/omega/T118-scientific-discrepancy-reporting/invalid.json
- Focused checks: tests/test_T118_edge.py and test_T118 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T118_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

