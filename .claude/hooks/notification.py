#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
CODEXA.app Notification Hook

Triggered on important events. Optionally speaks via TTS.
"""

import json
import sys
import os
from pathlib import Path

# Configuration
VOICE_ENABLED = os.getenv("CODEXA_VOICE_NOTIFICATIONS", "false").lower() == "true"
CODEXA_ROOT = Path(__file__).parent.parent.parent


def speak_notification(text: str):
    """Speak notification if voice enabled."""
    if not VOICE_ENABLED:
        return

    try:
        import subprocess
        voice_cli = CODEXA_ROOT / ".claude" / "hooks" / "utils" / "voice_cli.py"
        subprocess.run(
            ["uv", "run", str(voice_cli), "speak", text],
            capture_output=True,
            timeout=30
        )
    except Exception:
        pass  # Silent fail for notifications


def main():
    """Process notification event."""
    try:
        input_data = json.loads(sys.stdin.read())

        event_type = input_data.get('event_type', 'unknown')
        message = input_data.get('message', '')

        # Log notification
        print(f"[CODEXA] Notification: {event_type} - {message}", file=sys.stderr)

        # Voice notifications for important events
        if event_type in ['task_complete', 'error', 'confirmation_needed']:
            speak_notification(message)

        sys.exit(0)

    except Exception as e:
        print(f"[CODEXA] Notification error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
