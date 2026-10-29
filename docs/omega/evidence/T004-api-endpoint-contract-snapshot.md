# T004 validation evidence

## Command and environment

Command: `PYTHONPATH=python python -m neurosim.api_snapshot`  
Environment: Windows 11, Python 3.14.2.  
Code revision: `6cb325293ac32bffe2a3e1e7066803ef0ae1f54c`.

Five fresh runs produced byte-equivalent JSON and the same canonical schema digest: `61bc9d8a08098cedcfb873de2b68161a593cb4c5122710e223674f632fd19989`. The document contains **18 HTTP operations** across **16 paths**. Median process time was **886.49 ms** (minimum **878.46 ms**, maximum **905.12 ms**).

The focused test compares the CLI output directly with `app.openapi()` and passes (4 tests). It does not enter FastAPI lifespan, start a worker, open a socket, or call a route handler.

## Limits

The digest identifies the emitted schema under the installed FastAPI/Pydantic versions. It does not establish handler behavior, service availability, authentication, authorization, or API security.
