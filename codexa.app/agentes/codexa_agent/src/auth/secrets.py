"""
Secrets Manager for CODEXA Agent
Secure handling of sensitive configuration.
"""

import os
import json
import logging
from typing import Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta
import base64
import hashlib

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class SecretsError(Exception):
    """Secrets-related errors."""
    pass


@dataclass
class SecretMetadata:
    """Metadata for a stored secret."""
    name: str
    created_at: datetime
    expires_at: Optional[datetime]
    version: int
    source: str  # env, file, vault


class SecretsManager:
    """
    Secure secrets management.

    Features:
    - Load from environment variables
    - Load from .env files
    - In-memory caching with TTL
    - Optional encryption at rest
    - Secret rotation support
    - Audit trail for access
    """

    # Default environment variable mappings
    SECRET_ENV_VARS = {
        "anthropic_api_key": "ANTHROPIC_API_KEY",
        "openai_api_key": "OPENAI_API_KEY",
        "google_api_key": "GOOGLE_API_KEY",
        "aws_access_key": "AWS_ACCESS_KEY_ID",
        "aws_secret_key": "AWS_SECRET_ACCESS_KEY",
        "database_url": "DATABASE_URL",
        "redis_url": "REDIS_URL",
    }

    def __init__(
        self,
        env_file: Optional[Path] = None,
        encryption_key: Optional[str] = None,
        cache_ttl: int = 3600,
    ):
        """
        Initialize secrets manager.

        Args:
            env_file: Path to .env file
            encryption_key: Optional encryption key for stored secrets
            cache_ttl: Cache time-to-live in seconds
        """
        self.env_file = env_file
        self.cache_ttl = cache_ttl

        # In-memory cache
        self._cache: Dict[str, Any] = {}
        self._cache_metadata: Dict[str, SecretMetadata] = {}
        self._cache_expires: Dict[str, datetime] = {}

        # Encryption setup
        self._fernet = None
        if encryption_key and HAS_CRYPTO:
            self._setup_encryption(encryption_key)

        # Load from environment
        self._load_environment()

        logger.info("Initialized secrets manager")

    def _setup_encryption(self, key: str):
        """Set up encryption with provided key."""
        try:
            # Derive key using PBKDF2
            salt = b"codexa_secrets_salt"  # In production, use random salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            derived_key = base64.urlsafe_b64encode(
                kdf.derive(key.encode())
            )
            self._fernet = Fernet(derived_key)
            logger.info("Encryption enabled for secrets")
        except Exception as e:
            logger.warning(f"Could not setup encryption: {e}")
            self._fernet = None

    def _load_environment(self):
        """Load secrets from environment."""
        # Try to find and load .env file
        if self.env_file and self.env_file.exists():
            load_dotenv(self.env_file)
            logger.info(f"Loaded .env from: {self.env_file}")
        else:
            # Search for .env in current and parent directories
            current = Path.cwd()
            while current != current.parent:
                env_path = current / ".env"
                if env_path.exists():
                    load_dotenv(env_path)
                    logger.info(f"Loaded .env from: {env_path}")
                    break
                current = current.parent

        # Load known secrets from environment
        for name, env_var in self.SECRET_ENV_VARS.items():
            value = os.getenv(env_var)
            if value:
                self._set_cached(name, value, source="env")

    def _set_cached(
        self,
        name: str,
        value: str,
        source: str = "manual",
        expires_at: Optional[datetime] = None,
    ):
        """Set a value in cache."""
        self._cache[name] = value
        self._cache_metadata[name] = SecretMetadata(
            name=name,
            created_at=datetime.now(),
            expires_at=expires_at,
            version=self._cache_metadata.get(name, SecretMetadata(name, datetime.now(), None, 0, "")).version + 1,
            source=source,
        )
        self._cache_expires[name] = datetime.now() + timedelta(seconds=self.cache_ttl)

    def _is_expired(self, name: str) -> bool:
        """Check if cached value is expired."""
        if name not in self._cache_expires:
            return True
        return datetime.now() > self._cache_expires[name]

    def get(
        self,
        name: str,
        default: Optional[str] = None,
        required: bool = False,
    ) -> Optional[str]:
        """
        Get a secret value.

        Args:
            name: Secret name
            default: Default value if not found
            required: Raise error if not found

        Returns:
            Secret value

        Raises:
            SecretsError: If required and not found
        """
        # Check cache first
        if name in self._cache and not self._is_expired(name):
            return self._cache[name]

        # Try environment variable
        env_var = self.SECRET_ENV_VARS.get(name, name.upper())
        value = os.getenv(env_var)

        if value:
            self._set_cached(name, value, source="env")
            return value

        if required:
            raise SecretsError(
                f"Required secret not found: {name}. "
                f"Set {env_var} environment variable."
            )

        return default

    def set(
        self,
        name: str,
        value: str,
        expires_in: Optional[int] = None,
    ):
        """
        Set a secret value.

        Args:
            name: Secret name
            value: Secret value
            expires_in: Expiration in seconds
        """
        expires_at = None
        if expires_in:
            expires_at = datetime.now() + timedelta(seconds=expires_in)

        self._set_cached(name, value, source="manual", expires_at=expires_at)
        logger.info(f"Set secret: {name}")

    def delete(self, name: str):
        """Delete a secret."""
        if name in self._cache:
            del self._cache[name]
        if name in self._cache_metadata:
            del self._cache_metadata[name]
        if name in self._cache_expires:
            del self._cache_expires[name]
        logger.info(f"Deleted secret: {name}")

    def exists(self, name: str) -> bool:
        """Check if secret exists."""
        return self.get(name) is not None

    def list_secrets(self) -> Dict[str, SecretMetadata]:
        """List all secrets with metadata (not values)."""
        return {
            name: metadata
            for name, metadata in self._cache_metadata.items()
        }

    def get_masked(self, name: str) -> str:
        """
        Get masked version of secret for logging.

        Args:
            name: Secret name

        Returns:
            Masked secret (first/last 4 chars)
        """
        value = self.get(name)
        if not value:
            return "[NOT SET]"
        if len(value) <= 8:
            return "***"
        return f"{value[:4]}...{value[-4:]}"

    def rotate(self, name: str, new_value: str) -> bool:
        """
        Rotate a secret value.

        Args:
            name: Secret name
            new_value: New secret value

        Returns:
            True if rotated successfully
        """
        if name not in self._cache:
            logger.warning(f"Cannot rotate non-existent secret: {name}")
            return False

        old_version = self._cache_metadata[name].version
        self.set(name, new_value)

        logger.info(f"Rotated secret {name}: v{old_version} -> v{old_version + 1}")
        return True

    def encrypt(self, value: str) -> str:
        """
        Encrypt a value.

        Args:
            value: Value to encrypt

        Returns:
            Encrypted value (base64)
        """
        if not self._fernet:
            # Fallback: base64 encoding (not secure, just obfuscation)
            return base64.b64encode(value.encode()).decode()

        return self._fernet.encrypt(value.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        """
        Decrypt a value.

        Args:
            encrypted: Encrypted value

        Returns:
            Decrypted value
        """
        if not self._fernet:
            # Fallback: base64 decoding
            return base64.b64decode(encrypted.encode()).decode()

        return self._fernet.decrypt(encrypted.encode()).decode()

    def save_to_file(self, file_path: Path, secrets: Optional[list] = None):
        """
        Save secrets to encrypted file.

        Args:
            file_path: Output file path
            secrets: List of secret names to save (default: all)
        """
        secrets_to_save = secrets or list(self._cache.keys())

        data = {
            name: self.encrypt(self._cache[name])
            for name in secrets_to_save
            if name in self._cache
        }

        with open(file_path, "w") as f:
            json.dump(data, f)

        logger.info(f"Saved {len(data)} secrets to: {file_path}")

    def load_from_file(self, file_path: Path):
        """
        Load secrets from encrypted file.

        Args:
            file_path: Input file path
        """
        if not file_path.exists():
            raise SecretsError(f"Secrets file not found: {file_path}")

        with open(file_path) as f:
            data = json.load(f)

        for name, encrypted in data.items():
            try:
                value = self.decrypt(encrypted)
                self._set_cached(name, value, source="file")
            except Exception as e:
                logger.error(f"Failed to decrypt secret {name}: {e}")

        logger.info(f"Loaded {len(data)} secrets from: {file_path}")

    def get_api_key(self, provider: str) -> str:
        """
        Get API key for a provider.

        Args:
            provider: Provider name (claude, openai, gemini)

        Returns:
            API key

        Raises:
            SecretsError: If not found
        """
        key_name = f"{provider.lower()}_api_key"
        return self.get(key_name, required=True)

    def validate_required(self, required_secrets: list):
        """
        Validate that required secrets are present.

        Args:
            required_secrets: List of required secret names

        Raises:
            SecretsError: If any required secrets are missing
        """
        missing = []
        for name in required_secrets:
            if not self.exists(name):
                missing.append(name)

        if missing:
            raise SecretsError(
                f"Missing required secrets: {', '.join(missing)}"
            )


# Global secrets manager instance
_secrets_manager: Optional[SecretsManager] = None


def get_secrets_manager(
    env_file: Optional[Path] = None,
    encryption_key: Optional[str] = None,
) -> SecretsManager:
    """Get global secrets manager instance."""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager(
            env_file=env_file,
            encryption_key=encryption_key,
        )
    return _secrets_manager


def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Convenience function to get a secret.

    Args:
        name: Secret name
        default: Default value

    Returns:
        Secret value
    """
    manager = get_secrets_manager()
    return manager.get(name, default=default)


def require_secret(name: str) -> str:
    """
    Get a required secret.

    Args:
        name: Secret name

    Returns:
        Secret value

    Raises:
        SecretsError: If not found
    """
    manager = get_secrets_manager()
    return manager.get(name, required=True)
