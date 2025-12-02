<!-- iso_vectorstore -->
<!--
  Source: INSTRUCTIONS.md
  Agent: voice_agent
  Synced: 2025-11-30
  Version: 6.0.0
  Package: iso_vectorstore (export package)
-->

# Voice Agent | Instructions v6.0

## Quick Start

```
/v
```

This listens for ONE voice command, executes it, responds via TTS, then returns control.

## How It Works

```
1. /v called
2. Claude says "Pode falar."
3. Claude listens (15s max)
4. User says "codexa liste os arquivos"
5. Claude executes the command
6. Claude speaks response: "5 arquivos encontrados"
7. Control returns to chat
8. User types /v for next command
```

## Wake Words

Say one of these + your command:
- "codexa", "codex", "codigo", "code"
- "ei codexa", "hey codexa", "oi codexa"

Example: "codexa qual a hora"

## Exit Commands

Say any of: parar, sair, exit, quit, stop, tchau

## MCP Tools Used

```python
mcp__voice__speak("text")           # TTS
mcp__voice__listen_start()          # Start recording
mcp__voice__listen_poll(session_id) # Check status
```

## Filter Results

| Result | Meaning |
|--------|---------|
| `VOICE_COMMAND: {text}` | Valid command - execute it |
| `WAKE_WORD_DETECTED` | Just said "codexa" - listen again |
| `NOISE_FILTERED` | Background noise - ignored |
| `AWAITING_WAKE_WORD` | No wake word - ignored |
| `EXIT_VOICE_LOOP` | Exit command |

## Response Guidelines

- Keep TTS responses to 1-2 sentences
- Confirm actions: "Feito", "3 arquivos"
- User cannot see screen - be descriptive

## Configuration

Edit `.env` or `codexa.app/voice/config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `WAKE_WORD_ENABLED` | true | Require wake word |
| `STT_LANGUAGE` | pt | Language code |
| `EDGE_VOICE` | pt-BR-FranciscaNeural | TTS voice |

---

**Version**: 6.0.0
**Updated**: 2025-11-30
**Architecture**: Simple inline polling (one command per /v)
