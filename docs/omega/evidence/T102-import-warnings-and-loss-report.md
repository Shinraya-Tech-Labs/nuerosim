# T102 — import-warnings-and-loss-report

Reproducible evidence for the T102 contract and implementation.

- Positive fixture: tests/fixtures/omega/T102-import-warnings-and-loss-report/valid.json
- Negative fixture: tests/fixtures/omega/T102-import-warnings-and-loss-report/invalid.json
- Focused checks: tests/test_T102_edge.py and test_T102 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T102_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

