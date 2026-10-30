# T142 — synapse-direction-arrow

Reproducible evidence for the T142 contract and implementation.

- Positive fixture: tests/fixtures/omega/T142-synapse-direction-arrow/valid.json
- Negative fixture: tests/fixtures/omega/T142-synapse-direction-arrow/invalid.json
- Focused checks: tests/test_T142_edge.py and test_T142 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T142_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

