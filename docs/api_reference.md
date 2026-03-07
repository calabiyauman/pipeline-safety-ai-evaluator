# PSAE API Reference

This reference documents the primary public interfaces for the Pipeline Safety AI Evaluator.

## Package

- `psae`
  - `PipelineSafetyEvaluator`
  - `MetricCalculator`
  - `SafetyMetrics`
  - `StatisticalAnalyzer`
  - `TestScenario`
  - `TestSuite`
  - `AIModelInterface`

## Core Classes

### `PipelineSafetyEvaluator`

Main orchestration class for model benchmarking.

**Constructor**

```python
PipelineSafetyEvaluator(
    config_path: str | None = None,
    output_dir: str = "./results",
    verbose: bool = True,
)
```

**Methods**

- `evaluate(model, test_suite, runs=5, include_abnormal=True, random_order=True) -> dict`
  - Executes scenario evaluation loop and returns:
    - `summary`
    - `aggregated_results`
    - `raw_results`
    - `statistical_analysis`
    - `run_manifest`

### `MetricCalculator`

Computes the weighted metric set used in final scoring.

**Methods**

- `calculate(response, expected_elements, expected_standards, category) -> dict`
  - Returns metric objects with top-level `score` keys for:
    - `accuracy`
    - `relevance`
    - `safety`
    - `completeness`
    - `technical_depth`
    - `sources`

### `StatisticalAnalyzer`

Statistical utility class used by evaluator and comparison workflows.

**Methods**

- `confidence_interval(data, confidence_level=None)`
- `one_way_anova(groups)`
- `cohens_d(group1, group2)`
- `intraclass_correlation(ratings, model="single")`
- `power_analysis(effect_size, alpha=0.05, power=0.8, sample_size=None)`
- `normality_test(data)`
- `descriptive_statistics(data)`
- `compare_models(model_results)`

## Scenario Interfaces

Use the scenario package for built-in benchmark suites.

```python
from psae.scenarios import load_builtin_suite

safety_suite = load_builtin_suite("safety")
full_suite = load_builtin_suite("full")
```

Supported built-in suite values:

- `safety`
- `engineering`
- `inspection`
- `regulatory`
- `benchmark-sources`
- `full`

## Model Interfaces

```python
from psae.models import OpenAIWrapper, AnthropicWrapper, GeminiWrapper, HumanExpertBaseline
```

- `OpenAIWrapper`
- `AnthropicWrapper`
- `GeminiWrapper`
- `HumanExpertBaseline`

All wrappers implement the abstract contract:

- `query(prompt: str) -> str`
- `batch_query(prompts: list[str]) -> list[str]`

## Reporting Utilities

```python
from psae.utils import ReportGenerator
```

`ReportGenerator` supports:

- `generate_json_report(results)`
- `generate_html_report(results)`
- `generate_markdown_report(results)`
- `generate_latex_tables(results)`

Generated reports include metadata such as:

- report schema version
- benchmark manifest version
- benchmark dataset version

## Benchmark Integrity Utilities

```python
from psae.utils import validate_manifest

report = validate_manifest()
assert report["all_ok"]
```

Or via CLI:

```bash
psae validate-benchmark
```

Signature workflow CLI:

```bash
psae sign-benchmark --key-id maintainer-2026
psae verify-benchmark-signature
```

## CLI: Custom Suite Files

Use `--suite-file` to evaluate an external JSON benchmark suite without changing code:

```bash
psae evaluate --model gpt-4 --suite-file ./my_suites/custom_suite.json --runs 5
```

Expected JSON structure:

```json
{
  "name": "Custom Suite",
  "scenarios": [
    {
      "test_id": "CU-001",
      "name": "Scenario Name",
      "category": "safety",
      "risk_level": 8,
      "situation": "...",
      "task": "...",
      "expected_elements": [],
      "expected_standards": [],
      "critical_elements": [],
      "abnormal_variants": [],
      "validation_notes": ""
    }
  ]
}
```
