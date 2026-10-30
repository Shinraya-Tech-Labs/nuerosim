# T134 — chunked-result-handling

Reproducible evidence for the T134 contract and implementation.

- Positive fixture: tests/fixtures/omega/T134-chunked-result-handling/valid.json
- Negative fixture: tests/fixtures/omega/T134-chunked-result-handling/invalid.json
- Focused checks: tests/test_T134_edge.py and test_T134 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T134_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

