#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Setup Wizard
=========================

Interactive setup with voice instructions.
Designed for accessibility users who cannot see the screen.

Usage:
    python -m codexa.app.voice.setup
    python wizard.py
"""

import os
import sys
import time
from pathlib import Path

# Add project to path
VOICE_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = VOICE_ROOT.parent.parent  # codexa.gato/
sys.path.insert(0, str(PROJECT_ROOT))

# Try to import TTS (might not be installed yet)
TTS_AVAILABLE = False
try:
    from codexa.app.voice.tts import speak_edge, speak_pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pass


def say(text: str, also_print: bool = True):
    """Speak and optionally print text."""
    if also_print:
        print(text)

    if TTS_AVAILABLE:
        try:
            # Try Edge TTS first (free)
            if not speak_edge(text):
                speak_pyttsx3(text)
        except Exception:
            pass


def check_dependencies() -> dict:
    """Check which dependencies are installed."""
    deps = {
        'sounddevice': False,
        'soundfile': False,
        'edge_tts': False,
        'elevenlabs': False,
        'pyttsx3': False,
        'numpy': False,
        'pygame': False,
        'dotenv': False,
        'mcp': False,
    }

    for dep in deps:
        try:
            __import__(dep.replace('_', '-').replace('edge-tts', 'edge_tts'))
            deps[dep] = True
        except ImportError:
            pass

    return deps


def test_microphone() -> bool:
    """Test if microphone is working."""
    try:
        import sounddevice as sd
        import numpy as np

        print("\nTestando microfone...")
        duration = 2
        sample_rate = 44100

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()

        # Check if we got audio
        rms = np.sqrt(np.mean(recording.astype(np.float32) ** 2)) / 32767
        return rms > 0.001

    except Exception as e:
        print(f"Erro no microfone: {e}")
        return False


def test_speaker() -> bool:
    """Test if speaker is working."""
    try:
        import sounddevice as sd
        import numpy as np

        print("\nTestando alto-falante...")

        # Generate beep
        sample_rate = 44100
        duration = 0.3
        freq = 800
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        beep = 0.3 * np.sin(2 * np.pi * freq * t)

        sd.play(beep.astype(np.float32), sample_rate)
        sd.wait()

        return True

    except Exception as e:
        print(f"Erro no alto-falante: {e}")
        return False


def create_env_file():
    """Create .env file if not exists."""
    env_path = PROJECT_ROOT / '.env'

    if env_path.exists():
        print("\n.env ja existe")
        return True

    content = """# CODEXA Voice Configuration
# ==========================

# Your name (optional)
CODEXA_USER_NAME=Usuario

# Language for STT
CODEXA_LANGUAGE=pt
STT_LANGUAGE=pt

# ElevenLabs API Key (optional - for premium TTS)
# Get your key at: https://elevenlabs.io
# ELEVENLABS_API_KEY=your_key_here

# TTS Provider: auto, edge, elevenlabs, pyttsx3
TTS_PROVIDER=auto

# Edge TTS Voice
EDGE_VOICE=pt-BR-FranciscaNeural
"""

    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n.env criado em: {env_path}")
        return True
    except Exception as e:
        print(f"Erro ao criar .env: {e}")
        return False


def print_missing_deps(deps: dict):
    """Print installation command for missing dependencies."""
    missing = [name for name, installed in deps.items() if not installed]

    if not missing:
        return

    print("\n" + "=" * 50)
    print("DEPENDENCIAS FALTANDO")
    print("=" * 50)
    print("\nExecute este comando para instalar:")
    print()
    print(f"pip install {' '.join(missing)}")
    print()


def run_setup():
    """Run the setup wizard."""
    print()
    print("=" * 50)
    print("  CODEXA VOICE SETUP")
    print("  Configuracao do Sistema de Voz")
    print("=" * 50)
    print()

    # Say welcome if TTS available
    if TTS_AVAILABLE:
        say("Ola! Vou configurar o sistema de voz.")
        time.sleep(0.5)

    # Step 1: Check dependencies
    print("\n[1/4] Verificando dependencias...")
    deps = check_dependencies()

    installed = sum(1 for v in deps.values() if v)
    total = len(deps)
    print(f"Dependencias: {installed}/{total} instaladas")

    # Critical dependencies
    critical = ['sounddevice', 'soundfile', 'numpy', 'dotenv']
    critical_missing = [d for d in critical if not deps[d]]

    if critical_missing:
        print(f"\nFaltando dependencias criticas: {', '.join(critical_missing)}")
        print_missing_deps(deps)

        if TTS_AVAILABLE:
            say("Algumas dependencias estao faltando. Veja as instrucoes na tela.")
        return False

    # Step 2: Test microphone
    print("\n[2/4] Testando microfone...")
    if TTS_AVAILABLE:
        say("Testando seu microfone. Aguarde.")

    mic_ok = test_microphone()

    if mic_ok:
        print("Microfone: OK")
        if TTS_AVAILABLE:
            say("Microfone funcionando.")
    else:
        print("Microfone: FALHOU")
        if TTS_AVAILABLE:
            say("Microfone nao detectado. Verifique a conexao.")
        # Continue anyway - might work later

    # Step 3: Test speaker
    print("\n[3/4] Testando alto-falante...")
    if TTS_AVAILABLE:
        say("Voce deve ouvir um bipe agora.")

    speaker_ok = test_speaker()

    if speaker_ok:
        print("Alto-falante: OK")
    else:
        print("Alto-falante: FALHOU")

    # Step 4: Create .env
    print("\n[4/4] Criando arquivo de configuracao...")
    create_env_file()

    # Summary
    print()
    print("=" * 50)
    print("  SETUP COMPLETO!")
    print("=" * 50)
    print()
    print("Para usar o modo voz:")
    print("  1. Abra o Claude Code")
    print("  2. Digite: /v")
    print("  3. Fale seus comandos!")
    print()
    print("Comandos de saida: parar, sair, exit, tchau")
    print()

    if TTS_AVAILABLE:
        say("Configuracao completa! Digite barra v para comecar.")

    # Print any missing optional deps
    if not all(deps.values()):
        print_missing_deps(deps)

    return True


if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)
