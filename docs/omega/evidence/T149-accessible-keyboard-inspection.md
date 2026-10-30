# T149 — accessible-keyboard-inspection

Reproducible evidence for the T149 contract and implementation.

- Positive fixture: tests/fixtures/omega/T149-accessible-keyboard-inspection/valid.json
- Negative fixture: tests/fixtures/omega/T149-accessible-keyboard-inspection/invalid.json
- Focused checks: tests/test_T149_edge.py and test_T149 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T149_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

