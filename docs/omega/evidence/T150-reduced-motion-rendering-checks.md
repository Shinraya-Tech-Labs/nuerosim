# T150 — reduced-motion-rendering-checks

Reproducible evidence for the T150 contract and implementation.

- Positive fixture: tests/fixtures/omega/T150-reduced-motion-rendering-checks/valid.json
- Negative fixture: tests/fixtures/omega/T150-reduced-motion-rendering-checks/invalid.json
- Focused checks: tests/test_T150_edge.py and test_T150 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T150_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

