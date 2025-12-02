# /v - Voice Mode v7.0 (Simplified UX)

Single voice capture with beep feedback. No wake word, no TTS greeting.

## FLOW

```
1. /v is called
2. BEEP plays (recording starts immediately after beep)
3. User has 15s window to speak anything
4. Whisper transcribes
5. Claude interprets as "desire/intent"
6. If unclear -> speak "Nao entendi. Repita."
7. If clear -> execute and speak short response
8. Return to chat (user types /v for next command)
```

## IMPLEMENTATION

```python
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

## KEY CHANGES (v7.0)

| Old (v4.0) | New (v7.0) |
|------------|------------|
| TTS greeting "Modo voz ativado" | Just BEEP |
| Wake word required "codexa" | No wake word - speak freely |
| Continuous loop | Single capture per /v |
| Silent on noise | Ask "Nao entendi. Repita." |

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
# In .env (already set for v7.0)
WAKE_WORD_ENABLED=false    # No wake word
STT_LANGUAGE=pt
STT_MAX_DURATION=15
```

---
**Version**: 7.0.0
**Date**: 2025-11-30
**Changes**: Beep-only feedback, no wake word, single capture per /v
