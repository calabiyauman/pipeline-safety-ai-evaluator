"""
Command line interface for PSAE.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

try:
    from . import __version__
    from .core.evaluator import PipelineSafetyEvaluator
    from .models import OpenAIWrapper, AnthropicWrapper, GeminiWrapper
    from .scenarios.base import load_builtin_suite, TestSuite
    from .utils.reporting import ReportGenerator
    from .utils.benchmark_manifest import validate_manifest, sign_manifest, verify_manifest_signature
except ImportError:
    __version__ = "1.0.0"
    from core.evaluator import PipelineSafetyEvaluator
    from models import OpenAIWrapper, AnthropicWrapper, GeminiWrapper
    from scenarios.base import load_builtin_suite, TestSuite
    from utils.reporting import ReportGenerator
    from utils.benchmark_manifest import validate_manifest, sign_manifest, verify_manifest_signature


MODEL_CHOICES = [
    "gpt-4",
    "gpt-4-turbo",
    "claude-3-5-sonnet",
    "claude-3-opus",
    "gemini-1-5-pro",
]


def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("YAML config must be an object at top level.")
    return data


def _build_model(name: str):
    if name in ("gpt-4", "gpt-4-turbo"):
        model_id = "gpt-4" if name == "gpt-4" else "gpt-4-turbo-preview"
        return OpenAIWrapper(api_key=os.getenv("OPENAI_API_KEY"), model=model_id)
    if name in ("claude-3-5-sonnet", "claude-3-opus"):
        model_id = (
            "claude-3-5-sonnet-20241022"
            if name == "claude-3-5-sonnet"
            else "claude-3-opus-20240229"
        )
        return AnthropicWrapper(api_key=os.getenv("ANTHROPIC_API_KEY"), model=model_id)
    if name == "gemini-1-5-pro":
        return GeminiWrapper(api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-1.5-pro")
    raise ValueError(f"Unsupported model: {name}")


def _load_evaluation_suite(args: argparse.Namespace) -> TestSuite:
    suite_file = getattr(args, "suite_file", None)
    if suite_file:
        path = Path(suite_file)
        if not path.exists():
            raise FileNotFoundError(f"Suite file not found: {path}")
        return TestSuite.load_from_json(str(path))

    suite_name = getattr(args, "suite", None) or "full"
    return load_builtin_suite(suite_name)


def cmd_evaluate(args: argparse.Namespace) -> None:
    evaluator = PipelineSafetyEvaluator(config_path=args.config, output_dir=args.output)
    model = _build_model(args.model)
    suite = _load_evaluation_suite(args)

    results = evaluator.evaluate(
        model=model,
        test_suite=suite,
        runs=args.runs,
        include_abnormal=not args.no_abnormal,
    )

    reporter = ReportGenerator(args.output)
    json_path = reporter.generate_json_report(results)
    print(f"JSON report written: {json_path}")

    if not args.no_html:
        html_path = reporter.generate_html_report(results)
        print(f"HTML report written: {html_path}")


def cmd_compare(args: argparse.Namespace) -> None:
    model_names = [m.strip() for m in args.models.split(",") if m.strip()]
    if not model_names:
        raise ValueError("No models provided for compare command.")

    suite = load_builtin_suite("full")
    reporter = ReportGenerator(args.output)
    comparison: Dict[str, Any] = {"models": {}, "summary": {}}

    for model_name in model_names:
        evaluator = PipelineSafetyEvaluator(config_path=args.config, output_dir=args.output)
        model = _build_model(model_name)
        result = evaluator.evaluate(model=model, test_suite=suite, runs=args.runs)
        comparison["models"][model_name] = result.get("summary", {})

    comparison["summary"]["model_count"] = len(comparison["models"])
    path = Path(args.output)
    path.mkdir(parents=True, exist_ok=True)
    out = path / "comparison_summary.json"
    out.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    print(f"Comparison summary written: {out}")

    reporter.generate_markdown_report({"model_name": "comparison", "summary": comparison["summary"]})


def cmd_validate_config(args: argparse.Namespace) -> None:
    data = _load_yaml(args.config)

    errors: List[str] = []
    eval_block = data.get("evaluation", data)
    if not isinstance(eval_block, dict):
        errors.append("Missing or invalid evaluation config object.")
    else:
        if "confidence_level" not in eval_block:
            errors.append("Missing evaluation.confidence_level")
        if "min_runs" not in eval_block:
            errors.append("Missing evaluation.min_runs")

    metrics_weights = data.get("metrics", {}).get("weights", data.get("metrics_weights", {}))
    if not isinstance(metrics_weights, dict) or not metrics_weights:
        errors.append("Missing metrics weights configuration.")
    else:
        total_weight = sum(float(v) for v in metrics_weights.values())
        if abs(total_weight - 1.0) > 1e-6:
            errors.append(f"Metric weights must sum to 1.0, got {total_weight:.4f}")

    if errors:
        print("Config validation failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("Config validation passed.")


def cmd_list_tests(args: argparse.Namespace) -> None:
    suite = load_builtin_suite("full")
    scenarios = list(suite.scenarios)

    if args.category:
        scenarios = [s for s in scenarios if s.category == args.category]
    if args.risk_level is not None:
        scenarios = [s for s in scenarios if s.risk_level >= args.risk_level]

    for scenario in scenarios:
        print(f"{scenario.test_id} | {scenario.category:<12} | risk={scenario.risk_level} | {scenario.name}")

    print(f"\nTotal: {len(scenarios)}")


def cmd_validate_benchmark(args: argparse.Namespace) -> None:
    report = validate_manifest(args.manifest)
    print(
        f"Benchmark manifest version: {report['manifest_version']} "
        f"(dataset {report['dataset_version']})"
    )
    for row in report["results"]:
        print(f"- {row['status']}: {row['path']}")
    print(f"Signature status: {report['signature']['status']}")
    if not report["all_ok"]:
        sys.exit(1)
    print("Benchmark integrity validation passed.")


def cmd_sign_benchmark(args: argparse.Namespace) -> None:
    signed_manifest = sign_manifest(args.manifest, signing_key=args.key, key_id=args.key_id)
    signature = signed_manifest.get("signature", {})
    print("Benchmark manifest signed.")
    print(f"- key_id: {signature.get('key_id')}")
    print(f"- algorithm: {signature.get('algorithm')}")
    print(f"- signed_at_utc: {signature.get('signed_at_utc')}")


def cmd_verify_benchmark_signature(args: argparse.Namespace) -> None:
    verification = verify_manifest_signature(args.manifest, signing_key=args.key)
    print(f"Signature status: {verification['status']}")
    if not verification["valid"]:
        sys.exit(1)
    print("Benchmark signature verification passed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pipeline Safety AI Evaluator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    eval_parser = subparsers.add_parser("evaluate", help="Run evaluation")
    eval_parser.add_argument("--model", required=True, choices=MODEL_CHOICES, help="Model to evaluate")
    suite_group = eval_parser.add_mutually_exclusive_group()
    suite_group.add_argument(
        "--suite",
        choices=["safety", "engineering", "inspection", "regulatory", "benchmark-sources", "full"],
        help="Built-in test suite to run (default: full)",
    )
    suite_group.add_argument(
        "--suite-file",
        help="Path to external JSON suite file matching TestSuite schema",
    )
    eval_parser.add_argument("--runs", type=int, default=5, help="Number of runs per test")
    eval_parser.add_argument("--config", help="Configuration file path")
    eval_parser.add_argument("--output", default="./results", help="Output directory")
    eval_parser.add_argument("--no-abnormal", action="store_true", help="Skip abnormal condition tests")
    eval_parser.add_argument("--no-html", action="store_true", help="Skip HTML report generation")

    compare_parser = subparsers.add_parser("compare", help="Compare models")
    compare_parser.add_argument("--models", required=True, help="Comma-separated model names")
    compare_parser.add_argument("--runs", type=int, default=3, help="Number of runs per test")
    compare_parser.add_argument("--config", help="Configuration file path")
    compare_parser.add_argument("--output", default="./results", help="Output directory")

    validate_parser = subparsers.add_parser("validate-config", help="Validate configuration")
    validate_parser.add_argument("config", help="Config file to validate")

    list_parser = subparsers.add_parser("list-tests", help="List test cases")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--risk-level", type=int, help="Filter by minimum risk level")

    benchmark_parser = subparsers.add_parser("validate-benchmark", help="Validate benchmark dataset checksums")
    benchmark_parser.add_argument("--manifest", help="Optional benchmark manifest path")

    sign_parser = subparsers.add_parser("sign-benchmark", help="Sign benchmark manifest using HMAC")
    sign_parser.add_argument("--manifest", help="Optional benchmark manifest path")
    sign_parser.add_argument("--key", help="Signing key (otherwise use PSAE_MANIFEST_SIGNING_KEY)")
    sign_parser.add_argument("--key-id", default="local", help="Identifier recorded in signature metadata")

    verify_sig_parser = subparsers.add_parser(
        "verify-benchmark-signature",
        help="Verify benchmark manifest signature",
    )
    verify_sig_parser.add_argument("--manifest", help="Optional benchmark manifest path")
    verify_sig_parser.add_argument("--key", help="Verification key (otherwise use PSAE_MANIFEST_SIGNING_KEY)")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "evaluate":
        cmd_evaluate(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "validate-config":
        cmd_validate_config(args)
    elif args.command == "list-tests":
        cmd_list_tests(args)
    elif args.command == "validate-benchmark":
        cmd_validate_benchmark(args)
    elif args.command == "sign-benchmark":
        cmd_sign_benchmark(args)
    elif args.command == "verify-benchmark-signature":
        cmd_verify_benchmark_signature(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
