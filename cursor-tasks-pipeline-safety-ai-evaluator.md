# Pipeline Safety AI Evaluator (PSAE) - Cursor Task List

## Project Overview
A PhD-level evaluation framework for AI systems in pipeline safety-critical applications. Built with comprehensive statistical methodology, STAR-R test framework, and risk-adjusted scoring.

**Current Status:** Core engine, model interfaces, CLI, configs, test data, statistical outputs, benchmark governance checks, and CI are implemented. Remaining work is documentation depth, advanced reporting polish, and benchmark release immutability/signing.

---

## 🎯 Phase 1: Model Interfaces (CRITICAL - Blocking)

### Task 1.1: Create `src/models/ai_interface.py`
**File:** `projects/pipeline-safety-ai-evaluator/src/models/ai_interface.py`

Create abstract base class and implementations for AI model interfaces. This is imported by the main `__init__.py` and is currently missing.

```python
# Required components:
# 1. AIModelInterface (abstract base class)
#    - name: str property
#    - version: str property
#    - query(prompt: str) -> str method (abstract)
#    - batch_query(prompts: List[str]) -> List[str] method
#
# 2. OpenAIWrapper (implements AIModelInterface)
#    - Initialize with api_key, model="gpt-4"
#    - Implement query() using openai.ChatCompletion
#    - Handle errors gracefully
#
# 3. AnthropicWrapper (implements AIModelInterface)
#    - Initialize with api_key, model="claude-3-5-sonnet"
#    - Implement query() using anthropic.Anthropic
#
# 4. GeminiWrapper (implements AIModelInterface)
#    - Initialize with api_key, model="gemini-1.5-pro"
#    - Implement query() using google.generativeai
#
# 5. HumanExpertBaseline (for comparison)
#    - Loads pre-scored human expert responses from JSON
#    - Returns stored responses based on test_id
```

**Acceptance Criteria:**
- All three model wrappers can be instantiated
- query() method returns string response
- Proper error handling for API failures
- Rate limiting support

---

### Task 1.2: Create `src/models/__init__.py`
**File:** `projects/pipeline-safety-ai-evaluator/src/models/__init__.py`

Export all model interfaces:
```python
from .ai_interface import (
    AIModelInterface,
    OpenAIWrapper,
    AnthropicWrapper,
    GeminiWrapper,
    HumanExpertBaseline,
)

__all__ = [
    "AIModelInterface",
    "OpenAIWrapper", 
    "AnthropicWrapper",
    "GeminiWrapper",
    "HumanExpertBaseline",
]
```

---

## 🛠️ Phase 2: Configuration Files

### Task 2.1: Create `configs/evaluation.yaml`
**File:** `projects/pipeline-safety-ai-evaluator/configs/evaluation.yaml`

```yaml
# PSAE Evaluation Configuration

evaluation:
  confidence_level: 0.95
  min_runs: 5
  max_runs: 10
  pass_threshold: 70.0
  excellent_threshold: 90.0
  dangerous_threshold: 30.0
  
scenarios:
  include_abnormal: true
  abnormal_ratio: 0.3  # 30% of tests include abnormal conditions
  random_order: true
  random_seed: 42
  
metrics:
  weights:
    accuracy: 0.25
    relevance: 0.20
    safety: 0.20
    completeness: 0.15
    technical_depth: 0.10
    sources: 0.10
    
penalties:
  minor_error: 2
  moderate_error: 5
  serious_error: 10
  critical_error: 25
  catastrophic_error: 50

statistical_tests:
  - anova
  - tukey_hsd
  - cohens_d
  - icc
  - normality

output:
  save_raw_responses: true
  save_metrics: true
  generate_html_report: true
  generate_json_report: true
  generate_latex_tables: false
```

---

### Task 2.2: Create `configs/models.yaml`
**File:** `projects/pipeline-safety-ai-evaluator/configs/models.yaml`

