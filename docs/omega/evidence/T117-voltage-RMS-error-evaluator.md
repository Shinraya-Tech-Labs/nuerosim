# T117 — voltage-RMS-error-evaluator

Reproducible evidence for the T117 contract and implementation.

- Positive fixture: tests/fixtures/omega/T117-voltage-RMS-error-evaluator/valid.json
- Negative fixture: tests/fixtures/omega/T117-voltage-RMS-error-evaluator/invalid.json
- Focused checks: tests/test_T117_edge.py and test_T117 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T117_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

