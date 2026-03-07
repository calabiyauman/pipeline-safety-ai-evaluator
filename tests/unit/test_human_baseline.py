from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from models.ai_interface import HumanExpertBaseline  # noqa: E402


def test_human_baseline_returns_known_response():
    baseline = HumanExpertBaseline(
        responses_path=str(PROJECT_ROOT / "data" / "human_baseline" / "responses.json")
    )
    response = baseline.query("Evaluate this scenario Test ID: SC-001 please.")
    assert "hot tapping" in response.lower() or "permit" in response.lower()


def test_human_baseline_default_on_missing_id():
    baseline = HumanExpertBaseline(
        responses_path=str(PROJECT_ROOT / "data" / "human_baseline" / "responses.json")
    )
    response = baseline.query("No test id appears in this prompt.")
    assert "No human baseline response found" in response
