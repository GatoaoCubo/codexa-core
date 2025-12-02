#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice STT (Speech-to-Text)
=================================

Captures voice and transcribes using ElevenLabs Scribe v1.
Features VAD (Voice Activity Detection) for natural conversation.
"""

import os
import sys
import wave
import tempfile
import struct
import math
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
from config import AUDIO_INPUT_DEVICE, AUDIO_OUTPUT_DEVICE


# =============================================================================
# AUDIO FEEDBACK (BEEPS)
# =============================================================================

def play_beep(frequency=800, duration_ms=150):
    """Play a beep sound for audio feedback."""
    try:
        import sounddevice as sd
        import numpy as np

        sample_rate = 44100
        num_samples = int(sample_rate * duration_ms / 1000)
        t = np.linspace(0, duration_ms / 1000, num_samples, False)

        # Generate sine wave with fade
        beep = 0.3 * np.sin(2 * np.pi * frequency * t)
        fade = int(num_samples * 0.1)
        beep[:fade] *= np.linspace(0, 1, fade)
        beep[-fade:] *= np.linspace(1, 0, fade)

        # Use configured output device
        sd.play(beep.astype(np.float32), sample_rate, device=AUDIO_OUTPUT_DEVICE)
        sd.wait()
    except Exception as e:
        print(f"Beep error: {e}", file=sys.stderr)


def play_start_beep():
    """Play beep indicating recording started."""
    play_beep(frequency=800, duration_ms=150)


def play_end_beep():
    """Play beep indicating recording ended."""
    play_beep(frequency=1200, duration_ms=100)


# =============================================================================
# VAD (Voice Activity Detection)
# =============================================================================

def calculate_rms(audio_chunk):
    """Calculate RMS of audio chunk for volume detection."""
    try:
        import numpy as np
        if isinstance(audio_chunk, bytes):
            audio_chunk = np.frombuffer(audio_chunk, dtype=np.int16)
        return np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2)) / 32767
    except Exception:
        return 0.5


def record_audio_with_vad(
    max_duration=15,
    sample_rate=44100,
    silence_threshold=0.01,
    silence_duration=1.5,
    min_recording=0.5
):
    """
    Records audio with Voice Activity Detection.
    Stops automatically when silence is detected.

    Args:
        max_duration: Maximum recording duration in seconds
        sample_rate: Audio sample rate (Hz)
        silence_threshold: RMS threshold for silence detection
        silence_duration: Seconds of silence before stopping
        min_recording: Minimum recording duration

    Returns:
        Path to temporary audio file
    """
    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy as np

        chunk_duration = 0.1
        chunk_samples = int(sample_rate * chunk_duration)

        print(f"Gravando (max {max_duration}s)...", file=sys.stderr)
        play_start_beep()

        all_audio = []
        silent_chunks = 0
        required_silent_chunks = int(silence_duration / chunk_duration)
        has_speech = False

        for _ in range(int(max_duration / chunk_duration)):
            chunk = sd.rec(chunk_samples, samplerate=sample_rate, channels=1, dtype='int16', device=AUDIO_INPUT_DEVICE)
            sd.wait()
            all_audio.append(chunk)

            rms = calculate_rms(chunk)

            if rms > silence_threshold:
                silent_chunks = 0
                has_speech = True
            else:
                silent_chunks += 1

            total_duration = len(all_audio) * chunk_duration
            if has_speech and silent_chunks >= required_silent_chunks and total_duration >= min_recording:
                print(f"Silencio detectado", file=sys.stderr)
                break

        play_end_beep()

        recording = np.concatenate(all_audio)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()

        sf.write(temp_path, recording, sample_rate)
        return temp_path

    except ImportError:
        return record_audio(duration=max_duration, sample_rate=sample_rate)


def record_audio(duration=5, sample_rate=44100):
    """Records audio for fixed duration."""
    try:
        import sounddevice as sd
        import soundfile as sf

        print(f"Gravando {duration}s...", file=sys.stderr)
        play_start_beep()

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16',
            device=AUDIO_INPUT_DEVICE
        )
        sd.wait()

        play_end_beep()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()

        sf.write(temp_path, recording, sample_rate)
        return temp_path

    except ImportError:
        print("Erro: sounddevice nao instalado", file=sys.stderr)
        return None


# =============================================================================
# TRANSCRIPTION
# =============================================================================

def transcribe_audio(audio_path, language='pt'):
    """
    Transcribes audio using ElevenLabs Scribe v1.

    Args:
        audio_path: Path to audio file
        language: Language code

    Returns:
        Transcribed text or error message starting with "ERROR:"
    """
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        error_msg = f"ERROR: ELEVENLABS_API_KEY not found. Checked .env at: {ENV_PATH}"
        print(error_msg, file=sys.stderr)
        return error_msg

    # Check if audio file exists and has content
    if not os.path.exists(audio_path):
        error_msg = f"ERROR: Audio file not found: {audio_path}"
        print(error_msg, file=sys.stderr)
        return error_msg

    file_size = os.path.getsize(audio_path)
    if file_size < 1000:  # Less than 1KB is probably empty/corrupted
        error_msg = f"ERROR: Audio file too small ({file_size} bytes), microphone may not be working"
        print(error_msg, file=sys.stderr)
        return error_msg

    try:
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(api_key=api_key)
        print(f"Transcribing audio ({file_size} bytes)...", file=sys.stderr)

        with open(audio_path, 'rb') as audio_file:
            response = client.speech_to_text.convert(
                file=audio_file,
                model_id="scribe_v1",
                language_code=language if language else None,
            )

        if hasattr(response, 'text'):
            text = response.text.strip()
        elif isinstance(response, dict) and 'text' in response:
            text = response['text'].strip()
        else:
            text = str(response).strip()

        if text:
            print(f"Transcribed: {text[:50]}...", file=sys.stderr)
        else:
            print("Transcription returned empty (no speech in audio)", file=sys.stderr)

        return text

    except ImportError:
        error_msg = "ERROR: elevenlabs package not installed. Run: pip install elevenlabs"
        print(error_msg, file=sys.stderr)
        return error_msg
    except Exception as e:
        error_msg = f"ERROR: Transcription failed: {e}"
        print(error_msg, file=sys.stderr)
        return error_msg


# =============================================================================
# MAIN API
# =============================================================================

def listen(duration=15, language='pt', use_vad=True):
    """
    Captures and transcribes voice.

    Args:
        duration: Max recording duration
        language: Language code
        use_vad: Use Voice Activity Detection

    Returns:
        Transcribed text
    """
    if use_vad:
        audio_path = record_audio_with_vad(max_duration=duration)
    else:
        audio_path = record_audio(duration=duration)

    if not audio_path:
        return ""

    try:
        return transcribe_audio(audio_path, language=language)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    text = listen()
    print(f"Voce disse: {text}")
