"""Run a command and capture bounded test-baseline metadata."""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


def _tail(value, limit=4096):
    if limit == 0:
        return ""
    data = value if isinstance(value, bytes) else (value or "").encode()
    return data[-limit:].decode("utf-8", errors="replace")


def capture_baseline(command, cwd=None, timeout=900, output_limit=4096):
    if not isinstance(command, (list, tuple)) or not command:
        raise ValueError("command must not be empty")
    if any(not isinstance(arg, str) for arg in command):
        raise ValueError("command arguments must be strings")
    if not isinstance(timeout, (int, float)) or not 1 <= timeout <= 86400:
        raise ValueError("timeout must be between 1 and 86400 seconds")
    if not isinstance(output_limit, int) or output_limit < 0:
        raise ValueError("output limit must be a non-negative integer")
    directory = Path(cwd or os.getcwd()).resolve()
    if not directory.is_dir():
        raise ValueError(f"working directory does not exist: {directory}")
    revision = None
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    started = time.perf_counter()
    timed_out = False
    try:
        result = subprocess.run(
            list(command),
            cwd=directory,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        exit_code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code, stdout, stderr = 124, exc.stdout or b"", exc.stderr or b""
    except OSError as exc:
        raise ValueError(f"cannot start command: {exc}") from exc
    return {
        "command": list(command),
        "working_directory": str(directory),
        "git_revision": revision,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "timed_out": timed_out,
        "exit_code": exit_code,
        "stdout_tail": _tail(stdout, output_limit),
        "stderr_tail": _tail(stderr, output_limit),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", help="working directory (default: current directory)")
    parser.add_argument("--timeout", type=float, default=900, help="timeout in seconds")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="command after --")
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        report = capture_baseline(command, cwd=args.cwd, timeout=args.timeout)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
