# T107 — Brian2-LIF-no-synapse-benchmark

Reproducible evidence for the T107 contract and implementation.

- Positive fixture: tests/fixtures/omega/T107-Brian2-LIF-no-synapse-benchmark/valid.json
- Negative fixture: tests/fixtures/omega/T107-Brian2-LIF-no-synapse-benchmark/invalid.json
- Focused checks: tests/test_T107_edge.py and test_T107 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T107_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

