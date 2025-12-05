# Voice Accessibility Guidelines | Knowledge Card

**Category**: VOICE_UI | **Quality Score**: 0.80
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

Voice accessibility ensures that voice-enabled systems are usable by people with diverse abilities, including those with visual, motor, cognitive, and speech impairments. Following WCAG (Web Content Accessibility Guidelines) principles adapted for voice creates inclusive experiences that benefit all users.

**Key Differentiator**: Universal design + legal compliance + expanded user base

---

## Key Concepts

### WCAG Principles Applied to Voice

| Principle | Voice Application |
|-----------|-------------------|
| **Perceivable** | Clear audio, adjustable speed, captions |
| **Operable** | Multiple input methods, timeout extensions |
| **Understandable** | Simple language, consistent patterns |
| **Robust** | Works across devices, fallback options |

### User Groups & Needs

| Group | Needs | Accommodations |
|-------|-------|----------------|
| Blind/Low Vision | Audio-only navigation | Full voice alternatives to visual |
| Deaf/Hard of Hearing | Visual feedback | Captions, transcripts, visual cues |
| Motor Impairments | Voice-only control | No gesture requirements |
| Cognitive | Simple interactions | Clear language, memory aids |
| Speech Impairments | Alternative input | Text input option, patience |
| Elderly | Slower pace | Adjustable speed, repetition |

### Accessibility Standards

| Standard | Scope | Relevance |
|----------|-------|-----------|
| WCAG 2.1 | Web content | Core guidelines |
| WCAG 2.2 | Extended | Focus, cognitive |
| Section 508 | US Federal | Legal compliance |
| EN 301 549 | EU | European compliance |
| ADA | US Disability | Legal requirement |

---

## Accessibility Requirements

### 1. Audio Output Accessibility

**1.1 Adjustable Speech Rate**

```python
# Allow users to control TTS speed
speech_settings = {
    "rate_options": [0.75, 1.0, 1.25, 1.5],  # Multipliers
    "default_rate": 1.0,
    "user_preference": "stored_in_profile"
}

def adjust_speech_rate(text: str, rate: float) -> str:
    """Apply SSML rate adjustment."""
    return f'<prosody rate="{int(rate * 100)}%">{text}</prosody>'
```

**1.2 Volume Control**

```python
# Independent volume control for voice output
volume_settings = {
    "min": 0.0,
    "max": 1.0,
    "default": 0.8,
    "step": 0.1
}
```

**1.3 Pause and Repeat**

```
User: "Pause"
System: [Pauses] "Pausado. Diga 'continuar' para retomar."

User: "Repetir"
System: [Repeats last response]

User: "Mais devagar"
System: [Repeats at slower rate]
```

---

### 2. Visual Feedback for Deaf/HoH

**2.1 Real-Time Captions**

```python
def display_caption(text: str, timing: dict) -> dict:
    """Generate synchronized captions for TTS output."""
    return {
        "text": text,
        "start_time": timing["start"],
        "end_time": timing["end"],
        "style": {
            "font_size": "adjustable",
            "background": "semi-transparent",
            "position": "bottom"
        }
    }
```

**2.2 Visual State Indicators**

| State | Visual Indicator |
|-------|------------------|
| Listening | Pulsing microphone icon |
| Processing | Animated dots/spinner |
| Speaking | Sound wave animation |
| Error | Red highlight + icon |
| Success | Green checkmark |

**2.3 Transcript History**

```python
# Maintain conversation transcript
transcript_log = {
    "entries": [
        {"speaker": "user", "text": "...", "timestamp": "..."},
        {"speaker": "system", "text": "...", "timestamp": "..."}
    ],
    "downloadable": True,
    "searchable": True
}
```

---

### 3. Motor Accessibility

**3.1 Voice-Only Operation**

All functions must be accessible without:
- Touch/mouse clicks
- Keyboard input
- Gestures
- Physical buttons

```python
# Voice alternatives for all actions
voice_commands = {
    "scroll_down": ["descer", "mais", "proxima pagina"],
    "scroll_up": ["subir", "voltar", "pagina anterior"],
    "select": ["selecionar", "escolher", "esse"],
    "back": ["voltar", "anterior", "cancelar"],
    "home": ["inicio", "menu principal", "comecar de novo"]
}
```

**3.2 Extended Timeouts**

```python
# Configurable timeout for users who need more time
timeout_settings = {
    "default": 10,  # seconds
    "extended": 30,  # seconds
    "no_timeout": True,  # Option to disable
    "warning_at": 0.7  # Warn at 70% of timeout
}

def timeout_warning() -> str:
    return "Ainda esta ai? Diga algo ou precisa de mais tempo?"
```

**3.3 Interrupt and Correct**

```
User: "Enviar mensagem para Joao... nao, para Maria"
System: "Entendi. Mensagem para Maria. O que voce quer dizer?"
```

---

### 4. Cognitive Accessibility

**4.1 Simple Language**

| Avoid | Use Instead |
|-------|-------------|
| "Authenticate your credentials" | "Digite sua senha" |
| "Navigate to the subsequent item" | "Proximo" |
| "Affirmative/Negative" | "Sim/Nao" |
| Technical jargon | Plain language |

**4.2 Memory Aids**

```python
def provide_context_reminder(current_step: int, total_steps: int, task: str) -> str:
    """Remind user of progress and context."""
    return f"Voce esta no passo {current_step} de {total_steps} para {task}."

# Example: "Voce esta no passo 2 de 4 para agendar sua consulta."
```

**4.3 Consistent Patterns**

- Same wake word throughout
- Consistent confirmation phrases
- Predictable menu structure
- Standard error messages

**4.4 Chunked Information**

