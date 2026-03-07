from pathlib import Path
import json
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from utils.reporting import ReportGenerator  # noqa: E402


def test_json_report_includes_schema_metadata(tmp_path):
    reporter = ReportGenerator(str(tmp_path))
    results = {
        "model_name": "mock-ai",
        "model_version": "0.1",
        "timestamp": "2026-03-06 12:00:00",
        "summary": {
            "overall_score": 90.0,
            "overall_pass_rate": 100.0,
            "overall_dangerous_error_rate": 0.0,
            "total_tests": 2,
        },
        "statistical_analysis": {},
    }
    report_path = reporter.generate_json_report(results)
    data = json.loads(Path(report_path).read_text(encoding="utf-8"))
    assert "report_metadata" in data
    assert data["report_metadata"]["schema_version"] == reporter.REPORT_SCHEMA_VERSION
