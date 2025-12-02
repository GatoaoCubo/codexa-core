# Voice Agent | Analysis & Construction Plan

> **⚠️ HISTORICAL DOCUMENT**
> This analysis was written on 2025-11-27 before the voice system refactor.
> The issues documented here have been **RESOLVED** in the new architecture:
> - OLD: `voice_lib/` → NEW: `voice/`
> - OLD: `mcp_servers/voice_server/` → NEW: `voice/server.py`
> - The `listen_and_respond` bug was fixed in `voice/server.py`
>
> See `voice/` directory for current implementation.

## MODULE_METADATA
- **id**: voice_agent_analysis_v1
- **version**: 1.0.0
- **purpose**: Complete analysis of voice system issues and agent construction plan
- **created**: 2025-11-27
- **status**: HISTORICAL (issues resolved)
- **category**: Meta-Construction | Agent Planning
- **methodology**: CODEXA 5-Phase ADW (Plan > Build > Test > Review > Document)

---

## PHASE 1: DISCOVERY | Current System Analysis

### 1.1 Architecture Overview

```
voice_lib/                     # Core voice library
├── stt.py                     # Speech-to-Text (ElevenLabs Scribe)
├── tts/                       # Text-to-Speech
│   ├── __init__.py           # Router (ElevenLabs + Edge TTS)
│   ├── elevenlabs_tts.py     # Premium TTS
│   └── edge_tts.py           # Free fallback TTS
├── config.py                  # Centralized configuration
├── continuous_session.py      # Continuous voice loop
├── agent_registry.py          # Agent routing
├── music_player.py           # Activation music
└── summarizer.py             # Response summarization

mcp_servers/voice_server/
└── server.py                  # MCP server (6 tools)

.claude/commands/
└── voice.md                   # /voice command definition
```

### 1.2 MCP Tools Available

| Tool | Purpose | Status |
|------|---------|--------|
| `listen` | Fixed duration STT | OK |
| `speak` | TTS output | OK (sometimes fails) |
| `listen_vad` | VAD-based STT | OK |
| `speak_summarized` | TTS with summarization | OK |
| `start_voice_loop` | Initialize continuous mode | OK |
| `listen_and_respond` | Continuous mode listening | BROKEN |
| `ask_agent` | Query specialized agents | OK |
| `list_agents` | List available agents | OK |

---

## PHASE 2: PROBLEM IDENTIFICATION

### 2.1 CRITICAL: listen_and_respond Broken

**Location**: `mcp_servers/voice_server/server.py:343`

**Issue**:
```python
# Line 343 - PROBLEM
transcribed_text = voice_listen(duration=max_duration, language="pt", use_vad=True)
```

**Root Cause**:
The `voice_listen` function in `voice_lib/stt.py` DOES accept `use_vad=True` (line 449), but there appears to be a module caching issue in the MCP server. The server imports `voice_listen` at startup, but if the stt.py file was modified after the server started, the old version without the parameter remains cached.

**Evidence**:
- Error: `listen() got an unexpected keyword argument 'use_vad'`
- But `stt.py:449` clearly shows: `def listen(duration=5, language='pt', use_vad=True)`
- The function signature is correct, so it's a runtime import/cache issue

**Impact**: Continuous voice mode completely non-functional

**Fix Required**:
1. Restart MCP server to reload modules
2. OR: Add explicit reload in server.py
3. OR: Use VAD function directly instead of through listen()

### 2.2 MEDIUM: TTS Intermittent Failures

**Symptom**: `speak()` sometimes returns "Failed to speak text"

**Possible Causes**:
1. ElevenLabs API rate limiting
2. Network latency issues
3. Audio device conflicts
4. Edge TTS fallback not triggering properly

**Location**: `voice_lib/tts/__init__.py:64-67`

**Current Code**:
```python
try:
    return speak_elevenlabs(text, voice_id=voice_id, save_to_file=save_to_file)
except Exception:
    return speak_edge(text, save_to_file=save_to_file)
```

**Issue**: Generic exception catching may hide specific errors. No logging.

### 2.3 MEDIUM: No Audio Feedback (Beeps)

**User Report**: "Não escutei nenhum bip"

**Expected**: Audio beep before listening starts

**Location**: `voice_lib/stt.py:139-146`

```python
def play_start_beep():
    """Play beep indicating recording started."""
    play_beep(frequency=800, duration_ms=150)
```

