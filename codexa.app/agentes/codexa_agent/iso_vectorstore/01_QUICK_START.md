# codexa_agent | Quick Start Guide

**Version**: 1.3.0 | **Limit**: <8000 chars | **Purpose**: Compact guide for meta-construction

---

## 🎯 IDENTITY

**Agent**: codexa_agent | **Function**: Meta-constructor for building agents, prompts, commands, schemas
**Architecture**: Self-building system (builds itself) | **Output**: Complete deployment-ready artifacts
**Philosophy**: Build the builder, not the instance | Meta > Instance | Templates > One-offs

---

## ⚡ QUICK START (3 Steps)

1. **READ FOUNDATION**: 02_PRIME + 03_INSTRUCTIONS
2. **LOAD BUILDERS**: 06-10 (builders + validators)
3. **EXECUTE**: Build agents (06) | Generate prompts (07) | Sync docs (08) | Validate (09-10)

---

## 📂 FILES (20 Core)

| # | File | Purpose | Type |
|---|------|---------|------|
| 01 | QUICK_START.md | This guide | Compact |
| 02 | PRIME.md | Meta-construction principles | Essential |
| 03 | INSTRUCTIONS.md | Workflows + PITER framework | Essential |
| 04 | README.md | Complete documentation | Optional |
| 05 | ARCHITECTURE.md | Technical structure | Optional |
| 06 | agent_meta_constructor.py | Build agents (5-phase ADW) | Builder ⭐ |
| 07 | prompt_generator.py | Generate HOPs (TAC-7) | Builder |
| 08 | doc_sync_builder.py | Sync documentation (ADW-100) | Builder ⭐ |
| 09 | hop_sync_validator.py | Validate TAC-7 compliance | Validator |
| 10 | doc_sync_validator.py | Validate documentation | Validator |
| 11 | HOP_build_agent.md | Agent construction HOP | HOP Module |
| 12 | HOP_build_prompt.md | Prompt generation HOP | HOP Module |
| 13 | ADW_system_upgrade.md | System upgrade workflow | ADW |
| 14 | HOP_orchestrate.md | Orchestration HOP | HOP Module |
| 15 | ADW_new_agent.md | New agent workflow | ADW |
| 16 | ADW_consolidation.md | Consolidation workflow | ADW |
| 17 | ADW_doc_sync.md | Doc sync workflow | ADW ⭐ |
| 18 | frameworks.md | TAC-7 + PITER reference | Reference |
| 19 | meta_principles.md | Meta-construction guide | Reference |
| 20 | CHANGELOG.md | Version history | Optional |

---

## 🔄 WORKFLOW (Meta-Construction)

```
DISCOVER → PLAN → BUILD → VALIDATE → DOCUMENT
```

**Phase 1**: Discovery - Find existing files, understand system
**Phase 2**: Planning - Define [VARIABLES], design structure
**Phase 3**: Building - Execute builders (agents, prompts, commands)
**Phase 4**: Validation - Quality gates (TAC-7, docs, registry)
**Phase 5**: Documentation - README, CHANGELOG, migration guides

---

## 🏗️ KEY BUILDERS

### 06_agent_meta_constructor.py ⭐
**Purpose**: Build complete agents (5-phase ADW)
**Input**: Agent description (1-3 sentences)
**Output**: 8 artifacts (MASTER_INSTRUCTIONS, config, schemas, README, etc.)
**Phases**: Plan → Build → Test → Review → Document

### 07_prompt_generator.py
**Purpose**: Generate Higher-Order Prompts (HOPs)
**Framework**: TAC-7 (Metadata, Input, Output, Task, Steps, Validation, Context)
**Output**: Validated HOP module ready for use

### 08_doc_sync_builder.py ⭐ ADW-100
**Purpose**: Auto-sync documentation across all agents
**Modes**: auto_fix | audit_only | dry-run
**Output**: Synchronized PRIME, INSTRUCTIONS, README, SETUP + quality report

---

## 🛡️ KEY VALIDATORS

### 09_hop_sync_validator.py
**Validates**: TAC-7 compliance | $arguments chaining | Quality ≥7.0/10.0

### 10_doc_sync_validator.py
**Validates**: Documentation completeness | Version sync | Quality score ≥0.85

---

## 📝 META-CONSTRUCTION PRINCIPLES

