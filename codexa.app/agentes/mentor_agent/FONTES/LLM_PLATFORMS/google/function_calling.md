# Gemini Function Calling Developer Guide

**Fonte**: ai.google.dev/gemini-api/docs/function-calling
**Atualizado**: 2025-12-02
**Categoria**: LLM_PLATFORMS
**Plataforma**: Google AI / Gemini

---

## Overview

Function calling enables models to:
- Augment knowledge through external data sources
- Extend capabilities via tools (calculators, etc.)
- Take actions through APIs

---

## Defining Functions

### Function Declaration Structure

Each declaration requires:

| Field | Description |
|-------|-------------|
| **name** | Unique identifier, no spaces/special chars |
| **description** | Clear explanation of purpose |
| **parameters** | Object defining input requirements |

### Schema Example

```json
{
  "name": "set_light_values",
  "description": "Sets brightness and color temperature of a light",
  "parameters": {
    "type": "object",
    "properties": {
      "brightness": {
        "type": "integer",
        "description": "Light level from 0 to 100"
      },
      "color_temp": {
        "type": "string",
        "enum": ["daylight", "cool", "warm"]
      }
    },
    "required": ["brightness", "color_temp"]
  }
}
```

---

## Implementation Workflow

1. **Define declarations** describing function name, parameters, purpose
2. **Call the model** with function declarations
3. **Execute the function** in your application (model does NOT execute)
4. **Send results back** to model for user-friendly response

---

## Advanced Capabilities

### Parallel Function Calling
Execute multiple independent functions simultaneously.

### Compositional Function Calling
Chain sequential function calls where one output becomes next input.

### Function Calling Modes

| Mode | Behavior |
|------|----------|
| **AUTO** | Model decides text vs function call (default) |
| **ANY** | Always predicts a function call |
| **NONE** | Prohibits function calling |
| **VALIDATED** | Function calls OR natural language with schema adherence |

---

## Python SDK Features

### Automatic Function Calling

Pass Python functions directly as tools:

```python
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: The city name to get weather for.
    """
    return f"Weather in {city}: Sunny, 25°C"

# SDK auto-converts to declaration
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=[get_weather]
)
```

The SDK automatically:
- Converts functions to declarations
- Manages function execution
- Handles response cycles

---

## Best Practices

### Description Quality
> "Be extremely clear and specific in your descriptions. The model relies on these to choose the correct function."

### Naming Conventions
- Use descriptive function names
- No spaces, periods, or dashes

### Strong Typing
- Employ specific types and enums
- Reduces errors significantly

### Tool Selection
- Provide only relevant tools
- Limit active set to 10-20 tools maximum

### Prompt Engineering
- Provide context about model's role
- Give explicit instructions on function usage
- Encourage clarification when needed
- Use low temperature (≈0) for deterministic calls

### Temperature Note
> For Gemini 3 models, maintain default temperature of 1.0

### Validation
For consequential operations, validate function calls with users before execution.

---

## Supported Models

| Model | Parallel | Compositional |
|-------|----------|---------------|
| Gemini 2.5 Pro | ✅ | ✅ |
| Gemini 2.5 Flash | ✅ | ✅ |
| Gemini 2.5 Flash-Lite | ✅ | ✅ |

---

## MCP Integration

The Gemini API supports Model Context Protocol (MCP):
- Open standard for connecting AI with external tools
- Built-in SDK support
- Automatic tool calling capabilities

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao implementar function calling com Gemini
- Ao integrar APIs externas via modelos Google
- Ao construir agentes autônomos
- Ao comparar implementações com Claude/OpenAI

**Tags**: gemini, function_calling, tools, api, agents, mcp
