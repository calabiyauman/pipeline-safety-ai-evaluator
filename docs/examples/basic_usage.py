"""Basic PSAE usage example."""

from psae import PipelineSafetyEvaluator
from psae.models import HumanExpertBaseline
from psae.scenarios import load_builtin_suite
from psae.utils import ReportGenerator


def main() -> None:
    evaluator = PipelineSafetyEvaluator(config_path="configs/evaluation.yaml")
    model = HumanExpertBaseline("data/human_baseline/responses.json")
    suite = load_builtin_suite("safety")

    # Use lower run count for a quick demo.
    results = evaluator.evaluate(
        model=model,
        test_suite=suite,
        runs=2,
        include_abnormal=False,
        random_order=False,
    )

    reporter = ReportGenerator("./results")
    json_report = reporter.generate_json_report(results)
    html_report = reporter.generate_html_report(results)

    print("Overall Score:", round(results["summary"]["overall_score"], 2))
    print("Pass Rate:", round(results["summary"]["overall_pass_rate"], 2))
    print("JSON Report:", json_report)
    print("HTML Report:", html_report)


if __name__ == "__main__":
    main()
