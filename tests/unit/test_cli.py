from pathlib import Path
import sys
import argparse
import json

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


import cli  # noqa: E402


def test_load_evaluation_suite_uses_builtin_default():
    args = argparse.Namespace(suite=None, suite_file=None)
    suite = cli._load_evaluation_suite(args)
    assert suite.name
    assert len(suite.scenarios) > 0


def test_load_evaluation_suite_uses_external_file(tmp_path):
    suite_path = tmp_path / "custom_suite.json"
    suite_payload = {
        "name": "Custom Test Suite",
        "scenarios": [
            {
                "test_id": "CU-001",
                "name": "Custom Scenario",
                "category": "safety",
                "risk_level": 8,
                "situation": "Custom situation.",
                "task": "Custom task.",
                "expected_elements": ["work permit"],
                "expected_standards": ["API 1104"],
                "critical_elements": ["work permit"],
                "abnormal_variants": [],
                "validation_notes": "custom"
            }
        ],
    }
    suite_path.write_text(json.dumps(suite_payload), encoding="utf-8")

    args = argparse.Namespace(suite=None, suite_file=str(suite_path))
    suite = cli._load_evaluation_suite(args)

    assert suite.name == "Custom Test Suite"
    assert len(suite.scenarios) == 1
    assert suite.scenarios[0].test_id == "CU-001"


def test_load_evaluation_suite_missing_file_raises():
    args = argparse.Namespace(suite=None, suite_file="does-not-exist.json")
    with pytest.raises(FileNotFoundError):
        cli._load_evaluation_suite(args)


def test_sign_and_verify_benchmark_commands(tmp_path):
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

    sign_args = argparse.Namespace(manifest=str(manifest_path), key="unit-key", key_id="ci-test")
    verify_args = argparse.Namespace(manifest=str(manifest_path), key="unit-key")
    cli.cmd_sign_benchmark(sign_args)
    cli.cmd_verify_benchmark_signature(verify_args)


def test_verify_benchmark_signature_fails_with_wrong_key(tmp_path):
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

    cli.cmd_sign_benchmark(argparse.Namespace(manifest=str(manifest_path), key="correct-key", key_id="ci-test"))
    with pytest.raises(SystemExit):
        cli.cmd_verify_benchmark_signature(
            argparse.Namespace(manifest=str(manifest_path), key="wrong-key")
        )
