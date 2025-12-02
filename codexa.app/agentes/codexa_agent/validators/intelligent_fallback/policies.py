"""
Intelligent Fallback - Policies Module
=======================================

Defines autonomy policies that control how aggressive or conservative
the fallback system behaves in different contexts.

Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

from .strategies import RiskLevel


class PolicyContext(Enum):
    """Available policy contexts."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    RESEARCH = "research"
    TESTING = "testing"


@dataclass
class AutonomyPolicy:
    """
    Defines the autonomy boundaries for a specific context.

    Controls how the fallback system behaves - from aggressive
    (tries many things before escalating) to conservative
    (escalates quickly).
    """

    name: str
    description: str

    # Retry limits
    max_auto_retries: int = 3
    max_variation_attempts: int = 2
    total_attempt_limit: int = 5

    # Confidence thresholds
    proceed_threshold: float = 0.9  # Above this, proceed without warning
    warning_threshold: float = 0.7  # Above this, proceed with warning
    retry_threshold: float = 0.5  # Above this, attempt auto-correct
    escalation_threshold: float = 0.3  # Below this, escalate

    # Risk tolerance
    max_risk_level: RiskLevel = RiskLevel.MEDIUM
    allow_irreversible: bool = False

    # Operation permissions
    allow_file_creation: bool = True
    allow_file_deletion: bool = False
    allow_file_modification: bool = True
    allow_model_upgrade: bool = True
    allow_external_calls: bool = True

    # Strategy restrictions
    blocked_strategies: List[str] = field(default_factory=list)
    preferred_strategies: List[str] = field(default_factory=list)

    # Cost controls
    max_cost_multiplier: float = 5.0  # Max cumulative cost increase

    # Timeout controls
    per_attempt_timeout_seconds: int = 60
    total_timeout_seconds: int = 300

    # Logging and audit
    log_all_attempts: bool = True
    require_audit_trail: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "retries": {
                "auto": self.max_auto_retries,
                "variation": self.max_variation_attempts,
                "total": self.total_attempt_limit
            },
            "thresholds": {
                "proceed": self.proceed_threshold,
                "warning": self.warning_threshold,
                "retry": self.retry_threshold,
                "escalation": self.escalation_threshold
            },
            "risk": {
                "max_level": self.max_risk_level.value,
                "allow_irreversible": self.allow_irreversible
            },
            "permissions": {
                "create_files": self.allow_file_creation,
                "delete_files": self.allow_file_deletion,
                "modify_files": self.allow_file_modification,
                "model_upgrade": self.allow_model_upgrade,
                "external_calls": self.allow_external_calls
            },
            "strategies": {
                "blocked": self.blocked_strategies,
                "preferred": self.preferred_strategies
            },
            "limits": {
                "max_cost": self.max_cost_multiplier,
                "per_attempt_timeout": self.per_attempt_timeout_seconds,
                "total_timeout": self.total_timeout_seconds
            },
            "audit": {
                "log_all": self.log_all_attempts,
                "require_trail": self.require_audit_trail
            }
        }


# =============================================================================
# PREDEFINED POLICIES
# =============================================================================

