# T010 validation evidence

## Declared workflow coverage

At code revision `967d6a8`, the audit parsed both repository workflows and reported 4 jobs and 11 declared matrix combinations: 10 across `cpu.yml` and 1 in `web.yml`. The CPU test matrix expands to 8 combinations across `ubuntu-latest` and `windows-latest`, with Python 3.11–3.14. The CPU dependency and Docker jobs each declare Ubuntu. The web job declares Ubuntu, Python 3.12, and Node 22.23.0.

The focused test file passed (6 passed). The CLI emitted deterministic JSON for the actual workflow files. Environment: Windows 11, Python 3.14.2, PyYAML 6.0.3.

## Limits

These are declared configuration values only. The audit does not inspect GitHub run history, job outcomes, real runner images/architectures, or evaluate matrix `include` and `exclude` transformations.
