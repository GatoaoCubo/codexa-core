"""
CODEXA Agent Core - Unified Exports
====================================

This module provides unified access to all CODEXA core components.

Usage:
    from src import (
        # LLM Providers
        get_llm_provider,
        ProviderFactory,
        ModelType,

        # Tools
        ToolExecutor,
        FileTools,
        BashTools,

        # Runtime
        AgentRuntime,
        AgentConfig,

        # Auth
        get_rate_limiter,
        get_audit_logger,
        get_secrets_manager,
    )

Version: 3.1.0
"""

__version__ = "3.1.0"

# LLM Providers
from .llm import (
    LLMProvider,
    ModelType,
    LLMResponse,
    LLMConfig,
    ProviderFactory,
    ClaudeProvider,
    OpenAIProvider,
    GeminiProvider,
    CostTracker,
)

# Tool Execution
from .tools import (
    ToolExecutor,
    ToolResult,
    ToolError,
    ToolType,
    FileTools,
    BashTools,
    PermissionManager,
    Permission,
    PermissionLevel,
)

# Agent Runtime
from .runtime import (
    AgentRuntime,
    AgentConfig,
    AgentState,
    AgentStatus,
    PromptLoader,
    get_standard_composition,
    AGENT_COMPOSITIONS,
)

# Authentication & Security
from .auth import (
    # API Keys
    APIKeyManager,
    APIKeyError,
    get_default_key_manager,
    # Rate Limiting
    RateLimiter,
    RateLimitConfig,
    RateLimitExceeded,
    get_rate_limiter,
    check_rate_limit,
    # Audit Logging
    AuditLogger,
    AuditLogHandler,
    AuditEvent,
    AuditContext,
    AuditEventType,
    AuditSeverity,
    get_audit_logger,
    audit_log,
    # Secrets
    SecretsManager,
    SecretsError,
    get_secrets_manager,
    get_secret,
    require_secret,
)

__all__ = [
    # Version
    "__version__",

    # LLM
    "LLMProvider",
    "ModelType",
    "LLMResponse",
    "LLMConfig",
    "ProviderFactory",
    "ClaudeProvider",
    "OpenAIProvider",
    "GeminiProvider",
    "CostTracker",

    # Tools
    "ToolExecutor",
    "ToolResult",
    "ToolError",
    "ToolType",
    "FileTools",
    "BashTools",
    "PermissionManager",
    "Permission",
    "PermissionLevel",

    # Runtime
    "AgentRuntime",
    "AgentConfig",
    "AgentState",
    "AgentStatus",
    "PromptLoader",
    "get_standard_composition",
    "AGENT_COMPOSITIONS",

    # Auth - API Keys
    "APIKeyManager",
    "APIKeyError",
    "get_default_key_manager",

    # Auth - Rate Limiting
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitExceeded",
    "get_rate_limiter",
    "check_rate_limit",

    # Auth - Audit
    "AuditLogger",
    "AuditLogHandler",
    "AuditEvent",
    "AuditContext",
    "AuditEventType",
    "AuditSeverity",
    "get_audit_logger",
    "audit_log",

    # Auth - Secrets
    "SecretsManager",
    "SecretsError",
    "get_secrets_manager",
    "get_secret",
    "require_secret",
]


def get_version() -> str:
    """Get CODEXA core version."""
    return __version__


def create_agent(
    agent_id: str,
    system_prompt: str,
    provider: str = "claude",
    model: str = None,
) -> AgentRuntime:
    """
    Convenience function to create an agent quickly.

    Args:
        agent_id: Unique agent identifier
        system_prompt: System prompt for the agent
        provider: LLM provider (claude, openai, gemini)
        model: Model to use (optional, uses default)

    Returns:
        Configured AgentRuntime

    Example:
        agent = create_agent(
            "my_agent",
            "You are a helpful assistant.",
            provider="claude"
        )
        result = await agent.run("Hello!")
    """
    # Get model type
    if model:
        model_type = ModelType(model)
    else:
        model_type = {
            "claude": ModelType.CLAUDE_SONNET,
            "openai": ModelType.GPT4_TURBO,
            "gemini": ModelType.GEMINI_PRO,
        }.get(provider.lower(), ModelType.CLAUDE_SONNET)

    # Create provider
    llm_provider = ProviderFactory.create_provider(model=model_type)

    # Create tool executor with default permissions
    tool_executor = ToolExecutor()
    permission = Permission(
        agent_id=agent_id,
        level=PermissionLevel.STANDARD,
    )

    # Create config
    config = AgentConfig(
        agent_id=agent_id,
        system_prompt=system_prompt,
        llm_provider=llm_provider,
        tool_executor=tool_executor,
        permission=permission,
    )

    return AgentRuntime(config=config)
