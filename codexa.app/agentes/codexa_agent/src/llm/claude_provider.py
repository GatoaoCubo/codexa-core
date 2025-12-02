"""
Claude Provider (Anthropic)
Implements LLM provider interface for Anthropic Claude models.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
import logging

from .provider import (
    LLMProvider,
    LLMConfig,
    LLMResponse,
    Message,
    ToolCall,
    LLMError,
    LLMTimeoutError,
    LLMRateLimitError,
    LLMAuthenticationError,
)

logger = logging.getLogger(__name__)


class ClaudeProvider(LLMProvider):
    """Anthropic Claude LLM provider."""

    # Pricing per 1M tokens (input, output)
    PRICING = {
        "claude-opus-4-20250514": (15.00, 75.00),
        "claude-sonnet-4-5-20250929": (3.00, 15.00),
        "claude-haiku-4-20250312": (0.25, 1.25),
    }

    def __init__(self, config: LLMConfig):
        """Initialize Claude provider."""
        super().__init__(config)

        # Import anthropic only when needed
        try:
            import anthropic
            self.anthropic = anthropic
            self.client = anthropic.Anthropic(
                api_key=config.api_key or self._get_api_key_from_env()
            )
        except ImportError:
            raise LLMError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )

    def _get_api_key_from_env(self) -> str:
        """Get API key from environment."""
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise LLMAuthenticationError(
                "ANTHROPIC_API_KEY not found in environment"
            )
        return api_key

    async def complete(
        self,
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]] = None,
        system: Optional[str] = None
    ) -> LLMResponse:
        """
        Get completion from Claude.

        Args:
            messages: List of chat messages
            tools: Optional list of tool definitions
            system: Optional system prompt

        Returns:
            LLM response
        """
        start_time = time.time()

        # Convert messages to Claude format
        claude_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        # Prepare request parameters
        request_params = {
            "model": self.config.model.value,
            "messages": claude_messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
        }

        if system:
            request_params["system"] = system

        if tools:
            request_params["tools"] = tools

        # Execute with retry logic
        for attempt in range(self.config.retry_attempts):
            try:
                # Call Claude API
                response = await asyncio.to_thread(
                    self.client.messages.create,
                    **request_params
                )

                # Calculate latency
                latency_ms = (time.time() - start_time) * 1000

                # Parse tool calls if any
                tool_calls = []
                content = ""

                for block in response.content:
                    if block.type == "text":
                        content += block.text
                    elif block.type == "tool_use":
                        tool_calls.append(ToolCall(
                            tool_name=block.name,
                            arguments=block.input,
                            id=block.id
                        ))

                # Get token usage
                tokens_input = response.usage.input_tokens
                tokens_output = response.usage.output_tokens
                tokens_total = tokens_input + tokens_output

                # Calculate cost
                cost = self.calculate_cost(
                    tokens_input,
                    tokens_output,
                    self.config.model.value
                )

                # Create response
                llm_response = LLMResponse(
                    content=content,
                    model=self.config.model.value,
                    provider="claude",
                    tool_calls=tool_calls,
                    tokens_used=tokens_total,
                    tokens_input=tokens_input,
                    tokens_output=tokens_output,
                    cost_usd=cost,
                    latency_ms=latency_ms,
                    metadata={
                        "stop_reason": response.stop_reason,
                        "response_id": response.id,
                    }
                )

                # Update stats
                self.update_stats(llm_response)

                logger.info(
                    f"Claude call successful: {tokens_total} tokens, "
                    f"${cost:.4f}, {latency_ms:.0f}ms"
                )

                return llm_response

            except self.anthropic.RateLimitError as e:
                if attempt < self.config.retry_attempts - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Rate limit hit, retrying in {delay}s (attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)
                else:
                    raise LLMRateLimitError(f"Rate limit exceeded: {e}")

            except self.anthropic.APITimeoutError as e:
                if attempt < self.config.retry_attempts - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Timeout, retrying in {delay}s (attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)
                else:
                    raise LLMTimeoutError(f"Request timed out: {e}")

            except self.anthropic.AuthenticationError as e:
                raise LLMAuthenticationError(f"Authentication failed: {e}")

            except Exception as e:
                logger.error(f"Claude API error: {e}")
                raise LLMError(f"Claude API call failed: {e}")

        raise LLMError("Max retry attempts exceeded")

    def get_cost_per_token(self, model: str) -> tuple[float, float]:
        """Get cost per token for Claude model."""
        return self.PRICING.get(model, (3.00, 15.00))  # Default to Sonnet pricing

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "claude"
