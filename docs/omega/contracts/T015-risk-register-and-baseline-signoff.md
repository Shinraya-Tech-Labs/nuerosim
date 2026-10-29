# T015 — risk register and baseline signoff

## Purpose

Validate a local verification record that names the tested revision, required checks, and explicitly reviewed residual risks.

## Contract

- **Input:** JSON object with a 40-character Git revision, required check records, and a non-empty risk register.
- **Output:** JSON reporting `baseline_gate_passed`, missing/failed checks, unresolved risks, checked revision, and risk count.
- **Required checks:** Python full test suite, web unit suite, web production build, and browser end-to-end suite. Each must have a unique ID, non-empty command/evidence, and status `passed`.
- **Risk disposition:** each risk requires a unique ID, non-empty title/rationale/evidence, severity (`low`, `medium`, `high`, `critical`), and disposition (`accepted` or `mitigated`). This is technical baseline review, not release approval.
- **Units:** check and risk counts are integers. Revision is a full 40-hex SHA; durations or scientific measurements are not inferred.
- **Acceptance example:** all four checks passed at a valid revision and every listed risk has a documented disposition; the gate passes while residual risks remain visible.
- **Errors:** reject malformed JSON, missing required fields, invalid statuses/severities/dispositions, duplicate IDs, or empty risk register. A valid record with failed checks returns a failed gate rather than an input error.
- **Exclusions:** this does not verify GitHub CI, deployment, hardware coverage, external review, or absence of risk. A passed local gate is not release authorization.
