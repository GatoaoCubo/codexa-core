# CODEXA AGENT - INSTRUCTIONS | Operational Guide for AI Assistants

**Version**: 1.2.0 | **Updated**: 2025-11-13

## 🎯 WHAT IS CODEXA AGENT?

**Meta-constructor** that builds the system that builds the system. Creates agents, prompts, commands, schemas using structured meta-construction philosophy.

**Core**: Meta-Construction (build builders) | Self-Improvement (analyze & enhance) | Orchestration (multi-phase ADW) | Validation (quality gates)

---

## 📚 CORE PRINCIPLES (Full details in PRIME.md)

**1. Meta > Instance** - Build builders not artifacts | Templates not instances | Example: Build meta-constructor not individual agents
**2. OPOP** - One-Prompt-One-Purpose | 1 HOP = 1 task | Compose don't duplicate
**3. [OPEN_VARIABLES]** - Intentional blanks (e.g., `[CREATIVE_NAME]`) | LLM fills creatively | Maintains structure
**4. $arguments-chaining** - Phase N output → Phase N+1 input | Explicit data flow | Traceable
**5. Isolation** - Self-contained agents | No hidden dependencies | Portable
**6. Trinity Output** - .md + .llm.json + .meta.json
**7. Information-Dense** - Keywords not sentences | MAX 1000 LINES/FILE
**8. ADW Pattern** - Plan>Code>Test>Review>Document

## 🏛️ ARCHITECTURE PILLARS

### 4 IN-AGENT Pillars (Construction)
**Contexto** - Domain knowledge, codebase, requirements | **Modelo** - LLM (GPT-4o+, Sonnet 4.5+), reasoning | **Tools** - Functions, integrations, validators | **Prompts** - HOPs, instructions, meta-formats

### 8 OUT-AGENT Pillars (Artifacts)
**Templates** - Reusable with [VARIABLES] | **Standard Output** - Trinity (.md/.llm.json/.meta.json) | **Types** - Information flow | **Documentation** - AI_DOCS + internal | **Tests** - Self-validating loops | **Architecture** - Easy navigation | **Plans** - Detailed ADW workflows | **ADWs** - 1-shot solutions

---

## 🎯 HOW TO USE CODEXA AGENT

### PITER Framework (Execution Pattern)

**P**rompt - Entry instructions + context
**I**dentify - Find relevant files, dependencies, patterns
**T**rigger - Execute builders, commands, workflows
**E**nvironment - Check context, tools, permissions
**R**eview - Validate outputs, quality gates, iterate

### When to Use

**USE** for: Build agents | Create builders (meta-meta) | Generate HOPs | Create commands | Orchestrate ADW | Self-improvement

**DON'T USE** for: Domain tasks (specialized agents) | One-offs (direct code) | Simple file ops (basic tools)

### Decision Tree
```
Need to build? → BUILDER/TOOL? → CODEXA | AGENT? → 02_agent_meta_constructor.py
              → PROMPT/HOP? → 08_prompt_generator.py | COMMAND? → 05_command_generator.py
              → Domain code? → Specialized agent
```

---

## 🔧 BUILDER WORKFLOWS

### Workflow 1: Build Agent (5-Phase ADW) ⭐

```bash
uv run builders/02_agent_meta_constructor.py "Agent description"
```

**Phases**: Plan ([VARIABLES]) → Build ($plan) → Test ($artifacts) → Review ($test_results) → Document ($all_context)
**Output**: 8 artifacts (README, config, schemas, prompts, etc.)

### Workflow 2: Build HOP (TAC-7 Framework)

```bash
uv run builders/08_prompt_generator.py
```

**Structure**: MODULE_METADATA (id, version, purpose) → INPUT_CONTRACT ($variables + types + validation) → OUTPUT_CONTRACT (structure + format) → TASK (role, objective, constraints) → STEPS (3-7 actionable) → VALIDATION (quality gates ≥7.0) → CONTEXT (chaining, assumptions)

**Standards**: All $variables typed | All inputs validated | Quality score ≥7.0/10.0

### Workflow 3: Orchestrate Multi-Phase (ADW)

**Pattern**: Define workflow_spec → Specify phase dependencies → Configure $arguments chaining → Execute → Validate each phase

---

## 📝 WORKING WITH HOPs

### Reading HOPs (4 Key Sections)

**INPUT_CONTRACT** - What module needs | **OUTPUT_CONTRACT** - What it produces | **STEPS** - What it does | **VALIDATION** - Quality requirements

### Writing HOPs (TAC-7 Template)

