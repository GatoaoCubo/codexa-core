#!/usr/bin/env python3
"""
CODEXA Implementation Plan Validator
Version: 1.0.0
Created: 2025-11-24

Validates implementation plans against schemas and business rules.
Ensures plans are complete, coherent, and ready for execution.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


class ValidationSeverity(Enum):
    """Severity level of validation issue."""
    ERROR = "error"       # Blocks execution
    WARNING = "warning"   # Should be fixed
    INFO = "info"         # Nice to have


@dataclass
class ValidationIssue:
    """A validation issue found in the plan."""
    severity: ValidationSeverity
    section: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of plan validation."""
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


class PlanValidator:
    """
    Validator for implementation plans.

    Checks plan completeness, coherence, and readiness for execution.
    """

    def __init__(self):
        """Initialize plan validator."""
        self.required_sections = [
            "feature_name",
            "overview",
            "goal",
            "scope",
            "current_architecture",
            "technical_approach",
            "implementation_phases",
            "acceptance_criteria",
            "rollback_plan"
        ]

    def validate(self, plan_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate implementation plan.

        Args:
            plan_data: Plan data dictionary

        Returns:
            ValidationResult with issues found
        """
        result = ValidationResult(valid=True)

        # Check required sections
        self._validate_required_sections(plan_data, result)

        # Validate feature name
        self._validate_feature_name(plan_data, result)

        # Validate overview and goal
        self._validate_overview_goal(plan_data, result)

        # Validate scope
        self._validate_scope(plan_data, result)

        # Validate technical approach
        self._validate_technical_approach(plan_data, result)

        # Validate implementation phases
        self._validate_implementation_phases(plan_data, result)

        # Validate risks
        self._validate_risks(plan_data, result)

        # Validate testing strategy
        self._validate_testing_strategy(plan_data, result)

        # Validate acceptance criteria
        self._validate_acceptance_criteria(plan_data, result)

        # Validate rollback plan
        self._validate_rollback_plan(plan_data, result)

        # Validate completeness
        self._validate_completeness(plan_data, result)

        return result

    def _validate_required_sections(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate all required sections are present."""
        for section in self.required_sections:
            if section not in plan_data or not plan_data[section]:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    section=section,
                    message=f"Required section '{section}' is missing or empty",
                    suggestion=f"Add {section} to the plan"
                ))

    def _validate_feature_name(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate feature name."""
        feature_name = plan_data.get("feature_name", "")

        if not feature_name:
            return  # Already caught by required sections

        # Feature name should be descriptive
        if len(feature_name) < 5:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="feature_name",
                message="Feature name is too short (< 5 characters)",
                suggestion="Use a more descriptive feature name"
            ))

        # Should not be all caps (except acronyms)
        if feature_name.isupper() and len(feature_name) > 5:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.INFO,
                section="feature_name",
                message="Feature name is all caps",
                suggestion="Use title case for better readability"
            ))

    def _validate_overview_goal(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate overview and goal."""
        overview = plan_data.get("overview", "")
        goal = plan_data.get("goal", "")

        if not overview or not goal:
            return  # Already caught by required sections

        # Overview should be substantial
        if len(overview) < 50:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="overview",
                message="Overview is too brief (< 50 characters)",
                suggestion="Provide more context about the feature"
            ))

        # Goal should be clear and actionable
        if len(goal) < 20:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="goal",
                message="Goal is too vague (< 20 characters)",
                suggestion="Define a clear, measurable goal"
            ))

    def _validate_scope(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate scope definition."""
        scope = plan_data.get("scope", "")

        if not scope:
            return  # Already caught by required sections

        # Scope should have boundaries
        if "not include" not in scope.lower() and "out of scope" not in scope.lower():
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.INFO,
                section="scope",
                message="Scope doesn't explicitly state what's NOT included",
                suggestion="Define what's out of scope to prevent scope creep"
            ))

    def _validate_technical_approach(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate technical approach."""
        approach = plan_data.get("technical_approach", {})

        if not approach:
            return  # Already caught by required sections

        # Should have pattern defined
        if "pattern" not in approach or not approach["pattern"]:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="technical_approach",
                message="No technical pattern specified",
                suggestion="Define the technical pattern to use"
            ))

        # Should have rationale
        if "rationale" not in approach or not approach["rationale"]:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="technical_approach",
                message="No rationale for technical approach",
                suggestion="Explain why this approach was chosen"
            ))

    def _validate_implementation_phases(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate implementation phases."""
        phases = plan_data.get("implementation_phases", [])

        if not phases:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="implementation_phases",
                message="No implementation phases defined",
                suggestion="Break implementation into phases"
            ))
            return

        # Should have at least one phase
        if len(phases) == 0:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="implementation_phases",
                message="At least one implementation phase required",
                suggestion="Define phases for the implementation"
            ))

        # Each phase should have files and steps
        for i, phase in enumerate(phases, 1):
            phase_name = phase.get("name", f"Phase {i}")

            # Should have files to create or modify
            files_to_create = phase.get("files_to_create", [])
            files_to_modify = phase.get("files_to_modify", [])

            if not files_to_create and not files_to_modify:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section=f"implementation_phases.{phase_name}",
                    message=f"Phase '{phase_name}' has no files to create or modify",
                    suggestion="Define which files will be affected"
                ))

            # Should have steps
            steps = phase.get("steps", [])
            if not steps or len(steps) == 0:
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section=f"implementation_phases.{phase_name}",
                    message=f"Phase '{phase_name}' has no steps defined",
                    suggestion="Break phase into actionable steps"
                ))

    def _validate_risks(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate risk assessment."""
        risks = plan_data.get("risks", {})

        # Should have risk assessment
        if not risks:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="risks",
                message="No risk assessment provided",
                suggestion="Identify and document risks"
            ))
            return

        # Check high risks have mitigation
        high_risks = risks.get("high", [])
        for risk in high_risks:
            if not risk.get("mitigation"):
                result.add_issue(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    section="risks",
                    message=f"High risk '{risk.get('name', 'unknown')}' has no mitigation",
                    suggestion="Define mitigation strategy for high risks"
                ))

    def _validate_testing_strategy(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate testing strategy."""
        testing = plan_data.get("testing_strategy", {})

        # Should have testing strategy
        if not testing:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="testing_strategy",
                message="No testing strategy defined",
                suggestion="Define unit, integration, and E2E tests"
            ))
            return

        # Should have at least unit tests
        unit_tests = testing.get("unit_tests", [])
        if not unit_tests or len(unit_tests) == 0:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="testing_strategy",
                message="No unit tests planned",
                suggestion="Define unit tests for the implementation"
            ))

    def _validate_acceptance_criteria(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate acceptance criteria."""
        criteria = plan_data.get("acceptance_criteria", [])

        if not criteria or len(criteria) == 0:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="acceptance_criteria",
                message="No acceptance criteria defined",
                suggestion="Define clear acceptance criteria"
            ))
            return

        # Should have at least 2 criteria
        if len(criteria) < 2:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.INFO,
                section="acceptance_criteria",
                message="Only one acceptance criterion (typically need 2+)",
                suggestion="Consider additional acceptance criteria"
            ))

    def _validate_rollback_plan(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate rollback plan."""
        rollback_plan = plan_data.get("rollback_plan", "")
        rollback_steps = plan_data.get("rollback_steps", [])

        if not rollback_plan:
            return  # Already caught by required sections

        # Should have rollback steps
        if not rollback_steps or len(rollback_steps) == 0:
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                section="rollback_plan",
                message="No rollback steps defined",
                suggestion="Define step-by-step rollback procedure"
            ))

    def _validate_completeness(
        self,
        plan_data: Dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Validate overall plan completeness."""
        # Check if ready for execution
        ready = plan_data.get("ready_for_execution", False)

        if not ready:
            blocking_issues = plan_data.get("blocking_issues", [])
            if blocking_issues:
                for issue in blocking_issues:
                    result.add_issue(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        section="ready_for_execution",
                        message=f"Blocking issue: {issue}",
                        suggestion="Resolve blocking issues before execution"
                    ))

    def validate_markdown(self, markdown_path: Path) -> ValidationResult:
        """
        Validate implementation plan from markdown file.

        Args:
            markdown_path: Path to implementation_plan.md

        Returns:
            ValidationResult
        """
        # This is a placeholder - would need markdown parsing
        # For now, just check file exists
        result = ValidationResult(valid=True)

        if not markdown_path.exists():
            result.add_issue(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                section="file",
                message=f"Plan file not found: {markdown_path}",
                suggestion="Create implementation_plan.md"
            ))

        return result


