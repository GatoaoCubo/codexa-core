#!/usr/bin/env python3
"""
CODEXA Validator Report Generator (Simple)
Version: 1.0.0
Created: 2025-11-24

Generates structured reports (JSON + MD) for validators.
Follows REPORT_STANDARD.md specification with minimal dependencies.

Usage:
    from validators.report_generator import ValidatorReportGenerator

    reporter = ValidatorReportGenerator("hop_sync_validator", "1.0.0")
    reporter.add_issue("file.md", "error", "Missing section", line=42)
    reporter.generate("prompts/*.md", passed=4, failed=1, warnings=2, output_dir=Path("reports"))
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import json


@dataclass
class ValidationIssue:
    """A single validation issue."""
    file: str
    severity: str  # error, warning, info
    message: str
    line: Optional[int] = None
    rule: str = ""
    fix_suggestion: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report structure."""
    validator: str
    version: str
    timestamp: str
    execution_id: str
    target: str
    duration_seconds: float
    status: str  # PASS, FAIL, PARTIAL
    results: Dict[str, int]
    issues: List[Dict[str, Any]]
    summary: str
    recommendations: List[str] = field(default_factory=list)


class ValidatorReportGenerator:
    """
    Simple report generator for validators.

    Generates both JSON (machine-parsable) and MD (human-readable) reports
    following the ##report standard.
    """

    def __init__(self, validator_name: str, version: str = "1.0.0"):
        """
        Initialize report generator.

        Args:
            validator_name: Name of the validator (e.g., "hop_sync_validator")
            version: Validator version
        """
        self.validator = validator_name
        self.version = version
        self.issues: List[ValidationIssue] = []
        self.recommendations: List[str] = []
        self.start_time = datetime.now()
        self.execution_id = f"{validator_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def add_issue(
        self,
        file: str,
        severity: str,
        message: str,
        line: Optional[int] = None,
        rule: str = "",
        fix_suggestion: Optional[str] = None
    ) -> None:
        """
        Add a validation issue.

        Args:
            file: File path where issue was found
            severity: Issue severity (error, warning, info)
            message: Issue description
            line: Line number (optional)
            rule: Rule ID or name (optional)
            fix_suggestion: Suggested fix (optional)
        """
        self.issues.append(ValidationIssue(
            file=file,
            severity=severity,
            message=message,
            line=line,
            rule=rule,
            fix_suggestion=fix_suggestion
        ))

    def add_recommendation(self, recommendation: str) -> None:
        """Add a recommendation for improvement."""
        self.recommendations.append(recommendation)

    def generate(
        self,
        target: str,
        passed: int,
        failed: int,
        warnings: int,
        output_dir: Optional[Path] = None
    ) -> ValidationReport:
        """
        Generate the validation report.

        Args:
            target: Target pattern or file(s) validated
            passed: Number of files that passed
            failed: Number of files that failed
            warnings: Number of warnings
            output_dir: Directory to save reports (optional)

        Returns:
            ValidationReport object
        """
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        # Determine status
        if failed > 0:
            status = "FAIL"
        elif warnings > 0:
            status = "PARTIAL"
        else:
            status = "PASS"

        # Build report
        report = ValidationReport(
            validator=self.validator,
            version=self.version,
            timestamp=end_time.isoformat(),
            execution_id=self.execution_id,
            target=target,
            duration_seconds=round(duration, 2),
            status=status,
            results={
                "total_files": passed + failed,
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "errors": len([i for i in self.issues if i.severity == "error"]),
                "info": len([i for i in self.issues if i.severity == "info"])
            },
            issues=[asdict(i) for i in self.issues],
            summary=f"{passed}/{passed + failed} files passed validation ({status})",
            recommendations=self.recommendations
        )

        # Save reports if output_dir specified
        if output_dir:
            self._save_reports(report, output_dir)

        return report

    def _save_reports(self, report: ValidationReport, output_dir: Path) -> tuple:
        """Save JSON and MD reports to output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # JSON report
        json_path = output_dir / f"{self.execution_id}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)

        # Markdown report
        md_path = output_dir / f"{self.execution_id}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._to_markdown(report))

        return json_path, md_path

    def _to_markdown(self, report: ValidationReport) -> str:
        """Convert report to markdown format."""
        status_emoji = {"PASS": "[OK]", "FAIL": "[FAIL]", "PARTIAL": "[WARN]"}
        severity_emoji = {"error": "[ERR]", "warning": "[WARN]", "info": "[INFO]"}

        lines = [
            f"# {report.validator} Report",
            "",
            f"**Status**: {status_emoji.get(report.status, '')} {report.status}",
            f"**Generated**: {report.timestamp}",
            f"**Duration**: {report.duration_seconds}s",
            f"**Target**: `{report.target}`",
            "",
            "## Results",
            "",
            f"- **Total Files**: {report.results['total_files']}",
            f"- **Passed**: {report.results['passed']}",
            f"- **Failed**: {report.results['failed']}",
            f"- **Warnings**: {report.results['warnings']}",
            "",
        ]

        # Issues section
        if report.issues:
            lines.extend([
                "## Issues",
                "",
            ])

            # Group by severity
            for severity in ["error", "warning", "info"]:
                severity_issues = [i for i in report.issues if i["severity"] == severity]
                if severity_issues:
                    lines.append(f"### {severity.upper()}S ({len(severity_issues)})")
                    lines.append("")
                    for issue in severity_issues:
                        location = f":{issue['line']}" if issue['line'] else ""
                        lines.append(f"- {severity_emoji.get(severity, '')} `{issue['file']}{location}`: {issue['message']}")
                        if issue.get('fix_suggestion'):
                            lines.append(f"  - Fix: {issue['fix_suggestion']}")
                    lines.append("")

        # Recommendations section
        if report.recommendations:
            lines.extend([
                "## Recommendations",
                "",
            ])
            for rec in report.recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        # Summary
        lines.extend([
            "## Summary",
            "",
            report.summary,
            "",
            "---",
            "",
            f"*Report generated by {report.validator} v{report.version}*",
            f"*Execution ID: {report.execution_id}*",
        ])

        return "\n".join(lines)

    def print_summary(self, report: ValidationReport) -> None:
        """Print summary to console."""
        status_emoji = {"PASS": "[OK]", "FAIL": "[FAIL]", "PARTIAL": "[WARN]"}

        print(f"\n{'=' * 50}")
        print(f"  {self.validator} - {status_emoji.get(report.status, '')} {report.status}")
        print(f"  Passed: {report.results['passed']}/{report.results['total_files']}")
        print(f"  Errors: {report.results['errors']} | Warnings: {report.results['warnings']}")
        print(f"  Duration: {report.duration_seconds}s")
        print(f"{'=' * 50}\n")


# Convenience function for quick validation reports
def quick_report(
    validator_name: str,
    target: str,
    passed: int,
    failed: int,
    issues: Optional[List[Dict]] = None,
    output_dir: Optional[Path] = None
) -> ValidationReport:
    """
    Generate a quick validation report.

    Args:
        validator_name: Name of the validator
        target: What was validated
        passed: Files passed
        failed: Files failed
        issues: List of issue dicts (optional)
        output_dir: Where to save (optional)

    Returns:
        ValidationReport
    """
    reporter = ValidatorReportGenerator(validator_name)

    if issues:
        for issue in issues:
            reporter.add_issue(**issue)

    warnings = len([i for i in (issues or []) if i.get("severity") == "warning"])

    return reporter.generate(target, passed, failed, warnings, output_dir)


if __name__ == "__main__":
    # Example usage
    reporter = ValidatorReportGenerator("hop_sync_validator", "2.0.0")

    # Add some issues
    reporter.add_issue(
        "prompts/91_meta_build_agent_HOP.md",
        "warning",
        "Missing PROMPT_LAYER_COMPOSITION section",
        line=None,
        rule="HOP-001",
        fix_suggestion="Add section after CONTEXT"
    )
    reporter.add_issue(
        "prompts/92_meta_chore_plan_HOP.md",
        "error",
        "Missing TASK_BOUNDARY section",
        line=None,
        rule="HOP-002"
    )
    reporter.add_recommendation("Update all HOPs to v2.0.0 format")

    # Generate report
    report = reporter.generate(
        target="prompts/9*_HOP.md",
        passed=3,
        failed=2,
        warnings=1,
        output_dir=Path("reports")
    )

    reporter.print_summary(report)
    print(f"[OK] Reports saved to reports/")
