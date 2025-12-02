# Voice Agent | Quick Start

## Overview
Voice Agent handles voice input/output for CODEXA - enabling hands-free interaction with all agents through speech recognition and text-to-speech.

## Quick Commands

```bash
# Start voice mode
/prime-voice

# Listen for voice input
mcp__voice__listen_start()

# Poll for result
mcp__voice__listen_poll(session_id)

# Speak response
mcp__voice__speak("Hello!")
```

## File Structure

```
voice_agent/
├── PRIME.md                  # Agent philosophy
├── INSTRUCTIONS.md           # Usage guide
├── README.md                 # Quick reference
├── SETUP.md                  # Installation
├── ANALYSIS_AND_PLAN.md      # Development notes
├── config/
│   └── 51_voice_agent.json   # Voice configuration
└── prompts/
    └── 01_voice_interaction_HOP.md  # Voice interaction HOP
```

## Key Features

1. **Voice Recognition** - Speech to text transcription
2. **Text-to-Speech** - Natural voice responses
3. **Session Management** - Non-blocking voice capture
4. **Multi-Language** - Portuguese (BR) + English support

## MCP Tools

| Tool | Purpose |
|------|---------|
| `listen_start()` | Start voice recording (non-blocking) |
| `listen_poll(id)` | Check recording status |
| `listen_stop(id)` | Cancel recording |
| `speak(text)` | TTS output |
| `start_voice_loop()` | Continuous mode |

## Next Steps

1. Read `02_PRIME.md` for voice architecture
2. Read `03_INSTRUCTIONS.md` for integration patterns
3. Check `config/` for voice settings

---

**Version**: 1.0.0 | **Updated**: 2025-11-30
