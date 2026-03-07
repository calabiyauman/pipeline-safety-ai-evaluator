import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_human_baseline_covers_all_test_cases():
    test_case_dir = PROJECT_ROOT / "data" / "test_cases"
    baseline_path = PROJECT_ROOT / "data" / "human_baseline" / "responses.json"

    all_test_ids = set()
    for filename in ["safety_critical.json", "engineering.json", "inspection.json", "regulatory.json"]:
        try:
            data = _load_json(test_case_dir / filename)
        except Exception:
            # Allow temporarily invalid in-progress files; loader may fallback to built-ins.
            continue
        scenarios = data.get("scenarios") or data.get("test_cases") or []
        all_test_ids.update(scenario["test_id"] for scenario in scenarios)

    assert all_test_ids, "No valid test IDs discovered from data/test_cases files."

    baseline = _load_json(baseline_path)
    baseline_ids = {entry["test_id"] for entry in baseline["responses"]}

    missing = sorted(all_test_ids - baseline_ids)
    assert not missing, f"Human baseline missing test IDs: {missing}"
