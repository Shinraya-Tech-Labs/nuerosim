# T104 — interop-documentation-examples

Reproducible evidence for the T104 contract and implementation.

- Positive fixture: tests/fixtures/omega/T104-interop-documentation-examples/valid.json
- Negative fixture: tests/fixtures/omega/T104-interop-documentation-examples/invalid.json
- Focused checks: tests/test_T104_edge.py and test_T104 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T104_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

