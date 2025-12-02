"""
Intelligent Fallback - Orchestrator Module
===========================================

The main orchestrator that coordinates fallback decisions based on
confidence reports, policies, history, and available strategies.

Version: 1.0.0
"""

import sys
import time
import uuid
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field

from .actions import (
    FallbackAction,
    FallbackResult,
    EscalationQuestion,
    EscalationReason,
    CorrectionResult
)
from .strategies import (
    AutoCorrectStrategy,
    VariationStrategy,
    get_auto_correct_strategy,
    get_applicable_variations,
    RiskLevel
)
from .policies import AutonomyPolicy, get_policy, detect_context
from .history import FallbackHistory, FallbackAttempt

# Import from parent validators package
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from value_function import GradientReport, ConfidenceLevel, ConfidenceCheckpoint
except ImportError:
    # Fallback if not available
    GradientReport = None
    ConfidenceLevel = None
    ConfidenceCheckpoint = None


@dataclass
class OrchestratorState:
    """Tracks the current state of a fallback session."""

    session_id: str
    total_attempts: int = 0
    auto_correct_attempts: int = 0
    variation_attempts: int = 0
    strategies_tried: List[str] = field(default_factory=list)
    cumulative_cost: float = 1.0
    start_time: float = field(default_factory=time.time)

    @property
    def elapsed_seconds(self) -> float:
        return time.time() - self.start_time


