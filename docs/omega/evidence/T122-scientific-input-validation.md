# T122 — scientific-input-validation

Reproducible evidence for the T122 contract and implementation.

- Positive fixture: tests/fixtures/omega/T122-scientific-input-validation/valid.json
- Negative fixture: tests/fixtures/omega/T122-scientific-input-validation/invalid.json
- Focused checks: tests/test_T122_edge.py and test_T122 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T122_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

