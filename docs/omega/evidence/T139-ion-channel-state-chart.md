# T139 — ion-channel-state-chart

Reproducible evidence for the T139 contract and implementation.

- Positive fixture: tests/fixtures/omega/T139-ion-channel-state-chart/valid.json
- Negative fixture: tests/fixtures/omega/T139-ion-channel-state-chart/invalid.json
- Focused checks: tests/test_T139_edge.py and test_T139 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T139_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

