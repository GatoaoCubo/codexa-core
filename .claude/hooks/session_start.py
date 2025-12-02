#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["python-dotenv"]
# ///
"""
CODEXA.app Session Start Hook

Triggered when Claude Code session starts.
Initializes CODEXA.app environment and services.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Paths
CODEXA_ROOT = Path(__file__).parent.parent.parent
VOICE_DIR = CODEXA_ROOT / "codexa.app" / "voice"
LOGS_DIR = CODEXA_ROOT / ".claude" / "logs"


def log(message: str):
    """Log to file and stderr."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"session_{datetime.now().strftime('%Y%m%d')}.log"

    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"

    with open(log_file, "a") as f:
        f.write(log_line)

    print(f"[CODEXA] {message}", file=sys.stderr)


def check_mcp_servers():
    """Verify MCP servers are configured."""
    mcp_config = CODEXA_ROOT / ".mcp.json"

    if not mcp_config.exists():
        log("WARNING: .mcp.json not found")
        return False

    with open(mcp_config) as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})
    log(f"MCP Servers configured: {list(servers.keys())}")

    return True


def check_voice_ready():
    """Check if voice system is available."""
    # Check for API keys
    has_elevenlabs = bool(os.getenv("ELEVENLABS_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    if has_elevenlabs:
        log("Voice: ElevenLabs API ready")
        return "elevenlabs"
    elif has_openai:
        log("Voice: OpenAI API ready")
        return "openai"
    else:
        log("Voice: Using local pyttsx3 (no API keys)")
        return "local"


def check_navigation_map():
    """Verify NAVIGATION_MAP.json exists."""
    nav_map = CODEXA_ROOT / "codexa.app" / "agentes" / "scout_agent" / "NAVIGATION_MAP.json"

    if nav_map.exists():
        with open(nav_map) as f:
            data = json.load(f)

        stats = data.get("stats", {})
        log(f"NAVIGATION_MAP: {stats.get('agents', 0)} agents, {stats.get('commands', 0)} commands")
        return True
    else:
        log("WARNING: NAVIGATION_MAP.json not found")
        return False


def main():
    """Session initialization."""
    try:
        # Read input if provided
        if not sys.stdin.isatty():
            input_data = json.loads(sys.stdin.read())
            session_id = input_data.get('session_id', 'unknown')
        else:
            session_id = 'cli'

        log(f"=== CODEXA.app Session Start (ID: {session_id}) ===")

        # Run checks
        check_mcp_servers()
        voice_provider = check_voice_ready()
        check_navigation_map()

        # Print welcome
        log("CODEXA.app ready. Use /codexa for orchestration.")

        # Optional: Voice greeting
        if voice_provider and os.getenv("CODEXA_VOICE_GREETING"):
            from utils.voice_cli import speak
            speak("CODEXA ponto app iniciado. Pronto para orquestrar.")

        sys.exit(0)

    except Exception as e:
        log(f"Session start error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
