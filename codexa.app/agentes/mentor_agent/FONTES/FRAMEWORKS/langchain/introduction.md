# LangChain: Comprehensive Overview Guide

**Fonte**: docs.langchain.com
**Atualizado**: 2025-12-02
**Categoria**: FRAMEWORKS
**Plataforma**: LangChain

---

## What is LangChain?

LangChain is a framework designed to simplify the development of applications powered by large language models. It enables developers to quickly integrate multiple LLM providers—including OpenAI, Anthropic, and Google—with minimal code.

> "Connect to OpenAI, Anthropic, Google, and more in under 10 lines of code."

---

## Core Architecture

### Foundation
LangChain agents are built on top of **LangGraph**, a lower-level orchestration framework that provides robust capabilities while maintaining ease of use.

### Key Components

| Component | Description |
|-----------|-------------|
| **Standard Model Interface** | Abstracts provider-specific API differences |
| **Agent Abstraction** | Pre-built architecture balancing simplicity with flexibility |
| **Built-in Capabilities** | Durable execution, streaming, human-in-the-loop, persistence |

---

## Quick Start Example

```python
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

---

## Primary Benefits

| Benefit | Description |
|---------|-------------|
| **Simplified Integration** | Standardized interfaces for multiple LLM providers |
| **Rapid Development** | Create agents with minimal boilerplate |
| **Enterprise Features** | Observability, persistence, durable execution |
| **Debugging** | LangSmith integration for tracing and monitoring |

---

## LangChain vs. LangGraph

### Choose LangChain for:
- Rapid prototyping
- Standard agent architectures
- Quick time-to-market projects

### Choose LangGraph for:
- Complex deterministic + agentic workflows
- Heavy customization requirements
- Fine-grained latency control

---

## Core Concepts

### Agents
Autonomous entities that use LLMs to decide actions and execute tools.

### Chains
Sequences of operations that process inputs through multiple steps.

### Tools
Functions that agents can call to interact with external systems.

### Memory
Systems for persisting conversation context across interactions.

### Retrieval
Integration with vector stores for RAG (Retrieval-Augmented Generation).

---

## Installation

```bash
# Basic installation
pip install langchain

# With specific provider
pip install "langchain[anthropic]"
pip install "langchain[openai]"
```

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao construir agentes autônomos
- Ao implementar RAG (Retrieval-Augmented Generation)
- Ao orquestrar múltiplas chamadas LLM
- Ao criar chains de processamento

**Tags**: langchain, agents, chains, rag, tools, memory, python
