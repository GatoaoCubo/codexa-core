# CODEXA Agent - System Structure

**Version**: 2.5.0
**Last Updated**: 2025-11-25
**Total Files**: ~151 | **Total Directories**: 40

---

## Quick Navigation

| What you want | Where to find it |
|---------------|------------------|
| Philosophy & Principles | `PRIME.md` |
| Getting Started | `README.md` |
| Operations Guide | `INSTRUCTIONS.md` |
| **This Map** | `STRUCTURE.md` |
| Entry Point | `codexa.py` |

---

## Directory Map

```
codexa_agent/
│
├── 📄 ENTRY POINTS
│   ├── codexa.py           # Single CLI entry point
│   ├── PRIME.md            # Philosophy [READ FIRST]
│   ├── README.md           # Overview & quick start
│   ├── INSTRUCTIONS.md     # AI operations guide
│   └── STRUCTURE.md        # This file - system map
│
├── 🧠 src/                 # CORE RUNTIME (Phase 3)
│   ├── __init__.py         # Unified exports
│   ├── llm/                # LLM Providers
│   │   ├── provider.py     # Abstract interface
│   │   ├── claude_provider.py
│   │   ├── openai_provider.py
│   │   ├── gemini_provider.py
│   │   ├── cost_tracker.py
│   │   └── provider_factory.py
│   │
│   ├── tools/              # Tool Execution
│   │   ├── executor.py     # Tool orchestration
│   │   ├── file_tools.py   # Read, Write, Edit, Glob, Grep
│   │   ├── bash_tools.py   # Command execution
│   │   └── permissions.py  # Access control
│   │
│   ├── runtime/            # Agent Runtime
│   │   ├── agent_runtime.py    # Main agent loop
│   │   └── prompt_loader.py    # Prompt composition
│   │
│   ├── auth/               # Authentication & Security
│   │   ├── api_keys.py     # API key management
│   │   ├── rate_limiter.py # Token bucket rate limiting
│   │   ├── audit_log.py    # Audit trail
│   │   └── secrets.py      # Secrets management
│   │
│   ├── orchestrator.py     # Multi-agent orchestration
│   └── workflow_executor.py # Workflow execution
│
├── 🏗️ builders/            # CONSTRUCTION TOOLS
│   ├── 01_agent_builder.py
│   ├── 02_agent_meta_constructor.py  ⭐ Core 5-phase builder
│   ├── 03_build_task.py
│   ├── 04_chore_task.py
│   ├── 05_command_generator.py
│   ├── 06_cron_orchestrator.py
│   ├── 08_prompt_generator.py
│   ├── 11_doc_sync_builder.py
│   ├── 13_fractal_nav_sync.py
│   ├── 14_tac7_header_generator.py
│   ├── 15_trinity_output_generator.py
│   ├── 17_adw_intelligent_constructor.py
│   ├── multi_agent_orchestrator.py
│   ├── task_boundary.py
│   └── adw_modules/        # Shared modules
│       ├── agent.py
│       ├── scout_integration.py
│       └── utils.py
│
├── ✅ validators/          # QUALITY GATES
│   ├── 07_hop_sync_validator.py      # TAC-7 compliance
│   ├── 09_readme_validator.py        # Documentation
│   ├── 10_taxonomy_validator.py      # Registry
│   ├── 12_doc_sync_validator.py      # Doc sync
│   └── 16_path_consistency_validator.py
│
├── 📝 prompts/             # PROMPTS & HOPs
│   ├── layers/             # Composable Layers (Phase 1)
│   │   ├── 01_identity_layer.md
│   │   ├── 02_operating_modes.md
│   │   ├── 03_tool_usage_layer.md
│   │   ├── 04_communication_layer.md
│   │   ├── 05_code_conventions.md
│   │   ├── 06_design_system.md
│   │   ├── 07_steering_hooks.md
│   │   ├── 08_workflows.md
│   │   └── composer.py     # Layer composition
│   │
│   ├── 91_meta_build_agent_HOP.md
│   ├── 92_meta_chore_plan_HOP.md
│   ├── 93_meta_review_HOP.md
│   ├── 94_meta_build_prompt_HOP.md
│   └── 96_meta_orchestrate_HOP.md
│
├── 🤖 agents/              # AGENT DEFINITIONS (Phase 2)
│   ├── planning_agent.md   # Read-only exploration
│   ├── execution_agent.md  # Write access
│   ├── verification_agent.md
│   ├── review_agent.md
│   ├── orchestrator.md
│   ├── _archive/           # Old builds
│   ├── _examples/          # Examples
│   └── generated/          # Generated agents
│
├── 🔄 workflows/           # ADW WORKFLOWS
│   ├── 97_ADW_NEW_AGENT_WORKFLOW.md
│   ├── 98_ADW_CONSOLIDATION_WORKFLOW.md
│   ├── 99_ADW_SYSTEM_UPGRADE_WORKFLOW.md
│   ├── 100_ADW_DOC_SYNC_WORKFLOW.md
│   └── reports/
│
├── ⚙️ config/              # CONFIGURATION
│   ├── paths.py            # Centralized path constants
│   ├── agent_modes.yml     # Operating modes (7 modes)
│   ├── artifact_schemas.yml
│   └── prompt_layers.yml   # Layer composition config
│
├── 📦 artifacts/           # ARTIFACT SYSTEM (Phase 3)
│   ├── generators/
│   │   ├── plan_generator.py
│   │   ├── report_generator.py
│   │   └── walkthrough_generator.py
│   ├── templates/
│   │   ├── implementation_plan.jinja2
│   │   ├── execution_report.jinja2
│   │   ├── verification_report.jinja2
│   │   └── review_report.jinja2
│   └── validators/
│       ├── plan_validator.py
│       └── report_validator.py
│
├── 🚀 deployment/          # PRODUCTION DEPLOYMENT
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── config/
│   │   └── production.yml
│   └── scripts/
│       ├── deploy.sh
│       └── healthcheck.sh
│
├── 📚 docs/                # DOCUMENTATION
│   ├── DEPLOYMENT.md
│   ├── MULTIAGENT_ARCHITECTURE.md
│   ├── PHASE2_SUMMARY.md
│   ├── PHASE3_INTEGRATION_GUIDE.md
│   ├── PHASE3_PLAN.md
│   └── PHASE3_SUMMARY.md
│
├── 📋 specs/               # SPECIFICATIONS & PLANS
│   ├── MASTER_PLAN_self_improvement_v2.md
│   └── PHASE_2_COMPLETION_REPORT.md
│
├── 🧪 tests/               # TESTS
│   └── integration/
│       └── test_full_integration.py
│
├── 📁 commands/            # SLASH COMMANDS
│   ├── 90_codexa_when_to_use.md
│   ├── 91_codexa_build_agent.md
│   ├── 92_codexa_build_command.md
│   ├── 93_codexa_build_mcp.md
│   ├── 94_codexa_build_prompt.md
│   ├── 95_codexa_build_schema.md
│   ├── 96_codexa_orchestrate.md
│   └── 98_codexa_cleanup.md
│
├── 📁 templates/           # DOCUMENT TEMPLATES
│   ├── REPORT_STANDARD.md
│   └── docs/
│
├── 📁 examples/            # CODE EXAMPLES
│   ├── simple_agent.py
│   └── multi_provider.py
│
├── 📁 outputs/             # GENERATED OUTPUTS
├── 📁 logs/                # LOG FILES
└── 📁 iso_vectorstore/     # VECTOR STORAGE
```

