#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice System - Unified Voice Interface
==============================================

Accessibility-first voice system for users who cannot type.
Designed for minimal setup and maximum reliability.

Quick Start:
    /v                  # Start voice mode (2 chars!)
    python -m codexa.app.voice.setup  # First-time setup

Features:
    - STT (Speech-to-Text) with VAD
    - TTS (Text-to-Speech) with fallback chain
    - MCP Server for Claude Code integration
    - Setup wizard with voice instructions

TTS Fallback Chain:
    1. Edge TTS (free, online, good quality)
    2. ElevenLabs (premium, if API key configured)
    3. pyttsx3 (offline, always works)
"""

__version__ = '2.0.0'
__author__ = 'CODEXA'

# Exports
from .stt import listen, transcribe_audio, record_audio_with_vad
from .tts import speak, speak_edge, speak_elevenlabs

__all__ = [
    # STT
    'listen',
    'transcribe_audio',
    'record_audio_with_vad',
    # TTS
    'speak',
    'speak_edge',
    'speak_elevenlabs',
]
