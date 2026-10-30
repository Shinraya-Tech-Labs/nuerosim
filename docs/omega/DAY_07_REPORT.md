# Omega Day 07 — T101–T150

T101 through T150 are complete on `exhibition-2026-10-28`.

- Interoperability, reference comparison, deterministic execution, sweep, archive, profiling, and UI projection helpers are implemented in `python/neurosim/`.
- Every task has a contract, positive and negative JSON fixtures, a focused edge test, catalog coverage, and reproducible evidence.
- Focused verification: `PYTHONPATH=python python -m pytest tests/test_T101_to_T150_catalog.py tests/test_T101_edge.py ... tests/test_T150_edge.py -q` — 101 passed; full regression `PYTHONPATH=python python -m pytest tests -q` — 426 passed.
- The next incomplete task is T151.