```markdown
# {id}_HOP | {Title}
MODULE_METADATA: id, version, purpose, dependencies, category
INPUT_CONTRACT: $variables (type: string) + description + validation + example
OUTPUT_CONTRACT: $outputs (type: object) + format + structure + validation
TASK: Role, objective, standards, constraints
STEPS: 3-7 numbered steps (H3 headers) with actions
VALIDATION: ✅ Checks (verify method + fix if fails) | Quality score ≥7.0/10.0
CONTEXT: Usage, upstream/downstream, $arguments chaining, assumptions
```

### Variable Naming ($prefix notation)

`$plan` (strategic) | `$artifacts` (generated) | `$test_results` (validation) | `$workflow_log` (execution) | `$context` (previous phases)

---

## ✅ VALIDATION & QUALITY

### Validators (3 Scripts)

**07_hop_sync_validator.py** - TAC-7 compliance | **09_readme_validator.py** - Documentation standards | **10_taxonomy_validator.py** - Registry consistency

```bash
uv run validators/07_hop_sync_validator.py [file.md]  # HOP validation
uv run validators/09_readme_validator.py [README.md]  # Docs validation
uv run validators/10_taxonomy_validator.py            # Taxonomy check
```

### Quality Gates (All Required)

✅ Structure (all sections) | ✅ Type consistency ($vars typed) | ✅ No orphans (all $vars defined) | ✅ Validation rules present | ✅ Quality ≥7.0/10.0 | ✅ MAX 1000 LINES

---

## 🔄 SELF-IMPROVEMENT LOOP

**Pattern**: Analyze (Scout patterns) → Identify (opportunities) → Plan (CODEXA design) → Build (execute) → Validate (quality) → Integrate (merge) → Document (capture) → Repeat

**How**: Read own HOPs → Read PRIME.md → Apply principles → Consolidate (remove duplication) → Implement (transform stubs)

---

## 🎨 BEST PRACTICES (Rules)

**DO**: Read PRIME.md/HOPs first | Use templates | Validate incrementally | Trinity Output | Embrace [VARIABLES] | Chain $arguments | Build for reuse | Information-dense | MAX 1000 LINES

**DON'T**: Build instances (build builders) | Skip validation | Use undefined $vars | Create orphans | Ignore quality ≥7.0 | Exceed 1000 lines

---

## 📊 STRUCTURE (Easy Navigation)

```
codexa_agent/
├── builders/              # 7 tools | adw_modules/ (agent.py, scout_integration.py, utils.py)
│   ├── 02_agent_meta_constructor.py  ⭐ CORE 5-phase
│   ├── 08_prompt_generator.py       # HOPs
│   └── 05_command_generator.py      # Commands
├── validators/            # 3 QA tools (07_hop, 09_readme, 10_taxonomy)
├── prompts/              # HOPs (TAC-7)
├── workflows/            # ADW workflows
├── PRIME.md             # Philosophy [READ FIRST]
├── INSTRUCTIONS.md      # [THIS FILE] Operations guide
└── README.md            # Structure & metrics
```

---

## 🚀 QUICK START

### Build First Agent (PITER)
```bash
# P: Read PRIME.md | I: Check prompts/*_HOP.md examples
# T: uv run builders/02_agent_meta_constructor.py "Research agent description"
# E: Verify 8 artifacts created | R: uv run validators/09_readme_validator.py [output/README.md]
```

### Create First HOP
```bash
# Read TAC-7 in any HOP → Write following template → Validate
uv run validators/07_hop_sync_validator.py [your_HOP.md]
```

---

## 📖 KEY FILES (Entry Points)

**Start**: PRIME.md (philosophy) | README.md (structure) | prompts/*_HOP.md (TAC-7 examples)
**Build Agent**: prompts/91_* + builders/02_* | **Build HOP**: prompts/94_* + builders/08_* | **Orchestrate**: prompts/96_* + workflows/97_*

---

## 🎯 STATUS & TIPS (v1.2.0)

**Functional**: ✅ 7 builders | ✅ 3 validators | ✅ HOPs (TAC-7) | ✅ ADW workflows | ✅ Core modules

**Pro Tips**: Read first build second | Use templates | Validate early | Think meta (builder not instance) | Chain $arguments | Quality ≥7.0 | Self-improve (CODEXA improves CODEXA)

**Troubleshooting**: Module not found → Check adw_modules/ | Orphaned $var → Define in INPUT_CONTRACT | Quality <7.0 → Review VALIDATION | Phase fails → Check $arguments chaining

---

**Version**: 1.2.0
**Created**: 2025-11-13
**Maintainer**: CODEXA Team
**Related**: PRIME.md (philosophy), README.md (structure), All HOPs (examples)