AUTONOMY_POLICIES: Dict[str, AutonomyPolicy] = {
    # Development: Most permissive, encourages experimentation
    "development": AutonomyPolicy(
        name="development",
        description="Permissive policy for local development",
        max_auto_retries=3,
        max_variation_attempts=3,
        total_attempt_limit=8,
        proceed_threshold=0.85,
        warning_threshold=0.65,
        retry_threshold=0.4,
        escalation_threshold=0.25,
        max_risk_level=RiskLevel.MEDIUM,
        allow_file_creation=True,
        allow_file_deletion=False,  # Still careful with deletions
        allow_file_modification=True,
        allow_model_upgrade=True,
        max_cost_multiplier=10.0,
        per_attempt_timeout_seconds=120,
        total_timeout_seconds=600,
        log_all_attempts=True,
        require_audit_trail=False
    ),

    # Staging: Balanced approach
    "staging": AutonomyPolicy(
        name="staging",
        description="Balanced policy for staging/testing environments",
        max_auto_retries=2,
        max_variation_attempts=2,
        total_attempt_limit=5,
        proceed_threshold=0.9,
        warning_threshold=0.7,
        retry_threshold=0.5,
        escalation_threshold=0.3,
        max_risk_level=RiskLevel.LOW,
        allow_file_creation=True,
        allow_file_deletion=False,
        allow_file_modification=True,
        allow_model_upgrade=True,
        max_cost_multiplier=5.0,
        per_attempt_timeout_seconds=60,
        total_timeout_seconds=300,
        log_all_attempts=True,
        require_audit_trail=True
    ),

    # Production: Most conservative
    "production": AutonomyPolicy(
        name="production",
        description="Conservative policy for production environments",
        max_auto_retries=1,
        max_variation_attempts=1,
        total_attempt_limit=2,
        proceed_threshold=0.95,
        warning_threshold=0.8,
        retry_threshold=0.6,
        escalation_threshold=0.5,  # Higher threshold - escalate sooner
        max_risk_level=RiskLevel.LOW,
        allow_file_creation=False,
        allow_file_deletion=False,
        allow_file_modification=False,  # Read-only in production
        allow_model_upgrade=False,  # Cost control
        blocked_strategies=["reorganize_files", "remove_dead_code", "fix_naming"],
        max_cost_multiplier=2.0,
        per_attempt_timeout_seconds=30,
        total_timeout_seconds=60,
        log_all_attempts=True,
        require_audit_trail=True
    ),

    # Research: Maximum autonomy for experimentation
    "research": AutonomyPolicy(
        name="research",
        description="Maximum autonomy for research and experimentation",
        max_auto_retries=5,
        max_variation_attempts=5,
        total_attempt_limit=15,
        proceed_threshold=0.8,
        warning_threshold=0.5,
        retry_threshold=0.3,
        escalation_threshold=0.15,  # Very tolerant
        max_risk_level=RiskLevel.HIGH,
        allow_irreversible=True,  # Allow risky operations
        allow_file_creation=True,
        allow_file_deletion=True,  # Allow cleanup
        allow_file_modification=True,
        allow_model_upgrade=True,
        max_cost_multiplier=20.0,  # Allow expensive experiments
        per_attempt_timeout_seconds=300,
        total_timeout_seconds=1800,
        log_all_attempts=True,
        require_audit_trail=False
    ),

    # Testing: Focused on validation
    "testing": AutonomyPolicy(
        name="testing",
        description="Policy optimized for test execution and validation",
        max_auto_retries=2,
        max_variation_attempts=1,
        total_attempt_limit=4,
        proceed_threshold=0.9,
        warning_threshold=0.7,
        retry_threshold=0.5,
        escalation_threshold=0.3,
        max_risk_level=RiskLevel.LOW,
        allow_file_creation=True,  # For test outputs
        allow_file_deletion=True,  # For cleanup
        allow_file_modification=False,  # Don't modify source during tests
        allow_model_upgrade=False,
        preferred_strategies=["temperature_decrease", "add_constraints"],
        max_cost_multiplier=3.0,
        per_attempt_timeout_seconds=60,
        total_timeout_seconds=180,
        log_all_attempts=True,
        require_audit_trail=True
    ),
}


# =============================================================================
# POLICY MANAGEMENT
# =============================================================================

def get_policy(context: str) -> AutonomyPolicy:
    """
    Get the autonomy policy for a given context.

    Args:
        context: Policy context name (development, staging, production, research, testing)

    Returns:
        AutonomyPolicy for the context

    Raises:
        ValueError: If context is unknown
    """
    if context not in AUTONOMY_POLICIES:
        raise ValueError(
            f"Unknown policy context: {context}. "
            f"Available: {list(AUTONOMY_POLICIES.keys())}"
        )
    return AUTONOMY_POLICIES[context]


