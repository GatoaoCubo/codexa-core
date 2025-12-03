# CLAUDE.md - Project Laws

**Auto-loaded by Claude Code** | v2.0.0 | 2025-12-03

---

## IDENTITY

Meta-construction framework for building AI agent systems. Creates templates, agents, and workflows that build other artifacts.

---

## CORE LAWS

### LAW 1: DISTILLATION

> "Every document must be a universal template."

**Principle**: Remove brand-specific content, create reusable templates.

```
SPECIFIC → TEMPLATE
"codexa.app"  → {{BRAND_URL}}
#0D9488       → {{PRIMARY_COLOR}}
```

**Process**: CREATE → DISTILL → HYDRATE → DEPLOY

**Trigger**: `/codexa-distill <path>`

**Validation**: No hardcoded brands, URLs, or colors. Only `{{PLACEHOLDERS}}`.

See: [docs/PLACEHOLDERS.md](docs/PLACEHOLDERS.md)

---

### LAW 2: FRACTAL NAVIGATION

> "Each level reflects the structure below."

Every directory follows the trinity pattern:

```
PRIME.md        → Entry point (what)
INSTRUCTIONS.md → Operations (how)
README.md       → Details (reference)
```

**Navigate**: `/prime` (root), `/prime-{agent}` (domain)

**Example**:
```
codexa.app/
├── PRIME.md              ← System entry
├── agentes/
│   └── anuncio_agent/
│       ├── PRIME.md      ← Agent entry
│       ├── INSTRUCTIONS.md
│       └── README.md
```

---

### LAW 3: META-CONSTRUCTION

> "Build the thing that builds the thing."

1. **Meta > Instance** - Build builders, not artifacts
2. **Templates > One-offs** - Reusable patterns
3. **Discovery-First** - Find before building
4. **Quality Gates** - Validate every phase (≥7.0/10.0)

---

### LAW 4: AGENTIC DESIGN

> "Agents are autonomous specialists."

**Structure**:
- **Domain** - What it knows (iso_vectorstore/)
- **Workflows (ADWs)** - What it does (workflows/)
- **Prompts (HOPs)** - How it thinks (prompts/)
- **Outputs** - What it produces (USER_DOCS/)

**Composition**: Agents can invoke other agents via MCP or slash commands.

See: [docs/WORKFLOWS.md](docs/WORKFLOWS.md)

---

### LAW 5: ORDINAL SEQUENCING

> "Numbers encode purpose."

File numbering convention:

| Range | Category | Purpose |
|-------|----------|---------|
| 00-09 | Foundation | Entry points, PRIME, README |
| 10-49 | Execution | Core modules, HOPs |
| 50-99 | Meta | System-level, cross-agent |
| 100+ | Production | Main workflows (ADWs) |
| 200+ | Advanced | Parallel, multi-agent |

**Example**: `11_ADW_orchestrator.md` = Foundation orchestrator

---

### LAW 6: EXECUTION INTELLIGENCE

> "LLM chooses the optimal execution environment."

**Environments**:
```
Windows (default)     │  WSL/Ubuntu (when needed)
├── Node.js / npm     │  ├── Complex Python deps
├── Git operations    │  ├── Docker containers
├── MCP servers       │  ├── Shell scripts (.sh)
└── PowerShell        │  └── GNU tools
```

**Decision heuristics**:
- `.sh` files → WSL
- Docker → WSL
- Simple Python → Windows
- MCP servers → Windows

**Execution**: `python script.py` (Windows) or `wsl python script.py` (WSL)

---

### LAW 7: ERROR RECOVERY

> "Anticipate, handle, recover."

**Patterns**:

1. **Retry with backoff**: API failures, network issues
2. **Fallback**: Alternative paths when primary fails
3. **Graceful degradation**: Partial success > total failure
4. **Explicit errors**: Clear messages, actionable fixes

**Quality gate failure**:
```
IF score < 7.0:
  → Identify weak dimensions
  → Retry (max 2 attempts)
  → IF still failing → Flag for manual review
```

---

## TOOLS

### Navigation Commands
- `/prime` - System navigator
- `/prime-{agent}` - Domain specialist (e.g., `/prime-anuncio`)

### Meta-Construction Commands
- `/codexa-distill` - Distill docs to templates
- `/codexa-build-agent` - Create new agent
- `/codexa-build-prompt` - Create HOP
- `/codexa-orchestrate` - Multi-phase workflows

### MCP Servers

| Server | Purpose | Key Functions |
|--------|---------|---------------|
| scout | File discovery | `discover`, `smart_context`, `search` |
| codexa-commands | Slash commands | `list_commands`, `get_command`, `execute_prompt` |
| browser | Web interaction | Screenshots, extraction |
| voice | Audio I/O | Speech recognition, TTS |

---

## CONSTRAINTS

### NEVER
- Create documents with hardcoded brand content
- Skip quality validation (≥7.0/10.0)
- Modify core files without reading first
- Guess file paths - use Scout to discover

### ALWAYS
- Distill documents to templates before delivery
- Use `{{PLACEHOLDER}}` syntax (mustache format)
- Validate outputs against quality gates
- Follow fractal navigation patterns

---

## REFERENCES

| Document | Purpose |
|----------|---------|
| [docs/PLACEHOLDERS.md](docs/PLACEHOLDERS.md) | Complete placeholder table |
| [docs/WORKFLOWS.md](docs/WORKFLOWS.md) | ADW catalog (41 workflows) |
| [docs/API_KEYS_REFERENCE.md](docs/API_KEYS_REFERENCE.md) | External services config |
| [path_registry.json](path_registry.json) | Path placeholder definitions |

---

**Version**: 2.0.0 | **Type**: Project Laws (Auto-loaded)

---

## Changelog

- **v2.0.0** (2025-12-03): Redesign - added LAW 5/7, externalized tables, fixed contradictions
- **v1.1.0** (2025-12-01): Added LAW 6 (Execution Intelligence)
- **v1.0.0** (2025-11-20): Initial laws
