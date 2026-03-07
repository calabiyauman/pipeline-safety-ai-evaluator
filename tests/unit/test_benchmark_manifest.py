from pathlib import Path
import sys
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from utils.benchmark_manifest import (  # noqa: E402
    validate_manifest,
    sign_manifest,
    verify_manifest_signature,
)


def test_benchmark_manifest_validation_passes():
    report = validate_manifest()
    assert report["all_ok"] is True
    assert len(report["results"]) >= 5
    assert all(row["status"] == "ok" for row in report["results"])
    assert report["signature"]["status"] in {"unsigned", "missing_key", "valid"}


def test_manifest_sign_and_verify_round_trip(tmp_path):
    manifest_path = tmp_path / "benchmark_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "manifest_version": "1.0.0",
                "dataset_version": "test",
                "hash_algorithm": "sha256",
                "files": {},
                "signature": {
                    "algorithm": "hmac-sha256",
                    "key_id": None,
                    "value": None,
                    "signed_at_utc": None,
                },
            }
        ),
        encoding="utf-8",
    )

    sign_manifest(str(manifest_path), signing_key="test-key", key_id="unit-test")
    verification = verify_manifest_signature(str(manifest_path), signing_key="test-key")
    assert verification["valid"] is True
    assert verification["status"] == "valid"


def test_manifest_verify_invalid_key(tmp_path):
    manifest_path = tmp_path / "benchmark_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "manifest_version": "1.0.0",
                "dataset_version": "test",
                "hash_algorithm": "sha256",
                "files": {},
                "signature": {
                    "algorithm": "hmac-sha256",
                    "key_id": None,
                    "value": None,
                    "signed_at_utc": None,
                },
            }
        ),
        encoding="utf-8",
    )

    sign_manifest(str(manifest_path), signing_key="correct-key", key_id="unit-test")
    verification = verify_manifest_signature(str(manifest_path), signing_key="wrong-key")
    assert verification["valid"] is False
    assert verification["status"] == "invalid"
