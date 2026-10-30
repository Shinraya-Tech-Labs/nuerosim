# T114 — NEST-event-semantics-comparison

Reproducible evidence for the T114 contract and implementation.

- Positive fixture: tests/fixtures/omega/T114-NEST-event-semantics-comparison/valid.json
- Negative fixture: tests/fixtures/omega/T114-NEST-event-semantics-comparison/invalid.json
- Focused checks: tests/test_T114_edge.py and test_T114 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T114_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

