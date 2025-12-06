#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Configuration
==========================

Centralized configuration with auto-detection and sensible defaults.
All settings can be overridden via environment variables.
"""

import os
from pathlib import Path

# =============================================================================
# PATHS
# =============================================================================

VOICE_ROOT = Path(__file__).parent
PROJECT_ROOT = VOICE_ROOT.parent.parent  # codexa.gato/
CONFIG_DIR = VOICE_ROOT / 'config'
SETUP_DIR = VOICE_ROOT / 'setup'

# Load environment variables
from dotenv import load_dotenv
ENV_PATH = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=ENV_PATH)

# =============================================================================
# HELPER
# =============================================================================

def _env(key: str, default, cast=str):
    """Load value from environment with type casting."""
    value = os.getenv(key)
    if value is None:
        return default
    if cast == bool:
        return value.lower() in ('true', '1', 'yes', 'on')
    return cast(value)


# =============================================================================
# USER SETTINGS
# =============================================================================

USER_NAME = _env('CODEXA_USER_NAME', 'Usuario')
LANGUAGE = _env('CODEXA_LANGUAGE', 'pt')

# =============================================================================
# TTS (Text-to-Speech)
# =============================================================================

# Provider priority: edge > elevenlabs > pyttsx3
TTS_PROVIDER = _env('TTS_PROVIDER', 'auto')  # auto, edge, elevenlabs, pyttsx3

# ElevenLabs (optional - premium)
ELEVENLABS_API_KEY = _env('ELEVENLABS_API_KEY', None)
ELEVENLABS_VOICE_ID = _env('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')

# Edge TTS (free)
EDGE_VOICE = _env('EDGE_VOICE', 'pt-BR-FranciscaNeural')

# =============================================================================
# STT (Speech-to-Text)
# =============================================================================

STT_LANGUAGE = _env('STT_LANGUAGE', 'pt')
STT_MAX_DURATION = _env('STT_MAX_DURATION', 15.0, float)

# =============================================================================
# AUDIO DEVICES
# =============================================================================

# Device indices (use sounddevice.query_devices() to list)
# Leave empty/None for system default
def _env_int_or_none(key: str):
    """Load optional integer from environment."""
    value = os.getenv(key)
    if value is None or value.strip() == '':
        return None
    try:
        return int(value)
    except ValueError:
        return None

# Use system default input device (None = auto-detect)
_default_input = None  # Let sounddevice pick the best available device
AUDIO_INPUT_DEVICE = _env_int_or_none('AUDIO_INPUT_DEVICE')
if AUDIO_INPUT_DEVICE is None:
    AUDIO_INPUT_DEVICE = _default_input
AUDIO_OUTPUT_DEVICE = _env_int_or_none('AUDIO_OUTPUT_DEVICE')

# =============================================================================
# VAD (Voice Activity Detection)
# =============================================================================

VAD_SILENCE_THRESHOLD = _env('VAD_SILENCE_THRESHOLD', 2.0, float)  # v10.1: 1.5→2.0 (menos cortes)
VAD_MAX_DURATION = _env('VAD_MAX_DURATION', 15.0, float)
VAD_MIN_SPEECH = _env('VAD_MIN_SPEECH', 0.3, float)
VAD_ENERGY_THRESHOLD = _env('VAD_ENERGY_THRESHOLD', 0.03, float)  # v10.2: 0.02→0.03 (ignora ruído leve)

# =============================================================================
# UX TIMING
# =============================================================================

# Delay after TTS before starting recording (avoids mic capturing TTS playback)
TTS_TO_RECORD_DELAY = _env('TTS_TO_RECORD_DELAY', 1.5, float)  # v10.1: 1.5s delay

# =============================================================================
# VOICE FILTER (Wake Word & Noise Gate)
# =============================================================================

# Wake word settings
WAKE_WORD_ENABLED = _env('WAKE_WORD_ENABLED', False, bool)  # v7.0: disabled, 15s window
WAKE_WORDS = _env('WAKE_WORDS', 'codexa,codex,codigo,codesa,code,ei codexa,ei codex,ei codigo,hey codexa,oi codexa')
WAKE_WORD_TIMEOUT = _env('WAKE_WORD_TIMEOUT', 30.0, float)

# Noise gate settings
NOISE_GATE_ENABLED = _env('NOISE_GATE_ENABLED', True, bool)
MIN_ENERGY_THRESHOLD = _env('MIN_ENERGY_THRESHOLD', 0.025, float)
MIN_COMMAND_WORDS = _env('MIN_COMMAND_WORDS', 1, int)

# Voice session settings
VOICE_INITIAL_TIMEOUT = _env('VOICE_INITIAL_TIMEOUT', 3.0, float)
VOICE_SILENCE_DURATION = _env('VOICE_SILENCE_DURATION', 2.0, float)  # v10.1: 1.2→2.0 (pausas naturais)
VOICE_SILENCE_THRESHOLD = _env('VOICE_SILENCE_THRESHOLD', 0.02, float)  # Increased

# =============================================================================
# VOICE COMMANDS
# =============================================================================

EXIT_COMMANDS = [
    'parar', 'sair', 'exit', 'quit', 'stop',
    'encerrar', 'tchau', 'pare', 'finalizar'
]

# =============================================================================
# MESSAGES
# =============================================================================

MSG_ACTIVATED = _env('MSG_ACTIVATED', 'Modo voz ativado. Pode falar.')
MSG_LISTENING = _env('MSG_LISTENING', 'Ouvindo...')
MSG_GOODBYE = _env('MSG_GOODBYE', 'Ate logo!')
MSG_ERROR = _env('MSG_ERROR', 'Erro. Tentando novamente.')
MSG_RETRY = _env('MSG_RETRY', 'Nao entendi. Repita por favor.')

# =============================================================================
# HELPERS
# =============================================================================

def is_elevenlabs_available() -> bool:
    """Check if ElevenLabs API key is configured."""
    return bool(ELEVENLABS_API_KEY)


def get_tts_provider() -> str:
    """Get the best available TTS provider."""
    if TTS_PROVIDER != 'auto':
        return TTS_PROVIDER

    # Auto-detect: prefer Edge (free), use ElevenLabs if configured
    return 'edge'


def is_exit_command(text: str) -> bool:
    """Check if text contains an exit command."""
    text_lower = text.lower().strip()
    return any(cmd in text_lower for cmd in EXIT_COMMANDS)


def get_wake_words_list() -> list:
    """Get wake words as a list."""
    if isinstance(WAKE_WORDS, str):
        return [w.strip() for w in WAKE_WORDS.split(',')]
    return list(WAKE_WORDS)


def print_config():
    """Print current configuration."""
    print("=" * 50)
    print("CODEXA Voice Config v3.0")
    print("=" * 50)
    print(f"User: {USER_NAME}")
    print(f"Language: {LANGUAGE}")
    print(f"TTS Provider: {get_tts_provider()}")
    print(f"ElevenLabs: {'Configured' if is_elevenlabs_available() else 'Not configured'}")
    print(f"Edge Voice: {EDGE_VOICE}")
    print("-" * 50)
    print(f"Wake Word: {'ON' if WAKE_WORD_ENABLED else 'OFF'}")
    if WAKE_WORD_ENABLED:
        print(f"Wake Words: {get_wake_words_list()}")
    print(f"Noise Gate: {'ON' if NOISE_GATE_ENABLED else 'OFF'}")
    print(f"Energy Threshold: {MIN_ENERGY_THRESHOLD}")
    print("=" * 50)


if __name__ == "__main__":
    print_config()
