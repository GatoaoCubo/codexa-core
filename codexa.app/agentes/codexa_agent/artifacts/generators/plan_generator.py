#!/usr/bin/env python3
"""
CODEXA Implementation Plan Generator
Version: 1.0.0
Created: 2025-11-24

Generates implementation_plan.md artifacts using Jinja2 templates.
Used by planning_agent to create structured, comprehensive implementation plans.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, Template
import json


@dataclass
class Pattern:
    """A code pattern used in the codebase."""
    name: str
    description: str


@dataclass
class RelevantFile:
    """A file relevant to the implementation."""
    path: str
    purpose: str


@dataclass
class Dependency:
    """An external dependency."""
    name: str
    version: str
    purpose: str


@dataclass
class Library:
    """A library to use in the implementation."""
    name: str
    version: str
    purpose: str
    rationale: str


@dataclass
class Alternative:
    """An alternative approach considered."""
    name: str
    pros: str
    cons: str


@dataclass
class DesignDecision:
    """A design decision made during planning."""
    name: str
    chosen: str
    rationale: str
    alternatives: List[Alternative]
    tradeoffs: Dict[str, str]


@dataclass
class FileChange:
    """A file to modify or create."""
    path: str
    reason: Optional[str] = None
    purpose: Optional[str] = None


@dataclass
class ImplementationPhase:
    """A phase in the implementation."""
    name: str
    duration: str
    files_to_modify: List[FileChange]
    files_to_create: List[FileChange]
    dependencies: List[str]
    steps: List[str]


@dataclass
class Risk:
    """A risk in the implementation."""
    name: str
    description: str
    impact: Optional[str] = None
    mitigation: Optional[str] = None


@dataclass
class Test:
    """A test to create."""
    name: str
    file: str
    tests_description: str
    coverage_target: Optional[str] = None
    flows: Optional[List[str]] = None
    user_flow: Optional[str] = None
    steps: Optional[int] = None


@dataclass
class TestData:
    """Test data requirements."""
    name: str
    description: str


@dataclass
class ImplementationPlan:
    """Complete implementation plan data."""
    feature_name: str
    overview: str
    goal: str
    scope: str
    current_architecture: str
    existing_patterns: List[Pattern]
    relevant_files: List[RelevantFile]
    dependencies: List[Dependency]
    technical_approach: Dict[str, Any]
    design_decisions: List[DesignDecision]
    implementation_phases: List[ImplementationPhase]
    risks: Dict[str, List[Risk]]
    testing_strategy: Dict[str, Any]
    acceptance_criteria: List[str]
    rollback_plan: str
    rollback_steps: List[str]
    files_summary: Dict[str, Any]
    next_steps: Dict[str, str]
    ready_for_execution: bool
    blocking_issues: List[str] = field(default_factory=list)

    # Metadata
    complexity: str = "Medium"
    estimated_duration: str = "2-3 hours"
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    generated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    agent_version: str = "1.0.0"
    adw_path: str = ""


class PlanGenerator:
    """
    Generator for implementation plan artifacts.

    Uses Jinja2 templates to generate structured implementation_plan.md files.
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize plan generator.

        Args:
            templates_dir: Directory containing Jinja2 templates
        """
        self.templates_dir = templates_dir or Path("artifacts/templates")
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate(
        self,
        plan: ImplementationPlan,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate implementation plan from data.

        Args:
            plan: Implementation plan data
            output_path: Optional path to save generated plan

        Returns:
            Generated implementation plan markdown
        """
        template = self.env.get_template("implementation_plan.jinja2")

        # Convert dataclasses to dicts for template
        context = self._plan_to_dict(plan)

        # Render template
        rendered = template.render(**context)

        # Save if output path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)

        return rendered

    def _plan_to_dict(self, plan: ImplementationPlan) -> Dict[str, Any]:
        """Convert ImplementationPlan to dictionary for template."""
        return {
            "feature_name": plan.feature_name,
            "created_at": plan.created_at,
            "complexity": plan.complexity,
            "estimated_duration": plan.estimated_duration,
            "agent_version": plan.agent_version,
            "overview": plan.overview,
            "goal": plan.goal,
            "scope": plan.scope,
            "current_architecture": plan.current_architecture,
            "existing_patterns": [
                {"name": p.name, "description": p.description}
                for p in plan.existing_patterns
            ],
            "relevant_files": [
                {"path": f.path, "purpose": f.purpose}
                for f in plan.relevant_files
            ],
            "dependencies": [
                {"name": d.name, "version": d.version, "purpose": d.purpose}
                for d in plan.dependencies
            ],
            "technical_approach": plan.technical_approach,
            "design_decisions": [
                {
                    "name": d.name,
                    "chosen": d.chosen,
                    "rationale": d.rationale,
                    "alternatives": [
                        {"name": a.name, "pros": a.pros, "cons": a.cons}
                        for a in d.alternatives
                    ],
                    "tradeoffs": d.tradeoffs
                }
                for d in plan.design_decisions
            ],
            "implementation_phases": [
                {
                    "name": p.name,
                    "duration": p.duration,
                    "files_to_modify": [
                        {"path": f.path, "reason": f.reason}
                        for f in p.files_to_modify
                    ],
                    "files_to_create": [
                        {"path": f.path, "purpose": f.purpose}
                        for f in p.files_to_create
                    ],
                    "dependencies": p.dependencies,
                    "steps": p.steps
                }
                for p in plan.implementation_phases
            ],
            "risks": {
                "high": [
                    {"name": r.name, "description": r.description, "impact": r.impact, "mitigation": r.mitigation}
                    for r in plan.risks.get("high", [])
                ],
                "medium": [
                    {"name": r.name, "description": r.description, "impact": r.impact, "mitigation": r.mitigation}
                    for r in plan.risks.get("medium", [])
                ],
                "low": [
                    {"name": r.name, "description": r.description}
                    for r in plan.risks.get("low", [])
                ]
            },
            "testing_strategy": plan.testing_strategy,
            "acceptance_criteria": plan.acceptance_criteria,
            "rollback_plan": plan.rollback_plan,
            "rollback_steps": plan.rollback_steps,
            "files_summary": plan.files_summary,
            "next_steps": plan.next_steps,
            "ready_for_execution": plan.ready_for_execution,
            "blocking_issues": plan.blocking_issues,
            "generated_at": plan.generated_at,
            "adw_path": plan.adw_path
        }

    def from_json(self, json_path: Path) -> ImplementationPlan:
        """
        Load implementation plan from JSON file.

        Args:
            json_path: Path to JSON file

        Returns:
            ImplementationPlan object
        """
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        # Convert JSON to ImplementationPlan
        # This is a simplified version - would need full conversion logic
        return ImplementationPlan(
            feature_name=data["feature_name"],
            overview=data["overview"],
            goal=data["goal"],
            scope=data["scope"],
            current_architecture=data["current_architecture"],
            existing_patterns=[
                Pattern(**p) for p in data.get("existing_patterns", [])
            ],
            relevant_files=[
                RelevantFile(**f) for f in data.get("relevant_files", [])
            ],
            dependencies=[
                Dependency(**d) for d in data.get("dependencies", [])
            ],
            technical_approach=data.get("technical_approach", {}),
            design_decisions=[
                DesignDecision(
                    name=d["name"],
                    chosen=d["chosen"],
                    rationale=d["rationale"],
                    alternatives=[Alternative(**a) for a in d.get("alternatives", [])],
                    tradeoffs=d.get("tradeoffs", {})
                )
                for d in data.get("design_decisions", [])
            ],
            implementation_phases=[
                ImplementationPhase(
                    name=p["name"],
                    duration=p["duration"],
                    files_to_modify=[FileChange(**f) for f in p.get("files_to_modify", [])],
                    files_to_create=[FileChange(**f) for f in p.get("files_to_create", [])],
                    dependencies=p.get("dependencies", []),
                    steps=p.get("steps", [])
                )
                for p in data.get("implementation_phases", [])
            ],
            risks=data.get("risks", {}),
            testing_strategy=data.get("testing_strategy", {}),
            acceptance_criteria=data.get("acceptance_criteria", []),
            rollback_plan=data.get("rollback_plan", ""),
            rollback_steps=data.get("rollback_steps", []),
            files_summary=data.get("files_summary", {}),
            next_steps=data.get("next_steps", {}),
            ready_for_execution=data.get("ready_for_execution", False),
            blocking_issues=data.get("blocking_issues", [])
        )


