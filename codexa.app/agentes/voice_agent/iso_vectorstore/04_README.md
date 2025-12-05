<!--
ISO_VECTORSTORE EXPORT
Source: voice_agent/README.md
Synced: 2025-12-05
Version: 7.0.0
-->

# Voice Agent

Accessibility-first voice interface controller for CODEXA. Enables hands-free interaction with Claude Code.

## Quick Start

```bash
# Activate voice mode
/v
```

A beep plays, speak your command, another beep signals end of recording.

## Architecture (v7.0 - Beep-Only)

The Voice Agent uses a **beep-only feedback** system with manual microphone control:

```
┌─────────────────────────────────────────────────────────────┐
│                      /v FLOW (v7.0)                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User types /v                                            │
│         │                                                    │
│         ▼                                                    │
│  2. BEEP (800Hz) - recording starts immediately              │
│         │                                                    │
│         ▼                                                    │
│  3. User speaks freely (15s window, no wake word)            │
│         │                                                    │
│         ▼                                                    │
│  4. BEEP (1200Hz) - recording ended                          │
│         │                                                    │
│         ▼                                                    │
│  5. Whisper transcribes                                      │
│         │                                                    │
│         ▼                                                    │
│  6. Claude interprets as "desire/intent"                     │
│         │                                                    │
│         ├─── Clear? → Execute, speak response                │
│         │                                                    │
│         └─── Unclear? → "Nao entendi. Repita."               │
│                         └─→ Listen again                     │
│                                                              │
│  7. Return to chat (user types /v for next command)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
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
| `server.py` | MCP server for voice commands |
| `stt.py` | Speech-to-Text with beep feedback |
| `tts.py` | Text-to-speech for responses |
| `voice_filter.py` | Noise filter (wake word disabled) |
| `config.py` | Centralized configuration |

## Feedback Signals

| Signal | Meaning |
|--------|---------|
| BEEP 800Hz | Recording started - speak now |
| BEEP 1200Hz | Recording ended - processing |
| BEEP 400Hz | Timeout - no speech detected |

## Configuration

Set in `.env`:

```
WAKE_WORD_ENABLED=false   # No wake word needed in v7.0
STT_LANGUAGE=pt
STT_MAX_DURATION=15
EDGE_VOICE=pt-BR-FranciscaNeural
ELEVENLABS_API_KEY=your_key_here
```

## Usage

### Single Command Mode (v7.0)

```
User: /v
System: BEEP (800Hz)
User: (speaks) "Liste os arquivos"
System: BEEP (1200Hz)
Claude: (runs ls, writes response)
Claude: (TTS) "Encontrei 5 arquivos"
[Control returns to chat]
User: /v
System: BEEP (800Hz)
User: (speaks) "parar"
Claude: (TTS) "Até logo"
```

## Exit Commands

Any of: parar, sair, exit, quit, stop, tchau

## Version

- **Version**: 7.0.0
- **Created**: 2025-11-27
- **Updated**: 2025-11-30
- **Status**: Production
- **Architecture**: Beep-only feedback, single capture per /v
