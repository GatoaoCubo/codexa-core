# ADW-100: Voice Interaction Workflow | Voice Agent

> **Version**: 1.0.0 | **Agent**: voice_agent | **Type**: Agentic Developer Workflow

---

## IDENTITY

**Purpose**: Voice-based interaction with Claude Code
**Domain**: Speech-to-text, text-to-speech, voice commands
**Output**: Transcribed text, spoken responses, voice loop

---

## TRIGGER

```yaml
triggers:
  - command: /voice
  - command: /voice-start
  - command: /voice-stop
  - tool: mcp__voice__listen
  - tool: mcp__voice__speak
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-100",
  "workflow_name": "Voice Interaction Workflow",
  "agent": "voice_agent",
  "version": "1.0.0",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "voice_interaction"},
    {"phase_id": "phase_1_capture", "phase_name": "Capture", "duration": "1-15s", "module": "VOICE_CAPTURE"},
    {"phase_id": "phase_2_process", "phase_name": "Process", "duration": "2-10s", "module": "CLAUDE_PROCESS"},
    {"phase_id": "phase_3_speak", "phase_name": "Speak", "duration": "1-10s", "module": "TTS_SPEAK"},
    {"phase_id": "phase_4_loop", "phase_name": "Loop", "duration": "continuous", "module": "VOICE_LOOP"}
  ]
}
```

---

## WORKFLOW PHASES

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `voice_interaction`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### Phase 1: CAPTURE (user speech)

```yaml
phase: capture
objective: Record and transcribe user speech
actions:
  - Start audio recording
  - Detect speech activity
  - Stop on silence or max duration
  - Send to Whisper API for transcription

outputs:
  - transcript: Transcribed text
  - confidence: Transcription confidence
  - duration: Recording length
```

**Tools**:
- `mcp__voice__listen_start()` - Non-blocking start
- `mcp__voice__listen_poll()` - Check status
- `mcp__voice__listen()` - Blocking (legacy)

### Phase 2: PROCESS (Claude response)

```yaml
phase: process
objective: Generate response to user input
actions:
  - Parse transcribed text
  - Route to appropriate handler:
    - Command detection
    - Question answering
    - Task execution

outputs:
  - response_text: Claude's response
  - action_taken: What was done
```

### Phase 3: SPEAK (TTS response)

```yaml
phase: speak
objective: Convert response to speech
actions:
  - Select TTS provider (Kokoro/OpenAI/System)
  - Generate audio from response text
  - Play audio to user

outputs:
  - audio_played: Boolean
  - duration: Playback length
```

**Tool**: `mcp__voice__speak({ text: "response" })`

### Phase 4: LOOP (continuous mode)

```yaml
phase: loop
objective: Maintain continuous voice conversation
actions:
  - After speaking, listen for next input
  - Repeat capture -> process -> speak
  - Exit on "stop" or "exit" command

outputs:
  - session_duration: Total conversation time
  - turns: Number of exchanges
```

**Tool**: `mcp__voice__start_voice_loop()`

---

## EXECUTION MODES

### Single Command

```javascript
// Listen once, respond, done
mcp__voice__listen()
// Process transcript
mcp__voice__speak("Response here")
```

### Non-blocking (Recommended)

```javascript
// Start recording in background
const session = mcp__voice__listen_start()

// Poll for completion
while (true) {
  const status = mcp__voice__listen_poll(session.session_id)
  if (status.status === "done") {
    // Process transcript
    break
  }
  // Continue other work
}
```

### Continuous Loop

```javascript
// Start voice loop with greeting
mcp__voice__start_voice_loop({
  greeting: "Voice mode activated. Speak your command."
})

// Loops until user says "exit" or "stop"
```

---

## QUALITY GATES

```yaml
quality_gates:
  transcription:
    - confidence > 0.7
    - no timeout (speech detected)

  tts:
    - audio plays successfully
    - response < 500 chars (for speed)
```

---

## CONFIGURATION

```json
{
  "language": "pt",
  "max_duration": 15,
  "initial_timeout": 3,
  "tts_provider": "kokoro",
  "voice": "bf_nicole",
  "speed": 1.0
}
```

---

## ERROR HANDLING

| Error | Response |
|-------|----------|
| No speech detected | "I didn't hear anything. Please try again." |
| Transcription failed | "Sorry, I couldn't understand that." |
| TTS failed | Fall back to text response |

---

## ACCESSIBILITY

Voice agent enables:
- Hands-free coding assistance
- Accessibility for users with mobility issues
- Faster interaction for quick commands

---

## INTEGRATION

**Upstream**: User microphone input
**Downstream**: Claude Code commands, other agents

---

**Created by**: voice_agent v1.0.0
**Last Updated**: 2025-11-30
