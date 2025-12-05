# ADW-100: {{PERSONA_NAME}} Chat Workflow

> **Version**: 1.0.0 | **Agent**: persona_agent | **Type**: Agentic Developer Workflow

---

## IDENTITY

**Purpose**: AI {{DOMAIN_EXPERTISE_PT}} consultant for {{BRAND_NAME}} e-commerce
**Domain**: {{DOMAIN_EXPERTISE}}, product recommendations
**Output**: Personalized recommendations, care tips, product links

---

## TRIGGER

```yaml
triggers:
  - chat: User message in {{PERSONA_NAME}} widget
  - api: {{persona_id}}-chat edge function
  - command: /{{persona_cmd}} (dev mode)
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-100",
  "agent": "persona_agent",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "{{DOMAIN_EXPERTISE}}"},
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
**Task Type**: `{{DOMAIN_EXPERTISE}}`

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
    - Question about {{DOMAIN_TOPIC}} care
    - Product inquiry
    - General chat
  - Identify keywords ({{DOMAIN_TOPIC}} behavior, symptoms, products)

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
  - Maintain {{PERSONA_NAME}} persona

outputs:
  - advice: {{DOMAIN_TOPIC}} care recommendations
  - tone: Friendly, {{DOMAIN_ADJECTIVE}} personality
```

### Phase 3: RECOMMEND (1 sec)

```yaml
phase: recommend
objective: Suggest relevant products
actions:
  - Map problem -> product categories
  - Query Supabase for matching products
  - Rank by relevance
  - Format product cards

outputs:
  - products: Array of recommendations
  - reason: Why each product helps
```

**Edge Function**: `{{persona_id}}-recommendations`

### Phase 4: RESPOND (1 sec)

```yaml
phase: respond
objective: Format final response
actions:
  - Combine advice + products
  - Add personality flourishes
  - Format for chat widget
  - Optionally generate TTS audio

outputs:
  - message: Chat response
  - products: Product cards
  - audio_url: TTS if requested
```

**Edge Function**: `{{persona_id}}-tts` (optional)

---

## PERSONA

**Name**: {{PERSONA_NAME}}
**Role**: {{PERSONA_ROLE}}
**Personality**:
- Friendly and warm
- Knowledgeable about {{DOMAIN_EXPERTISE_PT}}
- Occasionally makes domain-related expressions
- Uses warm language

**Example Responses**:

```
"{{EXAMPLE_RESPONSE_WORKFLOW}}"

[Product cards appear]
```

---

## INTENT MAPPING

| User Says | Intent | Products |
|-----------|--------|----------|
| "{{ISSUE_1_TRIGGER}}" | {{ISSUE_1_KEY}} | {{PRODUCT_CAT_1}} |
| "{{ISSUE_2_TRIGGER}}" | {{ISSUE_2_KEY}} | {{PRODUCT_CAT_2}} |
| "{{ISSUE_3_TRIGGER}}" | {{ISSUE_3_KEY}} | {{PRODUCT_CAT_3}} |
| "{{ISSUE_4_TRIGGER}}" | {{ISSUE_4_KEY}} | {{PRODUCT_CAT_4}} |
| "entediado" | boredom | brinquedos |
| "muito quente" | cooling | tapetes refrescantes |

---

## EXECUTION MODES

### Chat Mode (Production)

User sends message -> Edge function processes -> Response with products

### Dev Mode

```bash
/{{persona_cmd}} "{{EXAMPLE_USER_MESSAGE}}"
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

**Created by**: persona_agent v1.0.0
**Last Updated**: {{CURRENT_DATE}}
