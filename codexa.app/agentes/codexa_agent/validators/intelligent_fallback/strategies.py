"""
Intelligent Fallback - Strategies Module
=========================================

Defines auto-correction and variation strategies that the fallback
system can use to attempt recovery before escalating to humans.

Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from enum import Enum


class StrategyType(Enum):
    """Type of strategy execution."""

    DETERMINISTIC = "deterministic"  # Script-based, predictable
    MODEL_BASED = "model"  # Uses LLM for inference
    HYBRID = "hybrid"  # Combination of both


class RiskLevel(Enum):
    """Risk level of applying a strategy."""

    LOW = "low"  # Safe to apply automatically
    MEDIUM = "medium"  # Apply with caution
    HIGH = "high"  # Requires confirmation


@dataclass
class AutoCorrectStrategy:
    """
    Strategy for automatically correcting a specific checkpoint issue.

    Each strategy is tied to a specific checkpoint type and defines
    how to attempt correction.
    """

    name: str
    description: str
    checkpoint_name: str
    action: str
    strategy_type: StrategyType
    risk_level: RiskLevel = RiskLevel.LOW
    reversible: bool = True
    max_attempts: int = 2
    requires_confirmation: bool = False
    applicable_contexts: List[str] = field(default_factory=lambda: ["all"])

    # Optional: conditions for when this strategy applies
    min_confidence: float = 0.0
    max_confidence: float = 0.7

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "checkpoint": self.checkpoint_name,
            "action": self.action,
            "type": self.strategy_type.value,
            "risk": self.risk_level.value,
            "reversible": self.reversible,
            "max_attempts": self.max_attempts,
            "requires_confirmation": self.requires_confirmation,
            "contexts": self.applicable_contexts,
            "confidence_range": [self.min_confidence, self.max_confidence]
        }


@dataclass
class VariationStrategy:
    """
    Strategy for retrying with a different approach when auto-correct
    is not applicable.
    """

    name: str
    description: str
    applies_to: List[str]  # Checkpoint types this applies to
    change_type: str  # What aspect is being changed
    change_params: Dict[str, Any] = field(default_factory=dict)
    success_rate_threshold: float = 0.3  # Skip if historical success < this
    cost_multiplier: float = 1.0  # Relative cost (for model upgrades)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "applies_to": self.applies_to,
            "change_type": self.change_type,
            "params": self.change_params,
            "success_threshold": self.success_rate_threshold,
            "cost": self.cost_multiplier
        }


# =============================================================================
# AUTO-CORRECT STRATEGIES REGISTRY
# =============================================================================

AUTO_CORRECT_STRATEGIES: Dict[str, AutoCorrectStrategy] = {
    # Type annotation coverage
    "add_type_hints": AutoCorrectStrategy(
        name="add_type_hints",
        description="Use LLM to infer and add type annotations to functions",
        checkpoint_name="type_coverage",
        action="infer_and_add_types",
        strategy_type=StrategyType.MODEL_BASED,
        risk_level=RiskLevel.LOW,
        reversible=True,
        max_attempts=2,
        min_confidence=0.3,
        max_confidence=0.7
    ),

    # Documentation coverage
    "generate_docstrings": AutoCorrectStrategy(
        name="generate_docstrings",
        description="Generate docstrings for undocumented functions",
        checkpoint_name="doc_coverage",
        action="generate_docstrings",
        strategy_type=StrategyType.MODEL_BASED,
        risk_level=RiskLevel.LOW,
        reversible=True,
        max_attempts=2,
        min_confidence=0.2,
        max_confidence=0.6
    ),

    # File structure issues
    "reorganize_files": AutoCorrectStrategy(
        name="reorganize_files",
        description="Move files to correct directories based on naming conventions",
        checkpoint_name="file_structure",
        action="reorganize_by_convention",
        strategy_type=StrategyType.DETERMINISTIC,
        risk_level=RiskLevel.MEDIUM,
        reversible=True,
        max_attempts=1,
        requires_confirmation=True  # Moving files is sensitive
    ),

    # Function complexity
    "suggest_refactor": AutoCorrectStrategy(
        name="suggest_refactor",
        description="Suggest refactoring for complex functions (does not auto-apply)",
        checkpoint_name="function_complexity",
        action="analyze_and_suggest",
        strategy_type=StrategyType.MODEL_BASED,
        risk_level=RiskLevel.HIGH,
        reversible=True,
        max_attempts=1,
        requires_confirmation=True  # Refactoring requires human review
    ),

    # Import organization
    "organize_imports": AutoCorrectStrategy(
        name="organize_imports",
        description="Sort and organize imports using isort-like rules",
        checkpoint_name="import_organization",
        action="sort_imports",
        strategy_type=StrategyType.DETERMINISTIC,
        risk_level=RiskLevel.LOW,
        reversible=True,
        max_attempts=1
    ),

    # Naming conventions
    "fix_naming": AutoCorrectStrategy(
        name="fix_naming",
        description="Rename variables/functions to match conventions",
        checkpoint_name="naming_conventions",
        action="rename_to_convention",
        strategy_type=StrategyType.DETERMINISTIC,
        risk_level=RiskLevel.MEDIUM,
        reversible=True,
        max_attempts=1,
        requires_confirmation=True  # Renaming can break references
    ),

    # Dead code
    "remove_dead_code": AutoCorrectStrategy(
        name="remove_dead_code",
        description="Remove unused imports and unreachable code",
        checkpoint_name="dead_code",
        action="remove_unused",
        strategy_type=StrategyType.DETERMINISTIC,
        risk_level=RiskLevel.MEDIUM,
        reversible=True,
        max_attempts=1
    ),

    # Security - NEVER auto-correct
    "security_review": AutoCorrectStrategy(
        name="security_review",
        description="Security issues always require human review",
        checkpoint_name="security_scan",
        action="escalate",
        strategy_type=StrategyType.DETERMINISTIC,
        risk_level=RiskLevel.HIGH,
        reversible=False,
        max_attempts=0,  # Never attempt auto-fix
        requires_confirmation=True
    ),
}


# =============================================================================
# VARIATION STRATEGIES REGISTRY
# =============================================================================

VARIATION_STRATEGIES: List[VariationStrategy] = [
    VariationStrategy(
        name="temperature_increase",
        description="Increase model temperature for more creative output",
        applies_to=["generation", "creative", "doc_coverage"],
        change_type="model_params",
        change_params={"temperature_delta": 0.2, "max_temperature": 1.0},
        success_rate_threshold=0.25,
        cost_multiplier=1.0
    ),

    VariationStrategy(
        name="temperature_decrease",
        description="Decrease temperature for more deterministic output",
        applies_to=["type_coverage", "accuracy", "consistency"],
        change_type="model_params",
        change_params={"temperature_delta": -0.2, "min_temperature": 0.0},
        success_rate_threshold=0.25,
        cost_multiplier=1.0
    ),

    VariationStrategy(
        name="prompt_expansion",
        description="Add more examples and context to the prompt",
        applies_to=["all"],
        change_type="prompt",
        change_params={"action": "append_examples", "max_examples": 3},
        success_rate_threshold=0.3,
        cost_multiplier=1.2  # More tokens
    ),

    VariationStrategy(
        name="prompt_simplification",
        description="Simplify the prompt, remove unnecessary constraints",
        applies_to=["all"],
        change_type="prompt",
        change_params={"action": "simplify", "keep_core": True},
        success_rate_threshold=0.2,
        cost_multiplier=0.8  # Fewer tokens
    ),

    VariationStrategy(
        name="model_upgrade",
        description="Use a more capable model",
        applies_to=["complex_reasoning", "function_complexity", "accuracy"],
        change_type="model",
        change_params={"upgrade_path": {"haiku": "sonnet", "sonnet": "opus"}},
        success_rate_threshold=0.4,
        cost_multiplier=3.0  # Significantly more expensive
    ),

    VariationStrategy(
        name="decomposition",
        description="Break the task into smaller sub-tasks",
        applies_to=["large_tasks", "function_complexity"],
        change_type="approach",
        change_params={"strategy": "divide_and_conquer", "max_subtasks": 5},
        success_rate_threshold=0.35,
        cost_multiplier=2.0  # Multiple calls
    ),

    VariationStrategy(
        name="different_approach",
        description="Try a completely different algorithm/approach",
        applies_to=["all"],
        change_type="approach",
        change_params={"strategy": "alternative_method"},
        success_rate_threshold=0.2,
        cost_multiplier=1.5
    ),

    VariationStrategy(
        name="add_constraints",
        description="Add more constraints to focus the output",
        applies_to=["consistency", "format", "structure"],
        change_type="prompt",
        change_params={"action": "add_constraints", "constraint_type": "format"},
        success_rate_threshold=0.3,
        cost_multiplier=1.1
    ),
]


# =============================================================================
# STRATEGY SELECTION HELPERS
# =============================================================================

def get_auto_correct_strategy(checkpoint_name: str) -> Optional[AutoCorrectStrategy]:
    """Get the auto-correct strategy for a specific checkpoint."""
    for strategy in AUTO_CORRECT_STRATEGIES.values():
        if strategy.checkpoint_name == checkpoint_name:
            return strategy
    return None


def get_applicable_variations(
    checkpoint_name: str,
    context: str = "all"
) -> List[VariationStrategy]:
    """Get all variation strategies applicable to a checkpoint."""
    applicable = []
    for strategy in VARIATION_STRATEGIES:
        if "all" in strategy.applies_to or checkpoint_name in strategy.applies_to:
            applicable.append(strategy)
    return applicable


def get_strategy_by_name(name: str) -> Optional[AutoCorrectStrategy]:
    """Get a specific auto-correct strategy by name."""
    return AUTO_CORRECT_STRATEGIES.get(name)


def get_variation_by_name(name: str) -> Optional[VariationStrategy]:
    """Get a specific variation strategy by name."""
    for strategy in VARIATION_STRATEGIES:
        if strategy.name == name:
            return strategy
    return None


def filter_strategies_by_risk(
    max_risk: RiskLevel
) -> List[AutoCorrectStrategy]:
    """Get all strategies up to a certain risk level."""
    risk_order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]
    max_index = risk_order.index(max_risk)

    return [
        s for s in AUTO_CORRECT_STRATEGIES.values()
        if risk_order.index(s.risk_level) <= max_index
    ]


def filter_strategies_by_context(
    context: str
) -> List[AutoCorrectStrategy]:
    """Get all strategies applicable to a specific context."""
    return [
        s for s in AUTO_CORRECT_STRATEGIES.values()
        if "all" in s.applicable_contexts or context in s.applicable_contexts
    ]
