#!/usr/bin/env python3
"""
Value Function Module for CODEXA Validators
Version: 1.0.1
Created: 2025-11-29
Updated: 2025-11-29

Implements the Value Function pattern from PRIME.md:
- Intermediate feedback signals during validation (not just final pass/fail)
- Confidence scoring (0.0-1.0) with gradient thresholds
- Action recommendations based on confidence level
- Early course correction capabilities

Philosophy: "Emotions in humans act as immediate feedback ('this feels wrong').
            Apply 'confidence signals' at each step, not just final validation."

Usage:
    from validators.value_function import ValueFunctionMixin, ConfidenceLevel

    class MyValidator(ValueFunctionMixin):
        def validate(self):
            # Check something
            confidence = self.assess_confidence(score=0.75, context="type_coverage")

            # Get recommended action
            action = self.get_recommended_action(confidence)

            # Generate gradient report
            report = self.generate_gradient_report()
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime


class ConfidenceLevel(Enum):
    """
    Gradient confidence levels with associated actions.

    Based on PRIME.md Value Function pattern:
    - CRITICAL (0.0-0.3): Stop, escalate, fundamental issue
    - LOW (0.3-0.7): Retry current step with refinement
    - MEDIUM (0.7-0.9): Continue but flag for review
    - HIGH (0.9-1.0): Proceed with high confidence
    """
    CRITICAL = "critical"   # 0.0 - 0.3
    LOW = "low"             # 0.3 - 0.7
    MEDIUM = "medium"       # 0.7 - 0.9
    HIGH = "high"           # 0.9 - 1.0

    @classmethod
    def from_score(cls, score: float) -> "ConfidenceLevel":
        """Convert numeric score to confidence level."""
        if score < 0.3:
            return cls.CRITICAL
        elif score < 0.7:
            return cls.LOW
        elif score < 0.9:
            return cls.MEDIUM
        else:
            return cls.HIGH


@dataclass
class ConfidenceCheckpoint:
    """
    Represents a single confidence checkpoint during validation.

    Captures the state at a specific point in the validation process,
    enabling intermediate feedback and early course correction.
    """
    name: str                          # Checkpoint identifier
    score: float                       # 0.0 - 1.0
    level: ConfidenceLevel             # Derived from score
    context: str                       # What was being checked
    timestamp: datetime                # When the check occurred
    details: Dict[str, Any] = field(default_factory=dict)
    recommendation: Optional[str] = None


@dataclass
class GradientReport:
    """
    Gradient feedback report with confidence scoring.

    Unlike binary pass/fail, provides nuanced feedback:
    - Overall confidence score
    - Per-checkpoint confidence
    - Action recommendations
    - Early warning indicators
    """
    overall_confidence: float          # 0.0 - 1.0
    overall_level: ConfidenceLevel     # Derived from overall_confidence
    checkpoints: List[ConfidenceCheckpoint]
    recommended_action: str
    warnings: List[str]
    escalation_required: bool
    human_review_recommended: bool

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "overall_confidence": round(self.overall_confidence, 3),
            "overall_level": self.overall_level.value,
            "recommended_action": self.recommended_action,
            "escalation_required": self.escalation_required,
            "human_review_recommended": self.human_review_recommended,
            "warnings": self.warnings,
            "checkpoints": [
                {
                    "name": cp.name,
                    "score": round(cp.score, 3),
                    "level": cp.level.value,
                    "context": cp.context,
                    "recommendation": cp.recommendation,
                    "details": cp.details
                }
                for cp in self.checkpoints
            ]
        }


class ValueFunctionMixin:
    """
    Mixin that adds Value Function capabilities to any validator.

    Provides:
    - Checkpoint tracking during validation
    - Confidence scoring with gradient thresholds
    - Action recommendations
    - Gradient report generation

    Usage:
        class MyValidator(ValueFunctionMixin):
            def validate(self, file):
                # Start validation
                self.add_checkpoint("file_structure",
                                   score=0.85,
                                   context="Checking file structure")

                # Continue validation
                self.add_checkpoint("naming_conventions",
                                   score=0.72,
                                   context="Checking naming conventions")

                # Get gradient report
                return self.generate_gradient_report()
    """

    # Configurable thresholds
    CONFIDENCE_THRESHOLDS = {
        "critical": 0.3,
        "low": 0.7,
        "acceptable": 0.85,
        "high": 0.9
    }

    # Action recommendations per level
    ACTION_RECOMMENDATIONS = {
        ConfidenceLevel.CRITICAL: (
            "STOP: Fundamental issue detected. Escalate to human review immediately."
        ),
        ConfidenceLevel.LOW: (
            "RETRY: Low confidence. Refine inputs and re-run validation."
        ),
        ConfidenceLevel.MEDIUM: (
            "CONTINUE: Acceptable confidence. Flag for human review before production."
        ),
        ConfidenceLevel.HIGH: (
            "PROCEED: High confidence. Safe to continue with automated workflow."
        )
    }

    def __init__(self, *args, **kwargs):
        """Initialize Value Function tracking."""
        super().__init__(*args, **kwargs)
        self._checkpoints: List[ConfidenceCheckpoint] = []
        self._warnings: List[str] = []

    def reset_checkpoints(self) -> None:
        """Clear all checkpoints for new validation run."""
        self._checkpoints = []
        self._warnings = []

    def add_checkpoint(
        self,
        name: str,
        score: float,
        context: str,
        details: Optional[Dict[str, Any]] = None,
        recommendation: Optional[str] = None
    ) -> ConfidenceCheckpoint:
        """
        Add a confidence checkpoint during validation.

        This is the core method for implementing Value Function pattern.
        Call this at each significant step of your validation process.

        Args:
            name: Identifier for this checkpoint (e.g., "type_coverage")
            score: Confidence score 0.0-1.0
            context: Description of what was checked
            details: Additional data about the check
            recommendation: Optional specific recommendation

        Returns:
            The created ConfidenceCheckpoint

        Example:
            self.add_checkpoint(
                name="docstring_coverage",
                score=0.65,
                context="Checking public function documentation",
                details={"functions_with_docs": 13, "total_functions": 20},
                recommendation="Add docstrings to remaining 7 functions"
            )
        """
        level = ConfidenceLevel.from_score(score)

        checkpoint = ConfidenceCheckpoint(
            name=name,
            score=score,
            level=level,
            context=context,
            timestamp=datetime.now(),
            details=details or {},
            recommendation=recommendation or self._generate_checkpoint_recommendation(
                name, score, level
            )
        )

        self._checkpoints.append(checkpoint)

        # Add warning if confidence is below threshold
        if level in (ConfidenceLevel.CRITICAL, ConfidenceLevel.LOW):
            warning_msg = f"[{level.value.upper()}] {name}: {context} (score: {score:.2f})"
            self._warnings.append(warning_msg)

        return checkpoint

    def _generate_checkpoint_recommendation(
        self,
        name: str,
        score: float,
        level: ConfidenceLevel
    ) -> str:
        """Generate automatic recommendation based on checkpoint level."""
        if level == ConfidenceLevel.CRITICAL:
            return f"Critical issue in {name}. Stop and investigate before proceeding."
        elif level == ConfidenceLevel.LOW:
            return f"Low confidence in {name}. Consider improvements before final review."
        elif level == ConfidenceLevel.MEDIUM:
            return f"Acceptable {name}. Flag for human verification."
        else:
            return f"{name} meets quality standards."

    def assess_confidence(
        self,
        score: float,
        context: str = "general"
    ) -> ConfidenceLevel:
        """
        Quick confidence assessment without creating checkpoint.

        Use this for lightweight checks that don't need full tracking.
        """
        return ConfidenceLevel.from_score(score)

    def get_recommended_action(self, level: ConfidenceLevel) -> str:
        """Get the recommended action for a confidence level."""
        return self.ACTION_RECOMMENDATIONS.get(level, "Unknown confidence level")

    def calculate_overall_confidence(self) -> float:
        """
        Calculate weighted overall confidence from all checkpoints.

        Uses a pessimistic approach: overall confidence is pulled down
        by low-confidence checkpoints more than it's pulled up by high ones.
        """
        if not self._checkpoints:
            return 1.0  # No checks = full confidence (nothing to fail)

        scores = [cp.score for cp in self._checkpoints]

        # Weighted calculation: lower scores have more impact
        # This implements the "fail early" principle
        min_score = min(scores)
        avg_score = sum(scores) / len(scores)

        # Weight: 60% average, 40% minimum (pessimistic bias)
        overall = (avg_score * 0.6) + (min_score * 0.4)

        return round(overall, 3)

    def should_escalate(self) -> bool:
        """Check if any checkpoint requires escalation."""
        return any(cp.level == ConfidenceLevel.CRITICAL for cp in self._checkpoints)

    def needs_human_review(self) -> bool:
        """Check if human review is recommended."""
        overall = self.calculate_overall_confidence()
        return overall < self.CONFIDENCE_THRESHOLDS["high"]

    def get_lowest_confidence_checkpoint(self) -> Optional[ConfidenceCheckpoint]:
        """Get the checkpoint with lowest confidence score."""
        if not self._checkpoints:
            return None
        return min(self._checkpoints, key=lambda cp: cp.score)

    def generate_gradient_report(self) -> GradientReport:
        """
        Generate a comprehensive gradient feedback report.

        This is the main output of Value Function validation.
        Use this instead of simple pass/fail for nuanced feedback.
        """
        overall_confidence = self.calculate_overall_confidence()
        overall_level = ConfidenceLevel.from_score(overall_confidence)

        return GradientReport(
            overall_confidence=overall_confidence,
            overall_level=overall_level,
            checkpoints=self._checkpoints.copy(),
            recommended_action=self.get_recommended_action(overall_level),
            warnings=self._warnings.copy(),
            escalation_required=self.should_escalate(),
            human_review_recommended=self.needs_human_review()
        )

    def print_gradient_summary(self, report: Optional[GradientReport] = None) -> None:
        """Print a human-readable gradient report summary."""
        import sys

        if report is None:
            report = self.generate_gradient_report()

        # ANSI colors (if available)
        colors = {
            ConfidenceLevel.CRITICAL: "\033[91m",  # Red
            ConfidenceLevel.LOW: "\033[93m",       # Yellow
            ConfidenceLevel.MEDIUM: "\033[94m",    # Blue
            ConfidenceLevel.HIGH: "\033[92m",      # Green
        }
        reset = "\033[0m"

        # Windows-safe symbols
        is_windows = sys.platform == 'win32'
        sym_check = "[OK]" if is_windows else "✓"
        sym_circle = "[o]" if is_windows else "○"
        sym_warn = "[!]" if is_windows else "!"
        sym_escalate = "[!!]" if is_windows else "⚠"
        sym_human = "[HR]" if is_windows else "👤"
        sym_arrow = " -> " if is_windows else " └─ "

        print("\n" + "=" * 60)
        print("  VALUE FUNCTION GRADIENT REPORT")
        print("=" * 60)

        # Overall confidence
        color = colors.get(report.overall_level, "")
        level_str = report.overall_level.value.upper()
        conf_pct = f"{report.overall_confidence:.1%}"
        print(f"\nOverall Confidence: {color}{conf_pct} ({level_str}){reset}")

        # Action
        print(f"\nRecommended Action:")
        print(f"  {report.recommended_action}")

        # Flags
        if report.escalation_required:
            esc_color = colors[ConfidenceLevel.CRITICAL]
            print(f"\n{esc_color}{sym_escalate} ESCALATION REQUIRED{reset}")
        if report.human_review_recommended:
            rev_color = colors[ConfidenceLevel.MEDIUM]
            print(f"\n{rev_color}{sym_human} Human Review Recommended{reset}")

        # Checkpoints
        if report.checkpoints:
            print(f"\nCheckpoints ({len(report.checkpoints)}):")
            for cp in report.checkpoints:
                color = colors.get(cp.level, "")
                if cp.level == ConfidenceLevel.HIGH:
                    status = sym_check
                elif cp.level == ConfidenceLevel.MEDIUM:
                    status = sym_circle
                else:
                    status = sym_warn
                score_str = f"{cp.score:.1%}"
                print(f"  {color}{status} {cp.name}: {score_str} ({cp.level.value}){reset}")
                needs_rec = cp.level in (ConfidenceLevel.CRITICAL, ConfidenceLevel.LOW)
                if cp.recommendation and needs_rec:
                    print(f"    {sym_arrow}{cp.recommendation}")

        # Warnings
        if report.warnings:
            print(f"\nWarnings ({len(report.warnings)}):")
            for warning in report.warnings:
                print(f"  - {warning}")

        print("\n" + "=" * 60 + "\n")


# === Utility Functions ===

def confidence_gate(
    threshold: float = 0.7,
    action_on_fail: str = "retry"
) -> Callable[[Callable], Callable]:
    """
    Decorator that adds confidence gating to a function.

    Args:
        threshold: Minimum confidence score to pass (0.0-1.0)
        action_on_fail: Action to recommend on failure ("retry", "escalate")

    Returns:
        Decorated function with confidence gating

    Usage:
        @confidence_gate(threshold=0.8, action_on_fail="escalate")
        def validate_critical_component(self, data) -> float:
            ...
            return confidence_score
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # If result is a tuple (score, data), extract score
            if isinstance(result, tuple):
                score = result[0]
            else:
                score = result

            level = ConfidenceLevel.from_score(score)

            if score < threshold:
                fn_name = func.__name__
                print(f"[CONFIDENCE GATE] {fn_name}: {score:.2f} < {threshold}")
                print(f"[ACTION] {action_on_fail.upper()}")

            return result
        return wrapper
    return decorator


