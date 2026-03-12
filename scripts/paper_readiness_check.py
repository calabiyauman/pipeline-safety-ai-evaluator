"""
Paper readiness gate for PipelineAIEvalPaper2026 criteria.

Runs lightweight checks to determine whether the repository setup is aligned
with paper-grade requirements before generating final result tables.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


REQUIRED_STATS = {"anova", "tukey_hsd", "cohens_d", "icc"}
CATEGORY_TARGETS = {"safety": 8, "engineering": 8, "inspection": 4, "regulatory": 4}


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"_error": f"Invalid JSON: {exc}"}


def _scenario_count(payload: Dict[str, Any]) -> int:
    items = payload.get("test_cases") or payload.get("scenarios") or []
    if isinstance(items, list):
        return len(items)
    return 0


def run_checks(project_root: Path) -> Dict[str, Any]:
    src_dir = project_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    from scenarios.base import load_builtin_suite  # noqa: E402

    config = _load_yaml(project_root / "configs" / "evaluation.yaml")
    evaluation = config.get("evaluation", {}) if isinstance(config, dict) else {}
    tests = set(config.get("statistical_tests", []) or [])

    min_runs = int(evaluation.get("min_runs", 0) or 0)
    min_runs_ok = min_runs >= 5
    stats_ok = REQUIRED_STATS.issubset(tests)

    paper_suite = load_builtin_suite("paper")
    counts: Dict[str, int] = {}
    for scenario in paper_suite.scenarios:
        counts[scenario.category] = counts.get(scenario.category, 0) + 1
    dataset_total = len(paper_suite.scenarios)
    dataset_results: List[Dict[str, Any]] = []
    for category, target in CATEGORY_TARGETS.items():
        actual = counts.get(category, 0)
        dataset_results.append(
            {
                "file": f"{category} (paper suite)",
                "target": target,
                "actual": actual,
                "ok": actual >= target,
                "error": None,
            }
        )

    corpus_ok = all(item["ok"] for item in dataset_results) and dataset_total >= 24

    manifest = _load_json(project_root / "data" / "benchmark_manifest.json")
    signature = manifest.get("signature", {}) if isinstance(manifest, dict) else {}
    signature_present = bool(signature.get("algorithm") and signature.get("hmac_sha256"))

    return {
        "paper_recommendations_ready": bool(min_runs_ok and stats_ok and corpus_ok),
        "checks": {
            "min_runs_at_least_5": {"ok": min_runs_ok, "actual": min_runs},
            "required_statistical_tests_configured": {
                "ok": stats_ok,
                "required": sorted(REQUIRED_STATS),
                "actual": sorted(tests),
            },
            "paper_core_corpus_targets": {
                "ok": corpus_ok,
                "target_total": 24,
                "actual_total": dataset_total,
                "categories": dataset_results,
            },
            "benchmark_signature_present": {"ok": signature_present},
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check paper readiness criteria.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when not ready.")
    args = parser.parse_args()

    report = run_checks(Path(args.project_root).resolve())

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        ready = "PASS" if report["paper_recommendations_ready"] else "NOT READY"
        print(f"# Paper Readiness: {ready}")
        checks = report["checks"]
        print(f"- min_runs >= 5: {'PASS' if checks['min_runs_at_least_5']['ok'] else 'FAIL'} (actual={checks['min_runs_at_least_5']['actual']})")
        print(
            "- required stats configured (ANOVA, Tukey HSD, Cohen's d, ICC): "
            f"{'PASS' if checks['required_statistical_tests_configured']['ok'] else 'FAIL'}"
        )
        corpus = checks["paper_core_corpus_targets"]
        print(
            f"- core corpus target (24 total; 8/8/4/4): {'PASS' if corpus['ok'] else 'FAIL'} "
            f"(actual_total={corpus['actual_total']})"
        )
        for category in corpus["categories"]:
            detail = f"{category['actual']}/{category['target']}"
            if category.get("error"):
                detail = f"{detail}; error={category['error']}"
            print(f"  - {category['file']}: {detail}")
        print(f"- benchmark signature present: {'PASS' if checks['benchmark_signature_present']['ok'] else 'FAIL'}")

    if args.strict and not report["paper_recommendations_ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
