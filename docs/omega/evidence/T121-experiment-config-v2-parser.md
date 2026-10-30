# T121 — experiment-config-v2-parser

Reproducible evidence for the T121 contract and implementation.

- Positive fixture: tests/fixtures/omega/T121-experiment-config-v2-parser/valid.json
- Negative fixture: tests/fixtures/omega/T121-experiment-config-v2-parser/invalid.json
- Focused checks: tests/test_T121_edge.py and test_T121 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T121_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

