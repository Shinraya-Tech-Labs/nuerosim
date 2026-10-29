# T010 — CI platform matrix audit

## Purpose

Report the declared operating-system and runtime-version coverage in GitHub Actions workflow files. This reads workflow configuration; it does not claim that jobs actually ran or passed.

## Contract

- **Input:** one or more GitHub Actions workflow YAML files with a `jobs` mapping; supported job declarations include scalar or matrix `runs-on`, and matrix axes such as `os`, `python`, and `node`.
- **Output:** deterministic JSON listing sorted workflow/job records, declared platforms and runtime axis values, and total expanded matrix combinations where axes can be expanded.
- **Units:** matrix combinations and job counts are non-negative integers. Runtime values and runner labels are strings; versions are not parsed as numeric values.
- **Defaults:** no inferred platform or runtime coverage. Missing declarations are reported as empty/unknown.
- **Acceptance examples:** the CPU workflow reports Ubuntu and Windows over Python 3.11–3.14 (8 combinations); the web workflow reports Ubuntu and Python 3.12 / Node 22.23.0 (one declared job combination).
- **Errors:** reject unreadable, invalid YAML, or malformed workflow/job structures with a nonzero exit and concise error.
- **Dependencies:** YAML parsing uses PyYAML, included in the repository's development extra (`.[dev]`).
- **Exclusions:** do not infer actual runner image versions, architecture, browser or GPU availability, job success, trigger coverage, secrets, reusable workflow expansion, or all GitHub Actions expression semantics. Matrix `include`/`exclude` transformations are not expanded.
