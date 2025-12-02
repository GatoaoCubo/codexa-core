#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice MCP Server v3.0
============================

MCP Server for Claude Code voice integration.
Provides voice tools for accessibility users.

v3.0 CHANGES:
    - NEW: Poll-based API (listen_start, listen_poll, listen_stop)
    - Non-blocking voice capture with background recording
    - Maintains legacy API compatibility

Tools (NEW - Poll-Based):
    - listen_start: Start recording, returns session_id immediately
    - listen_poll: Check session status (recording/transcribing/done)
    - listen_stop: Cancel recording immediately

Tools (Legacy - Blocking):
    - listen: Capture voice (BLOCKING - may take 15s+)
    - speak: Text-to-speech
    - start_voice_loop: Begin continuous mode
    - listen_and_respond: Continuous mode listening
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Any

# Fix encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add voice module to path (this directory)
VOICE_ROOT = Path(__file__).parent
PROJECT_ROOT = VOICE_ROOT.parent.parent  # codexa.gato/
sys.path.insert(0, str(VOICE_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment from project root
from dotenv import load_dotenv
env_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=env_path)

# Import MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("MCP SDK nao instalado. pip install mcp", file=sys.stderr)
    sys.exit(1)

# Import voice modules
from stt import (
    listen as voice_listen,
    record_audio_with_vad,
    transcribe_audio,
    play_start_beep
)
from tts import speak as voice_speak
from config import (
    EXIT_COMMANDS,
    MSG_ACTIVATED,
    MSG_GOODBYE,
    is_exit_command,
    WAKE_WORD_ENABLED,
    NOISE_GATE_ENABLED,
    get_wake_words_list
)

# Import voice filter
from voice_filter import (
    filter_voice_input,
    FilterConfig,
    FilterResult,
    is_noise,
    clean_transcript
)

# Import new poll-based session manager
from voice_session import (
    get_manager,
    start_session,
    poll_session,
    stop_session,
    list_sessions
)

# Create MCP server
server = Server("codexa-voice")

# =============================================================================
# VOICE FILTER STATE
# =============================================================================

# Track wake word state per session
_wake_word_state = {
    "activated": False,
    "activated_at": 0.0,
    "timeout": 30.0  # Seconds to remember wake word
}


def _get_filter_config() -> FilterConfig:
    """Get filter config from settings."""
    return FilterConfig(
        wake_words=get_wake_words_list() if WAKE_WORD_ENABLED else [],
        require_wake_word=WAKE_WORD_ENABLED,
        wake_word_timeout=30.0
    )


def _check_wake_word_active() -> bool:
    """Check if wake word was recently activated."""
    import time
    if not _wake_word_state["activated"]:
        return False
    elapsed = time.time() - _wake_word_state["activated_at"]
    if elapsed > _wake_word_state["timeout"]:
        _wake_word_state["activated"] = False
        return False
    return True


def _activate_wake_word():
    """Mark wake word as activated."""
    import time
    _wake_word_state["activated"] = True
    _wake_word_state["activated_at"] = time.time()


def _deactivate_wake_word():
    """Clear wake word state."""
    _wake_word_state["activated"] = False


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available voice tools."""
    return [
        # =====================================================================
        # NEW POLL-BASED API (v3.0)
        # =====================================================================
        Tool(
            name="listen_start",
            description="""Start voice recording in background. Returns immediately with session_id.
Use listen_poll to check when recording is done.

RECOMMENDED for Claude Code - avoids blocking the interface.

Returns: {"session_id": "abc123", "status": "starting"}""",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_duration": {
                        "type": "number",
                        "description": "Max recording duration in seconds (default: 10)",
                        "default": 10
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code for transcription (default: 'pt')",
                        "default": "pt"
                    },
                    "initial_timeout": {
                        "type": "number",
                        "description": "Exit early if no speech detected in this time (default: 3)",
                        "default": 3
                    }
                }
            }
        ),
        Tool(
            name="listen_poll",
            description="""Check status of a voice recording session.
Returns immediately - does NOT block.

Status values:
- "recording": Still capturing audio
- "transcribing": Audio captured, calling transcription API
- "done": Complete! Check "transcript" field
- "timeout": No speech detected
- "error": Check "error" field
- "cancelled": Session was stopped

Returns: {"status": "done", "transcript": "user said this", "elapsed": 5.2}""",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID from listen_start"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="listen_stop",
            description="Cancel a recording session immediately.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID to cancel"
                    }
                },
                "required": ["session_id"]
            }
        ),

        # =====================================================================
        # LEGACY BLOCKING API (v2.x compatibility)
        # =====================================================================
        Tool(
            name="listen",
            description="[LEGACY/BLOCKING] Capture and transcribe voice. May block for 15+ seconds. Use listen_start for non-blocking.",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "Max recording duration in seconds (default: 10)",
                        "default": 10
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code (default: 'pt')",
                        "default": "pt"
                    }
                }
            }
        ),
        Tool(
            name="speak",
            description="Speak text using TTS. Auto-selects best provider.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to speak"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="start_voice_loop",
            description="Start continuous voice mode. Use for accessibility.",
            inputSchema={
                "type": "object",
                "properties": {
                    "greeting": {
                        "type": "string",
                        "description": "Optional greeting to speak",
                        "default": "Modo voz ativado. Pode falar."
                    }
                }
            }
        ),
        Tool(
            name="listen_and_respond",
            description="[LEGACY/BLOCKING] Listen for voice command in continuous mode. Use poll-based API instead.",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_duration": {
                        "type": "number",
                        "description": "Max recording duration",
                        "default": 15
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""

    try:
        # =================================================================
        # NEW POLL-BASED API
        # =================================================================

        if name == "listen_start":
            max_duration = arguments.get("max_duration", 10)
            language = arguments.get("language", "pt")
            initial_timeout = arguments.get("initial_timeout", 3)

            print(f"Starting voice session (max {max_duration}s, timeout {initial_timeout}s)...",
                  file=sys.stderr)

            # This returns immediately - recording happens in background
            result = start_session(
                max_duration=max_duration,
                language=language,
                initial_timeout=initial_timeout,
                use_vad=True
            )

            if result.get("session_id"):
                return [TextContent(
                    type="text",
                    text=f"""VOICE_SESSION_STARTED
session_id: {result['session_id']}
status: {result['status']}
max_duration: {max_duration}s

NEXT: Call listen_poll with session_id to check when done.
User can speak now - recording in background."""
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"ERROR: {result.get('error', 'Failed to start session')}"
                )]

        elif name == "listen_poll":
            session_id = arguments.get("session_id")

            if not session_id:
                return [TextContent(type="text", text="ERROR: session_id required")]

            # This returns immediately
            result = poll_session(session_id)
            status = result.get("status", "unknown")

            if status == "done":
                transcript = result.get("transcript", "")
                elapsed = result.get("elapsed", 0)

                if transcript:
                    # Apply voice filters
                    config = _get_filter_config()
                    wake_active = _check_wake_word_active()
                    filter_result = filter_voice_input(transcript, config, previous_wake_word=wake_active)

                    # Handle filter result
                    if filter_result.accepted:
                        # Valid command - clear wake word state after use
                        _deactivate_wake_word()

                        # Check for exit commands
                        if is_exit_command(filter_result.command):
                            return [TextContent(
                                type="text",
                                text=f"EXIT_VOICE_LOOP: User said exit command.\nTranscript: {filter_result.command}"
                            )]

                        return [TextContent(
                            type="text",
                            text=f"""VOICE_COMMAND: {filter_result.command}
session_id: {session_id}
elapsed: {elapsed}s
status: done
wake_word: {'detected' if filter_result.wake_word_detected else 'not_required'}"""
                        )]

                    elif filter_result.awaiting_command:
                        # Wake word detected, waiting for actual command
                        _activate_wake_word()
                        return [TextContent(
                            type="text",
                            text=f"""WAKE_WORD_DETECTED: Listening for command...
session_id: {session_id}
elapsed: {elapsed}s
original: {transcript}

NEXT: Call listen_start again to capture the actual command."""
                        )]

                    elif filter_result.reason == "noise":
                        # Filtered as noise - ignore silently
                        return [TextContent(
                            type="text",
                            text=f"""NOISE_FILTERED: Ignored ambient noise.
session_id: {session_id}
elapsed: {elapsed}s
original: {transcript}

NEXT: Call listen_start again to retry."""
                        )]

                    elif filter_result.reason == "no_wake_word":
                        # No wake word - ignore
                        return [TextContent(
                            type="text",
                            text=f"""AWAITING_WAKE_WORD: Say "codexa" to activate.
session_id: {session_id}
elapsed: {elapsed}s
original: {transcript}

NEXT: Call listen_start again."""
                        )]

                    else:
                        # Invalid command
                        return [TextContent(
                            type="text",
                            text=f"""INVALID_COMMAND: Filtered out.
session_id: {session_id}
elapsed: {elapsed}s
reason: {filter_result.reason}
original: {transcript}

NEXT: Call listen_start again."""
                        )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"NO_SPEECH_DETECTED: Transcription returned empty.\nsession_id: {session_id}"
                    )]

            elif status == "timeout":
                return [TextContent(
                    type="text",
                    text=f"""NO_SPEECH_DETECTED: No speech in initial timeout period.
session_id: {session_id}
elapsed: {result.get('elapsed', 0)}s

To retry: call listen_start again."""
                )]

            elif status == "error":
                return [TextContent(
                    type="text",
                    text=f"VOICE_ERROR: {result.get('error', 'Unknown error')}\nsession_id: {session_id}"
                )]

            elif status == "cancelled":
                return [TextContent(
                    type="text",
                    text=f"SESSION_CANCELLED: Recording was stopped.\nsession_id: {session_id}"
                )]

            elif status == "not_found":
                return [TextContent(
                    type="text",
                    text=f"SESSION_NOT_FOUND: {result.get('error', 'Session expired or invalid')}"
                )]

            else:
                # Still in progress (recording, processing, transcribing)
                return [TextContent(
                    type="text",
                    text=f"""VOICE_SESSION_IN_PROGRESS
session_id: {session_id}
status: {status}
elapsed: {result.get('elapsed', 0)}s
has_speech: {result.get('has_speech', False)}

Poll again in ~500ms to check status."""
                )]

        elif name == "listen_stop":
            session_id = arguments.get("session_id")

            if not session_id:
                return [TextContent(type="text", text="ERROR: session_id required")]

            result = stop_session(session_id)

            return [TextContent(
                type="text",
                text=f"Session {session_id} {result.get('status', 'unknown')}"
            )]

        # =================================================================
        # LEGACY BLOCKING API
        # =================================================================

        elif name == "listen":
            duration = arguments.get("duration", 10)
            language = arguments.get("language", "pt")

            print(f"[LEGACY] Listening for {duration}s...", file=sys.stderr)

            # BLOCKING - runs in thread pool
            text = await asyncio.to_thread(
                voice_listen,
                duration=duration,
                language=language
            )

            if text and text.strip():
                if text.startswith("ERROR:"):
                    return [TextContent(type="text", text=text)]
                return [TextContent(type="text", text=f"User said: {text}")]
            else:
                return [TextContent(type="text", text="No speech detected.")]

        elif name == "speak":
            text = arguments.get("text", "")

            if not text:
                return [TextContent(type="text", text="No text provided.")]

            print(f"Speaking: {text[:50]}...", file=sys.stderr)

            success = await asyncio.to_thread(voice_speak, text)

            if success:
                return [TextContent(type="text", text=f"Spoke: {text[:100]}")]
            else:
                return [TextContent(type="text", text="Failed to speak text")]

        elif name == "start_voice_loop":
            greeting = arguments.get("greeting", MSG_ACTIVATED)

            print("Starting voice loop...", file=sys.stderr)

            await asyncio.to_thread(voice_speak, greeting)

            return [TextContent(
                type="text",
                text="""VOICE_LOOP_MODE_STARTED

RECOMMENDED: Use poll-based API for better UX:
1. listen_start → get session_id (instant)
2. listen_poll → check status (instant)
3. Process command when done
4. speak → respond to user
5. listen_start → next command

EXIT KEYWORDS: parar, sair, exit, quit, stop, tchau"""
            )]

        elif name == "listen_and_respond":
            max_duration = arguments.get("max_duration", 8)

            print(f"[LEGACY] Listening (continuous, {max_duration}s)...", file=sys.stderr)

            try:
                text = await asyncio.to_thread(
                    voice_listen,
                    duration=max_duration,
                    language="pt",
                    use_vad=True
                )

                if text and text.strip():
                    if text.startswith("ERROR:"):
                        return [TextContent(type="text", text=f"VOICE_ERROR: {text}")]

                    if is_exit_command(text):
                        await asyncio.to_thread(voice_speak, MSG_GOODBYE)
                        return [TextContent(type="text", text="EXIT_VOICE_LOOP: User requested exit.")]

                    return [TextContent(type="text", text=f"VOICE_COMMAND: {text}")]
                else:
                    return [TextContent(type="text", text="NO_SPEECH_DETECTED: Call listen_and_respond again.")]

            except Exception as e:
                print(f"Listen error: {e}", file=sys.stderr)
                return [TextContent(type="text", text=f"LISTEN_ERROR: {str(e)}")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    print("=" * 60, file=sys.stderr)
    print("CODEXA Voice Server v3.0", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("NEW: Poll-based API (listen_start, listen_poll, listen_stop)", file=sys.stderr)
    print("LEGACY: Blocking API (listen, speak, listen_and_respond)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
