# T003 validation evidence

## Command and environment

Command: `PYTHONPATH=python python -m neurosim.module_boundaries HEAD`  
Environment: Windows 11, Python 3.14.2.  
Revision: `8b90737642077b1834ce50e5084a5384c7a53839`.

Five fresh CLI runs took a median of **251.78 ms** (minimum **228.41 ms**, maximum **273.43 ms**), including process startup and Git reads.

## Cross-check

The command reported **1** legacy-named Python module (`python/neurosim/legacy_cli.py`), **9** archived files under `docs/legacy/`, and **2** registered console entry points, both targeting `neurosim.workbench`. These matched a direct scan of the selected commit tree and its parsed `project.scripts` table. Repeated normalized JSON was identical. The focused tests passed (4 passed).

## Limits

This is a path naming and console-entry-point map, not a runtime import graph. It may miss legacy code outside the documented naming/location rules and cannot determine whether any module is scientifically valid or safe to delete.
