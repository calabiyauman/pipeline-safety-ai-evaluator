"""
Test Scenarios Module
=====================

Defines test scenario classes and test suite definitions.
Implements the STAR-R framework for scenario generation.
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class TestCategory(Enum):
    """Test categories."""
    SAFETY = "safety"
    ENGINEERING = "engineering"
    INSPECTION = "inspection"
    STANDARDS = "standards"
    REGULATORY = "regulatory"
    EMERGENCY = "emergency"


class RiskLevel(Enum):
    """Risk levels for test scenarios."""
    CRITICAL = 10
    HIGH = 8
    STANDARD = 5
    LOW = 2


@dataclass
class AbnormalVariant:
    """
    Abnormal condition variant for a test scenario.
    
    Attributes:
        description: Description of the abnormal condition
        impact: Impact on operations
        type: Type of abnormality (equipment, environmental, etc.)
        severity: Severity level (1-10)
    """
    description: str
    impact: str
    type: str  # equipment, environmental, human, system
    severity: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass 
class TestScenario:
    """
    Test scenario implementing STAR-R framework.
    
    STAR-R Framework:
    - S: Situation (operational context)
    - T: Task (specific objective)
    - A: Action (expected correct procedure)
    - R: Result (expected outcome)
    - R: Risk (consequences of failure)
    
    Attributes:
        test_id: Unique test identifier
        name: Test name
        category: Test category
        risk_level: Risk level (1-10)
        situation: Operational situation description
        task: Specific task objective
        expected_elements: List of expected elements in response
        expected_standards: List of expected standards to cite
        critical_elements: Critical safety elements that must be present
        abnormal_variants: List of abnormal condition variants
        validation_notes: Notes for human validators
    """
    test_id: str
    name: str
    category: str
    risk_level: int
    situation: str
    task: str
    expected_elements: List[str] = field(default_factory=list)
    expected_standards: List[str] = field(default_factory=list)
    critical_elements: List[str] = field(default_factory=list)
    abnormal_variants: List[AbnormalVariant] = field(default_factory=list)
    validation_notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "test_id": self.test_id,
            "name": self.name,
            "category": self.category,
            "risk_level": self.risk_level,
            "situation": self.situation,
            "task": self.task,
            "expected_elements": self.expected_elements,
            "expected_standards": self.expected_standards,
            "critical_elements": self.critical_elements,
            "abnormal_variants": [v.to_dict() for v in self.abnormal_variants],
            "validation_notes": self.validation_notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestScenario':
        """Create from dictionary."""
        abnormal_variants = []
        for item in data.get("abnormal_variants", []):
            if not isinstance(item, dict):
                continue
            description = str(item.get("description", "")).strip()
            if not description:
                continue
            abnormal_variants.append(
                AbnormalVariant(
                    description=description,
                    impact=str(item.get("impact", "")).strip(),
                    type=str(item.get("type", "system")).strip() or "system",
                    severity=int(item.get("severity", 5)),
                )
            )
        
        return cls(
            test_id=data["test_id"],
            name=data["name"],
            category=data["category"],
            risk_level=data["risk_level"],
            situation=data["situation"],
            task=data["task"],
            expected_elements=data.get("expected_elements", []),
            expected_standards=data.get("expected_standards", []),
            critical_elements=data.get("critical_elements", []),
            abnormal_variants=abnormal_variants,
            validation_notes=data.get("validation_notes", "")
        )
    
    def add_abnormal_variant(self, variant: AbnormalVariant):
        """Add an abnormal condition variant."""
        self.abnormal_variants.append(variant)
    
    def get_expected_result_summary(self) -> str:
        """Generate expected result summary."""
        return f"""
