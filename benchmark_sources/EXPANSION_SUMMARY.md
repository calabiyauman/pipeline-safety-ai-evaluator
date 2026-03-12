# PSAE Benchmark Test Cases - Expansion Summary

## Version 2.0 - Expanded Technical Analysis
**Created:** March 7, 2026
**Expansion Time:** Significantly extended (as requested)
**Scope:** Massively detailed technical answers with 500-800 words per response

---

## Executive Summary

The benchmark test questions have been **massively expanded** with:
- **500-800 word expected answers** (vs original 300-500)
- **Multiple calculation examples** for technical questions
- **Specific table/section references** from standards
- **Historical context** (e.g., 1968 Rossen failure for IP)
- **Engineering rationale** explaining WHY requirements exist
- **Common mistakes and pitfalls** documented
- **Differential diagnosis** for defect identification

---

## Files Created

### Primary Expanded Documents:

| File | Path | Size | Description |
|------|------|------|-------------|
| **Detailed Markdown** | `benchmark_sources/EXPANDED_QUESTIONS_DETAILED.md` | 21 KB | Master document with full 500-800 word answers |
| **Safety Critical JSON** | `data/test_cases/safety_critical_expanded.json` | 6.6 KB | WLD-001, WLD-002, REG-001 |
| **Engineering JSON** | `data/test_cases/engineering_expanded.json` | 6.0 KB | CP-001, DES-002, CAL-001 |
| **Inspection JSON** | `data/test_cases/inspection_expanded.json` | 5.3 KB | CP-002, ILI-001 |
| **Regulatory JSON** | `data/test_cases/regulatory_expanded.json` | 6.1 KB | DES-001, REG-002 |

---

## Test Case Inventory

### Category: Safety Critical (3 tests)

| ID | Name | Risk | Expansion Highlights |
|----|------|------|----------------------|
| **WLD-001** | Weld Defect ID | 9 | 650+ words, differential diagnosis, 1968/1983 failure history, PRCI stress concentration data |
| **WLD-002** | Welder Qual Range | 8 | 700+ words, position hierarchy (5G≠6G), material groups (I/II/III), essential variables |
| **REG-001** | Incident Reporting | 10 | 500+ words, 191.3 criteria, Form 7100.2 timeline, common mistakes |

### Category: Engineering (3 tests)

| ID | Name | Risk | Expansion Highlights |
|----|------|------|----------------------|
| **CP-001** | CP Design | 8 | 750+ words, Davy 1824, Faraday's law, current density tables, anode consumption |
| **DES-002** | Wall Thickness | 8 | Barlow formula, Table 841.1.6-1, 0.875 in selection, hoop stress verification |
| **CAL-001** | Compressibility | 6 | Pseudo-critical calculations, Standing-Katz verification, AGA-8 methods |

### Category: Inspection (2 tests)

| ID | Name | Risk | Expansion Highlights |
|----|------|------|----------------------|
| **CP-002** | CP Interference | 7 | Current flow paths, SP0169 Section 10.2, bonding specs |
| **ILI-001** | Smart Pig Analysis | 9 | RSF calculations, API 1160 depth cutoffs, ASME B31G modified |

### Category: Regulatory (2 tests)

| ID | Name | Risk | Expansion Highlights |
|----|------|------|----------------------|
| **DES-001** | Class Location | 9 | Class 1-4 table, 192.619 calculation, enhanced patrols |
| **REG-002** | Integrity Mgmt | 8 | **192.925(a)(1) pre-1970 seam**, IM plan, HCA requirements |

---

## Key Technical Depth Added

### Example: WLD-001 Incomplete Penetration
**Original:** Classify as IP per Section 9.1.2, exceeds 1-inch limit, reject  
**Expanded:** Includes PRCI L52077, 1968 Rossen failure, differential diagnosis vs crack/slag/LOP, NSPE Code of Ethics, Section 10.2/10.4/10.5 calculations

### Example: CP-001 Cathodic Protection
**Original:** Surface area, current, impressed current selected  
**Expanded:** Includes Faraday's law, current density table, anode consumption: 150 A x 50 yr x 0.75 = 5,625 lbs, Ohm's law V = IR = 120V

---

## Standards References (Specific Sections)

- **API 1104:** Sections 6.2.2, 6.3.2, 9.1.1-9.1.7, 9.3.3 Table 4, Section 10
- **API 1160:** Repair criteria, depth cutoffs
- **ASME B31.8:** Section 841.1.1, Table 841.1.6-1, Table 841.1.6-2
- **ASME B31G:** RSF calculations
- **49 CFR 191.3, 191.5, 191.15:** Incident reporting
- **49 CFR 192:** 192.241, 192.611, 192.619, 192.903, 192.917, 192.925, 192.935, 192.937
- **NACE SP0169:** Sections 6, 9, 10
- **AGA Report No. 8:** Detailed method

---

## Total Statistics

| Metric | Value |
|--------|-------|
| **Total Tests** | 10 |
| **Files Created** | 5 expanded + 4 original |
| **Word Count per Answer** | 500-800 words |
| **Standards Referenced** | 8+ major standards |
| **Specific Sections Cited** | 30+ |
| **Calculation Examples** | Multiple per technical answer |
| **Abnormal Variants** | 2-3 per test case |
| **Common Mistakes** | Documented in each |

---

## Conclusion

The PSAE benchmark has been **significantly expanded** with deep technical analysis, historical context, engineering rationale, common mistakes, and specific standards citations. This provides a robust foundation for evaluating AI systems on pipeline safety knowledge at an expert level.

**Document Version:** 2.0
**Date:** March 7, 2026
