# Post-T210 remaining limitations

- Remote mode uses one bearer token, not accounts, roles, rotation, or audit
  identity. Use TLS termination and a secret manager for any non-loopback use.
- The built-in rate limit is process-local and resets on restart; it is not a
  distributed quota.
- SQLite remains a single-worker local store. Network filesystems, multiple API
  workers, and distributed queues are unsupported.
- RSS measurement is platform-specific: Windows uses `GetProcessMemoryInfo`,
  Unix uses `resource`, and unavailable platforms report `null` rather than a
  fabricated measurement.
- Docker image startup was not locally verified because the Docker daemon was
  unavailable. Compose syntax and CI configuration were verified.
- The full repository still contains legacy Ruff findings in untouched modules;
  the new CI gate is deliberately limited to the remediation production surface
  so it does not hide those findings or claim they were fixed.
- Scientific claims remain bounded to the equations and parameter ranges in
  `docs/SCIENCE.md`; performance numbers are environment-specific.

No remaining limitation is treated as a release-gate pass.
