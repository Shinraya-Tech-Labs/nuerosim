# T136 — exhibition-picker-UX

Reproducible evidence for the T136 contract and implementation.

- Positive fixture: tests/fixtures/omega/T136-exhibition-picker-UX/valid.json
- Negative fixture: tests/fixtures/omega/T136-exhibition-picker-UX/invalid.json
- Focused checks: tests/test_T136_edge.py and test_T136 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T136_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

