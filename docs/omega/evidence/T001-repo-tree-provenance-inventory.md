# T001 validation evidence

## Command and environment

The inventory was exercised with `PYTHONPATH=python python -m neurosim.repo_inventory HEAD` on Windows 11, Python 3.14.2, at revision `067b3771b30b87080874d99ed4c75602ddd1ad79`.

Five fresh CLI runs took a median of **176.85 ms** (minimum **171.79 ms**, maximum **192.31 ms**). This includes Python process startup and is an audit-command timing, not a simulation benchmark.

## Independent count cross-check

| Source | Tracked paths |
| --- | ---: |
| Inventory command | 148 |
| `git ls-tree -r --name-only -z <revision>` | 148 |
| `git ls-files -z` | 148 |

All three counts matched, and the inventory revision matched the requested commit. The positive fixture's deterministic summary passes `tests/test_repo_inventory.py`; an empty inventory produces zero counts and empty summaries. The invalid revision fixture exits with status 2 and states that the revision must resolve to a commit.

## Limits

This checks repository metadata and path counts only. It does not establish file ownership, authorship, license rights, scientific validity, or provenance of ignored/untracked files. The timing is from one Windows host and is not a cross-platform performance claim.
