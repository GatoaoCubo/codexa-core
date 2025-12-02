<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: voice_agent
  Synced: 2025-11-30
  Version: 6.0.0
  Package: iso_vectorstore (export package)
-->

# Voice Agent | PRIME

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

## PURPOSE

**VOICE_AGENT**: Accessibility-first voice interface for CODEXA. Enables hands-free interaction with Claude Code.

**Provides**: Voice-to-text | Text-to-speech | Wake word detection | Noise filtering

**Philosophy**: Simple, reliable, one command at a time.

**Activation**: `/v`

## ARCHITECTURE (v6.0 - Simplified)

```
┌─────────────────────────────────────────────────────────────┐
│                         /v FLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User types /v                                            │
│         │                                                    │
│         ▼                                                    │
│  2. Claude: mcp__voice__speak("Pode falar.")                │
│         │                                                    │
│         ▼                                                    │
│  3. Claude: mcp__voice__listen_start()                      │
│         │                                                    │
│         ▼                                                    │
│  4. Claude polls: mcp__voice__listen_poll()                 │
│         │                                                    │
│         ▼                                                    │
│  5. User says: "codexa liste arquivos"                      │
│         │                                                    │
│         ▼                                                    │
│  6. Filter: wake word detected? noise? valid command?       │
│         │                                                    │
│         ▼                                                    │
│  7. Claude executes command                                  │
│         │                                                    │
│         ▼                                                    │
│  8. Claude: mcp__voice__speak("5 arquivos encontrados")     │
│         │                                                    │
│         ▼                                                    │
│  9. Control returns to chat                                  │
│         │                                                    │
│         ▼                                                    │
│  10. User types /v for next command                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## KEY FILES

| File | Purpose |
|------|---------|
| `.claude/commands/v.md` | /v command definition |
| `codexa.app/voice/server.py` | MCP server |
| `codexa.app/voice/stt.py` | Speech-to-text |
| `codexa.app/voice/tts.py` | Text-to-speech |
| `codexa.app/voice/voice_filter.py` | Wake word + noise filter |
| `codexa.app/voice/config.py` | Configuration |

## INSTRUCTIONS FOR AI

### When /v is called:

1. **Speak greeting**: `mcp__voice__speak("Pode falar.")`
2. **Start listening**: `mcp__voice__listen_start(max_duration=15, initial_timeout=5)`
3. **Poll until done**: Keep calling `mcp__voice__listen_poll(session_id)`
4. **Handle result**:
   - `VOICE_COMMAND: {text}` → Execute, speak response
   - `NOISE_FILTERED` → Speak "Nao entendi"
   - `EXIT_VOICE_LOOP` → Speak "Ate logo", stop
   - Timeout → Say "Use /v para tentar novamente"
5. **Return to chat**

### Response Rules

- Keep TTS to 1-2 sentences
- Confirm actions: "Feito", "3 arquivos"
- User cannot see screen - be descriptive

## WAKE WORDS

- "codexa", "codex", "codigo", "code"
- "ei codexa", "hey codexa", "oi codexa"

## EXIT COMMANDS

parar, sair, exit, quit, stop, tchau

## CONFIGURATION

```bash
# In .env
WAKE_WORD_ENABLED=true
STT_LANGUAGE=pt
EDGE_VOICE=pt-BR-FranciscaNeural
```

---

**Version**: 6.0.0
**Created**: 2025-11-27
**Updated**: 2025-11-30
**Agent Type**: Voice Interface
**Architecture**: Simple inline polling
**Dependencies**: sounddevice, edge-tts, ElevenLabs API (optional)
