# T138 — input-current-visual-plot

Reproducible evidence for the T138 contract and implementation.

- Positive fixture: tests/fixtures/omega/T138-input-current-visual-plot/valid.json
- Negative fixture: tests/fixtures/omega/T138-input-current-visual-plot/invalid.json
- Focused checks: tests/test_T138_edge.py and test_T138 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T138_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

