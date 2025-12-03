# /prime-voice - Voice System Configuration Hub

## PURPOSE
**Central hub for voice/audio configuration** - Everything a new user needs to set up and use voice mode.

**Role**: Voice Interface | **Domain**: Accessibility | **Activation**: `/v`

---

## QUICK START (New User)

### Step 1: Install Dependencies

```bash
pip install sounddevice soundfile numpy elevenlabs edge-tts pyttsx3 python-dotenv
```

Or use requirements:
```bash
pip install -r codexa.app/voice/requirements.txt
```

### Step 2: Configure .env

Add to `.env` in project root:

```env
# REQUIRED (minimum)
STT_LANGUAGE=pt
EDGE_VOICE=pt-BR-FranciscaNeural

# OPTIONAL (premium voices)
ELEVENLABS_API_KEY=your_key_here

# OPTIONAL (device selection)
AUDIO_INPUT_DEVICE=
AUDIO_OUTPUT_DEVICE=
```

### Step 3: Test Audio

```bash
# Check microphone
python -c "import sounddevice as sd; print(sd.query_devices())"

# Test TTS
python -c "from codexa.app.voice.tts import speak; speak('Teste de voz')"

# Test STT
python -c "from codexa.app.voice.stt import listen; print(listen(duration=3))"
```

### Step 4: Use Voice Mode

In Claude Code, type:
```
/v
```

Speak your command after the BEEP.

---

## ARCHITECTURE (v7.0)

```
┌─────────────────────────────────────────────────────────────┐
│                      /v FLOW                                 │
├─────────────────────────────────────────────────────────────┤
│  1. User types /v                                            │
│         │                                                    │
│         ▼                                                    │
│  2. BEEP (800Hz) ← Recording starts                          │
│         │                                                    │
│         ▼                                                    │
│  3. User speaks (15s window, no wake word needed)            │
│         │                                                    │
│         ▼                                                    │
│  4. BEEP (1200Hz) ← Recording ended                          │
│         │                                                    │
│         ▼                                                    │
│  5. Whisper/ElevenLabs transcribes                           │
│         │                                                    │
│         ▼                                                    │
│  6. Claude interprets + executes                             │
│         │                                                    │
│         ▼                                                    │
│  7. TTS speaks response → Return to chat                     │
└─────────────────────────────────────────────────────────────┘
```

---

## FILE MAP

### Configuration Files
| File | Purpose |
|------|---------|
| `.env` | API keys, device settings, language |
| `codexa.app/voice/config.py` | Python config loader |
| `codexa.app/voice/config/voices.json` | Available TTS voices |
| `voice_agent/config/51_voice_agent.json` | Agent metadata |

### Implementation Files
| File | Purpose |
|------|---------|
| `codexa.app/voice/stt.py` | Speech-to-Text (Whisper/ElevenLabs) |
| `codexa.app/voice/tts.py` | Text-to-Speech (Edge/ElevenLabs/pyttsx3) |
| `codexa.app/voice/server.py` | MCP Server |
| `codexa.app/voice/voice_daemon.py` | Background daemon |
| `codexa.app/voice/voice_filter.py` | Noise filtering |

### Documentation
| File | Purpose |
|------|---------|
| `voice_agent/PRIME.md` | Agent overview |
| `voice_agent/SETUP.md` | Detailed setup guide |
| `voice_agent/INSTRUCTIONS.md` | AI instructions |
| `codexa.app/voice/README.md` | Quick start |
| `codexa.app/voice/docs/SETUP.md` | Extended setup |

### Commands
| File | Purpose |
|------|---------|
| `.claude/commands/v.md` | `/v` command definition |
| `.claude/commands/vstart.md` | Start voice daemon |
| `.claude/commands/vstop.md` | Stop voice daemon |
| `.claude/commands/vstatus.md` | Check daemon status |
| `.claude/commands/vgui.md` | Voice GUI mode |

---

## CONFIGURATION OPTIONS

### .env Variables (Complete Reference)

```env
# ═══════════════════════════════════════════════════════════
# LANGUAGE & LOCALIZATION
# ═══════════════════════════════════════════════════════════
STT_LANGUAGE=pt                    # pt, en, es
CODEXA_LANGUAGE=pt                 # System language
CODEXA_USER_NAME=User              # User name for greetings

# ═══════════════════════════════════════════════════════════
# SPEECH-TO-TEXT (STT)
# ═══════════════════════════════════════════════════════════
STT_MAX_DURATION=15                # Max recording seconds
WAKE_WORD_ENABLED=false            # v7.0: No wake word needed

# ═══════════════════════════════════════════════════════════
# TEXT-TO-SPEECH (TTS)
# ═══════════════════════════════════════════════════════════
EDGE_VOICE=pt-BR-FranciscaNeural   # Default voice (free)
TTS_MAX_RESPONSE_DURATION=30       # Max TTS duration
TTS_FALLBACK_OFFLINE=true          # Use pyttsx3 if online fails

# ═══════════════════════════════════════════════════════════
# ELEVENLABS (Premium - Optional)
# ═══════════════════════════════════════════════════════════
ELEVENLABS_API_KEY=                # Get from elevenlabs.io
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# ═══════════════════════════════════════════════════════════
# AUDIO DEVICES (Optional)
# ═══════════════════════════════════════════════════════════
AUDIO_INPUT_DEVICE=                # Microphone ID (blank = default)
AUDIO_OUTPUT_DEVICE=               # Speaker ID (blank = default)

# ═══════════════════════════════════════════════════════════
# VOICE ACTIVITY DETECTION (VAD)
# ═══════════════════════════════════════════════════════════
VAD_SILENCE_THRESHOLD=1.5          # Seconds of silence to stop
VAD_MAX_DURATION=15.0              # Max recording duration
VAD_ENERGY_THRESHOLD=0.02          # Noise threshold
```

