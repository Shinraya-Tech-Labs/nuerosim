# T146 — two-run-voltage-comparison

Reproducible evidence for the T146 contract and implementation.

- Positive fixture: tests/fixtures/omega/T146-two-run-voltage-comparison/valid.json
- Negative fixture: tests/fixtures/omega/T146-two-run-voltage-comparison/invalid.json
- Focused checks: tests/test_T146_edge.py and test_T146 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T146_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

