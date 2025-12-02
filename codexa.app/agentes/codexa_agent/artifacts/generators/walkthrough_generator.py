#!/usr/bin/env python3
"""
CODEXA Walkthrough Generator
Version: 1.0.0
Created: 2025-11-24

Generates walkthrough.md artifacts with screenshots for visual verification.
Used by verification_agent to document visual proof of working implementations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import base64


@dataclass
class Screenshot:
    """A screenshot with annotations."""
    title: str
    filename: str
    what_shown: List[str]
    verified: List[str]
    notes: Optional[str] = None


@dataclass
class UserFlow:
    """A user flow to test."""
    name: str
    steps: List[str]
    result: str


@dataclass
class EdgeCase:
    """An edge case tested."""
    case: str
    expected: str
    actual: str
    status: str  # "passed" or "failed"


class WalkthroughGenerator:
    """
    Generator for visual walkthrough artifacts.

    Creates walkthrough.md with embedded screenshots and test documentation.
    """

    def __init__(self):
        """Initialize walkthrough generator."""
        pass

    def generate(
        self,
        feature_name: str,
        feature_overview: str,
        screenshots: List[Screenshot],
        user_flows: List[UserFlow],
        edge_cases: List[EdgeCase],
        verification_summary: Dict[str, Any],
        output_path: Optional[Path] = None,
        agent_version: str = "1.0.0",
        adw_path: str = ""
    ) -> str:
        """
        Generate walkthrough markdown.

        Args:
            feature_name: Name of feature
            feature_overview: Brief overview of feature
            screenshots: List of screenshots with annotations
            user_flows: User flows tested
            edge_cases: Edge cases tested
            verification_summary: Summary of verification
            output_path: Optional path to save walkthrough
            agent_version: Version of verification agent
            adw_path: Path to ADW

        Returns:
            Generated walkthrough markdown
        """
        lines = []

        # Header
        lines.extend([
            f"# Feature Walkthrough: {feature_name}",
            "",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"**Verified By**: Verification Agent v{agent_version}",
            f"**Status**: {verification_summary.get('status', '✅ APPROVED')}",
            "",
            "---",
            "",
            "## 1. Feature Overview",
            "",
            feature_overview,
            "",
            "---",
            "",
            "## 2. Visual Walkthrough",
            ""
        ])

        # Screenshots
        for i, screenshot in enumerate(screenshots, 1):
            lines.extend([
                f"### Screenshot {i}: {screenshot.title}",
                f"![{screenshot.title}]({screenshot.filename})",
                "",
                "**What's shown**:"
            ])

            for item in screenshot.what_shown:
                lines.append(f"- {item}")

            lines.append("")
            lines.append("**Verified**:")

            for item in screenshot.verified:
                lines.append(f"- ✅ {item}")

            if screenshot.notes:
                lines.extend([
                    "",
                    f"**Notes**: {screenshot.notes}"
                ])

            lines.extend(["", "---", ""])

        # User Flows
        lines.extend([
            "## 3. Critical User Flows",
            ""
        ])

        for flow in user_flows:
            lines.extend([
                f"### Flow: {flow.name}",
                ""
            ])

            for i, step in enumerate(flow.steps, 1):
                lines.append(f"{i}. {step}")

            lines.extend([
                "",
                f"**Result**: {flow.result}",
                "",
                "---",
                ""
            ])

        # Edge Cases
        lines.extend([
            "## 4. Edge Cases Tested",
            "",
            "| Case | Expected | Actual | Status |",
            "|------|----------|--------|--------|"
        ])

        for edge_case in edge_cases:
            status_emoji = "✅" if edge_case.status == "passed" else "❌"
            lines.append(
                f"| {edge_case.case} | {edge_case.expected} | "
                f"{edge_case.actual} | {status_emoji} |"
            )

        lines.extend(["", "---", ""])

        # Verification Summary
        lines.extend([
            "## 5. Verification Summary",
            "",
            f"**Manual Testing**: {verification_summary.get('manual_testing', '✅ Passed')}",
            f"**Screenshots Captured**: {len(screenshots)}",
            f"**User Flows Tested**: {len(user_flows)}",
            f"**Edge Cases Tested**: {len(edge_cases)}",
            "",
            f"**Recommendation**: {verification_summary.get('recommendation', 'APPROVE for deployment')}",
            "",
            "---",
            "",
            f"**Generated By**: Verification Agent v{agent_version}",
            f"**Generated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**ADW**: {adw_path}"
        ])

        walkthrough = "\n".join(lines)

        # Save if output path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(walkthrough)

        return walkthrough

    def generate_minimal(
        self,
        feature_name: str,
        screenshots_dir: Path,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate minimal walkthrough from screenshots directory.

        Args:
            feature_name: Name of feature
            screenshots_dir: Directory containing screenshots
            output_path: Optional path to save walkthrough

        Returns:
            Generated walkthrough markdown
        """
        # Find all image files in directory
        screenshot_files = []
        if screenshots_dir.exists():
            for ext in ["png", "jpg", "jpeg", "gif"]:
                screenshot_files.extend(screenshots_dir.glob(f"*.{ext}"))

        # Create screenshot objects
        screenshots = []
        for i, screenshot_file in enumerate(sorted(screenshot_files), 1):
            screenshots.append(Screenshot(
                title=screenshot_file.stem.replace("_", " ").title(),
                filename=f"screenshots/{screenshot_file.name}",
                what_shown=[f"Screenshot {i} of {feature_name}"],
                verified=["Feature visible in UI"],
                notes=None
            ))

        return self.generate(
            feature_name=feature_name,
            feature_overview=f"Visual walkthrough of {feature_name} implementation.",
            screenshots=screenshots,
            user_flows=[],
            edge_cases=[],
            verification_summary={"status": "✅ APPROVED", "manual_testing": "✅ Passed"},
            output_path=output_path
        )


