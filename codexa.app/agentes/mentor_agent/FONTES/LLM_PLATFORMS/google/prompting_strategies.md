# Gemini Prompting Strategies & Best Practices

**Fonte**: ai.google.dev/gemini-api/docs/prompting-strategies
**Atualizado**: 2025-12-02
**Categoria**: LLM_PLATFORMS
**Plataforma**: Google AI / Gemini

---

## Core Techniques

### 1. Clear & Specific Instructions

Provide explicit directions through:
- **Question input**: Direct queries expecting answers
- **Task input**: Procedural instructions to execute
- **Entity input**: Material for classification or analysis
- **Completion input**: Partial prompts for model to continue

### 2. Few-Shot Prompting

> "Prompts without few-shot examples are likely to be less effective"

**Best practices:**
- Use 2-5 varied, specific examples
- Show positive patterns, not negative ones
- Maintain consistent formatting across examples

### 3. Add Contextual Information
Include necessary background data within prompts rather than assuming the model possesses it.

### 4. Use Output Prefixes
Signal expected response formats through prefixes like "JSON:" or "The answer is:"

### 5. Break Complex Prompts
- **Separate instructions**: One prompt per task
- **Chain prompts**: Sequential steps
- **Aggregate responses**: Parallel processing

---

## Optimization Parameters

| Parameter | Effect |
|-----------|--------|
| **Max output tokens** | Limits response length (100 tokens ≈ 60-80 words) |
| **Temperature** | Controls randomness (0 = deterministic; higher = creative) |
| **topK** | Selects from top K probable tokens |
| **topP** | Selects tokens until probability sum reaches threshold |
| **stop_sequences** | Halts generation at specified text |

*Note: For Gemini 3, keep temperature at default 1.0 to avoid performance degradation.*

---

## Iteration Strategies

When results disappoint:
1. **Rephrase**: Different wording often yields different responses
2. **Switch tasks**: Reframe as analogous task
3. **Reorder content**: Different arrangement of examples, context, input
4. **Increase temperature**: If hitting safety filters

---

## Gemini 3 Specific Practices

- **Be precise**: State goals clearly without persuasive language
- **Use consistent delimiters**: XML tags or Markdown headings (pick one)
- **Define ambiguous terms**: Explicitly explain parameters
- **Control verbosity**: Request detailed responses if needed
- **Prioritize critical instructions**: Place at prompt start
- **Structure for length**: Large contexts first, questions last

### Structured Prompt Template

```xml
<role>
You are a [specialized assistant for domain]
</role>

<constraints>
1. [Requirement]
2. [Requirement]
</constraints>

<context>
[Background information]
</context>

<task>
[Specific request]
</task>
```

---

## Advanced Reasoning

Request planning before responses:

> "Before providing the final answer, parse the goal into distinct sub-tasks, verify information completeness, and create a structured outline."

Enable self-critique:

> "Review your generated output against the user's original constraints before returning your response."

---

## Things to Avoid

- Relying on models for factual information without verification
- Using models for complex math/logic without validation
- Assuming models know context you haven't provided
- Using anti-patterns (showing what NOT to do) in examples

---

## Quick Reference

| Goal | Approach |
|------|----------|
| Concise answers | Brief examples in few-shot |
| Specific structure | Output prefix + example format |
| JSON output | "JSON:" prefix + structured example |
| Troubleshooting | Include reference guide in context |

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao construir prompts para Gemini
- Ao otimizar respostas de modelos Google
- Ao comparar técnicas com Claude/GPT
- Ao implementar few-shot prompting

**Tags**: gemini, prompting, few_shot, temperature, xml_tags
