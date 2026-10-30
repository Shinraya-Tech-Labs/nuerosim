# T128 — parameter-random-sweep-executor

Reproducible evidence for the T128 contract and implementation.

- Positive fixture: tests/fixtures/omega/T128-parameter-random-sweep-executor/valid.json
- Negative fixture: tests/fixtures/omega/T128-parameter-random-sweep-executor/invalid.json
- Focused checks: tests/test_T128_edge.py and test_T128 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T128_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

