"""
Intelligent Fallback - Actions Module
=====================================

Defines the possible actions the fallback system can take,
along with result types for communicating decisions.

Version: 1.0.0
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


class FallbackAction(Enum):
    """
    6 levels of fallback actions, from most autonomous to most conservative.

    The fallback orchestrator evaluates confidence scores and context
    to determine which action to take.
    """

    # Level 0: High confidence (>= 0.9) - proceed without interruption
    PROCEED = auto()

    # Level 1: Medium confidence (>= 0.7) - proceed but log warning
    PROCEED_WITH_WARNING = auto()

    # Level 2: Low confidence (>= 0.5) - attempt automatic correction
    AUTO_CORRECT = auto()

    # Level 3: Low confidence (>= 0.3) - retry with different approach
    RETRY_VARIATION = auto()

    # Level 4: Critical (< 0.3) - ask specific questions
    PARTIAL_ESCALATION = auto()

    # Level 5: Critical + high risk - full stop, wait for human
    FULL_ESCALATION = auto()


class EscalationReason(Enum):
    """Reasons why escalation was triggered."""

    CRITICAL_CHECKPOINT = "critical_checkpoint"
    MAX_RETRIES_EXCEEDED = "max_retries_exceeded"
    NO_VALID_STRATEGY = "no_valid_strategy"
    SECURITY_CONCERN = "security_concern"
    IRREVERSIBLE_ACTION = "irreversible_action"
    POLICY_VIOLATION = "policy_violation"
    CONFIDENCE_TOO_LOW = "confidence_too_low"


@dataclass
class EscalationQuestion:
    """A specific question to ask during partial escalation."""

    checkpoint_name: str
    question: str
    options: List[str]
    context: str
    default: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint": self.checkpoint_name,
            "question": self.question,
            "options": self.options,
            "context": self.context,
            "default": self.default
        }


@dataclass
class FallbackResult:
    """
    Result of a fallback decision.

    Contains the action to take, along with any necessary context
    for executing that action.
    """

    action: FallbackAction
    message: str

    # For AUTO_CORRECT and RETRY_VARIATION
    strategy: Optional[Dict[str, Any]] = None
    checkpoint_name: Optional[str] = None

    # For PARTIAL_ESCALATION
    questions: List[EscalationQuestion] = field(default_factory=list)

    # For FULL_ESCALATION
    escalation_reasons: List[EscalationReason] = field(default_factory=list)

    # For all actions - current state
    attempt_number: int = 0
    confidence: float = 0.0

    # For logging and debugging
    context: Dict[str, Any] = field(default_factory=dict)

    @property
    def should_retry(self) -> bool:
        """Whether this result indicates a retry should happen."""
        return self.action in (FallbackAction.AUTO_CORRECT, FallbackAction.RETRY_VARIATION)

    @property
    def should_proceed(self) -> bool:
        """Whether this result indicates work should proceed."""
        return self.action in (FallbackAction.PROCEED, FallbackAction.PROCEED_WITH_WARNING)

    @property
    def needs_human(self) -> bool:
        """Whether this result requires human intervention."""
        return self.action in (FallbackAction.PARTIAL_ESCALATION, FallbackAction.FULL_ESCALATION)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action.name,
            "message": self.message,
            "strategy": self.strategy,
            "checkpoint": self.checkpoint_name,
            "questions": [q.to_dict() for q in self.questions],
            "escalation_reasons": [r.value for r in self.escalation_reasons],
            "attempt": self.attempt_number,
            "confidence": self.confidence,
            "context": self.context
        }


@dataclass
class CorrectionResult:
    """Result of an auto-correction attempt."""

    success: bool
    checkpoint_name: str
    strategy_used: str
    before_confidence: float
    after_confidence: float
    changes_made: List[str] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def improvement(self) -> float:
        """How much confidence improved."""
        return self.after_confidence - self.before_confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "checkpoint": self.checkpoint_name,
            "strategy": self.strategy_used,
            "before": self.before_confidence,
            "after": self.after_confidence,
            "improvement": self.improvement,
            "changes": self.changes_made,
            "error": self.error
        }
