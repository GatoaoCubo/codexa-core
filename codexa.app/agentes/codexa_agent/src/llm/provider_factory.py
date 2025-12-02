"""
Provider Factory
Creates LLM providers based on configuration.
"""

from typing import Optional
import logging

from .provider import LLMProvider, LLMConfig, ModelType
from .claude_provider import ClaudeProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider

logger = logging.getLogger(__name__)


class ProviderFactory:
    """Factory for creating LLM providers."""

    @staticmethod
    def create_provider(
        model: ModelType,
        api_key: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        """
        Create LLM provider based on model type.

        Args:
            model: Model type
            api_key: Optional API key (will use env var if not provided)
            **kwargs: Additional configuration parameters

        Returns:
            LLM provider instance

        Raises:
            ValueError: If model type is not supported
        """
        # Create config
        config = LLMConfig(
            model=model,
            api_key=api_key,
            **kwargs
        )

        # Determine provider from model type
        model_name = model.value

        if model_name.startswith("claude"):
            logger.info(f"Creating Claude provider for model: {model_name}")
            return ClaudeProvider(config)

        elif model_name.startswith("gpt"):
            logger.info(f"Creating OpenAI provider for model: {model_name}")
            return OpenAIProvider(config)

        elif model_name.startswith("gemini"):
            logger.info(f"Creating Gemini provider for model: {model_name}")
            return GeminiProvider(config)

        else:
            raise ValueError(f"Unsupported model type: {model_name}")

    @staticmethod
    def create_provider_by_name(
        provider_name: str,
        model_name: str,
        api_key: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        """
        Create provider by provider name and model name.

        Args:
            provider_name: Provider name ("claude", "openai", "gemini")
            model_name: Model name string
            api_key: Optional API key
            **kwargs: Additional configuration

        Returns:
            LLM provider instance
        """
        # Find matching ModelType
        for model_type in ModelType:
            if model_type.value == model_name:
                return ProviderFactory.create_provider(
                    model=model_type,
                    api_key=api_key,
                    **kwargs
                )

        raise ValueError(f"Unknown model: {model_name}")

    @staticmethod
    def get_default_provider(api_key: Optional[str] = None) -> LLMProvider:
        """
        Get default provider (Claude Sonnet 4).

        Args:
            api_key: Optional API key

        Returns:
            Default LLM provider
        """
        return ProviderFactory.create_provider(
            model=ModelType.CLAUDE_SONNET,
            api_key=api_key
        )

    @staticmethod
    def get_fast_provider(api_key: Optional[str] = None) -> LLMProvider:
        """
        Get fast/cheap provider (Claude Haiku).

        Args:
            api_key: Optional API key

        Returns:
            Fast LLM provider
        """
        return ProviderFactory.create_provider(
            model=ModelType.CLAUDE_HAIKU,
            api_key=api_key
        )

    @staticmethod
    def get_smart_provider(api_key: Optional[str] = None) -> LLMProvider:
        """
        Get smartest provider (Claude Opus).

        Args:
            api_key: Optional API key

        Returns:
            Smart LLM provider
        """
        return ProviderFactory.create_provider(
            model=ModelType.CLAUDE_OPUS,
            api_key=api_key
        )
