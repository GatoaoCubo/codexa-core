# Voice System Setup Guide

## Requirements

- Python 3.10+
- Working microphone
- Internet connection (for ElevenLabs STT and Edge TTS)

## Installation

```bash
# Install dependencies
pip install -r codexa.app/voice/requirements.txt
```

## Dependencies

| Package | Purpose |
|---------|---------|
| sounddevice | Audio recording |
| soundfile | Audio file handling |
| numpy | Audio processing |
| edge-tts | Free TTS (Microsoft Edge) |
| elevenlabs | Premium STT/TTS |
| pygame | Audio playback |
| python-dotenv | Environment variables |
| mcp | Claude Code integration |

## Configuration

### 1. Set API Key

Add to `.env` in project root:

```env
ELEVENLABS_API_KEY=sk_your_key_here
```

Get your key at: https://elevenlabs.io/

### 2. MCP Configuration

Already configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "voice": {
      "type": "stdio",
      "command": "py",
      "args": ["-3.12", "codexa.app/voice/server.py"],
      "env": {
        "PYTHONPATH": "...",
        "ELEVENLABS_API_KEY": "..."
      }
    }
  }
}
```

### 3. Test Setup

```bash
# Test audio devices
python -c "from codexa.app.voice.lib.device_manager import AudioDeviceManager; m = AudioDeviceManager(); m.print_devices()"

# Test TTS
python -c "from codexa.app.voice.tts import speak; speak('Teste de voz')"

# Test STT
python -c "from codexa.app.voice.stt import listen; print(listen())"
```

## Troubleshooting

### Microphone not detected

1. Check system sound settings
2. Grant terminal/Python microphone permissions
3. Try different audio device:
   ```bash
   set AUDIO_INPUT_DEVICE=1
   ```

### ElevenLabs errors

1. Verify API key is correct
2. Check API quota at elevenlabs.io
3. Check internet connection

### Edge TTS errors

1. Check internet connection
2. Falls back to pyttsx3 automatically

## Voice Mode Commands

Use `/v` in Claude Code to start voice mode.

Exit by saying: "parar", "sair", or "exit"
