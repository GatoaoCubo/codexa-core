#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CODEXA Voice STT - Google Speech (free) + ElevenLabs fallback"""

import os
import sys
import tempfile
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from dotenv import load_dotenv
VOICE_ROOT = Path(__file__).parent
PROJECT_ROOT = VOICE_ROOT.parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

from config import AUDIO_INPUT_DEVICE, AUDIO_OUTPUT_DEVICE

def play_beep(frequency=800, duration_ms=150):
    try:
        import sounddevice as sd
        import numpy as np
        sr = 44100
        t = np.linspace(0, duration_ms/1000, int(sr*duration_ms/1000), False)
        beep = 0.3 * np.sin(2*np.pi*frequency*t)
        fade = int(len(beep)*0.1)
        beep[:fade] *= np.linspace(0,1,fade)
        beep[-fade:] *= np.linspace(1,0,fade)
        sd.play(beep.astype(np.float32), sr, device=AUDIO_OUTPUT_DEVICE)
        sd.wait()
    except Exception as e:
        print(f'Beep error: {e}', file=sys.stderr)

def play_start_beep(): play_beep(800, 150)
def play_end_beep(): play_beep(1200, 100)

def calculate_rms(chunk):
    try:
        import numpy as np
        if isinstance(chunk, bytes): chunk = np.frombuffer(chunk, dtype=np.int16)
        return np.sqrt(np.mean(chunk.astype(np.float32)**2)) / 32767
    except: return 0.5

def record_audio_with_vad(max_duration=15, sample_rate=44100, silence_threshold=0.01, silence_duration=1.5, min_recording=0.5):
    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy as np
        chunk_dur = 0.1
        chunk_samples = int(sample_rate * chunk_dur)
        print(f'Gravando (max {max_duration}s)...', file=sys.stderr)
        play_start_beep()
        all_audio = []
        silent_chunks = 0
        required_silent = int(silence_duration / chunk_dur)
        has_speech = False
        for _ in range(int(max_duration / chunk_dur)):
            chunk = sd.rec(chunk_samples, samplerate=sample_rate, channels=1, dtype='int16', device=AUDIO_INPUT_DEVICE)
            sd.wait()
            all_audio.append(chunk)
            rms = calculate_rms(chunk)
            if rms > silence_threshold:
                silent_chunks = 0
                has_speech = True
            else:
                silent_chunks += 1
            if has_speech and silent_chunks >= required_silent and len(all_audio)*chunk_dur >= min_recording:
                print('Silencio detectado', file=sys.stderr)
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
    try:
        import sounddevice as sd
        import soundfile as sf
        print(f'Gravando {duration}s...', file=sys.stderr)
        play_start_beep()
        recording = sd.rec(int(duration*sample_rate), samplerate=sample_rate, channels=1, dtype='int16', device=AUDIO_INPUT_DEVICE)
        sd.wait()
        play_end_beep()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        sf.write(temp_path, recording, sample_rate)
        return temp_path
    except ImportError:
        print('Erro: sounddevice nao instalado', file=sys.stderr)
        return None

def transcribe_with_google(audio_path, language='pt-BR'):
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        lang_map = {'pt': 'pt-BR', 'en': 'en-US', 'es': 'es-ES'}
        lang = lang_map.get(language, language)
        print(f'Transcribing with Google ({lang})...', file=sys.stderr)
        text = recognizer.recognize_google(audio_data, language=lang)
        if text: print(f'Google: {text[:50]}...', file=sys.stderr)
        return text
    except Exception as e:
        print(f'Google error: {e}', file=sys.stderr)
        return None

def transcribe_with_elevenlabs(audio_path, language='pt'):
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print('ElevenLabs: No API key', file=sys.stderr)
        return None
    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)
        file_size = os.path.getsize(audio_path)
        print(f'ElevenLabs: Sending {file_size} bytes, lang={language}', file=sys.stderr)
        with open(audio_path, 'rb') as f:
            response = client.speech_to_text.convert(file=f, model_id='scribe_v1', language_code=language if language else None)
        print(f'ElevenLabs response type: {type(response)}', file=sys.stderr)
        print(f'ElevenLabs response: {response}', file=sys.stderr)
        if hasattr(response, 'text'):
            text = response.text.strip()
            print(f'ElevenLabs text: "{text}"', file=sys.stderr)
            return text if text else None
        elif isinstance(response, dict) and 'text' in response:
            text = response['text'].strip()
            print(f'ElevenLabs dict text: "{text}"', file=sys.stderr)
            return text if text else None
        result = str(response).strip()
        print(f'ElevenLabs str result: "{result}"', file=sys.stderr)
        return result if result else None
    except Exception as e:
        print(f'ElevenLabs error: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return None

def transcribe_audio(audio_path, language='pt'):
    if not os.path.exists(audio_path): return f'ERROR: Audio file not found: {audio_path}'
    file_size = os.path.getsize(audio_path)
    if file_size < 1000: return f'ERROR: Audio file too small ({file_size} bytes)'
    print(f'Transcribing ({file_size} bytes)...', file=sys.stderr)
    # Priority: ElevenLabs Scribe (premium) > Google Speech (free)
    text = transcribe_with_elevenlabs(audio_path, language)
    if text: return text
    text = transcribe_with_google(audio_path, language)
    if text: return text
    return 'ERROR: Transcription failed - no speech detected'

def listen(duration=15, language='pt', use_vad=True):
    audio_path = record_audio_with_vad(max_duration=duration) if use_vad else record_audio(duration=duration)
    if not audio_path: return ''
    try:
        return transcribe_audio(audio_path, language=language)
    finally:
        if os.path.exists(audio_path): os.remove(audio_path)

if __name__ == '__main__':
    text = listen()
    print(f'Voce disse: {text}')
