# T115 — solver-tolerance-sweep-matrix

Reproducible evidence for the T115 contract and implementation.

- Positive fixture: tests/fixtures/omega/T115-solver-tolerance-sweep-matrix/valid.json
- Negative fixture: tests/fixtures/omega/T115-solver-tolerance-sweep-matrix/invalid.json
- Focused checks: tests/test_T115_edge.py and test_T115 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T115_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

