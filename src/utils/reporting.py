"""
Report generation for PSAE evaluation results.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any, Dict

from .benchmark_manifest import load_manifest


class ReportGenerator:
    """Generate evaluation reports in multiple formats."""

    REPORT_SCHEMA_VERSION = "1.1.0"

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def _manifest_metadata(self) -> Dict[str, Any]:
        try:
            manifest = load_manifest()
            return {
                "benchmark_manifest_version": manifest.get("manifest_version"),
                "benchmark_dataset_version": manifest.get("dataset_version"),
            }
        except Exception:
            return {
                "benchmark_manifest_version": None,
                "benchmark_dataset_version": None,
            }

    def _with_report_metadata(self, results: Dict[str, Any]) -> Dict[str, Any]:
        enriched = dict(results)
        enriched["report_metadata"] = {
            "schema_version": self.REPORT_SCHEMA_VERSION,
            "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            **self._manifest_metadata(),
        }
        return enriched

    def generate_html_report(self, results: Dict[str, Any]) -> str:
        """Generate a simple HTML report."""
        enriched = self._with_report_metadata(results)
        summary = enriched.get("summary", {})
        model_name = enriched.get("model_name", "unknown")
        model_version = enriched.get("model_version", "unknown")
        statistical = enriched.get("statistical_analysis", {})
        report_meta = enriched.get("report_metadata", {})
        category_stats = statistical.get("descriptive_by_category", {})

        category_rows = ""
        for category, stats in category_stats.items():
            category_rows += (
                f"<tr><td>{category}</td>"
                f"<td>{stats.get('n', 'n/a')}</td>"
                f"<td>{stats.get('mean', 'n/a')}</td>"
                f"<td>{stats.get('std', 'n/a')}</td>"
                f"<td>{stats.get('ci_lower', 'n/a')} to {stats.get('ci_upper', 'n/a')}</td></tr>"
            )

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>PSAE Evaluation Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.5; }}
    h1, h2 {{ margin-bottom: 8px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    code {{ background: #f7f7f7; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>Pipeline Safety AI Evaluator Report</h1>
  <p><strong>Model:</strong> {model_name} ({model_version})</p>
  <p><strong>Generated:</strong> {enriched.get("timestamp", "unknown")}</p>
  <p><strong>Schema:</strong> {report_meta.get("schema_version", "unknown")}</p>
  <p><strong>Benchmark Dataset:</strong> {report_meta.get("benchmark_dataset_version", "unknown")}</p>

  <h2>Executive Summary</h2>
  <table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Overall Score</td><td>{summary.get("overall_score", "n/a")}</td></tr>
    <tr><td>Pass Rate</td><td>{summary.get("overall_pass_rate", "n/a")}</td></tr>
    <tr><td>Dangerous Error Rate</td><td>{summary.get("overall_dangerous_error_rate", "n/a")}</td></tr>
    <tr><td>Total Tests</td><td>{summary.get("total_tests", "n/a")}</td></tr>
  </table>

  <h2>Category Breakdown</h2>
  <table>
    <tr><th>Category</th><th>N</th><th>Mean</th><th>Std</th><th>95% CI</th></tr>
    {category_rows or "<tr><td colspan='5'>No category statistics available.</td></tr>"}
  </table>

  <h2>Statistical Analysis</h2>
  <pre>{json.dumps(statistical, indent=2)}</pre>

  <h2>Notes</h2>
  <p>Report includes run summary, category descriptives, and statistical analysis outputs.</p>
</body>
</html>
"""
        filepath = self.output_dir / f"report_{self._timestamp()}.html"
        filepath.write_text(html, encoding="utf-8")
        return str(filepath)

    def generate_json_report(self, results: Dict[str, Any]) -> str:
        """Generate machine-readable JSON report."""
        filepath = self.output_dir / f"report_{self._timestamp()}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self._with_report_metadata(results), f, indent=2)
        return str(filepath)

    def generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate Markdown report for documentation."""
        enriched = self._with_report_metadata(results)
        summary = enriched.get("summary", {})
        report_meta = enriched.get("report_metadata", {})
        lines = [
            "# PSAE Evaluation Report",
            "",
            f"- Model: {enriched.get('model_name', 'unknown')} ({enriched.get('model_version', 'unknown')})",
            f"- Generated: {enriched.get('timestamp', 'unknown')}",
            f"- Report Schema Version: {report_meta.get('schema_version', 'unknown')}",
            f"- Benchmark Dataset Version: {report_meta.get('benchmark_dataset_version', 'unknown')}",
            "",
            "## Summary",
            "",
            f"- Overall Score: {summary.get('overall_score', 'n/a')}",
            f"- Pass Rate: {summary.get('overall_pass_rate', 'n/a')}",
            f"- Dangerous Error Rate: {summary.get('overall_dangerous_error_rate', 'n/a')}",
            f"- Total Tests: {summary.get('total_tests', 'n/a')}",
            "",
            "## Statistical Analysis",
            "",
            "```json",
            json.dumps(enriched.get("statistical_analysis", {}), indent=2),
            "```",
            "",
        ]
        filepath = self.output_dir / f"report_{self._timestamp()}.md"
        filepath.write_text("\n".join(lines), encoding="utf-8")
        return str(filepath)

    def generate_latex_tables(self, results: Dict[str, Any]) -> str:
        """Generate a minimal LaTeX table scaffold."""
        summary = self._with_report_metadata(results).get("summary", {})
        latex = r"""\begin{table}[h]
\centering
\begin{tabular}{ll}
\hline
Metric & Value \\
\hline
Overall Score & %s \\
Pass Rate & %s \\
Dangerous Error Rate & %s \\
Total Tests & %s \\
\hline
\end{tabular}
\caption{PSAE Evaluation Summary}
\end{table}
""" % (
            summary.get("overall_score", "n/a"),
            summary.get("overall_pass_rate", "n/a"),
            summary.get("overall_dangerous_error_rate", "n/a"),
            summary.get("total_tests", "n/a"),
        )
        filepath = self.output_dir / f"report_{self._timestamp()}.tex"
        filepath.write_text(latex, encoding="utf-8")
        return str(filepath)
