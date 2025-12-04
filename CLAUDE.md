# CLAUDE.md - Project Laws

**Auto-loaded by Claude Code** | v2.1.0 | 2025-12-03

---

## IDENTITY

Meta-construction framework for building AI agent systems. Creates templates, agents, and workflows that build other artifacts. **LLM-first**: Laws are guidelines for autonomous execution, not rigid rules.

---

## CORE LAWS

### LAW 1: DISTILLATION

> "Documents for external use should work for any brand."

**Guideline**: When creating deliverables, distill to `{{PLACEHOLDERS}}` for reusability.

```
"codexa.app"  → {{BRAND_URL}}
#0D9488       → {{PRIMARY_COLOR}}
```

**Decision Heuristics**:
| Distill | Skip |
|---------|------|
| Marketing/sales materials | Internal workflows (ADWs, HOPs) |
| Course/content templates | System config (MCP, paths) |
| Multi-brand deliverables | Drafts/prototypes |

**Trigger**: `/flow distill path/to/file.md`

**Reference**: [docs/PLACEHOLDERS.md](docs/PLACEHOLDERS.md)

---

### LAW 2: FRACTAL NAVIGATION

> "Start with PRIME, drill down as needed."

**Trinity Pattern** (at every level):
```
PRIME.md        → Entry point (what/when/why) ← READ FIRST
INSTRUCTIONS.md → Operations (how to execute)
README.md       → Reference (architecture, details)
```

**Decision Tree**:
1. New to domain? → Read `PRIME.md` (2min context)
2. Need to execute? → Read `INSTRUCTIONS.md`
3. Need deep details? → Read `README.md`
4. Files missing? → `mcp__scout__smart_context`

**Commands**: `/prime` (root), `/prime-{agent}` (domain)

---

### LAW 3: META-CONSTRUCTION

> "Build the thing that builds the thing."

**Decision Heuristics** (when to go meta):

| Signal | Go Meta | Do Direct |
|--------|---------|-----------|
| Repetition | Task repeats 3+ times | One-off task |
| Scale | 5+ similar items | 1-2 items |
| Similarity | 80%+ overlap | Unique requirements |

**Pattern**: `1 Template → N Plans → M Results`

**Standards**:
- **Discovery-First**: Find existing templates before building new
- **Quality Gate**: Validate outputs ≥7.0/10.0
- **$arguments**: Chain outputs between phases

**Triggers**: `/codexa-build-agent`, `/codexa-build-prompt`

---

### LAW 4: AGENTIC DESIGN

> "Agents are specialists. Choose by task, compose by outcome."

**Quick Selection**:
| Need | Agent | Trigger |
|------|-------|---------|
| Product copy (BR) | anuncio_agent | `/prime-anuncio` |
| Market research | pesquisa_agent | `/prime-pesquisa` |
| Brand strategy | marca_agent | `/prime-marca` |
| Images | photo_agent | `/prime-photo` |
| Videos | video_agent | `/prime-video` |
| Courses | curso_agent | `/prime-curso` |
| System building | codexa_agent | `/codexa-*` |
| File discovery | scout_agent | `mcp__scout__*` |

**Agent Structure**:
- `PRIME.md` - Identity (read first)
- `iso_vectorstore/` - Knowledge base
- `workflows/` - ADWs (what it does)
- `prompts/` - HOPs (how it thinks)

**Composition**: Sequential (`/prime-pesquisa → /prime-anuncio → /prime-photo`) or parallel (`/spawn`)

**Discovery**: `mcp__scout__discover("task description")` when uncertain.

---

### LAW 5: ORDINAL SEQUENCING

> "Numbers signal intent, not rules."

**Quick Lookup**:
```
00-09 → Foundation (PRIME, QUICKSTART) ← Read first
10-19 → Core HOPs (domain prompts)
20-49 → Context (changelog, reference)
100+  → Workflows (ADWs, production)
200+  → Advanced (parallel, multi-phase)
```

**Examples**:
- `04_README.md` = Foundation doc
- `11_ADW_orchestrator.md` = Core orchestrator
- `100_ADW_RUN_PHOTO.md` = Production workflow

**Not following convention?** Read anyway. Use Scout to find by intent.

---

### LAW 6: EXECUTION INTELLIGENCE

> "Try Windows first. WSL when needed. Let errors guide you."

**Environments**:
```
WINDOWS (default)          WSL (when needed)
├── Python (simple)        ├── Python (numpy, torch)
├── Node.js / npm          ├── Bash scripts (.sh)
├── Git, PowerShell        ├── Docker
└── MCP servers            └── GNU tools
```

