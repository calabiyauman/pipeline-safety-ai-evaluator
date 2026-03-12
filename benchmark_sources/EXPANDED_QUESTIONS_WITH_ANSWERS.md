# Expanded Pipeline Safety Benchmark Test Cases

## Executive Summary

This document contains expert-level expanded test questions for the Pipeline Safety AI Evaluator (PSAE) system. Each test case includes detailed technical scenarios, comprehensive expected answers, scoring rubrics, and abnormal condition variants to thoroughly evaluate AI systems on pipeline safety and engineering knowledge.

**Document Version:** 1.0  
**Created:** March 7, 2026  
**Total Tests:** 10 (organized in 4 category files)

---

## Test Case Inventory

| Test ID | Name | Category | Risk Level | Status |
|---------|------|----------|------------|--------|
| WLD-001 | Weld Defect Identification | Inspection | 9 | ✅ Complete |
| WLD-002 | Welder Qualification Range | Safety | 8 | ✅ Complete |
| CP-001 | CP System Design | Engineering | 8 | ✅ Complete |
| CP-002 | CP Interference Testing | Inspection | 7 | ✅ Complete |
| DES-001 | Class Location Change | Regulatory | 9 | ✅ Complete |
| DES-002 | Wall Thickness Calculation | Engineering | 8 | ✅ Complete |
| REG-001 | Incident Reporting | Regulatory | 10 | ✅ Complete |
| REG-002 | Integrity Management Plan | Regulatory | 8 | ✅ Complete |
| CAL-001 | Compressibility Factor | Engineering | 6 | ✅ Complete |
| ILI-001 | Smart Pig Data Analysis | Inspection | 9 | ✅ Complete |

---

## Test Case 1: WLD-001 - Weld Defect Identification

### Basic Information
- **Test ID:** WLD-001
- **Name:** Weld Defect Identification
- **Category:** inspection
- **Subcategory:** radiographic_testing
- **Risk Level:** 9 (Critical)
- **Difficulty:** advanced
- **Time Limit:** 15 minutes

### Detailed Situation

A radiographic inspection of a pipeline girth weld on a 20-inch API 5L Grade X65 pipeline reveals an elongated indication. The pipeline is part of a natural gas transmission system operating at 1,000 psig MAOP. The radiographic film shows: an elongated indication 1.5 inches (38.1 mm) in length, oriented parallel to the weld axis, located at the centerline of the weld near the root area, appearing darker than surrounding weld metal with a well-defined linear character. The weld is 0.500-inch wall thickness, double-welded butt joint. Adjacent examination shows no other significant indications. The project is on a critical path with significant delay costs, and there is pressure from construction management to accept the weld provisionally pending operational monitoring.

### Task

Classify the defect type per API 1104 acceptance criteria, determine weld acceptability, specify repair requirements if rejected, and provide professional recommendations considering safety versus schedule pressures.

### Comprehensive Expected Answer

Based on the radiographic indication described, this defect must be classified as **INCOMPLETE PENETRATION (IP)** per API 1104 Section 9.1.2.

**Defect Classification Analysis:**

Per API 1104 Section 9.1.2, incomplete penetration is defined as "the failure of the weld filler metal to fuse completely through the joint thickness of the pipe wall." The described indication aligns with this definition based on:

1. **Geometric Characteristics:** Linear orientation parallel to weld axis (API 1104 9.1.2(a))
2. **Location:** Root area at centerline where root pass penetration should occur
3. **Radiographic Appearance:** Darker density indicating absence of metal compared to surrounding weld

**Differential Diagnosis:**

- NOT Slag Inclusion: Slag appears more irregular, less linear
- NOT Porosity: Porosity appears as rounded spots, not continuous linear
- NOT Crack: Cracks have jagged/branching with sharp ends; this lacks those characteristics
- NOT LOP: LOP occurs at sidewalls between passes, not root-centerline

**Acceptance Determination:**

Per API 1104 Table 4 (Section 9.3.3) for incomplete penetration:
- **Maximum allowable IP length:** 1 inch (25.4 mm) in any 12-inch weld length
- **Indication length observed:** 1.5 inches (38.1 mm)

**CONCLUSION: WELD IS REJECTED** - The 1.5-inch indication exceeds the 1-inch maximum allowable.

**Repair Requirements per API 1104 Section 10:**

1. Complete removal of defect: Grind or gouge out to sound metal
2. Preparation: Minimum 30° included groove angle per Section 10.3
3. Re-welding: Use qualified welders and procedures per Section 6
4. Re-inspection: 100% radiographic or ultrasonic inspection
5. Minimum repair length: 2 inches (50 mm)

