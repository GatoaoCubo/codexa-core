# CODEXA AGENT - INSTRUCTIONS | Operational Guide for AI Assistants

**Version**: 2.6.0 | **Updated**: 2025-12-05

## 🎯 WHAT IS CODEXA AGENT?

**Meta-constructor** that builds the system that builds the system. Creates agents, prompts, commands, schemas using structured meta-construction philosophy.

**Core**: Meta-Construction (build builders) | Self-Improvement (analyze & enhance) | Orchestration (multi-phase ADW) | Validation (quality gates)

---

## 📚 CORE PRINCIPLES (Full details in PRIME.md)

**1. Scout-First (LAW 9)** - Discover before create | CRUD Priority: Delete > Update > Read > Create | Consolidate before duplicate
**2. Meta > Instance** - Build builders not artifacts | Templates not instances | Example: Build meta-constructor not individual agents
**3. OPOP** - One-Prompt-One-Purpose | 1 HOP = 1 task | Compose don't duplicate
**4. [OPEN_VARIABLES]** - Intentional blanks (e.g., `[CREATIVE_NAME]`) | LLM fills creatively | Maintains structure
**5. $arguments-chaining** - Phase N output → Phase N+1 input | Explicit data flow | Traceable
**6. Isolation** - Self-contained agents | No hidden dependencies | Portable
**7. Trinity Output** - .md + .llm.json + .meta.json
**8. Information-Dense** - Keywords not sentences | MAX 1000 LINES/FILE
**9. ADW Pattern** - Plan>Code>Test>Review>Document
**10. Feedback Loops** - Test → Validate → Fix → Repeat | Self-correcting systems

## 🏛️ ARCHITECTURE PILLARS

### 4 IN-AGENT Pillars (Construction)
**Contexto** - Domain knowledge, codebase, requirements | **Modelo** - LLM (GPT-4o+, Sonnet 4.5+), reasoning | **Tools** - Functions, integrations, validators | **Prompts** - HOPs, instructions, meta-formats

### 8 OUT-AGENT Pillars (Artifacts)
**Templates** - Reusable with [VARIABLES] | **Standard Output** - Trinity (.md/.llm.json/.meta.json) | **Types** - Information flow | **Documentation** - AI_DOCS + internal | **Tests** - Self-validating loops | **Architecture** - Easy navigation | **Plans** - Detailed ADW workflows | **ADWs** - 1-shot solutions

---

## 🎯 HOW TO USE CODEXA AGENT

### Scout-First Workflow (LAW 9) ⭐ NEW

**Pattern**: Scout → Analyze Consolidatables → CRUD Priority → Execute

```bash
# 0. SCOUT FIRST (MANDATORY - LAW 9)
# Before ANY task, spawn scouts to find relevant files and duplicates
/spawn model:haiku
1. explore: find files relevant to "{task description}"
2. explore: find consolidatable duplicates in affected directories

# 1. ANALYZE: Review scout findings
# - Existing files to UPDATE (not duplicate)
# - Similar files to CONSOLIDATE
# - Orphaned files to DELETE

# 2. BUILD: Execute construction (5-phase agent / 3-phase workflow)
uv run builders/02_agent_meta_constructor.py "Agent description"

# 3. VALIDATE: Quality gates
uv run validators/07_hop_sync_validator.py [file.md]
```

**CRUD Priority** (highest to lowest):
1. **DELETE** - Remove stale, orphaned, duplicate files first
2. **UPDATE** - Modify existing files to match new requirements
3. **READ** - Use existing content as foundation
4. **CREATE** - Only when scouts confirm nothing exists

### PITER Framework (Execution Pattern)

**P**rompt - Entry instructions + context
**I**dentify - Find relevant files, dependencies, patterns (SCOUT FIRST!)
**T**rigger - Execute builders, commands, workflows
**E**nvironment - Check context, tools, permissions
**R**eview - Validate outputs, quality gates, iterate

### When to Use

**USE** for: Build agents | Create builders (meta-meta) | Generate HOPs | Create commands | Orchestrate ADW | Self-improvement | Documentation sync | Consolidation workflows

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

### Workflow 3: Sync Documentation (ADW-100) ⭐

```bash
# Automatic documentation synchronization across ALL agents
python builders/11_doc_sync_builder.py --mode auto_fix

# Audit only (no changes)
python builders/11_doc_sync_builder.py --mode audit_only

# Validate results
python validators/12_doc_sync_validator.py --all
```

**Output**: Missing INSTRUCTIONS/SETUP created | Versions synchronized | Quality score improvement: avg +69%

### Workflow 4: Orchestrate Multi-Phase (ADW)

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

### Validators (9 Scripts)

**Primary Validators**:
- `12_doc_sync_validator.py` ⭐ - Full documentation synchronization validation
- `13_code_quality_validator.py` ⭐ - Code style guide compliance (naming, types, docs)
- `07_hop_sync_validator.py` - HOP TAC-7 compliance
- `09_readme_validator.py` - Documentation standards
- `10_taxonomy_validator.py` - Registry consistency
- `16_path_consistency_validator.py` - Path validation

