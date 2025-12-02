"""
Secrets and API Keys Manager for CODEXA

Handles secure loading of API keys from .env file.
NEVER commit .env to git! Use .env.example as template.

Usage:
    from config.secrets import get_google_api_key, validate_api_keys

    api_key = get_google_api_key()
    if api_key:
        # Use API
        pass
    else:
        # Handle missing key
        pass

Version: 1.0.0
Created: 2025-11-24
Purpose: Secure API key management
"""

import os
from pathlib import Path
from typing import Optional, Dict
import warnings


# Get .env path (at codexa.app/)
CODEXA_APP = Path(__file__).parent.parent
ENV_FILE = CODEXA_APP / ".env"
ENV_EXAMPLE_FILE = CODEXA_APP / ".env.example"


def load_env_file() -> Dict[str, str]:
    """
    Load environment variables from .env file.

    Returns:
        Dictionary of key-value pairs from .env
    """
    env_vars = {}

    if not ENV_FILE.exists():
        warnings.warn(
            f"⚠️  .env file not found at {ENV_FILE}\n"
            f"Copy {ENV_EXAMPLE_FILE} to .env and add your API keys.",
            UserWarning
        )
        return env_vars

    try:
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Parse KEY=value
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    env_vars[key] = value

                    # Also set in os.environ for compatibility
                    os.environ[key] = value

        return env_vars

    except Exception as e:
        warnings.warn(f"Error loading .env file: {e}", UserWarning)
        return env_vars


# Load .env on import
_ENV_VARS = load_env_file()


def get_google_api_key() -> Optional[str]:
    """
    Get Google API key from environment.

    Returns:
        API key string or None if not found

    Example:
        >>> api_key = get_google_api_key()
        >>> if api_key:
        ...     # Use API
        ...     pass
    """
    # Try .env first, then os.environ (for system-level vars)
    key = _ENV_VARS.get('GOOGLE_API_KEY') or os.environ.get('GOOGLE_API_KEY')

    if not key or key == 'your_google_api_key_here':
        return None

    return key


def get_google_imagen_model() -> str:
    """
    Get Google Imagen model name.

    Returns:
        Model name (default: imagen-3.0-generate-001)
    """
    return (
        _ENV_VARS.get('GOOGLE_IMAGEN_MODEL') or
        os.environ.get('GOOGLE_IMAGEN_MODEL') or
        'imagen-3.0-generate-001'
    )


def get_google_gemini_model() -> str:
    """
    Get Google Gemini model name.

    Returns:
        Model name (default: gemini-2.0-flash-exp)
    """
    return (
        _ENV_VARS.get('GOOGLE_GEMINI_MODEL') or
        os.environ.get('GOOGLE_GEMINI_MODEL') or
        'gemini-2.0-flash-exp'
    )


def get_api_timeout() -> int:
    """
    Get API timeout in seconds.

    Returns:
        Timeout value (default: 30)
    """
    timeout = (
        _ENV_VARS.get('GOOGLE_API_TIMEOUT') or
        os.environ.get('GOOGLE_API_TIMEOUT') or
        '30'
    )

    try:
        return int(timeout)
    except ValueError:
        return 30


def get_max_image_size_mb() -> int:
    """
    Get maximum image size in MB.

    Returns:
        Max size in MB (default: 10)
    """
    size = (
        _ENV_VARS.get('MAX_IMAGE_SIZE_MB') or
        os.environ.get('MAX_IMAGE_SIZE_MB') or
        '10'
    )

    try:
        return int(size)
    except ValueError:
        return 10


def validate_api_keys() -> Dict[str, bool]:
    """
    Validate that required API keys are configured.

    Returns:
        Dictionary mapping key name to validity boolean

    Example:
        >>> status = validate_api_keys()
        >>> if status['google_api_key']:
        ...     print("✓ Google API configured")
        ... else:
        ...     print("✗ Google API key missing")
    """
    return {
        'google_api_key': get_google_api_key() is not None,
        'env_file_exists': ENV_FILE.exists(),
        'env_example_exists': ENV_EXAMPLE_FILE.exists(),
    }


def print_api_status():
    """
    Print current API configuration status.

    Useful for debugging and setup verification.
    """
    print("=" * 70)
    print("CODEXA API Keys Status")
    print("=" * 70)
    print()

    status = validate_api_keys()

    # Check symbols
    CHECK = '✓' if all(status.values()) else '✓'
    CROSS = '✗'

    print("Configuration Files:")
    print(f"  {CHECK if status['env_example_exists'] else CROSS} .env.example exists")
    print(f"  {CHECK if status['env_file_exists'] else CROSS} .env exists")
    print()

    print("API Keys:")
    if status['google_api_key']:
        key = get_google_api_key()
        masked_key = f"{key[:8]}...{key[-4:]}" if key else "None"
        print(f"  {CHECK} Google API Key: {masked_key}")
    else:
        print(f"  {CROSS} Google API Key: Missing")
        print(f"      → Copy .env.example to .env and add your key")
        print(f"      → Get key at: https://aistudio.google.com/app/apikey")
    print()

    print("Models:")
    print(f"  Imagen: {get_google_imagen_model()}")
    print(f"  Gemini: {get_google_gemini_model()}")
    print()

    print("Settings:")
    print(f"  API Timeout: {get_api_timeout()}s")
    print(f"  Max Image Size: {get_max_image_size_mb()}MB")
    print()

    print("=" * 70)
    if all(status.values()):
        print("✓ All API keys configured and ready")
    else:
        print("⚠️  Some API keys are missing - check .env file")
    print("=" * 70)


# === MAIN ===
if __name__ == "__main__":
    print_api_status()
