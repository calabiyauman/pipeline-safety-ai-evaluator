#!/usr/bin/env python3
"""
Restore the four canonical test case JSON files from archive.
Use when data/test_cases/*.json were overwritten with incorrect data.
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "test_cases"
ARCHIVE_DIR = DATA_DIR / "archive"


def dedupe_by_test_id(cases: list) -> list:
    """Keep first occurrence of each test_id."""
    seen = set()
    result = []
    for c in cases:
        tid = c.get("test_id")
        if tid and tid in seen:
            continue
        if tid:
            seen.add(tid)
        result.append(c)
    return result


def ensure_situation_task(tc: dict) -> dict:
    """Ensure scenario has situation and task (required by TestScenario.from_dict)."""
    situation = (tc.get("situation") or "").strip()
    task = (tc.get("task") or "").strip()
    if situation and task:
        return tc
    # Derive from available fields
    name = (tc.get("name") or tc.get("test_id") or "").strip()
    detailed = (tc.get("expected_response_detailed") or "").strip()
    if not situation:
        situation = name or (detailed[:400] + "..." if len(detailed) > 400 else detailed) or "Scenario context."
    if not task:
        task = "Provide detailed analysis per applicable standards and codes."
    tc = dict(tc)
    tc["situation"] = situation
    tc["task"] = task
    return tc


def restore_safety_critical():
    """Restore safety_critical.json from safety_critical_combined.json (category=safety_critical only)."""
    src = ARCHIVE_DIR / "safety_critical_combined.json"
    if not src.exists():
        print(f"  SKIP: {src} not found")
        return 0
    data = json.loads(src.read_text(encoding="utf-8"))
    cases = data if isinstance(data, list) else data.get("test_cases", [])
    filtered = [ensure_situation_task(c) for c in cases if c.get("category") == "safety_critical"]
    filtered = dedupe_by_test_id(filtered)
    out = {
        "metadata": {
            "file_name": "safety_critical.json",
            "description": "Safety-critical pipeline test cases with high risk levels",
            "total_tests": len(filtered),
            "created_date": "2026-03-07",
            "version": "1.0",
        },
        "test_cases": filtered,
    }
    dest = DATA_DIR / "safety_critical.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Restored {len(filtered)} cases to {dest.name}")
    return len(filtered)


def restore_engineering():
    """Restore engineering.json from engineering_combined.json."""
    src = ARCHIVE_DIR / "engineering_combined.json"
    if not src.exists():
        print(f"  SKIP: {src} not found")
        return 0
    data = json.loads(src.read_text(encoding="utf-8"))
    cases = data if isinstance(data, list) else data.get("test_cases", [])
    filtered = [c for c in cases if c.get("category") == "engineering"]
    filtered = [ensure_situation_task(c) for c in filtered]
    filtered = dedupe_by_test_id(filtered)
    out = {
        "metadata": {
            "file_name": "engineering.json",
            "description": "Engineering calculation and design test cases",
            "total_tests": len(filtered),
            "created_date": "2026-03-07",
            "version": "1.0",
        },
        "test_cases": filtered,
    }
    dest = DATA_DIR / "engineering.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Restored {len(filtered)} cases to {dest.name}")
    return len(filtered)


def restore_inspection():
    """Restore inspection.json from inspection_combined.json."""
    src = ARCHIVE_DIR / "inspection_combined.json"
    if not src.exists():
        print(f"  SKIP: {src} not found")
        return 0
    data = json.loads(src.read_text(encoding="utf-8"))
    cases = data.get("test_cases", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    filtered = [c for c in cases if c.get("category") == "inspection"]
    filtered = [ensure_situation_task(c) for c in filtered]
    filtered = dedupe_by_test_id(filtered)
    out = {
        "metadata": {
            "file_name": "inspection.json",
            "description": "Inspection and testing test cases",
            "total_tests": len(filtered),
            "created_date": "2026-03-07",
            "version": "1.0",
        },
        "test_cases": filtered,
    }
    dest = DATA_DIR / "inspection.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Restored {len(filtered)} cases to {dest.name}")
    return len(filtered)


def restore_regulatory():
    """Restore regulatory.json from regulatory_combined.json."""
    src = ARCHIVE_DIR / "regulatory_combined.json"
    if not src.exists():
        print(f"  SKIP: {src} not found")
        return 0
    data = json.loads(src.read_text(encoding="utf-8"))
    cases = data.get("test_cases", [])
    filtered = [c for c in cases if c.get("category") == "regulatory"]
    filtered = [ensure_situation_task(c) for c in filtered]
    filtered = dedupe_by_test_id(filtered)
    out = {
        "metadata": {
            "file_name": "regulatory.json",
            "description": "Regulatory compliance test cases",
            "total_tests": len(filtered),
            "created_date": "2026-03-07",
            "version": "1.0",
        },
        "test_cases": filtered,
    }
    dest = DATA_DIR / "regulatory.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Restored {len(filtered)} cases to {dest.name}")
    return len(filtered)


def main():
    print("Restoring test case files from archive...")
    n1 = restore_safety_critical()
    n2 = restore_engineering()
    n3 = restore_inspection()
    n4 = restore_regulatory()
    print(f"Done. Total: safety_critical={n1}, engineering={n2}, inspection={n3}, regulatory={n4}")


if __name__ == "__main__":
    main()
