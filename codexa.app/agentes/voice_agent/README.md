# Voice Agent

Accessibility-first voice interface controller for CODEXA. Enables hands-free interaction with Claude Code.

## Quick Start

```bash
# Activate voice mode
/v
```

That's it. The daemon starts in background and you can speak commands.

## Architecture (v3.0)

The Voice Agent uses a **background daemon** architecture:

```
Voice Daemon (Background) <---> Files (IPC) <---> Claude Code (Main)
     |                              |                    |
     v                              v                    v
  Listen                    command.txt              Poll
  Transcribe                response.txt             Process
  Speak                     status.txt               Respond
```

## Structure

```
voice_agent/
├── PRIME.md              # Agent context and instructions
├── README.md             # This file
├── INSTRUCTIONS.md       # Operational details
├── SETUP.md              # Installation guide
├── config/
│   └── 51_voice_agent.json   # Agent configuration
└── prompts/
    └── 01_voice_interaction_HOP.md  # Voice interaction HOP
```

## Core Files (in codexa.app/voice/)

| File | Purpose |
|------|---------|
| `voice_daemon.py` | Background daemon for continuous listening |
| `stt.py` | Speech-to-Text with VAD |
| `tts.py` | TTS router (Edge > ElevenLabs > pyttsx3) |
| `config.py` | Centralized configuration |
| `server.py` | MCP server (alternative) |

## IPC Files (Temp Directory)

| File | Purpose |
|------|---------|
| `codexa_voice_command.txt` | Voice commands from daemon |
| `codexa_voice_response.txt` | Responses for daemon to speak |
| `codexa_voice_status.txt` | Daemon status |

## Configuration

Set in `.env`:

```
ELEVENLABS_API_KEY=your_key_here
STT_LANGUAGE=pt
VAD_SILENCE_THRESHOLD=1.5
EDGE_VOICE=pt-BR-FranciscaNeural
```

## Usage

### Continuous Mode

```
User: /v
Daemon: "Modo voz ativado. Pode falar!"
User: (speaks) "Liste os arquivos"
Claude: (runs ls, writes response)
Daemon: "Encontrei 5 arquivos"
User: (speaks) "parar"
Daemon: "Até logo!"
```

### Daemon Commands

```bash
# Start daemon manually
py -3.12 codexa.app/voice/voice_daemon.py start

# Stop daemon
py -3.12 codexa.app/voice/voice_daemon.py stop

# Check status
py -3.12 codexa.app/voice/voice_daemon.py status
```

## Exit Commands

Any of: parar, sair, exit, quit, stop, encerrar, tchau

## Version

- **Version**: 3.0.0
- **Created**: 2025-11-27
- **Updated**: 2025-11-28
- **Status**: Production
- **Architecture**: Background daemon with file-based IPC
