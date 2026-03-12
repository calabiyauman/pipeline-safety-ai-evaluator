# Category-Based Scoring

## Overview

The PSAE evaluator computes grades per category (safety, engineering, inspection, regulatory) and then combines them into a single final score. This makes it easy to see performance by domain and to weight categories differently if desired.

## How It Works

1. **Per-category scores**: For each category present in the run, the mean of all evaluation scores in that category is computed.
2. **Combination**: The final score is the weighted average of category scores. If `category_weights` is configured, those weights are used; otherwise categories are weighted equally.
3. **Output**: The summary includes:
   - `category_scores`: `{ "safety": 85.2, "engineering": 78.1, ... }`
   - `overall_score`: the combined final score
   - Individual `safety_score`, `engineering_score`, `inspection_score`, `regulatory_score` for backward compatibility

## Configuration

### Equal weighting (default)

If `category_weights` is omitted, each category present in the run contributes equally:

```
Final = mean(safety_score, engineering_score, inspection_score, regulatory_score)
```

### Custom weights

Add `category_weights` to `configs/evaluation.yaml`:

```yaml
category_weights:
  safety: 0.35
  engineering: 0.25
  inspection: 0.20
  regulatory: 0.20
```

Weights are normalized across categories present in the run. Categories not listed use weight 1.0.

## Reports

- **HTML**: "Category Grades (combined for final score)" table shows each category score; "Final Score" in Executive Summary is the combined value.
- **Markdown**: "Category Grades" section lists per-category scores; "Final Score (combined from categories)" in Summary.
- **JSON**: `summary.category_scores` and `summary.overall_score` contain the breakdown and final value.
