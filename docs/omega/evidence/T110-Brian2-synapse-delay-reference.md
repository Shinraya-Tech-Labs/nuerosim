# T110 — Brian2-synapse-delay-reference

Reproducible evidence for the T110 contract and implementation.

- Positive fixture: tests/fixtures/omega/T110-Brian2-synapse-delay-reference/valid.json
- Negative fixture: tests/fixtures/omega/T110-Brian2-synapse-delay-reference/invalid.json
- Focused checks: tests/test_T110_edge.py and test_T110 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T110_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

