# T120 — reproducibility-benchmark-report

Reproducible evidence for the T120 contract and implementation.

- Positive fixture: tests/fixtures/omega/T120-reproducibility-benchmark-report/valid.json
- Negative fixture: tests/fixtures/omega/T120-reproducibility-benchmark-report/invalid.json
- Focused checks: tests/test_T120_edge.py and test_T120 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T120_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

