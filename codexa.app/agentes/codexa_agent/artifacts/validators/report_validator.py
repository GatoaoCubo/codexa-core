#!/usr/bin/env python3
"""
CODEXA Report Validator
Version: 1.0.0
Created: 2025-11-24

Validates execution, verification, and review reports.
Ensures reports are complete, accurate, and properly formatted.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any


class ValidationSeverity(Enum):
    """Severity level of validation issue."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """A validation issue found in the report."""
    severity: ValidationSeverity
    section: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of report validation."""
    valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    errors_count: int = 0
    warnings_count: int = 0
    info_count: int = 0

    def add_issue(self, issue: ValidationIssue) -> None:
        """Add a validation issue and update counts."""
        self.issues.append(issue)
        if issue.severity == ValidationSeverity.ERROR:
            self.errors_count += 1
            self.valid = False
        elif issue.severity == ValidationSeverity.WARNING:
            self.warnings_count += 1
        else:
            self.info_count += 1


class ReportValidator:
    """
    Unified validator for all report types.

    Validates execution_report.md, verification_report.md, and review_report.md.
    """

    def __init__(self):
        """Initialize report validator."""
        pass

    def validate_execution_report(self, report_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate execution report.

        Args:
            report_data: Execution report data

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        # Required fields
        required_fields = [
            "feature_name", "execution_id", "status", "summary",
            "metrics", "files", "tasks"
        ]

        for field in required_fields:
            if field not in report_data or not report_data[field]:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section=field,
                    message=f"Required field '{field}' is missing",
                    suggestion=f"Add {field} to the report"
                ))

        # Validate status
        status = report_data.get("status", "")
        if status not in ["success", "partial", "failed"]:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="status",
                message=f"Invalid status: '{status}'",
                suggestion="Status must be 'success', 'partial', or 'failed'"
            ))

        # Validate metrics
        metrics = report_data.get("metrics", {})
        required_metrics = [
            "total_tasks", "completed_tasks", "files_created",
            "files_modified", "tests_created"
        ]

        for metric in required_metrics:
            if metric not in metrics:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section="metrics",
                    message=f"Metric '{metric}' is missing",
                    suggestion=f"Include {metric} in metrics"
                ))

        # Validate completion percentage
        if "completion_percentage" in metrics:
            pct = metrics["completion_percentage"]
            if not isinstance(pct, (int, float)) or pct < 0 or pct > 100:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section="metrics",
                    message=f"Invalid completion_percentage: {pct}",
                    suggestion="Completion percentage must be between 0 and 100"
                ))

        # Validate files
        files = report_data.get("files", {})
        if "created" not in files:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="files",
                message="No 'created' files list",
                suggestion="Include list of created files"
            ))

        if "modified" not in files:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="files",
                message="No 'modified' files list",
                suggestion="Include list of modified files"
            ))

        # Validate tasks
        tasks = report_data.get("tasks", [])
        if not tasks or len(tasks) == 0:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="tasks",
                message="No tasks in execution report",
                suggestion="Include task execution details"
            ))

        return result

    def validate_verification_report(self, report_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate verification report.

        Args:
            report_data: Verification report data

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        # Required fields
        required_fields = [
            "feature_name", "verification_id", "status", "gates",
            "spec_compliance_matrix"
        ]

        for field in required_fields:
            if field not in report_data or report_data[field] is None:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section=field,
                    message=f"Required field '{field}' is missing",
                    suggestion=f"Add {field} to the report"
                ))

        # Validate status
        status = report_data.get("status", "")
        if status not in ["approved", "revise", "reject"]:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="status",
                message=f"Invalid status: '{status}'",
                suggestion="Status must be 'approved', 'revise', or 'reject'"
            ))

        # Validate 7 quality gates
        gates = report_data.get("gates", {})
        required_gates = [
            "unit_tests", "integration_tests", "e2e_tests",
            "type_check", "lint", "coverage", "spec_compliance"
        ]

        for gate in required_gates:
            if gate not in gates:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section="gates",
                    message=f"Quality gate '{gate}' is missing",
                    suggestion=f"Include {gate} quality gate results"
                ))
            else:
                gate_data = gates[gate]
                if "status" not in gate_data:
                    result.add_issue(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        section=f"gates.{gate}",
                        message=f"Gate '{gate}' missing status",
                        suggestion="Add 'passed' or 'failed' status"
                    ))

        # Validate compliance score
        compliance_score = report_data.get("compliance_score", 0)
        if not isinstance(compliance_score, (int, float)) or compliance_score < 0 or compliance_score > 100:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="compliance_score",
                message=f"Invalid compliance_score: {compliance_score}",
                suggestion="Compliance score must be between 0 and 100"
            ))

        # Validate coverage percentage
        coverage = report_data.get("coverage_percentage", 0)
        if not isinstance(coverage, (int, float)) or coverage < 0 or coverage > 100:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="coverage_percentage",
                message=f"Invalid coverage_percentage: {coverage}",
                suggestion="Coverage percentage must be between 0 and 100"
            ))

        return result

    def validate_review_report(self, report_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate review report.

        Args:
            report_data: Review report data

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        # Required fields
        required_fields = [
            "feature_name", "review_id", "decision", "compliance_score",
            "quality_score", "scores", "requirements"
        ]

        for field in required_fields:
            if field not in report_data or report_data[field] is None:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section=field,
                    message=f"Required field '{field}' is missing",
                    suggestion=f"Add {field} to the report"
                ))

        # Validate decision
        decision = report_data.get("decision", "")
        if decision not in ["APPROVE", "REVISE", "REJECT"]:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="decision",
                message=f"Invalid decision: '{decision}'",
                suggestion="Decision must be 'APPROVE', 'REVISE', or 'REJECT'"
            ))

        # Validate scores (5 criteria)
        scores = report_data.get("scores", {})
        required_scores = [
            "code_structure", "code_quality", "testing",
            "documentation", "spec_compliance"
        ]

        for score_name in required_scores:
            if score_name not in scores:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section="scores",
                    message=f"Score '{score_name}' is missing",
                    suggestion=f"Add {score_name} score (0-20)"
                ))
            else:
                score = scores[score_name]
                if not isinstance(score, (int, float)) or score < 0 or score > 20:
                    result.add_issue(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        section=f"scores.{score_name}",
                        message=f"Invalid score: {score} (must be 0-20)",
                        suggestion="Score must be between 0 and 20"
                    ))

        # Validate total quality score
        quality_score = report_data.get("quality_score", 0)
        if not isinstance(quality_score, (int, float)) or quality_score < 0 or quality_score > 100:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="quality_score",
                message=f"Invalid quality_score: {quality_score}",
                suggestion="Quality score must be between 0 and 100"
            ))

        # Validate grade
        quality_grade = report_data.get("quality_grade", "")
        if quality_grade not in ["A", "B", "C", "D", "F"]:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="quality_grade",
                message=f"Invalid quality_grade: '{quality_grade}'",
                suggestion="Grade must be A, B, C, D, or F"
            ))

        # Validate compliance score
        compliance_score = report_data.get("compliance_score", 0)
        if not isinstance(compliance_score, (int, float)) or compliance_score < 0 or compliance_score > 100:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="compliance_score",
                message=f"Invalid compliance_score: {compliance_score}",
                suggestion="Compliance score must be between 0 and 100"
            ))

        # Validate decision consistency
        if decision == "APPROVE" and quality_score < 80:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="decision",
                message=f"Decision is APPROVE but quality score is {quality_score} (< 80)",
                suggestion="Consider REVISE decision for scores below 80"
            ))

        if decision == "REJECT" and quality_score >= 60:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="decision",
                message=f"Decision is REJECT but quality score is {quality_score} (>= 60)",
                suggestion="Consider REVISE instead of REJECT for scores 60-79"
            ))

        return result


