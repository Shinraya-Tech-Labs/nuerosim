# T109 — Brian2-sparse-spike-reference

Reproducible evidence for the T109 contract and implementation.

- Positive fixture: tests/fixtures/omega/T109-Brian2-sparse-spike-reference/valid.json
- Negative fixture: tests/fixtures/omega/T109-Brian2-sparse-spike-reference/invalid.json
- Focused checks: tests/test_T109_edge.py and test_T109 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T109_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