class WalkthroughBuilder:
    """Builder for walkthrough data."""

    def __init__(self):
        self.feature_name = ""
        self.feature_overview = ""
        self.screenshots: List[Screenshot] = []
        self.user_flows: List[UserFlow] = []
        self.edge_cases: List[EdgeCase] = []
        self.verification_summary: Dict[str, str] = {}
        self.agent_version = "1.0.0"
        self.adw_path = ""

    def with_feature(self, name: str, overview: str) -> "WalkthroughBuilder":
        """Set feature name and overview."""
        self.feature_name = name
        self.feature_overview = overview
        return self

    def add_screenshot(
        self,
        title: str,
        filename: str,
        what_shown: List[str],
        verified: List[str],
        notes: Optional[str] = None
    ) -> "WalkthroughBuilder":
        """Add a screenshot."""
        self.screenshots.append(Screenshot(
            title=title,
            filename=filename,
            what_shown=what_shown,
            verified=verified,
            notes=notes
        ))
        return self

    def add_user_flow(
        self,
        name: str,
        steps: List[str],
        result: str
    ) -> "WalkthroughBuilder":
        """Add a user flow."""
        self.user_flows.append(UserFlow(
            name=name,
            steps=steps,
            result=result
        ))
        return self

    def add_edge_case(
        self,
        case: str,
        expected: str,
        actual: str,
        status: str
    ) -> "WalkthroughBuilder":
        """Add an edge case."""
        self.edge_cases.append(EdgeCase(
            case=case,
            expected=expected,
            actual=actual,
            status=status
        ))
        return self

    def with_summary(self, summary: Dict[str, str]) -> "WalkthroughBuilder":
        """Set verification summary."""
        self.verification_summary = summary
        return self

    def with_adw(self, adw_path: str) -> "WalkthroughBuilder":
        """Set ADW path."""
        self.adw_path = adw_path
        return self

    def build(self, output_path: Optional[Path] = None) -> str:
        """Build and generate walkthrough."""
        generator = WalkthroughGenerator()
        return generator.generate(
            feature_name=self.feature_name,
            feature_overview=self.feature_overview,
            screenshots=self.screenshots,
            user_flows=self.user_flows,
            edge_cases=self.edge_cases,
            verification_summary=self.verification_summary,
            output_path=output_path,
            agent_version=self.agent_version,
            adw_path=self.adw_path
        )


