# Claude Prompt Engineering Guide

**Fonte**: platform.claude.com/docs
**Atualizado**: 2025-12-02
**Categoria**: LLM_PLATFORMS
**Plataforma**: Anthropic/Claude

---

## Prerequisites

Before optimizing your prompts, establish:

1. **Clear success metrics** for your use case
2. **Empirical testing methods** to validate performance
3. **Initial prompt draft** ready for refinement

---

## When to Use Prompt Engineering

Prompt engineering beats alternatives like fine-tuning for most scenarios:

| Advantage | Description |
|-----------|-------------|
| **Speed** | Nearly instantaneous results versus hours/days for fine-tuning |
| **Cost** | Uses base model pricing; no GPU infrastructure required |
| **Flexibility** | Rapidly iterate and experiment with variations |
| **Data efficiency** | Works with few-shot or zero-shot approaches |
| **Model compatibility** | Prompts survive provider model updates |
| **Transparency** | Human-readable inputs aid debugging |
| **Knowledge preservation** | Avoids catastrophic forgetting risks |
| **External content** | Superior for leveraging retrieved documents |

*Note: Some issues (latency, cost) may be better solved by model selection.*

---

## Prompt Engineering Techniques (Priority Order)

Apply these strategies progressively based on your specific needs:

### 1. Be Clear and Direct
Write unambiguous instructions without unnecessary complexity.

### 2. Use Examples (Multishot Prompting)
Provide multiple input-output examples showing desired behavior patterns.

### 3. Enable Chain of Thought
Encourage step-by-step reasoning: "Let Claude think" through problems.

### 4. Implement XML Tags
Structure information with semantic tags for clarity and parsing.

```xml
<context>
Background information here
</context>

<instructions>
Step-by-step task description
</instructions>

<examples>
<example>
Input: X
Output: Y
</example>
</examples>
```

### 5. Assign Roles (System Prompts)
Define context by giving Claude specific personas or domains.

### 6. Prefill Responses
Start Claude's output to guide format and tone.

### 7. Chain Complex Prompts
Break multi-step tasks into sequential prompts for reliability.

### 8. Optimize for Long Context
Apply specific strategies when working with extended documents.

---

## Key Principles

- Start with foundational techniques before specialized methods
- Test each adjustment against your success criteria
- Prioritize prompt engineering over fine-tuning for rapid improvement
- Maintain model's general knowledge while adding task specificity

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao construir prompts para agentes CODEXA
- Ao otimizar HOPs existentes
- Ao debuggar comportamentos inesperados do modelo
- Ao criar system prompts para novos workflows

**Tags**: claude, prompt_engineering, xml_tags, chain_of_thought, few_shot