```yaml
# Model configurations and API settings

models:
  gpt-4-turbo:
    provider: openai
    model_id: gpt-4-turbo-preview
    temperature: 0.1
    max_tokens: 4096
    timeout: 60
    retry_attempts: 3
    
  gpt-4:
    provider: openai
    model_id: gpt-4
    temperature: 0.1
    max_tokens: 4096
    timeout: 60
    retry_attempts: 3
    
  claude-3-5-sonnet:
    provider: anthropic
    model_id: claude-3-5-sonnet-20241022
    temperature: 0.1
    max_tokens: 4096
    timeout: 60
    retry_attempts: 3
    
  claude-3-opus:
    provider: anthropic
    model_id: claude-3-opus-20240229
    temperature: 0.1
    max_tokens: 4096
    timeout: 60
    retry_attempts: 3
    
  gemini-1-5-pro:
    provider: google
    model_id: gemini-1.5-pro
    temperature: 0.1
    max_tokens: 4096
    timeout: 60
    retry_attempts: 3

# API Keys (set via environment variables)
# OPENAI_API_KEY
# ANTHROPIC_API_KEY  
# GOOGLE_API_KEY
```

---

## 📝 Phase 3: Test Data Files

### Task 3.1: Create `data/test_cases/safety_critical.json`
**File:** `projects/pipeline-safety-ai-evaluator/data/test_cases/safety_critical.json`

Extract the 8 safety-critical test scenarios from `src/scenarios/base.py` into JSON format. Add 4 more to reach the promised 8 safety-critical tests.

Structure per test case:
```json
{
  "test_id": "SC-001",
  "name": "Hot Tapping Safety Protocols",
  "category": "safety",
  "risk_level": 10,
  "situation": "...",
  "task": "...",
  "expected_elements": [...],
  "expected_standards": [...],
  "critical_elements": [...],
  "abnormal_variants": [...],
  "validation_notes": "...",
  "reference_human_response": "...",
  "human_expert_score": 94.5
}
```

**Required test cases:**
1. SC-001: Hot Tapping Safety Protocols (exists in base.py)
2. SC-002: Emergency Gas Leak Response (exists in base.py)
3. SC-003: Confined Space Entry (Gas)
4. SC-004: Excavation Near Pipeline
5. SC-005: Valve Operation Under Pressure
6. SC-006: Compressor Station Emergency Shutdown
7. SC-007: Fire at Pipeline Facility
8. SC-008: Sour Gas Release Response

---

### Task 3.2: Create `data/test_cases/engineering.json`
**File:** `projects/pipeline-safety-ai-evaluator/data/test_cases/engineering.json`

Extract 2 from base.py + add 6 more to reach 8 tests:
1. EN-001: Control Valve Cv Calculation (exists)
2. EN-002: ASME B31.8 Hydrostatic Testing (exists)
3. EN-003: Sour Gas Material Selection
4. EN-004: Natural Gas Flow Calculation
5. EN-005: Cathodic Protection Design
6. EN-006: Pipeline Stress Analysis
7. EN-007: Leak Detection System Design
8. EN-008: Compressor Sizing

---

### Task 3.3: Create `data/test_cases/inspection.json`
**File:** `projects/pipeline-safety-ai-evaluator/data/test_cases/inspection.json`

Create 4 inspection tests (1 exists in base.py + 3 new):
1. IN-001: Sour Gas Corrosion Detection (exists)
2. IN-002: Smart Pigging Data Analysis
3. IN-003: External Corrosion Assessment
4. IN-004: Weld Inspection Protocols

---

### Task 3.4: Create `data/test_cases/regulatory.json`
**File:** `projects/pipeline-safety-ai-evaluator/data/test_cases/regulatory.json`

Create 4 regulatory tests:
1. RE-001: API Valve Standards Comparison
2. RE-002: PHMSA Compliance Assessment
3. RE-003: O&M Manual Development
4. RE-004: MAOP Verification

