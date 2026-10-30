# T133 — CPU-profiling-per-subsystem

Reproducible evidence for the T133 contract and implementation.

- Positive fixture: tests/fixtures/omega/T133-CPU-profiling-per-subsystem/valid.json
- Negative fixture: tests/fixtures/omega/T133-CPU-profiling-per-subsystem/invalid.json
- Focused checks: tests/test_T133_edge.py and test_T133 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T133_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