Expected Result for {self.name}:
- All critical elements must be present: {', '.join(self.critical_elements)}
- Expected standards: {', '.join(self.expected_standards)}
- Key elements to cover: {len(self.expected_elements)} items
- Abnormal variants available: {len(self.abnormal_variants)}
"""


class TestSuite:
    """Collection of test scenarios."""
    
    def __init__(self, name: str, scenarios: Optional[List[TestScenario]] = None):
        """
        Initialize test suite.
        
        Args:
            name: Suite name
            scenarios: List of test scenarios
        """
        self.name = name
        self.scenarios = scenarios or []
    
    def add_scenario(self, scenario: TestScenario):
        """Add a scenario to the suite."""
        self.scenarios.append(scenario)
    
    def get_by_category(self, category: str) -> List[TestScenario]:
        """Get scenarios by category."""
        return [s for s in self.scenarios if s.category == category]
    
    def get_by_risk_level(self, min_risk: int) -> List[TestScenario]:
        """Get scenarios with risk level >= min_risk."""
        return [s for s in self.scenarios if s.risk_level >= min_risk]
    
    def get_safety_critical(self) -> List[TestScenario]:
        """Get safety-critical scenarios (risk >= 8)."""
        return self.get_by_risk_level(8)
    
    def save_to_json(self, filepath: str):
        """Save suite to JSON file."""
        data = {
            "name": self.name,
            "scenarios": [s.to_dict() for s in self.scenarios]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Test suite saved to {filepath}")
    
    @classmethod
    def load_from_json(cls, filepath: str) -> 'TestSuite':
        """Load suite from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        raw_scenarios = data.get("scenarios")
        if raw_scenarios is None:
            raw_scenarios = data.get("test_cases", [])

        if not isinstance(raw_scenarios, list):
            raise ValueError("Suite JSON must contain 'scenarios' or 'test_cases' as a list.")

        scenarios = [TestScenario.from_dict(s) for s in raw_scenarios]
        suite_name = data.get("name") or data.get("metadata", {}).get("file_name", "Imported Suite")
        suite = cls(suite_name, scenarios)
        
        logger.info(f"Loaded {len(scenarios)} scenarios from {filepath}")
        return suite
    
    def __len__(self) -> int:
        return len(self.scenarios)
    
    def __iter__(self):
        return iter(self.scenarios)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        categories = {}
        risk_levels = {}
        
        for scenario in self.scenarios:
            # Category counts
            cat = scenario.category
            categories[cat] = categories.get(cat, 0) + 1
            
            # Risk level counts
            risk = scenario.risk_level
            risk_levels[risk] = risk_levels.get(risk, 0) + 1
        
        return {
            "total_scenarios": len(self.scenarios),
            "categories": categories,
            "risk_distribution": risk_levels,
            "safety_critical_count": len(self.get_safety_critical()),
            "with_abnormal_variants": sum(
                1 for s in self.scenarios if s.abnormal_variants
            )
        }


# Predefined test suites

SAFETY_CRITICAL_SUITE = TestSuite("Safety-Critical")
ENGINEERING_SUITE = TestSuite("Engineering")
FULL_SUITE = TestSuite("Full Evaluation")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _suite_file_map() -> Dict[str, Path]:
    base = _project_root() / "data" / "test_cases"
    return {
        "safety": base / "safety_critical.json",
        "engineering": base / "engineering.json",
        "inspection": base / "inspection.json",
        "regulatory": base / "regulatory.json",
    }


def _load_suite_from_file(path: Path) -> Optional[TestSuite]:
    if not path.exists():
        return None
    try:
        return TestSuite.load_from_json(str(path))
    except Exception as exc:
        logger.warning(f"Failed loading suite from {path}: {exc}")
        return None


def _benchmark_sources_root() -> Path:
    return _project_root() / "benchmark_sources"


def _list_to_variants(items: List[Dict[str, Any]]) -> List[AbnormalVariant]:
    variants: List[AbnormalVariant] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        description = str(item.get("description", "")).strip()
        impact = str(item.get("impact", "")).strip()
        variant_type = str(item.get("type", "system")).strip() or "system"
        severity = int(item.get("severity", 5))
        if not description:
            continue
        variants.append(
            AbnormalVariant(
                description=description,
                impact=impact or "Operational impact requires reassessment.",
                type=variant_type,
                severity=max(1, min(10, severity)),
            )
        )
    return variants


