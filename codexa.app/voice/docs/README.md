# CODEXA Voice System Documentation

## Quick Start

```bash
# Activate voice mode in Claude Code
/v
```

## Architecture

```
codexa.app/voice/
├── server.py       # MCP Server (main entry point)
├── stt.py          # Speech-to-Text with VAD
├── tts.py          # Text-to-Speech with fallback
├── config.py       # Configuration
├── lib/            # Advanced modules
│   ├── summarizer.py     # Response summarization for TTS
│   └── device_manager.py # Audio device management
└── docs/           # Documentation (you are here)
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `listen` | Capture and transcribe voice |
| `speak` | Text-to-speech output |
| `start_voice_loop` | Begin continuous mode |
| `listen_and_respond` | VAD-based listening loop |

## TTS Fallback Chain

1. **Edge TTS** (free, online) - Default
2. **ElevenLabs** (premium, if API key set)
3. **pyttsx3** (offline fallback)

## Configuration

Environment variables (in `.env`):

```env
ELEVENLABS_API_KEY=sk_...  # Required for STT transcription
EDGE_VOICE=pt-BR-FranciscaNeural  # TTS voice
STT_LANGUAGE=pt  # Transcription language
```

## Troubleshooting

### "No speech detected"
1. Check microphone is connected
2. Check ELEVENLABS_API_KEY is set
3. Run device test: `python -m codexa.app.voice.lib.device_manager`

### TTS not working
1. Check internet connection (Edge TTS needs internet)
2. Falls back to pyttsx3 automatically

## Exit Commands

Say any of these to exit voice mode:
- parar, sair, exit, quit, stop
- encerrar, tchau, pare, finalizar
