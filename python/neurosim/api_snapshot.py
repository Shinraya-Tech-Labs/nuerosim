"""Deterministic JSON snapshot of the workbench OpenAPI contract."""

import hashlib
import json
import sys

from neurosim.workbench.api import app

HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


def build_snapshot(schema: dict) -> dict[str, object]:
    if not isinstance(schema, dict) or not isinstance(schema.get("paths"), dict):
        raise ValueError("OpenAPI paths must be an object")
    operation_count = sum(
        method.lower() in HTTP_METHODS
        for path_item in schema["paths"].values()
        if isinstance(path_item, dict)
        for method in path_item
    )
    canonical = json.dumps(
        schema,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return {
        "schema": schema,
        "operation_count": operation_count,
        "sha256": hashlib.sha256(canonical).hexdigest(),
    }


def main() -> None:
    try:
        result = build_snapshot(app.openapi())
        output = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as error:
        print(f"API snapshot: {error}", file=sys.stderr)
        raise SystemExit(2) from None
    sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
