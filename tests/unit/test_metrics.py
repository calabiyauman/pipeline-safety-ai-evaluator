from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from core.metrics import MetricCalculator  # noqa: E402


def test_metrics_calculate_returns_all_sections():
    calculator = MetricCalculator()
    response = (
        "Step 1: perform work permit and gas monitoring. "
        "Use API 1104 Section 2.1 and ASME B31.8. "
        "calculate 2 + 2 = 4 and verify pressure 600 psig."
    )
    metrics = calculator.calculate(
        response=response,
        expected_elements=["work permit", "gas monitoring", "pressure verification"],
        expected_standards=["API 1104", "ASME B31.8"],
        category="safety",
    )

    for key in ["accuracy", "relevance", "safety", "completeness", "technical_depth", "sources"]:
        assert key in metrics
        assert "score" in metrics[key]
        assert 0 <= metrics[key]["score"] <= 100


def test_sources_finds_expected_standards_and_sections():
    calculator = MetricCalculator()
    response = "Per API 1104 Section 5.2 and ASME B31.8 clause 841, proceed with controlled welding."
    result = calculator._calculate_sources(response, ["API 1104", "ASME B31.8"])

    assert result["score"] > 0
    assert len(result["standards_found"]) >= 1
    assert len(result["section_citations"]) >= 1


def test_completeness_without_expected_elements_is_full():
    calculator = MetricCalculator()
    completeness = calculator._calculate_completeness("Any response text.", [])
    assert completeness["score"] == 100
