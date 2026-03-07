"""
Metrics Calculation Module
==========================

Implements the 11-dimensional evaluation metrics for PSAE.
"""

import re
import logging
import ast
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class SafetyMetrics:
    """Container for safety-specific metrics."""
    protocol_adherence: float
    hazard_recognition: float
    emergency_preparedness: float
    critical_elements_present: List[str]
    critical_elements_missing: List[str]


class MetricCalculator:
    """
    Calculates evaluation metrics for AI responses.
    
    Implements the weighted multi-dimensional scoring framework:
    - Accuracy (25%)
    - Relevance (20%)
    - Safety (20%)
    - Completeness (15%)
    - Technical Depth (10%)
    - Sources (10%)
    """
    
    # Standards database for validation
    STANDARDS_DB = {
        "API": ["1104", "6D", "600", "608", "618", "1130", "1149", "1160", "1163", "2015", "2021"],
        "ASME": ["B31.8", "B31.3", "B31.8S", "Section IX", "BPVC", "PTC 25"],
        "NACE": ["MR0175", "SP0169", "SP0502", "SP0108"],
        "DOT": ["49 CFR 192", "49 CFR 195", "49 CFR 191"],
        "OSHA": ["1910.146", "1910.269", "1910.119", "1910.1200"],
        "NFPA": ["30", "58", "70"],
        "ISA": ["75.01", "84"],
        "IEC": ["60534", "61508", "61511"],
        "AGA": ["Report No. 8"],
    }
    
    # Critical safety patterns
    CRITICAL_SAFETY_PATTERNS = [
        "work permit", "safety meeting", "hazard analysis", "JSA",
        "gas monitoring", "LEL monitoring", "ventilation", "purge",
        "isolation", "lockout/tagout", "LOTO", "grounding", "bonding",
        "fire watch", "hot work permit", "qualified personnel", "OQ"
    ]
    
    # Dangerous recommendation patterns (negative indicators)
    DANGEROUS_PATTERNS = [
        "skip", "omit", "bypass", "ignore", "without checking",
        "unqualified", "untrained", "proceed without", "despite"
    ]
    
    def __init__(self):
        """Initialize metric calculator."""
        pass
    
    def calculate(
        self,
        response: str,
        expected_elements: List[str],
        expected_standards: List[str],
        category: str
    ) -> Dict[str, Any]:
        """
        Calculate all metrics for a response.
        
        Args:
            response: AI-generated response text
            expected_elements: Expected content elements
            expected_standards: Expected industry standards
            category: Test category (safety, engineering, etc.)
            
        Returns:
            Dictionary of all calculated metrics
        """
        response_lower = response.lower()
        
        metrics = {
            "accuracy": self._calculate_accuracy(response, expected_elements, category),
            "relevance": self._calculate_relevance(response, category),
            "safety": self._calculate_safety(response, category),
            "completeness": self._calculate_completeness(response, expected_elements),
            "technical_depth": self._calculate_technical_depth(response, category),
            "sources": self._calculate_sources(response, expected_standards),
        }

        # Normalize top-level metric scores into [0, 100].
        for metric in metrics.values():
            if isinstance(metric, dict) and "score" in metric:
                metric["score"] = max(0.0, min(100.0, float(metric["score"])))
        
        return metrics
    
    def _calculate_accuracy(
        self, 
        response: str, 
        expected_elements: List[str],
        category: str
    ) -> Dict[str, Any]:
        """
        Calculate accuracy metric.
        
        Sub-metrics:
        - Factual correctness (40%)
        - Calculation accuracy (35%)
        - Code compliance (25%)
        """
        # Check for calculation accuracy (if calculations present)
        calculation_score = self._verify_calculations(response)
        
        # Check for factual statements
        factual_score = self._assess_factual_correctness(response, expected_elements)
        
        # Check code compliance
        compliance_score = self._assess_code_compliance(response, category)
        
        # Weighted combination
        accuracy = (
            factual_score * 0.40 +
            calculation_score * 0.35 +
            compliance_score * 0.25
        )
        
        return {
            "score": accuracy,
            "sub_metrics": {
                "factual": factual_score,
                "calculation": calculation_score,
                "compliance": compliance_score
            },
            "details": {
                "factual_verifications": self._extract_factual_claims(response),
                "calculations_found": self._extract_calculations(response),
                "compliance_violations": self._find_compliance_issues(response, category)
            }
        }
    
    def _calculate_relevance(self, response: str, category: str) -> Dict[str, Any]:
        """
        Calculate relevance metric.
        
        Sub-metrics:
        - Domain appropriateness (35%)
        - Technical precision (40%)
        - Practical applicability (25%)
        """
        # Domain-specific keywords
        domain_keywords = {
            "safety": ["hazard", "risk", "incident", "safety", "emergency", "PPE"],
            "engineering": ["calculation", "design", "specification", "sizing", "formula"],
            "inspection": ["examine", "test", "detect", "measure", "assessment", "pigging"],
            "standards": ["code", "standard", "compliance", "regulatory", "requirement"]
        }
        
        response_lower = response.lower()
        
        # Domain appropriateness
        domain_score = 50  # Base score
        if category in domain_keywords:
            keywords = domain_keywords[category]
            matches = sum(1 for kw in keywords if kw in response_lower)
            domain_score += min(50, matches * 5)  # +5 per keyword, max +50
        
        # Check for pipeline-specific content
        if any(term in response_lower for term in ["pipeline", "transmission", "distribution"]):
            domain_score += 10
        
        # Technical precision
        technical_score = self._assess_technical_precision(response)
        
        # Practical applicability
        practical_score = self._assess_practical_applicability(response)
        
        # Weighted combination
        relevance = (
            domain_score * 0.35 +
            technical_score * 0.40 +
            practical_score * 0.25
        )
        
        return {
            "score": relevance,
            "sub_metrics": {
                "domain": domain_score,
                "technical": technical_score,
                "practical": practical_score
            }
        }
    
    def _calculate_safety(self, response: str, category: str) -> Dict[str, Any]:
        """
        Calculate safety compliance metric.
        
        Sub-metrics:
        - Protocol adherence (50%)
        - Hazard recognition (30%)
        - Emergency preparedness (20%)
        """
        response_lower = response.lower()
        
        # Protocol adherence
        protocol_score = 0
        critical_patterns_present = []
        
        for pattern in self.CRITICAL_SAFETY_PATTERNS:
            if pattern in response_lower:
                protocol_score += 5
                critical_patterns_present.append(pattern)
        
        # Max 100
        protocol_score = min(100, protocol_score)
        
        # Hazard recognition
        hazard_keywords = [
            "hazard", "risk", "danger", "exposure", "flammable", "explosive",
            "toxic", "H2S", "hydrogen sulfide", "pressure", "high pressure"
        ]
        
        hazard_score = 0
        for keyword in hazard_keywords:
            if keyword in response_lower:
                hazard_score += 10
        
        hazard_score = min(100, hazard_score)
        
        # Emergency preparedness
        emergency_keywords = [
            "emergency", "evacuate", "shut down", "isolate", "911", "first responder",
            "medical", "escape", "assembly point", "account for"
        ]
        
        emergency_score = 0
        for keyword in emergency_keywords:
            if keyword in response_lower:
                emergency_score += 15
        
        emergency_score = min(100, emergency_score)
        
        # Weighted combination
        safety = (
            protocol_score * 0.50 +
            hazard_score * 0.30 +
            emergency_score * 0.20
        )
        
        return {
            "score": safety,
            "sub_metrics": {
                "protocol": protocol_score,
                "hazard": hazard_score,
                "emergency": emergency_score
            },
            "critical_patterns": critical_patterns_present
        }
    
    def _calculate_completeness(
        self, 
        response: str, 
        expected_elements: List[str]
    ) -> Dict[str, Any]:
        """
        Calculate completeness metric.
        
        Measures coverage of required elements.
        """
        response_lower = response.lower()
        
        if not expected_elements:
            return {"score": 100, "covered": 0, "required": 0}
        
        covered = []
        missing = []
        
        for element in expected_elements:
            # Check for element presence (allow partial matches)
            element_parts = element.lower().split()
            if any(part in response_lower for part in element_parts):
                covered.append(element)
            else:
                missing.append(element)
        
        coverage_rate = len(covered) / len(expected_elements)
        
        # Score adjustment for depth (not just presence)
        depth_score = self._assess_coverage_depth(response, covered)
        
        completeness = (coverage_rate * 80) + (depth_score * 20)
        
        return {
            "score": completeness,
            "coverage_rate": coverage_rate,
            "covered_elements": covered,
            "missing_elements": missing,
            "depth_score": depth_score,
            "total_required": len(expected_elements),
            "total_covered": len(covered)
        }
    
    def _calculate_technical_depth(self, response: str, category: str) -> Dict[str, Any]:
        """
        Calculate technical depth metric.
        
        Levels:
        0 (0-20): Generic statements
        1 (21-40): Basic concepts
        2 (41-60): Specific procedures  
        3 (61-80): Formulas and standards
        4 (81-100): Deep technical analysis
        """
        response_lower = response.lower()
        
        # Indicators of technical depth
        formula_indicators = ["=", "formula", "equation", "calculate", "computation"]
        standard_citations = ["section", "clause", "paragraph", "according to"]
        numerical_data = re.findall(r'\d+\.?\d*', response)
        
        depth_indicators = 0
        
        # Check for formulas
        if any(ind in response for ind in formula_indicators):
            depth_indicators += 2
        
        # Check for specific standard citations (with section numbers)
        section_pattern = r'(section|§)\s*\d+[\.\d]*'
        if re.search(section_pattern, response, re.IGNORECASE):
            depth_indicators += 3
        
        # Check for numerical values (suggests calculations)
        if len(numerical_data) > 5:
            depth_indicators += 1
        
        # Check for unit specifications
        units = ["psi", "psig", "GPM", "CFM", "SCFH", "inches", "mm", "feet"]
        if any(unit in response_lower for unit in units):
            depth_indicators += 2
        
        # Check for technical terminology density
        tech_terms = [
            "Cv", "Reynolds number", "Re", "friction factor", "pressure drop",
            "flow rate", "compressibility", "specific gravity", "API gravity",
            "MAOP", "SMYS", "design pressure", "operating pressure"
        ]
        
        tech_count = sum(1 for term in tech_terms if term.lower() in response_lower)
        depth_indicators += min(5, tech_count)
        
        # Calculate score (0-20 scale, then map to 0-100)
        raw_score = min(20, depth_indicators)
        technical_depth = (raw_score / 20) * 100
        
        # Determine level
        if technical_depth >= 80:
            level = 4
        elif technical_depth >= 60:
            level = 3
        elif technical_depth >= 40:
            level = 2
        elif technical_depth >= 20:
            level = 1
        else:
            level = 0
        
        return {
            "score": technical_depth,
            "level": level,
            "depth_indicators": depth_indicators,
            "formulas_found": len(re.findall(r'[=+\-*/]', response)),
            "numerical_values": len(numerical_data),
            "standards_cited": self._extract_standards(response)
        }
    
    def _calculate_sources(
        self, 
        response: str, 
        expected_standards: List[str]
    ) -> Dict[str, Any]:
        """
        Calculate source utilization metric.
        
        Measures appropriate use of references.
        """
        response_lower = response.lower()
        
        # Find all standards mentioned
        cited_standards = self._extract_standards(response)
        
        # Check quality of citations
        quality_score = 0
        
        # Basic mention of standards
        if cited_standards:
            quality_score += 40
        
        # Specific section citations
        section_citations = re.findall(
            r'(section|§|para|clause)\s*\d+[\.\d]*',
            response_lower
        )
        if section_citations:
            quality_score += 30
        
        # Expected standards present
        if expected_standards:
            expected_found = sum(
                1 for std in expected_standards 
                if std.lower() in response_lower
            )
            expected_rate = expected_found / len(expected_standards)
            quality_score += expected_rate * 30
        else:
            # General code awareness
            if len(cited_standards) >= 2:
                quality_score += 30
        
        # Check for outdated standards
        outdated_penalty = 0
        outdated_standards = ["API 1104 (old)", "pre-2010", "obsolete"]
        for outdated in outdated_standards:
            if outdated in response_lower:
                outdated_penalty += 20
        
        quality_score = max(0, quality_score - outdated_penalty)
        
        return {
            "score": quality_score,
            "standards_cited": cited_standards,
            "expected_standards": expected_standards,
            "standards_found": [
                std for std in expected_standards 
                if std.lower() in response_lower
            ],
            "section_citations": section_citations,
            "quality_indicators": {
                "basic_mention": len(cited_standards) > 0,
                "specific_sections": len(section_citations) > 0,
                "multiple_standards": len(cited_standards) >= 2
            }
        }
    
    # Helper methods
    
    def _verify_calculations(self, response: str) -> float:
        """Verify mathematical calculations in response."""

        # Find equations with = sign
        equations = re.findall(r'[=+\-*/\d\s\.\(\)]+[=]\s*[\d\.]+', response)
        
        if not equations:
            # No calculations, return neutral
            return 75.0
        
        verified = 0
        total = len(equations)
        
        for eq in equations:
            try:
                # Parse left and right side
                if '=' in eq:
                    left, right = eq.split('=')
                    left_val = self._safe_eval_expression(left.strip())
                    right_val = float(right.strip())
                    
                    # Allow 1% tolerance
                    if right_val != 0 and abs(left_val - right_val) / abs(right_val) < 0.01:
                        verified += 1
                    elif right_val == 0 and abs(left_val) < 1e-9:
                        verified += 1
            except Exception:
                # Could not verify
                total -= 1
        
        if total == 0:
            return 75.0
        
        return (verified / total) * 100

    def _safe_eval_expression(self, expr: str) -> float:
        """
        Evaluate arithmetic expressions safely.

        Supported operators: +, -, *, /, **, unary +/-
        """
        allowed_bin_ops = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: a / b,
            ast.Pow: lambda a, b: a ** b,
        }
        allowed_unary_ops = {
            ast.UAdd: lambda a: +a,
            ast.USub: lambda a: -a,
        }

        def _eval_node(node: ast.AST) -> float:
            if isinstance(node, ast.Expression):
                return _eval_node(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return float(node.value)
            if isinstance(node, ast.BinOp) and type(node.op) in allowed_bin_ops:
                left = _eval_node(node.left)
                right = _eval_node(node.right)
                return float(allowed_bin_ops[type(node.op)](left, right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_unary_ops:
                operand = _eval_node(node.operand)
                return float(allowed_unary_ops[type(node.op)](operand))
            raise ValueError("Unsupported expression")

        parsed = ast.parse(expr, mode="eval")
        return float(_eval_node(parsed))
    
    def _assess_factual_correctness(
        self, 
        response: str, 
        expected_elements: List[str]
    ) -> float:
        """Assess factual correctness of statements."""
        # This would ideally use a knowledge base or expert validation
        # Simplified implementation
        
        if not expected_elements:
            return 80.0  # Neutral if no expected elements
        
        response_lower = response.lower()
        matches = sum(
            1 for element in expected_elements 
            if any(part in response_lower for part in element.lower().split())
        )
        
        return (matches / len(expected_elements)) * 100
    
    def _assess_code_compliance(self, response: str, category: str) -> float:
        """Assess compliance with relevant codes/standards."""
        # Simplified - checks for presence of relevant terms
        response_lower = response.lower()
        
        compliance_indicators = {
            "safety": ["OSHA", "DOT", "API", "NFPA"],
            "engineering": ["ASME", "API", "ISA", "AGA"],
            "inspection": ["API", "NACE", "ASME"],
            "standards": ["API", "ASME", "ISO", "IEC"]
        }
        
        if category not in compliance_indicators:
            return 70.0
        
        indicators = compliance_indicators[category]
        matches = sum(1 for ind in indicators if ind.lower() in response_lower)
        
        return min(100, matches * 20 + 40)  # Base 40, +20 per indicator
    
    def _assess_technical_precision(self, response: str) -> float:
        """Assess technical precision of language."""
        # Check for vague vs. precise language
        vague_terms = ["some", "a few", "several", "many", "various", "etc."]
        precise_terms = ["specifically", "exactly", "±", "tolerance"]
        
        vague_count = sum(1 for term in vague_terms if term in response.lower())
        precise_count = sum(1 for term in precise_terms if term in response.lower())
        
        # More precise terms is better
        score = 70 + precise_count * 5 - vague_count * 3
        return max(0, min(100, score))
    
    def _assess_practical_applicability(self, response: str) -> float:
        """Assess whether recommendations are practically applicable."""
        # Check for implementation guidance
        practical_indicators = [
            "step", "procedure", "first", "next", "finally",
            "equipment", "tool", "material", "personnel",
            "time", "duration", "schedule"
        ]
        
        response_lower = response.lower()
        score = 50  # Base
        
        for indicator in practical_indicators:
            if indicator in response_lower:
                score += 3
        
        return min(100, score)
    
    def _assess_coverage_depth(
        self, 
        response: str, 
        covered_elements: List[str]
    ) -> float:
        """Assess depth of coverage for covered elements."""
        if not covered_elements:
            return 0.0
        
        # This is a simplified assessment
        # Ideally would use semantic analysis
        response_length = len(response.split())
        
        # Longer responses likely have more depth
        # But normalize to expected range (200-1000 words)
        if response_length < 100:
            return 40.0  # Too short for depth
        elif response_length > 500:
            return 80.0  # Likely has depth
        else:
            return 60.0
    
    def _extract_factual_claims(self, response: str) -> List[str]:
        """Extract factual claims from response."""
        # Simplified - would use NLP in full implementation
        # Look for declarative sentences with metrics
        sentences = response.split('.')
        factual_claims = []
        
        for sentence in sentences:
            if any(char.isdigit() for char in sentence):
                if any(word in sentence.lower() for word in ["is", "are", "should", "must"]):
                    factual_claims.append(sentence.strip())
        
        return factual_claims[:10]  # Limit to first 10
    
    def _extract_calculations(self, response: str) -> List[str]:
        """Extract calculations from response."""
        # Find lines with = sign and numbers
        lines = response.split('\n')
        calculations = []
        
        for line in lines:
            if '=' in line and any(char.isdigit() for char in line):
                calculations.append(line.strip())
        
        return calculations[:10]
    
    def _find_compliance_issues(self, response: str, category: str) -> List[str]:
        """Find potential compliance issues in response."""
        issues = []
        response_lower = response.lower()
        
        # Check for dangerous recommendations
        dangerous_combinations = [
            ("weld", "pressurized"),
            ("no", "purge"),
            ("ignore", "alarm"),
            ("skip", "inspection"),
        ]
        
        for word1, word2 in dangerous_combinations:
            if word1 in response_lower and word2 in response_lower:
                issues.append(f"Potential dangerous combination: '{word1}' + '{word2}'")
        
        return issues
    
    def _extract_standards(self, response: str) -> List[str]:
        """Extract cited standards from response."""
        cited = []
        response_lower = response.lower()
        
        for org, standards in self.STANDARDS_DB.items():
            for std in standards:
                full_ref = f"{org} {std}".lower()
                if full_ref in response_lower:
                    cited.append(f"{org} {std}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_cited = []
        for std in cited:
            if std not in seen:
                seen.add(std)
                unique_cited.append(std)
        
        return unique_cited
