# Voice Integration Plan: /voice + Voice Engine

## Current Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLAUDE CODE                                 │
├─────────────────────────────────────────────────────────────────┤
│  Slash Commands          │  MCP Server (voice-server)           │
│  ├── /voice.md           │  ├── listen (basic)                  │
│  ├── /ironman.md         │  ├── speak (TTS)                     │
│  └── /snap.md            │  ├── listen_and_respond (VAD)        │
│                          │  └── start_voice_loop                │
├─────────────────────────────────────────────────────────────────┤
│                      VOICE LIB                                   │
│  ├── stt/ (Speech-to-Text)                                      │
│  │   ├── elevenlabs_stt.py (listen, transcribe, VAD)            │
│  │   └── __init__.py (exports)                                  │
│  ├── tts/ (Text-to-Speech)                                      │
│  │   └── elevenlabs_tts.py (speak)                              │
│  ├── continuous_session.py (ContinuousVoiceSession)             │
│  └── config.py (settings)                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Problem

1. **Import Error**: MCP server can't import `record_audio_with_vad` because it was added to `elevenlabs_stt.py` after server startup
2. **Cache Issue**: Python caches modules, so server restart is required for changes
3. **Redundancy**: `/voice` command relies on MCP tools, but could use `ContinuousVoiceSession` directly

## Proposed Solution

### Option A: Fix MCP Server (Recommended)
Ensure all VAD functions are properly exported and restart server once.

**Steps:**
1. ✅ Add `record_audio_with_vad` to `elevenlabs_stt.py`
2. ✅ Update `voice_lib/stt/__init__.py` to export it
3. Restart Claude Code session to reload MCP server
4. Test `/voice` command

### Option B: Use ContinuousVoiceSession Directly
Create a new slash command that uses the Python session directly.

**Pros:**
- No MCP server dependency
- Uses battle-tested ContinuousVoiceSession class
- More reliable VAD handling

**Cons:**
- Requires running Python subprocess
- Less integration with Claude Code tools

### Option C: Hybrid Approach
Use MCP for basic voice tools, but fallback to direct Python for continuous mode.

## Recommended Implementation

### 1. Fix the Import (Already Done)
```python
# voice_lib/stt/__init__.py
from .elevenlabs_stt import (
    listen,
    record_audio,
    transcribe_audio,
    record_audio_with_vad,  # ← Added
    play_start_beep,
    play_end_beep,
)
```

### 2. Update /voice.md to Handle Fallback
If `listen_and_respond` fails, use basic `listen` tool in a loop:

```markdown
## FALLBACK MODE
If listen_and_respond returns an error:
1. Use mcp__voice__listen (basic mode)
2. Process command
3. Speak response
4. Repeat until exit command
```

### 3. Create /voice-direct.md (Alternative)
A slash command that runs ContinuousVoiceSession via subprocess:

```bash
cd C:\Users\Dell\Documents\GitHub\connect-my-github\lm.codexa
py -3.12 -c "from voice_lib.continuous_session import run_standalone_session; run_standalone_session()"
```

## Testing Checklist

- [ ] Restart Claude Code session
- [ ] Test `mcp__voice__listen_and_respond`
- [ ] Test `/voice` command
- [ ] Test exit commands (parar, sair, exit)
- [ ] Test error handling

## Next Steps

1. **Immediate**: Restart Claude Code to apply changes
2. **Short-term**: Update /voice.md with fallback logic
3. **Long-term**: Consider migrating to ContinuousVoiceSession for reliability
