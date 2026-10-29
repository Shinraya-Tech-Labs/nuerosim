# API endpoint contract snapshot

Run from the repository root to print the current workbench OpenAPI schema and its canonical digest:

```sh
PYTHONPATH=python python -m neurosim.api_snapshot
```

The JSON contains the OpenAPI document, HTTP operation count, and SHA-256 of the document serialized as sorted, compact UTF-8 JSON. The command calls `app.openapi()` only; it does not start the API lifespan, create a database, start a worker, bind a socket, or call route handlers. Repeating it with the same source and FastAPI/Pydantic versions should produce the same digest.

Schema-generation or serialization errors exit nonzero and write an error to stderr. The digest describes the declared contract only. It does not prove that handlers run, requests succeed, or access is protected. The workbench API is a single-user localhost service and should not be exposed without an authenticated reverse proxy. No biological claim is implied by the endpoint schema.

## Verification checklist

- [x] Check the golden schema hash and operation count.
- [x] Check malformed paths and the empty-path boundary.
- [x] Compare CLI output with `app.openapi()`.
- [x] Repeat the command and compare the schema digest.

See the [contract](contracts/T004-api-endpoint-contract-snapshot.md) and [validation evidence](evidence/T004-api-endpoint-contract-snapshot.md).