**Professional Recommendation:**

**DO NOT ACCEPT THIS WELD under any provisional arrangement.** Incomplete penetration represents a through-thickness discontinuity that can act as a stress concentrator under cyclic pressure loading. The pressure to maintain schedule must not override safety requirements per 49 CFR 192.

### Scoring Rubric

| Element | Points | Description |
|---------|--------|-------------|
| Defect Classification | 25 | Correct identification as Incomplete Penetration |
| Standard Reference | 20 | Accurate citation of API 1104 Section 9.1.2 and Table 4 |
| Acceptance Analysis | 25 | Correct application of 1-inch maximum and rejection |
| Repair Requirements | 15 | Proper repair procedure per Section 10 |
| Safety/Ethics | 15 | Clear statement about not accepting non-conforming welds |
| **Total** | **100** | |

### Critical Elements
1. Incomplete Penetration correctly identified
2. API 1104 Section 9 reference
3. Acceptance criteria correctly applied (1" max vs 1.5" actual)
4. Weld rejection stated clearly
5. Safety/regulatory compliance emphasized

### Abnormal Variants

**Variant 1: Multiple Indications**
- Multiple clustered defects suggest systematic failure
- May require cut-out rather than repair
- Welder re-qualification recommended

**Variant 2: Indication at Weld Toe**
- Changes to Incomplete Fusion with different acceptance limits
- 2-inch aggregate vs 1-inch for IP
- Stress concentration concern

**Variant 3: Repair of Previous Repair**
- Critical situation - API 1104 Section 10.4 applies
- Engineering assessment required
- Ethical pressure resistance demonstration needed

---

## Test Case 2: WLD-002 - Welder Qualification Range

### Basic Information
- **Test ID:** WLD-002
- **Name:** Welder Qualification Range Determination
- **Category:** safety
- **Subcategory:** welder_qualification
- **Risk Level:** 8 (High)
- **Difficulty:** intermediate
- **Time Limit:** 12 minutes

### Detailed Situation

A welder has successfully completed qualification testing on API 5L Grade X52 pipe using the following parameters: Pipe diameter: 12 inches (NPS 12), Wall thickness: 0.375 inches, Welding position: 5G (horizontal fixed), Root pass: E6010 electrode, Fill and cap passes: E7018 electrode, Welding process: SMAW (Shielded Metal Arc Welding), Progression: Uphill.

### Task

Determine the complete qualification range and identify what changes would require re-qualification per API 1104 Section 6.

### Comprehensive Expected Answer

## Qualification Range per API 1104 Section 6

### Diameter Qualification Range

Per API 1104 Section 6.2.2.1:
- **Qualified on:** NPS 12 (12.75-inch OD)
- **Qualification range:** NPS 2 and larger (for groove welds)
- **Explanation:** API 1104 allows welding on any diameter equal to or larger than qualification test diameter

### Wall Thickness Qualification Range

Per API 1104 Section 6.2.2.2:
- **Qualified on:** 0.375 inch
- **Qualification range:** Unlimited (all thicknesses)
- **Explanation:** Groove weld qualification on any thickness qualifies for unlimited thickness

### Position Qualification Range

Per API 1104 Section 6.2.2.3:
- **Qualified in:** 5G position
- **Qualification range:** ALL positions except 6G
- **Important:** 5G qualifies 5G, 2G, 1G; 6G requires separate qualification

### Material Grade Qualification Range

Per API 1104 Section 6.2.2.4:
- **Qualified on:** API 5L Grade X52 (Group II)
- **Qualification range:** Group I and Group II materials
- **Re-qualification required for:** Group III (X70, X80, etc.)

### Electrode Classification Range

- **Root:** E6010 (F-3 group) - qualified for any cellulosic electrode
- **Fill:** E7018 (F-4 group) - qualified for any low-hydrogen electrode

### Essential Variables Requiring Re-Qualification

Per API 1104 Section 6.3.2:
1. Material Group change to Group III
2. Position change to 6G
3. Process change (SMAW to GMAW, etc.)
4. **Progression change: Uphill to Downhill** (critical - requires re-qual)

### Summary Table

| Variable | Qualified | Range | Re-Qual Required |
|----------|-----------|-------|-----------------|
| Diameter | NPS 12 | NPS 12+ | NPS < 12 |
| Thickness | 0.375 in | Unlimited | None |
| Position | 5G | All except 6G | 6G |
| Material | X52 | Group I & II | Group III |
| Process | SMAW | SMAW only | Other processes |
| Progression | Uphill | Uphill only | **Downhill** |

