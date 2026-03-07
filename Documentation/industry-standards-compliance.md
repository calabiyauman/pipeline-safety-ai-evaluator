# PSAE Industry Standards Compliance

## Scope
This checklist tracks implementation alignment with industry expectations for AI evaluation and benchmark tooling in safety-critical contexts.

## Controls and Status

- [x] **Secure metric computation**
  - Removed unsafe dynamic code execution in calculation checks.
  - Implemented safe arithmetic parser for equation verification.

- [x] **Statistical output in evaluator**
  - Replaced placeholder statistical block with computed outputs:
    - descriptive statistics
    - normality test
    - category ANOVA (when sample sufficiency is met)
    - normal vs. abnormal effect size

- [x] **Configuration contract normalization**
  - Added support for nested config schema (`evaluation`, `metrics.weights`, `penalties`, `scenarios`) and flat schema.
  - Added stronger CLI config validation for metric weight normalization.

- [x] **Benchmark governance baseline coverage**
  - Human baseline file now includes all test IDs in the benchmark corpus.
  - Added automated test to verify complete ID coverage.

- [x] **Reproducibility artifacts**
  - Added run manifest fields in evaluation output (Python version, platform, scenario/runs metadata).

- [x] **Quality gates**
  - Added CI workflow to run linting and test suite on push/PR.

- [ ] **Independent factual verification backend**
  - Current scoring remains heuristic/lexical in several dimensions.
  - Future work: integrate expert adjudication model, retrieval-based verifier, or rubric grading pipeline with calibrated ground truth.

- [x] **Formal benchmark versioning and immutability controls (baseline)**
  - Added benchmark checksum manifest (`data/benchmark_manifest.json`) and validation utility/tests.
  - Added manifest signing and signature verification workflow (`sign-benchmark`, `verify-benchmark-signature`).
  - Remaining future work: signed release artifacts and key-rotation policy automation.

## Validation Evidence

- Full tests pass locally (`pytest tests -q`).
- Governance test included:
  - `tests/unit/test_benchmark_governance.py`

## Next Actions

1. Add benchmark checksum manifest and validation command.
2. Add adjudication/rubric calibration pipeline for factual correctness.
3. Expand report templates with confidence intervals and significance tables by default.
