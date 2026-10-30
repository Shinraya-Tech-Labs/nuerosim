# Post-T210 validation results

Run date: 2026-10-31 (Windows, Python 3.14, Node 22.23.0).

| Check | Result |
|---|---|
| Python regression suite | 628 passed |
| Focused remediation/catalog tests | 202 passed |
| Frontend unit tests | 6 passed |
| Next.js production build and TypeScript | passed |
| Playwright browser tests | 6 passed |
| Targeted Ruff gate | clean for `python/neurosim/omega_final.py`, `python/neurosim/workbench`, and remediation tests |
| Python dependency audit | `pip-audit -r requirements-runtime.lock`: no known vulnerabilities |
| npm dependency audit | `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities |
| Docker Compose syntax | passed (`docker compose config --quiet`) |
| Docker image/startup smoke | not run: Docker daemon unavailable on this host |
| Cross-platform CI-equivalent | workflow matrix remains Ubuntu/Windows Python 3.11–3.14; remote execution is the authoritative check |
| Scientific numerical regression | included in the 628-test Python suite; vectorized LIF now has an independent scalar reference |

The Playwright run launched the real FastAPI worker and Next.js dev server. It
reported expected headless-WebGL fallback warnings, but all six tests passed.

Commands:

```powershell
$env:PYTHONPATH = 'python'
python -m pytest tests -q
python -m ruff check python/neurosim/omega_final.py python/neurosim/workbench tests/test_post_t210_remediation.py
pip-audit -r requirements-runtime.lock
cd web; npm test; npm run build; npm run test:e2e; npm audit --omit=dev --audit-level=high
cd ..; $env:NEUROSIM_AUTH_TOKEN = 'local-neurosim-token-2026'; docker compose config --quiet
```

Commit references are filled after the verified push.
