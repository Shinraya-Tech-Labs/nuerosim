# T126 — persistent-queue-restart-tests

Reproducible evidence for the T126 contract and implementation.

- Positive fixture: tests/fixtures/omega/T126-persistent-queue-restart-tests/valid.json
- Negative fixture: tests/fixtures/omega/T126-persistent-queue-restart-tests/invalid.json
- Focused checks: tests/test_T126_edge.py and test_T126 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T126_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

