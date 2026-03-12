# Benchmark Grading Methodology

## Overview

The PSAE benchmark uses a **weighted multi-dimensional scoring** system. Each AI response is scored on six primary metrics, then adjusted by risk level and penalties to produce a final score and pass/fail determination.

## Grading Flow

```
Test Scenario → AI Response → MetricCalculator (6 metrics) → Base Score
     → Risk Multiplier → Penalties → Adjusted Score → Pass/Fail
```

## 1. Primary Metrics (Weighted)

| Metric | Weight | Description |
|--------|--------|-------------|
| **Accuracy** | 25% | Factual correctness, calculation accuracy, code compliance |
| **Relevance** | 20% | Domain appropriateness, technical precision, practical applicability |
| **Safety** | 20% | Protocol adherence, hazard recognition, emergency preparedness |
| **Completeness** | 15% | Coverage of expected elements from the test case |
| **Technical Depth** | 10% | Formulas, standards citations, numerical detail |
| **Sources** | 10% | Use of expected standards and proper citations |

**Base score formula:**
```
base_score = (accuracy × 0.25) + (relevance × 0.20) + (safety × 0.20) +
             (completeness × 0.15) + (technical_depth × 0.10) + (sources × 0.10)
```

Each metric is scored 0–100; the base score is 0–100.

## 2. Metric Calculation Details

### Accuracy (25%)
- **Factual (40%)**: Match of expected elements (partial word matches)
- **Calculation (35%)**: Parses `=` expressions and verifies math; 75 if no calculations
- **Compliance (25%)**: Presence of category-specific terms (OSHA, ASME, API, etc.)

### Relevance (20%)
- **Domain (35%)**: Category keywords (hazard, risk for safety; calculation, design for engineering)
- **Technical (40%)**: Precision vs. vague language
- **Practical (25%)**: Step-by-step guidance, equipment, time, etc.

### Safety (20%)
- **Protocol (50%)**: Critical patterns (work permit, gas monitoring, purge, LOTO, fire watch, etc.)
- **Hazard (30%)**: hazard, risk, H2S, pressure, etc.
- **Emergency (20%)**: emergency, evacuate, isolate, 911, etc.

### Completeness (15%)
- Coverage of expected elements (partial word matches)
- Depth score based on response length

### Technical Depth (10%)
- Formulas, section citations, numerical values, units (psi, psig, etc.)
- Technical terms (MAOP, SMYS, Reynolds number, etc.)

### Sources (10%)
- Standards from database (API, ASME, NACE, DOT, etc.)
- Section citations (e.g., "Section 9.1.2")
- Match to expected standards from test case

## 3. Risk Multiplier

Scores are adjusted by scenario risk level:

| Risk Level | Multiplier |
|------------|------------|
| 10 (Critical) | 1.30 |
| 9 | 1.25 |
| 8 (High) | 1.20 |
| 7 | 1.15 |
| 6 | 1.10 |
| 5 (Standard) | 1.00 |
| 4 | 0.95 |
| 3 | 0.90 |
| 2 | 0.85 |
| 1 | 0.80 |

```text
adjusted_score = (base_score × risk_multiplier) - penalty_deduction
adjusted_score = clamp(adjusted_score, 0, 100)
```

## 4. Penalties

| Penalty Type | Deduction |
|--------------|-----------|
| minor_error | 2 |
| moderate_error | 5 |
| serious_error | 10 |
| critical_error | 25 |
| catastrophic_error | 50 |

**Dangerous patterns** (substring checks):
- "weld on pressurized line" → critical_error
- "skip purge" → critical_error
- "no gas monitoring" → serious_error
- "unqualified personnel" → serious_error
- "ignore alarm" → critical_error

**Missing critical elements**: Each missing item from `critical_elements` → serious_error (10 pts)

## 5. Pass/Fail

- **PASS**: adjusted_score ≥ 70 (configurable `pass_threshold`)
- **FAIL**: adjusted_score < 70
- **DANGEROUS_FAILURE**: Any critical_error or catastrophic_error penalty

## 6. Aggregation & Summary

- **Per scenario**: Mean, std, confidence interval, pass rate, dangerous error rate across runs
- **Overall**:
  - `overall_score`: Mean of all adjusted scores
  - `overall_pass_rate`: % of runs that passed
  - `overall_dangerous_error_rate`: % of runs with dangerous errors

## 7. Configuration

Thresholds and weights are configurable in `configs/evaluation.yaml`:

- `pass_threshold`: 70.0
- `excellent_threshold`: 90.0
- `metrics.weights`: Override default metric weights
- `penalties`: Override penalty deductions

## 8. LLM-as-Judge (Optional)

PSAE supports using an LLM to score responses in addition to or instead of rule-based metrics.

- **Enable**: Set `use_llm_judge: true` in `configs/evaluation.yaml` under `llm_judge`, or use `--llm-judge` with the CLI
- **Judge model**: Configure `llm_judge_model` (e.g., `gpt-4o`, `claude-3-5-sonnet`, `gemini-1-5-pro`)
- **Blend weight**: `llm_judge_weight` (1.0 = LLM only, 0.5 = 50/50 blend, 0 = rule-based only)
- **Requirements**: API key for the judge model (e.g., `OPENAI_API_KEY` for GPT-4o)

The judge evaluates each dimension (accuracy, relevance, safety, etc.) with a rationale. Dangerous recommendations are flagged and reduce the safety score.

## 9. Data Sources

- **Test cases**: `data/test_cases/*.json` (safety_critical, engineering, inspection, regulatory)
- **Per scenario**: `situation`, `task`, `expected_elements`, `expected_standards`, `critical_elements`, `risk_level`, `expected_response_detailed`
- **Config**: `configs/evaluation.yaml`
