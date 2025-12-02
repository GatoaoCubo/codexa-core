"""
Gemini Provider (Google)
Implements LLM provider interface for Google Gemini models.
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


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""

    # Pricing per 1M tokens (input, output)
    PRICING = {
        "gemini-1.5-pro": (1.25, 5.00),
        "gemini-2.0": (0.50, 2.00),  # Estimated
        "gemini-cli-3": (0.50, 2.00),  # Estimated
    }

    def __init__(self, config: LLMConfig):
        """Initialize Gemini provider."""
        super().__init__(config)

        # Import google.generativeai only when needed
        try:
            import google.generativeai as genai
            self.genai = genai
            genai.configure(api_key=config.api_key or self._get_api_key_from_env())

            # Initialize model
            self.model = genai.GenerativeModel(self.config.model.value)
        except ImportError:
            raise LLMError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai"
            )

    def _get_api_key_from_env(self) -> str:
        """Get API key from environment."""
        import os
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise LLMAuthenticationError(
                "GOOGLE_API_KEY or GEMINI_API_KEY not found in environment"
            )
        return api_key

    async def complete(
        self,
        messages: List[Message],
        tools: Optional[List[Dict[str, Any]]] = None,
        system: Optional[str] = None
    ) -> LLMResponse:
        """
        Get completion from Gemini.

        Args:
            messages: List of chat messages
            tools: Optional list of tool definitions
            system: Optional system prompt

        Returns:
            LLM response
        """
        start_time = time.time()

        # Convert messages to Gemini format
        # Gemini uses a simpler format: just content strings
        conversation = []
        if system:
            conversation.append({"role": "user", "parts": [system]})
            conversation.append({"role": "model", "parts": ["Understood."]})

        for msg in messages:
            # Gemini uses "model" instead of "assistant"
            role = "model" if msg.role == "assistant" else msg.role
            conversation.append({"role": role, "parts": [msg.content]})

        # Prepare generation config
        generation_config = {
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "max_output_tokens": self.config.max_tokens,
        }

        # Execute with retry logic
        for attempt in range(self.config.retry_attempts):
            try:
                # Call Gemini API
                if tools:
                    # TODO: Implement tool calling for Gemini
                    # Gemini has function calling but different format
                    logger.warning("Tool calling not yet implemented for Gemini")

                response = await asyncio.to_thread(
                    self.model.generate_content,
                    conversation,
                    generation_config=generation_config
                )

                # Calculate latency
                latency_ms = (time.time() - start_time) * 1000

                # Parse response
                content = response.text

                # Get token usage (if available)
                tokens_input = 0
                tokens_output = 0
                try:
                    if hasattr(response, 'usage_metadata'):
                        tokens_input = response.usage_metadata.prompt_token_count
                        tokens_output = response.usage_metadata.candidates_token_count
                except:
                    # Estimate tokens if not provided
                    tokens_input = len(str(conversation)) // 4
                    tokens_output = len(content) // 4

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
                    provider="gemini",
                    tool_calls=[],  # TODO: Parse tool calls when implemented
                    tokens_used=tokens_total,
                    tokens_input=tokens_input,
                    tokens_output=tokens_output,
                    cost_usd=cost,
                    latency_ms=latency_ms,
                    metadata={
                        "finish_reason": str(response.candidates[0].finish_reason) if response.candidates else None,
                    }
                )

                # Update stats
                self.update_stats(llm_response)

                logger.info(
                    f"Gemini call successful: {tokens_total} tokens, "
                    f"${cost:.4f}, {latency_ms:.0f}ms"
                )

                return llm_response

            except Exception as e:
                error_str = str(e).lower()

                # Handle rate limiting
                if "rate" in error_str or "quota" in error_str:
                    if attempt < self.config.retry_attempts - 1:
                        delay = self.config.retry_delay * (2 ** attempt)
                        logger.warning(
                            f"Rate limit hit, retrying in {delay}s (attempt {attempt + 1})"
                        )
                        await asyncio.sleep(delay)
                    else:
                        raise LLMRateLimitError(f"Rate limit exceeded: {e}")

                # Handle timeout
                elif "timeout" in error_str:
                    if attempt < self.config.retry_attempts - 1:
                        delay = self.config.retry_delay * (2 ** attempt)
                        logger.warning(
                            f"Timeout, retrying in {delay}s (attempt {attempt + 1})"
                        )
                        await asyncio.sleep(delay)
                    else:
                        raise LLMTimeoutError(f"Request timed out: {e}")

                # Handle authentication
                elif "auth" in error_str or "api key" in error_str:
                    raise LLMAuthenticationError(f"Authentication failed: {e}")

                else:
                    logger.error(f"Gemini API error: {e}")
                    raise LLMError(f"Gemini API call failed: {e}")

        raise LLMError("Max retry attempts exceeded")

    def get_cost_per_token(self, model: str) -> tuple[float, float]:
        """Get cost per token for Gemini model."""
        return self.PRICING.get(model, (1.25, 5.00))  # Default to 1.5 Pro pricing

    def get_provider_name(self) -> str:
        """Get provider name."""
        return "gemini"
