# Voice Interaction Patterns | Knowledge Card

**Category**: VOICE_UI | **Quality Score**: 0.82
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

Voice interaction patterns define how users communicate with voice-enabled systems. This card covers 12 essential patterns for designing natural, intuitive voice experiences. Proper pattern selection improves user satisfaction, reduces errors, and increases task completion rates.

**Key Differentiator**: User-centered design + error recovery + natural conversation flow

---

## Key Concepts

### Voice UI Principles

| Principle | Description |
|-----------|-------------|
| Brevity | Keep prompts short (< 20 words) |
| Clarity | Use simple, unambiguous language |
| Forgiveness | Handle errors gracefully |
| Feedback | Confirm actions immediately |
| Control | Let users interrupt and correct |
| Context | Remember conversation state |

### Conversation States

```
IDLE → LISTENING → PROCESSING → RESPONDING → IDLE
         ↓            ↓             ↓
      TIMEOUT      ERROR       CLARIFY
```

### Voice vs Text Differences

| Aspect | Text UI | Voice UI |
|--------|---------|----------|
| Information density | High | Low |
| Navigation | Visual scan | Sequential |
| Error correction | Easy edit | Must re-speak |
| User attention | Partial | Full |
| Memory load | Low (visible) | High (ephemeral) |

---

## 12 Essential Patterns

### Pattern 1: Wake Word Activation

**Purpose**: Initialize voice interaction without accidental triggers.

```
[DORMANT] "Hey Assistant" → [ACTIVE] "I'm listening"

Examples:
- "Alexa, what's the weather?"
- "OK Google, set a timer"
- "Hey Siri, call Mom"
```

**Design Guidelines**:
- Choose distinctive, multi-syllable wake words
- Provide audio/visual confirmation of activation
- Set reasonable timeout (5-10 seconds)
- Allow customization where possible

---

### Pattern 2: Explicit Confirmation

**Purpose**: Verify critical actions before execution.

```
User: "Transfer 500 dollars to John"
System: "You want to transfer 500 dollars to John Smith. Is that correct?"
User: "Yes" / "No, 50 dollars"
```

**When to Use**:
- Financial transactions
- Irreversible actions (delete, send)
- Actions affecting others
- Ambiguous commands

**Implementation**:
```python
def confirm_action(action: str, details: dict) -> str:
    return f"Voce quer {action}: {details['summary']}. Confirma?"
```

---

### Pattern 3: Implicit Confirmation

**Purpose**: Acknowledge without blocking flow.

```
User: "Add milk to my shopping list"
System: "Milk added. Anything else?"
```

**When to Use**:
- Low-risk actions
- Reversible operations
- Frequent/routine tasks
- When speed matters

**Implementation**:
```python
def implicit_confirm(action: str, next_prompt: str = "Mais alguma coisa?") -> str:
    return f"{action}. {next_prompt}"
```

---

### Pattern 4: Progressive Disclosure

**Purpose**: Reveal information in digestible chunks.

```
User: "What are today's meetings?"
System: "You have 3 meetings today. The first is at 9 AM with the design team. Want to hear the others?"
User: "Yes"
System: "At 2 PM you have a client call, and at 4 PM the weekly standup."
```

**Design Guidelines**:
- Start with summary (count, overview)
- Offer to expand on request
- Group related items (max 3-4 per chunk)
- Allow skipping ("Skip to the last one")

---

### Pattern 5: Slot Filling

**Purpose**: Collect required information piece by piece.

```
System: "Para agendar sua consulta, preciso de algumas informações."
System: "Qual a data preferida?"
User: "Proxima segunda"
System: "Segunda, dia 9. Qual horario: manha ou tarde?"
User: "Manha"
System: "Qual seu telefone para contato?"
User: "11 99999 8888"
System: "Perfeito! Consulta agendada para segunda, 9 de dezembro, pela manha. Confirmaremos pelo 11 99999-8888."
```

**Implementation**:
```python
slots = {
    "date": {"prompt": "Qual a data preferida?", "required": True},
    "time": {"prompt": "Qual horario: manha ou tarde?", "required": True},
    "phone": {"prompt": "Qual seu telefone para contato?", "required": True}
}

def fill_slot(slot_name: str, slots: dict) -> str:
    return slots[slot_name]["prompt"]
```

---

### Pattern 6: Error Recovery - Reprompt

**Purpose**: Handle unrecognized input gracefully.

```
User: [inaudible or ambiguous]
System: "Desculpe, nao entendi. Voce pode repetir?"
User: "Quero cancelar meu pedido"
System: "Entendi. Voce quer cancelar o pedido numero..."
```

**Escalation Levels**:
1. Simple reprompt: "Pode repetir?"
2. Rephrase request: "De outra forma, o que voce gostaria?"
3. Offer options: "Voce quer A, B ou C?"
4. Fallback: "Vou transferir para um atendente."

**Implementation**:
```python
def handle_error(attempt: int) -> str:
    prompts = [
        "Desculpe, pode repetir?",
        "Nao consegui entender. Tente de outra forma.",
        "Ainda nao entendi. Voce quer: cancelar, trocar ou falar com atendente?",
        "Vou transferir voce para um atendente. Um momento."
    ]
    return prompts[min(attempt, len(prompts) - 1)]
```

---

### Pattern 7: Disambiguation

**Purpose**: Resolve ambiguous references or commands.

```
User: "Ligar para Maria"
System: "Encontrei duas Marias. Maria Silva ou Maria Santos?"
User: "Maria Santos"
System: "Ligando para Maria Santos..."
```

