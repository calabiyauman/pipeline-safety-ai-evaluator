"""
Public package namespace for Pipeline Safety AI Evaluator (PSAE).
"""

from core.evaluator import PipelineSafetyEvaluator
from core.metrics import MetricCalculator, SafetyMetrics
from core.statistical import StatisticalAnalyzer
from scenarios.base import TestScenario, TestSuite
from models.ai_interface import AIModelInterface

__version__ = "0.1.0"
__author__ = "Pipeline AI Solutions LLC"
__license__ = "MIT"

__all__ = [
    "PipelineSafetyEvaluator",
    "MetricCalculator",
    "SafetyMetrics",
    "StatisticalAnalyzer",
    "TestScenario",
    "TestSuite",
    "AIModelInterface",
]
