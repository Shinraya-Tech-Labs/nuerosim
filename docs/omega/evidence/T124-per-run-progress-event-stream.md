# T124 — per-run-progress-event-stream

Reproducible evidence for the T124 contract and implementation.

- Positive fixture: tests/fixtures/omega/T124-per-run-progress-event-stream/valid.json
- Negative fixture: tests/fixtures/omega/T124-per-run-progress-event-stream/invalid.json
- Focused checks: tests/test_T124_edge.py and test_T124 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T124_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

