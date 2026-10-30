# T101 — dataset-license-provenance

Reproducible evidence for the T101 contract and implementation.

- Positive fixture: tests/fixtures/omega/T101-dataset-license-provenance/valid.json
- Negative fixture: tests/fixtures/omega/T101-dataset-license-provenance/invalid.json
- Focused checks: tests/test_T101_edge.py and test_T101 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T101_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

