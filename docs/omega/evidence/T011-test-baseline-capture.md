# T011 validation evidence

## Captured test run

At code revision `fd0fe341e4aa4ff09fe47f04e2f7df6d4d502a9e`, the baseline command ran `python -m pytest tests/test_test_baseline.py -q` on Windows 11 with Python 3.14.2. It recorded exit code 0, no timeout, an elapsed process time of 5.565141 seconds, and the bounded output tail `7 passed in 1.77s`.

The baseline capture test file passed (7 passed). It covers successful and failing commands, a one-second timeout, bounded and zero-length output tails, invalid working directories, and CLI JSON output.

## Limits

The command and environment metadata describe this run only. The capture is not proof of repeatability, scientific correctness, or CI behavior. Output is bounded to its final 4,096 bytes and can be changed with a caller-side redirect if a persistent artifact is required.
