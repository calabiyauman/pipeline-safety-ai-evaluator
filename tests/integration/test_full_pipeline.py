from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from core.evaluator import PipelineSafetyEvaluator  # noqa: E402
from models.ai_interface import AIModelInterface  # noqa: E402
from scenarios.base import load_builtin_suite  # noqa: E402
from utils.reporting import ReportGenerator  # noqa: E402


class MockAIModel(AIModelInterface):
    def __init__(self):
        super().__init__(name="mock-ai", version="0.1")

    def query(self, prompt: str) -> str:
        return (
            "Work permit, gas monitoring, qualified personnel, and emergency procedures are required. "
            "Follow API 1104 and ASME B31.8 with controlled isolation and verification."
        )


def test_full_pipeline_with_mock_model(tmp_path):
    suite = load_builtin_suite("safety")
    scenarios = suite.scenarios[:2]

    evaluator = PipelineSafetyEvaluator(output_dir=str(tmp_path), verbose=False)
    results = evaluator.evaluate(
        model=MockAIModel(),
        test_suite=scenarios,
        runs=2,
        include_abnormal=False,
        random_order=False,
    )

    assert results["model_name"] == "mock-ai"
    assert results["summary"]["total_tests"] == 2
    assert len(results["raw_results"]) == 4

    reporter = ReportGenerator(str(tmp_path))
    report_path = reporter.generate_json_report(results)
    assert Path(report_path).exists()
