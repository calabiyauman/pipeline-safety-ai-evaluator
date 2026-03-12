# Local CI Preflight

## Purpose

Use a local preflight check before every push so CI failures are caught early.

## Command

Run from repository root:

```bash
python scripts/ci_preflight.py
```

## What It Runs

1. `python -m flake8 src tests`
2. `python -m pytest tests -q`

If either step fails, the script exits non-zero and should block deployment/push decisions until fixed.

## Recommended Workflow

1. Make code/data changes.
2. Run local preflight.
3. Fix any failures.
4. Push only when preflight passes.
