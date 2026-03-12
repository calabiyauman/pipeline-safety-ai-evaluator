"""
LLM-as-Judge Scoring Module
===========================

Uses an LLM to evaluate AI responses against expected criteria.
Returns metrics in the same format as MetricCalculator for drop-in compatibility.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional

try:
    from ..scenarios.base import TestScenario
except ImportError:
    from scenarios.base import TestScenario

try:
    from ..models.ai_interface import AIModelInterface
except ImportError:
    from models.ai_interface import AIModelInterface

logger = logging.getLogger(__name__)

METRIC_NAMES = [
    "accuracy",
    "relevance",
    "safety",
    "completeness",
    "technical_depth",
    "sources",
]


class LLMJudge:
    """
    Uses an LLM to score AI responses on the six PSAE dimensions.
    
    Produces metrics compatible with MetricCalculator output format.
    """

    def __init__(self, judge_model: AIModelInterface):
        """
        Initialize the LLM judge.
        
        Args:
            judge_model: AI model to use as judge (e.g., GPT-4, Claude).
                        Should be a capable model; typically use a different
                        model than the one being evaluated.
        """
        self.judge_model = judge_model

    def score(
        self,
        response: str,
        scenario: TestScenario,
    ) -> Dict[str, Any]:
        """
        Score an AI response using the LLM judge.
        
        Args:
            response: The AI-generated response to evaluate
            scenario: The test scenario with expected elements, standards, etc.
            
        Returns:
            Metrics dict in MetricCalculator format:
            {
                "accuracy": {"score": float, "rationale": str},
                "relevance": {"score": float, "rationale": str},
                ...
            }
        """
        prompt = self._build_judge_prompt(response, scenario)
        
        try:
            raw_output = self.judge_model.query(prompt)
        except Exception as e:
            logger.warning(f"LLM judge query failed: {e}")
            return self._fallback_metrics()

        return self._parse_judge_response(raw_output)

    def _build_judge_prompt(self, response: str, scenario: TestScenario) -> str:
        """Build the scoring prompt for the judge LLM."""
        expected_ref = ""
        if scenario.expected_response_detailed:
            expected_ref = f"""
EXPECTED REFERENCE (ideal response elements):
{scenario.expected_response_detailed[:4000]}
"""
        elif scenario.expected_elements:
            expected_ref = "\n".join(
                f"- {e}" for e in (scenario.expected_elements or [])[:30]
            )
            expected_ref = f"\nEXPECTED ELEMENTS:\n{expected_ref}\n"

        standards_ref = ""
        if scenario.expected_standards:
            standards_ref = "\n".join(
                f"- {s}" for s in scenario.expected_standards[:20]
            )
            standards_ref = f"\nEXPECTED STANDARDS TO CITE:\n{standards_ref}\n"

        critical_ref = ""
        if scenario.critical_elements:
            critical_ref = "\n".join(
                f"- {c}" for c in scenario.critical_elements[:20]
            )
            critical_ref = f"\nCRITICAL ELEMENTS (must be present):\n{critical_ref}\n"

        return f"""You are an expert pipeline safety evaluator.
Score the following AI response on six dimensions (0-100 each).
Be strict: pipeline safety requires precision and compliance.

SCENARIO:
Test ID: {scenario.test_id}
Category: {scenario.category}
Situation: {scenario.situation[:1500]}
Task: {scenario.task[:800]}
{expected_ref}{standards_ref}{critical_ref}

AI RESPONSE TO EVALUATE:
---
{response[:6000]}
---

Score each dimension 0-100. Return ONLY valid JSON in this exact format (no markdown, no extra text):
{{
  "accuracy": {{"score": <0-100>, "rationale": "<brief reason>"}},
  "relevance": {{"score": <0-100>, "rationale": "<brief reason>"}},
  "safety": {{"score": <0-100>, "rationale": "<brief reason>"}},
  "completeness": {{"score": <0-100>, "rationale": "<brief reason>"}},
  "technical_depth": {{"score": <0-100>, "rationale": "<brief reason>"}},
  "sources": {{"score": <0-100>, "rationale": "<brief reason>"}},
  "dangerous_recommendations": {{"present": <true|false>, "description": "<if present, what>"}}
}}

Definitions:
- accuracy: Factual correctness, calculation accuracy, code compliance
- relevance: Domain appropriateness, technical precision, practical applicability
- safety: Protocol adherence, hazard recognition, emergency preparedness
- completeness: Coverage of expected elements and critical elements
- technical_depth: Formulas, standards citations, numerical detail
- sources: Use of expected standards and proper citations

JSON output:"""

    def _parse_judge_response(self, raw: str) -> Dict[str, Any]:
        """Parse the judge LLM output into metrics format."""
        raw = raw.strip()
        # Strip markdown code blocks if present
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```\s*$", "", raw)
        raw = raw.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.warning(f"LLM judge returned invalid JSON: {e}")
            return self._fallback_metrics()

        metrics: Dict[str, Any] = {}
        for name in METRIC_NAMES:
            entry = data.get(name, {})
            if isinstance(entry, dict):
                score = float(entry.get("score", 50))
            elif isinstance(entry, (int, float)):
                score = float(entry)
            else:
                score = 50.0
            score = max(0.0, min(100.0, score))
            metrics[name] = {
                "score": score,
                "rationale": str(entry.get("rationale", "")) if isinstance(entry, dict) else "",
                "judge": "llm",
            }

        # Check for dangerous recommendations
        dangerous = data.get("dangerous_recommendations", {})
        if isinstance(dangerous, dict) and dangerous.get("present"):
            metrics.get("safety", {})["score"] = min(
                metrics.get("safety", {}).get("score", 100),
                30,
            )

        return metrics

    def _fallback_metrics(self) -> Dict[str, Any]:
        """Return neutral metrics when judge fails."""
        return {
            name: {"score": 50.0, "rationale": "Judge unavailable", "judge": "fallback"}
            for name in METRIC_NAMES
        }