**Design Guidelines**:
- Present max 3-4 options
- Include distinguishing details
- Allow "the first one" / "the last one"
- Remember preferences for future

---

### Pattern 8: Barge-In (Interruption)

**Purpose**: Let users interrupt long responses.

```
System: "Voce tem 5 mensagens novas. A primeira e de João sobre o projeto de marketing que..."
User: "Pular para a ultima"
System: "A ultima mensagem e de Ana: 'Reuniao confirmada para amanha.'"
```

**Implementation**:
- Enable voice activity detection during playback
- Process interruption immediately
- Maintain context of what was interrupted

---

### Pattern 9: Help & Discovery

**Purpose**: Guide users to available capabilities.

```
User: "O que voce pode fazer?"
System: "Posso ajudar com: agendar compromissos, enviar mensagens, fazer ligacoes, tocar musica, e responder perguntas. O que voce gostaria?"

User: "Como eu agendo uma reuniao?"
System: "Diga 'agendar reuniao' seguido da data e horario. Por exemplo: 'agendar reuniao amanha as 10 horas'."
```

**Help Levels**:
1. Overview: What can you do?
2. Category: Help with calendar
3. Specific: How do I reschedule?
4. Contextual: Help (during task)

---

### Pattern 10: Context Carryover

**Purpose**: Maintain conversation context across turns.

```
User: "Qual a previsao do tempo para Sao Paulo?"
System: "Em Sao Paulo faz 28 graus com sol."
User: "E amanha?"
System: "Amanha em Sao Paulo, 30 graus com possibilidade de chuva a tarde."
User: "E no Rio?"
System: "No Rio de Janeiro amanha, 32 graus com sol."
```

**Implementation**:
```python
context = {
    "location": "Sao Paulo",
    "date": "hoje",
    "topic": "weather"
}

def update_context(user_input: str, current_context: dict) -> dict:
    # Extract and merge new entities
    new_entities = extract_entities(user_input)
    return {**current_context, **new_entities}
```

---

### Pattern 11: Proactive Notification

**Purpose**: Initiate interaction when relevant.

```
System: [Notification sound]
System: "Lembrete: sua reuniao com o cliente comeca em 15 minutos."
User: "OK" / "Adiar 10 minutos" / "Cancelar"
```

**Design Guidelines**:
- Use audio cue before speaking
- Keep notifications brief
- Offer clear action options
- Respect quiet hours / DND modes

---

### Pattern 12: Graceful Degradation

**Purpose**: Handle system limitations transparently.

```
User: "Mostrar fotos da minha viagem"
System: "Nao consigo mostrar fotos por voz, mas enviei um link para seu telefone. Posso descrever as fotos se preferir."

User: "Comprar ingresso para o show"
System: "Por seguranca, compras precisam de confirmacao visual. Abri o app no seu celular para voce finalizar."
```

**Strategies**:
- Offer alternative modality (visual, text)
- Explain limitation simply
- Provide next best action
- Never dead-end the user

---

## How to Apply

### Voice Prompt Template

```python
def create_voice_prompt(
    greeting: str = None,
    main_content: str,
    options: list = None,
    question: str = None
) -> str:
    """Build natural voice prompt."""

    parts = []

    if greeting:
        parts.append(greeting)

    parts.append(main_content)

    if options:
        parts.append(f"As opcoes sao: {', '.join(options[:-1])}, ou {options[-1]}.")

    if question:
        parts.append(question)

    return " ".join(parts)

# Usage
prompt = create_voice_prompt(
    main_content="Encontrei 3 restaurantes proximos.",
    options=["italiano", "japones", "brasileiro"],
    question="Qual voce prefere?"
)
# Output: "Encontrei 3 restaurantes proximos. As opcoes sao: italiano, japones, ou brasileiro. Qual voce prefere?"
```

### Conversation Flow Design

```python
class VoiceConversation:
    def __init__(self):
        self.state = "idle"
        self.context = {}
        self.error_count = 0

    def process_input(self, user_input: str) -> str:
        if not user_input or user_input == "[NO_SPEECH]":
            self.error_count += 1
            return self.handle_error()

        self.error_count = 0
        self.context = self.update_context(user_input)

        intent = self.classify_intent(user_input)

        if intent == "help":
            return self.provide_help()
        elif intent == "cancel":
            return self.cancel_current()
        else:
            return self.execute_intent(intent)

    def handle_error(self) -> str:
        if self.error_count >= 3:
            return "Parece que estamos com dificuldade. Tente mais tarde ou use o app."
        return "Desculpe, pode repetir?"
```

---

## When to Use

### Pattern Selection Guide

| Scenario | Primary Pattern | Secondary |
|----------|-----------------|-----------|
| First interaction | Help & Discovery | Wake Word |
| Collecting info | Slot Filling | Progressive Disclosure |
| Critical action | Explicit Confirmation | Disambiguation |
| Routine task | Implicit Confirmation | Context Carryover |
| Recognition failure | Error Recovery | Graceful Degradation |
| Long response | Barge-In | Progressive Disclosure |
| Ambiguous input | Disambiguation | Reprompt |
| System limitation | Graceful Degradation | Help |

---

## Cross-References

| Related File | Context |
|--------------|---------|
| accessibility.md | WCAG compliance for voice |
| elevenlabs.md | TTS implementation |
| openai_tts.md | Alternative TTS |
| whisper_api.md | STT implementation |

---

**Quality Score**: 0.82 | **Confidence**: High
**Source**: Voice UI Design Best Practices (Google, Amazon, Apple guidelines)
