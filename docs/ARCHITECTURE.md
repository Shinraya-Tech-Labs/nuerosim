# Architecture and operational boundaries

The packaged `neurosim.workbench` module is the supported application:

* `config.py`: strict Pydantic manifest, finite values, unknown-field rejection,
  limits on steps, duration, network and output size.
* `engine.py`: deterministic CPU state integration, conductance events, recording,
  rate analysis and provenance. No dependency on API or storage.
* `store.py`: SQLite transactions and compressed JSON results; exclusive OS file
  lock; one background thread; cooperative cancellation. No pickle loading.
* `api.py`: validated experiment, history, result, manifest, ZIP and SWC routes.
* `index.html`: same-origin browser client, one-second polling, SVG plots.
* `cli.py`: config/manifest execution through the identical engine.

Jobs transition `queued -> running -> completed/failed`, or
`queued -> cancelled` / `running -> cancelling -> cancelled`. Completion and
result storage are atomic. Cancellation wins if requested before completion's
transaction. Retries create new IDs and preserve `parent_id`; originals remain
immutable. On startup, interrupted running jobs are marked failed with an
explicit reason, while queued jobs resume. This is restart-from-manifest, not
checkpoint continuation. A second server on the same database is rejected.

One Uvicorn worker is required. SQLite is local storage, not a distributed queue;
do not put the database on a network filesystem. The worker thread does CPU work
outside request handlers; it is not a sandbox for arbitrary Python, and no such
code can be submitted. Progress writes are throttled to 250 ms. Cancellation is
checked at most every 20 simulation steps and database polling is throttled to
50 ms; serialization and a database transaction can add latency.

## Security and capacity

This is a **single-user localhost application**, without accounts, TLS or remote
authorization. The CLI binds loopback; Compose publishes loopback only. For any
remote access, configure authentication, TLS, request/body/rate limits and quotas
at an administrator-managed reverse proxy first. No CORS wildcard is enabled.
Never expose the legacy Celery/dashboard paths as network services.

SQL is parameterized. Exports use fixed member names; clients cannot select
filesystem paths. SWC text is bounded and validated for finite values, unique
IDs, one root, parent existence and cycles. Names/errors are rendered as text.
The API limits 16 active and 500 retained experiments. Large results are bounded
but JSON serialization can use several times the array size in memory; this is
not suitable for giant networks. Retained-result quotas are by count, not bytes;
monitor disk usage and delete/export old experiments. SQLite deletion does not
necessarily shrink its file; offline VACUUM can reclaim space after backups.

Back up the database while the application is stopped, or use SQLite's backup
API. Do not copy a live database while ignoring its WAL file. Graceful shutdown
cancels current work and leaves queued work for next startup.

## Release gates

No release or deployment has been published. A candidate needs:
clean installed-wheel tests; dependency audit; CPU reference/convergence and
API lifecycle tests; browser workflow verification; Docker build + real-job
smoke; green Windows/Linux CI; provenance and examples; licensing resolution.
The repository originally claimed Apache-2.0 but supplied no LICENSE; ownership
and license text must be confirmed before publishing a release. Version
`0.2.0.dev0` explicitly denotes unreleased development work.

Original scientific modules and root tests are retained as research material.
Passing `tests/` validates the workbench contract, not those original prototypes.
Backward compatibility and their outstanding numerical defects remain outside
this contract and block any release claiming their support.
