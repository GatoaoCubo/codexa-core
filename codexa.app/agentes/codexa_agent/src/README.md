# CODEXA Core Runtime

**Version**: 3.1.0
**Purpose**: Core runtime for LLM agents with tool execution

---

## Overview

This is the **production runtime** for CODEXA agents. It provides:

- **LLM Integration**: Claude, OpenAI, Gemini providers
- **Tool Execution**: File operations, bash commands
- **Agent Runtime**: Autonomous agent loop
- **Security**: Rate limiting, audit logging, secrets

---

## Quick Start

```python
from src import create_agent

# Create and run agent
agent = create_agent(
    agent_id="my_agent",
    system_prompt="You are a helpful assistant.",
    provider="claude"
)

result = await agent.run("Hello!")
print(result.final_response)
```

---

## Modules

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `llm/` | LLM providers | `ProviderFactory`, `ClaudeProvider` |
| `tools/` | Tool execution | `ToolExecutor`, `FileTools`, `BashTools` |
| `runtime/` | Agent loop | `AgentRuntime`, `PromptLoader` |
| `auth/` | Security | `RateLimiter`, `AuditLogger`, `SecretsManager` |

---

## Usage

### LLM Providers

```python
from src.llm import ProviderFactory, ModelType

provider = ProviderFactory.create_provider(
    model=ModelType.CLAUDE_SONNET
)

response = await provider.complete("Hello!")
```

### Tool Execution

```python
from src.tools import ToolExecutor, ToolPermission

executor = ToolExecutor()
result = executor.execute_tool(
    "read",
    {"file_path": "/path/to/file"},
    permission=permission
)
```

### Agent Runtime

```python
from src.runtime import AgentRuntime, AgentConfig

config = AgentConfig(
    agent_id="my_agent",
    system_prompt="...",
    llm_provider=provider,
    tool_executor=executor,
)

runtime = AgentRuntime(config=config)
state = await runtime.run("task")
```

---

## Architecture

```
src/
├── __init__.py      # Unified exports
├── llm/             # LLM providers
├── tools/           # Tool execution
├── runtime/         # Agent loop
├── auth/            # Security
├── orchestrator.py  # Multi-agent
└── workflow_executor.py
```

---

**See also**: [STRUCTURE.md](../STRUCTURE.md) | [docs/PHASE3_INTEGRATION_GUIDE.md](../docs/PHASE3_INTEGRATION_GUIDE.md)
