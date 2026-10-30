# T145 — morphology-compartment-view

Reproducible evidence for the T145 contract and implementation.

- Positive fixture: tests/fixtures/omega/T145-morphology-compartment-view/valid.json
- Negative fixture: tests/fixtures/omega/T145-morphology-compartment-view/invalid.json
- Focused checks: tests/test_T145_edge.py and test_T145 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T145_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

