#!/usr/bin/env python3
import json

test_cases = []

# Generate test cases covering all 12 categories
categories = [
    ("radiographic_testing", "ASME V"),
    ("ultrasonic_testing", "ASME V"),
    ("mfl_inspection", "API 1163"),
    ("caliper_geometry", "API 1163"),
    ("crack_detection", "API 579"),
    ("external_corrosion", "NACE SP0502"),
    ("internal_corrosion", "NACE SP0502"),
    ("coating_assessment", "NACE SP0288"),
    ("cathodic_protection", "NACE SP0169"),
    ("ac_dc_interference", "NACE SP0169"),
    ("weld_inspection", "API 1104"),
    ("pressure_testing", "ASME B31.8")
]

test_cases.append({
    "test_id": "INSP-001",
    "name": "Radiographic Testing - Incomplete Penetration Classification",
    "category": "inspection",
    "subcategory": "radiographic_testing",
    "risk_level": 9,
    "difficulty": "advanced",
    "time_limit_minutes": 20,
    "situation": "A radiographic inspection on a 24-inch API 5L X65 gas transmission pipeline reveals an elongated indication at the weld root. The indication measures 1.8 inches in length, runs parallel to the weld axis, appears darker than adjacent weld metal, and has well-defined parallel edges. Wall thickness is 0.500 inches. Pipeline operates at 1,000 psig MAOP. Weld completed using single V-groove with E6010 root and E7018 fill passes.",
    "task": "Classify the discontinuity type per API 1104 and ASME V, determine acceptance criteria, calculate repair requirements, and document the decision.",
    "expected_response": "IP defect classification and rejection with Section 10 repair.",
    "expected_response_detailed": "**Diagnosis: INCOMPLETE PENETRATION (IP)** Per API 1104 Section 9.1.2. Key indicators: linear parallel to axis, root location, darker density (void), well-defined boundaries. Differential: NOT crack (no jagged), NOT slag (not irregular), NOT porosity (not rounded). Acceptance per Table 4: Isolated IP 2 inches max. This 1.8 inches acceptable isolated BUT Section 9.3.4 Note states IP extending >10% of thickness is REJECTABLE. 10% of 0.500 = 0.050 inch max. Estimated depth 0.100-0.150 inch > 0.050 inch. CONCLUSION: REJECTED. Repair per Section 10: Length = 1.8 + 2 + 2 = 5.8 inches minimum, 30 degree bevel, 100% RT re-inspection, cut-out if second repair fails. Regulatory: 49 CFR 192.241(c) - acceptance criteria apply regardless of schedule.",
    "expected_elements": ["IP classification", "Table 4 criteria", "10% depth limitation", "REJECTED status", "5.8 inch repair length"],
    "critical_elements": ["IP classification correct", "Table 4 cited", "10% depth evaluation", "Rejection decision", "Repair requirements"],
    "expected_standards": ["API 1104 Section 9.3.3", "API 1104 Section 9.3.4", "API 1104 Section 10", "ASME V T-282", "49 CFR 192.241(c)"],
    "scoring_rubric": {
        "defect_classification": {"points": 25, "description": "Correct IP identification"},
        "acceptance_analysis": {"points": 25, "description": "Table 4 application with depth"},
        "repair_requirements": {"points": 30, "description": "Section 10 repair specs"},
        "standard_references": {"points": 20, "description": "Proper code citations"}
    },
    "total_possible_points": 100,
    "abnormal_variants": [
        {
            "variant_id": "INSP-001-V1",
            "description": "Multiple similar IPs suggest systematic welding issue",
            "modified_situation": "Five consecutive welds show IP indications of 1.2, 1.5, 1.8, 1.3, and 1.6 inches suggesting systematic problem",
            "modified_expected_response": "SYSTEMATIC FAILURE - STOP WORK IMMEDIATELY. Multiple IPs indicate: (1) Welder qualification failure - revoke welder certification, (2) WPS inadequacy - review welding procedure, (3) Electrode handling issues - check moisture content and storage, (4) Joint preparation problems - verify root opening and alignment. Actions: Cease all welding operations, notify welding inspector supervisor and project engineer, comprehensive review of last 50 welds, re-qualify welders before resuming work, update WPS if necessary. Root cause analysis mandatory.",
            "additional_critical_elements": ["Stop work order", "Welder re-qualification", "WPS review", "Root cause analysis"]
        },
        {
            "variant_id": "INSP-001-V2",
            "description": "IP located at high-stress highway crossing",
            "modified_situation": "Same IP indication at major highway crossing with expected 100°F temperature differential stress creating additional thermal stress",
            "modified_expected_response": "HIGH-STRESS LOCATION - ENHANCED CRITERIA. Highway crossings create additional stress from thermal expansion/contraction cycles. Per API 1104 Section 9.3.5, defects in high-stress areas require more stringent evaluation. Enhanced requirements: Immediate repair (not 72-hour window), consider Type B sleeve as permanent repair option, stress analysis for bending stress at crossing, additional NDE (UT) to verify defect characteristics, enhanced quality control for repair - Level III inspector sign-off. Total cost estimate may exceed standard repair due to traffic control requirements.",
            "additional_critical_elements": ["High-stress considerations", "Enhanced quality requirements", "Level III sign-off", "Traffic coordination"]
        }
    ]
})

# Continue with more test cases...
print(json.dumps(test_cases, indent=2))
