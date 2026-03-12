# Paper Criteria Alignment

## Purpose

Track implementation status against `PipelineAIEvalPaper2026` recommendations and provide a repeatable local readiness gate before final result publication.

## What Was Added

- Statistical output now explicitly includes:
  - `anova_by_category`
  - `tukey_hsd_by_category`
  - `normal_vs_abnormal_effect` (Cohen's d)
  - `icc_inter_rater`
- Added `paper` built-in suite profile:
  - `psae evaluate --suite paper --runs 5`
  - merges base + extended datasets with deduplication to target `8/8/4/4` minimum coverage.
- New readiness gate script:
  - `scripts/paper_readiness_check.py`
  - verifies:
    - `min_runs >= 5`
    - required statistical tests are configured (`anova`, `tukey_hsd`, `cohens_d`, `icc`)
    - paper core corpus target (`8/8/4/4`, total `24`)
    - benchmark manifest signature presence

## How To Run

- Human-readable:
  - `python scripts/paper_readiness_check.py --output markdown`
- Machine-readable:
  - `python scripts/paper_readiness_check.py --output json`
- CI/strict gate mode:
  - `python scripts/paper_readiness_check.py --strict`

## Notes

- This gate checks setup/readiness, not model quality outcomes.
- If corpus counts are below target, finalize dataset expansion first, then re-run this check before regenerating paper tables.