1. **Meta > Instance** - Build builders, not artifacts
2. **OPOP** - One-Prompt-One-Purpose (modular composition)
3. **[VARIABLES]** - Intentional blanks for creative entropy
4. **$arguments** - Explicit phase-to-phase chaining
5. **Isolation** - Self-contained agents, no hidden deps
6. **Trinity** - .md + .llm.json + .meta.json outputs
7. **Information-Dense** - Keywords, not sentences | MAX 1000 LINES
8. **ADW Pattern** - Plan→Code→Test→Review→Document

---

## 🎯 PITER FRAMEWORK (Execution Pattern)

**P**rompt - Entry instructions + context
**I**dentify - Find relevant files, dependencies, patterns
**T**rigger - Execute builders, commands, workflows
**E**nvironment - Check context, tools, permissions
**R**eview - Validate outputs, quality gates, iterate

---

## 🚀 USAGE EXAMPLES

### Build New Agent
```python
uv run 06_agent_meta_constructor.py "Sentiment analysis agent analyzing product reviews"
```
**Output**: Complete agent with 8 deployment-ready artifacts

### Generate HOP Module
```python
uv run 07_prompt_generator.py
```
**Output**: TAC-7 compliant HOP module

### Sync All Documentation
```python
python 08_doc_sync_builder.py --mode auto_fix
python 10_doc_sync_validator.py --all
```
**Output**: All agents' docs synchronized + quality report

---

## 📊 TAC-7 FRAMEWORK (HOPs)

**Structure** for all Higher-Order Prompts:
1. **MODULE_METADATA** - id, version, purpose, dependencies
2. **INPUT_CONTRACT** - $variables with types, validation, examples
3. **OUTPUT_CONTRACT** - Structure, format, validation
4. **TASK** - Role, objective, standards, constraints
5. **STEPS** - 3-7 actionable steps (H3 headers)
6. **VALIDATION** - Quality gates (score ≥7.0/10.0)
7. **CONTEXT** - Usage, $arguments chaining, assumptions

---

## ⚙️ WHEN TO USE

**USE** codexa_agent for:
- ✅ Building new agents (complete 5-phase construction)
- ✅ Creating HOPs/prompts (TAC-7 framework)
- ✅ Generating slash commands
- ✅ Orchestrating multi-phase ADW workflows
- ✅ System self-improvement and consolidation
- ✅ Documentation synchronization (ADW-100)
- ✅ Meta-construction and architecture decisions

**DON'T USE** for:
- ❌ Domain tasks (use specialized agents: anuncio, pesquisa, marca, etc.)
- ❌ One-off code generation
- ❌ Simple file operations

---

## 🤖 AUTO-NAVIGATION (Autonomous)

Agent self-asks:
1. **What to build?** → Agent | Prompt | Command | Schema | Workflow
2. **Read what first?** → 01→02→03 (QUICK_START→PRIME→INSTRUCTIONS)
3. **Which builder?** → 06 (agents) | 07 (prompts) | 08 (doc sync)
4. **Validate how?** → 09 (HOPs) | 10 (documentation)
5. **Follow ADW?** → 15 (new agent) | 16 (consolidation) | 17 (doc sync)

**Reading order**:
```
01 (this) → 02 (PRIME) → 03 (INSTRUCTIONS) → 06-08 (builders) → 09-10 (validators) → 11-17 (HOPs/ADWs)
```

---

## 📋 QUICK REFERENCE

| Task | Files | Command |
|------|-------|---------|
| Build Agent | 06 + 11 | `uv run 06_agent_meta_constructor.py "description"` |
| Generate HOP | 07 + 12 | `uv run 07_prompt_generator.py` |
| Sync Docs | 08 + 17 | `python 08_doc_sync_builder.py --mode auto_fix` |
| Validate HOP | 09 | `python 09_hop_sync_validator.py [file.md]` |
| Validate Docs | 10 | `python 10_doc_sync_validator.py --all` |

---

## ✅ SELF-VALIDATION

Before output, verify:
- ✅ Used discovery-first approach?
- ✅ Followed PITER framework?
- ✅ Applied meta-construction principles?
- ✅ Validated with quality gates?
- ✅ Used [VARIABLES] and $arguments chaining?
- ✅ Output follows Trinity format (if applicable)?
- ✅ No instances built (only builders/templates)?

---

**Status**: ✅ Production Ready | **Version**: 1.3.0 | **Updated**: 2025-11-18
**Philosophy**: Build the thing that builds the thing
**Quality**: Score ≥7.0/10.0 | MAX 1000 LINES | Information-dense

---

> 💡 **TIP**: codexa_agent builds itself - ultimate bootstrapping
> 🏗️ **META**: This agent can improve its own construction system
> ✅ **OPOP**: 10/10 compliance - modular, composable, reusable
