# T140 — spike-raster-large-set-handling

Reproducible evidence for the T140 contract and implementation.

- Positive fixture: tests/fixtures/omega/T140-spike-raster-large-set-handling/valid.json
- Negative fixture: tests/fixtures/omega/T140-spike-raster-large-set-handling/invalid.json
- Focused checks: tests/test_T140_edge.py and test_T140 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T140_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

