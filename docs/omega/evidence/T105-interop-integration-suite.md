# T105 — interop-integration-suite

Reproducible evidence for the T105 contract and implementation.

- Positive fixture: tests/fixtures/omega/T105-interop-integration-suite/valid.json
- Negative fixture: tests/fixtures/omega/T105-interop-integration-suite/invalid.json
- Focused checks: tests/test_T105_edge.py and test_T105 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T105_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

