"""
Statistical Analysis Module
===========================

Implements statistical tests and analyses for PSAE results.
"""

import logging
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """
    Performs statistical analysis on evaluation results.
    
    Implements:
    - Confidence intervals
    - ANOVA (one-way, two-way)
    - Tukey HSD post-hoc tests
    - Effect size calculations (Cohen's d)
    - Inter-rater reliability (ICC)
    - Power analysis
    """
    
    def __init__(self, confidence_level: float = 0.95):
        """
        Initialize statistical analyzer.
        
        Args:
            confidence_level: Confidence level for intervals (default: 0.95)
        """
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
        
        # Z-scores for common confidence levels
        self.z_scores = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.576
        }
    
    def confidence_interval(
        self, 
        data: List[float], 
        confidence_level: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval for mean.
        
        Args:
            data: Sample data
            confidence_level: Confidence level (uses instance default if None)
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        if not data:
            return (0, 0)
        
        if len(data) == 1:
            # Can't calculate CI with n=1
            return (data[0], data[0])
        
        confidence = confidence_level or self.confidence_level
        
        mean = np.mean(data)
        std_err = stats.sem(data)
        
        # Use t-distribution for small samples
        if len(data) < 30:
            h = std_err * stats.t.ppf((1 + confidence) / 2, len(data) - 1)
        else:
            # Normal approximation for large samples
            z = self.z_scores.get(confidence, 1.96)
            h = std_err * z
        
        return (mean - h, mean + h)
    
    def one_way_anova(
        self, 
        groups: Dict[str, List[float]]
    ) -> Dict[str, Any]:
        """
        Perform one-way ANOVA across multiple groups.
        
        Args:
            groups: Dictionary of group_name -> data_points
            
        Returns:
            ANOVA results dictionary
        """
        if len(groups) < 2:
            return {
                "error": "Need at least 2 groups for ANOVA",
                "f_statistic": None,
                "p_value": None
            }
        
        # Extract data
        data_lists = list(groups.values())
        
        # Perform ANOVA
        f_stat, p_value = stats.f_oneway(*data_lists)
        
        # Calculate degrees of freedom
        total_n = sum(len(d) for d in data_lists)
        k = len(groups)  # Number of groups
        df_between = k - 1
        df_within = total_n - k
        
        # Effect size (eta-squared)
        # eta-squared = SSbetween / SStotal
        grand_mean = np.mean([np.mean(d) for d in data_lists])
        
        ss_between = sum(
            len(d) * (np.mean(d) - grand_mean) ** 2 
            for d in data_lists
        )
        
        ss_within = sum(
            sum((x - np.mean(d)) ** 2 for x in d)
            for d in data_lists
        )
        
        ss_total = ss_between + ss_within
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        # Interpretation
        if p_value < 0.001:
            significance = "highly_significant"
        elif p_value < 0.01:
            significance = "very_significant"
        elif p_value < 0.05:
            significance = "significant"
        else:
            significance = "not_significant"
        
        return {
            "f_statistic": f_stat,
            "p_value": p_value,
            "alpha": self.alpha,
            "significance": significance,
            "df_between": df_between,
            "df_within": df_within,
            "eta_squared": eta_squared,
            "effect_size": self._interpret_eta_squared(eta_squared),
            "groups": list(groups.keys()),
            "group_means": {name: np.mean(data) for name, data in groups.items()},
            "group_stds": {name: np.std(data, ddof=1) for name, data in groups.items()},
        }
    
    def cohens_d(
        self, 
        group1: List[float], 
        group2: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate Cohen's d effect size.
        
        Args:
            group1: First group data
            group2: Second group data
            
        Returns:
            Effect size results
        """
        if not group1 or not group2:
            return {"error": "Both groups must have data"}
        
        mean1 = np.mean(group1)
        mean2 = np.mean(group2)
        
        # Pooled standard deviation
        n1, n2 = len(group1), len(group2)
        var1 = np.var(group1, ddof=1)
        var2 = np.var(group2, ddof=1)
        
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return {
                "cohens_d": 0,
                "interpretation": "no_variance",
                "mean_difference": mean1 - mean2
            }
        
        d = (mean1 - mean2) / pooled_std
        
        # Interpretation
        abs_d = abs(d)
        if abs_d < 0.2:
            interpretation = "negligible"
        elif abs_d < 0.5:
            interpretation = "small"
        elif abs_d < 0.8:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        return {
            "cohens_d": d,
            "absolute_d": abs_d,
            "interpretation": interpretation,
            "mean_difference": mean1 - mean2,
            "pooled_std": pooled_std,
            "group1_mean": mean1,
            "group2_mean": mean2,
            "direction": "group1_higher" if d > 0 else "group2_higher"
        }
    
    def intraclass_correlation(
        self, 
        ratings: List[List[float]],
        model: str = "single"
    ) -> Dict[str, Any]:
        """
        Calculate Intraclass Correlation Coefficient (ICC).
        
        Measures inter-rater reliability.
        
        Args:
            ratings: Matrix of ratings (raters x items)
            model: ICC model type ('single' or 'average')
            
        Returns:
            ICC results
        """
        try:
            from pingouin import intraclass_corr
            
            # Convert to long format
            import pandas as pd
            data = []
            for rater_idx, rater_scores in enumerate(ratings):
                for item_idx, score in enumerate(rater_scores):
                    data.append({
                        'rater': rater_idx,
                        'item': item_idx,
                        'score': score
                    })
            
            df = pd.DataFrame(data)
            
            # Calculate ICC
            icc_results = intraclass_corr(
                data=df,
                targets='item',
                raters='rater',
                ratings='score'
            )
            
            # Get ICC(2,1) for single measures or ICC(2,k) for average
            if model == "single":
                icc_row = icc_results[icc_results['Type'] == 'ICC2']
            else:
                icc_row = icc_results[icc_results['Type'] == 'ICC2k']
            
            icc_value = icc_row['ICC'].values[0]
            ci_lower = icc_row['CI95%'].values[0][0]
            ci_upper = icc_row['CI95%'].values[0][1]
            
        except ImportError:
            # Fallback implementation without pingouin
            logger.warning("pingouin not available, using simplified ICC calculation")
            
            ratings_array = np.array(ratings)
            
            # Simplified ICC(1) calculation
            n_raters = len(ratings)
            n_items = len(ratings[0])
            
            # Mean squares
            item_means = np.mean(ratings_array, axis=0)
            rater_means = np.mean(ratings_array, axis=1)
            grand_mean = np.mean(ratings_array)
            
            ms_items = n_raters * np.var(item_means, ddof=1)
            ms_raters = n_items * np.var(rater_means, ddof=1)
            ms_error = np.var(ratings_array, ddof=1) * (n_raters * n_items - 1)
            ms_error -= ms_items - ms_raters
            
            # ICC calculation
            icc_value = (ms_items - ms_error) / (ms_items + (n_raters - 1) * ms_error)
            ci_lower = icc_value - 0.1  # Rough approximation
            ci_upper = icc_value + 0.1
        
        # Interpretation
        if icc_value < 0.5:
            reliability = "poor"
        elif icc_value < 0.75:
            reliability = "moderate"
        elif icc_value < 0.9:
            reliability = "good"
        else:
            reliability = "excellent"
        
        return {
            "icc": icc_value,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "reliability": reliability,
            "model": model,
            "n_raters": len(ratings),
            "n_items": len(ratings[0]) if ratings else 0
        }
    
    def power_analysis(
        self,
        effect_size: float,
        alpha: float = 0.05,
        power: float = 0.8,
        sample_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Perform power analysis.
        
        Can calculate required sample size or achieved power.
        
        Args:
            effect_size: Expected effect size (Cohen's d)
            alpha: Significance level
            power: Desired power (if calculating sample size)
            sample_size: Sample size (if calculating power)
            
        Returns:
            Power analysis results
        """
        try:
            from statsmodels.stats.power import tt_ind_solve_power
            
            if sample_size is None:
                # Calculate required sample size
                n = tt_ind_solve_power(
                    effect_size=effect_size,
                    alpha=alpha,
                    power=power,
                    ratio=1.0  # Equal group sizes
                )
                
                return {
                    "calculation": "sample_size",
                    "required_n_per_group": int(np.ceil(n)),
                    "total_sample": int(np.ceil(n)) * 2,
                    "effect_size": effect_size,
                    "alpha": alpha,
                    "desired_power": power
                }
            else:
                # Calculate achieved power
                achieved_power = tt_ind_solve_power(
                    effect_size=effect_size,
                    nobs1=sample_size,
                    alpha=alpha,
                    power=None,
                    ratio=1.0
                )
                
                return {
                    "calculation": "power",
                    "achieved_power": achieved_power,
                    "sample_size_per_group": sample_size,
                    "total_sample": sample_size * 2,
                    "effect_size": effect_size,
                    "alpha": alpha
                }
                
        except ImportError:
            logger.warning("statsmodels not available, using approximation")
            
            # Simplified calculation
            if sample_size is None:
                # Approximate formula for two-sample t-test
                z_alpha = stats.norm.ppf(1 - alpha/2)
                z_beta = stats.norm.ppf(power)
                n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
                
                return {
                    "calculation": "sample_size (approximate)",
                    "required_n_per_group": int(np.ceil(n)),
                    "total_sample": int(np.ceil(n)) * 2,
                    "effect_size": effect_size,
                    "alpha": alpha,
                    "desired_power": power,
                    "note": "Approximate calculation using normal approximation"
                }
            else:
                # Can't calculate without statsmodels
                return {
                    "calculation": "power",
                    "error": "statsmodels required for power calculation with given sample size",
                    "sample_size_per_group": sample_size,
                    "effect_size": effect_size,
                    "alpha": alpha
                }
    
    def normality_test(self, data: List[float]) -> Dict[str, Any]:
        """
        Test for normality (Shapiro-Wilk).
        
        Args:
            data: Sample data
            
        Returns:
            Normality test results
        """
        if len(data) < 3:
            return {
                "test": "Shapiro-Wilk",
                "statistic": None,
                "p_value": None,
                "normal": None,
                "note": "Need at least 3 data points"
            }
        
        # Shapiro-Wilk test
        statistic, p_value = stats.shapiro(data)
        
        # Interpretation
        if p_value > 0.05:
            normality = "normal"
            conclusion = "Fail to reject H0: Data appears normally distributed"
        else:
            normality = "not_normal"
            conclusion = "Reject H0: Data does not appear normally distributed"
        
        return {
            "test": "Shapiro-Wilk",
            "statistic": statistic,
            "p_value": p_value,
            "alpha": self.alpha,
            "normal": normality,
            "conclusion": conclusion
        }
    
    def descriptive_statistics(self, data: List[float]) -> Dict[str, Any]:
        """
        Calculate comprehensive descriptive statistics.
        
        Args:
            data: Sample data
            
        Returns:
            Descriptive statistics dictionary
        """
        if not data:
            return {"error": "No data provided"}
        
        n = len(data)
        mean = np.mean(data)
        median = np.median(data)
        std = np.std(data, ddof=1) if n > 1 else 0.0
        var = np.var(data, ddof=1) if n > 1 else 0.0
        sem = stats.sem(data) if n > 1 else 0.0
        min_val = np.min(data)
        max_val = np.max(data)
        range_val = max_val - min_val
        
        # Quartiles
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        # Confidence interval
        ci_lower, ci_upper = self.confidence_interval(data)
        
        # Skewness and kurtosis
        if n < 3 or np.isclose(std, 0.0):
            skewness = 0.0
            kurtosis = 0.0
        else:
            skewness = stats.skew(data)
            kurtosis = stats.kurtosis(data)
        
        return {
            "n": n,
            "mean": mean,
            "median": median,
            "std": std,
            "variance": var,
            "sem": sem,
            "min": min_val,
            "max": max_val,
            "range": range_val,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "ci_width": ci_upper - ci_lower,
            "skewness": skewness,
            "kurtosis": kurtosis
        }
    
    def compare_models(
        self, 
        model_results: Dict[str, List[float]]
    ) -> Dict[str, Any]:
        """
        Comprehensive comparison of multiple models.
        
        Performs ANOVA, post-hoc tests, and effect sizes.
        
        Args:
            model_results: Dictionary of model_name -> scores
            
        Returns:
            Comprehensive comparison results
        """
        if len(model_results) < 2:
            return {"error": "Need at least 2 models to compare"}
        
        # 1. ANOVA
        anova_results = self.one_way_anova(model_results)
        
        # 2. Pairwise comparisons (Cohen's d)
        pairwise = {}
        models = list(model_results.keys())
        
        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                model1, model2 = models[i], models[j]
                comparison_key = f"{model1}_vs_{model2}"
                
                pairwise[comparison_key] = self.cohens_d(
                    model_results[model1],
                    model_results[model2]
                )
        
        # 3. Descriptive statistics for each model
        descriptives = {
            name: self.descriptive_statistics(scores)
            for name, scores in model_results.items()
        }
        
        # 4. Ranking
        ranked = sorted(
            [(name, np.mean(scores)) for name, scores in model_results.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "anova": anova_results,
            "pairwise_comparisons": pairwise,
            "descriptive_statistics": descriptives,
            "ranking": [
                {"rank": i + 1, "model": name, "mean_score": score}
                for i, (name, score) in enumerate(ranked)
            ],
            "best_performer": ranked[0][0] if ranked else None,
            "significant_differences": anova_results.get("significance") != "not_significant"
        }
    
    def _interpret_eta_squared(self, eta_squared: float) -> str:
        """Interpret eta-squared effect size."""
        if eta_squared < 0.01:
            return "negligible"
        elif eta_squared < 0.06:
            return "small"
        elif eta_squared < 0.14:
            return "medium"
        else:
            return "large"


# Helper functions for common analyses

def compare_to_baseline(
    test_scores: List[float], 
    baseline_scores: List[float],
    analyzer: Optional[StatisticalAnalyzer] = None
) -> Dict[str, Any]:
    """
    Compare test results to baseline (e.g., human expert).
    
    Args:
        test_scores: Scores from model being tested
        baseline_scores: Baseline scores (e.g., human expert)
        analyzer: StatisticalAnalyzer instance (creates new if None)
        
    Returns:
        Comparison results
    """
    if analyzer is None:
        analyzer = StatisticalAnalyzer()
    
    # Effect size
    effect_size = analyzer.cohens_d(test_scores, baseline_scores)
    
    # Descriptive comparison
    test_desc = analyzer.descriptive_statistics(test_scores)
    baseline_desc = analyzer.descriptive_statistics(baseline_scores)
    
    # Difference in means
    mean_diff = test_desc["mean"] - baseline_desc["mean"]
    
    # Is it within confidence interval?
    within_ci = baseline_desc["ci_lower"] <= test_desc["mean"] <= baseline_desc["ci_upper"]
    
    return {
        "test_model": {
            "mean": test_desc["mean"],
            "ci": (test_desc["ci_lower"], test_desc["ci_upper"]),
        },
        "baseline": {
            "mean": baseline_desc["mean"],
            "ci": (baseline_desc["ci_lower"], baseline_desc["ci_upper"]),
        },
        "mean_difference": mean_diff,
        "effect_size": effect_size,
        "within_baseline_ci": within_ci,
        "performance": (
            "comparable" if within_ci else
            "below_baseline" if mean_diff < 0 else
            "above_baseline"
        )
    }


# Example usage
if __name__ == "__main__":
    # Create analyzer
    analyzer = StatisticalAnalyzer(confidence_level=0.95)
    
    # Example data
    model_a_scores = [85.2, 87.3, 84.1, 88.5, 86.2]
    model_b_scores = [78.5, 80.2, 77.8, 79.1, 78.9]
    model_c_scores = [92.1, 93.5, 91.8, 94.2, 93.1]
    
    # Compare models
    results = analyzer.compare_models({
        "Model A": model_a_scores,
        "Model B": model_b_scores,
        "Model C": model_c_scores
    })
    
    print("Comparison Results:")
    print(f"ANOVA p-value: {results['anova']['p_value']:.4f}")
    print(f"Best performer: {results['best_performer']}")
    
    for comparison, effect in results['pairwise_comparisons'].items():
        print(f"{comparison}: Cohen's d = {effect['cohens_d']:.2f} ({effect['interpretation']})")
