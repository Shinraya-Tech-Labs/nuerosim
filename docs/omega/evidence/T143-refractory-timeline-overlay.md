# T143 — refractory-timeline-overlay

Reproducible evidence for the T143 contract and implementation.

- Positive fixture: tests/fixtures/omega/T143-refractory-timeline-overlay/valid.json
- Negative fixture: tests/fixtures/omega/T143-refractory-timeline-overlay/invalid.json
- Focused checks: tests/test_T143_edge.py and test_T143 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T143_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

