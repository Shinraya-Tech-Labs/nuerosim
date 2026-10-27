# Archived, unsupported prototypes

These deployment/build recipes and documents refer to absent source trees and
unvalidated capabilities. They are retained as historical material, not runnable
deployment instructions. The standalone dashboard contains a duplicated engine.
Use the root README and `neurosim.workbench` instead. No scientific source was
deleted. `python/neurosim/legacy_cli.py`, models, simulation, analysis and pipeline
remain available for future remediation but are outside the validated workbench.

The original test files remain at the repository root. Run them explicitly with
`python -m pytest test_neuron_models.py test_integration.py` to audit that legacy
path. They are not silently counted as passing or replaced with mocks. Their
known failures block a release claiming backward compatibility.
