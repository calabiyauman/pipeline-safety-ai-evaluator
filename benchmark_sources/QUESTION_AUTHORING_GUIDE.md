# Question Authoring Guide (Standards-Linked)

Use this guide when adding benchmark questions and answers sourced from standards in `benchmark_sources/`.

## Goal

Create questions that can be:
1. traced to a real standard/regulatory reference,
2. scored consistently,
3. converted into PSAE runtime test cases under `data/test_cases/`.

## Authoring Workflow

1. Start from `question_bank.template.json`.
2. Fill fields according to `question_bank.schema.json`.
3. Keep `source_reference` specific (section/paragraph where possible).
4. Provide `expected_answer` as a concise expert baseline.
5. Define `expected_elements` and `critical_elements` distinctly:
   - `expected_elements`: ideal coverage items
   - `critical_elements`: safety-critical must-have items
6. Add at least one abnormal variant for high-risk questions (risk >= 8).
7. Convert approved entries into `data/test_cases/*.json` records.

## Field Mapping to Runtime Test Cases

- `question_id` -> `test_id`
- `category` -> `category`
- `risk_level` -> `risk_level`
- `situation` -> `situation`
- `task` -> `task`
- `expected_elements` -> `expected_elements`
- `expected_standards` -> `expected_standards`
- `critical_elements` -> `critical_elements`
- `abnormal_variants` -> `abnormal_variants`
- `notes` -> `validation_notes`

## Quality Checklist

- [ ] Source reference is specific and verifiable
- [ ] Question is operationally realistic (not trivia-only)
- [ ] Expected answer is technically correct and standards-aligned
- [ ] Critical elements are explicit and safety-focused
- [ ] Rubric is clear enough for consistent scoring
- [ ] Risk level is justified

## Recommended Naming

- API/Welding: `WLD-###`
- Cathodic Protection: `CP-###`
- Regulatory: `REG-###`
- Design/Engineering: `DES-###`, `CAL-###`

Consistency in IDs helps maintain traceability between source drafts and final benchmark artifacts.