---

### Task 3.5: Create `data/human_baseline/responses.json`
**File:** `projects/pipeline-safety-ai-evaluator/data/human_baseline/responses.json`

Pre-scored human expert responses for baseline comparison:
- Include response text for each test case
- Include element-by-element scoring
- Expert credentials: "Licensed PE with 15+ years pipeline experience"

---

## 🧪 Phase 4: Testing Infrastructure

### Task 4.1: Create `tests/unit/test_evaluator.py`
**File:** `projects/pipeline-safety-ai-evaluator/tests/unit/test_evaluator.py`

Unit tests for the evaluator core:
- Test initialization with/without config
- Test single evaluation run
- Test aggregation logic
- Test penalty calculation
- Test risk multiplier application

---

### Task 4.2: Create `tests/unit/test_metrics.py`
**File:** `projects/pipeline-safety-ai-evaluator/tests/unit/test_metrics.py`

Unit tests for metrics calculation:
- Test accuracy calculation with sample responses
- Test safety scoring
- Test completeness calculation
- Test technical depth assessment
- Test standards extraction

---

### Task 4.3: Create `tests/unit/test_statistical.py`
**File:** `projects/pipeline-safety-ai-evaluator/tests/unit/test_statistical.py`

Unit tests for statistical functions:
- Test confidence interval calculation
- Test ANOVA
- Test Cohen's d
- Test ICC
- Test power analysis
- Test normality test

---

### Task 4.4: Create `tests/integration/test_full_pipeline.py`
**File:** `projects/pipeline-safety-ai-evaluator/tests/integration/test_full_pipeline.py`

Integration test with mock AI model:
- Create MockAIModel class (returns canned responses)
- Run full evaluation cycle
- Verify results structure
- Verify report generation

---

### Task 4.5: Create `tests/__init__.py` and `tests/unit/__init__.py`
**Files:** 
- `projects/pipeline-safety-ai-evaluator/tests/__init__.py`
- `projects/pipeline-safety-ai-evaluator/tests/unit/__init__.py`
- `projects/pipeline-safety-ai-evaluator/tests/integration/__init__.py`

---

## 💻 Phase 5: CLI and Utils

### Task 5.1: Create `src/cli.py`
**File:** `projects/pipeline-safety-ai-evaluator/src/cli.py`

Complete CLI implementation:

```python
"""
Command line interface for PSAE.
"""

import argparse
import json
import sys
from pathlib import Path
from . import PipelineSafetyEvaluator, __version__
from .models import OpenAIWrapper, AnthropicWrapper, GeminiWrapper

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline Safety AI Evaluator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Run evaluation")
    eval_parser.add_argument("--model", required=True, 
                            choices=["gpt-4", "gpt-4-turbo", "claude-3-5-sonnet", 
                                    "claude-3-opus", "gemini-1-5-pro"],
                            help="Model to evaluate")
    eval_parser.add_argument("--suite", default="full",
                          choices=["safety", "engineering", "inspection", "full"],
                          help="Test suite to run")
    eval_parser.add_argument("--runs", type=int, default=5,
                          help="Number of runs per test")
    eval_parser.add_argument("--config", help="Configuration file path")
    eval_parser.add_argument("--output", default="./results",
                          help="Output directory")
    eval_parser.add_argument("--no-abnormal", action="store_true",
                          help="Skip abnormal condition tests")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare models")
    compare_parser.add_argument("--models", required=True,
                              help="Comma-separated model names")
    compare_parser.add_argument("--output", default="./results",
                               help="Output directory")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate-config", 
                                            help="Validate configuration")
    validate_parser.add_argument("config", help="Config file to validate")
    
    # List command
    list_parser = subparsers.add_parser("list-tests", help="List test cases")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--risk-level", type=int, help="Filter by min risk")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Implement command handlers
    if args.command == "evaluate":
        cmd_evaluate(args)
    elif args.command == "compare":
        cmd_compare(args)
    # etc.

def cmd_evaluate(args):
    """Handle evaluate command."""
    # Load model
    # Initialize evaluator
    # Run evaluation
    # Generate reports
    pass

def cmd_compare(args):
    """Handle compare command."""
    pass

if __name__ == "__main__":
    main()
```

