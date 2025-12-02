#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
CODEXA.app Session Stop Hook

Cleanup when Claude Code session ends.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Paths
CODEXA_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = CODEXA_ROOT / ".claude" / "logs"


def log(message: str):
    """Log to file."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"session_{datetime.now().strftime('%Y%m%d')}.log"

    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"

    with open(log_file, "a") as f:
        f.write(log_line)


def cleanup_temp_files():
    """Clean up temporary files."""
    temp_patterns = [
        CODEXA_ROOT / "outputs" / "temp" / "*",
        CODEXA_ROOT / ".claude" / "temp" / "*",
    ]

    for pattern in temp_patterns:
        parent = pattern.parent
        if parent.exists():
            for f in parent.glob("*"):
                if f.is_file():
                    try:
                        f.unlink()
                    except Exception:
                        pass


def main():
    """Session cleanup."""
    try:
        input_data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
        session_id = input_data.get('session_id', 'unknown')

        log(f"=== Session Stop (ID: {session_id}) ===")

        # Cleanup
        cleanup_temp_files()

        # Optional: Voice goodbye
        if os.getenv("CODEXA_VOICE_GREETING"):
            try:
                from utils.voice_cli import speak
                speak("Sessão encerrada. Até logo!")
            except Exception:
                pass

        log("Session cleanup complete")
        sys.exit(0)

    except Exception as e:
        log(f"Session stop error: {e}")
        sys.exit(0)  # Don't block on error


if __name__ == '__main__':
    main()
