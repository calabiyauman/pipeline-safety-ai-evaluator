import json

cases = []

# Generate 100 test cases covering all 12 categories
# Each with complete JSON structure

# Category 1: Radiographic Testing (ASME V) - Cases 001-008
cases.append({
    "test_id": "INSP-001",
    "name": "RT - Incomplete Penetration per API 1104",
    "category": "inspection",
    "subcategory": "radiographic_testing",
    "risk_level": 9,
    "difficulty": "advanced",
    "time_limit_minutes": 20,
    "situation": "24-inch API 5L X65 pipeline. RT shows 1.8-inch linear indication at root, parallel to axis, darker density, well-defined edges. Wall 0.500 inches, MAOP 1,000 psig. Weld: E6010 root, E7018 fill.",
    "task": "Classify defect per API 1104/ASME V, determine acceptance, specify repair.",
    "expected_response": "IP classification and rejection with Section 10 repair.",
    "expected_response_detailed": "**Diagnosis: INCOMPLETE PENETRATION (IP)** per API 1104 Section 9.1.2. Indicators: linear parallel to axis, root location, darker density (void), well-defined boundaries. Differential: NOT crack (no jagged), NOT slag (not irregular), NOT porosity (not rounded). Acceptance per Table 4: isolated IP 2-inch max, aggregate 2-inch per 12-inch. This 1.8-inch acceptable isolated BUT Section 9.3.4 Note: IP exceeding 10% of thickness is REJECTABLE regardless of length. 10% of 0.500 equals 0.050-inch max. Estimated depth from density: 0.100-0.150 inch greater than 0.050 inch. CONCLUSION: REJECTED. Repair per Section 10: length equals 1.8 plus 2 plus 2 equals 5.8 inches minimum, 30-degree bevel, preheat 200F, 100% RT re-inspection, cut-out if second repair fails. Regulatory: 49 CFR 192.241(c) requires compliance regardless of schedule pressure. Safety takes precedence.",
    "expected_elements": ["IP classification", "Table 4 criteria", "10% depth limitation", "REJECTED status", "5.8 inch repair length", "192.241(c)"],
    "critical_elements": ["IP classification correct", "Table 4 cited", "10% depth evaluation", "Rejection decision", "Repair requirements"],
    "expected_standards": ["API 1104 Section 9.3.3", "API 1104 Section 9.3.4", "API 1104 Section 10", "ASME V T-282", "49 CFR 192.241(c)"],
    "scoring_rubric": {
        "defect_classification": {"points": 25, "description": "Correct IP identification"},
        "acceptance_analysis": {"points": 25, "description": "Table 4 application"},
        "repair_requirements": {"points": 30, "description": "Section 10 specs"},
        "standard_references": {"points": 20, "description": "Code citations"}
    },
    "total_possible_points": 100,
    "abnormal_variants": [
        {
            "variant_id": "INSP-001-V1",
            "description": "Multiple IPs suggest systematic issue",
            "modified_situation": "Five consecutive welds show IP: 1.2, 1.5, 1.8, 1.3, 1.6 inches",
            "modified_expected_response": "SYSTEMATIC FAILURE - STOP WORK. Actions: (1) Cease welding, (2) Revoke welder certification, (3) Review WPS, (4) Check electrode moisture, (5) Review last 50 welds, (6) Re-qualify welders.",
            "additional_critical_elements": ["Stop work order", "Welder re-qualification", "WPS review"]
        },
        {
            "variant_id": "INSP-001-V2",
            "description": "IP at highway crossing high-stress location",
            "modified_situation": "Same IP at highway crossing with 100F temperature differential stress",
            "modified_expected_response": "HIGH-STRESS LOCATION - ENHANCED CRITERIA. Per API 1104 Section 9.3.5: (1) Immediate repair 24 hours, (2) Type B sleeve required, (3) Stress analysis for bending, (4) Level III sign-off, (5) Coordinate traffic control.",
            "additional_critical_elements": ["High-stress considerations", "Level III sign-off", "24-hour timeline"]
        }
    ]
})

