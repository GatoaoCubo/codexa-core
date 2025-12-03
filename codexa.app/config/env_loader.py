"""
CODEXA Environment Loader | Centralized Configuration Module
=============================================================

Single source of truth for ALL environment variables across CODEXA.
Loads from project root .env file and provides typed accessors.

Usage:
    from config.env_loader import env, supabase, llm, voice, video

    # LLM Keys
    api_key = llm.anthropic_key

    # Supabase
    url = supabase.url
    admin_key = supabase.service_role_key

    # Check configuration
    env.print_status()

Version: 1.0.0
Created: 2025-12-03
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any


# ==============================================================================
# PATH DETECTION
# ==============================================================================

def find_project_root() -> Path:
    """Find project root by looking for .env or .git directory."""
    current = Path(__file__).resolve().parent

    for _ in range(10):  # Max 10 levels up
        # Check for project markers
        if (current / ".env").exists():
            return current
        if (current / ".env.example").exists():
            return current
        if (current / ".git").exists():
            return current
        if (current / "CLAUDE.md").exists():
            return current

        parent = current.parent
        if parent == current:
            break
        current = parent

    # Fallback to codexa.app parent
    return Path(__file__).resolve().parent.parent.parent


PROJECT_ROOT = find_project_root()
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"


# ==============================================================================
# ENV LOADING
# ==============================================================================

def load_env() -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}

    if not ENV_FILE.exists():
        return env_vars

    try:
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Parse KEY=value
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                env_vars[key] = value

                # Also set in os.environ for compatibility
                if key not in os.environ:
                    os.environ[key] = value

    except Exception:
        pass

    return env_vars


# Load on import
_ENV = load_env()


def get(key: str, default: str = "") -> str:
    """Get environment variable with fallback to os.environ."""
    return _ENV.get(key) or os.environ.get(key) or default


def get_bool(key: str, default: bool = False) -> bool:
    """Get boolean environment variable."""
    val = get(key, str(default)).lower()
    return val in ("true", "1", "yes", "on")


def get_int(key: str, default: int = 0) -> int:
    """Get integer environment variable."""
    try:
        return int(get(key, str(default)))
    except ValueError:
        return default


def get_float(key: str, default: float = 0.0) -> float:
    """Get float environment variable."""
    try:
        return float(get(key, str(default)))
    except ValueError:
        return default


def is_placeholder(value: str) -> bool:
    """Check if value is a placeholder (not filled in)."""
    if not value:
        return True
    placeholders = [
        "{YOUR_", "your_", "xxxxx", "YOUR_",
        "sk-ant-xxxxx", "sk-xxxxx", "AIzaSy...",
        "eyJhbGciOi...", "rw_xxxxx", "pk_xxxxx"
    ]
    return any(p in value for p in placeholders)


# ==============================================================================
# CONFIGURATION CLASSES
# ==============================================================================

@dataclass
class LLMConfig:
    """LLM Provider configuration."""

    @property
    def anthropic_key(self) -> str:
        return get("ANTHROPIC_API_KEY")

    @property
    def openai_key(self) -> str:
        return get("OPENAI_API_KEY")

    @property
    def google_key(self) -> str:
        return get("GOOGLE_API_KEY")

    @property
    def has_any_key(self) -> bool:
        """Check if at least one LLM key is configured."""
        return any([
            self.anthropic_key and not is_placeholder(self.anthropic_key),
            self.openai_key and not is_placeholder(self.openai_key),
            self.google_key and not is_placeholder(self.google_key),
        ])

    @property
    def primary_provider(self) -> Optional[str]:
        """Get the first available provider."""
        if self.anthropic_key and not is_placeholder(self.anthropic_key):
            return "anthropic"
        if self.openai_key and not is_placeholder(self.openai_key):
            return "openai"
        if self.google_key and not is_placeholder(self.google_key):
            return "google"
        return None


@dataclass
class SupabaseConfig:
    """Supabase configuration."""

    @property
    def url(self) -> str:
        return get("SUPABASE_URL")

    @property
    def service_role_key(self) -> str:
        return get("SUPABASE_SERVICE_ROLE_KEY")

    @property
    def anon_key(self) -> str:
        return get("SUPABASE_ANON_KEY")

    @property
    def is_configured(self) -> bool:
        """Check if Supabase is fully configured."""
        return bool(
            self.url and not is_placeholder(self.url) and
            self.anon_key and not is_placeholder(self.anon_key)
        )

    @property
    def has_admin_access(self) -> bool:
        """Check if admin (service role) access is available."""
        return bool(
            self.service_role_key and
            not is_placeholder(self.service_role_key)
        )

    def get_headers(self, admin: bool = False) -> Dict[str, str]:
        """Get HTTP headers for Supabase API calls."""
        key = self.service_role_key if admin else self.anon_key
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }


@dataclass
class VoiceConfig:
    """Voice/TTS configuration."""

    @property
    def elevenlabs_key(self) -> str:
        return get("ELEVENLABS_API_KEY")

    @property
    def voice_id(self) -> str:
        return get("ELEVENLABS_VOICE_ID", "pMsXgVXv3BLzUgSXRplE")

    @property
    def model_id(self) -> str:
        return get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

    @property
    def port(self) -> int:
        return get_int("VOICE_PORT", 5000)

    @property
    def language(self) -> str:
        return get("VOICE_LANGUAGE", "pt-BR")

    @property
    def is_configured(self) -> bool:
        return bool(self.elevenlabs_key and not is_placeholder(self.elevenlabs_key))


@dataclass
class VideoConfig:
    """Video generation configuration."""

    @property
    def runway_key(self) -> str:
        return get("RUNWAY_API_KEY")

    @property
    def pika_key(self) -> str:
        return get("PIKA_API_KEY")

    @property
    def google_ai_key(self) -> str:
        return get("GOOGLE_AI_API_KEY")

    @property
    def kling_key(self) -> str:
        return get("KLING_API_KEY")

    @property
    def hailuo_key(self) -> str:
        return get("HAILUO_API_KEY")

    @property
    def debug(self) -> bool:
        return get_bool("VIDEO_AGENT_DEBUG", False)

    @property
    def mock_api(self) -> bool:
        return get_bool("VIDEO_AGENT_MOCK_API", False)

    @property
    def log_level(self) -> str:
        return get("VIDEO_AGENT_LOG_LEVEL", "INFO")

    @property
    def output_dir(self) -> str:
        return get("VIDEO_AGENT_OUTPUT_DIR", "./outputs")

    @property
    def max_concurrent(self) -> int:
        return get_int("VIDEO_AGENT_MAX_CONCURRENT", 5)

    @property
    def api_timeout(self) -> int:
        return get_int("VIDEO_AGENT_API_TIMEOUT", 300)

    @property
    def max_cost_per_video(self) -> float:
        return get_float("VIDEO_AGENT_MAX_COST_PER_VIDEO", 5.0)

    @property
    def daily_cost_limit(self) -> float:
        return get_float("VIDEO_AGENT_DAILY_COST_LIMIT", 50.0)

    @property
    def min_quality_score(self) -> float:
        return get_float("VIDEO_AGENT_MIN_QUALITY_SCORE", 7.0)

    @property
    def is_configured(self) -> bool:
        """Check if at least one video provider is configured."""
        return any([
            self.runway_key and not is_placeholder(self.runway_key),
            self.pika_key and not is_placeholder(self.pika_key),
        ])


@dataclass
class GoogleConfig:
    """Google AI configuration."""

    @property
    def api_key(self) -> str:
        return get("GOOGLE_API_KEY")

    @property
    def imagen_model(self) -> str:
        return get("GOOGLE_IMAGEN_MODEL", "imagen-3.0-generate-001")

    @property
    def gemini_model(self) -> str:
        return get("GOOGLE_GEMINI_MODEL", "gemini-2.0-flash-exp")

    @property
    def timeout(self) -> int:
        return get_int("GOOGLE_API_TIMEOUT", 30)

    @property
    def max_image_size_mb(self) -> int:
        return get_int("MAX_IMAGE_SIZE_MB", 10)


@dataclass
class CloudStorageConfig:
    """Cloud storage configuration."""

    # AWS S3
    @property
    def aws_access_key(self) -> str:
        return get("AWS_ACCESS_KEY_ID")

    @property
    def aws_secret_key(self) -> str:
        return get("AWS_SECRET_ACCESS_KEY")

    @property
    def aws_bucket(self) -> str:
        return get("AWS_S3_BUCKET", "codexa-outputs")

    @property
    def aws_region(self) -> str:
        return get("AWS_REGION", "us-east-1")

    # Cloudflare R2
    @property
    def r2_account_id(self) -> str:
        return get("CLOUDFLARE_ACCOUNT_ID")

    @property
    def r2_access_key(self) -> str:
        return get("CLOUDFLARE_R2_ACCESS_KEY_ID")

    @property
    def r2_secret_key(self) -> str:
        return get("CLOUDFLARE_R2_SECRET_ACCESS_KEY")

    @property
    def r2_bucket(self) -> str:
        return get("CLOUDFLARE_R2_BUCKET_NAME", "codexa-assets")

    @property
    def r2_public_domain(self) -> str:
        return get("CLOUDFLARE_R2_PUBLIC_DOMAIN")


@dataclass
class AutomationConfig:
    """Automation and CI/CD configuration."""

    @property
    def github_pat(self) -> str:
        return get("GITHUB_PAT")

    @property
    def e2b_key(self) -> str:
        return get("E2B_API_KEY")


@dataclass
class PesquisaConfig:
    """Pesquisa agent configuration."""

    @property
    def web_search(self) -> bool:
        return get_bool("WEB_SEARCH", True)

    @property
    def vision(self) -> bool:
        return get_bool("VISION", True)

    @property
    def file_search(self) -> bool:
        return get_bool("FILE_SEARCH", False)

    @property
    def code_interpreter(self) -> bool:
        return get_bool("CODE_INTERPRETER", False)

    @property
    def marketplace_priority(self) -> str:
        return get("MARKETPLACE_PRIORITY", "mercadolivre,shopee,magazineluiza,amazon_br")

    @property
    def min_competitors(self) -> int:
        return get_int("MIN_COMPETITORS", 3)

    @property
    def min_confidence_score(self) -> float:
        return get_float("MIN_CONFIDENCE_SCORE", 0.75)

    @property
    def validate_anvisa(self) -> bool:
        return get_bool("VALIDATE_ANVISA", True)

    @property
    def validate_inmetro(self) -> bool:
        return get_bool("VALIDATE_INMETRO", True)


# ==============================================================================
# MAIN ENV CLASS
# ==============================================================================

class EnvConfig:
    """Main environment configuration class."""

    def __init__(self):
        self.llm = LLMConfig()
        self.supabase = SupabaseConfig()
        self.voice = VoiceConfig()
        self.video = VideoConfig()
        self.google = GoogleConfig()
        self.storage = CloudStorageConfig()
        self.automation = AutomationConfig()
        self.pesquisa = PesquisaConfig()

    @property
    def project_root(self) -> Path:
        return PROJECT_ROOT

    @property
    def env_file(self) -> Path:
        return ENV_FILE

    @property
    def env_exists(self) -> bool:
        return ENV_FILE.exists()

    def reload(self):
        """Reload environment variables from .env file."""
        global _ENV
        _ENV = load_env()

    def validate(self) -> Dict[str, bool]:
        """Validate configuration status."""
        return {
            "env_file_exists": self.env_exists,
            "llm_configured": self.llm.has_any_key,
            "supabase_configured": self.supabase.is_configured,
            "supabase_admin": self.supabase.has_admin_access,
            "voice_configured": self.voice.is_configured,
            "video_configured": self.video.is_configured,
        }

    def print_status(self):
        """Print configuration status to console."""
        # Cross-platform symbols
        CHECK = "[OK]" if sys.platform == "win32" else "OK"
        CROSS = "[X]" if sys.platform == "win32" else "X"
        WARN = "[!]" if sys.platform == "win32" else "!"

        def status_icon(ok: bool, required: bool = True) -> str:
            if ok:
                return CHECK
            return CROSS if required else WARN

        def mask_key(key: str) -> str:
            if not key or is_placeholder(key):
                return "(not set)"
            if len(key) > 12:
                return f"{key[:8]}...{key[-4:]}"
            return "****"

        print("=" * 70)
        print("CODEXA Environment Configuration Status")
        print("=" * 70)
        print(f"\nProject Root: {PROJECT_ROOT}")
        print(f"ENV File: {ENV_FILE} {'(exists)' if self.env_exists else '(MISSING)'}")
        print()

        # LLM Providers
        print("--- LLM PROVIDERS (at least 1 required) ---")
        print(f"  {status_icon(self.llm.anthropic_key and not is_placeholder(self.llm.anthropic_key))} Anthropic: {mask_key(self.llm.anthropic_key)}")
        print(f"  {status_icon(self.llm.openai_key and not is_placeholder(self.llm.openai_key), False)} OpenAI: {mask_key(self.llm.openai_key)}")
        print(f"  {status_icon(self.llm.google_key and not is_placeholder(self.llm.google_key), False)} Google: {mask_key(self.llm.google_key)}")
        if self.llm.primary_provider:
            print(f"  -> Primary: {self.llm.primary_provider}")
        print()

        # Supabase
        print("--- SUPABASE (required for anuncio_agent) ---")
        print(f"  {status_icon(bool(self.supabase.url and not is_placeholder(self.supabase.url)))} URL: {self.supabase.url or '(not set)'}")
        print(f"  {status_icon(self.supabase.has_admin_access)} Service Role Key: {mask_key(self.supabase.service_role_key)}")
        print(f"  {status_icon(bool(self.supabase.anon_key and not is_placeholder(self.supabase.anon_key)), False)} Anon Key: {mask_key(self.supabase.anon_key)}")
        print()

        # Voice
        print("--- VOICE (optional) ---")
        print(f"  {status_icon(self.voice.is_configured, False)} ElevenLabs: {mask_key(self.voice.elevenlabs_key)}")
        print(f"     Voice ID: {self.voice.voice_id}")
        print(f"     Language: {self.voice.language}")
        print()

        # Video
        print("--- VIDEO (optional) ---")
        print(f"  {status_icon(bool(self.video.runway_key and not is_placeholder(self.video.runway_key)), False)} Runway: {mask_key(self.video.runway_key)}")
        print(f"  {status_icon(bool(self.video.pika_key and not is_placeholder(self.video.pika_key)), False)} Pika: {mask_key(self.video.pika_key)}")
        print()

        # Summary
        print("=" * 70)
        status = self.validate()
        if status["llm_configured"]:
            print(f"{CHECK} Ready to use CODEXA")
        else:
            print(f"{CROSS} Missing required configuration - edit .env file")
        print("=" * 70)


# ==============================================================================
# SINGLETON INSTANCES
# ==============================================================================

# Main config instance
env = EnvConfig()

# Shortcut accessors
llm = env.llm
supabase = env.supabase
voice = env.voice
video = env.video
google = env.google
storage = env.storage
automation = env.automation
pesquisa = env.pesquisa


# ==============================================================================
# LEGACY COMPATIBILITY
# ==============================================================================

# For scripts that use os.getenv directly, ensure vars are loaded
def ensure_loaded():
    """Ensure environment variables are loaded into os.environ."""
    load_env()


# ==============================================================================
# CLI
# ==============================================================================

if __name__ == "__main__":
    env.print_status()