```bash
uv run validators/07_hop_sync_validator.py [file.md]  # HOP validation
uv run validators/09_readme_validator.py [README.md]  # Docs validation
uv run validators/10_taxonomy_validator.py            # Taxonomy check
uv run validators/12_doc_sync_validator.py --all      # Doc sync validation
uv run validators/13_code_quality_validator.py [file] # Code quality
python codexa.py validate all                          # Run all validators
```

### Quality Gates (All Required)

✅ Structure (all sections) | ✅ Type consistency ($vars typed) | ✅ No orphans (all $vars defined) | ✅ Validation rules present | ✅ Quality ≥7.0/10.0 | ✅ MAX 1000 LINES

---

## 🔄 SELF-IMPROVEMENT LOOP

**Pattern**: Scout (LAW 9 discover) → Analyze (patterns) → Identify (opportunities) → Plan (CODEXA design) → Build (execute) → Validate (quality) → Integrate (merge) → Document (capture) → Repeat

**How**: Scout existing files FIRST → Read own HOPs → Read PRIME.md → Apply principles → Consolidate (remove duplication) → Update existing (not create duplicates) → Implement (transform stubs)

**Key Workflows**:
- `/consolidate` - Scan for duplicates + auto-consolidate
- `/bugloop` - Autonomous test→fix→verify→commit cycle
- ADW-100 (Doc Sync) - Auto-sync documentation across all agents

---

## 🎨 BEST PRACTICES (Rules)

**DO**: Scout first (LAW 9) | Read PRIME.md/HOPs first | Use templates | Validate incrementally | Trinity Output | Embrace [VARIABLES] | Chain $arguments | Build for reuse | Information-dense | MAX 1000 LINES | Consolidate before create | Update existing files

**DON'T**: Skip scouting | Create without checking existing | Build instances (build builders) | Skip validation | Use undefined $vars | Create orphans | Ignore quality ≥7.0 | Exceed 1000 lines | Duplicate content unnecessarily

---

## 📊 STRUCTURE (Easy Navigation)

```
codexa_agent/
├── builders/              # 15 tools | adw_modules/ (agent.py, scout_integration.py, utils.py)
│   ├── 02_agent_meta_constructor.py  ⭐ CORE 5-phase
│   ├── 11_doc_sync_builder.py       ⭐ ADW-100 Doc Sync
│   ├── 08_prompt_generator.py       # HOPs
│   └── 05_command_generator.py      # Commands
├── validators/            # 9 QA tools (07_hop, 09_readme, 10_taxonomy, 12_doc_sync, 13_code_quality, 16_path)
├── prompts/              # HOPs (TAC-7) + 8 composable layers
├── workflows/            # 16 ADW workflows
├── PRIME.md             # Philosophy [READ FIRST] v2.6.0
├── INSTRUCTIONS.md      # [THIS FILE] Operations guide v2.6.0
└── README.md            # Structure & metrics v2.6.0
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

## 🎯 STATUS & TIPS (v2.6.0)

**Functional**: ✅ 15 builders | ✅ 9 validators | ✅ HOPs (TAC-7) | ✅ 16 ADW workflows | ✅ 8 prompt layers | ✅ Scout integration

**Pro Tips**: Scout FIRST (LAW 9) | Read first build second | Use templates | Validate early | Think meta (builder not instance) | Chain $arguments | Quality ≥7.0 | Self-improve (CODEXA improves CODEXA) | Consolidate before create

**Troubleshooting**: Module not found → Check adw_modules/ | Orphaned $var → Define in INPUT_CONTRACT | Quality <7.0 → Review VALIDATION | Phase fails → Check $arguments chaining | Duplicates found → Run /consolidate

**New in v2.6.0**: LAW 9 Scout-First workflow | CRUD Priority discipline | Enhanced consolidation | Documentation sync (ADW-100) | Code quality validator | 16 ADW workflows

---

**Version**: 2.6.0
**Created**: 2025-11-13
**Updated**: 2025-12-05
**Maintainer**: CODEXA Team
**Related**: PRIME.md (philosophy v2.6.0), README.md (structure v2.6.0), All HOPs (examples)

**Changelog v2.6.0** (LAW 9 INTEGRATION):
- ✅ Added Scout-First Workflow section (LAW 9)
- ✅ Added CRUD Priority discipline (Delete > Update > Read > Create)
- ✅ Updated builder count: 7 → 15 tools
- ✅ Updated validator count: 3 → 9 tools
- ✅ Added ADW-100 (Doc Sync) workflow section
- ✅ Added 6 new validators to reference list
- ✅ Added consolidation workflows and /consolidate command
- ✅ Updated Best Practices with consolidation rules
- ✅ Updated PITER framework with Scout-First requirement
- ✅ Synchronized with PRIME.md v2.6.0 and README.md v2.6.0
