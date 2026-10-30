# T106 — Brian2-reference-harness-setup

Reproducible evidence for the T106 contract and implementation.

- Positive fixture: tests/fixtures/omega/T106-Brian2-reference-harness-setup/valid.json
- Negative fixture: tests/fixtures/omega/T106-Brian2-reference-harness-setup/invalid.json
- Focused checks: tests/test_T106_edge.py and test_T106 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T106_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

