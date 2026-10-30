# Post-T210 critical findings remediation

Date: 2026-10-31  
Scope: findings from Ponytail Audit and Ponytail Review after T210.

## Disposition

| Finding | Root cause | Remediation | Regression evidence |
|---|---|---|---|
| Vectorized LIF | One current was applied to every voltage on each loop iteration. | `vectorized_lif` now performs one bounded element-wise update per current, with scalar support and strict shape/type validation. | `test_vectorized_lif_matches_independent_scalar_reference` |
| Release gates | `bool(value)` allowed strings, numbers, and containers to pass. | Gate, challenge, and platform manifests require actual booleans. | `test_release_gates_require_actual_booleans` |
| Resource validation | `int(float)` silently truncated values; RSS accepted negatives. | Strict integer helper rejects booleans/floats/negative values; RSS samples are finite and nonnegative. | `test_resource_integer_validation`, `test_rss_rejects_negative_samples` |
| API security | The server bound locally but Docker exposed a remote-capable process without an enforceable policy. | Localhost remains the default. Remote mode requires a 16+ character bearer token, protects non-health requests, applies a request rate limit, and supports boundary read-only mode. Compose/server/web/smoke paths use the same policy. | `test_remote_api_requires_bearer_and_health_is_public`, `test_remote_api_rejects_missing_token`, `test_read_only_api_rejects_mutations` |
| Performance/RSS | T151 returned synthetic `steps * neurons` only. | T151 runs a bounded real LIF simulation and reports wall time, process RSS where supported, configuration, platform, and work units. | T151 catalog fixture plus full suite |
| Backup/checksum | Backup compared JSON values; checksum hashed reconstructed JSON. | Store uses SQLite backup/restore; T209 hashes artifact bytes from a path or explicit byte string. | `test_backup_restore_round_trip`, `test_corrupt_backup_is_rejected`, `test_checksum_hashes_artifact_bytes` |
| Activity pagination | Every page sorted every spike list from scratch. | Engine materializes ordered activity events once; views paginate the materialized list, with a legacy fallback. | `test_activity_pagination_uses_materialized_order` |
| History N+1 | History selected IDs, then opened a connection for every job. | One query selects the page and one decoder reconstructs manifests. | `test_history_is_batched_and_ordered` |
| CLI malformed input | Nested list items were dereferenced before type validation. | Nested action/item/model/edge validation and controlled CLI error handling prevent tracebacks. | `test_cli_malformed_nested_input_is_controlled` |
| Worker shutdown | `join()` was unbounded and terminal states could be overwritten. | Bounded join, safe interruption marker, and terminal-state guard preserve cancellation/failure truth. | Existing worker cancellation/restart tests plus full suite |
| CI action pinning | Workflows referenced mutable major tags. | Checkout, setup-python, setup-node, and upload-artifact use verified release SHAs with version comments. | Workflow inspection; CI gate |
| README accuracy | Test counts and deployment claims were stale. | README records the current validation run and explicit local/remote security modes. | Documentation cross-check |
| Test duplication | T151–T210 each repeated identical unit/CLI/edge harnesses. | One parametrized `test_omega_catalog.py` preserves 180 contracts while removing 1,947 duplicated lines. | Catalog tests and full suite |
| Ruff gate | No CI gate covered the remediation entry points. | CI now checks the changed production surface (`omega_final`, workbench, and remediation tests). Existing unrelated legacy Ruff debt is documented as a limitation. | Targeted Ruff run: clean |

## Files changed

Production and deployment: `python/neurosim/omega_final.py`, workbench API/store/engine/views,
`Dockerfile.api`, `docker-compose.yml`, `scripts/smoke_http.py`, `web/middleware.ts`,
and pinned workflow actions.

Tests: `tests/test_post_t210_remediation.py`, `tests/test_omega_catalog.py`, and the
T209 fixture. The three repeated T151–T210 test modules per task were consolidated;
the task-specific remediation tests remain separate.

## Remaining risks

The bearer token is intentionally simple and should be placed behind TLS and a
secret manager. There are no accounts or roles. Docker was not runnable on this
Windows host because the Docker daemon was unavailable. Full-repository Ruff still
reports pre-existing legacy-module findings outside the gated production surface.

## Commit reference

The verified remediation commit is `d5166adc69aa5eb71ab18da7b7df50a575987250`.
The follow-up documentation commit records the final report references.
