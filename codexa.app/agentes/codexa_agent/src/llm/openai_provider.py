"""
OpenAI Provider (GPT)
Implements LLM provider interface for OpenAI GPT models.
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


class OpenAIProvider(LLMProvider):
    """OpenAI GPT LLM provider."""

    # Pricing per 1M tokens (input, output)
    PRICING = {
        "gpt-4": (30.00, 60.00),
        "gpt-4-turbo": (10.00, 30.00),
        "gpt-5": (5.00, 15.00),  # Estimated
        "gpt-4-code": (10.00, 30.00),
    }

    def __init__(self, config: LLMConfig):
        """Initialize OpenAI provider."""
        super().__init__(config)

        # Import openai only when needed
        try:
            import openai
            self.openai = openai
            self.client = openai.AsyncOpenAI(
                api_key=config.api_key or self._get_api_key_from_env()
            )
        except ImportError:
            raise LLMError(
                "openai package not installed. "
                "Install with: pip install openai"
            )

    def _get_api_key_from_env(self) -> str:
        """Get API key from environment."""
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMAuthenticationError(
                "OPENAI_API_KEY not found in environment"
            )
        return api_key

    async def complete(
        self,
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]] = None,
        system: Optional[str] = None
    ) -> LLMResponse:
        """
        Get completion from OpenAI.

        Args:
            messages: List of chat messages
            tools: Optional list of tool definitions
            system: Optional system prompt

        Returns:
            LLM response
        """
        start_time = time.time()

        # Convert messages to OpenAI format
        openai_messages = []

        if system:
            openai_messages.append({"role": "system", "content": system})

        for msg in messages:
            openai_messages.append({"role": msg.role, "content": msg.content})

        # Prepare request parameters
        request_params = {
            "model": self.config.model.value,
            "messages": openai_messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
        }

        if tools:
            # Convert tools to OpenAI format
            request_params["tools"] = [
                {
                    "type": "function",
                    "function": tool
                }
                for tool in tools
            ]
            request_params["tool_choice"] = "auto"

        # Execute with retry logic
        for attempt in range(self.config.retry_attempts):
            try:
                # Call OpenAI API
                response = await self.client.chat.completions.create(**request_params)

                # Calculate latency
                latency_ms = (time.time() - start_time) * 1000

                # Parse response
                message = response.choices[0].message
                content = message.content or ""

                # Parse tool calls if any
                tool_calls = []
                if message.tool_calls:
                    for tc in message.tool_calls:
                        import json
                        tool_calls.append(ToolCall(
                            tool_name=tc.function.name,
                            arguments=json.loads(tc.function.arguments),
                            id=tc.id
                        ))

                # Get token usage
                tokens_input = response.usage.prompt_tokens
                tokens_output = response.usage.completion_tokens
                tokens_total = response.usage.total_tokens

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
                    provider="openai",
                    tool_calls=tool_calls,
                    tokens_used=tokens_total,
                    tokens_input=tokens_input,
                    tokens_output=tokens_output,
                    cost_usd=cost,
                    latency_ms=latency_ms,
                    metadata={
                        "finish_reason": response.choices[0].finish_reason,
                        "response_id": response.id,
                    }
                )

                # Update stats
                self.update_stats(llm_response)

                logger.info(
                    f"OpenAI call successful: {tokens_total} tokens, "
                    f"${cost:.4f}, {latency_ms:.0f}ms"
                )

                return llm_response

            except self.openai.RateLimitError as e:
                if attempt < self.config.retry_attempts - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Rate limit hit, retrying in {delay}s (attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)
                else:
                    raise LLMRateLimitError(f"Rate limit exceeded: {e}")

            except self.openai.APITimeoutError as e:
                if attempt < self.config.retry_attempts - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Timeout, retrying in {delay}s (attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)
                else:
                    raise LLMTimeoutError(f"Request timed out: {e}")

            except self.openai.AuthenticationError as e:
                raise LLMAuthenticationError(f"Authentication failed: {e}")

            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                raise LLMError(f"OpenAI API call failed: {e}")

        raise LLMError("Max retry attempts exceeded")

    def get_cost_per_token(self, model: str) -> tuple[float, float]:
        """Get cost per token for OpenAI model."""
        return self.PRICING.get(model, (10.00, 30.00))  # Default to GPT-4 Turbo pricing

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "openai"
