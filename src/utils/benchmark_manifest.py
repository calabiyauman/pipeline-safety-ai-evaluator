"""
Benchmark manifest utilities for dataset integrity checks.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import datetime
from pathlib import Path
from typing import Any, Dict, List


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_manifest(manifest_path: str | None = None) -> Dict[str, Any]:
    path = Path(manifest_path) if manifest_path else (_project_root() / "data" / "benchmark_manifest.json")
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest_core_payload(manifest: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "manifest_version": manifest.get("manifest_version"),
        "dataset_version": manifest.get("dataset_version"),
        "hash_algorithm": manifest.get("hash_algorithm"),
        "files": manifest.get("files", {}),
    }


def _canonical_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def compute_manifest_signature(manifest: Dict[str, Any], signing_key: str) -> str:
    payload = _canonical_json(_manifest_core_payload(manifest)).encode("utf-8")
    return hmac.new(signing_key.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def sign_manifest(
    manifest_path: str | None = None,
    signing_key: str | None = None,
    key_id: str = "local",
) -> Dict[str, Any]:
    key = signing_key or os.getenv("PSAE_MANIFEST_SIGNING_KEY")
    if not key:
        raise ValueError("Signing key required. Provide signing_key or set PSAE_MANIFEST_SIGNING_KEY.")

    path = Path(manifest_path) if manifest_path else (_project_root() / "data" / "benchmark_manifest.json")
    manifest = load_manifest(str(path))
    signature_value = compute_manifest_signature(manifest, key)
    manifest["signature"] = {
        "algorithm": "hmac-sha256",
        "key_id": key_id,
        "value": signature_value,
        "signed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    return manifest


def verify_manifest_signature(
    manifest_path: str | None = None,
    signing_key: str | None = None,
) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    signature = manifest.get("signature", {})
    signature_value = signature.get("value")
    key = signing_key or os.getenv("PSAE_MANIFEST_SIGNING_KEY")

    if not signature_value:
        return {"status": "unsigned", "valid": False, "reason": "Manifest has no signature value."}
    if not key:
        return {"status": "missing_key", "valid": False, "reason": "Signing key not provided for verification."}

    expected = compute_manifest_signature(manifest, key)
    valid = hmac.compare_digest(signature_value, expected)
    return {
        "status": "valid" if valid else "invalid",
        "valid": valid,
        "key_id": signature.get("key_id"),
        "algorithm": signature.get("algorithm"),
    }


def validate_manifest(manifest_path: str | None = None) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    root = _project_root()
    entries = manifest.get("files", {})

    results: List[Dict[str, Any]] = []
    all_ok = True
    for relative_path, expected_sha in entries.items():
        file_path = root / relative_path
        if not file_path.exists():
            all_ok = False
            results.append(
                {
                    "path": relative_path,
                    "status": "missing",
                    "expected_sha256": expected_sha,
                    "actual_sha256": None,
                }
            )
            continue

        actual_sha = file_sha256(file_path)
        ok = actual_sha == expected_sha
        if not ok:
            all_ok = False
        results.append(
            {
                "path": relative_path,
                "status": "ok" if ok else "mismatch",
                "expected_sha256": expected_sha,
                "actual_sha256": actual_sha,
            }
        )

    return {
        "manifest_version": manifest.get("manifest_version", "unknown"),
        "dataset_version": manifest.get("dataset_version", "unknown"),
        "all_ok": all_ok,
        "results": results,
        "signature": verify_manifest_signature(manifest_path),
    }
