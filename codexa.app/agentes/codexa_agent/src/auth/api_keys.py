"""
API Key Manager
Manages API keys for LLM providers.
"""

import os
from pathlib import Path
from typing import Optional, Dict
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class APIKeyError(Exception):
    """API key related errors."""
    pass


class APIKeyManager:
    """
    Manages API keys for different LLM providers.

    Features:
    - Load from environment variables
    - Load from .env file
    - Validate key presence
    - Support multiple providers
    """

    # Environment variable names for each provider
    KEY_ENV_VARS = {
        "claude": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "gemini": "GOOGLE_API_KEY",
    }

    def __init__(self, env_file: Optional[Path] = None, auto_load: bool = True):
        """
        Initialize API key manager.

        Args:
            env_file: Optional path to .env file
            auto_load: Automatically load from environment (default: True)
        """
        self.env_file = env_file
        self.keys: Dict[str, str] = {}

        if auto_load:
            self.load_from_env(env_file)

        logger.info("Initialized API key manager")

    def load_from_env(self, env_file: Optional[Path] = None):
        """
        Load API keys from environment variables.

        Args:
            env_file: Optional .env file path
        """
        # Load .env file if specified
        if env_file and env_file.exists():
            load_dotenv(env_file)
            logger.info(f"Loaded environment from: {env_file}")
        else:
            # Try to find .env in current directory or parents
            current = Path.cwd()
            while current != current.parent:
                env_path = current / ".env"
                if env_path.exists():
                    load_dotenv(env_path)
                    logger.info(f"Loaded environment from: {env_path}")
                    break
                current = current.parent

        # Load keys from environment
        for provider, env_var in self.KEY_ENV_VARS.items():
            key = os.getenv(env_var)
            if key:
                self.keys[provider] = key
                logger.info(f"Loaded API key for: {provider}")
            else:
                logger.debug(f"No API key found for: {provider} ({env_var})")

    def get_key(self, provider: str) -> str:
        """
        Get API key for a provider.

        Args:
            provider: Provider name (claude, openai, gemini)

        Returns:
            API key

        Raises:
            APIKeyError: If key not found
        """
        provider = provider.lower()

        if provider not in self.keys:
            env_var = self.KEY_ENV_VARS.get(provider, f"{provider.upper()}_API_KEY")
            raise APIKeyError(
                f"API key not found for provider: {provider}. "
                f"Set {env_var} environment variable."
            )

        return self.keys[provider]

    def has_key(self, provider: str) -> bool:
        """
        Check if API key exists for provider.

        Args:
            provider: Provider name

        Returns:
            True if key exists
        """
        return provider.lower() in self.keys

    def set_key(self, provider: str, key: str):
        """
        Manually set API key for a provider.

        Args:
            provider: Provider name
            key: API key
        """
        provider = provider.lower()
        self.keys[provider] = key
        logger.info(f"Set API key for: {provider}")

    def list_providers(self) -> list:
        """
        List providers with loaded keys.

        Returns:
            List of provider names
        """
        return list(self.keys.keys())

    def validate_keys(self, required_providers: Optional[list] = None):
        """
        Validate that required API keys are present.

        Args:
            required_providers: List of required providers (default: all)

        Raises:
            APIKeyError: If required keys are missing
        """
        providers_to_check = required_providers or list(self.KEY_ENV_VARS.keys())

        missing = []
        for provider in providers_to_check:
            if not self.has_key(provider):
                missing.append(provider)

        if missing:
            raise APIKeyError(
                f"Missing API keys for: {', '.join(missing)}. "
                f"Set the following environment variables: "
                f"{', '.join(self.KEY_ENV_VARS[p] for p in missing)}"
            )

        logger.info(f"Validated API keys for: {', '.join(providers_to_check)}")

    def get_masked_key(self, provider: str) -> str:
        """
        Get masked version of API key for logging.

        Args:
            provider: Provider name

        Returns:
            Masked key (shows only first/last 4 chars)
        """
        try:
            key = self.get_key(provider)
            if len(key) <= 8:
                return "***"
            return f"{key[:4]}...{key[-4:]}"
        except APIKeyError:
            return "[NOT SET]"

    def __repr__(self) -> str:
        """String representation."""
        providers = ", ".join(
            f"{p}: {self.get_masked_key(p)}"
            for p in self.KEY_ENV_VARS.keys()
        )
        return f"APIKeyManager({providers})"


# Utility functions

def get_default_key_manager() -> APIKeyManager:
    """
    Get default API key manager instance.

    Returns:
        Configured APIKeyManager
    """
    return APIKeyManager(auto_load=True)


def validate_provider_key(provider: str) -> str:
    """
    Validate and get API key for a provider.

    Args:
        provider: Provider name

    Returns:
        API key

    Raises:
        APIKeyError: If key not found
    """
    manager = get_default_key_manager()
    return manager.get_key(provider)