**Issue**:
1. Beep uses `sounddevice` which may conflict with recording
2. MCP server catches beep exceptions silently (lines 333-337)
3. No fallback if beep fails

### 2.4 LOW: Inconsistent Configuration

**Location**: `voice_lib/config.py`

**Issues**:
1. `AUDIO_INPUT_DEVICE` and `AUDIO_OUTPUT_DEVICE` default to None
2. Device IDs can change when devices are connected/disconnected
3. No automatic device detection

### 2.5 LOW: Missing Error Recovery

**Current State**: When errors occur, loop may break
**Expected**: Graceful error handling with retry

---

## PHASE 3: PROPOSED SOLUTION | voice_agent

### 3.1 Agent Purpose

Create a dedicated `voice_agent` to manage all voice interactions, following CODEXA patterns:

**Role**: Voice Interface Controller
**Domain**: Accessibility, Voice I/O
**Focus**: Reliable, continuous voice interaction

### 3.2 Agent Architecture

```
codexa.app/agentes/voice_agent/
├── PRIME.md                   # Agent context (this will be created)
├── README.md                  # Structure documentation
├── INSTRUCTIONS.md            # Operational instructions
├── SETUP.md                   # Installation guide
├── config/
│   └── 51_voice_agent.json   # Agent configuration
├── prompts/
│   ├── 01_voice_interaction_HOP.md
│   └── 02_error_recovery_HOP.md
├── builders/
│   └── voice_session_builder.py
├── validators/
│   └── audio_device_validator.py
└── tests/
    └── test_voice_pipeline.py
```

### 3.3 Core Components to Build

#### Component 1: Robust VAD Listener
```python
# New: voice_lib/vad_robust.py
class RobustVADListener:
    """VAD listener with retry, fallback, and device management."""

    def __init__(self):
        self.device_manager = AudioDeviceManager()
        self.retry_policy = RetryPolicy(max_attempts=3, backoff=1.5)

    def listen(self, max_duration=15) -> Optional[str]:
        """Listen with automatic retry and device fallback."""
        pass
```

#### Component 2: TTS Manager with Queue
```python
# New: voice_lib/tts_manager.py
class TTSManager:
    """Manages TTS with queue, retry, and fallback."""

    def speak(self, text: str, priority: int = 1) -> bool:
        """Queued speech with priority."""
        pass

    def speak_immediate(self, text: str) -> bool:
        """Bypass queue for urgent messages."""
        pass
```

#### Component 3: Audio Device Manager
```python
# New: voice_lib/device_manager.py
class AudioDeviceManager:
    """Automatic device detection and management."""

    def get_best_input_device(self) -> int:
        """Auto-detect best microphone."""
        pass

    def get_best_output_device(self) -> int:
        """Auto-detect best speaker."""
        pass
```

#### Component 4: Voice Session Controller
```python
# Enhanced: voice_lib/continuous_session.py
class VoiceSessionController:
    """Enhanced session with state machine."""

    states = ['IDLE', 'LISTENING', 'PROCESSING', 'SPEAKING', 'ERROR']

    def transition(self, new_state: str):
        """State transition with hooks."""
        pass
```

### 3.4 MCP Server Fixes

**File**: `mcp_servers/voice_server/server.py`

**Fix 1**: Direct VAD call (bypass caching issue)
```python
# Replace line 343
from voice_lib.stt import record_audio_with_vad, transcribe_audio

audio_path = record_audio_with_vad(max_duration=max_duration)
transcribed_text = transcribe_audio(audio_path, language="pt")
```

**Fix 2**: Add beep with fallback
```python
if beep_ready:
    try:
        from voice_lib.stt import play_start_beep
        play_start_beep()
    except Exception as e:
        print(f"Beep failed (non-critical): {e}", file=sys.stderr)
        # Continue without beep - don't block listening
```

**Fix 3**: Improved error handling
```python
except Exception as e:
    error_msg = str(e)
    print(f"Listen error: {error_msg}", file=sys.stderr)

    # Speak error to user
    try:
        voice_speak("Erro de áudio. Tentando novamente.")
    except:
        pass

    return [TextContent(
        type="text",
        text=f"LISTEN_RETRY: {error_msg}. Call listen_and_respond to retry."
    )]
```

---

## PHASE 4: IMPLEMENTATION PLAN

