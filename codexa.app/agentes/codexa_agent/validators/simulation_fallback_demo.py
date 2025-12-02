#!/usr/bin/env python3
"""
Intelligent Fallback System - Live Simulation
==============================================

Demonstrates the interaction between Value Function and Intelligent Fallback
across multiple scenarios with varying confidence levels.

Run: python validators/simulation_fallback_demo.py

Version: 1.0.0
"""

import sys
import time
import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.value_function import (
    ValueFunctionMixin,
    GradientReport,
    ConfidenceLevel,
)
from validators.intelligent_fallback import (
    IntelligentFallbackOrchestrator,
    FallbackAction,
    FallbackResult,
    FallbackMixin,
    get_policy,
)


class Colors:
    """ANSI color codes."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(title: str) -> None:
    """Print a formatted header."""
    width = 70
    print(f"\n{Colors.CYAN}{'=' * width}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}  {title}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * width}{Colors.END}\n")


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.YELLOW}--- {title} ---{Colors.END}\n")


def print_result(label: str, value: Any, color: str = Colors.WHITE) -> None:
    """Print a labeled result."""
    print(f"  {Colors.BOLD}{label}:{Colors.END} {color}{value}{Colors.END}")


# =============================================================================
# SIMULATED VALIDATOR
# =============================================================================

@dataclass
class SimulatedFile:
    """Represents a file being validated."""
    name: str
    type_coverage: float
    doc_coverage: float
    complexity: float
    has_security_issue: bool = False


class SimulatedValidator(ValueFunctionMixin, FallbackMixin):
    """
    A simulated validator that demonstrates the Value Function + Fallback
    integration with configurable scenarios.
    """

    def __init__(self):
        super().__init__()
        self.files_validated = 0
        self.corrections_applied = 0
        self.current_file: Optional[SimulatedFile] = None

    def validate_file(self, file: SimulatedFile) -> Dict[str, Any]:
        """
        Validate a simulated file and generate confidence checkpoints.
        """
        self.reset_checkpoints()
        self.current_file = file
        self.files_validated += 1

        # Checkpoint 1: Type Coverage
        self.add_checkpoint(
            name="type_coverage",
            score=file.type_coverage,
            context=f"Type annotation coverage for {file.name}",
            details={"coverage_percent": file.type_coverage * 100}
        )

        # Checkpoint 2: Documentation
        self.add_checkpoint(
            name="doc_coverage",
            score=file.doc_coverage,
            context=f"Documentation coverage for {file.name}",
            details={"coverage_percent": file.doc_coverage * 100}
        )

        # Checkpoint 3: Complexity
        complexity_score = 1.0 - (file.complexity / 100)  # Lower complexity = higher score
        self.add_checkpoint(
            name="function_complexity",
            score=max(0.1, complexity_score),
            context=f"Code complexity analysis for {file.name}",
            details={"cyclomatic_complexity": file.complexity}
        )

        # Checkpoint 4: Security (if applicable)
        if file.has_security_issue:
            self.add_checkpoint(
                name="security_scan",
                score=0.2,
                context=f"Security vulnerability detected in {file.name}",
                details={"issue": "Potential SQL injection"}
            )

        return {
            "file": file.name,
            "checkpoints": len(self._checkpoints),
            "warnings": len(self._warnings)
        }

    def apply_correction(self, strategy_name: str) -> bool:
        """
        Simulate applying a correction strategy.
        Returns True if successful.
        """
        self.corrections_applied += 1

        # Simulate improvement based on strategy
        if self.current_file and strategy_name == "add_type_hints":
            old = self.current_file.type_coverage
            self.current_file.type_coverage = min(1.0, old + 0.3)
            print(f"    {Colors.GREEN}[CORRECTED]{Colors.END} type_coverage: "
                  f"{old:.0%} -> {self.current_file.type_coverage:.0%}")
            return True

        elif self.current_file and strategy_name == "generate_docstrings":
            old = self.current_file.doc_coverage
            self.current_file.doc_coverage = min(1.0, old + 0.4)
            print(f"    {Colors.GREEN}[CORRECTED]{Colors.END} doc_coverage: "
                  f"{old:.0%} -> {self.current_file.doc_coverage:.0%}")
            return True

        return False


# =============================================================================
# SIMULATION SCENARIOS
# =============================================================================

def scenario_high_quality_file():
    """Scenario 1: High quality file - should PROCEED immediately."""
    print_header("SCENARIO 1: High Quality File")
    print("A well-written file with good coverage - expects PROCEED\n")

    file = SimulatedFile(
        name="utils/helpers.py",
        type_coverage=0.95,
        doc_coverage=0.90,
        complexity=15
    )

    validator = SimulatedValidator()
    orchestrator = IntelligentFallbackOrchestrator(policy="development")

    # Validate
    validator.validate_file(file)
    report = validator.generate_gradient_report()

    # Get fallback decision
    result = orchestrator.handle(gradient_report=report)

    # Display results
    print_section("Validation Results")
    print_result("File", file.name)
    print_result("Overall Confidence", f"{report.overall_confidence:.1%}",
                 Colors.GREEN if report.overall_confidence >= 0.9 else Colors.YELLOW)
    print_result("Fallback Action", result.action.name,
                 Colors.GREEN if result.action == FallbackAction.PROCEED else Colors.YELLOW)
    print_result("Message", result.message)

    validator.print_gradient_summary(report)

    return result.action == FallbackAction.PROCEED


def scenario_medium_quality_file():
    """Scenario 2: Medium quality file - should PROCEED_WITH_WARNING."""
    print_header("SCENARIO 2: Medium Quality File")
    print("Acceptable file but needs improvement - expects PROCEED_WITH_WARNING\n")

    file = SimulatedFile(
        name="services/api_client.py",
        type_coverage=0.75,
        doc_coverage=0.70,
        complexity=25
    )

    validator = SimulatedValidator()
    orchestrator = IntelligentFallbackOrchestrator(policy="development")

    validator.validate_file(file)
    report = validator.generate_gradient_report()
    result = orchestrator.handle(gradient_report=report)

    print_section("Validation Results")
    print_result("File", file.name)
    print_result("Overall Confidence", f"{report.overall_confidence:.1%}",
                 Colors.YELLOW)
    print_result("Fallback Action", result.action.name,
                 Colors.YELLOW)
    print_result("Human Review", "Recommended" if report.human_review_recommended else "Not needed",
                 Colors.YELLOW if report.human_review_recommended else Colors.GREEN)

    validator.print_gradient_summary(report)

    return result.action == FallbackAction.PROCEED_WITH_WARNING


def scenario_low_quality_with_autocorrect():
    """Scenario 3: Low quality file - should AUTO_CORRECT and improve."""
    print_header("SCENARIO 3: Low Quality File with Auto-Correction")
    print("Poor coverage but correctable - expects AUTO_CORRECT loop\n")

    file = SimulatedFile(
        name="models/user.py",
        type_coverage=0.40,
        doc_coverage=0.30,
        complexity=20
    )

    validator = SimulatedValidator()
    orchestrator = IntelligentFallbackOrchestrator(policy="development")

    max_iterations = 5
    iteration = 0

    print_section("Fallback Loop")

    while iteration < max_iterations:
        iteration += 1
        print(f"\n{Colors.CYAN}[Iteration {iteration}]{Colors.END}")

        # Validate
        validator.validate_file(file)
        report = validator.generate_gradient_report()

        print(f"  Confidence: {report.overall_confidence:.1%} ({report.overall_level.value})")

        # Get fallback decision
        result = orchestrator.handle(gradient_report=report)
        print(f"  Action: {result.action.name}")

        if result.should_proceed:
            print(f"\n{Colors.GREEN}[SUCCESS]{Colors.END} Validation passed after {iteration} iterations")
            break

        if result.action == FallbackAction.AUTO_CORRECT:
            strategy = result.strategy
            if strategy:
                print(f"  Strategy: {strategy.get('name', 'unknown')}")
                validator.apply_correction(strategy.get('name', ''))

        elif result.action == FallbackAction.RETRY_VARIATION:
            strategy = result.strategy
            if strategy:
                print(f"  Variation: {strategy.get('name', 'unknown')}")
                # Simulate improvement from variation
                file.type_coverage = min(1.0, file.type_coverage + 0.15)
                file.doc_coverage = min(1.0, file.doc_coverage + 0.20)

        elif result.needs_human:
            print(f"\n{Colors.YELLOW}[ESCALATED]{Colors.END} Human review required")
            break

    print_section("Final State")
    print_result("Iterations", iteration)
    print_result("Corrections Applied", validator.corrections_applied)
    print_result("Final Type Coverage", f"{file.type_coverage:.0%}")
    print_result("Final Doc Coverage", f"{file.doc_coverage:.0%}")

    return iteration < max_iterations


def scenario_critical_security_issue():
    """Scenario 4: Security issue - should ESCALATE immediately."""
    print_header("SCENARIO 4: Critical Security Issue")
    print("File with security vulnerability - expects immediate ESCALATION\n")

    file = SimulatedFile(
        name="auth/login_handler.py",
        type_coverage=0.80,
        doc_coverage=0.75,
        complexity=30,
        has_security_issue=True
    )

    validator = SimulatedValidator()
    # Use production policy - more conservative
    orchestrator = IntelligentFallbackOrchestrator(policy="production")

    validator.validate_file(file)
    report = validator.generate_gradient_report()
    result = orchestrator.handle(gradient_report=report)

    print_section("Validation Results")
    print_result("File", file.name)
    print_result("Overall Confidence", f"{report.overall_confidence:.1%}",
                 Colors.RED)
    print_result("Escalation Required", "YES" if report.escalation_required else "NO",
                 Colors.RED if report.escalation_required else Colors.GREEN)
    print_result("Fallback Action", result.action.name,
                 Colors.RED)

    if result.needs_human:
        print(f"\n{Colors.RED}[CRITICAL]{Colors.END} Security issue requires human review!")
        if result.questions:
            print("\nQuestions for human:")
            for q in result.questions:
                print(f"  - {q.question}")

    validator.print_gradient_summary(report)

    return result.needs_human or report.escalation_required


def scenario_policy_comparison():
    """Scenario 5: Compare different policies on same file."""
    print_header("SCENARIO 5: Policy Comparison")
    print("Same file validated with different autonomy policies\n")

    file = SimulatedFile(
        name="core/processor.py",
        type_coverage=0.55,
        doc_coverage=0.50,
        complexity=35
    )

    policies = ["development", "staging", "production", "research"]
    results = {}

    for policy_name in policies:
        validator = SimulatedValidator()
        orchestrator = IntelligentFallbackOrchestrator(policy=policy_name)
        policy = get_policy(policy_name)

        validator.validate_file(file)
        report = validator.generate_gradient_report()
        result = orchestrator.handle(gradient_report=report)

        results[policy_name] = {
            "action": result.action.name,
            "confidence": report.overall_confidence,
            "escalation_threshold": policy.escalation_threshold,
            "max_retries": policy.max_auto_retries
        }

    print_section("Results by Policy")
    print(f"\n  {'Policy':<15} {'Action':<25} {'Threshold':<12} {'Max Retries'}")
    print(f"  {'-'*15} {'-'*25} {'-'*12} {'-'*11}")

    for policy_name, data in results.items():
        action_color = {
            "PROCEED": Colors.GREEN,
            "PROCEED_WITH_WARNING": Colors.YELLOW,
            "AUTO_CORRECT": Colors.CYAN,
            "RETRY_VARIATION": Colors.BLUE,
            "PARTIAL_ESCALATION": Colors.MAGENTA,
            "FULL_ESCALATION": Colors.RED,
        }.get(data["action"], Colors.WHITE)

        print(f"  {policy_name:<15} {action_color}{data['action']:<25}{Colors.END} "
              f"{data['escalation_threshold']:<12.0%} {data['max_retries']}")

    print(f"\n  File confidence: {file.type_coverage:.0%} type, {file.doc_coverage:.0%} doc")

    return True


def scenario_learning_from_history():
    """Scenario 6: Demonstrate historical learning."""
    print_header("SCENARIO 6: Learning from History")
    print("Shows how the system learns from past attempts\n")

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        history_path = f.name

    try:
        orchestrator = IntelligentFallbackOrchestrator(
            policy="development",
            history_path=history_path
        )

        # Simulate several attempts with different outcomes
        simulations = [
            ("add_type_hints", True, 0.4, 0.8),   # Success
            ("add_type_hints", True, 0.3, 0.7),   # Success
            ("generate_docstrings", True, 0.2, 0.6),  # Success
            ("add_type_hints", False, 0.5, 0.5),  # Failure
            ("temperature_increase", False, 0.4, 0.4),  # Failure
            ("temperature_increase", False, 0.3, 0.3),  # Failure
            ("temperature_increase", False, 0.35, 0.35),  # Failure (consecutive)
        ]

        print_section("Recording Attempts")
        for strategy, success, initial, final in simulations:
            result = FallbackResult(
                action=FallbackAction.AUTO_CORRECT,
                message="Test",
                checkpoint_name="test",
                strategy={"name": strategy},
                confidence=initial,
                attempt_number=1
            )
            orchestrator.record_attempt_result(
                result=result,
                success=success,
                final_confidence=final,
                duration_ms=100
            )
            status = Colors.GREEN + "SUCCESS" + Colors.END if success else Colors.RED + "FAIL" + Colors.END
            print(f"  {strategy:<25} {status}")

        # Check analytics
        analytics = orchestrator.get_analytics()

        print_section("Strategy Performance")
        print(f"\n  {'Strategy':<25} {'Attempts':<10} {'Success Rate':<15} {'Should Skip?'}")
        print(f"  {'-'*25} {'-'*10} {'-'*15} {'-'*12}")

        for name, stats in analytics.get("strategies", {}).items():
            rate = stats.get("success_rate", 0)
            attempts = stats.get("attempts", 0)
            consecutive_failures = stats.get("consecutive_failures", 0)

            should_skip = orchestrator.history.should_skip(name)
            skip_color = Colors.RED if should_skip else Colors.GREEN
            skip_text = "YES" if should_skip else "NO"

            rate_color = Colors.GREEN if rate >= 0.5 else Colors.YELLOW if rate >= 0.3 else Colors.RED

            print(f"  {name:<25} {attempts:<10} {rate_color}{rate:<15.0%}{Colors.END} "
                  f"{skip_color}{skip_text}{Colors.END}")

        print(f"\n{Colors.CYAN}[INSIGHT]{Colors.END} temperature_increase has 3 consecutive failures")
        print(f"          -> Will be SKIPPED in future attempts to save resources")

        return True

    finally:
        Path(history_path).unlink(missing_ok=True)


# =============================================================================
# MAIN SIMULATION
# =============================================================================

def run_simulation():
    """Run all simulation scenarios."""
    print_header("INTELLIGENT FALLBACK SYSTEM - LIVE SIMULATION")
    print(f"This simulation demonstrates the Value Function + Fallback integration.\n")
    print(f"Components:")
    print(f"  - {Colors.CYAN}Value Function{Colors.END}: Provides confidence scoring (0.0-1.0)")
    print(f"  - {Colors.CYAN}Intelligent Fallback{Colors.END}: Decides actions based on confidence")
    print(f"  - {Colors.CYAN}Policies{Colors.END}: Control autonomy level (dev/staging/prod)")
    print(f"  - {Colors.CYAN}History{Colors.END}: Learns from past attempts")

    scenarios = [
        ("High Quality File", scenario_high_quality_file),
        ("Medium Quality File", scenario_medium_quality_file),
        ("Low Quality + Auto-Correct", scenario_low_quality_with_autocorrect),
        ("Critical Security Issue", scenario_critical_security_issue),
        ("Policy Comparison", scenario_policy_comparison),
        ("Learning from History", scenario_learning_from_history),
    ]

    results = []
    for name, scenario_fn in scenarios:
        try:
            success = scenario_fn()
            results.append((name, success))
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR]{Colors.END} {name}: {e}")
            results.append((name, False))

    # Summary
    print_header("SIMULATION SUMMARY")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"  Scenarios: {passed}/{total} passed\n")

    for name, success in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if success else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  [{status}] {name}")

    print(f"\n{Colors.CYAN}{'=' * 70}{Colors.END}")

    # Key insights
    print(f"\n{Colors.BOLD}KEY INSIGHTS:{Colors.END}")
    print(f"""
  1. {Colors.GREEN}PROCEED{Colors.END} (>= 0.9): High quality code passes immediately
  2. {Colors.YELLOW}PROCEED_WITH_WARNING{Colors.END} (>= 0.7): Acceptable but flagged
  3. {Colors.CYAN}AUTO_CORRECT{Colors.END} (>= 0.5): System attempts to fix issues
  4. {Colors.BLUE}RETRY_VARIATION{Colors.END} (>= 0.3): Tries different approaches
  5. {Colors.MAGENTA}PARTIAL_ESCALATION{Colors.END} (< 0.3): Asks specific questions
  6. {Colors.RED}FULL_ESCALATION{Colors.END} (critical): Stops for human review

  {Colors.BOLD}Policies{Colors.END} control how aggressive the system is:
  - {Colors.GREEN}development{Colors.END}: Most permissive, tries many corrections
  - {Colors.YELLOW}staging{Colors.END}: Balanced approach
  - {Colors.RED}production{Colors.END}: Conservative, escalates quickly

  {Colors.BOLD}Learning{Colors.END} improves over time:
  - Strategies that fail repeatedly are skipped
  - Successful strategies are preferred
  - History is persisted for future sessions
""")

    return passed == total


if __name__ == "__main__":
    success = run_simulation()
    sys.exit(0 if success else 1)
