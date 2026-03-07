# Extracted Test Questions for PSAE Integration

## Overview
This document contains specific test questions extracted or developed from the research sources. These questions are ready to be formatted into the PSAE JSON test case format.

## API 1104 Welding Questions

### Question 1: Weld Defect Identification
**Test ID**: WLD-001
**Category**: inspection
**Risk Level**: 9

**Scenario**:
A radiographic inspection of a pipeline girth weld reveals the following indications:
- Elongated indication: 1.5 inches long, parallel to weld axis
- Location: Center of weld, near root
- Density: Darker than surrounding weld metal

**Task**:
Classify the defect per API 1104 acceptance criteria and determine if the weld is acceptable.

**Expected Elements**:
- Defect classification (crack, incomplete penetration, slag, etc.)
- Reference to API 1104 acceptance tables
- Length limitations per code
- Repair requirements if rejected

**Critical Elements**:
- Crack identification (automatic reject)
- API 1104 Section 9 reference
- Acceptance criteria application

**Standards**: API 1104, Section 9 (Acceptance Standards)

**Abnormal Variants**:
1. Multiple indications clustered in one area
2. Indication at weld toe (geometric issue)
3. Indication in repaired weld section

---

### Question 2: Welder Qualification Range
**Test ID**: WLD-002
**Category**: safety
**Risk Level**: 8

**Scenario**:
A welder is qualified on API 5L Grade X52, 12-inch diameter, 0.375-inch wall thickness pipe in the 5G position using E6010 root and E7018 fill passes.

**Task**:
Determine the qualification range (diameter, wall thickness, position, material grade) for this welder per API 1104.

**Expected Elements**:
- Diameter range qualification
- Wall thickness range
- Position qualifications
- Material group limitations
- Essential variables that require requalification

**Critical Elements**:
- Essential variables identification
- Position limitations
- Material group requirements

**Standards**: API 1104, Section 6 (Welder Qualification)

---

## NACE/AMPP Cathodic Protection Questions

### Question 3: CP System Design
**Test ID**: CP-001
**Category**: engineering
**Risk Level**: 8

**Scenario**:
A new 15-mile coated pipeline requires cathodic protection design:
- Diameter: 16 inches
- Coating: Fusion-bonded epoxy (excellent quality)
- Soil resistivity: 3,000 ohm-cm (average)
- Adjacent structures: None

**Task**:
Design a cathodic protection system including:
1. Current requirement calculation
2. Groundbed type selection (galvanic vs. impressed current)
3. Rectifier sizing (if impressed current)
4. Anode selection and quantity

**Expected Elements**:
- Surface area calculation
- Current density selection (1-3 mA/m² for FBE)
- Total current requirement
- Groundbed design calculations
- Attenuation considerations

**Critical Elements**:
- Current requirement calculation
- Groundbed design
- NACE SP0169 criteria reference

**Standards**: NACE SP0169, Peabody's Control of Pipeline Corrosion

---

### Question 4: Interference Testing
**Test ID**: CP-002
**Category**: inspection
**Risk Level**: 7

**Scenario**:
Two pipelines share a common corridor:
- Pipeline A: Has impressed current CP system, potential -1,100 mV
- Pipeline B: No CP system, potential -650 mV (native)
- Pipeline B shows accelerated corrosion near crossing with Pipeline A

**Task**:
Diagnose the problem and recommend mitigation measures.

**Expected Elements**:
- DC interference identification
- Current flow direction determination
- Mitigation options (bonding, drainage, etc.)
- Testing procedures to confirm

**Critical Elements**:
- DC interference recognition
- Mitigation strategy
- Safety considerations

**Standards**: NACE SP0169, Section 10

---

## ASME B31.8 Design Questions

### Question 5: Class Location Change
**Test ID**: DES-001
**Category**: regulatory
**Risk Level**: 9

**Scenario**:
A natural gas transmission pipeline was constructed in 1985:
- Original class location: Class 1
- Original MAOP: 1,000 psig
- Original test pressure: 1,250 psig
- Current class location: Class 3 (due to development)

**Task**:
Determine the required actions per ASME B31.8 and 49 CFR 192.

**Expected Elements**:
- MAOP verification requirements
- Pressure reduction calculation
- Re-testing requirements
- Documentation needs
- Timeline for compliance

**Critical Elements**:
- Class location change implications
- MAOP determination per 192.619
- Safety margin assessment

**Standards**: ASME B31.8, 49 CFR 192.611, 192.619

---

### Question 6: Wall Thickness Verification
**Test ID**: DES-002
**Category**: engineering
**Risk Level**: 8

**Scenario**:
Design a new natural gas pipeline:
- Material: API 5L Grade X70
- Diameter: 42 inches
- MAOP: 1,440 psig
- Class location: Class 2
- Temperature: 100°F

**Task**:
Calculate the minimum required wall thickness per ASME B31.8.

**Expected Elements**:
- Barlow's formula application
- Design factor selection (F = 0.60 for Class 2)
- Temperature derating factor
- Corrosion allowance consideration
- Commercial wall thickness selection

**Critical Elements**:
- Correct formula application
- Design factor selection
- SMYS value for X70 (70,000 psi)

**Standards**: ASME B31.8, Section 841.1

---

## PHMSA Regulatory Questions

