#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice TTS (Text-to-Speech)
=================================

Robust TTS with automatic fallback chain:
1. Edge TTS (free, online, good quality)
2. ElevenLabs (premium, if API key configured)
3. pyttsx3 (offline, always works)

The system automatically selects the best available option.
"""

import os
import sys
import tempfile
import asyncio
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load environment from project root (not current directory!)
from dotenv import load_dotenv
VOICE_ROOT = Path(__file__).parent
PROJECT_ROOT = VOICE_ROOT.parent.parent  # codexa.gato/
ENV_PATH = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=ENV_PATH)

# Import audio device config (after loading .env)
from config import AUDIO_OUTPUT_DEVICE


# =============================================================================
# AUDIO PLAYBACK (Works in MCP context!)
# =============================================================================

def _play_audio_file(file_path: str) -> bool:
    """
    Play audio file using the best available method.
    Works in MCP subprocess context.
    """
    # Method 1: pygame (most reliable)
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        return True
    except Exception:
        pass

    # Method 2: playsound
    try:
        from playsound import playsound
        playsound(file_path)
        return True
    except Exception:
        pass

    # Method 3: sounddevice + soundfile
    try:
        import sounddevice as sd
        import soundfile as sf
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate, device=AUDIO_OUTPUT_DEVICE)
        sd.wait()
        return True
    except Exception:
        pass

    # Method 4: Windows-specific (fallback)
    if sys.platform == 'win32':
        try:
            import winsound
            winsound.PlaySound(file_path, winsound.SND_FILENAME)
            return True
        except Exception:
            pass

    return False


# =============================================================================
# EDGE TTS (FREE)
# =============================================================================

def speak_edge(text: str, voice: str = "pt-BR-FranciscaNeural", save_to_file: str = None) -> bool:
    """
    Speak using Microsoft Edge TTS (FREE).

    Args:
        text: Text to speak
        voice: Edge TTS voice name
        save_to_file: If specified, saves audio to file

    Returns:
        True if success
    """
    if not text or not text.strip():
        return True

    try:
        import edge_tts

        output_file = save_to_file or tempfile.mktemp(suffix='.mp3')

        async def _generate():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)

        asyncio.run(_generate())

        if not save_to_file:
            success = _play_audio_file(output_file)
            # Cleanup temp file
            try:
                import threading
                def cleanup():
                    import time
                    time.sleep(5)
                    try:
                        os.remove(output_file)
                    except:
                        pass
                threading.Thread(target=cleanup, daemon=True).start()
            except:
                pass
            return success

        return True

    except ImportError:
        print("edge-tts nao instalado", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Erro Edge TTS: {e}", file=sys.stderr)
        return False


# =============================================================================
# ELEVENLABS TTS (PREMIUM)
# =============================================================================

def speak_elevenlabs(text: str, voice_id: str = None, save_to_file: str = None) -> bool:
    """
    Speak using ElevenLabs (premium).

    Args:
        text: Text to speak
        voice_id: ElevenLabs voice ID
        save_to_file: If specified, saves audio to file

    Returns:
        True if success
    """
    if not text or not text.strip():
        return True

    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        return False

    if not voice_id:
        voice_id = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')

    try:
        from elevenlabs import ElevenLabs
        from elevenlabs.play import play

        client = ElevenLabs(api_key=api_key)

        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128"
        )

        if save_to_file:
            with open(save_to_file, 'wb') as f:
                for chunk in audio:
                    if isinstance(chunk, bytes):
                        f.write(chunk)
            return True

        # Try to play directly
        try:
            play(audio)
            return True
        except Exception:
            # Save to temp file and play
            temp_file = tempfile.mktemp(suffix='.mp3')
            # Regenerate audio (iterator was consumed)
            audio = client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128"
            )
            with open(temp_file, 'wb') as f:
                for chunk in audio:
                    if isinstance(chunk, bytes):
                        f.write(chunk)
            success = _play_audio_file(temp_file)
            try:
                os.remove(temp_file)
            except:
                pass
            return success

    except ImportError:
        print("elevenlabs nao instalado", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Erro ElevenLabs: {e}", file=sys.stderr)
        return False


# =============================================================================
# PYTTSX3 TTS (OFFLINE)
# =============================================================================

def speak_pyttsx3(text: str) -> bool:
    """
    Speak using pyttsx3 (offline, always works).

    Args:
        text: Text to speak

    Returns:
        True if success
    """
    if not text or not text.strip():
        return True

    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"Erro pyttsx3: {e}", file=sys.stderr)
        return False


# =============================================================================
# MAIN API - AUTOMATIC FALLBACK
# =============================================================================

def speak(
    text: str,
    voice_id: str = None,
    save_to_file: str = None,
    provider: str = 'auto'
) -> bool:
    """
    Speak text using the best available TTS provider.

    Fallback chain (auto mode):
    1. Edge TTS (FREE, online, good quality) - always works if internet available
    2. ElevenLabs (PREMIUM, requires ELEVENLABS_API_KEY in .env)
    3. pyttsx3 (FREE, offline, basic quality) - always works

    Args:
        text: Text to speak
        voice_id: Voice ID (for ElevenLabs)
        save_to_file: If specified, saves audio to file
        provider: 'auto', 'edge', 'elevenlabs', or 'pyttsx3'

    Returns:
        True if success

    Example:
        # Auto-select best available (recommended)
        speak("Hello world")

        # Force specific provider
        speak("Hello world", provider='pyttsx3')

        # Save to file
        speak("Hello world", save_to_file='output.mp3')
    """
    if not text or not text.strip():
        return True

    # If specific provider requested
    if provider == 'edge':
        return speak_edge(text, save_to_file=save_to_file)
    elif provider == 'elevenlabs':
        return speak_elevenlabs(text, voice_id=voice_id, save_to_file=save_to_file)
    elif provider == 'pyttsx3':
        return speak_pyttsx3(text)

    # Auto mode: try each provider in order
    # Edge TTS first (free, good quality)
    # ElevenLabs second (premium, only if configured)
    # pyttsx3 last (offline fallback, always works)
    providers = [
        ('edge', lambda: speak_edge(text, save_to_file=save_to_file)),
        ('elevenlabs', lambda: speak_elevenlabs(text, voice_id=voice_id, save_to_file=save_to_file)),
        ('pyttsx3', lambda: speak_pyttsx3(text)),
    ]

    for name, func in providers:
        try:
            result = func()
            if result:
                print(f"TTS provider: {name}", file=sys.stderr)
                return True
        except Exception as e:
            print(f"{name} falhou: {e}", file=sys.stderr)
            continue

    print("ERRO: Todos os providers TTS falharam", file=sys.stderr)
    return False


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Ola! Sistema de voz funcionando."
    success = speak(text)
    print(f"Resultado: {'Sucesso' if success else 'Falha'}")
