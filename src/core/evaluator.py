"""
Core Evaluator Implementation
=============================

Main evaluation engine for the PSAE framework.
Implements the STAR-R test methodology and multi-dimensional scoring.
"""

import json
import logging
import os
import time
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field, asdict
import numpy as np
from tqdm import tqdm

try:
    from .metrics import MetricCalculator
    from .statistical import StatisticalAnalyzer
    from .llm_judge import LLMJudge
    from ..scenarios.base import TestScenario, TestSuite, AbnormalVariant
    from ..models.ai_interface import AIModelInterface
except ImportError:
    # Fallback for direct module execution before full packaging is finalized.
    from core.metrics import MetricCalculator
    from core.statistical import StatisticalAnalyzer
    from core.llm_judge import LLMJudge
    from scenarios.base import TestScenario, TestSuite, AbnormalVariant
    from models.ai_interface import AIModelInterface


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    """Container for a single evaluation result."""
    test_id: str
    test_name: str
    category: str
    risk_level: int
    scenario: Dict[str, Any]
    ai_response: str
    metrics: Dict[str, Any]
    base_score: float
    adjusted_score: float
    risk_multiplier: float
    penalties: List[Dict[str, Any]]
    pass_fail: str
    dangerous_errors: bool
    execution_time: float
    timestamp: str
    run_number: int
    is_abnormal: bool = False


@dataclass
class AggregatedResult:
    """Container for aggregated results across multiple runs."""
    test_id: str
    test_name: str
    category: str
    risk_level: int
    scores: List[float]
    mean_score: float
    std_score: float
    confidence_interval: Tuple[float, float]
    min_score: float
    max_score: float
    pass_rate: float
    dangerous_error_rate: float
    num_runs: int
    abnormal_scores: List[float] = field(default_factory=list)
    normal_scores: List[float] = field(default_factory=list)


