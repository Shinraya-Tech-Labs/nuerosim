# T132 — result-archive-validation

Reproducible evidence for the T132 contract and implementation.

- Positive fixture: tests/fixtures/omega/T132-result-archive-validation/valid.json
- Negative fixture: tests/fixtures/omega/T132-result-archive-validation/invalid.json
- Focused checks: tests/test_T132_edge.py and test_T132 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T132_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