---

### Task 5.2: Create `src/utils/reporting.py`
**File:** `projects/pipeline-safety-ai-evaluator/src/utils/reporting.py`

Report generation utilities:

```python
"""
Report generation for PSAE evaluation results.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import datetime

class ReportGenerator:
    """Generate evaluation reports in multiple formats."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html_report(self, results: Dict[str, Any]) -> str:
        """Generate HTML report with charts and tables."""
        # Use Jinja2 templating
        # Include:
        # - Executive summary
        # - Score breakdown by category
        # - Statistical significance tables
        # - Abnormal condition handling
        # - Detailed test results
        pass
    
    def generate_json_report(self, results: Dict[str, Any]) -> str:
        """Generate machine-readable JSON report."""
        filepath = self.output_dir / f"report_{datetime.datetime.now().isoformat()}.json"
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        return str(filepath)
    
    def generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate Markdown report for documentation."""
        pass
    
    def generate_latex_tables(self, results: Dict[str, Any]) -> str:
        """Generate LaTeX tables for academic papers."""
        pass
```

---

### Task 5.3: Create `src/utils/__init__.py`
**File:** `projects/pipeline-safety-ai-evaluator/src/utils/__init__.py`

```python
from .reporting import ReportGenerator

__all__ = ["ReportGenerator"]
```

---

## 📊 Phase 6: Documentation

### Task 6.1: Create `docs/api_reference.md`
**File:** `projects/pipeline-safety-ai-evaluator/docs/api_reference.md`

API documentation for all public classes and methods.

---

### Task 6.2: Create `docs/examples/basic_usage.py`
**File:** `projects/pipeline-safety-ai-evaluator/docs/examples/basic_usage.py`

Working example:
```python
"""Basic usage example for PSAE."""

from psae import PipelineSafetyEvaluator, TestSuite
from psae.models import OpenAIWrapper

# Initialize evaluator
evaluator = PipelineSafetyEvaluator(
    config_path="configs/evaluation.yaml"
)

# Load model
model = OpenAIWrapper(
    model="gpt-4",
    api_key="your-api-key-here"
)

# Run evaluation
results = evaluator.evaluate(
    model=model,
    test_suite=TestSuite.load_from_json("data/test_cases/safety_critical.json"),
    runs=5,
    include_abnormal=True
)

# Print summary
print(f"Overall Score: {results['summary']['overall_score']:.2f}")
print(f"Safety Score: {results['summary']['safety_score']:.2f}")
```

---

### Task 6.3: Create `docs/examples/comparison_analysis.py`
**File:** `projects/pipeline-safety-ai-evaluator/docs/examples/comparison_analysis.py`

Example comparing multiple models:
```python
"""Compare multiple AI models."""

from psae import PipelineSafetyEvaluator
from psae.models import OpenAIWrapper, AnthropicWrapper
from psae.core.statistical import StatisticalAnalyzer

# Evaluate multiple models
models = {
    "GPT-4": OpenAIWrapper(model="gpt-4"),
    "Claude": AnthropicWrapper(model="claude-3-5-sonnet"),
}

results = {}
for name, model in models.items():
    evaluator = PipelineSafetyEvaluator()
    results[name] = evaluator.evaluate(model, ...)

# Statistical comparison
analyzer = StatisticalAnalyzer()
comparison = analyzer.compare_model_results(results)
print(comparison)
```

---

## 🔧 Phase 7: Update `__init__.py`

### Task 7.1: Fix Import in Root `__init__.py`
**File:** `projects/pipeline-safety-ai-evaluator/src/__init__.py`

