# ADW-100: Ronronalda Chat Workflow

> **Version**: 1.0.0 | **Agent**: ronronalda_agent | **Type**: Agentic Developer Workflow

---

## IDENTITY

**Purpose**: AI cat consultant for GATO3 e-commerce
**Domain**: Pet care advice, product recommendations
**Output**: Personalized recommendations, care tips, product links

---

## TRIGGER

```yaml
triggers:
  - chat: User message in Ronronalda widget
  - api: ronronalda-chat edge function
  - command: /ronronalda (dev mode)
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-100",
  "agent": "ronronalda_agent",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "cat_consulting"},
    {"phase_id": "phase_1_understand", "phase_name": "Understand", "duration": "1sec"},
    {"phase_id": "phase_2_consult", "phase_name": "Consult", "duration": "2sec"},
    {"phase_id": "phase_3_recommend", "phase_name": "Recommend", "duration": "1sec"},
    {"phase_id": "phase_4_respond", "phase_name": "Respond", "duration": "1sec"}
  ]
}
```

---

## WORKFLOW PHASES

### Phase 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `cat_consulting`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### Phase 1: UNDERSTAND (1 sec)

```yaml
phase: understand
objective: Parse and classify user message
actions:
  - Extract user intent:
    - Problem description
    - Question about cat care
    - Product inquiry
    - General chat
  - Identify keywords (cat behavior, symptoms, products)

outputs:
  - intent: classified intent
  - keywords: extracted terms
  - urgency: low/medium/high
```

### Phase 2: CONSULT (2 sec)

```yaml
phase: consult
objective: Generate expert advice
actions:
  - Match intent to knowledge base
  - Generate personalized response
  - Include care tips if relevant
  - Maintain cat personality (Ronronalda persona)

outputs:
  - advice: Cat care recommendations
  - tone: Friendly, cat-like personality
```

### Phase 3: RECOMMEND (1 sec)

```yaml
phase: recommend
objective: Suggest relevant products
actions:
  - Map problem → product categories
  - Query Supabase for matching products
  - Rank by relevance
  - Format product cards

outputs:
  - products: Array of recommendations
  - reason: Why each product helps
```

**Edge Function**: `ronronalda-recommendations`

### Phase 4: RESPOND (1 sec)

```yaml
phase: respond
objective: Format final response
actions:
  - Combine advice + products
  - Add personality flourishes (purrs, cat expressions)
  - Format for chat widget
  - Optionally generate TTS audio

outputs:
  - message: Chat response
  - products: Product cards
  - audio_url: TTS if requested
```

**Edge Function**: `ronronalda-tts` (optional)

---

## PERSONA

**Name**: Ronronalda
**Species**: Cat (obviously)
**Role**: Feline wellness consultant
**Personality**:
- Friendly and warm
- Knowledgeable about cat behavior
- Occasionally makes cat puns
- Uses cat-related expressions ("purrrfect", "meow")

**Example Responses**:

```
"Entendi, seu gatinho está arranhando o sofá... Isso é
completamente normal! Gatos precisam arranhar para manter
as unhas saudáveis e marcar território. 🐱

Tenho algumas sugestões purrrfeitas para você:"

[Product cards appear]
```

---

## INTENT MAPPING

| User Says | Intent | Products |
|-----------|--------|----------|
| "arranha o sofá" | scratching | arranhadores |
| "vomita após comer" | vomiting | comedouros elevados |
| "estressado" | stress | tocas, camas |
| "xixi fora da caixa" | litter_box | caixas sanitárias |
| "entediado" | boredom | brinquedos |
| "muito quente" | cooling | tapetes refrescantes |

---

## EXECUTION MODES

### Chat Mode (Production)

User sends message → Edge function processes → Response with products

### Dev Mode

```bash
/ronronalda "Meu gato está arranhando o sofá"
```

Simulates chat interaction locally.

---

## QUALITY GATES

```yaml
quality_gates:
  response:
    - relevant_to_input: true
    - has_personality: true
    - max_response_length: 500 chars

  recommendations:
    - products_available: true
    - products_relevant: true
```

---

## INTEGRATION

**Upstream**: Chat widget, Edge Function
**Downstream**: Product catalog, TTS

---

**Created by**: ronronalda_agent v1.0.0
**Last Updated**: 2025-11-30
