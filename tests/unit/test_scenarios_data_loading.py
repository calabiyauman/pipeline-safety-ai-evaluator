import sys


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from scenarios.base import load_builtin_suite  # noqa: E402


def test_full_suite_prefers_json_data_files():
    suite = load_builtin_suite("full")
    assert len(suite.scenarios) > 0

    ids = {scenario.test_id for scenario in suite.scenarios}
    expected_ids = set()
    for category in ["safety", "engineering", "inspection", "regulatory"]:
        expected_ids.update(s.test_id for s in load_builtin_suite(category).scenarios)

    # Full suite should include IDs from all category suites (JSON or fallback built-ins).
    assert expected_ids.issubset(ids)


def test_regulatory_suite_loads_from_data():
    suite = load_builtin_suite("regulatory")
    assert len(suite.scenarios) > 0
    assert all(s.category == "regulatory" for s in suite.scenarios)