# === Example Usage ===

if __name__ == "__main__":
    """Demonstrate Value Function usage."""

    class ExampleValidator(ValueFunctionMixin):
        """Example validator using Value Function pattern."""

        def validate(self, data: dict) -> GradientReport:
            """Run validation with confidence checkpoints."""
            self.reset_checkpoints()

            # Checkpoint 1: Schema validation
            schema_score = 0.95 if "required_field" in data else 0.3
            self.add_checkpoint(
                name="schema_validation",
                score=schema_score,
                context="Checking required fields",
                details={"fields_present": list(data.keys())}
            )

            # Checkpoint 2: Content quality
            content_score = min(len(data.get("content", "")) / 100, 1.0)
            self.add_checkpoint(
                name="content_quality",
                score=content_score,
                context="Checking content length and quality",
                details={"content_length": len(data.get("content", ""))}
            )

            # Checkpoint 3: Metadata
            meta_score = 0.85 if data.get("metadata") else 0.5
            self.add_checkpoint(
                name="metadata_check",
                score=meta_score,
                context="Verifying metadata presence"
            )

            return self.generate_gradient_report()

    # Demo
    validator = ExampleValidator()

    # Test case 1: Good data
    print("Test 1: Good data")
    report = validator.validate({
        "required_field": True,
        "content": "This is a sufficiently long content string " * 3,
        "metadata": {"author": "test"}
    })
    validator.print_gradient_summary(report)

    # Test case 2: Poor data
    print("Test 2: Poor data")
    report = validator.validate({
        "content": "short"
    })
    validator.print_gradient_summary(report)