def main():
    """Example usage of report validator."""
    validator = ReportValidator()

    # Example 1: Validate execution report
    exec_report = {
        "feature_name": "Dark Mode Toggle",
        "execution_id": "exec_20251124_153045",
        "status": "success",
        "summary": "Successfully implemented dark mode toggle",
        "metrics": {
            "total_tasks": 12,
            "completed_tasks": 12,
            "completion_percentage": 100,
            "files_created": 4,
            "files_modified": 2,
            "tests_created": 8
        },
        "files": {
            "created": [],
            "modified": []
        },
        "tasks": [{"id": 1, "status": "completed"}]
    }

    result = validator.validate_execution_report(exec_report)
    print(f"Execution Report: {'✅ VALID' if result.valid else '❌ INVALID'}")
    print(f"  Errors: {result.errors_count}, Warnings: {result.warnings_count}, Info: {result.info_count}")

    # Example 2: Validate verification report
    verify_report = {
        "feature_name": "Dark Mode Toggle",
        "verification_id": "verify_20251124_153045",
        "status": "approved",
        "compliance_score": 100,
        "coverage_percentage": 96,
        "gates": {
            "unit_tests": {"status": "passed"},
            "integration_tests": {"status": "passed"},
            "e2e_tests": {"status": "passed"},
            "type_check": {"status": "passed"},
            "lint": {"status": "passed"},
            "coverage": {"status": "passed"},
            "spec_compliance": {"status": "passed"}
        },
        "spec_compliance_matrix": []
    }

    result = validator.validate_verification_report(verify_report)
    print(f"\nVerification Report: {'✅ VALID' if result.valid else '❌ INVALID'}")
    print(f"  Errors: {result.errors_count}, Warnings: {result.warnings_count}, Info: {result.info_count}")

    # Example 3: Validate review report
    review_report = {
        "feature_name": "Dark Mode Toggle",
        "review_id": "review_20251124_153045",
        "decision": "APPROVE",
        "compliance_score": 100,
        "quality_score": 92,
        "quality_grade": "A",
        "scores": {
            "code_structure": 20,
            "code_quality": 18,
            "testing": 19,
            "documentation": 17,
            "spec_compliance": 20
        },
        "requirements": []
    }

    result = validator.validate_review_report(review_report)
    print(f"\nReview Report: {'✅ VALID' if result.valid else '❌ INVALID'}")
    print(f"  Errors: {result.errors_count}, Warnings: {result.warnings_count}, Info: {result.info_count}")


if __name__ == "__main__":
    main()
