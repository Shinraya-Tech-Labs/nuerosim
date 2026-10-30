# T131 — result-manifest-hashing

Reproducible evidence for the T131 contract and implementation.

- Positive fixture: tests/fixtures/omega/T131-result-manifest-hashing/valid.json
- Negative fixture: tests/fixtures/omega/T131-result-manifest-hashing/invalid.json
- Focused checks: tests/test_T131_edge.py and test_T131 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T131_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