---

## AVAILABLE VOICES

### Edge TTS (Free)

| Voice ID | Name | Language | Gender |
|----------|------|----------|--------|
| `pt-BR-FranciscaNeural` | Francisca | BR Portuguese | Female |
| `pt-BR-AntonioNeural` | Antonio | BR Portuguese | Male |
| `pt-PT-RaquelNeural` | Raquel | PT Portuguese | Female |
| `en-US-JennyNeural` | Jenny | US English | Female |
| `en-US-GuyNeural` | Guy | US English | Male |

### ElevenLabs (Premium)

| Voice ID | Name | Description |
|----------|------|-------------|
| `21m00Tcm4TlvDq8ikWAM` | Rachel | Natural, calm |
| `pMsXgVXv3BLzUgSXRplE` | Camila | Brazilian Portuguese |
| `EXAVITQu4vr4xnSDxMaL` | Bella | Soft, sophisticated |
| `TX3LPaxmHKxFdv7VOQHJ` | Rafael | Deep, authoritative |

---

## TTS FALLBACK CHAIN

The system automatically falls back:

```
1. Edge TTS (free, online, good quality)
      │
      ▼ if fails
2. ElevenLabs (premium, requires API key)
      │
      ▼ if fails
3. pyttsx3 (offline, always works)
```

---

## FEEDBACK SIGNALS

| Signal | Frequency | Meaning |
|--------|-----------|---------|
| BEEP | 800Hz | Recording started - speak now |
| BEEP | 1200Hz | Recording ended - processing |
| BEEP | 400Hz | Timeout - no speech detected |

---

## EXIT COMMANDS

Say any of these to exit voice mode:
- parar, sair, exit, quit, stop
- encerrar, tchau, pare, finalizar

---

## TROUBLESHOOTING

### "No module named 'sounddevice'"
```bash
pip install sounddevice
# Windows may need Visual C++ redistributable
```

### "No audio input device"
1. Check microphone is connected
2. Grant microphone permissions in OS settings
3. Set device manually: `AUDIO_INPUT_DEVICE=0`
4. List devices: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### "TTS fails silently"
1. Check internet connection (Edge TTS needs it)
2. Set `TTS_FALLBACK_OFFLINE=true` in .env
3. Test offline: `python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"`

### "ELEVENLABS_API_KEY not found"
1. Get key from https://elevenlabs.io/
2. Add to `.env`: `ELEVENLABS_API_KEY=your_key`
3. Or skip - system uses free Edge TTS by default

### "VAD doesn't stop recording"
Increase silence threshold:
```env
VAD_SILENCE_THRESHOLD=2.0
```

### Platform-Specific

**Windows**:
- Use Python 3.10+
- May need Visual C++ redistributable
- Settings > Privacy > Microphone permissions

**macOS**:
- System Preferences > Security > Microphone
- Grant Terminal/IDE permission

**Linux**:
- `sudo apt install portaudio19-dev`
- Add user to `audio` group

---

## RELATED COMMANDS

| Command | Description |
|---------|-------------|
| `/v` | Activate voice mode (single capture) |
| `/vstart` | Start voice daemon (background) |
| `/vstop` | Stop voice daemon |
| `/vstatus` | Check daemon status |
| `/vgui` | Open voice GUI |

---

## INSTRUCTIONS FOR AI ASSISTANTS

### When `/prime-voice` is called:

1. Read this file for configuration context
2. Check if user needs setup help
3. Guide through troubleshooting if needed
4. Explain available options

### When `/v` is called:

1. Start listening: `mcp__voice__listen_start(max_duration=15)`
2. Poll: `mcp__voice__listen_poll(session_id)`
3. Handle result:
   - `VOICE_COMMAND:` → Execute, speak response
   - `NOISE_FILTERED:` → "Nao entendi. Repita."
   - `EXIT_VOICE_LOOP:` → "Ate logo", stop
   - Timeout → Return to chat silently

### Response Rules
- Keep TTS to 1-2 sentences
- Be descriptive (user may not see screen)
- Confirm actions: "Feito", "3 arquivos encontrados"

---

**Version**: 1.0.0
**Last Updated**: 2025-12-03
**Type**: Configuration Hub - Voice System
**Context Load**: Light (configuration reference)