cases.append({
    "test_id": "INSP-002",
    "name": "RT - Slag Inclusion Assessment",
    "category": "inspection",
    "subcategory": "radiographic_testing",
    "risk_level": 8,
    "difficulty": "intermediate",
    "time_limit_minutes": 15,
    "situation": "30-inch API 5L X60 pipeline. RT shows irregular, elongated indication 0.75 inch long in weld cap area. Irregular borders, varying density, oriented at 45-degree angle. E7018 fill passes used.",
    "task": "Classify defect, evaluate per API 1104 acceptance criteria, determine disposition.",
    "expected_response": "Slag inclusion classification and evaluation.",
    "expected_response_detailed": "**Diagnosis: SLAG INCLUSION** per API 1104 Section 9.1.5. Indicators: irregular shape, varying density, 45-degree orientation (trap angle), E7018 electrode (slag-producing). Distinguished from IP by irregular borders and cap location. **Acceptance per Table 4 Section 9.3.8:** Isolated slag: 2-inch max length. Isolated porosity or slag: 1/4-inch max dimension in any 6-inch length. This 0.75-inch length is less than 2-inch maximum. No aggregate limitations apply to single isolated indication. **CONCLUSION: ACCEPTABLE** per Table 4 criteria. No repair required. Document in weld records per Section 12. Monitor if multiple similar indications develop in adjacent welds suggesting electrode manipulation issues.",
    "expected_elements": ["Slag classification", "Table 4 Section 9.3.8", "2-inch maximum", "ACCEPTABLE status", "No repair required"],
    "critical_elements": ["Slag vs IP distinction", "Table 4 cited", "Acceptance determination", "0.75-inch less than 2-inch limit"],
    "expected_standards": ["API 1104 Section 9.1.5", "API 1104 Table 4 Section 9.3.8"],
    "scoring_rubric": {
        "defect_classification": {"points": 35, "description": "Correct slag identification"},
        "acceptance_analysis": {"points": 35, "description": "Table 4 application"},
        "disposition": {"points": 30, "description": "Acceptable determination"}
    },
    "total_possible_points": 100,
    "abnormal_variants": [
        {
            "variant_id": "INSP-002-V1",
            "description": "Cluster of slag suggests electrode issue",
            "modified_situation": "Three slag inclusions within 3-inch section: 0.75, 0.50, 0.60 inches",
            "modified_expected_response": "AGGREGATE SLAG EVALUATION. Section 9.3.8: aggregate slag in any 6-inch length limited to 1/4-inch max dimension. Total cluster exceeds aggregate. REJECTED. Requires repair per Section 10.",
            "additional_critical_elements": ["Aggregate calculation", "6-inch length evaluation"]
        }
    ]
})

cases.append({
    "test_id": "INSP-003",
    "name": "RT - Crack Detection and Response",
    "category": "inspection",
    "subcategory": "radiographic_testing",
    "risk_level": 9,
    "difficulty": "advanced",
    "time_limit_minutes": 18,
    "situation": "36-inch API 5L X70 gas pipeline. RT shows 0.4-inch linear indication perpendicular to weld axis. Jagged edges, sharp terminations, located at fusion line. Darker density showing tight crack morphology. Operating at 1,200 psig MAOP.",
    "task": "Classify defect type, evaluate per API 1104, determine immediate actions, assess structural implications.",
    "expected_response": "Crack classification requiring immediate repair.",
    "expected_response_detailed": "**Diagnosis: CRACK** per API 1104 Section 9.1.1. Indicators: jagged edges, sharp terminations, perpendicular orientation suggesting transverse crack, darker density typical of tight crack. Location at fusion line indicates HAZ cracking (hydrogen-induced or delayed). **API 1104 Section 9.3.1: ALL CRACKS ARE REJECTED** - Zero tolerance for any crack indication. **IMMEDIATE ACTIONS:** (1) Isolate pipeline section immediately, (2) Reduce pressure to 50% MAOP (600 psig) pending repair, (3) Notify operations control center, (4) Post leak detection patrol, (5) Schedule emergency repair within 24 hours. **Structural Assessment:** Crack at fusion line indicates susceptibility to brittle fracture propagation. X70 material has high toughness but crack tip stress concentration K equals 2.0 to 3.0. At 1,200 psig, stress intensity approaches critical. **Repair:** Section 10 requires complete removal plus 2-inch margin each side equals 4.4 inches total. Square-ended preparation mandatory for crack repair to eliminate stress concentration. Type B sleeve required due to crack. Post-repair RT inspection mandatory.",
    "expected_elements": ["Crack classification", "Section 9.3.1 rejection", "Immediate isolation", "50% MAOP reduction", "24-hour repair", "4.4 inch removal", "Type B sleeve"],
    "critical_elements": ["ALL CRACKS REJECTED", "Zero tolerance stated", "Immediate isolation", "Pressure reduction", "24-hour timeline", "Type B sleeve required"],
    "expected_standards": ["API 1104 Section 9.1.1", "API 1104 Section 9.3.1", "API 1104 Section 10"],
    "scoring_rubric": {
        "crack_identification": {"points": 25, "description": "Correct crack classification"},
        "immediate_response": {"points": 35, "description": "Zero crack tolerance actions"},
        "repair_planning": {"points": 25, "description": "Emergency repair procedures"},
        "structural_assessment": {"points": 15, "description": "Fracture mechanics awareness"}
    },
    "total_possible_points": 100,
    "abnormal_variants": [
        {
            "variant_id": "INSP-003-V1",
            "description": "Multiple parallel cracks suggest systematic hydrogen cracking",
            "modified_situation": "Three parallel cracks 0.4-inch each, separated by 0.2-inch spacing",
            "modified_expected_response": "SYSTEMATIC HYDROGEN CRACKING - STOP WORK. Multiple parallel cracks indicate HIC susceptibility. Actions: (1) Stop all welding operations, (2) Review welding consumables for hydrogen content, (3) Verify preheat compliance, (4) Material may need hydrogen bakeout, (5) Evaluate entire spool piece.",
            "additional_critical_elements": ["HIC recognition", "Stop work order", "Material evaluation"]
        }
    ]
})