def create_custom_policy(
    base: str,
    overrides: Dict[str, Any]
) -> AutonomyPolicy:
    """
    Create a custom policy based on an existing one with overrides.

    Args:
        base: Name of the base policy to start from
        overrides: Dictionary of field overrides

    Returns:
        New AutonomyPolicy with overrides applied
    """
    base_policy = get_policy(base)
    base_dict = base_policy.to_dict()

    # Flatten nested dicts for override
    flat_overrides = {}
    for key, value in overrides.items():
        if isinstance(value, dict):
            # Handle nested overrides
            if key in base_dict and isinstance(base_dict[key], dict):
                base_dict[key].update(value)
        else:
            flat_overrides[key] = value

    # Create new policy with overrides
    return AutonomyPolicy(
        name=overrides.get("name", f"{base}_custom"),
        description=overrides.get("description", f"Custom policy based on {base}"),
        max_auto_retries=flat_overrides.get("max_auto_retries", base_policy.max_auto_retries),
        max_variation_attempts=flat_overrides.get("max_variation_attempts", base_policy.max_variation_attempts),
        total_attempt_limit=flat_overrides.get("total_attempt_limit", base_policy.total_attempt_limit),
        proceed_threshold=flat_overrides.get("proceed_threshold", base_policy.proceed_threshold),
        warning_threshold=flat_overrides.get("warning_threshold", base_policy.warning_threshold),
        retry_threshold=flat_overrides.get("retry_threshold", base_policy.retry_threshold),
        escalation_threshold=flat_overrides.get("escalation_threshold", base_policy.escalation_threshold),
        max_risk_level=flat_overrides.get("max_risk_level", base_policy.max_risk_level),
        allow_irreversible=flat_overrides.get("allow_irreversible", base_policy.allow_irreversible),
        allow_file_creation=flat_overrides.get("allow_file_creation", base_policy.allow_file_creation),
        allow_file_deletion=flat_overrides.get("allow_file_deletion", base_policy.allow_file_deletion),
        allow_file_modification=flat_overrides.get("allow_file_modification", base_policy.allow_file_modification),
        allow_model_upgrade=flat_overrides.get("allow_model_upgrade", base_policy.allow_model_upgrade),
        allow_external_calls=flat_overrides.get("allow_external_calls", base_policy.allow_external_calls),
        blocked_strategies=flat_overrides.get("blocked_strategies", base_policy.blocked_strategies),
        preferred_strategies=flat_overrides.get("preferred_strategies", base_policy.preferred_strategies),
        max_cost_multiplier=flat_overrides.get("max_cost_multiplier", base_policy.max_cost_multiplier),
        per_attempt_timeout_seconds=flat_overrides.get("per_attempt_timeout_seconds", base_policy.per_attempt_timeout_seconds),
        total_timeout_seconds=flat_overrides.get("total_timeout_seconds", base_policy.total_timeout_seconds),
        log_all_attempts=flat_overrides.get("log_all_attempts", base_policy.log_all_attempts),
        require_audit_trail=flat_overrides.get("require_audit_trail", base_policy.require_audit_trail),
    )


def detect_context() -> str:
    """
    Auto-detect the current context based on environment.

    Checks environment variables and other signals to determine
    the appropriate policy context.

    Returns:
        Policy context name
    """
    import os

    # Check environment variables
    env = os.environ.get("ENV", "").lower()
    node_env = os.environ.get("NODE_ENV", "").lower()
    python_env = os.environ.get("PYTHON_ENV", "").lower()

    for env_val in [env, node_env, python_env]:
        if env_val in AUTONOMY_POLICIES:
            return env_val

    # Check for CI/CD
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        return "testing"

    # Check for common production indicators
    if any(x in [env, node_env, python_env] for x in ["prod", "prd", "live"]):
        return "production"

    # Default to development
    return "development"
