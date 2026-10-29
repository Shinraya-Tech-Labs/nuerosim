# T004 — API endpoint contract snapshot

## Purpose

Emit a deterministic snapshot of the supported FastAPI application's declared OpenAPI contract, using the existing app factory without starting the server or touching its database.

## Contract

- **Input:** the current checkout's `neurosim.workbench.api.create_app()` and its OpenAPI generation. The command does not claim to snapshot an arbitrary historical Git revision.
- **Output:** JSON containing the OpenAPI document, integer HTTP operation count, and lowercase SHA-256 over the document's canonical UTF-8 JSON representation (`sort_keys=True`, compact separators, no ASCII escaping). Human-readable output may indent the outer JSON but must not change the hash input.
- **Units:** operation count is the number of declared HTTP method operations under `paths`; the digest is 32 bytes represented by 64 lowercase hexadecimal characters.
- **Defaults:** use the app factory's declared routes and schemas; sort paths and keys in the emitted document.
- **Side effects:** do not enter FastAPI lifespan, bind a socket, create a database, start a worker, or call any endpoint.
- **Errors:** schema generation or serialization errors fail with a nonzero status and no partial JSON output.
- **Acceptance example:** repeated runs in the same dependency environment produce identical schema, operation count, and digest.
- **Exclusions:** this snapshot does not exercise route handlers, prove runtime availability, validate every request/response behavior, or establish authentication/security. The app remains a single-user localhost API; the schema is influenced by the installed FastAPI/Pydantic versions.