### Step 1: Fix Critical Bug (30 min)
- [ ] Fix `listen_and_respond` in server.py
- [ ] Test continuous mode works
- [ ] Verify beep plays

### Step 2: Create voice_agent Structure (1 hour)
- [ ] Create directory structure
- [ ] Write PRIME.md
- [ ] Write README.md
- [ ] Write INSTRUCTIONS.md
- [ ] Create 51_voice_agent.json config

### Step 3: Build Core Components (2 hours)
- [ ] RobustVADListener
- [ ] TTSManager with queue
- [ ] AudioDeviceManager
- [ ] VoiceSessionController with state machine

### Step 4: Update MCP Server (1 hour)
- [ ] Replace listen_and_respond implementation
- [ ] Add robust error handling
- [ ] Add logging
- [ ] Test all 6 tools

### Step 5: Create HOPs (1 hour)
- [ ] 01_voice_interaction_HOP.md
- [ ] 02_error_recovery_HOP.md

### Step 6: Validation & Documentation (1 hour)
- [ ] Run validators
- [ ] Update /voice command
- [ ] Test end-to-end

---

## PHASE 5: SUCCESS CRITERIA

### Functional Requirements
- [ ] Continuous voice mode works for 10+ minutes without failure
- [ ] Beep plays before each listen
- [ ] TTS works with <5% failure rate
- [ ] Graceful error recovery (no crashes)
- [ ] Exit commands work reliably

### Quality Requirements
- [ ] Agent follows CODEXA 12 pillars
- [ ] HOPs use TAC-7 format
- [ ] Config centralized in config.py
- [ ] All functions have docstrings
- [ ] Tests cover happy path + error cases

### Performance Requirements
- [ ] Listen latency <500ms
- [ ] TTS latency <1s
- [ ] VAD stops within 1.5s of silence
- [ ] No audio device conflicts

---

## APPENDIX A: Quick Fix for Immediate Use

Apply this fix NOW to restore `listen_and_respond`:

**File**: `mcp_servers/voice_server/server.py`

**Replace lines 341-372 with**:

```python
elif name == "listen_and_respond":
    # Listen with VAD for continuous mode
    beep_ready = arguments.get("beep_ready", True)
    max_duration = arguments.get("max_duration", 15)

    # Play ready beep
    if beep_ready:
        try:
            from voice_lib.stt import play_start_beep
            play_start_beep()
        except Exception as e:
            print(f"Beep skipped: {e}", file=sys.stderr)

    print(f"Listening (continuous mode, max {max_duration}s)...", file=sys.stderr)

    try:
        # FIXED: Use VAD functions directly
        from voice_lib.stt import record_audio_with_vad, transcribe_audio
        import os

        audio_path = record_audio_with_vad(
            max_duration=max_duration,
            silence_duration=1.5,
            min_recording=0.5
        )

        transcribed_text = transcribe_audio(audio_path, language="pt")

        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)

        if transcribed_text and transcribed_text.strip():
            # Check for exit commands
            exit_commands = ['parar', 'sair', 'exit', 'quit', 'stop', 'encerrar', 'tchau', 'pare']
            text_lower = transcribed_text.lower().strip()

            if any(cmd in text_lower for cmd in exit_commands):
                voice_speak("Até logo!")
                return [TextContent(
                    type="text",
                    text="EXIT_VOICE_LOOP: User requested to exit continuous mode."
                )]

            return [TextContent(
                type="text",
                text=f"VOICE_COMMAND: {transcribed_text}"
            )]
        else:
            return [TextContent(
                type="text",
                text="NO_SPEECH_DETECTED: Continue listening by calling listen_and_respond again."
            )]

    except Exception as e:
        print(f"Listen error: {e}", file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"LISTEN_ERROR: {str(e)}. Call listen_and_respond to retry."
        )]
```

---

## APPENDIX B: Validation Commands

```bash
# Test VAD listening
python -c "from voice_lib.stt import listen; print(listen(use_vad=True))"

# Test TTS
python -c "from voice_lib.tts import speak; speak('Teste de voz')"

# Test config
python voice_lib/config.py

# Test continuous session
python voice_lib/continuous_session.py
```

---

**Report Generated**: 2025-11-27
**Methodology**: CODEXA 5-Phase ADW
**Status**: Ready for Implementation
**Priority**: CRITICAL (continuous mode broken)
