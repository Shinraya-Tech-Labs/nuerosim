# Local Compose deployment

NeuroSim is a bounded, single-user workbench. The supported container setup is
Docker Compose on one host with a local named volume for the SQLite database.
The API and web ports bind to host loopback (`127.0.0.1`); they are not exposed
to the LAN by this Compose file.

## Requirements and secret

Install Docker Engine or Docker Desktop with the Compose v2 plugin. Generate a
private bearer token of at least 16 characters and set it in the shell that
runs Compose. Do not put the token in source control or share it in logs.

PowerShell example, generating a fresh 256-bit token for the current shell:

```powershell
$bytes = New-Object byte[] 32
$rng = [Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($bytes)
$rng.Dispose()
$env:NEUROSIM_AUTH_TOKEN = [Convert]::ToBase64String($bytes)
```

POSIX shell example:

```sh
export NEUROSIM_AUTH_TOKEN="$(openssl rand -base64 32)"
```

## Start the API

From the repository root, validate the rendered Compose configuration and start
the API service:

```sh
docker compose config --quiet
docker compose up --build --detach --wait
docker compose ps
```

The API health endpoint is available without a token at
`http://127.0.0.1:8000/health`. Other API routes require
`Authorization: Bearer <token>`. The service stores experiments in the
`experiments` named volume mounted at `/data`.

## Start the browser workbench

Enable the `web` Compose profile to build and run the Next.js workbench with the
API. The web server forwards the bearer token to FastAPI on the server side; the
secret is not embedded in browser code.

```sh
docker compose --profile web up --build --detach --wait
```

Open `http://127.0.0.1:3000`. Compose applies a 1 GiB memory limit to each
service and a two-CPU limit to the API container. These are container resource
ceilings, not throughput guarantees. The authenticated full-stack smoke checks
are recorded in the [release ledger](omega/V020_PROGRESS.md) and exercise job
creation, result retrieval, retry, cancellation, API restart, and persistence.

## Persistence, backup, and shutdown

Stopping the services with `docker compose down` preserves the named
`experiments` volume. Removing the project volume deletes saved experiments;
review the command carefully before using `docker compose down --volumes`.

For a consistent online backup, use SQLite's backup API in the running API
container, then copy the backup out of the container:

```sh
docker compose exec -T neurosim python -c "import sqlite3; source=sqlite3.connect('/data/experiments.db'); backup=sqlite3.connect('/tmp/experiments.db'); source.backup(backup); backup.close(); source.close()"
```

Copy the snapshot to a new, timestamped path. PowerShell:

```powershell
$backupPath = Join-Path $env:USERPROFILE ("neurosim-experiments-{0}.db" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
docker compose cp neurosim:/tmp/experiments.db $backupPath
```

POSIX shell:

```sh
backup_path="$HOME/neurosim-experiments-$(date -u +%Y%m%dT%H%M%SZ).db"
docker compose cp neurosim:/tmp/experiments.db "$backup_path"
```

Store the resulting file securely and verify that it can be opened before
relying on it. To shut down while preserving data, run:

```sh
docker compose down
```

SQLite is a local, single-worker store. Do not run multiple API containers
against the same database or place the database on a network filesystem.

## Security boundary

Compose enables authenticated remote mode inside the container network, but
publishes both services on host loopback. For access through a reverse proxy,
keep the services on a trusted host/network, configure TLS at the proxy, protect
the bearer token as a secret, and apply administrator-managed request-size,
rate, and quota limits. The application does not provide user accounts,
roles, built-in TLS, token rotation, or a distributed rate limiter. Do not
change the port bindings to `0.0.0.0` as a substitute for a secured deployment.

## Supported scope and limits

The container runs the CPU workbench described in the
[scientific model contract](SCIENCE.md). It is bounded to 512 network neurons,
2,000 ms per experiment, ten million neuron-steps, 32,768 realized synapses,
and a passive cable of at most 32 compartments. These are input/resource limits,
not a guarantee that every permitted parameter combination is numerically
stable or biologically validated. The network layout is illustrative, and an
SWC import displays morphology without creating an electrical morphology model.

CUDA and MPI are unsupported and unvalidated. Headless browser renderer
measurements are environment-specific; they do not establish physical-GPU
performance. See the [measured validation record](VALIDATION.md) and
[remaining limitations](omega/POST_T210_REMAINING_LIMITATIONS.md).

The project does not yet have confirmed license terms. The version metadata
remains `0.2.0.dev0`, and this candidate has not passed all release gates. Do
not treat these deployment instructions as publication or redistribution
authorization.
