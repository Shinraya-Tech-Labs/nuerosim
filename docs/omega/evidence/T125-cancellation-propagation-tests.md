# T125 — cancellation-propagation-tests

Reproducible evidence for the T125 contract and implementation.

- Positive fixture: tests/fixtures/omega/T125-cancellation-propagation-tests/valid.json
- Negative fixture: tests/fixtures/omega/T125-cancellation-propagation-tests/invalid.json
- Focused checks: tests/test_T125_edge.py and test_T125 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T125_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

