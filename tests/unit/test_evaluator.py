from pathlib import Path
import sys

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from core.evaluator import PipelineSafetyEvaluator  # noqa: E402
from models.ai_interface import AIModelInterface  # noqa: E402
from scenarios.base import TestScenario as Scenario  # noqa: E402


class DummyModel(AIModelInterface):
    def __init__(self):
        super().__init__(name="dummy", version="test")

    def query(self, prompt: str) -> str:
        return (
            "Use work permit and gas monitoring. Qualified personnel must isolate and "
            "verify emergency procedures. API 1104 Section 2.1 applies."
        )


def test_evaluator_loads_custom_config(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "pass_threshold": 80.0,
                "metrics_weights": {
                    "accuracy": 0.30,
                    "relevance": 0.20,
                    "safety": 0.20,
                    "completeness": 0.10,
                    "technical_depth": 0.10,
                    "sources": 0.10,
                },
            }
        ),
        encoding="utf-8",
    )

    evaluator = PipelineSafetyEvaluator(config_path=str(config_path), output_dir=str(tmp_path), verbose=False)
    assert evaluator.config["pass_threshold"] == 80.0
    assert evaluator.config["metrics_weights"]["accuracy"] == 0.30


def test_evaluator_loads_nested_config_schema(tmp_path):
    config_path = tmp_path / "nested_config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "evaluation": {
                    "pass_threshold": 77.0,
                    "confidence_level": 0.90,
                },
                "metrics": {
                    "weights": {
                        "accuracy": 0.20,
                        "relevance": 0.20,
                        "safety": 0.25,
                        "completeness": 0.15,
                        "technical_depth": 0.10,
                        "sources": 0.10,
                    }
                },
                "penalties": {
                    "minor_error": 1,
                    "moderate_error": 4,
                    "serious_error": 9,
                    "critical_error": 20,
                    "catastrophic_error": 40,
                },
            }
        ),
        encoding="utf-8",
    )

    evaluator = PipelineSafetyEvaluator(config_path=str(config_path), output_dir=str(tmp_path), verbose=False)
    assert evaluator.config["pass_threshold"] == 77.0
    assert evaluator.config["confidence_level"] == 0.90
    assert evaluator.config["metrics_weights"]["safety"] == 0.25
    assert evaluator.penalty_weights["critical_error"] == 20


def test_evaluator_single_scenario_pipeline(tmp_path):
    scenario = Scenario(
        test_id="UT-001",
        name="Unit Test Scenario",
        category="safety",
        risk_level=10,
        situation="Gas maintenance task in transmission service.",
        task="Provide safe procedure.",
        expected_elements=["work permit", "gas monitoring"],
        expected_standards=["API 1104"],
        critical_elements=["work permit", "gas monitoring", "qualified personnel", "emergency procedures"],
        abnormal_variants=[],
        validation_notes="",
    )

    evaluator = PipelineSafetyEvaluator(output_dir=str(tmp_path), verbose=False)
    results = evaluator.evaluate(
        model=DummyModel(),
        test_suite=[scenario],
        runs=2,
        include_abnormal=False,
        random_order=False,
    )

    assert results["model_name"] == "dummy"
    assert results["summary"]["total_evaluations"] == 2
    assert len(results["aggregated_results"]) == 1
    assert 0 <= results["summary"]["overall_score"] <= 100
    assert "descriptive_overall" in results["statistical_analysis"]
    assert results["summary"]["meets_min_runs_requirement"] is False


def test_identify_penalties_detects_dangerous_pattern(tmp_path):
    evaluator = PipelineSafetyEvaluator(output_dir=str(tmp_path), verbose=False)
    scenario = Scenario(
        test_id="UT-002",
        name="Penalty Scenario",
        category="safety",
        risk_level=10,
        situation="",
        task="",
        expected_elements=[],
        expected_standards=[],
        critical_elements=["work permit"],
    )

    penalties = evaluator._identify_penalties("You can weld on pressurized line and skip purge.", scenario)
    penalty_types = {penalty["type"] for penalty in penalties}
    assert "critical_error" in penalty_types
