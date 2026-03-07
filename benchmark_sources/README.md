# Pipeline Safety AI Evaluator - Benchmark Test Sources

## Overview
This folder contains research and resources for developing benchmark test questions for the Pipeline Safety AI Evaluator (PSAE). The sources are organized by certification body and regulatory authority.

## Folder Structure

```
benchmark_sources/
├── AGA/           # American Gas Association resources
├── API/           # American Petroleum Institute certifications
├── NACE_AMPP/     # Corrosion and materials protection
├── ASME/          # ASME B31.8 and related codes
├── PHMSA/         # DOT regulations (49 CFR 192)
├── General/       # Cross-cutting industry topics
└── README.md      # This file
```

## Quick Reference by Certification Body

| Organization | Primary Standard | Certification Programs | Key Topics |
|--------------|------------------|------------------------|------------|
| **AGA** | AGA Report No. 8, ANSI GPTC | Gas safety, distribution | Gas calculations, distribution systems |
| **API** | API 1104, 1169, 1110 | API 1169, 1184, 570, 510 | Welding, inspection, pressure testing |
| **NACE/AMPP** | SP0169, MR0175 | CP 1-4, CT, PCIM | Corrosion, cathodic protection |
| **ASME** | B31.8, B31.8S | N/A (code body) | Design, construction, testing |
| **PHMSA** | 49 CFR 192 | N/A (regulator) | Compliance, safety, integrity management |

## Test Question Inventory

### Safety-Critical Tests (Risk Level 10)
1. Hot Tapping Safety Protocols (API 1104, OSHA 1910.269)
2. Emergency Gas Leak Response (DOT 49 CFR 192.615)
3. Confined Space Entry (OSHA 1910.146)
4. Excavation Near Pipeline (DOT 49 CFR 192.614)
5. Valve Operation Under Pressure (API 6D)
6. Compressor Station Emergency Shutdown (API 618)
7. Fire at Pipeline Facility (NFPA 30)
8. Sour Gas Release Response (H2S contingency)

### Engineering-Critical Tests (Risk Level 8-9)
1. Control Valve Cv Calculation (ISA-75.01)
2. ASME B31.8 Hydrostatic Testing (ASME B31.8)
3. Sour Gas Material Selection (NACE MR0175)
4. Natural Gas Flow Calculation (AGA Report No. 8)
5. Cathodic Protection Design (NACE SP0169)
6. Pipeline Stress Analysis (ASME B31.8)
7. Leak Detection System Design (API 1130)
8. Compressor Sizing (API 618)

### Inspection-Critical Tests (Risk Level 7-9)
1. Sour Gas Corrosion Detection (API 1160)
2. Smart Pigging Data Analysis (API 1163)
3. External Corrosion Assessment (NACE SP0502)
4. Weld Inspection Protocols (API 1104)

### Regulatory & Standards Tests (Risk Level 5-6)
1. API Valve Standards Comparison (API 6D, 600, 608)
2. PHMSA Compliance Assessment (49 CFR 192)
3. O&M Manual Development (49 CFR 192.605)
4. MAOP Verification (49 CFR 192.619)

## Priority Sources for Question Development

### High Priority (Immediate Use)
1. **API 1169 Body of Knowledge** - Comprehensive pipeline construction inspection
2. **NACE CP 2-4 Exam Prep Guides** - Cathodic protection scenarios
3. **ASME B31.8 Flashcards** - 52 questions on gas pipeline code
4. **PHMSA OQ FAQs** - Operator qualification scenarios
5. **API 1104 Study Guide** - Welding questions and scenarios

### Medium Priority (Next Phase)
1. **API 1110** - Pressure testing procedures
2. **NACE PCIM** - Pipeline corrosion integrity management
3. **ASME B31.8 Training Materials** - Design and construction
4. **PHMSA Gas IM FAQs** - Integrity management scenarios
5. **AGA Report No. 8** - Gas calculations

### Lower Priority (Future Expansion)
1. **API 1163** - ILI qualification
2. **API 1160** - Managing system integrity
3. **NACE Internal Corrosion** - Internal corrosion technologist
4. **General Industry Resources** - Pigging, flow assurance

## Sample Question Templates

### Template 1: Calculation-Based
```
Scenario: [Technical parameters provided]
Task: [Calculation or sizing requirement]
Expected Elements:
- Formula application
- Unit conversions
- Safety factors
- Code references
Standards: [Applicable codes]
```

### Template 2: Procedure Development
```
Scenario: [Operational situation]
Task: [Develop procedure or response plan]
Expected Elements:
- Step-by-step actions
- Safety considerations
- Regulatory requirements
- Documentation needs
Standards: [Applicable codes]
```

### Template 3: Compliance Assessment
```
Scenario: [Inspection or audit finding]
Task: [Assess compliance and recommend actions]
Expected Elements:
- Regulatory citations
- Acceptance criteria
- Corrective actions
- Timeline requirements
Standards: [Applicable regulations]
```

## Structured Authoring Assets

To keep question/answer additions consistent and machine-validated:

- `question_bank.schema.json` - canonical schema for standards-linked question entries
- `question_bank.template.json` - starter template for new entries
- `QUESTION_AUTHORING_GUIDE.md` - field guidance and conversion workflow

Recommended process:

1. Draft using `question_bank.template.json`
2. Validate against `question_bank.schema.json`
3. Convert approved entries into runtime test cases in `data/test_cases/*.json`

You can also run evaluation directly from this folder:

```bash
psae evaluate --model gpt-4 --suite benchmark-sources --runs 5
```

The loader scans `benchmark_sources/` recursively and automatically picks up newly added:
- JSON question files
- Markdown question blocks using `### Question N: ...` format

## Integration Checklist

To integrate these sources into PSAE:

- [ ] Extract specific questions from API 1169 BOK
- [ ] Convert NACE CP exam prep scenarios to STAR-R format
- [ ] Adapt ASME B31.8 flashcards to AI evaluation format
- [ ] Develop PHMSA regulatory compliance scenarios
- [ ] Create abnormal condition variants for each test case
- [ ] Define expected_elements and critical_elements for each test
- [ ] Assign risk levels and standards references
- [ ] Create human expert baseline responses
- [ ] Validate questions with subject matter experts
- [ ] Add to JSON test case files

## Contact Information for Official Materials

### API
- Website: https://www.api.org
- ICP Program: https://www.api.org/icp
- Standards: https://www.api.org/standards

### NACE/AMPP
- Website: https://www.ampp.org
- Certification: https://www.ampp.org/education/certification

### ASME
- Website: https://www.asme.org
- Codes & Standards: https://www.asme.org/codes-standards

### PHMSA
- Website: https://www.phmsa.dot.gov
- Pipeline Safety: https://www.phmsa.dot.gov/pipeline

### AGA
- Website: https://www.aga.org
- Standards: https://global.ihs.com/standards.cfm?publisher=AGA

## License and Copyright Notes

- API standards and exam materials are copyrighted
- ASME codes require purchase or subscription
- PHMSA regulations are public domain (federal government)
- NACE/AMPP materials are copyrighted
- This research compiles publicly available information and links
- Official test questions should be obtained through proper channels

## Research Timestamp

- **Search Date**: March 7, 2026
- **Researcher**: Sterling (Pipeline AI Solutions)
- **Purpose**: PSAE benchmark test development
- **Next Review**: Quarterly or when standards are updated
