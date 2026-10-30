# T127 — parameter-grid-sweep-executor

Reproducible evidence for the T127 contract and implementation.

- Positive fixture: tests/fixtures/omega/T127-parameter-grid-sweep-executor/valid.json
- Negative fixture: tests/fixtures/omega/T127-parameter-grid-sweep-executor/invalid.json
- Focused checks: tests/test_T127_edge.py and test_T127 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T127_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

