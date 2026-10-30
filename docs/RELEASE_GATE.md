# NeuroSim v0.2.0 candidate release gate

Review date: 2026-10-31

Branch: `codex/neurosim-v020-release`

Candidate revision reviewed: `8687dc53a97bdc58b1d85f92cf8447e47f2dc82e`

## Verification results

| Gate | Result | Evidence |
|---|---|---|
| Python regression | PASS — 649 tests passed from the checkout and 649 passed with the built wheel installed in a clean virtual environment. | `docs/omega/V020_PROGRESS.md`, CP14 record |
| Packaging and dependencies | PASS — wheel built; fresh installed-wheel environment reported no broken requirements. | CP14 record |
| Python dependency security | PASS — `pip-audit -r requirements-runtime.lock` found no known vulnerabilities; hosted dependency job passed. | [CPU workflow](https://github.com/sreerevanth/nuerosim/actions/runs/41123539549) |
| Web dependency security | PASS — `npm audit --audit-level=high` found 0 vulnerabilities; hosted audit passed. | [Web workflow](https://github.com/sreerevanth/nuerosim/actions/runs/41123539587) |
| Cross-platform CI | PASS — Python 3.11–3.14 on Windows and Ubuntu; science/reference validation passed on Ubuntu/Python 3.12. | [CPU workflow](https://github.com/sreerevanth/nuerosim/actions/runs/41123539549) |
| Browser integration | PASS — frontend unit tests, e2e TypeScript, production build, and six Chromium end-to-end tests passed. | [Web workflow](https://github.com/sreerevanth/nuerosim/actions/runs/41123539587) |
| Docker stack | PASS — hosted Compose build, health checks, authenticated API and web proxy, simulation result, retry, cancellation, restart, and persistence smoke passed. The local Docker daemon was unavailable, so local image startup was not observed. | [CPU/Docker workflow](https://github.com/sreerevanth/nuerosim/actions/runs/41123539549) |
| Version and publication state | Development metadata remains `0.2.0.dev0`; no `v0.2.0` tag or GitHub release exists. | `pyproject.toml`, local tag inspection, GitHub Releases API |

## Publication blocker

The repository contains no `LICENSE*` or `COPYING*` file and `pyproject.toml`
does not declare license metadata. The project README and architecture record
state that ownership and license terms are unconfirmed. A public release must
not be tagged or published until the owner resolves and records those terms.

**Decision: CP15 is prohibited for this candidate.** Keep the development
version and branch available for review; do not create an annotated v0.2.0 tag
or GitHub release. This is a licensing release gate, not a failed software
test. Docker and scientific validation are green in hosted CI.

The local shared Python environment also contains unrelated dependency
conflicts (`fastmcp`/`python-dotenv` and `yfinance`/`curl-cffi`). A clean
project virtual environment passed `pip check` and the installed-wheel test
suite. The test run emitted one upstream Starlette/httpx deprecation warning;
no project test failed.

See [validation records](VALIDATION.md), the
[deployment guide](DEPLOYMENT.md), and the
[persistent checkpoint ledger](omega/V020_PROGRESS.md) for full commands,
scopes, and evidence.
