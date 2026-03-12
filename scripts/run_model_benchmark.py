"""
Run benchmark across configured models and print score table.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Suppress verbose logging during benchmark
logging.getLogger("scenarios").setLevel(logging.WARNING)
logging.getLogger("core").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Ensure src is on path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Load .env before imports
_env = PROJECT_ROOT / ".env"
if _env.exists():
    for line in _env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip("'").strip('"')
            if k and k not in os.environ:
                os.environ[k] = v

from core.evaluator import PipelineSafetyEvaluator
from scenarios.base import load_builtin_suite
from cli import _build_model

ALL_MODELS = [
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "claude-3-5-sonnet",
    "claude-3-opus",
    "gemini-1-5-pro",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PSAE model benchmark")
    parser.add_argument("--model", help="Single model to run (e.g. gpt-4o)")
    parser.add_argument("--full", action="store_true", help="Use full suite instead of 5 scenarios")
    parser.add_argument("--runs", type=int, default=1, help="Runs per scenario")
    parser.add_argument("--llm-judge", action="store_true", help="Use LLM-as-judge for scoring")
    args = parser.parse_args()

    # Load from data/test_cases/*.json (safety_critical, engineering, inspection, regulatory)
    suite = load_builtin_suite("full")
    if args.full:
        scenarios = suite.scenarios
    else:
        scenarios = suite.scenarios[:5]  # Quick run: first 5 only
    runs = args.runs
    models = [args.model] if args.model else ALL_MODELS

    overrides = {}
    if args.llm_judge:
        overrides["use_llm_judge"] = True
    # Align min_runs with requested runs to avoid "below minimum" warning
    overrides["min_runs"] = args.runs
    evaluator = PipelineSafetyEvaluator(
        config_path=str(PROJECT_ROOT / "configs" / "evaluation.yaml"),
        output_dir=str(PROJECT_ROOT / "results"),
        verbose=False,
        config_overrides=overrides,
    )

    scores: dict[str, dict] = {}
    out_path = PROJECT_ROOT / "results" / "model_benchmark_scores.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for model_name in models:
        try:
            model = _build_model(model_name)
        except Exception as e:
            print(f"  {model_name}: SKIP ({e})")
            scores[model_name] = {"overall_score": None, "error": str(e)}
            continue

        try:
            result = evaluator.evaluate(
                model=model,
                test_suite=scenarios,
                runs=runs,
                include_abnormal=False,
                random_order=False,
            )
            summary = result.get("summary", {})
            scores[model_name] = {
                "overall_score": summary.get("overall_score"),
                "pass_rate": summary.get("overall_pass_rate"),
                "dangerous_error_rate": summary.get("overall_dangerous_error_rate"),
                "total_evaluations": summary.get("total_evaluations"),
            }
        except Exception as e:
            scores[model_name] = {"overall_score": None, "error": str(e)}

        # Save incrementally after each model
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                {"scenarios_used": len(scenarios), "runs": runs, "scores": scores},
                f,
                indent=2,
            )

    # Print table
    print("\n" + "=" * 70)
    print("PSAE Model Benchmark Results")
    print("=" * 70)
    print(f"Suite: {len(scenarios)} scenarios, {runs} run(s) each")
    print("-" * 70)
    print(f"{'Model':<25} {'Overall Score':<14} {'Pass Rate':<12} {'Danger %':<10}")
    print("-" * 70)

    for name, s in scores.items():
        if "error" in s:
            print(f"{name:<25} ERROR: {s['error'][:35]}")
        else:
            score = s.get("overall_score")
            pass_r = s.get("pass_rate")
            dang = s.get("dangerous_error_rate")
            score_str = f"{score:.1f}" if score is not None else "N/A"
            pass_str = f"{pass_r:.1f}%" if pass_r is not None else "N/A"
            dang_str = f"{dang:.1f}%" if dang is not None else "N/A"
            print(f"{name:<25} {score_str:<14} {pass_str:<12} {dang_str:<10}")

    print("=" * 70)
    print(f"\nResults saved to: {out_path}")


if __name__ == "__main__":
    main()