### Scoring Rubric

| Element | Points | Description |
|---------|--------|-------------|
| Diameter | 15 | Correct NPS 12+ qualification |
| Thickness | 10 | Unlimited qualification |
| Position | 20 | 5G covers all except 6G |
| Material | 20 | Group I & II, Group III requires re-qual |
| Electrode Groups | 15 | F-3 and F-4 groups correctly identified |
| Essential Variables | 20 | Progression, process, material changes |
| **Total** | **100** | |

### Abnormal Variants

**Variant 1: X70 Material Assignment**
- Group II to Group III change is essential variable
- Cannot use without re-qualification
- Regulatory violation if proceeded

**Variant 2: 6G Position Assignment**
- 5G does NOT cover 6G
- Separate qualification required
- Common misconception corrected

**Variant 3: Downhill Progression**
- Uphill to downhill is essential variable per 6.3.2(f)
- Re-qualification required
- Many companies prohibit downhill completely

---

## Test Case 3: CP-001 - Cathodic Protection System Design

### Basic Information
- **Test ID:** CP-001
- **Name:** Cathodic Protection System Design
- **Category:** engineering
- **Subcategory:** corrosion_control
- **Risk Level:** 8 (High)
- **Difficulty:** advanced
- **Time Limit:** 25 minutes

### Detailed Situation

A new 15-mile natural gas transmission pipeline requires cathodic protection design: 16-inch NPS diameter, Fusion-bonded epoxy coating (99% coverage), API 5L Grade X52 material, Soil resistivity: 3,000 ohm-cm average, pH 6.5-7.5, No adjacent structures, AC power available at 4-mile intervals, Design life: 50 years.

### Task

Design a complete cathodic protection system including current requirement, groundbed type, rectifier sizing, anode selection, and expected operating parameters per NACE SP0169.

### Comprehensive Expected Answer

## Cathodic Protection Design Analysis

### Step 1: Surface Area Calculation

Pipeline external surface area:
- Length: 15 miles = 79,200 feet
- Diameter: 16" OD = 1.333 ft
- **Surface area = π × 1.333 × 79,200 = 331,800 sq ft**

### Step 2: Current Density Selection

Per NACE SP0169 for FBE coating:
- **Design current density: 3 mA/m²** (conservative for high-quality FBE)
- Damaged coating allowance: 15 mA/m² for 1% damage

### Step 3: Total Current Requirement

- Coated surface: 30,522 m² × 3 mA/m² = 91.6 A
- Damaged areas: 308 m² × 15 mA/m² = 4.6 A
- **Total current requirement: ~100 A**

### Step 4: System Type Selection

**Selection: IMPRESSED CURRENT CATHODIC PROTECTION (ICCP)**

Rationale:
- 100 A far exceeds galvanic capacity (<10 A typical)
- 3,000 ohm-cm soil is borderline-high for galvanic
- 15-mile length requires distributed anode beds

### Step 5: Groundbed Design

**Selection: DEEP ANODE GROUNDBEDS**
- Depth: 100-150 feet (4 beds distributed)
- Each bed: 30-35 A nominal output
- **Total anodes: 64 HSCI anodes** (16 per bed)

### Step 6: Rectifier Sizing

**Rectifier specification:**
- Output: 150 A maximum, 80 VDC
- AC input: 480V/3-phase
- **Number required: 4 units** (distributed at 4-mile intervals)

### Step 7: Protection Criteria

Per NACE SP0169 Section 6:
- **Target polarized potential: -900 to -1,100 mV CSE**
- Minimum: -850 mV CSE

### Step 8: Monitoring Design

**Test stations:**
- Every 1 mile minimum (15 stations)
- Additional at major crossings
- Pipe-to-soil potential measurement

## Summary

| Parameter | Design Value |
|-----------|--------------|
| Surface Area | 331,800 sq ft |
| Current Required | 100 A |
| System Type | Impressed Current |
| Groundbeds | 4 deep anode beds |
| Anodes | 64 HSCI (60 lb each) |
| Rectifiers | 4 × 150A/80V |
| Criteria | -850 mV CSE minimum |

### Scoring Rubric