```python
def chunk_information(items: list, chunk_size: int = 3) -> list:
    """Break large lists into digestible chunks."""
    chunks = []
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

# Present as: "Primeiro, temos: A, B, C. Quer ouvir mais?"
```

---

### 5. Speech Impairment Support

**5.1 Alternative Input**

```python
input_methods = {
    "voice": True,  # Primary
    "text": True,   # Alternative typing
    "touch": True,  # Button selection
    "switch": True  # Accessibility switch
}
```

**5.2 Recognition Tolerance**

```python
# More forgiving speech recognition settings
recognition_settings = {
    "confidence_threshold": 0.5,  # Lower for speech impairments
    "timeout_multiplier": 2.0,    # More time to speak
    "retry_automatically": False,  # Ask before retrying
    "accept_partial": True         # Accept partial matches
}
```

**5.3 Patient Responses**

```python
def patient_reprompt(attempt: int) -> str:
    """Non-frustrating error messages."""
    prompts = [
        "Nao consegui entender. Pode tentar novamente?",
        "Ainda nao captei. Tente falar mais devagar, ou digite se preferir.",
        "Sem problemas. Vamos tentar de outra forma. Voce pode digitar ou escolher uma opcao na tela."
    ]
    return prompts[min(attempt, len(prompts) - 1)]
```

---

### 6. Multi-Modal Fallbacks

**6.1 Voice-to-Visual Handoff**

```python
def handoff_to_visual(reason: str, link: str) -> str:
    """Graceful transition to visual interface."""
    return f"Para {reason}, e mais facil pela tela. Enviei um link para seu celular: {link}"
```

**6.2 Visual-to-Voice Handoff**

```python
def enable_voice_mode() -> str:
    """Help users switch to voice."""
    return "Voce pode usar comandos de voz a qualquer momento. Diga 'ajuda' para saber os comandos disponiveis."
```

---

## Implementation Checklist

### Minimum Requirements

```
[ ] Adjustable speech rate (0.5x - 2.0x)
[ ] Volume control independent of system
[ ] Pause/Resume/Repeat commands
[ ] Visual feedback for all states
[ ] Real-time captions available
[ ] Transcript download option
[ ] All features voice-accessible
[ ] Extended timeout option
[ ] Text input alternative
[ ] Simple, clear language
[ ] Progress indicators
[ ] Consistent navigation
```

### Enhanced Accessibility

```
[ ] Speech rate remembered per user
[ ] Custom wake word support
[ ] Personalized vocabulary
[ ] Context reminders
[ ] Multi-modal sync (voice + visual)
[ ] Screen reader compatibility
[ ] Keyboard navigation
[ ] High contrast captions
[ ] Adjustable caption size
[ ] Language simplification option
```

---

## How to Apply

### Accessible Voice Prompt Design

```python
def create_accessible_prompt(
    content: str,
    context: str = None,
    options: list = None,
    help_hint: bool = True
) -> str:
    """Create prompt following accessibility guidelines."""

    parts = []

    # Add context reminder if helpful
    if context:
        parts.append(context)

    # Main content in simple language
    parts.append(content)

    # Clear options (max 4)
    if options:
        if len(options) <= 4:
            parts.append(f"Voce pode: {', '.join(options[:-1])}, ou {options[-1]}.")
        else:
            parts.append(f"Algumas opcoes: {', '.join(options[:3])}. Diga 'mais opcoes' para outras.")

    # Help reminder
    if help_hint:
        parts.append("Diga 'ajuda' a qualquer momento.")

    return " ".join(parts)
```

### Testing Accessibility

```python
def accessibility_audit(voice_flow: dict) -> dict:
    """Audit voice flow for accessibility compliance."""

    issues = []

    # Check speech rate options
    if not voice_flow.get("adjustable_rate"):
        issues.append("Missing: Adjustable speech rate")

    # Check visual feedback
    if not voice_flow.get("visual_indicators"):
        issues.append("Missing: Visual state indicators")

    # Check timeout settings
    if voice_flow.get("timeout", 0) < 15:
        issues.append("Warning: Short timeout may exclude some users")

    # Check text alternative
    if not voice_flow.get("text_input_option"):
        issues.append("Missing: Text input alternative")

    # Check language complexity
    if voice_flow.get("avg_words_per_prompt", 0) > 20:
        issues.append("Warning: Prompts may be too long")

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "score": max(0, 1 - (len(issues) * 0.15))
    }
```

---

## When to Use

### Accessibility Priority by Feature

| Feature Type | Priority | Minimum | Enhanced |
|--------------|----------|---------|----------|
| Core functions | Critical | All users | All users |
| Settings/config | High | Voice + 1 alt | Voice + visual + keyboard |
| Help/support | High | Voice + visual | All modalities |
| Advanced features | Medium | Primary modality | Multiple options |
| Entertainment | Lower | Primary + captions | Full accessibility |

### Legal Compliance Scenarios

| Scenario | Requirements |
|----------|--------------|
| Public sector (US) | Section 508 compliance |
| Public sector (EU) | EN 301 549 compliance |
| Large business | ADA compliance recommended |
| Healthcare | HIPAA + accessibility |
| Education | WCAG 2.1 AA minimum |
| E-commerce | ADA + WCAG recommended |

---

## Cross-References

| Related File | Context |
|--------------|---------|
| interaction_patterns.md | Voice UX patterns |
| elevenlabs.md | TTS with rate control |
| openai_tts.md | Alternative TTS |
| whisper_api.md | STT with language support |

---

**Quality Score**: 0.80 | **Confidence**: High
**Source**: WCAG 2.1/2.2, Section 508, Voice UI Best Practices
