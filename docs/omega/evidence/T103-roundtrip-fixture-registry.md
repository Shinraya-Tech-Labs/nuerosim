# T103 — roundtrip-fixture-registry

Reproducible evidence for the T103 contract and implementation.

- Positive fixture: tests/fixtures/omega/T103-roundtrip-fixture-registry/valid.json
- Negative fixture: tests/fixtures/omega/T103-roundtrip-fixture-registry/invalid.json
- Focused checks: tests/test_T103_edge.py and test_T103 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T103_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

