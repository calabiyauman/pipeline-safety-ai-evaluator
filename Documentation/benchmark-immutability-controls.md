# Benchmark Immutability Controls

## Purpose
This document defines how benchmark datasets are protected against silent drift by using a signed manifest workflow.

## Components

- `data/benchmark_manifest.json`
  - Contains SHA-256 checksums for benchmark data files.
  - Contains a signature block for immutability validation.
- `src/utils/benchmark_manifest.py`
  - `validate_manifest()`
  - `sign_manifest()`
  - `verify_manifest_signature()`
- CLI commands in `src/cli.py`
  - `validate-benchmark`
  - `sign-benchmark`
  - `verify-benchmark-signature`

## Signing Workflow

1. Update benchmark data files under `data/test_cases/` or `data/human_baseline/`.
2. Refresh checksum entries in `data/benchmark_manifest.json` (if needed).
3. Sign the manifest:

```bash
psae sign-benchmark --key-id maintainer-2026
```

Notes:
- By default, signing key is read from `PSAE_MANIFEST_SIGNING_KEY`.
- You can pass `--key` explicitly for local signing.

4. Verify signature:

```bash
psae verify-benchmark-signature
```

5. Validate checksums + signature status:

```bash
psae validate-benchmark
```

## CI/Review Expectations

- Benchmark file changes must include an updated manifest.
- Signature verification should pass in reviewer validation using authorized key material.
- Pull requests touching benchmark artifacts must include test output and manifest verification output.

## Security Notes

- Never commit signing secrets.
- Use environment-managed keys in local secure shells/CI secrets.
- Rotate signing keys based on project governance policy and update `key_id` accordingly.
