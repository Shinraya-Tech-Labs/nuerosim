# T002 validation evidence

## Command and environment

Command: `PYTHONPATH=python python -m neurosim.lockfile_inventory HEAD`  
Environment: Windows 11, Python 3.14.2.  
Revision: `51119006ac0f6849b3dd0ce7b73e9379fc9fd44a`.

Five fresh CLI runs took a median of **291.47 ms** (minimum **272.88 ms**, maximum **292.90 ms**). This includes process startup and Git object reads; it is not a dependency-installation benchmark.

## Inventory and independent check

| Tracked lockfile | Bytes | SHA-256 |
| --- | ---: | --- |
| `requirements-runtime.lock` | 367 | `61167385bfc596341889d83bd0d34f1f46c5a9b57e709023cf2c62e483172ebb` |
| `web/package-lock.json` | 106896 | `120fca46a443fc965f6c20a864ad3dd4d8330963cd6e910efbfdac7633382635` |

Both sizes and hashes matched the raw blobs returned by `git show <revision>:<path>`. The focused unit and CLI integration tests pass, including an unresolved-revision case and a zero-byte lockfile boundary.

## Limits

This proves only that the command reports exact metadata for those Git blobs. The Python lock is labeled a runtime snapshot and says Linux Docker validation is pending; the inventory does not establish full environment reproducibility or scientific reproducibility.
