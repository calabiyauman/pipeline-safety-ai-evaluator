from pathlib import Path
import json

from jsonschema import validate


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_question_bank_template_matches_schema():
    schema_path = PROJECT_ROOT / "benchmark_sources" / "question_bank.schema.json"
    template_path = PROJECT_ROOT / "benchmark_sources" / "question_bank.template.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    template = json.loads(template_path.read_text(encoding="utf-8"))

    validate(instance=template, schema=schema)
