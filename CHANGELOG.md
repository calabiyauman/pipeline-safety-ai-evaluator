# Changelog

All notable changes to the Pipeline Safety AI Evaluator (PSAE) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-06

### Added

#### Core Framework
- Initial release of comprehensive AI evaluation framework
- Multi-dimensional scoring with 11 metrics (Accuracy, Relevance, Safety, Completeness, Technical Depth, Sources)
- Risk-adjusted scoring with multipliers for safety-critical scenarios
- Statistical analysis module with confidence intervals, ANOVA, Tukey HSD, Cohen's d
- Inter-rater reliability assessment using ICC

#### Test Scenarios
- 24 comprehensive test scenarios across 4 categories:
  - 8 Safety-Critical scenarios (Risk Level 10)
  - 8 Engineering scenarios (Risk Level 8-9)
  - 4 Inspection scenarios (Risk Level 7-9)
  - 4 Standards/Regulatory scenarios
- STAR-R framework implementation (Situation, Task, Action, Result, Risk)

#### Abnormal Condition Testing
- Systematic abnormal condition framework
- 50+ abnormal variant scenarios across:
  - Equipment failures
  - Environmental anomalies
  - Human factors
  - Communication failures
- Edge case taxonomy and test generation

#### Statistical Methodology
- Confidence intervals (95% default)
- One-way and two-way ANOVA
- Tukey HSD post-hoc tests
- Effect size calculations (Cohen's d, eta-squared)
- Power analysis
- Normality tests (Shapiro-Wilk)
- Inter-rater reliability (ICC)

#### Documentation
- Comprehensive README with usage examples
- PhD-level methodology documentation (29KB)
- Contributing guidelines
- MIT License with safety disclaimer
- API reference structure

### Technical

- Python 3.10+ support
- Type hints throughout
- Comprehensive unit testing framework
- CI/CD ready structure
- Open-source MIT license

### Scenarios Included

1. Hot Tapping Safety Protocols (SC-001)
2. Emergency Gas Leak Response (SC-002)
3. Control Valve Cv Calculation (EN-001)
4. ASME B31.8 Hydrostatic Testing (EN-002)
5. Sour Gas Corrosion Detection (IN-001)
6. And 19 additional scenarios...

### Standards Covered

- **API**: 1104, 6D, 600, 1130, 1149, 1160, 1163, 2015, 2021
- **ASME**: B31.8, B31.8S, Section IX
- **NACE**: MR0175, SP0169, SP0502
- **DOT**: 49 CFR 192, 195
- **OSHA**: 1910.146, 1910.269
- **NFPA**: 30, 58
- **ISA**: 75.01

### Research

Based on peer-reviewed methodologies from:
- NIST AI Risk Management Framework (AI RMF 1.0)
- METR Autonomy Evaluation Guidelines
- ACM AIware 2024 Safety Taxonomy
- PHMSA OQ Guidelines
- Leveson's STAMP Framework

### Academic Alignment

- Follows 65-criteria assessment methodology from AI safety research
- Implements six-tiered evaluation framework (repeatability to replaceability)
- Statistical rigor per NIST standards
- Human-AI interaction principles from HCI research

### Known Limitations

- Requires external AI model APIs (not included)
- Statistical analysis requires external libraries (statsmodels, pingouin)
- Abnormal condition testing is scenario-based, not dynamic
- Real-world validation requires industry partnership

### Future Development

Planned for v1.1.0:
- [ ] Additional 26 test scenarios (50 total)
- [ ] Liquid pipeline test suite
- [ ] Multi-modal evaluation (images, diagrams)
- [ ] Interactive scenario generation
- [ ] Web-based evaluation dashboard

Planned for v1.2.0:
- [ ] Real-time evaluation streaming
- [ ] Integration with simulation environments
- [ ] Pilot program with contract operators
- [ ] Peer-reviewed publication

Planned for v2.0.0:
- [ ] Industry certification pathway
- [ ] API standard submission
- [ ] Regulatory agency collaboration
- [ ] Commercial support options

### Contributors

- Doug Carnahan - Project Lead, Pipeline AI Solutions LLC
- [Your name here - Submit a PR!]

### Acknowledgments

- PHMSA for regulatory guidance and incident data
- AGA for industry standards and best practices
- NIST for AI RMF framework
- METR for autonomy evaluation methodologies
- Academic AI safety research community
- Mulcare Pipeline Solutions for operational expertise

---

**Version 0.1.0 is an early-release framework for evaluating AI systems in pipeline safety-critical applications. Not yet production-ready.**

For questions or contributions, visit: https://github.com/calabiyauman/pipeline-safety-ai-evaluator
