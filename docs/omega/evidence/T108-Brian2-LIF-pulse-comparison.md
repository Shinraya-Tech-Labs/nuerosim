# T108 — Brian2-LIF-pulse-comparison

Reproducible evidence for the T108 contract and implementation.

- Positive fixture: tests/fixtures/omega/T108-Brian2-LIF-pulse-comparison/valid.json
- Negative fixture: tests/fixtures/omega/T108-Brian2-LIF-pulse-comparison/invalid.json
- Focused checks: tests/test_T108_edge.py and test_T108 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T108_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

