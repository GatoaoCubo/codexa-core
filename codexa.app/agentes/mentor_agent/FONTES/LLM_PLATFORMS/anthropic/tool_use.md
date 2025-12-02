# Claude Tool Use & Function Calling Guide

**Fonte**: platform.claude.com/docs
**Atualizado**: 2025-12-02
**Categoria**: LLM_PLATFORMS
**Plataforma**: Anthropic/Claude

---

## Overview

Claude supports tool use to extend its capabilities through custom functions and integrations. The API enables Claude to request tool execution, creating a workflow for solving complex tasks.

---

## Tool Types

### Client Tools
Execute on your infrastructure:
- Custom user-defined tools you implement
- Anthropic-defined tools (computer use, text editor) requiring client implementation

### Server Tools
Run on Anthropic's infrastructure:
- Web search and web fetch utilities
- Require no implementation; just include in API requests

---

## Defining Tools

Each tool requires three components:

| Component | Description |
|-----------|-------------|
| **Name** | A unique identifier for the tool |
| **Description** | Clear explanation of what the tool does |
| **Input Schema** | JSON Schema defining required and optional parameters |

### Example Tool Definition

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "Temperature unit preference"
      }
    },
    "required": ["location"]
  }
}
```

### Schema Best Practices

- Use descriptive property names and descriptions
- Specify `required` parameters explicitly
- Include examples in descriptions (e.g., "San Francisco, CA")
- Use enums for constrained options
- Provide clear guidance on parameter formats

---

## Tool Use Workflow

### Step 1: Provide Tools and Prompt
Submit tools and user query to the API. Claude analyzes whether tools are needed.

### Step 2: Claude Decides
Claude determines which tool(s) to use and constructs formatted requests. The API response includes `stop_reason: "tool_use"` and tool use blocks.

### Step 3: Execute and Return
Extract tool name and input parameters, execute locally, and return results in a `tool_result` content block within a new user message.

### Step 4: Process Results
Claude analyzes tool outputs to formulate the final response.

---

## Handling Tool Calls

### Single Tool Response

Claude returns a structured response:

```json
{
  "type": "tool_use",
  "id": "toolu_01A09q90qw90lq917835lq9",
  "name": "get_weather",
  "input": {"location": "San Francisco, CA", "unit": "celsius"}
}
```

Return results with matching tool_use_id:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "15 degrees"
    }
  ]
}
```

### Parallel Tool Use

Claude can call multiple tools simultaneously. All `tool_use` blocks appear in one assistant message, and all corresponding `tool_result` blocks must be provided in the subsequent user message.

### Sequential Tool Use

Some workflows require chaining tools where output from one feeds into another. Claude calls tools one at a time, receiving results between calls.

---

## Advanced Features

### Forcing Tool Use

Control with `tool_choice` parameter:

| Value | Behavior |
|-------|----------|
| `"auto"` | Claude decides (default) |
| `"any"` | Claude must use any available tool |
| `{"type": "tool", "name": "tool_name"}` | Require specific tool |

### Strict Tool Use

Enable guaranteed schema conformance:

```json
"strict": true
```

Ensures Claude's tool calls always match your schema exactly.

### JSON Mode for Structured Output

Use tools to enforce structured JSON output:
1. Define a single tool with your desired output schema
2. Set `tool_choice` to force that specific tool
3. Extract the `input` parameter as your structured data

---

## Best Practices

### Parameter Clarity
- Use unambiguous descriptions
- Provide concrete examples
- Specify expected formats (dates, addresses, units)

### Handling Missing Information
- Claude Opus recognizes missing required parameters and asks for clarification
- Claude Sonnet may infer values; provide context to guide reasoning

### Chain of Thought Prompting
For Claude Sonnet/Haiku:

> "Before calling a tool, analyze which tool is relevant and verify all required parameters are provided or inferable. If required values are missing, ask rather than guess."

### Error Handling
- Implement graceful fallbacks for tool failures
- Return informative error messages in `tool_result`
- Consider including context about partial failures

---

## Pricing Considerations

| Item | Cost |
|------|------|
| Tool use system prompt | 264-346 tokens |
| Client tools | Standard API pricing |
| Server tools | May incur additional fees |

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao implementar function calling em agentes
- Ao criar tools customizadas para workflows
- Ao integrar APIs externas via Claude
- Ao construir agentes que executam ações

**Tags**: claude, tool_use, function_calling, api, agents, json_schema