### Question 7: Incident Reporting
**Test ID**: REG-001
**Category**: regulatory
**Risk Level**: 10

**Scenario**:
A pipeline incident occurs at 14:30 on Friday:
- 20-inch natural gas transmission line rupture
- Fire occurred
- 1 worker injured (hospitalized)
- 50 homes evacuated
- Gas flow isolated at 15:45

**Task**:
Determine the incident reporting requirements per 49 CFR 191.

**Expected Elements**:
- Immediate notification requirements (911, NRC)
- Written report timelines
- Report type (Form RSPA F 7100.1, 7100.2)
- Information required in reports
- Follow-up reporting requirements

**Critical Elements**:
- Immediate notification within 1 hour
- Written report within 30 days
- NRC notification requirements

**Standards**: 49 CFR 191.5, 191.15, 191.29

---

### Question 8: Integrity Management Assessment
**Test ID**: REG-002
**Category**: inspection
**Risk Level**: 8

**Scenario**:
A gas transmission pipeline in an HCA has the following threats identified:
- External corrosion: Moderate (coating damage observed)
- Internal corrosion: Low (dry gas)
- Third-party damage: High (construction activity nearby)
- Manufacturing defects: Unknown (pre-1970 pipe)

**Task**:
Develop an integrity assessment plan per 49 CFR 192, Subpart O.

**Expected Elements**:
- Assessment method selection for each threat
- Priority of assessments
- Timeline requirements
- Follow-up assessment intervals
- Risk mitigation measures

**Critical Elements**:
- Threat-specific assessment methods
- HCA requirements
- Baseline assessment deadlines

**Standards**: 49 CFR 192.917, 192.925, 192.937

---

## AGA Gas Calculations

### Question 9: Compressibility Factor
**Test ID**: CAL-001
**Category**: engineering
**Risk Level**: 6

**Scenario**:
Calculate gas properties for:
- Gas: Natural gas (95% methane, specific gravity 0.6)
- Pressure: 1,000 psig
- Temperature: 80°F
- Pipeline: 24-inch, 50 miles long

**Task**:
Calculate the compressibility factor (Z) using AGA Report No. 8 and determine the actual gas volume at operating conditions.

**Expected Elements**:
- Pseudo-critical property calculations
- Reduced temperature and pressure
- Compressibility factor determination
- Real gas law application

**Critical Elements**:
- AGA Report No. 8 method
- Pseudo-critical calculations
- Unit consistency

**Standards**: AGA Report No. 8

---

## General Pipeline Questions

### Question 10: Smart Pig Data Analysis
**Test ID**: ILI-001
**Category**: inspection
**Risk Level**: 9

**Scenario**:
An MFL inspection reports the following metal loss features:
- Feature A: 20% wall loss, 3 inches long, external, general corrosion
- Feature B: 50% wall loss, 1 inch long, external, pitting
- Feature C: 40% wall loss, 6 inches long, internal, general corrosion

**Task**:
Prioritize repairs per API 1160 and determine response timelines.

**Expected Elements**:
- Severity assessment (depth, length, location)
- Burst pressure calculations
- Remaining strength factor
- Repair categories and timelines
- Re-inspection intervals

**Critical Elements**:
- Severity ranking
- API 1160 repair criteria
- Safety factor application

**Standards**: API 1160, API 1163

---

## Abnormal Condition Variants

Each question should have 2-3 abnormal condition variants:

### Example for Question 1 (Weld Defect):
1. **Equipment Failure**: Radiography equipment malfunction - only partial film available
2. **Time Pressure**: Weld must be accepted to maintain schedule (production pressure)
3. **Environmental**: Rain/wind making re-inspection difficult

### Example for Question 3 (CP Design):
1. **Soil Anomaly**: Encountered low resistivity soil (500 ohm-cm) in one section
2. **Interference**: New adjacent pipeline with existing CP system
3. **Access Issue**: Property owner denies access for groundbed installation

### Example for Question 7 (Incident Reporting):
1. **Communication Failure**: Phone systems down, no immediate way to contact NRC
2. **Multiple Incidents**: Second smaller leak discovered during response
3. **Media Presence**: News crews on scene asking for information

## JSON Format Template

```json
{
  "test_id": "WLD-001",
  "name": "Weld Defect Identification",
  "category": "inspection",
  "risk_level": 9,
  "situation": "A radiographic inspection of a pipeline girth weld reveals...",
  "task": "Classify the defect per API 1104 acceptance criteria...",
  "expected_elements": [
    "Defect classification",
    "API 1104 acceptance tables reference",
    "Length limitations",
    "Repair requirements"
  ],
  "expected_standards": ["API 1104"],
  "critical_elements": [
    "Crack identification",
    "API 1104 Section 9 reference",
    "Acceptance criteria application"
  ],
  "abnormal_variants": [
    {
      "description": "Multiple indications clustered in one area",
      "impact": "May indicate systematic welding issue",
      "type": "system"
    }
  ],
  "validation_notes": "Critical inspection test - proper defect classification is essential for pipeline safety"
}
```

## Next Steps

1. Convert these questions to official PSAE JSON format
2. Develop human expert baseline responses
3. Create scoring rubrics for each question
4. Add abnormal condition variants
5. Validate with subject matter experts
6. Test with AI models to establish baseline scores
