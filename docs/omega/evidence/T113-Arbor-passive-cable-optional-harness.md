# T113 — Arbor-passive-cable-optional-harness

Reproducible evidence for the T113 contract and implementation.

- Positive fixture: tests/fixtures/omega/T113-Arbor-passive-cable-optional-harness/valid.json
- Negative fixture: tests/fixtures/omega/T113-Arbor-passive-cable-optional-harness/invalid.json
- Focused checks: tests/test_T113_edge.py and test_T113 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T113_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

