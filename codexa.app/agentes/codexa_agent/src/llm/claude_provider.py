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
        "claude-3-opus-latest": (15.00, 75.00),
        "claude-sonnet-4-20250514": (3.00, 15.00),
        "claude-3-5-haiku-latest": (0.80, 4.00),
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
        system: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Get completion from Claude.

        Args:
            messages: List of chat messages (dict or Message objects)
            tools: Optional list of tool definitions
            system: Optional system prompt
            **kwargs: Optional overrides (temperature, top_p, max_tokens)

        Returns:
            LLM response
        """
        start_time = time.time()

        # Convert messages to Claude format (accept both dict and Message objects)
        claude_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg["role"]
                content = msg["content"]
                tool_calls = msg.get("tool_calls", [])
                tool_call_id = msg.get("tool_call_id")
            else:
                role = msg.role
                content = msg.content
                tool_calls = getattr(msg, 'tool_calls', []) or []
                tool_call_id = getattr(msg, 'tool_call_id', None)

            # Handle tool result messages (convert role "tool" to "user" with tool_result block)
            if role == "tool" and tool_call_id:
                claude_messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_call_id,
                            "content": content
                        }
                    ]
                })
            # Handle assistant messages with tool calls
            elif role == "assistant" and tool_calls:
                content_blocks = []
                if content:
                    content_blocks.append({"type": "text", "text": content})
                for tc in tool_calls:
                    tc_name = tc.tool_name if hasattr(tc, 'tool_name') else tc.get('tool_name', tc.get('name'))
                    tc_args = tc.arguments if hasattr(tc, 'arguments') else tc.get('arguments', {})
                    tc_id = tc.id if hasattr(tc, 'id') else tc.get('id')
                    content_blocks.append({
                        "type": "tool_use",
                        "id": tc_id,
                        "name": tc_name,
                        "input": tc_args
                    })
                claude_messages.append({"role": "assistant", "content": content_blocks})
            # Regular messages
            else:
                claude_messages.append({"role": role, "content": content})

        # Prepare request parameters (allow kwargs to override config)
        request_params = {
            "model": self.config.model.value,
            "messages": claude_messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", self.config.top_p),
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
