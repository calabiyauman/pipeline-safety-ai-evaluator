from pathlib import Path
import sys
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from scenarios.base import load_benchmark_sources_suite  # noqa: E402


def test_load_benchmark_sources_suite_from_repo_sources():
    suite = load_benchmark_sources_suite()
    assert len(suite.scenarios) > 0
    ids = {scenario.test_id for scenario in suite.scenarios}
    assert "WLD-001" in ids


def test_load_benchmark_sources_suite_auto_picks_new_json(tmp_path):
    sources_root = tmp_path / "benchmark_sources"
    sources_root.mkdir(parents=True, exist_ok=True)

    new_questions = [
        {
            "question_id": "NEW-001",
            "title": "New Auto Picked Question",
            "category": "engineering",
            "risk_level": 6,
            "situation": "A custom scenario is added by contributor.",
            "task": "Determine required design action.",
            "expected_elements": ["formula application", "code reference", "safety margin"],
            "critical_elements": ["code reference"],
            "expected_standards": ["ASME B31.8"],
            "abnormal_variants": [],
            "notes": "auto-picked",
        }
    ]
    (sources_root / "new_questions.json").write_text(
        json.dumps(new_questions),
        encoding="utf-8",
    )

    suite = load_benchmark_sources_suite(str(sources_root))
    ids = {scenario.test_id for scenario in suite.scenarios}
    assert "NEW-001" in ids
