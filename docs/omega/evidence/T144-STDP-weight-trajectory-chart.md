# T144 — STDP-weight-trajectory-chart

Reproducible evidence for the T144 contract and implementation.

- Positive fixture: tests/fixtures/omega/T144-STDP-weight-trajectory-chart/valid.json
- Negative fixture: tests/fixtures/omega/T144-STDP-weight-trajectory-chart/invalid.json
- Focused checks: tests/test_T144_edge.py and test_T144 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T144_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

