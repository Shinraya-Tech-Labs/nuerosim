# T148 — plot-SVG-export-metadata

Reproducible evidence for the T148 contract and implementation.

- Positive fixture: tests/fixtures/omega/T148-plot-SVG-export-metadata/valid.json
- Negative fixture: tests/fixtures/omega/T148-plot-SVG-export-metadata/invalid.json
- Focused checks: tests/test_T148_edge.py and test_T148 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T148_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