class IntelligentFallbackOrchestrator:
    """
    Orchestrates the intelligent fallback loop.

    Given a GradientReport (or confidence score), determines the best
    action to take based on:
    - Current confidence level
    - Configured policy
    - Historical success rates
    - Available strategies
    """

    def __init__(
        self,
        policy: Optional[str] = None,
        history_path: Optional[str] = None,
        custom_policy: Optional[AutonomyPolicy] = None
    ):
        """
        Initialize the orchestrator.

        Args:
            policy: Policy name (development, staging, production, research, testing)
                    If None, auto-detects from environment
            history_path: Path to history file (optional)
            custom_policy: Custom AutonomyPolicy to use instead of named policy
        """
        if custom_policy:
            self.policy = custom_policy
        else:
            policy_name = policy or detect_context()
            self.policy = get_policy(policy_name)

        self.history = FallbackHistory(history_path)
        self.state = OrchestratorState(session_id=str(uuid.uuid4())[:8])

        # Callbacks for executing corrections (set by integrations)
        self._correction_handlers: Dict[str, Callable] = {}
        self._variation_handlers: Dict[str, Callable] = {}

    def register_correction_handler(
        self,
        strategy_name: str,
        handler: Callable[[str, Dict[str, Any]], CorrectionResult]
    ) -> None:
        """Register a handler for executing a specific correction strategy."""
        self._correction_handlers[strategy_name] = handler

    def register_variation_handler(
        self,
        variation_name: str,
        handler: Callable[[Dict[str, Any]], bool]
    ) -> None:
        """Register a handler for applying a variation strategy."""
        self._variation_handlers[variation_name] = handler

    def handle(
        self,
        gradient_report: Optional[Any] = None,
        confidence: Optional[float] = None,
        checkpoints: Optional[List[Dict[str, Any]]] = None
    ) -> FallbackResult:
        """
        Determine the appropriate fallback action.

        Args:
            gradient_report: GradientReport from ValueFunctionMixin
            confidence: Overall confidence score (0.0-1.0)
            checkpoints: List of checkpoint dicts with name, score, level

        Returns:
            FallbackResult with action and context
        """
        # Extract confidence from gradient report if provided
        if gradient_report is not None and hasattr(gradient_report, 'overall_confidence'):
            confidence = gradient_report.overall_confidence
            checkpoints = [
                {
                    "name": cp.name,
                    "score": cp.score,
                    "level": cp.level.value if hasattr(cp.level, 'value') else str(cp.level)
                }
                for cp in gradient_report.checkpoints
            ]

        if confidence is None:
            raise ValueError("Must provide either gradient_report or confidence score")

        checkpoints = checkpoints or []

        # Check timeout
        if self.state.elapsed_seconds > self.policy.total_timeout_seconds:
            return self._escalate(
                confidence,
                [EscalationReason.MAX_RETRIES_EXCEEDED],
                "Total timeout exceeded"
            )

        # Check total attempts
        if self.state.total_attempts >= self.policy.total_attempt_limit:
            return self._escalate(
                confidence,
                [EscalationReason.MAX_RETRIES_EXCEEDED],
                f"Maximum attempts ({self.policy.total_attempt_limit}) exceeded"
            )

        # Level 0: High confidence - proceed
        if confidence >= self.policy.proceed_threshold:
            return FallbackResult(
                action=FallbackAction.PROCEED,
                message="High confidence - proceeding",
                confidence=confidence,
                attempt_number=self.state.total_attempts
            )

        # Level 1: Medium confidence - proceed with warning
        if confidence >= self.policy.warning_threshold:
            return FallbackResult(
                action=FallbackAction.PROCEED_WITH_WARNING,
                message=f"Medium confidence ({confidence:.1%}) - review recommended",
                confidence=confidence,
                attempt_number=self.state.total_attempts
            )

        # Identify problematic checkpoints
        critical = [c for c in checkpoints if c.get("level") == "critical"]
        low = [c for c in checkpoints if c.get("level") == "low"]
        problematic = critical + low

        # IMMEDIATE ESCALATION for security issues (never auto-correct security)
        security_critical = [
            c for c in critical
            if c.get("name", "").startswith("security")
        ]
        if security_critical:
            return self._escalate(
                confidence,
                [EscalationReason.SECURITY_CONCERN],
                "Security issue detected - immediate human review required",
                checkpoints=security_critical
            )

        # Level 2: Try auto-correction
        if confidence >= self.policy.retry_threshold:
            correction = self._try_auto_correct(problematic)
            if correction:
                return correction

        # Level 3: Try variation
        if self.state.variation_attempts < self.policy.max_variation_attempts:
            variation = self._try_variation(problematic)
            if variation:
                return variation

        # Level 4 or 5: Escalation
        if critical:
            return self._escalate(
                confidence,
                [EscalationReason.CRITICAL_CHECKPOINT],
                "Critical checkpoint(s) require human review",
                checkpoints=critical
            )

        if low:
            return self._partial_escalate(confidence, low)

        return self._escalate(
            confidence,
            [EscalationReason.CONFIDENCE_TOO_LOW],
            f"Confidence too low ({confidence:.1%}) after all attempts"
        )

    def _try_auto_correct(
        self,
        checkpoints: List[Dict[str, Any]]
    ) -> Optional[FallbackResult]:
        """Attempt auto-correction for problematic checkpoints."""
        if self.state.auto_correct_attempts >= self.policy.max_auto_retries:
            return None

        for checkpoint in checkpoints:
            name = checkpoint.get("name", "")
            strategy = get_auto_correct_strategy(name)

            if strategy is None:
                continue

            # Check if strategy is allowed
            if strategy.name in self.policy.blocked_strategies:
                continue

            # Check risk level
            risk_order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]
            if risk_order.index(strategy.risk_level) > risk_order.index(self.policy.max_risk_level):
                continue

            # Check if already tried
            if strategy.name in self.state.strategies_tried:
                continue

            # Check historical success rate
            if self.history.should_skip(strategy.name, name):
                continue

            # Check if confirmation required
            if strategy.requires_confirmation:
                return self._partial_escalate_for_strategy(
                    checkpoint,
                    strategy
                )

            # Attempt correction
            self.state.auto_correct_attempts += 1
            self.state.total_attempts += 1
            self.state.strategies_tried.append(strategy.name)

            return FallbackResult(
                action=FallbackAction.AUTO_CORRECT,
                message=f"Attempting auto-correction: {strategy.action}",
                strategy=strategy.to_dict(),
                checkpoint_name=name,
                attempt_number=self.state.total_attempts,
                confidence=checkpoint.get("score", 0.0)
            )

        return None

    def _try_variation(
        self,
        checkpoints: List[Dict[str, Any]]
    ) -> Optional[FallbackResult]:
        """Attempt a variation strategy."""
        if not checkpoints:
            return None

        # Get the most problematic checkpoint
        checkpoint = min(checkpoints, key=lambda c: c.get("score", 0))
        name = checkpoint.get("name", "")

        # Get applicable variations
        variations = get_applicable_variations(name)

        # Filter by policy and history
        viable_variations = []
        for var in variations:
            if var.name in self.state.strategies_tried:
                continue
            if var.name in self.policy.blocked_strategies:
                continue
            if self.history.should_skip(var.name, name):
                continue
            if var.cost_multiplier * self.state.cumulative_cost > self.policy.max_cost_multiplier:
                continue
            viable_variations.append(var)

        # Sort by preference and success rate
        def sort_key(v: VariationStrategy) -> float:
            base = self.history.success_rate_for_checkpoint(v.name, name)
            if v.name in self.policy.preferred_strategies:
                base += 0.2  # Boost preferred strategies
            return base

        viable_variations.sort(key=sort_key, reverse=True)

        if not viable_variations:
            return None

        # Select best variation
        variation = viable_variations[0]

        self.state.variation_attempts += 1
        self.state.total_attempts += 1
        self.state.strategies_tried.append(variation.name)
        self.state.cumulative_cost *= variation.cost_multiplier

        return FallbackResult(
            action=FallbackAction.RETRY_VARIATION,
            message=f"Retrying with variation: {variation.name}",
            strategy=variation.to_dict(),
            checkpoint_name=name,
            attempt_number=self.state.total_attempts,
            confidence=checkpoint.get("score", 0.0)
        )

    def _partial_escalate(
        self,
        confidence: float,
        checkpoints: List[Dict[str, Any]]
    ) -> FallbackResult:
        """Create partial escalation with specific questions."""
        questions = []
        for cp in checkpoints[:3]:  # Max 3 questions
            name = cp.get("name", "unknown")
            score = cp.get("score", 0.0)
            questions.append(
                EscalationQuestion(
                    checkpoint_name=name,
                    question=f"How should we handle {name} (current: {score:.1%})?",
                    options=["Retry with different approach", "Accept current state", "Skip this check"],
                    context=f"Checkpoint {name} has low confidence"
                )
            )

        return FallbackResult(
            action=FallbackAction.PARTIAL_ESCALATION,
            message="Need human input on specific decisions",
            questions=questions,
            confidence=confidence,
            attempt_number=self.state.total_attempts
        )

    def _partial_escalate_for_strategy(
        self,
        checkpoint: Dict[str, Any],
        strategy: AutoCorrectStrategy
    ) -> FallbackResult:
        """Create partial escalation for a strategy requiring confirmation."""
        name = checkpoint.get("name", "unknown")

        questions = [
            EscalationQuestion(
                checkpoint_name=name,
                question=f"Apply auto-correction '{strategy.name}'?",
                options=["Yes, apply correction", "No, skip this", "Escalate to full review"],
                context=f"Strategy: {strategy.description}",
                default="Yes, apply correction"
            )
        ]

        return FallbackResult(
            action=FallbackAction.PARTIAL_ESCALATION,
            message=f"Strategy '{strategy.name}' requires confirmation",
            strategy=strategy.to_dict(),
            checkpoint_name=name,
            questions=questions,
            confidence=checkpoint.get("score", 0.0),
            attempt_number=self.state.total_attempts
        )

    def _escalate(
        self,
        confidence: float,
        reasons: List[EscalationReason],
        message: str,
        checkpoints: Optional[List[Dict[str, Any]]] = None
    ) -> FallbackResult:
        """Create full escalation."""
        return FallbackResult(
            action=FallbackAction.FULL_ESCALATION,
            message=message,
            escalation_reasons=reasons,
            confidence=confidence,
            attempt_number=self.state.total_attempts,
            context={
                "checkpoints": checkpoints or [],
                "strategies_tried": self.state.strategies_tried,
                "cumulative_cost": self.state.cumulative_cost,
                "elapsed_seconds": self.state.elapsed_seconds
            }
        )

    def record_attempt_result(
        self,
        result: FallbackResult,
        success: bool,
        final_confidence: float,
        duration_ms: int,
        error: Optional[str] = None
    ) -> None:
        """Record the result of an attempt for learning."""
        attempt = FallbackAttempt.create(
            session_id=self.state.session_id,
            checkpoint_name=result.checkpoint_name or "unknown",
            initial_confidence=result.confidence,
            action=result.action,
            strategy=result.strategy.get("name") if result.strategy else None,
            final_confidence=final_confidence,
            success=success,
            duration_ms=duration_ms,
            error=error
        )
        self.history.record(attempt)

    def reset_session(self) -> None:
        """Reset the session state for a new fallback loop."""
        self.state = OrchestratorState(session_id=str(uuid.uuid4())[:8])

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics from history."""
        return self.history.get_analytics()


# =============================================================================
# MIXIN FOR EASY INTEGRATION
# =============================================================================

class FallbackMixin:
    """
    Mixin that adds intelligent fallback capabilities to any validator.

    Usage:
        class MyValidator(ValueFunctionMixin, FallbackMixin):
            def validate_with_fallback(self, target):
                return self.run_with_fallback(
                    lambda: self.validate(target),
                    policy="development"
                )
    """

    _fallback_orchestrator: Optional[IntelligentFallbackOrchestrator] = None

    def init_fallback(
        self,
        policy: str = "development",
        history_path: Optional[str] = None
    ) -> None:
        """Initialize the fallback orchestrator."""
        self._fallback_orchestrator = IntelligentFallbackOrchestrator(
            policy=policy,
            history_path=history_path
        )

    def run_with_fallback(
        self,
        validate_fn: Callable[[], Any],
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Run validation with intelligent fallback.

        Args:
            validate_fn: Function that performs validation and returns result
            max_iterations: Maximum fallback loop iterations

        Returns:
            Dict with final result and fallback summary
        """
        if self._fallback_orchestrator is None:
            self.init_fallback()

        orchestrator = self._fallback_orchestrator
        orchestrator.reset_session()

        iterations = 0
        results = []

        while iterations < max_iterations:
            iterations += 1
            start_time = time.time()

            # Run validation
            result = validate_fn()

            # Get gradient report if available
            gradient_report = None
            if hasattr(self, 'generate_gradient_report'):
                gradient_report = self.generate_gradient_report()

            # Get fallback decision
            fallback = orchestrator.handle(gradient_report=gradient_report)

            duration_ms = int((time.time() - start_time) * 1000)

            results.append({
                "iteration": iterations,
                "action": fallback.action.name,
                "confidence": fallback.confidence,
                "duration_ms": duration_ms
            })

            # Handle the fallback action
            if fallback.should_proceed:
                return {
                    "status": "success",
                    "result": result,
                    "iterations": iterations,
                    "final_action": fallback.action.name,
                    "history": results
                }

            if fallback.needs_human:
                return {
                    "status": "escalated",
                    "result": result,
                    "fallback": fallback.to_dict(),
                    "iterations": iterations,
                    "history": results
                }

            # Record for learning
            orchestrator.record_attempt_result(
                result=fallback,
                success=False,
                final_confidence=fallback.confidence,
                duration_ms=duration_ms
            )

            # For retry actions, the caller should apply corrections
            # This mixin just tracks state; actual corrections are handled externally

        return {
            "status": "max_iterations",
            "iterations": iterations,
            "history": results
        }
