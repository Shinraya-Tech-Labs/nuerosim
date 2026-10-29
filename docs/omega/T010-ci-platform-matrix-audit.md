# CI platform matrix audit

Install the development dependencies, then audit the repository workflows:

```sh
python -m pip install '.[dev]'
PYTHONPATH=python python -m neurosim.ci_matrix_audit .github/workflows/cpu.yml .github/workflows/web.yml
```

The JSON output lists declared jobs, runner labels, matrix platforms, runtime versions, and expanded combinations for simple list-valued matrix axes. Scalar `runs-on` and setup-python/setup-node versions are reported when declared. It does not claim that CI ran or passed.

The auditor rejects malformed workflow/job/matrix structures. It does not expand `include`/`exclude`, expressions, reusable workflows, runner image versions, or architecture. See the [contract](contracts/T010-ci-platform-matrix-audit.md) and [validation evidence](evidence/T010-ci-platform-matrix-audit.md).
