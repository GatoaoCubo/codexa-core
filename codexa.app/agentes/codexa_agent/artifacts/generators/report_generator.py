#!/usr/bin/env python3
"""
CODEXA Report Generator
Version: 1.0.0
Created: 2025-11-24

Unified generator for execution, verification, and review reports.
Uses Jinja2 templates to generate structured markdown reports.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader
import json


class ReportType(Enum):
    """Types of reports that can be generated."""
    EXECUTION = "execution"
    VERIFICATION = "verification"
    REVIEW = "review"


class ReportGenerator:
    """
    Unified generator for all report types.

    Generates execution_report.md, verification_report.md, and review_report.md
    using Jinja2 templates.
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize report generator.

        Args:
            templates_dir: Directory containing Jinja2 templates
        """
        self.templates_dir = templates_dir or Path("artifacts/templates")
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate_execution_report(
        self,
        data: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate execution report.

        Args:
            data: Execution report data
            output_path: Optional path to save report

        Returns:
            Generated report markdown
        """
        template = self.env.get_template("execution_report.jinja2")
        rendered = template.render(**data)

        if output_path:
            self._save_report(rendered, output_path)

        return rendered

    def generate_verification_report(
        self,
        data: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate verification report.

        Args:
            data: Verification report data
            output_path: Optional path to save report

        Returns:
            Generated report markdown
        """
        template = self.env.get_template("verification_report.jinja2")
        rendered = template.render(**data)

        if output_path:
            self._save_report(rendered, output_path)

        return rendered

    def generate_review_report(
        self,
        data: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate review report.

        Args:
            data: Review report data
            output_path: Optional path to save report

        Returns:
            Generated report markdown
        """
        template = self.env.get_template("review_report.jinja2")
        rendered = template.render(**data)

        if output_path:
            self._save_report(rendered, output_path)

        return rendered

    def generate(
        self,
        report_type: ReportType,
        data: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate report of specified type.

        Args:
            report_type: Type of report to generate
            data: Report data
            output_path: Optional path to save report

        Returns:
            Generated report markdown
        """
        if report_type == ReportType.EXECUTION:
            return self.generate_execution_report(data, output_path)
        elif report_type == ReportType.VERIFICATION:
            return self.generate_verification_report(data, output_path)
        elif report_type == ReportType.REVIEW:
            return self.generate_review_report(data, output_path)
        else:
            raise ValueError(f"Unknown report type: {report_type}")

    def _save_report(self, content: str, output_path: Path) -> None:
        """Save report to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def from_json(
        self,
        report_type: ReportType,
        json_path: Path,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate report from JSON data file.

        Args:
            report_type: Type of report to generate
            json_path: Path to JSON data file
            output_path: Optional path to save report

        Returns:
            Generated report markdown
        """
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        return self.generate(report_type, data, output_path)


class ExecutionReportBuilder:
    """Builder for execution report data."""

    def __init__(self):
        self.data: Dict[str, Any] = {
            "feature_name": "",
            "execution_id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": "0 minutes",
            "status": "success",
            "summary": "",
            "metrics": {},
            "plan_file": "",
            "task_file": "",
            "plan_adherence": 100,
            "plan_deviations": [],
            "files": {"created": [], "modified": [], "deleted": []},
            "tasks": [],
            "progress_checkpoints": [],
            "phases": [],
            "code_quality": {},
            "issues": [],
            "dependencies": {"installed": [], "updated": []},
            "git": {},
            "performance": {},
            "next_steps": {},
            "artifacts": [],
            "agent_version": "1.0.0",
            "execution_pattern": "systematic",
            "adw_path": "",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def with_feature_name(self, name: str) -> "ExecutionReportBuilder":
        self.data["feature_name"] = name
        return self

    def with_metrics(self, metrics: Dict[str, Any]) -> "ExecutionReportBuilder":
        self.data["metrics"] = metrics
        return self

    def with_files(self, files: Dict[str, List]) -> "ExecutionReportBuilder":
        self.data["files"] = files
        return self

    def with_tasks(self, tasks: List[Dict]) -> "ExecutionReportBuilder":
        self.data["tasks"] = tasks
        return self

    def build(self) -> Dict[str, Any]:
        return self.data


class VerificationReportBuilder:
    """Builder for verification report data."""

    def __init__(self):
        self.data: Dict[str, Any] = {
            "feature_name": "",
            "verification_id": f"verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "spec_file": "",
            "execution_report": "",
            "status": "approved",
            "summary": "",
            "compliance_score": 100,
            "coverage_percentage": 95,
            "gates_failed": 0,
            "issues_count": 0,
            "estimated_fix_time": "0 min",
            "gates": {
                "unit_tests": {"status": "passed", "command": "", "tests_run": 0, "tests_passed": 0, "pass_rate": 100, "duration": 0, "failures": []},
                "integration_tests": {"status": "passed", "command": "", "tests_run": 0, "tests_passed": 0, "pass_rate": 100, "duration": 0, "failures": []},
                "e2e_tests": {"status": "passed", "command": "", "tests_run": 0, "tests_passed": 0, "pass_rate": 100, "duration": 0, "flows_tested": [], "failures": []},
                "type_check": {"status": "passed", "command": "", "errors": 0, "warnings": 0, "error_list": []},
                "lint": {"status": "passed", "command": "", "errors": 0, "warnings": 0, "error_list": []},
                "coverage": {"status": "passed", "command": "", "percentage": 95, "threshold": 80, "statements": 95, "branches": 90, "functions": 95, "lines": 95, "uncovered_files": []},
                "spec_compliance": {"status": "passed", "percentage": 100, "total_requirements": 0, "met": 0, "partial": 0, "missing": 0}
            },
            "spec_compliance_matrix": [],
            "extra_features": [],
            "manual_verification": {},
            "files_verified": {"created": [], "modified": [], "total": 0, "total_lines": 0},
            "issues": [],
            "optional_improvements": [],
            "issues_to_fix": [],
            "total_fix_time": "0 min",
            "critical_issues": [],
            "industry_comparison": [],
            "spec_comparison": [],
            "verification_duration": 60,
            "total_tests_analyzed": 0,
            "traceability_matrix": [],
            "traceability_percentage": 100,
            "agent_version": "1.0.0",
            "adw_path": "",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def with_feature_name(self, name: str) -> "VerificationReportBuilder":
        self.data["feature_name"] = name
        return self

    def with_status(self, status: str) -> "VerificationReportBuilder":
        self.data["status"] = status
        return self

    def with_gates(self, gates: Dict[str, Any]) -> "VerificationReportBuilder":
        self.data["gates"] = gates
        return self

    def build(self) -> Dict[str, Any]:
        return self.data


class ReviewReportBuilder:
    """Builder for review report data."""

    def __init__(self):
        self.data: Dict[str, Any] = {
            "feature_name": "",
            "review_id": f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "review_date": datetime.now().strftime("%Y-%m-%d"),
            "spec_file": "",
            "execution_report": "",
            "decision": "APPROVE",
            "summary": "",
            "compliance_score": 100,
            "requirements_met": 0,
            "total_requirements": 0,
            "requirements_partial": 0,
            "requirements_missing": 0,
            "quality_score": 92,
            "quality_grade": "A",
            "requirements": [],
            "extra_features": [],
            "scores": {
                "code_structure": 20,
                "code_quality": 18,
                "testing": 19,
                "documentation": 17,
                "spec_compliance": 20
            },
            "weighted_scores": {},
            "total_score": 94,
            "code_structure": {"strengths": [], "areas_for_improvement": [], "evidence": ""},
            "code_quality": {"strengths": [], "areas_for_improvement": [], "evidence": "", "evidence_language": "typescript"},
            "testing": {"strengths": [], "areas_for_improvement": [], "evidence": ""},
            "documentation": {"strengths": [], "areas_for_improvement": [], "evidence": "", "evidence_language": "typescript"},
            "spec_compliance": {"strengths": [], "areas_for_improvement": []},
            "visual_verification": None,
            "strengths": [],
            "areas_for_improvement": [],
            "total_estimated_fix_time": "0 min",
            "approval_conditions": None,
            "optional_improvements": [],
            "issues_count": 0,
            "issues_to_fix": [],
            "critical_issues": [],
            "recommended_action": "",
            "industry_comparison": [],
            "spec_comparison": [],
            "review_duration": 80,
            "files_reviewed": 0,
            "lines_reviewed": 0,
            "tests_analyzed": 0,
            "files": {"created": [], "modified": [], "total": 0},
            "traceability_matrix": [],
            "traceability_percentage": 100,
            "agent_version": "1.0.0",
            "adw_path": "",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def with_feature_name(self, name: str) -> "ReviewReportBuilder":
        self.data["feature_name"] = name
        return self

    def with_decision(self, decision: str) -> "ReviewReportBuilder":
        self.data["decision"] = decision
        return self

    def with_scores(self, scores: Dict[str, int]) -> "ReviewReportBuilder":
        self.data["scores"] = scores
        total = sum(scores.values())
        self.data["total_score"] = total
        self.data["quality_score"] = total

        # Calculate grade
        if total >= 90:
            grade = "A"
        elif total >= 80:
            grade = "B"
        elif total >= 70:
            grade = "C"
        elif total >= 60:
            grade = "D"
        else:
            grade = "F"

        self.data["quality_grade"] = grade

        # Calculate weighted scores (each worth 20%)
        self.data["weighted_scores"] = {
            k: v for k, v in scores.items()
        }

        return self

    def build(self) -> Dict[str, Any]:
        return self.data


def main():
    """Example usage of report generator."""
    generator = ReportGenerator()

    # Example 1: Generate execution report
    exec_data = (ExecutionReportBuilder()
        .with_feature_name("Dark Mode Toggle")
        .with_metrics({
            "total_tasks": 12,
            "completed_tasks": 12,
            "completion_percentage": 100,
            "files_created": 4,
            "files_modified": 2,
            "lines_added": 487,
            "tests_created": 8,
            "tests_passing": 8
        })
        .with_files({
            "created": [
                {"path": "src/components/DarkModeToggle.tsx", "lines": 87, "purpose": "Toggle component", "complexity": "medium"}
            ],
            "modified": [
                {"path": "src/context/ThemeContext.tsx", "lines_added": 32, "lines_removed": 0, "changes_description": "Added dark mode state", "impact": "Low"}
            ],
            "deleted": []
        })
        .build())

    exec_report = generator.generate_execution_report(
        exec_data,
        Path("agents/adw_test/execution_report.md")
    )

    print(f"✅ Generated execution report ({len(exec_report)} chars)")

    # Example 2: Generate verification report
    verify_data = (VerificationReportBuilder()
        .with_feature_name("Dark Mode Toggle")
        .with_status("approved")
        .build())

    verify_report = generator.generate_verification_report(
        verify_data,
        Path("agents/adw_test/verification_report.md")
    )

    print(f"✅ Generated verification report ({len(verify_report)} chars)")

    # Example 3: Generate review report
    review_data = (ReviewReportBuilder()
        .with_feature_name("Dark Mode Toggle")
        .with_decision("APPROVE")
        .with_scores({
            "code_structure": 20,
            "code_quality": 18,
            "testing": 19,
            "documentation": 17,
            "spec_compliance": 20
        })
        .build())

    review_report = generator.generate_review_report(
        review_data,
        Path("agents/adw_test/review_report.md")
    )

    print(f"✅ Generated review report ({len(review_report)} chars)")


if __name__ == "__main__":
    main()