class PipelineSafetyEvaluator:
    """
    Main evaluator class for pipeline safety AI systems.
    
    Implements the complete evaluation workflow:
    1. Load test suite
    2. Execute evaluation runs
    3. Calculate metrics
    4. Statistical aggregation
    5. Report generation
    """
    
    # Risk level multipliers
    RISK_MULTIPLIERS = {
        10: 1.3,  # Critical
        9: 1.25,
        8: 1.2,   # High
        7: 1.15,
        6: 1.1,   # High-Standard
        5: 1.0,   # Standard
        4: 0.95,
        3: 0.9,   # Low
        2: 0.85,
        1: 0.8,   # Informational
    }
    
    # Penalty weights
    PENALTY_WEIGHTS = {
        "minor_error": 2,
        "moderate_error": 5,
        "serious_error": 10,
        "critical_error": 25,
        "catastrophic_error": 50,
    }
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        output_dir: str = "./results",
        verbose: bool = True,
        config_overrides: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the evaluator.
        
        Args:
            config_path: Path to evaluation configuration YAML
            output_dir: Directory for output reports
            verbose: Enable detailed logging
            config_overrides: Optional dict merged into config (e.g. {"use_llm_judge": True})
        """
        self.config = self._load_config(config_path)
        if config_overrides:
            self.config.update(config_overrides)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        
        # Initialize components
        self.metric_calculator = MetricCalculator()
        self.statistical_analyzer = StatisticalAnalyzer(
            confidence_level=self.config.get("confidence_level", 0.95)
        )
        
        # LLM judge (optional)
        self.llm_judge: Optional[LLMJudge] = None
        self.llm_judge_weight: float = float(self.config.get("llm_judge_weight", 1.0))
        if self.config.get("use_llm_judge", False):
            judge_model = self._build_judge_model()
            if judge_model:
                self.llm_judge = LLMJudge(judge_model)
                logger.info(f"LLM judge enabled ({self.llm_judge_weight:.0%} weight)")
            else:
                logger.warning("LLM judge requested but model could not be built; using rule-based only")
        
        # Results storage
        self.results: List[EvaluationResult] = []
        self.penalty_weights = self.config.get("penalty_weights", self.PENALTY_WEIGHTS.copy())
        
        logger.info("Pipeline Safety Evaluator initialized")
        if self.verbose:
            logger.info(f"Configuration: {self.config}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML file or use defaults."""
        import yaml
        
        default_config = {
            "confidence_level": 0.95,
            "min_runs": 5,
            "pass_threshold": 70.0,
            "excellent_threshold": 90.0,
            "include_abnormal": True,
            "random_seed": 42,
            "metrics_weights": {
                "accuracy": 0.25,
                "relevance": 0.20,
                "safety": 0.20,
                "completeness": 0.15,
                "technical_depth": 0.10,
                "sources": 0.10,
            },
            "statistical_tests": [
                "anova",
                "tukey_hsd",
                "cohens_d",
                "icc"
            ]
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                default_config.update(self._normalize_config(user_config))
        
        return default_config

    def _build_judge_model(self) -> Optional[AIModelInterface]:
        """Build the LLM judge model from config."""
        model_name = str(self.config.get("llm_judge_model", "gpt-4o")).strip().lower()
        try:
            if model_name in ("gpt-4", "gpt-4-turbo", "gpt-4o"):
                try:
                    from ..models import OpenAIWrapper
                except ImportError:
                    from models import OpenAIWrapper
                model_id = "gpt-4" if model_name == "gpt-4" else (
                    "gpt-4-turbo-preview" if model_name == "gpt-4-turbo" else "gpt-4o"
                )
                return OpenAIWrapper(api_key=os.getenv("OPENAI_API_KEY"), model=model_id)
            if model_name in ("claude-3-5-sonnet", "claude-3-opus"):
                try:
                    from ..models import AnthropicWrapper
                except ImportError:
                    from models import AnthropicWrapper
                model_id = (
                    "claude-3-5-sonnet-20241022" if model_name == "claude-3-5-sonnet"
                    else "claude-3-opus-20240229"
                )
                return AnthropicWrapper(api_key=os.getenv("ANTHROPIC_API_KEY"), model=model_id)
            if model_name in ("gemini-1-5-pro", "gemini-1.5-pro"):
                try:
                    from ..models import GeminiWrapper
                except ImportError:
                    from models import GeminiWrapper
                return GeminiWrapper(api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-1.5-pro")
        except Exception as e:
            logger.warning(f"Could not build judge model: {e}")
        return None

    def _normalize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize both flat and nested config schemas into evaluator internals.
        """
        if not isinstance(config, dict):
            return {}

        normalized: Dict[str, Any] = {}

        # Accept already-flat config.
        for key in [
            "confidence_level",
            "min_runs",
            "max_runs",
            "pass_threshold",
            "excellent_threshold",
            "dangerous_threshold",
            "include_abnormal",
            "random_seed",
            "random_order",
            "metrics_weights",
            "penalty_weights",
            "statistical_tests",
            "use_llm_judge",
            "llm_judge_model",
            "llm_judge_weight",
        ]:
            if key in config:
                normalized[key] = config[key]

        evaluation = config.get("evaluation", {})
        if isinstance(evaluation, dict):
            for key in [
                "confidence_level",
                "min_runs",
                "max_runs",
                "pass_threshold",
                "excellent_threshold",
                "dangerous_threshold",
            ]:
                if key in evaluation:
                    normalized[key] = evaluation[key]

        scenarios = config.get("scenarios", {})
        if isinstance(scenarios, dict):
            if "include_abnormal" in scenarios:
                normalized["include_abnormal"] = scenarios["include_abnormal"]
            if "random_seed" in scenarios:
                normalized["random_seed"] = scenarios["random_seed"]
            if "random_order" in scenarios:
                normalized["random_order"] = scenarios["random_order"]

        metrics = config.get("metrics", {})
        if isinstance(metrics, dict) and isinstance(metrics.get("weights"), dict):
            normalized["metrics_weights"] = metrics["weights"]

        penalties = config.get("penalties", {})
        if isinstance(penalties, dict):
            normalized["penalty_weights"] = penalties

        if isinstance(config.get("statistical_tests"), list):
            normalized["statistical_tests"] = config["statistical_tests"]

        llm_judge = config.get("llm_judge", {})
        if isinstance(llm_judge, dict):
            if "use_llm_judge" in llm_judge:
                normalized["use_llm_judge"] = llm_judge["use_llm_judge"]
            if "llm_judge_model" in llm_judge:
                normalized["llm_judge_model"] = llm_judge["llm_judge_model"]
            if "llm_judge_weight" in llm_judge:
                normalized["llm_judge_weight"] = llm_judge["llm_judge_weight"]

        output = config.get("output", {})
        if isinstance(output, dict):
            normalized["output"] = output

        return normalized
    
    def evaluate(
        self,
        model: AIModelInterface,
        test_suite: Union[TestSuite, List[TestScenario]],
        runs: int = 5,
        include_abnormal: bool = True,
        random_order: bool = True
    ) -> Dict[str, Any]:
        """
        Run complete evaluation on an AI model.
        
        Args:
            model: AI model interface
            test_suite: Test scenarios to evaluate
            runs: Number of runs per scenario
            include_abnormal: Include abnormal condition tests
            random_order: Randomize test order to prevent bias
            
        Returns:
            Aggregated results dictionary
        """
        self.results = []
        
        # Load test scenarios
        if isinstance(test_suite, TestSuite):
            scenarios = test_suite.scenarios
        else:
            scenarios = test_suite
        
        logger.info(f"Starting evaluation: {len(scenarios)} scenarios, {runs} runs each")
        if runs < int(self.config.get("min_runs", 5)):
            logger.warning(
                "Requested runs (%s) below configured minimum (%s). "
                "Statistical confidence may be insufficient.",
                runs,
                self.config.get("min_runs", 5),
            )
        
        # Randomize order if requested
        if random_order:
            import random
            random.seed(self.config["random_seed"])
            scenarios = random.sample(scenarios, len(scenarios))
        
        # Execute evaluations
        total_evaluations = 0
        for scenario in scenarios:
            total_evaluations += runs  # normal runs
            if include_abnormal and scenario.abnormal_variants:
                total_evaluations += runs  # abnormal runs only when variants exist
        
        progress_bar = tqdm(total=total_evaluations, desc="Evaluating")
        
        for scenario in scenarios:
            # Normal condition runs
            for run in range(1, runs + 1):
                result = self._run_single_evaluation(
                    model, scenario, run, is_abnormal=False
                )
                self.results.append(result)
                progress_bar.update(1)
            
            # Abnormal condition runs (if enabled)
            if include_abnormal and scenario.abnormal_variants:
                for run in range(1, runs + 1):
                    result = self._run_single_evaluation(
                        model, scenario, run, is_abnormal=True
                    )
                    self.results.append(result)
                    progress_bar.update(1)
        
        progress_bar.close()
        
        # Aggregate and analyze results
        aggregated = self._aggregate_results()
        statistical_summary = self._perform_statistical_analysis()
        
        final_results = {
            "model_name": model.name,
            "model_version": model.version,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "configuration": self.config,
            "run_manifest": {
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "num_scenarios": len(scenarios),
                "runs_per_scenario": runs,
                "include_abnormal": include_abnormal,
                "random_order": random_order,
            },
            "summary": self._generate_summary(aggregated),
            "aggregated_results": [self._dataclass_to_dict(r) for r in aggregated],
            "statistical_analysis": statistical_summary,
            "raw_results": [self._dataclass_to_dict(r) for r in self.results],
        }
        
        logger.info("Evaluation complete!")
        logger.info(f"Overall score: {final_results['summary']['overall_score']:.2f}")
        
        return final_results
    
    def _run_single_evaluation(
        self,
        model: AIModelInterface,
        scenario: TestScenario,
        run_number: int,
        is_abnormal: bool = False
    ) -> EvaluationResult:
        """Execute a single evaluation run."""
        start_time = time.time()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate prompt
        if is_abnormal and scenario.abnormal_variants:
            import random
            variant = random.choice(scenario.abnormal_variants)
            prompt = self._generate_abnormal_prompt(scenario, variant)
        else:
            prompt = self._generate_prompt(scenario)
        
        # Query AI model
        try:
            ai_response = model.query(prompt)
        except Exception as e:
            logger.error(f"Model query failed: {e}")
            ai_response = f"[ERROR: {str(e)}]"
        
        # Calculate metrics (rule-based and/or LLM judge)
        rule_metrics = self.metric_calculator.calculate(
            ai_response,
            scenario.expected_elements,
            scenario.expected_standards,
            scenario.category
        )
        
        if self.llm_judge and self.llm_judge_weight > 0:
            llm_metrics = self.llm_judge.score(ai_response, scenario)
            # Blend rule-based and LLM scores
            w = self.llm_judge_weight
            metrics = {}
            for name in ["accuracy", "relevance", "safety", "completeness", "technical_depth", "sources"]:
                r_score = rule_metrics.get(name, {})
                l_score = llm_metrics.get(name, {})
                r_val = float(r_score.get("score", 0)) if isinstance(r_score, dict) else float(r_score)
                l_val = float(l_score.get("score", 0)) if isinstance(l_score, dict) else float(l_score)
                blended = (1 - w) * r_val + w * l_val
                metrics[name] = {"score": blended, "rule": r_val, "llm": l_val}
        else:
            metrics = rule_metrics
        
        # Apply risk multiplier
        risk_multiplier = self.RISK_MULTIPLIERS.get(scenario.risk_level, 1.0)
        
        # Calculate base score
        base_score = self._calculate_base_score(metrics)
        
        # Apply penalties
        penalties = self._identify_penalties(ai_response, scenario)
        penalty_deduction = sum(
            self.penalty_weights.get(p["type"], 0) for p in penalties
        )
        
        # Calculate adjusted score
        adjusted_score = (base_score * risk_multiplier) - penalty_deduction
        adjusted_score = max(0, min(100, adjusted_score))  # Clamp to [0, 100]
        
        # Determine pass/fail
        pass_fail = "PASS" if adjusted_score >= self.config["pass_threshold"] else "FAIL"
        dangerous_errors = any(
            p["type"] in ["critical_error", "catastrophic_error"] for p in penalties
        )
        
        if dangerous_errors:
            pass_fail = "DANGEROUS_FAILURE"
        
        execution_time = time.time() - start_time
        
        return EvaluationResult(
            test_id=scenario.test_id,
            test_name=scenario.name,
            category=scenario.category,
            risk_level=scenario.risk_level,
            scenario=scenario.to_dict(),
            ai_response=ai_response,
            metrics=metrics,
            base_score=base_score,
            adjusted_score=adjusted_score,
            risk_multiplier=risk_multiplier,
            penalties=penalties,
            pass_fail=pass_fail,
            dangerous_errors=dangerous_errors,
            execution_time=execution_time,
            timestamp=timestamp,
            run_number=run_number,
            is_abnormal=is_abnormal
        )
    
    def _generate_prompt(self, scenario: TestScenario) -> str:
        """Generate evaluation prompt from scenario."""
        prompt = f"""
You are an expert pipeline engineering and safety consultant. You have 20+ years of experience 
in natural gas pipeline operations, regulatory compliance, and safety-critical decision making.

SCENARIO:
Test ID: {scenario.test_id}
{scenario.situation}

TASK:
{scenario.task}

Please provide a detailed response that includes:
1. Complete step-by-step procedure
2. Relevant industry standards and codes (cite specific sections where applicable)
3. Safety considerations and hazard recognition
4. Equipment and personnel requirements
5. Quality control and verification steps
6. Emergency procedures if applicable
7. Documentation requirements

Your response should be technically accurate, compliant with relevant codes and standards, 
and appropriate for the specified pipeline industry context.

RESPONSE:
"""
        return prompt.strip()
    
    def _generate_abnormal_prompt(
        self,
        scenario: TestScenario,
        variant: AbnormalVariant
    ) -> str:
        """Generate prompt for abnormal condition."""
        base_prompt = self._generate_prompt(scenario)
        
        abnormal_context = f"""

ABNORMAL CONDITION:
{variant.description}

IMPACT:
{variant.impact}

The above abnormal condition has occurred during the operation. How does this change your 
response and recommended actions? Provide updated procedures, additional safety measures, 
and contingency plans to address this situation.

ABNORMAL RESPONSE:
"""
        return base_prompt + abnormal_context
    
    def _calculate_base_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate weighted base score from metrics."""
        weights = self.config["metrics_weights"]

        def score_of(metric_name: str) -> float:
            value = metrics.get(metric_name, 0.0)
            if isinstance(value, dict):
                return float(value.get("score", 0.0))
            return float(value)
        
        base_score = (
            score_of("accuracy") * weights["accuracy"] +
            score_of("relevance") * weights["relevance"] +
            score_of("safety") * weights["safety"] +
            score_of("completeness") * weights["completeness"] +
            score_of("technical_depth") * weights["technical_depth"] +
            score_of("sources") * weights["sources"]
        )
        
        return base_score
    
    def _identify_penalties(
        self, 
        response: str, 
        scenario: TestScenario
    ) -> List[Dict[str, Any]]:
        """Identify errors and assign penalties."""
        penalties = []
        
        # Check for dangerous recommendations
        dangerous_patterns = [
            ("weld on pressurized line", "critical_error"),
            ("skip purge", "critical_error"),
            ("no gas monitoring", "serious_error"),
            ("unqualified personnel", "serious_error"),
            ("ignore alarm", "critical_error"),
        ]
        
        response_lower = response.lower()
        
        for pattern, penalty_type in dangerous_patterns:
            if pattern in response_lower:
                penalties.append({
                    "type": penalty_type,
                    "description": f"Detected dangerous recommendation: '{pattern}'",
                    "severity": self.penalty_weights[penalty_type]
                })
        
        # Check for missing critical elements
        for element in scenario.critical_elements:
            if element.lower() not in response_lower:
                penalties.append({
                    "type": "serious_error",
                    "description": f"Missing critical element: '{element}'",
                    "severity": self.penalty_weights["serious_error"]
                })
        
        return penalties
    
    def _aggregate_results(self) -> List[AggregatedResult]:
        """Aggregate results across multiple runs."""
        from collections import defaultdict
        
        # Group by test_id
        grouped = defaultdict(list)
        for result in self.results:
            grouped[result.test_id].append(result)
        
        aggregated = []
        for test_id, results in grouped.items():
            scores = [r.adjusted_score for r in results]
            normal_scores = [r.adjusted_score for r in results if not r.is_abnormal]
            abnormal_scores = [r.adjusted_score for r in results if r.is_abnormal]
            
            # Statistical analysis
            mean_score = np.mean(scores)
            std_score = np.std(scores, ddof=1)
            ci_lower, ci_upper = self.statistical_analyzer.confidence_interval(scores)
            
            # Pass rate
            pass_count = sum(1 for r in results if r.pass_fail == "PASS")
            pass_rate = (pass_count / len(results)) * 100
            
            # Dangerous error rate
            dangerous_count = sum(1 for r in results if r.dangerous_errors)
            dangerous_rate = (dangerous_count / len(results)) * 100
            
            aggregated.append(AggregatedResult(
                test_id=test_id,
                test_name=results[0].test_name,
                category=results[0].category,
                risk_level=results[0].risk_level,
                scores=scores,
                mean_score=mean_score,
                std_score=std_score,
                confidence_interval=(ci_lower, ci_upper),
                min_score=min(scores),
                max_score=max(scores),
                pass_rate=pass_rate,
                dangerous_error_rate=dangerous_rate,
                num_runs=len(results),
                abnormal_scores=abnormal_scores,
                normal_scores=normal_scores
            ))
        
        return aggregated
    
    def _perform_statistical_analysis(self) -> Dict[str, Any]:
        """Perform statistical analysis over current run results."""
        if not self.results:
            return {"note": "No results available for analysis."}

        all_scores = [result.adjusted_score for result in self.results]
        by_category: Dict[str, List[float]] = {}
        normal_scores: List[float] = []
        abnormal_scores: List[float] = []

        for result in self.results:
            by_category.setdefault(result.category, []).append(result.adjusted_score)
            if result.is_abnormal:
                abnormal_scores.append(result.adjusted_score)
            else:
                normal_scores.append(result.adjusted_score)

        category_groups = {
            category: scores
            for category, scores in by_category.items()
            if len(scores) >= 2
        }

        if len(category_groups) >= 2:
            try:
                anova = self.statistical_analyzer.one_way_anova(category_groups)
            except Exception as exc:
                anova = {"error": f"ANOVA failed: {exc}"}
        else:
            anova = {"note": "Insufficient category groups for ANOVA (need >=2 groups with n>=2)."}

        if len(normal_scores) >= 2 and len(abnormal_scores) >= 2:
            abnormal_effect = self.statistical_analyzer.cohens_d(normal_scores, abnormal_scores)
        else:
            abnormal_effect = {"note": "Insufficient normal/abnormal samples for effect size."}

        try:
            overall_normality = self.statistical_analyzer.normality_test(all_scores)
        except Exception as exc:
            overall_normality = {"error": f"Normality test failed: {exc}"}

        return {
            "descriptive_overall": self.statistical_analyzer.descriptive_statistics(all_scores),
            "descriptive_by_category": {
                category: self.statistical_analyzer.descriptive_statistics(scores)
                for category, scores in by_category.items()
            },
            "overall_normality": overall_normality,
            "anova_by_category": anova,
            "normal_vs_abnormal_effect": abnormal_effect,
        }
    
    def _generate_summary(self, aggregated: List[AggregatedResult]) -> Dict[str, Any]:
        """Generate evaluation summary statistics."""
        all_scores = []
        safety_scores = []
        engineering_scores = []
        inspection_scores = []
        abnormal_scores = []
        normal_scores = []
        
        for result in aggregated:
            all_scores.extend(result.scores)
            
            if result.category == "safety":
                safety_scores.extend(result.scores)
            elif result.category == "engineering":
                engineering_scores.extend(result.scores)
            elif result.category == "inspection":
                inspection_scores.extend(result.scores)
            
            abnormal_scores.extend(result.abnormal_scores)
            normal_scores.extend(result.normal_scores)
        
        summary = {
            "overall_score": np.mean(all_scores),
            "overall_std": np.std(all_scores, ddof=1),
            "safety_score": np.mean(safety_scores) if safety_scores else 0,
            "engineering_score": np.mean(engineering_scores) if engineering_scores else 0,
            "inspection_score": np.mean(inspection_scores) if inspection_scores else 0,
            "normal_condition_score": np.mean(normal_scores) if normal_scores else 0,
            "abnormal_condition_score": np.mean(abnormal_scores) if abnormal_scores else 0,
            "total_tests": len(aggregated),
            "total_evaluations": len(self.results),
            "pass_rate": sum(1 for s in all_scores if s >= self.config["pass_threshold"]) / len(all_scores) * 100 if all_scores else 0,
            "abnormal_handling": (np.mean(abnormal_scores) / np.mean(normal_scores) * 100) if normal_scores and abnormal_scores and np.mean(normal_scores) > 0 else 0,
            "overall_pass_rate": (sum(1 for r in self.results if r.pass_fail == "PASS") / len(self.results) * 100) if self.results else 0,
            "overall_dangerous_error_rate": (sum(1 for r in self.results if r.dangerous_errors) / len(self.results) * 100) if self.results else 0,
        }

        min_required_runs = int(self.config.get("min_runs", 5))
        observed_normal_runs = [
            len(result.normal_scores) for result in aggregated if result.normal_scores
        ]
        min_observed_normal_runs = min(observed_normal_runs) if observed_normal_runs else 0
        summary["min_required_runs"] = min_required_runs
        summary["min_observed_normal_runs"] = min_observed_normal_runs
        summary["meets_min_runs_requirement"] = min_observed_normal_runs >= min_required_runs
        
        return summary
    
    def _dataclass_to_dict(self, obj):
        """Convert dataclass to dictionary for serialization."""
        if hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        return obj


# CLI entry point
def main():
    """Command-line interface for the evaluator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline Safety AI Evaluator")
    parser.add_argument("--model", required=True, help="Model name to evaluate")
    parser.add_argument("--suite", default="full", help="Test suite to run")
    parser.add_argument("--runs", type=int, default=5, help="Number of runs per test")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--output", default="./results", help="Output directory")
    parser.add_argument("--abnormal", action="store_true", help="Include abnormal tests")
    
    args = parser.parse_args()
    
    evaluator = PipelineSafetyEvaluator(
        config_path=args.config,
        output_dir=args.output
    )
    
    # Load model (would need to implement model loading)
    logger.info(f"Evaluation would run: model={args.model}, suite={args.suite}, runs={args.runs}")
    logger.info("Full CLI implementation requires model interface setup")


if __name__ == "__main__":
    main()
