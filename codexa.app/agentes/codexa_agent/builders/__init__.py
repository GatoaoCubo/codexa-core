"""
CODEXA Builders
===============

Construction tools for agents, prompts, commands, and workflows.

Available Builders:
    - agent_meta_constructor: 5-phase agent construction
    - prompt_generator: HOP generation (TAC-7)
    - command_generator: Slash commands
    - doc_sync_builder: Documentation sync

Usage:
    # CLI
    uv run builders/02_agent_meta_constructor.py "Agent description"

    # Python
    from builders.task_boundary import TaskBoundary
    from builders.multi_agent_orchestrator import MultiAgentOrchestrator
"""

__version__ = "2.0.0"

# Import shared modules
from .task_boundary import (
    TaskBoundary,
    TaskBoundaryBuilder,
    Task,
    TaskProgress,
    AgentMode,
    TaskStatus,
)

from .multi_agent_orchestrator import (
    MultiAgentOrchestrator,
    OrchestrationBuilder,
    AgentDefinition,
    AgentExecution,
    OrchestrationPattern,
    AgentStatus,
)

__all__ = [
    # Task Boundary
    "TaskBoundary",
    "TaskBoundaryBuilder",
    "Task",
    "TaskProgress",
    "AgentMode",
    "TaskStatus",

    # Orchestration
    "MultiAgentOrchestrator",
    "OrchestrationBuilder",
    "AgentDefinition",
    "AgentExecution",
    "OrchestrationPattern",
    "AgentStatus",
]