def main():
    """Example usage of plan generator."""
    # Create example implementation plan
    plan = ImplementationPlan(
        feature_name="Dark Mode Toggle",
        overview="Add a dark mode toggle to the application settings.",
        goal="Allow users to switch between light and dark themes.",
        scope="UI toggle, theme context, CSS variables, localStorage persistence.",
        current_architecture="React application with Tailwind CSS and context API.",
        existing_patterns=[
            Pattern("React Context", "Used for global state management"),
            Pattern("Tailwind CSS", "Utility-first CSS framework")
        ],
        relevant_files=[
            RelevantFile("src/App.tsx", "Main application component"),
            RelevantFile("src/context/ThemeContext.tsx", "Existing theme context")
        ],
        dependencies=[
            Dependency("react", "^18.2.0", "UI framework"),
            Dependency("tailwindcss", "^3.3.0", "CSS framework")
        ],
        technical_approach={
            "pattern": "React Context + CSS Variables",
            "rationale": "Standard React pattern for theme management",
            "libraries": [
                {
                    "name": "react",
                    "version": "^18.2.0",
                    "purpose": "UI framework",
                    "rationale": "Already in use"
                }
            ],
            "architecture": "Context provider wraps app, CSS variables for theming",
            "data_flow": "User clicks toggle → Context updates → CSS variables change → UI re-renders"
        },
        design_decisions=[
            DesignDecision(
                name="Theme Storage",
                chosen="localStorage",
                rationale="Persists user preference across sessions",
                alternatives=[
                    Alternative("Cookies", "Works across domains", "More complex, GDPR concerns"),
                    Alternative("No persistence", "Simpler", "Poor UX")
                ],
                tradeoffs={
                    "positive": "Simple, no backend needed",
                    "negative": "Not synced across devices",
                    "risks": "localStorage can be cleared"
                }
            )
        ],
        implementation_phases=[
            ImplementationPhase(
                name="Setup",
                duration="30 min",
                files_to_modify=[
                    FileChange("src/context/ThemeContext.tsx", "Add dark mode state")
                ],
                files_to_create=[
                    FileChange("src/components/DarkModeToggle.tsx", "Toggle component")
                ],
                dependencies=[],
                steps=[
                    "Add dark mode state to ThemeContext",
                    "Create toggle component",
                    "Add localStorage persistence"
                ]
            )
        ],
        risks={
            "high": [],
            "medium": [
                Risk(
                    "Browser compatibility",
                    "CSS variables not supported in old browsers",
                    "Users on old browsers see broken themes",
                    "Add fallback CSS"
                )
            ],
            "low": [
                Risk("localStorage quota", "Storage might be full")
            ]
        },
        testing_strategy={
            "unit_tests": [
                {
                    "name": "DarkModeToggle tests",
                    "file": "src/components/__tests__/DarkModeToggle.test.tsx",
                    "tests_description": "Toggle functionality, localStorage persistence",
                    "coverage_target": "100%"
                }
            ],
            "integration_tests": [],
            "e2e_tests": [],
            "test_data": []
        },
        acceptance_criteria=[
            "User can toggle between light and dark themes",
            "Theme preference persists across sessions",
            "All UI elements adapt to theme"
        ],
        rollback_plan="Remove DarkModeToggle component, revert ThemeContext changes",
        rollback_steps=[
            "Delete src/components/DarkModeToggle.tsx",
            "Revert src/context/ThemeContext.tsx"
        ],
        files_summary={
            "to_modify": 1,
            "to_create": 1,
            "total": 2,
            "estimated_lines": {
                "code": 150,
                "tests": 50,
                "config": 0,
                "total": 200
            },
            "complexity": {
                "high": 0,
                "medium": 1,
                "low": 1
            }
        },
        next_steps={
            "immediate": "Review plan with user",
            "after_approval": "Begin execution phase"
        },
        ready_for_execution=True,
        complexity="Medium",
        estimated_duration="2-3 hours",
        adw_path="agents/adw_20251124_153045"
    )

    # Generate plan
    generator = PlanGenerator()
    output_path = Path("agents/adw_20251124_153045/implementation_plan.md")

    rendered = generator.generate(plan, output_path)

    print(f"✅ Generated implementation plan: {output_path}")
    print(f"   Size: {len(rendered)} characters")
    print(f"   Sections: 11")


if __name__ == "__main__":
    main()
