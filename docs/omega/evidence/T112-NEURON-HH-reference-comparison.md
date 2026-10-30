# T112 — NEURON-HH-reference-comparison

Reproducible evidence for the T112 contract and implementation.

- Positive fixture: tests/fixtures/omega/T112-NEURON-HH-reference-comparison/valid.json
- Negative fixture: tests/fixtures/omega/T112-NEURON-HH-reference-comparison/invalid.json
- Focused checks: tests/test_T112_edge.py and test_T112 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T112_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

