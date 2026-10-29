"""Validate local baseline checks and their explicitly reviewed risk register."""

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_CHECKS = ("python", "web-unit", "web-build", "web-e2e")
SEVERITIES = {"low", "medium", "high", "critical"}
DISPOSITIONS = {"accepted", "mitigated"}


def _records(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty list")
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"each {label[:-1]} must be an object")
        for key in ("id", "command", "status", "evidence") if label == "checks" else (
            "id", "title", "severity", "disposition", "rationale", "evidence"
        ):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f"each {label[:-1]} requires non-empty {key}")
    ids = [item["id"] for item in value]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{label} IDs must be unique")
    return value


def validate_signoff(record):
    if not isinstance(record, dict):
        raise ValueError("signoff must be a JSON object")
    revision = record.get("tested_revision")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        raise ValueError("tested_revision must be a full 40-character Git SHA")
    checks = _records(record.get("checks"), "checks")
    risks = _records(record.get("risks"), "risks")
    for check in checks:
        if check["status"] not in {"passed", "failed"}:
            raise ValueError(f"invalid status for check {check['id']}")
    for risk in risks:
        if risk["severity"] not in SEVERITIES:
            raise ValueError(f"invalid severity for risk {risk['id']}")
        if risk["disposition"] not in DISPOSITIONS:
            raise ValueError(f"invalid disposition for risk {risk['id']}")
    by_id = {check["id"]: check for check in checks}
    missing = sorted(set(REQUIRED_CHECKS) - by_id.keys())
    failed = sorted(
        check_id
        for check_id in REQUIRED_CHECKS
        if check_id in by_id and by_id[check_id]["status"] != "passed"
    )
    accepted_risks = sorted(risk["id"] for risk in risks if risk["disposition"] == "accepted")
    return {
        "tested_revision": revision.lower(),
        "baseline_gate_passed": not missing and not failed,
        "required_check_count": len(REQUIRED_CHECKS),
        "passed_check_count": sum(by_id.get(check_id, {}).get("status") == "passed" for check_id in REQUIRED_CHECKS),
        "missing_checks": missing,
        "failed_checks": failed,
        "risk_count": len(risks),
        "accepted_risks": accepted_risks,
    }


def audit_file(path):
    try:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read signoff record: {exc}") from exc
    return validate_signoff(record)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", help="JSON baseline and risk register")
    args = parser.parse_args(argv)
    try:
        report = audit_file(args.record)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["baseline_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