def main():
    """Example usage of plan validator."""
    # Example: Validate a plan
    plan_data = {
        "feature_name": "Dark Mode Toggle",
        "overview": "Add a dark mode toggle to the application settings allowing users to switch between light and dark themes.",
        "goal": "Allow users to switch between light and dark themes",
        "scope": "UI toggle, theme context, CSS variables, localStorage persistence",
        "current_architecture": "React app with Tailwind CSS",
        "technical_approach": {
            "pattern": "React Context + CSS Variables",
            "rationale": "Standard React pattern for theme management"
        },
        "implementation_phases": [
            {
                "name": "Setup",
                "files_to_create": ["src/components/DarkModeToggle.tsx"],
                "files_to_modify": ["src/context/ThemeContext.tsx"],
                "steps": ["Add state", "Create toggle", "Add persistence"]
            }
        ],
        "risks": {
            "high": [],
            "medium": []
        },
        "testing_strategy": {
            "unit_tests": [
                {"name": "DarkModeToggle tests"}
            ]
        },
        "acceptance_criteria": [
            "User can toggle themes",
            "Theme persists across sessions"
        ],
        "rollback_plan": "Remove component, revert changes",
        "rollback_steps": ["Delete DarkModeToggle.tsx"],
        "ready_for_execution": True
    }

    validator = PlanValidator()
    result = validator.validate(plan_data)

    print(f"Validation Result: {'✅ VALID' if result.valid else '❌ INVALID'}")
    print(f"  Errors: {result.errors_count}")
    print(f"  Warnings: {result.warnings_count}")
    print(f"  Info: {result.info_count}")

    if result.issues:
        print("\nIssues:")
        for issue in result.issues:
            emoji = "❌" if issue.severity == ValidationSeverity.ERROR else "⚠️" if issue.severity == ValidationSeverity.WARNING else "ℹ️"
            print(f"  {emoji} [{issue.section}] {issue.message}")
            if issue.suggestion:
                print(f"     → {issue.suggestion}")


if __name__ == "__main__":
    main()
