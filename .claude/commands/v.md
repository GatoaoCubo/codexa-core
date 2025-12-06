# /v - Voice Mode v8.0 (Boot + Simplified UX)

Single voice capture with beep feedback. Auto-installs dependencies on first run.

## BOOT SEQUENCE (Run First)

**Before calling voice tools, verify MCP is ready:**

```python
# Step 1: Check if voice tools are available
IF mcp__voice__listen_start NOT available:
    # Boot sequence needed
    RUN boot_voice()
    RETURN "Voice MCP reiniciando. Execute /v novamente."

# Step 2: Voice tools available - proceed to FLOW
```

### boot_voice() Implementation

```bash
# Check and install dependencies
pip show mcp sounddevice soundfile numpy edge-tts pyttsx3 pygame faster-whisper python-dotenv webrtcvad-wheels 2>&1 | grep -q "not found"

IF any missing:
    pip install -r codexa.app/voice/requirements.txt
    pip install webrtcvad-wheels  # Windows-compatible wheel
    pip install mcp

# Verify voice server can start
python codexa.app/voice/server.py --check

# If all good, inform user to restart Claude Code
RETURN "Dependencias instaladas. Reinicie o Claude Code para ativar voice MCP."
```

### Quick Boot Commands (for manual execution)

```bash
# Install all voice dependencies
pip install mcp sounddevice soundfile numpy edge-tts pyttsx3 pygame faster-whisper python-dotenv webrtcvad-wheels

# Test voice server
python codexa.app/voice/server.py --check

# If MCP still not available, restart Claude Code
```

---

## FLOW (After Boot)

```
1. /v is called
2. Check if mcp__voice__ tools available
   - NO: Run boot sequence, ask user to restart
   - YES: Continue
3. BEEP plays (recording starts immediately after beep)
4. User has 15s window to speak anything
5. Whisper transcribes
6. Claude interprets as "desire/intent"
7. If unclear -> speak "Nao entendi. Repita."
8. If clear -> execute and speak short response
9. Return to chat (user types /v for next command)
```

## IMPLEMENTATION

```python
# BOOT CHECK
IF mcp__voice__listen_start NOT in available_tools:
    # Run installation
    Bash("pip install mcp sounddevice soundfile numpy edge-tts pyttsx3 pygame faster-whisper python-dotenv webrtcvad-wheels --quiet")
    Bash("python codexa.app/voice/server.py --check")
    RETURN "Voice dependencies installed. Restart Claude Code to activate."

# NO TTS greeting - just start listening
session = listen_start(max_duration=15, initial_timeout=5)

# Poll until done
WHILE polling:
    result = listen_poll(session_id)

    IF result.status == "done":
        BREAK
    IF result.status in ["timeout", "error"]:
        # No speech - exit silently, user can type /v again
        RETURN "Use /v para tentar novamente"

    # Keep polling
    WAIT ~500ms

# PROCESS RESULT
IF result starts with "VOICE_COMMAND:":
    command = extract_command(result)

    # Check exit
    IF is_exit_command(command):
        speak("Ate logo")
        RETURN

    # Execute user's intent
    execute(command)
    speak(short_response)  # "Feito", "3 arquivos", etc

ELIF result starts with "NOISE_FILTERED:" or "INVALID_COMMAND:":
    # Couldn't understand - ask to repeat
    speak("Nao entendi. Repita.")
    # Start new listen immediately
    session = listen_start(...)
    # Continue polling...

ELIF result starts with "EXIT_VOICE_LOOP:":
    speak("Ate logo")
    RETURN

ELSE:
    # Timeout, error, etc - return to chat
    RETURN "Use /v para tentar novamente"
```

## KEY CHANGES (v8.0)

| Old (v7.0) | New (v8.0) |
|------------|------------|
| Assumes MCP ready | Boot check + auto-install |
| Fails silently on missing deps | Clear install instructions |
| Manual dependency setup | One-command install |

## DEPENDENCIES

Required packages (auto-installed by boot):

| Package | Purpose |
|---------|---------|
| `mcp` | MCP SDK for Claude Code |
| `sounddevice` | Audio capture |
| `soundfile` | Audio file handling |
| `numpy` | Audio processing |
| `edge-tts` | TTS (free, online) |
| `pyttsx3` | TTS fallback (offline) |
| `pygame` | Audio playback |
| `faster-whisper` | STT (free, offline) |
| `python-dotenv` | Environment loading |
| `webrtcvad-wheels` | Voice activity detection (Windows) |

## FEEDBACK SIGNALS

| Signal | Meaning |
|--------|---------|
| BEEP (800Hz) | Recording started - speak now |
| BEEP (1200Hz) | Recording ended - processing |
| BEEP (400Hz low) | Timeout - no speech detected |

## RESPONSE GUIDELINES

- Keep TTS to 1-2 sentences max
- Be descriptive (user may not see screen)
- Confirm actions: "Feito", "3 arquivos encontrados"
- On unclear: "Nao entendi. Repita por favor."

## EXIT KEYWORDS

parar, sair, exit, quit, stop, encerrar, tchau

## CONFIGURATION

```bash
# In .env (already set for v8.0)
WAKE_WORD_ENABLED=false    # No wake word
STT_LANGUAGE=pt
STT_MAX_DURATION=15
```

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| `mcp__voice__* not available` | Run boot sequence, restart Claude Code |
| `webrtcvad failed to build` | Use `pip install webrtcvad-wheels` instead |
| `No microphone detected` | Check Windows Sound Settings > Recording |
| `Whisper model download` | First run downloads ~500MB model (one-time) |

---
**Version**: 8.0.0
**Date**: 2025-12-06
**Changes**: Boot sequence with auto-install, webrtcvad-wheels for Windows, troubleshooting guide
