# Test baseline capture

Run a command through the baseline recorder; use `--` to separate recorder options from the command:

```sh
PYTHONPATH=python python -m neurosim.test_baseline --timeout 900 -- python -m pytest tests -q
```

The JSON report includes the command, working directory, Git revision when available, Python and platform versions, elapsed seconds, exit status, timeout status, and up to 4,096 trailing bytes from each output stream. It runs the command without a shell and returns the captured command's exit status, so shell pipelines can continue to treat failures normally.

Errors include an empty command, invalid timeout, missing working directory, or a command that cannot start. A timeout stops the child and records exit code 124. The command does not dump environment variables. Redirect the JSON output if you need a saved baseline artifact.

See the [contract](contracts/T011-test-baseline-capture.md) and [validation evidence](evidence/T011-test-baseline-capture.md).