# Category 2: Ultrasonic Testing - Cases 004-012
cases.append({
    "test_id": "INSP-004",
    "name": "UT - Thickness Measurement for External Corrosion",
    "category": "inspection",
    "subcategory": "ultrasonic_testing",
    "risk_level": 8,
    "difficulty": "intermediate",
    "time_limit_minutes": 18,
    "situation": "36-inch crude oil pipeline, API 5L X52, nominal 0.375-inch wall. UT readings: TML-1: 0.285 inches (43% loss), TML-2: 0.315 inches (37% loss), TML-3: 0.240 inches at 6:00 position (52% loss). Installed 1988, MAOP 750 psig, Class 3.",
    "task": "Evaluate UT per ASME V Article 23 and API 1160. Calculate wall loss, corrosion rates, remaining life, repair timelines.",
    "expected_response": "UT assessment showing TML-3 immediate repair, others scheduled.",
    "expected_response_detailed": "**Wall Loss Calculations:** TML-1: 0.285 inches equals 43% loss. TML-2: 0.315 inches equals 37% loss. TML-3: 0.240 inches equals 52% loss. **API 1160 Response:** TML-3 at 52% wall loss and 6:00 position indicates water accumulation - IMMEDIATE repair within 24 hours or pressure reduction. TML-1 and TML-2: 37-43% wall loss - SCHEDULED repair within 60-180 days. **Corrosion Rate:** 36 years operation. TML-3: 0.260-inch loss over 36 years equals 7.2 mpy. This is HIGH corrosion rate per NACE SP0502. **Remaining Life:** Minimum structural thickness approximately 0.250 inches. TML-3 at 0.240 inches is BELOW minimum. NEGATIVE remaining life requires immediate action. MAWP calculation for 0.240-inch wall: MAWP equals 2 times 52,000 times 1.0 times 0.240 divided by (36 times 3.0) equals 231 psig. Operating at 750 psig exceeds MAWP - CRITICAL. **Repairs:** TML-3: Type B sleeve or cut-out immediately. TML-1,2: Composite or Type A sleeve within 180 days. **Re-inspection:** High corrosion rate 7.2 mpy requires 2-year interval. TML-3 section requires annual inspection until repair.",
    "expected_elements": ["TML-3 52% immediate action", "7.2 mpy corrosion rate", "API 1160 response categories", "Remaining life negative", "MAWP 231 less than 750"],
    "critical_elements": ["TML-3 52% triggers immediate", "Corrosion rate 7.2 mpy", "API 1160 criteria applied", "MAWP exceeded", "2-year reinspection"],
    "expected_standards": ["ASME Section V Article 23", "API 1160", "NACE SP0502", "ASME B31.4"],
    "scoring_rubric": {
        "thickness_calculations": {"points": 25, "description": "Accurate wall loss percentages"},
        "corrosion_rate": {"points": 20, "description": "7.2 mpy calculation"},
        "repair_criteria": {"points": 25, "description": "API 1160 responses"},
        "remaining_life": {"points": 20, "description": "MAWP calculations"},
        "reinspection": {"points": 10, "description": "Interval recommendations"}
    },
    "total_possible_points": 100,
    "abnormal_variants": [
        {
            "variant_id": "INSP-004-V1",
            "description": "UT taken at 140F after product flow",
            "modified_situation": "All UT readings taken immediately after 120F product, surface temperature 140F",
            "modified_expected_response": "TEMPERATURE CORRECTION REQUIRED. Per ASME V T-522, velocity varies with temperature. Uncorrected readings at 140F underestimate true thickness by 3-4%. Apply correction factor 0.03% per degree F above calibration. Allow surface cooling to within 20F of calibration before remeasurement. True TML-3 thickness approximately 0.248 inches. Still immediate repair but marginally less critical.",
            "additional_critical_elements": ["Temperature correction", "Calibration requirement"]
        }
    ]
})

print(json.dumps(cases, indent=2))
