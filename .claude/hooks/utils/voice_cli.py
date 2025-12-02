#!/usr/bin/env python3
"""
CODEXA.app Voice CLI - Bidirectional Voice Interface
Based on TAC-8 voice_cli.py patterns

Provides:
- speak(text) - Text to Speech via ElevenLabs/OpenAI/pyttsx3
- listen(duration, language) - Speech to Text via ElevenLabs Scribe
"""

import subprocess
import sys
import os
from pathlib import Path

# Paths
CODEXA_ROOT = Path(__file__).parent.parent.parent.parent
VOICE_DIR = CODEXA_ROOT / "codexa.app" / "voice"


def speak(text: str, voice_id: str = None) -> bool:
    """
    Convert text to speech using available TTS provider.

    Priority:
    1. ElevenLabs (if ELEVENLABS_API_KEY set)
    2. OpenAI (if OPENAI_API_KEY set)
    3. pyttsx3 (local, no API key)

    Args:
        text: Text to speak
        voice_id: Optional voice ID for ElevenLabs

    Returns:
        True if successful, False otherwise
    """
    if not text or not text.strip():
        return False

    tts_script = VOICE_DIR / "tts.py"

    try:
        cmd = ["uv", "run", str(tts_script), text]
        if voice_id:
            cmd.extend(["--voice", voice_id])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(CODEXA_ROOT)
        )

        if result.returncode != 0:
            print(f"[VOICE] TTS error: {result.stderr}", file=sys.stderr)
            return False

        return True

    except subprocess.TimeoutExpired:
        print("[VOICE] TTS timeout", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[VOICE] TTS exception: {e}", file=sys.stderr)
        return False


def listen(duration: int = 5, language: str = "pt") -> str:
    """
    Capture audio and transcribe via STT.

    Uses ElevenLabs Scribe v1 for transcription.

    Args:
        duration: Recording duration in seconds
        language: Language code (pt, en, es, fr, de, etc.)

    Returns:
        Transcribed text or empty string on failure
    """
    stt_script = VOICE_DIR / "stt.py"

    try:
        result = subprocess.run(
            ["uv", "run", str(stt_script), str(duration), language],
            capture_output=True,
            text=True,
            timeout=duration + 30,
            cwd=str(CODEXA_ROOT)
        )

        if result.returncode != 0:
            print(f"[VOICE] STT error: {result.stderr}", file=sys.stderr)
            return ""

        # Get last line (transcription result)
        lines = result.stdout.strip().split('\n')
        transcription = lines[-1] if lines else ""

        return transcription

    except subprocess.TimeoutExpired:
        print("[VOICE] STT timeout", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"[VOICE] STT exception: {e}", file=sys.stderr)
        return ""


def voice_prompt(prompt_text: str = "Diga algo...", duration: int = 10, language: str = "pt") -> str:
    """
    Speak a prompt, then listen for response.

    Args:
        prompt_text: Text to speak as prompt
        duration: How long to listen
        language: Language code

    Returns:
        User's transcribed response
    """
    speak(prompt_text)
    return listen(duration, language)


def voice_report(text: str, summary: bool = True) -> bool:
    """
    Speak a report, optionally summarizing long text.

    Args:
        text: Full text to report
        summary: If True and text > 500 chars, summarize

    Returns:
        True if successful
    """
    if summary and len(text) > 500:
        # Truncate to first 500 chars + "..."
        text = text[:500] + "... e mais detalhes no relatório escrito."

    return speak(text)


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CODEXA Voice CLI")
    subparsers = parser.add_subparsers(dest="command")

    # speak command
    speak_parser = subparsers.add_parser("speak", help="Text to speech")
    speak_parser.add_argument("text", help="Text to speak")
    speak_parser.add_argument("--voice", help="Voice ID")

    # listen command
    listen_parser = subparsers.add_parser("listen", help="Speech to text")
    listen_parser.add_argument("--duration", type=int, default=5, help="Duration in seconds")
    listen_parser.add_argument("--language", default="pt", help="Language code")

    # prompt command
    prompt_parser = subparsers.add_parser("prompt", help="Speak then listen")
    prompt_parser.add_argument("text", help="Prompt text")
    prompt_parser.add_argument("--duration", type=int, default=10)
    prompt_parser.add_argument("--language", default="pt")

    args = parser.parse_args()

    if args.command == "speak":
        success = speak(args.text, args.voice if hasattr(args, 'voice') else None)
        sys.exit(0 if success else 1)

    elif args.command == "listen":
        result = listen(args.duration, args.language)
        print(result)
        sys.exit(0 if result else 1)

    elif args.command == "prompt":
        result = voice_prompt(args.text, args.duration, args.language)
        print(result)
        sys.exit(0 if result else 1)

    else:
        parser.print_help()
        sys.exit(1)