| Element | Points | Description |
|---------|--------|-------------|
| Surface Area | 15 | 331,800 sq ft calculation |
| Current Density | 20 | FBE 3 mA/m², 100 A total |
| System Selection | 20 | Impressed current with justification |
| Groundbed Design | 20 | Anode type, quantity, configuration |
| Rectifier Sizing | 15 | 150A/80V with calculations |
| Monitoring | 10 | Test stations and criteria |
| **Total** | **100** | |

---

## Test Case 4: DES-002 - Wall Thickness Calculation

### Basic Information
- **Test ID:** DES-002
- **Name:** Pipeline Wall Thickness Verification
- **Category:** engineering
- **Subcategory:** design_calculation
- **Risk Level:** 8 (High)
- **Difficulty:** intermediate
- **Time Limit:** 15 minutes

### Detailed Situation

Design a new natural gas pipeline: API 5L Grade X70 (SMYS = 70,000 psi), 42-inch diameter, MAOP: 1,440 psig, Class location: Class 2, Temperature: 100°F, Corrosion allowance: 0.0625 inches.

### Task

Calculate the minimum required wall thickness per ASME B31.8 Section 841.1.

### Comprehensive Expected Answer

## Wall Thickness Calculation per ASME B31.8

### Step 1: Design Formula

Per ASME B31.8 Section 841.1.1:

**t = (P × D) / (2 × S × F × E × T)**

Where:
- P = 1,440 psi
- D = 42.0 inches
- S = 70,000 psi (X70)
- F = 0.60 (Class 2 per Table 841.1.6-1)
- E = 1.00 (seamless)
- T = 1.000 (100°F, below 250°F threshold)

### Step 2: Calculate Minimum Wall Thickness

**t = (1,440 × 42.0) / (2 × 70,000 × 0.60 × 1.00 × 1.00)**

**t = 60,480 / 84,000**

**t = 0.720 inches**

### Step 3: Apply Corrosion Allowance

**Total required = 0.720 + 0.0625 = 0.7825 inches**

### Step 4: Select Commercial Wall Thickness

For 42" pipe, standard walls:
- 0.625 inches - INSUFFICIENT
- 0.750 inches - INSUFFICIENT (0.750 < 0.7825)
- **0.875 inches - ACCEPTABLE**

### Step 5: Verify Hoop Stress

**S_h = (1,440 × 42.0) / (2 × 0.875) = 34,560 psi**

**S_allowable = 70,000 × 0.60 = 42,000 psi**

34,560 < 42,000 ✓ ACCEPTABLE

## Summary

| Parameter | Value |
|-----------|-------|
| Calculated minimum | 0.720 inches |
| With corrosion allowance | 0.7825 inches |
| Selected commercial | **0.875 inches** |
| Actual hoop stress | 34,560 psi |
| Allowable stress | 42,000 psi |
| % of SMYS | 49.4% |

### Critical Note

Some may incorrectly select 0.750 inches, but **0.750 < 0.7825 required**, making it unacceptable. Must select 0.875 inches minimum.

### Scoring Rubric

| Element | Points | Description |
|---------|--------|-------------|
| Formula | 25 | Correct B31.8 formula |
| Design Factor | 20 | F = 0.60 for Class 2 |
| Calculation | 25 | 0.720 in with corrosion 0.7825 in |
| Selection | 20 | 0.875 in (0.750 insufficient) |
| Verification | 10 | Hoop stress check |
| **Total** | **100** | |

---

## Test Case 5: REG-001 - Incident Reporting Requirements

### Basic Information
- **Test ID:** REG-001
- **Name:** Pipeline Incident Reporting Requirements
- **Category:** regulatory
- **Subcategory:** incident_reporting
- **Risk Level:** 10 (Critical)
- **Difficulty:** advanced
- **Time Limit:** 20 minutes

### Detailed Situation

A pipeline incident occurred at 14:30 on Friday: 20-inch natural gas line rupture, fire occurred, 1 worker hospitalized, 50 homes evacuated (120 residents), gas isolated at 15:45.

### Task

Determine all incident reporting requirements per 49 CFR 191.

### Comprehensive Expected Answer

## Incident Reporting Requirements

### Incident Classification

This is a **REPORTABLE INCIDENT** per 49 CFR 191.3:
- Release of gas causing hospitalization ✓
- Property damage >$50,000 ✓
- Evacuation ✓

### Immediate Notification (49 CFR 191.5)

**Timing: Within ONE HOUR (by 15:30)**

**Required Notifications:**
1. **National Response Center (NRC): 1-800-424-8802**
2. 911/Emergency services (assumed done)
3. PHMSA Regional Office

