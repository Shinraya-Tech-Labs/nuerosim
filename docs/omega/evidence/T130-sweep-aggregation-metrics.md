# T130 — sweep-aggregation-metrics

Reproducible evidence for the T130 contract and implementation.

- Positive fixture: tests/fixtures/omega/T130-sweep-aggregation-metrics/valid.json
- Negative fixture: tests/fixtures/omega/T130-sweep-aggregation-metrics/invalid.json
- Focused checks: tests/test_T130_edge.py and test_T130 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T130_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