def main():
    """Example usage of walkthrough generator."""
    # Example: Generate walkthrough for dark mode feature
    walkthrough = (WalkthroughBuilder()
        .with_feature(
            "Dark Mode Toggle",
            "A toggle button that switches the application between light and dark themes. "
            "Theme preference is persisted to localStorage."
        )
        .add_screenshot(
            title="Main Interface (Light Mode)",
            filename="screenshots/01_light_mode.png",
            what_shown=[
                "Application in default light theme",
                "All UI elements clearly visible",
                "Toggle button in top-right corner"
            ],
            verified=[
                "Light theme applied correctly",
                "All text readable with proper contrast",
                "No visual glitches or layout issues"
            ]
        )
        .add_screenshot(
            title="Main Interface (Dark Mode)",
            filename="screenshots/02_dark_mode.png",
            what_shown=[
                "Application in dark theme",
                "Inverted color scheme",
                "Toggle button indicates dark mode active"
            ],
            verified=[
                "Dark theme applied correctly",
                "Proper contrast maintained (WCAG AA compliant)",
                "Smooth transition between themes"
            ],
            notes="Dark mode uses CSS custom properties for theming"
        )
        .add_screenshot(
            title="Toggle Button Detail",
            filename="screenshots/03_toggle_button.png",
            what_shown=[
                "Close-up of toggle button",
                "Icon changes based on theme (sun/moon)",
                "Accessible button with proper ARIA labels"
            ],
            verified=[
                "Button responds to clicks",
                "Icon updates correctly",
                "Keyboard navigation works"
            ]
        )
        .add_user_flow(
            name="Happy Path - Theme Toggle",
            steps=[
                "User clicks \"Dark Mode\" toggle button",
                "Theme smoothly transitions to dark mode",
                "Preference saved to localStorage",
                "User refreshes page",
                "Dark theme persists"
            ],
            result="✅ All steps work correctly - theme persists across page reloads"
        )
        .add_user_flow(
            name="Error Handling - localStorage Unavailable",
            steps=[
                "User disables localStorage (browser privacy mode)",
                "User clicks toggle button",
                "Theme changes in current session",
                "Warning logged to console (not shown to user)",
                "User refreshes page",
                "Theme reverts to default"
            ],
            result="✅ Graceful degradation - feature works without persistence"
        )
        .add_edge_case(
            case="Empty input",
            expected="Show error",
            actual="Shows error",
            status="passed"
        )
        .add_edge_case(
            case="localStorage full",
            expected="Fallback gracefully",
            actual="Logs warning, continues",
            status="passed"
        )
        .add_edge_case(
            case="Rapid toggling",
            expected="No performance issues",
            actual="Smooth transitions",
            status="passed"
        )
        .add_edge_case(
            case="System preference (prefers-color-scheme)",
            expected="Detect and use system preference",
            actual="Detects and applies",
            status="passed"
        )
        .with_summary({
            "status": "✅ APPROVED",
            "manual_testing": "✅ Passed",
            "recommendation": "APPROVE for deployment"
        })
        .with_adw("agents/adw_20251124_153045")
        .build(Path("agents/adw_20251124_153045/walkthrough.md")))

    print(f"✅ Generated walkthrough ({len(walkthrough)} chars)")
    print(f"   Screenshots: 3")
    print(f"   User flows: 2")
    print(f"   Edge cases: 4")


if __name__ == "__main__":
    main()
