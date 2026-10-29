# T011 — test baseline capture

## Purpose

Run an explicit test command and capture enough environment and result metadata to compare later runs without claiming broader reproducibility.

## Contract

- **Input:** an argument vector after `--`, optional working directory, and timeout from 1 to 86,400 seconds. Commands are launched without a shell.
- **Output:** deterministic JSON fields for command, resolved working directory, current Git revision when available, Python version, OS/platform, elapsed seconds, timed-out flag, process exit code, and bounded stdout/stderr tails.
- **Units:** timeout and elapsed values are seconds; output tail limits are bytes before UTF-8 decoding.
- **Defaults:** current directory; 900 second timeout; at most 4,096 bytes from the end of each output stream.
- **Acceptance examples:** a successful command records exit code 0 and its output tail; a failing command preserves its exit code; a timed-out command is terminated and recorded with exit code 124.
- **Errors:** reject an empty command, invalid timeout, or missing/unreadable working directory with a concise nonzero CLI status.
- **Safety:** no shell evaluation, environment dump, or file writes unless the user redirects stdout.
- **Exclusions:** this captures one process invocation only. It does not prove determinism, correctness, hardware equivalence, dependency reproducibility, or CI results.
