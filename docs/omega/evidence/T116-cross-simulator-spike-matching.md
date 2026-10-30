# T116 — cross-simulator-spike-matching

Reproducible evidence for the T116 contract and implementation.

- Positive fixture: tests/fixtures/omega/T116-cross-simulator-spike-matching/valid.json
- Negative fixture: tests/fixtures/omega/T116-cross-simulator-spike-matching/invalid.json
- Focused checks: tests/test_T116_edge.py and test_T116 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T116_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

