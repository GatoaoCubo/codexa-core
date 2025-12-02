# Voice Agent | Setup Guide

## Prerequisites

### Python Packages

```bash
pip install sounddevice soundfile numpy elevenlabs edge-tts pyttsx3
```

### API Keys

Add to `.env` in project root:

```
ELEVENLABS_API_KEY=your_key_here
```

Get key from: https://elevenlabs.io/

### Audio Devices

Check available devices:
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

Set specific devices (optional):
```
AUDIO_INPUT_DEVICE=1
AUDIO_OUTPUT_DEVICE=2
```

## Installation Verification

### 1. Test STT
```bash
python -c "from voice.stt import listen; print(listen(duration=3))"
```
Expected: Speak, see transcribed text

### 2. Test TTS
```bash
python -c "from voice.tts import speak; speak('Olá, teste de voz')"
```
Expected: Hear "Olá, teste de voz"

### 3. Test VAD
```bash
python -c "from voice.stt import listen; print(listen(use_vad=True))"
```
Expected: Recording stops when you stop talking

### 4. Test MCP Server
```bash
python voice/server.py
```
Expected: "CODEXA Voice Server v2.0 starting..."

## Configuration

### Minimal (.env)
```
ELEVENLABS_API_KEY=sk-xxx
```

### Full (.env)
```
# API
ELEVENLABS_API_KEY=sk-xxx
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Audio
AUDIO_INPUT_DEVICE=
AUDIO_OUTPUT_DEVICE=

# STT
STT_LANGUAGE=pt
STT_MAX_DURATION=15.0

# TTS
TTS_MAX_RESPONSE_DURATION=30.0
TTS_FALLBACK_OFFLINE=true

# VAD
VAD_SILENCE_THRESHOLD=1.5
VAD_MAX_DURATION=15.0
VAD_ENERGY_THRESHOLD=0.02

# User
IRONMAN_USER_NAME=Gato
IRONMAN_GREETING=Sim?
```

## Claude Code Integration

### MCP Server Config

In `.claude/settings.json`:
```json
{
  "mcpServers": {
    "voice": {
      "command": "python",
      "args": ["voice/server.py"],
      "cwd": "."
    }
  }
}
```

### Verify Integration

In Claude Code:
```
/voice
```

Expected: "Modo contínuo ativado. Pode falar!"

## Troubleshooting

### "No module named 'sounddevice'"
```bash
pip install sounddevice
```

### "No module named 'elevenlabs'"
```bash
pip install elevenlabs
```

### "ELEVENLABS_API_KEY not found"
Add to `.env`:
```
ELEVENLABS_API_KEY=your_key_here
```

### "No audio input device"
1. Check microphone connected
2. Grant permissions in OS settings
3. Set device manually: `AUDIO_INPUT_DEVICE=0`

### "TTS fails silently"
1. Check API key valid
2. Check internet connection
3. Try Edge TTS: `from voice.tts import speak_edge; speak_edge("test")`

### "VAD doesn't stop"
Increase silence threshold:
```
VAD_SILENCE_THRESHOLD=2.0
```

## Platform Notes

### Windows
- Use Python 3.10+
- May need Visual C++ redistributable for sounddevice
- Microphone permissions in Settings > Privacy

### macOS
- Grant Terminal/IDE microphone permission
- System Preferences > Security & Privacy > Microphone

### Linux
- Install PortAudio: `sudo apt install portaudio19-dev`
- May need to be in `audio` group

---

**Version**: 1.0.0
**Updated**: 2025-11-27
