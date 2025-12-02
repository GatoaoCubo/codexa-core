"""
Abstract LLM Provider Interface
Defines the contract that all LLM providers must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class ModelType(Enum):
    """Available model types across providers."""
    # Claude models
    CLAUDE_OPUS = "claude-opus-4-20250514"
    CLAUDE_SONNET = "claude-sonnet-4-5-20250929"
    CLAUDE_HAIKU = "claude-haiku-4-20250312"

    # OpenAI models
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_5 = "gpt-5"
    GPT_CODEX = "gpt-4-code"

    # Gemini models
    GEMINI_15_PRO = "gemini-1.5-pro"
    GEMINI_20 = "gemini-2.0"
    GEMINI_CLI_3 = "gemini-cli-3"


@dataclass
class LLMConfig:
    """Configuration for LLM provider."""
    model: ModelType
    temperature: float = 1.0
    max_tokens: int = 4096
    top_p: float = 1.0
    api_key: Optional[str] = None
    timeout: int = 120  # seconds
    retry_attempts: int = 3
    retry_delay: float = 1.0  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """Chat message."""
    role: str  # "user", "assistant", "system"
    content: str


@dataclass
class ToolCall:
    """Represents a tool call from LLM."""
    tool_name: str
    arguments: Dict[str, Any]
    id: Optional[str] = None


@dataclass
class LLMResponse:
    """Response from LLM provider."""
    content: str
    model: str
    provider: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    tokens_used: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_tool_calls(self) -> bool:
        """Check if response contains tool calls."""
        return len(self.tool_calls) > 0


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All LLM providers (Claude, OpenAI, Gemini) must implement this interface.
    """

    def __init__(self, config: LLMConfig):
        """
        Initialize provider with configuration.

        Args:
            config: LLM configuration
        """
        self.config = config
        self.call_count = 0
        self.total_tokens = 0
        self.total_cost = 0.0

    @abstractmethod
    async def complete(
        self,
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]] = None,
        system: Optional[str] = None
    ) -> LLMResponse:
        """
        Get completion from LLM.

        Args:
            messages: List of chat messages
            tools: Optional list of tool definitions
            system: Optional system prompt

        Returns:
            LLM response

        Raises:
            LLMError: If LLM call fails
        """
        pass

    @abstractmethod
    def get_cost_per_token(self, model: str) -> tuple[float, float]:
        """
        Get cost per token for model.

        Args:
            model: Model name

        Returns:
            Tuple of (input_cost_per_1m, output_cost_per_1m)
        """
        pass

    def calculate_cost(self, tokens_input: int, tokens_output: int, model: str) -> float:
        """
        Calculate cost of API call.

        Args:
            tokens_input: Input tokens
            tokens_output: Output tokens
            model: Model name

        Returns:
            Cost in USD
        """
        input_cost, output_cost = self.get_cost_per_token(model)

        cost = (
            (tokens_input / 1_000_000) * input_cost +
            (tokens_output / 1_000_000) * output_cost
        )

        return cost

    def update_stats(self, response: LLMResponse):
        """Update provider statistics."""
        self.call_count += 1
        self.total_tokens += response.tokens_used
        self.total_cost += response.cost_usd

    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics."""
        return {
            "call_count": self.call_count,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "avg_tokens_per_call": self.total_tokens / self.call_count if self.call_count > 0 else 0,
            "avg_cost_per_call": self.total_cost / self.call_count if self.call_count > 0 else 0,
        }

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name (e.g., 'claude', 'openai', 'gemini')."""
        pass


class LLMError(Exception):
    """Base exception for LLM errors."""
    pass


class LLMTimeoutError(LLMError):
    """LLM call timed out."""
    pass


class LLMRateLimitError(LLMError):
    """Rate limit exceeded."""
    pass


class LLMAuthenticationError(LLMError):
    """Authentication failed."""
    pass


class LLMInvalidRequestError(LLMError):
    """Invalid request to LLM."""
    pass
