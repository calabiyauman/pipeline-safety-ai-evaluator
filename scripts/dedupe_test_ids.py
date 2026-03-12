#!/usr/bin/env python3
"""
Remove duplicate test_ids from the four canonical test case JSON files.
Keeps the first occurrence of each test_id per file.
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "test_cases"

FILES = ["safety_critical.json", "engineering.json", "inspection.json", "regulatory.json"]


def dedupe_file(path: Path) -> tuple[int, int]:
    """Remove duplicate test_ids. Returns (original_count, deduped_count)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("test_cases", [])
    original = len(cases)
    seen = set()
    deduped = []
    for c in cases:
        tid = c.get("test_id")
        if tid and tid in seen:
            continue
        if tid:
            seen.add(tid)
        deduped.append(c)
    data["test_cases"] = deduped
    if "metadata" in data and "total_tests" in data["metadata"]:
        data["metadata"]["total_tests"] = len(deduped)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return original, len(deduped)


def main():
    print("Deduplicating test_ids...")
    total_removed = 0
    for name in FILES:
        path = DATA_DIR / name
        if not path.exists():
            print(f"  SKIP: {name} not found")
            continue
        orig, new = dedupe_file(path)
        removed = orig - new
        if removed:
            print(f"  {name}: {orig} -> {new} (removed {removed} duplicates)")
            total_removed += removed
        else:
            print(f"  {name}: no duplicates")
    print(f"Done. Removed {total_removed} duplicate(s) total.")


if __name__ == "__main__":
    main()