---

## Component Map

### By Phase (Self-Improvement Journey)

| Phase | Component | Location | Status |
|-------|-----------|----------|--------|
| 1 | Prompt Layers | `prompts/layers/` | ✅ Complete |
| 2 | Multi-Agent System | `agents/*.md` | ✅ Complete |
| 2 | Task Boundary | `builders/task_boundary.py` | ✅ Complete |
| 2 | Agent Modes | `config/agent_modes.yml` | ✅ Complete |
| 3 | LLM Providers | `src/llm/` | ✅ Complete |
| 3 | Tool Execution | `src/tools/` | ✅ Complete |
| 3 | Agent Runtime | `src/runtime/` | ✅ Complete |
| 3 | Authentication | `src/auth/` | ✅ Complete |
| 3 | Artifact System | `artifacts/` | ✅ Complete |
| 3 | Deployment | `deployment/` | ✅ Complete |

### By Function

| Function | Files | Entry Point |
|----------|-------|-------------|
| Build Agent | `builders/02_*.py` | `codexa.py build agent` |
| Build HOP | `builders/08_*.py` | `codexa.py build prompt` |
| Validate | `validators/*.py` | `codexa.py validate` |
| Run Agent | `src/runtime/` | `codexa.py agent run` |
| Deploy | `deployment/` | `deployment/scripts/deploy.sh` |

---

## Key Files Quick Reference

### Must Read (In Order)

1. **PRIME.md** - Philosophy & principles
2. **STRUCTURE.md** - This file
3. **README.md** - Quick start
4. **INSTRUCTIONS.md** - AI operations

### Core Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| `codexa.py` | CLI | `python codexa.py <cmd>` |
| `src/__init__.py` | Python API | `from src import create_agent` |
| `builders/02_*.py` | Agent builder | `uv run builders/02_*.py` |

### Configuration

| File | Purpose |
|------|---------|
| `config/paths.py` | All path constants |
| `config/agent_modes.yml` | Operating modes |
| `config/prompt_layers.yml` | Layer composition |
| `.env` | API keys (not committed) |

---

## Integration Points

### How Components Connect

```
USER REQUEST
     │
     ▼
codexa.py (CLI)
     │
     ├──► src/runtime/agent_runtime.py
     │         │
     │         ├──► src/llm/ (LLM calls)
     │         │
     │         ├──► src/tools/ (tool execution)
     │         │
     │         └──► src/auth/ (rate limit, audit)
     │
     └──► builders/ (construction)
               │
               └──► prompts/layers/ (composition)
```

### Import Patterns

```python
# From codexa.py or any script
from src import (
    create_agent,           # Quick agent creation
    AgentRuntime,           # Full control
    ProviderFactory,        # LLM providers
    ToolExecutor,           # Tools
    get_rate_limiter,       # Rate limiting
)

# From config
from config.paths import (
    PROJECT_ROOT,
    CODEXA_AGENT_DIR,
    PATH_PROMPTS,
)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-11-24 | Phase 3 complete, full integration |
| 1.3.0 | 2025-11-24 | Template Metaprompt Framework |
| 1.2.0 | 2025-11-16 | Path normalization |
| 1.0.0 | 2025-11-13 | Initial structure |

---

**Navigation**: [PRIME.md](PRIME.md) | [README.md](README.md) | [INSTRUCTIONS.md](INSTRUCTIONS.md)