The `__init__.py` tries to import from `.models.ai_interface` which doesn't exist. Update to include proper imports once models are created, or add placeholder that won't break imports.

Current problematic line 15:
```python
from .models.ai_interface import AIModelInterface
```

Either:
- Option A: Create the models module (preferred - Task 1.1)
- Option B: Comment out until models module exists

---

## 🚀 Phase 8: CI/CD and Workflows

### Task 8.1: Create `.github/workflows/ci.yml`
**File:** `projects/pipeline-safety-ai-evaluator/.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e .
    
    - name: Lint with flake8
      run: flake8 src tests
    
    - name: Format check with black
      run: black --check src tests
    
    - name: Type check with mypy
      run: mypy src
    
    - name: Test with pytest
      run: pytest tests/ --cov=psae --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## 📋 Task Summary Checklist

### Critical Path (Must Complete First)
- [x] Task 1.1: Create `src/models/ai_interface.py` (BLOCKING)
- [x] Task 1.2: Create `src/models/__init__.py` (BLOCKING)
- [x] Task 7.1: Fix `src/__init__.py` imports

### High Priority
- [x] Task 2.1: Create `configs/evaluation.yaml`
- [x] Task 2.2: Create `configs/models.yaml`
- [x] Task 5.1: Create `src/cli.py` (entry point referenced in setup.py)
- [x] Task 5.2: Create `src/utils/reporting.py`

### Medium Priority (Test Data)
- [x] Task 3.1: Create `data/test_cases/safety_critical.json`
- [x] Task 3.2: Create `data/test_cases/engineering.json`
- [x] Task 3.3: Create `data/test_cases/inspection.json`
- [x] Task 3.4: Create `data/test_cases/regulatory.json`
- [x] Task 3.5: Create `data/human_baseline/responses.json`

### Lower Priority (Testing & Documentation)
- [x] Task 4.1-4.5: Testing infrastructure
- [x] Task 6.1-6.3: Documentation
- [x] Task 8.1: CI/CD workflow

---

## 🧪 Verification Commands

Once complete, verify with:

```bash
# Install package
pip install -e .

# Test imports
python -c "from psae import PipelineSafetyEvaluator; print('✓ Imports work')"

# Test CLI
psae --version
psae list-tests

# Run tests
pytest tests/ -v

# Run evaluation (requires API key)
psae evaluate --model gpt-4 --suite safety --runs 5

# Validate benchmark manifest integrity
psae validate-benchmark
```

---

## 📝 Notes for Cursor

1. **File paths are relative to:** `projects/pipeline-safety-ai-evaluator/`

2. **Existing completed code:**
   - `src/core/evaluator.py` - Main evaluation engine (COMPLETE)
   - `src/core/metrics.py` - Metric calculation (COMPLETE)
   - `src/core/statistical.py` - Statistical analysis (COMPLETE)
   - `src/scenarios/base.py` - JSON-backed suite loading + built-in fallback (COMPLETE)
   - `src/models/` - AI interfaces and wrappers (COMPLETE)
   - `src/cli.py` - CLI commands (`evaluate`, `compare`, `validate-config`, `list-tests`, `validate-benchmark`) (COMPLETE)
   - `src/utils/reporting.py` - Multi-format report generation with schema metadata (COMPLETE)
   - `data/benchmark_manifest.json` - Benchmark checksum manifest (COMPLETE)

3. **Key architectural decisions:**
   - Follow the existing dataclass patterns in `evaluator.py`
   - Use the Abstract Base Class pattern for AI model interfaces
   - Maintain type hints throughout (Python 3.10+)
   - Follow PEP 8 (Black code style)

4. **Test data:** The existing test cases in `base.py` should be extracted to JSON files as the source of truth. Eventually `base.py` could load from these JSON files.

5. **Environment:** Python 3.10+, see `requirements.txt` for dependencies.
