# T147 — five-run-comparison-matrix

Reproducible evidence for the T147 contract and implementation.

- Positive fixture: tests/fixtures/omega/T147-five-run-comparison-matrix/valid.json
- Negative fixture: tests/fixtures/omega/T147-five-run-comparison-matrix/invalid.json
- Focused checks: tests/test_T147_edge.py and test_T147 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T147_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