**Decision** (3-second rule):
1. Default to Windows (faster)
2. Switch to WSL if: `.sh` file, Docker, complex Python deps, Linux tools
3. Fallback: `cmd` → `wsl cmd` → ask user

**Execution**: `python script.py` (Win) or `wsl python script.py` (WSL)

---

### LAW 7: ERROR RECOVERY

> "Retry, fallback, fail fast, or degrade gracefully."

**Error Categories**:
```
RECOVERABLE (retry)        FATAL (fail fast)
├── API timeout            ├── Missing env var
├── Rate limit (429)       ├── Invalid config
├── Network hiccup         ├── Auth failure
└── File lock              └── Corrupt data
```

**Strategies**:
1. **Retry**: Transient errors → backoff 1-3x
2. **Fallback**: Alternative path exists
3. **Fail Fast**: Unrecoverable → exit with clear message
4. **Degrade**: Partial success > total failure (18/22 OK → continue)

**Quality Gate**:
```
IF score < 7.0 → Retry once → IF still < 7.0 → Flag for review
```

**Logging**: Always log errors with context. Never fail silently.

---

## TOOLS

### Navigation
- `/prime` - System navigator
- `/prime-{agent}` - Domain specialist

### Meta-Construction
- `/codexa-build-agent` - Create agent
- `/codexa-build-prompt` - Create HOP
- `/codexa-orchestrate` - Multi-phase workflows

### Task Pipeline
- `/flow plan "task"` - Create execution plan
- `/flow do` - Execute approved plan
- `/flow distill file.md` - Convert to template
- `/handoff` - Generate cross-chat transfer block

### Parallel Execution
- `/spawn` - Launch N agents in parallel (max 10)
  ```
  /spawn
  1. explore: find ADW files
  2. explore: find HOP files
  3. plan: design new feature
  ```
- `/spawn preset:discovery` - 10 scouts for full path audit
- `/spawn preset:health` - 5 validators for LAW compliance
- `/spawn model:haiku` - Use fast model for simple searches

### Agent Chains
Agents connect in pipelines. Each output feeds the next input.

```
marca → ALL (brand hub)
pesquisa → anuncio → photo
curso → video → voice
```

**Chain Patterns**:
- Sequential: `/pesquisa` → `/handoff` → `/anuncio`
- Parallel: `/spawn` with multiple agents
- Full Pipeline: `/flow auto "full content for product X"`

**Reference**: [docs/AGENT_CHAINS.md](docs/AGENT_CHAINS.md)

### MCP Servers
| Server | Purpose | Key Functions |
|--------|---------|---------------|
| scout | File discovery | `discover`, `smart_context`, `search` |
| codexa-commands | Slash commands | `list_commands`, `execute_prompt` |
| browser | Web interaction | Screenshots, extraction |
| voice | Audio I/O | Speech recognition, TTS |

---

## CONSTRAINTS

### NEVER
- Hardcode brand content in deliverables
- Skip quality validation (≥7.0)
- Guess file paths (use Scout)
- Fail silently (always log)

### ALWAYS
- Start with PRIME.md for new domains
- Distill deliverables to templates
- Use `{{PLACEHOLDER}}` syntax
- Log errors with context

---

## REFERENCES

| Document | Purpose |
|----------|---------|
| [docs/PLACEHOLDERS.md](docs/PLACEHOLDERS.md) | Placeholder definitions |
| [docs/WORKFLOWS.md](docs/WORKFLOWS.md) | ADW catalog (41 workflows) |
| [docs/AGENT_CHAINS.md](docs/AGENT_CHAINS.md) | Agent connections & pipelines |
| [docs/API_KEYS_REFERENCE.md](docs/API_KEYS_REFERENCE.md) | External services |
| [docs/COMMERCIALIZATION_ROADMAP.md](docs/COMMERCIALIZATION_ROADMAP.md) | Business strategy & monetization |
| [path_registry.json](path_registry.json) | Path placeholders |

---

**Version**: 2.4.0 | **Type**: Project Laws (Auto-loaded)

## Changelog
- **v2.4.0** (2025-12-03): Fixed trigger references (`/prime-*`), added Task Pipeline section
- **v2.3.0** (2025-12-03): Added Agent Chains section and AGENT_CHAINS.md reference
- **v2.2.0** (2025-12-03): Added /spawn parallel execution tool with presets
- **v2.1.0** (2025-12-03): LLM-optimized LAWs with decision heuristics, non-rigid guidelines
- **v2.0.0** (2025-12-03): Redesign - added LAW 5/7, externalized tables
- **v1.0.0** (2025-11-20): Initial laws
