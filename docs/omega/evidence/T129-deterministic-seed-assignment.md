# T129 — deterministic-seed-assignment

Reproducible evidence for the T129 contract and implementation.

- Positive fixture: tests/fixtures/omega/T129-deterministic-seed-assignment/valid.json
- Negative fixture: tests/fixtures/omega/T129-deterministic-seed-assignment/invalid.json
- Focused checks: tests/test_T129_edge.py and test_T129 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T129_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

