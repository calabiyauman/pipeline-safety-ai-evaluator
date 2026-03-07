from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from core.statistical import StatisticalAnalyzer, compare_to_baseline  # noqa: E402


def test_confidence_interval_single_point():
    analyzer = StatisticalAnalyzer()
    ci = analyzer.confidence_interval([88.0])
    assert ci == (88.0, 88.0)


def test_one_way_anova_detects_difference():
    analyzer = StatisticalAnalyzer()
    result = analyzer.one_way_anova(
        {
            "A": [90, 91, 92, 90, 91],
            "B": [70, 71, 72, 69, 70],
            "C": [80, 79, 81, 80, 82],
        }
    )
    assert result["p_value"] < 0.05
    assert result["significance"] in {"highly_significant", "very_significant", "significant"}


def test_cohens_d_direction_and_interpretation():
    analyzer = StatisticalAnalyzer()
    result = analyzer.cohens_d([90, 92, 91, 93], [70, 71, 72, 69])
    assert result["cohens_d"] > 0
    assert result["direction"] == "group1_higher"
    assert result["interpretation"] in {"medium", "large"}


def test_normality_test_requires_minimum_points():
    analyzer = StatisticalAnalyzer()
    result = analyzer.normality_test([1.0, 2.0])
    assert result["statistic"] is None
    assert "Need at least 3 data points" in result["note"]


def test_power_analysis_sample_size_mode():
    analyzer = StatisticalAnalyzer()
    result = analyzer.power_analysis(effect_size=0.5, alpha=0.05, power=0.8)
    assert "required_n_per_group" in result
    assert result["required_n_per_group"] > 0


def test_compare_to_baseline_returns_performance_label():
    analyzer = StatisticalAnalyzer()
    comparison = compare_to_baseline(
        test_scores=[85, 86, 84, 85, 87],
        baseline_scores=[90, 91, 89, 90, 92],
        analyzer=analyzer,
    )
    assert comparison["performance"] in {"comparable", "below_baseline", "above_baseline"}