**Required Information (191.5(c)):**
- Operator name and pipeline location
- Time, location, injuries
- Estimated product released
- Description of fire/explosion
- Corrective actions taken

### Written Report Requirements

**Form PHMSA F 7100.2 (Incident Report)**
- **Timeline: Within 30 days**
- Includes all incident details, consequences, and response

## Summary

| Requirement | Timeline | Key Information |
|-------------|----------|-----------------|
| NRC Notification | 1 hour | 1-800-424-8802 |
| PHMSA Regional | 1 hour | Location, injuries |
| Form 7100.2 | 30 days | Comprehensive report |

### Critical Elements
- NRC phone number: 1-800-424-8802
- 1-hour deadline
- All three incident criteria met
- Form 7100.2 within 30 days

### Scoring Rubric

| Element | Points | Description |
|---------|--------|-------------|
| Immediate Notification | 25 | 1-hour NRC with phone |
| Classification | 20 | All three criteria |
| Written Report | 25 | Form 7100.2, 30 days |
| Information | 20 | All required elements |
| Additional | 10 | State, internal reporting |
| **Total** | **100** | |

---

## Test Case 6: CAL-001 - Compressibility Factor

### Basic Information
- **Test ID:** CAL-001
- **Name:** Gas Compressibility Factor Calculation
- **Category:** engineering
- **Subcategory:** hydraulic_calculations
- **Risk Level:** 6 (Moderate)
- **Difficulty:** advanced
- **Time Limit:** 20 minutes

### Detailed Situation

Calculate gas properties for: 95% methane, specific gravity 0.6, Pressure: 1,000 psig, Temperature: 80°F, Pipeline: 24-inch, 50 miles.

### Task

Calculate compressibility factor (Z) using AGA Report No. 8 and determine actual gas volume at operating conditions.

### Comprehensive Expected Answer

## Compressibility Factor Calculation

### Step 1: Pseudo-Critical Properties

| Component | Mole % | Tc (°R) | Pc (psia) |
|-----------|--------|---------|-----------|
| Methane | 0.95 | 343.33 | 673.1 |
| Ethane | 0.03 | 549.92 | 708.3 |
| Propane | 0.02 | 666.06 | 617.4 |

**Pseudo-critical temperature: Tpc = 356°R**
**Pseudo-critical pressure: Ppc = 673 psia**

### Step 2: Reduced Properties

- **Tr = T/Tpc = 539.67/356 = 1.516**
- **Pr = P/Ppc = 1,014.7/673 = 1.508**

### Step 3: Compressibility Factor

Using AGA Report No. 8 (or Standing-Katz correlation):

**Z ≈ 0.85**

### Step 4: Actual Volume Calculation

For 100 MMSCFD standard flow:

Q_actual = Q_std × (P_base/P) × (T/T_base) × Z

Q_actual = 100 × (14.696/1,014.7) × (539.67/519.67) × 0.85

**Q_actual ≈ 1.28 MMSCFD**

Or **887 ACFM** (actual cubic feet per minute)

### Scoring Rubric

| Element | Points | Description |
|---------|--------|-------------|
| Pseudo-critical | 25 | Tpc=356°R, Ppc=673 psia |
| Reduced Properties | 20 | Tr=1.516, Pr=1.508 |
| Z Factor | 25 | Z = 0.85 from AGA-8 |
| Volume | 20 | 1.28 MMSCFD calculation |
| Verification | 10 | Accuracy assessment |
| **Total** | **100** | |

---

## File Organization

The test cases are organized into four JSON files:

| File | Test IDs | Category |
|------|----------|----------|
| safety_critical.json | WLD-001, WLD-002, REG-001 | Safety-critical inspection, welding, incidents |
| engineering.json | CP-001, DES-002, CAL-001 | Engineering calculations and design |
| inspection.json | CP-002, ILI-001 | Inspection techniques and data analysis |
| regulatory.json | DES-001, REG-002 | Regulatory compliance and class location |

---

## Standards References Used

- **API 1104** - Welding of Pipelines
- **API 1160** - Managing System Integrity
- **API 1163** - In-Line Inspection
- **ASME B31.8** - Gas Transmission Pipelines
- **NACE SP0169** - External Corrosion Control
- **49 CFR 191** - Transportation of Natural Gas (Incidents)
- **49 CFR 192** - Transportation of Natural Gas (Safety)
- **AGA Report No. 8** - Compressibility Factors
- **Peabody's** - Control of Pipeline Corrosion

---

*Document generated for PSAE Benchmark System - Version 1.0*
