"""Model comparison analysis example."""

from psae.core import StatisticalAnalyzer
from psae.models import HumanExpertBaseline
from psae.scenarios import load_builtin_suite
from psae import PipelineSafetyEvaluator


def evaluate_model(model_name: str, baseline_path: str) -> dict:
    evaluator = PipelineSafetyEvaluator(config_path="configs/evaluation.yaml", verbose=False)
    model = HumanExpertBaseline(baseline_path)
    suite = load_builtin_suite("engineering")
    result = evaluator.evaluate(
        model=model,
        test_suite=suite,
        runs=2,
        include_abnormal=False,
        random_order=False,
    )
    return {"name": model_name, "result": result}


def main() -> None:
    baseline_path = "data/human_baseline/responses.json"

    # Demo setup uses the same deterministic baseline for two labels.
    # Replace with real model wrappers in production runs.
    model_runs = [
        evaluate_model("Human-Baseline-A", baseline_path),
        evaluate_model("Human-Baseline-B", baseline_path),
    ]

    model_scores = {
        run["name"]: [row["adjusted_score"] for row in run["result"]["raw_results"]]
        for run in model_runs
    }

    analyzer = StatisticalAnalyzer(confidence_level=0.95)
    comparison = analyzer.compare_models(model_scores)

    print("Best Performer:", comparison["best_performer"])
    print("ANOVA p-value:", comparison["anova"].get("p_value"))
    print("Ranking:")
    for row in comparison["ranking"]:
        print(f"  {row['rank']}. {row['model']} -> {row['mean_score']:.2f}")


if __name__ == "__main__":
    main()
