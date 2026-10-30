# T141 — population-firing-rate-chart

Reproducible evidence for the T141 contract and implementation.

- Positive fixture: tests/fixtures/omega/T141-population-firing-rate-chart/valid.json
- Negative fixture: tests/fixtures/omega/T141-population-firing-rate-chart/invalid.json
- Focused checks: tests/test_T141_edge.py and test_T141 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T141_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

