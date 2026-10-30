# T119 — independent-seed-policy

Reproducible evidence for the T119 contract and implementation.

- Positive fixture: tests/fixtures/omega/T119-independent-seed-policy/valid.json
- Negative fixture: tests/fixtures/omega/T119-independent-seed-policy/invalid.json
- Focused checks: tests/test_T119_edge.py and test_T119 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T119_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