def _split_standards(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


def _scenario_from_source_entry(
    entry: Dict[str, Any],
    source_label: str,
    fallback_idx: int,
) -> Optional[TestScenario]:
    if not isinstance(entry, dict):
        return None

    test_id = str(entry.get("question_id") or entry.get("test_id") or "").strip()
    if not test_id:
        test_id = f"SRC-{fallback_idx:03d}"

    name = str(entry.get("name") or entry.get("title") or entry.get("question_title") or test_id).strip()
    category = str(entry.get("category", "engineering")).strip().lower()
    if category not in {"safety", "engineering", "inspection", "regulatory"}:
        category = "engineering"

    try:
        risk_level = int(entry.get("risk_level", 5))
    except Exception:
        risk_level = 5
    risk_level = max(1, min(10, risk_level))

    situation = str(entry.get("situation", "")).strip()
    task = str(entry.get("task", "")).strip()
    if not situation or not task:
        return None

    expected_elements = [
        str(v).strip()
        for v in entry.get("expected_elements", [])
        if str(v).strip()
    ]
    critical_elements = [
        str(v).strip()
        for v in entry.get("critical_elements", [])
        if str(v).strip()
    ]
    expected_standards = _split_standards(
        entry.get("expected_standards") or entry.get("standards")
    )
    abnormal_variants = _list_to_variants(entry.get("abnormal_variants", []))

    notes = str(entry.get("validation_notes") or entry.get("notes") or "").strip()
    if source_label:
        notes = (notes + "\n\n" if notes else "") + f"Source: {source_label}"

    return TestScenario(
        test_id=test_id,
        name=name,
        category=category,
        risk_level=risk_level,
        situation=situation,
        task=task,
        expected_elements=expected_elements,
        expected_standards=expected_standards,
        critical_elements=critical_elements,
        abnormal_variants=abnormal_variants,
        validation_notes=notes,
    )


def _extract_markdown_questions(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    matches = list(
        re.finditer(
            r"^###\s+Question\s+\d+:\s*(.+)$",
            text,
            flags=re.MULTILINE,
        )
    )
    entries: List[Dict[str, Any]] = []
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end]

        def _field(pattern: str) -> str:
            found = re.search(pattern, block, flags=re.IGNORECASE | re.MULTILINE)
            return found.group(1).strip() if found else ""

        test_id = _field(r"\*\*Test ID\*\*:\s*([A-Z0-9-]+)")
        category = _field(r"\*\*Category\*\*:\s*([a-zA-Z_]+)").lower()
        risk_raw = _field(r"\*\*Risk Level\*\*:\s*(\d+)")
        risk_level = int(risk_raw) if risk_raw else 5

        situation = _field(r"\*\*Scenario\*\*:\s*([\s\S]*?)\n\*\*Task\*\*:")
        task = _field(r"\*\*Task\*\*:\s*([\s\S]*?)\n\*\*Expected Elements\*\*:")

        expected_raw = _field(r"\*\*Expected Elements\*\*:\s*([\s\S]*?)\n\*\*Critical Elements\*\*:")
        critical_raw = _field(r"\*\*Critical Elements\*\*:\s*([\s\S]*?)\n\*\*Standards\*\*:")
        standards_raw = _field(r"\*\*Standards\*\*:\s*([^\n]+)")

        def _bullets(raw: str) -> List[str]:
            return [
                line[1:].strip()
                for line in [ln.strip() for ln in raw.splitlines()]
                if line.startswith("-")
            ]

        if not test_id or not situation or not task:
            continue

        entries.append(
            {
                "question_id": test_id,
                "title": title,
                "category": category or "engineering",
                "risk_level": risk_level,
                "situation": situation.strip(),
                "task": task.strip(),
                "expected_elements": _bullets(expected_raw),
                "critical_elements": _bullets(critical_raw),
                "standards": standards_raw,
                "notes": f"Auto-extracted from markdown: {path.name}",
            }
        )
    return entries


def load_benchmark_sources_suite(root_path: Optional[str] = None) -> TestSuite:
    """
    Build a suite from benchmark_sources files.

    Supports:
    - JSON files containing one object or list of objects with question/test fields
    - Markdown files using the '### Question N: ...' block format
    """
    root = Path(root_path) if root_path else _benchmark_sources_root()
    suite = TestSuite("Benchmark Sources")
    if not root.exists():
        logger.warning(f"Benchmark sources directory not found: {root}")
        return suite

    entries: List[Dict[str, Any]] = []

    for json_path in sorted(root.rglob("*.json")):
        if json_path.name in {"question_bank.schema.json", "question_bank.template.json"}:
            continue
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                entries.extend(payload)
            elif isinstance(payload, dict):
                if isinstance(payload.get("questions"), list):
                    entries.extend(payload["questions"])
                else:
                    entries.append(payload)
        except Exception as exc:
            logger.warning(f"Skipping invalid benchmark source JSON {json_path}: {exc}")

    for md_path in sorted(root.rglob("*.md")):
        try:
            entries.extend(_extract_markdown_questions(md_path))
        except Exception as exc:
            logger.warning(f"Skipping benchmark source markdown {md_path}: {exc}")

    seen_ids = set()
    counter = 1
    for entry in entries:
        scenario = _scenario_from_source_entry(entry, str(root), counter)
        counter += 1
        if scenario is None:
            continue
        if scenario.test_id in seen_ids:
            logger.warning(f"Duplicate benchmark source test_id skipped: {scenario.test_id}")
            continue
        seen_ids.add(scenario.test_id)
        suite.add_scenario(scenario)

    logger.info(f"Loaded {len(suite.scenarios)} benchmark source scenarios from {root}")
    return suite


def load_builtin_suite(suite_type: str = "full") -> TestSuite:
    """
    Load built-in test suite.
    
    Args:
        suite_type: 'safety', 'engineering', or 'full'
        
    Returns:
        TestSuite instance
    """
    files = _suite_file_map()
    if suite_type in ("safety", "engineering", "inspection", "regulatory"):
        loaded = _load_suite_from_file(files[suite_type])
        if loaded is not None:
            return loaded

    if suite_type == "benchmark-sources":
        return load_benchmark_sources_suite()

    if suite_type == "full":
        merged = TestSuite("Full Evaluation")
        for key in ("safety", "engineering", "inspection", "regulatory"):
            loaded = _load_suite_from_file(files[key])
            if loaded is None:
                loaded = load_builtin_suite(key)
            for scenario in loaded.scenarios:
                merged.add_scenario(scenario)
        if merged.scenarios:
            return merged

    if suite_type == "safety":
        return SAFETY_CRITICAL_SUITE
    if suite_type == "engineering":
        return ENGINEERING_SUITE
    return FULL_SUITE


def initialize_builtin_suites():
    """Initialize built-in test suites with actual test cases."""
    
    # === SAFETY-CRITICAL SCENARIOS (Risk Level 10) ===
    
    # 1. Hot Tapping Safety Protocols
    hot_tapping = TestScenario(
        test_id="SC-001",
        name="Hot Tapping Safety Protocols",
        category="safety",
        risk_level=10,
        situation="""
12-inch natural gas transmission line operating at 600 psig with flow rate of 50 MMSCFD. 
Location is Class 3 High Consequence Area (HCA) near residential neighborhood. 
Operation involves installing a 4-inch branch connection via hot tapping for new 
customer tap. Work crew consists of 4 OQ-qualified personnel. Equipment includes 
hot tap machine, drilling motor, valve, and N2 purging system.
""",
        task="""
Develop a complete hot tapping procedure that ensures safe completion of the branch 
connection without interrupting service or causing safety incidents. Include pre-job 
requirements, step-by-step operations, safety measures, and contingency procedures.
""",
        expected_elements=[
            "Pre-job safety meeting",
            "Work permit requirements",
            "Pressure verification",
            "Purging procedure (N2 or natural gas)",
            "Hot tap machine setup and testing",
            "Drilling procedure",
            "Coupon retention",
            "Welding procedure per API 1104",
            "Post-weld inspection",
            "Pressure testing",
            "Cleanup and restoration",
            "Documentation requirements"
        ],
        expected_standards=["API 1104", "ASME B31.8", "OSHA 1910.269"],
        critical_elements=[
            "gas monitoring",
            "purge verification",
            "qualified personnel",
            "work permit",
            "emergency procedures"
        ],
        validation_notes="""
Critical test case. AI must demonstrate comprehensive understanding of hot tapping 
hazards and proper safety protocols. Missing critical elements should result in 
substantial penalties. Response should cite specific standards sections.
"""
    )
    
    # Add abnormal variants
    hot_tapping.add_abnormal_variant(AbnormalVariant(
        description="Nitrogen purge supply interrupted during welding phase",
        impact="Risk of gas accumulation and potential explosion",
        type="equipment",
        severity=9
    ))
    hot_tapping.add_abnormal_variant(AbnormalVariant(
        description="Unexpected pressure spike to 750 psig during hot tap",
        impact="Overpressure risk, potential equipment failure",
        type="system",
        severity=10
    ))
    hot_tapping.add_abnormal_variant(AbnormalVariant(
        description="Lightning storm approaching within 2 miles",
        impact="Ignition risk, must suspend operations",
        type="environmental",
        severity=8
    ))
    
    SAFETY_CRITICAL_SUITE.add_scenario(hot_tapping)
    FULL_SUITE.add_scenario(hot_tapping)
    
    # 2. Emergency Gas Leak Response
    emergency_leak = TestScenario(
        test_id="SC-002",
        name="Emergency Gas Leak Response",
        category="safety",
        risk_level=10,
        situation="""
12-inch natural gas transmission line in rural area. Operator receives report 
of visible gas cloud near pipeline right-of-way. Wind direction: blowing toward 
adjacent farm buildings. Initial LEL reading at edge of cloud: 40% LEL. 
Time: 14:30, weather clear, wind 10 mph.
""",
        task="""
Develop immediate emergency response procedures including personnel actions, 
evacuation requirements, isolation procedures, notification protocols, and 
safe approach procedures. Include considerations for flammability, wind direction, 
and public safety.
""",
        expected_elements=[
            "Immediate actions (evacuation, upwind approach)",
            "Area isolation and cordoning",
            "Emergency services notification",
            "Leak location and assessment",
            "Isolation valve operation",
            "Venting procedures",
            "Ignition source control",
            "Public safety measures",
            "Communication protocols",
            "Documentation requirements"
        ],
        expected_standards=["DOT 49 CFR 192.615", "API 1162", "NFPA 58"],
        critical_elements=[
            "upwind approach",
            "evacuation",
            "isolation",
            "emergency services",
            "ignition source control"
        ],
        validation_notes="""
Critical safety scenario - lives depend on correct emergency response. AI must 
prioritize immediate safety actions and demonstrate understanding of gas hazards.
"""
    )
    
    emergency_leak.add_abnormal_variant(AbnormalVariant(
        description="Ignition source identified near leak (farm equipment)",
        impact="Imminent explosion risk",
        type="environmental",
        severity=10
    ))
    
    SAFETY_CRITICAL_SUITE.add_scenario(emergency_leak)
    FULL_SUITE.add_scenario(emergency_leak)
    
    # === ENGINEERING SCENARIOS ===
    
    # 3. Control Valve Sizing
    cv_sizing = TestScenario(
        test_id="EN-001",
        name="Control Valve Cv Calculation",
        category="engineering",
        risk_level=8,
        situation="""
Liquid propane pipeline with the following conditions:
- Flow rate: 5,000 bbl/day
- Inlet pressure: 250 psig
- Outlet pressure required: 150 psig  
- Specific gravity: 0.495
- Temperature: 80°F
- Valve type: Globe valve with equal percentage trim
- Service: Liquefied petroleum gas (LPG)
""",
        task="""
Calculate the required Cv (flow coefficient) for proper valve sizing. Select 
appropriate valve size from standard Cv ratings. Check for potential cavitation 
and verify choked flow conditions. Provide justification for valve selection.
""",
        expected_elements=[
            "Cv formula application",
            "Unit conversions",
            "Numerical calculation",
            "Valve selection from manufacturer data",
            "Cavitation check",
            "Choked flow verification",
            "Safety margin consideration"
        ],
        expected_standards=["ISA-75.01", "IEC 60534"],
        critical_elements=["Cv calculation", "unit conversion", "cavitation check"],
        validation_notes="""
Engineering calculation test. AI must show correct formula application and 
calculations. Numerical accuracy is critical.
"""
    )
    
    ENGINEERING_SUITE.add_scenario(cv_sizing)
    FULL_SUITE.add_scenario(cv_sizing)
    
    # 4. ASME B31.8 Hydrostatic Testing
    hydrotest = TestScenario(
        test_id="EN-002",
        name="ASME B31.8 Hydrostatic Testing",
        category="engineering",
        risk_level=10,
        situation="""
New 20-inch natural gas transmission pipeline installation, Class 3 location. 
Pipeline specifications:
- Material: API 5L Grade X52
- Wall thickness: 0.375 inches
- Design pressure: 1,440 psig
- Test section: 5 miles
- Elevation change: +500 feet
- Temperature: 70°F
""",
        task="""
Develop a complete hydrostatic testing procedure per ASME B31.8 and DOT 49 CFR 192. 
Calculate test pressure considering elevation, specify hold time, define acceptance 
criteria, and outline safety procedures.
""",
        expected_elements=[
            "Test pressure calculation",
            "Elevation considerations",
            "Hold time determination",
            "Acceptance criteria",
            "Safety procedures",
            "Equipment requirements",
            "Documentation",
            "Failure response"
        ],
        expected_standards=["ASME B31.8", "DOT 49 CFR 192.505"],
        critical_elements=["test pressure calculation", "safety procedures", "acceptance criteria"],
        validation_notes="""
High-risk engineering test. Incorrect test pressure or procedures could result 
in test failure or safety incident.
"""
    )
    
    hydrotest.add_abnormal_variant(AbnormalVariant(
        description="Pressure drop of 50 psi observed during hold period",
        impact="Potential leak in test section",
        type="system",
        severity=7
    ))
    
    ENGINEERING_SUITE.add_scenario(hydrotest)
    FULL_SUITE.add_scenario(hydrotest)
    
    # === INSPECTION SCENARIOS ===
    
    # 5. Sour Gas Corrosion Detection
    sour_gas_inspection = TestScenario(
        test_id="IN-001",
        name="Sour Gas Corrosion Detection",
        category="inspection",
        risk_level=9,
        situation="""
10-mile sour gas transmission pipeline (H2S: 500 ppm) operating at 800 psig. 
Pipe: API 5L X52, 20-inch OD, 0.375-inch wall. Pipeline age: 25 years. 
Last inspection: 8 years ago (ultrasonic thickness measurement). 
Operating history: H2S service for entire life.
""",
        task="""
Develop a comprehensive inspection and monitoring program for internal corrosion. 
Estimate corrosion rates, determine remaining life, recommend inspection technology, 
and propose mitigation strategies.
""",
        expected_elements=[
            "Corrosion rate estimation",
            "Remaining life calculation",
            "Inspection technology selection",
            "Inspection frequency",
            "Mitigation options",
            "Monitoring program"
        ],
        expected_standards=["API 1160", "NACE SP0169", "ASME B31.8S"],
        critical_elements=["corrosion rate", "remaining life", "inspection frequency"],
        validation_notes="""
Critical inspection test. Undetected corrosion could lead to pipeline failure. 
AI must demonstrate understanding of sour gas corrosion mechanisms.
"""
    )
    
    sour_gas_inspection.add_abnormal_variant(AbnormalVariant(
        description="Previous inspection data appears corrupted/missing",
        impact="Cannot determine corrosion rate trend",
        type="system",
        severity=6
    ))
    
    FULL_SUITE.add_scenario(sour_gas_inspection)
    
    logger.info(f"Initialized built-in test suites:")
    logger.info(f"  - Safety-Critical: {len(SAFETY_CRITICAL_SUITE)} scenarios")
    logger.info(f"  - Engineering: {len(ENGINEERING_SUITE)} scenarios")
    logger.info(f"  - Full Suite: {len(FULL_SUITE)} scenarios")


# Initialize on import
initialize_builtin_suites()
