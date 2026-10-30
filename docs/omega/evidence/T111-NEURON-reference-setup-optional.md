# T111 — NEURON-reference-setup-optional

Reproducible evidence for the T111 contract and implementation.

- Positive fixture: tests/fixtures/omega/T111-NEURON-reference-setup-optional/valid.json
- Negative fixture: tests/fixtures/omega/T111-NEURON-reference-setup-optional/invalid.json
- Focused checks: tests/test_T111_edge.py and test_T111 in tests/test_T101_to_T150_catalog.py
- Verification command: PYTHONPATH=python python -m pytest tests/test_T111_edge.py tests/test_T101_to_T150_catalog.py -q
- Expected result: all selected checks pass.

