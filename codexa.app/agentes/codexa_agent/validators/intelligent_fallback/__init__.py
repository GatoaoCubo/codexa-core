"""
Intelligent Fallback System
============================

A sophisticated fallback system that enables refined autonomy for AI agents.
Instead of binary pass/fail, this system provides a cascade of fallback
actions that allow agents to attempt self-correction before escalating.

## Core Concepts

1. **Cascading Actions**: 6 levels from fully autonomous to full escalation
2. **Policy-Driven**: Different autonomy levels for different contexts
3. **Learning**: Historical tracking to improve strategy selection
4. **Human-in-the-Loop**: Smart escalation when confidence is low

## Quick Start

```python
from validators.intelligent_fallback import (
    IntelligentFallbackOrchestrator,
    FallbackAction,
    FallbackMixin
)

# Option 1: Direct orchestrator usage
orchestrator = IntelligentFallbackOrchestrator(policy="development")
result = orchestrator.handle(gradient_report=my_report)

if result.should_retry:
    # Apply correction/variation and retry
    pass
elif result.needs_human:
    # Show questions to user
    pass
else:
    # Proceed with result
    pass

# Option 2: Mixin for validators
class MyValidator(ValueFunctionMixin, FallbackMixin):
    def validate_with_fallback(self, target):
        return self.run_with_fallback(
            lambda: self.validate(target),
            policy="development"
        )
```

## Policies

- `development`: Permissive, allows experimentation
- `staging`: Balanced approach
- `production`: Conservative, escalates quickly
- `research`: Maximum autonomy
- `testing`: Optimized for test execution

## Version History

- 1.0.0 (2025-11-29): Initial implementation
"""

__version__ = "1.0.0"

# Core actions and results
from .actions import (
    FallbackAction,
    FallbackResult,
    EscalationReason,
    EscalationQuestion,
    CorrectionResult,
)

# Strategies
from .strategies import (
    AutoCorrectStrategy,
    VariationStrategy,
    StrategyType,
    RiskLevel,
    AUTO_CORRECT_STRATEGIES,
    VARIATION_STRATEGIES,
    get_auto_correct_strategy,
    get_applicable_variations,
    get_strategy_by_name,
    get_variation_by_name,
    filter_strategies_by_risk,
    filter_strategies_by_context,
)

# Policies
from .policies import (
    AutonomyPolicy,
    PolicyContext,
    AUTONOMY_POLICIES,
    get_policy,
    create_custom_policy,
    detect_context,
)

# History and learning
from .history import (
    FallbackHistory,
    FallbackAttempt,
    StrategyStats,
)

# Main orchestrator
from .orchestrator import (
    IntelligentFallbackOrchestrator,
    OrchestratorState,
    FallbackMixin,
)


__all__ = [
    # Version
    "__version__",
    # Actions
    "FallbackAction",
    "FallbackResult",
    "EscalationReason",
    "EscalationQuestion",
    "CorrectionResult",
    # Strategies
    "AutoCorrectStrategy",
    "VariationStrategy",
    "StrategyType",
    "RiskLevel",
    "AUTO_CORRECT_STRATEGIES",
    "VARIATION_STRATEGIES",
    "get_auto_correct_strategy",
    "get_applicable_variations",
    "get_strategy_by_name",
    "get_variation_by_name",
    "filter_strategies_by_risk",
    "filter_strategies_by_context",
    # Policies
    "AutonomyPolicy",
    "PolicyContext",
    "AUTONOMY_POLICIES",
    "get_policy",
    "create_custom_policy",
    "detect_context",
    # History
    "FallbackHistory",
    "FallbackAttempt",
    "StrategyStats",
    # Orchestrator
    "IntelligentFallbackOrchestrator",
    "OrchestratorState",
    "FallbackMixin",
]
