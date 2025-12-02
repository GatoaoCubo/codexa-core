# CODEXA Agent | Meta-Constructor & Multi-Agent System

**Version**: 2.5.0 | **Status**: Production-Ready
**Purpose**: Self-building meta-construction system with LLM integration

---

## Quick Start

```bash
# Show system info
python codexa.py info

# Run agent with task
python codexa.py agent run "Create a hello world script"

# Build new agent
python codexa.py build agent "Sentiment analysis agent"

# Validate HOPs
python codexa.py validate hop prompts/91_meta_build_agent_HOP.md
```

---

## What's New in v2.5.0

- **Phase 1-4**: 8 composable prompt layers + Multi-Agent System
- **Phase 5**: Code Quality Standards (CODE_STYLE_GUIDE, DESIGN_SYSTEM)
- **Phase 6**: ADW Suite v2.0 (Two-Phase Planning, Parallel Orchestration)
- **Phase 7**: Reference Documentation (PLATFORM_ANALYSIS, INTEGRATION_GUIDE)
- **Phase 8**: Comprehensive Test Suite (4 test modules)
- **Phase 9**: Production Deployment Ready
- **12 Leverage Points**: ADWs, Templates, Plans, Architecture, Tests, Documentation, Types, Standard Out, Tools, Prompt, Model, Context

---

## Navigation

| Document | Purpose |
|----------|---------|
| **[PRIME.md](PRIME.md)** | Philosophy & principles [READ FIRST] |
| **[STRUCTURE.md](STRUCTURE.md)** | Complete system map |
| **[INSTRUCTIONS.md](INSTRUCTIONS.md)** | AI operations guide |
| **[codexa.py](codexa.py)** | CLI entry point |

---

## Architecture Overview

```
codexa_agent/
├── codexa.py           # CLI entry point
├── src/                # Core runtime
│   ├── llm/           # LLM providers (Claude, OpenAI, Gemini)
│   ├── tools/         # File & bash tools
│   ├── runtime/       # Agent loop
│   └── auth/          # Security
├── builders/          # Construction tools (14 scripts)
├── validators/        # Quality gates (5 scripts)
├── prompts/           # HOPs + 8 composable layers
├── agents/            # 5 agent definitions
├── config/            # Configuration (paths, modes)
└── deployment/        # Docker + scripts
```

**Full map**: [STRUCTURE.md](STRUCTURE.md)

---

## Core Components

### LLM Providers

```python
from src import ProviderFactory, ModelType

provider = ProviderFactory.create_provider(model=ModelType.CLAUDE_SONNET)
```

| Provider | Models |
|----------|--------|
| Claude | opus, sonnet, haiku |
| OpenAI | gpt-4, gpt-4-turbo |
| Gemini | pro, 2.0 |

### Tool Execution

```python
from src import ToolExecutor

executor = ToolExecutor()
result = executor.execute_tool("read", {"file_path": "file.txt"})
```

| Tool | Purpose |
|------|---------|
| Read | Read files |
| Write | Write files |
| Edit | Edit files |
| Glob | Find files |
| Grep | Search content |
| Bash | Execute commands |

### Agent Runtime

```python
from src import create_agent

agent = create_agent("my_agent", "You are helpful.", provider="claude")
result = await agent.run("Hello!")
```

---

## Builders (14 tools)

| Builder | Purpose |
|---------|---------|
| `02_agent_meta_constructor.py` | 5-phase agent construction |
| `08_prompt_generator.py` | HOP generation (TAC-7) |
| `11_doc_sync_builder.py` | Documentation sync |
| `05_command_generator.py` | Slash commands |

**Usage**:
```bash
uv run builders/02_agent_meta_constructor.py "Agent description"
```

---

## Validators (5 tools)

| Validator | Purpose |
|-----------|---------|
| `07_hop_sync_validator.py` | TAC-7 compliance |
| `09_readme_validator.py` | Documentation |
| `12_doc_sync_validator.py` | Doc sync |
| `16_path_consistency_validator.py` | Path validation |

**Usage**:
```bash
python codexa.py validate all
```

---

## Prompt Layers (8 layers)

Composable layers for agent construction:

| Layer | Purpose |
|-------|---------|
| Identity | Agent role & capabilities |
| Operating Modes | 7 execution modes |
| Tool Usage | Tool definitions |
| Communication | User interaction |
| Code Conventions | Code style |
| Design System | Visual tokens |
| Steering Hooks | Behavior control |
| Workflows | ADW patterns |

**Location**: `prompts/layers/`

---

## Agent Definitions (5 agents)

| Agent | Mode | Purpose |
|-------|------|---------|
| Planning | READ_ONLY | Exploration & planning |
| Execution | FULL_WRITE | Implementation |
| Verification | READ_TEST | Testing & validation |
| Review | READ_ANALYSIS | Quality assurance |
| Orchestrator | COORDINATION | Multi-agent |

**Location**: `agents/`

---

## Configuration

### Paths

```python
from config.paths import PROJECT_ROOT, CODEXA_AGENT_DIR
```

### Agent Modes

7 operating modes defined in `config/agent_modes.yml`:
- PLANNING, EXECUTION, VERIFICATION, FIX, RESEARCH, ORCHESTRATION, REVIEW

### Environment

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

---

## Deployment

```bash
# Deploy with Docker
./deployment/scripts/deploy.sh deploy

# Health check
./deployment/scripts/healthcheck.sh
```

**Full guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## Metrics

| Component | Count |
|-----------|-------|
| Builders | 14 |
| Validators | 5 |
| HOPs | 5 |
| Prompt Layers | 8 |
| Agent Definitions | 5 |
| LLM Providers | 3 |
| Tools | 6 |
| Total Files | ~151 |
| Total Lines | ~15,000 |

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 2.0.0 | 2025-11-24 | Phase 3 complete, full integration |
| 1.3.0 | 2025-11-24 | Template Metaprompt Framework |
| 1.2.0 | 2025-11-16 | Path normalization |
| 1.0.0 | 2025-11-13 | Initial release |

---

## Related

- **Entry Points**: [PRIME.md](PRIME.md) | [STRUCTURE.md](STRUCTURE.md) | [codexa.py](codexa.py)
- **Docs**: [docs/](docs/) | [specs/](specs/)
- **Source**: [src/](src/) | [builders/](builders/)

---

**Build the thing that builds the thing.**
