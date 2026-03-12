"""
Pipeline Safety AI Evaluator (PSAE) - Core Implementation
=========================================================

A rigorous evaluation framework for AI systems in pipeline safety-critical
applications. Based on peer-reviewed methodologies from NIST AI RMF, METR,
and safety-critical systems research.

Author: Pipeline AI Solutions Research Team
License: MIT
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Pipeline AI Solutions LLC"
__license__ = "MIT"

from .core.evaluator import PipelineSafetyEvaluator
from .core.metrics import MetricCalculator, SafetyMetrics
from .core.statistical import StatisticalAnalyzer
from .scenarios.base import TestScenario, TestSuite
from .models.ai_interface import AIModelInterface

__all__ = [
    "PipelineSafetyEvaluator",
    "MetricCalculator",
    "SafetyMetrics",
    "StatisticalAnalyzer",
    "TestScenario",
    "TestSuite",
    "AIModelInterface",
]

# Framework metadata
FRAMEWORK_INFO = {
    "name": "Pipeline Safety AI Evaluator",
    "version": "0.1.0",
    "status": "Beta",
    "target_domain": "Pipeline Safety-Critical Applications",
    "evaluation_dimensions": 11,
    "test_case_library": 24,
    "abnormal_conditions": 50,
    "statistical_confidence": 0.95,
    "min_runs": 5,
    "risk_categories": ["Critical", "High", "Standard", "Low"],
}

# Supported models
SUPPORTED_MODELS = [
    "gpt-4",
    "gpt-4-turbo",
    "claude-3-5-sonnet",
    "claude-3-opus",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]

# Evaluation standards
STANDARDS_DB = {
    "API": ["1104", "6D", "600", "608", "618", "1130", "1149", "1160", "1163", "2015", "2021"],
    "ASME": ["B31.8", "B31.8S", "Section IX", "BPVC"],
    "NACE": ["MR0175", "SP0169", "SP0502"],
    "DOT": ["49 CFR 192", "49 CFR 195"],
    "OSHA": ["1910.146", "1910.269", "1910.119"],
    "NFPA": ["30", "58", "70"],
    "ISA": ["75.01"],
    "IEC": ["60534"],
}
