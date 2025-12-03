# WORKFLOWS Reference (ADWs)

**Version**: 1.0.0
**Updated**: 2025-12-03
**Purpose**: Catalog of all Agentic Developer Workflows (ADWs)

---

## What is an ADW?

**ADW** = Agentic Developer Workflow

A structured, multi-phase workflow that LLMs execute autonomously. Each ADW defines:
- **Phases**: Sequential steps with inputs/outputs
- **Quality Gates**: Validation thresholds (≥7.0/10.0)
- **Triggers**: Commands or conditions that start the workflow

---

## ADW Architecture

```
┌─────────────────────────────────────────────────┐
│                    ADW Layer                     │
│  (What to do - orchestration)                   │
├─────────────────────────────────────────────────┤
│                    HOP Layer                     │
│  (How to think - prompts)                       │
└─────────────────────────────────────────────────┘
```

---

## Numbering Convention (LAW 5: Ordinal Sequencing)

| Range | Category | Description |
|-------|----------|-------------|
| 00-09 | Foundation | Entry points, orchestrators |
| 10-49 | Execution | Core workflow phases |
| 50-99 | Meta | System-level, cross-agent |
| 100+ | Production | Main execution workflows |
| 200+ | Advanced | Parallel, multi-agent |

---

## Global Workflows

| ID | Name | Path | Trigger |
|----|------|------|---------|
| 100 | Orchestration | `codexa.app/workflows/100_ADW_CODEXA_ORCHESTRATION.md` | `/codexa-orchestrate` |

---

## codexa_agent (Meta-Construction)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 13 | System Upgrade | `iso_vectorstore/13_ADW_system_upgrade.md` | Upgrade workflows |
| 15 | New Agent | `iso_vectorstore/15_ADW_new_agent.md` | Agent creation |
| 16 | Consolidation | `iso_vectorstore/16_ADW_consolidation.md` | Merge/cleanup |
| 17 | Doc Sync | `iso_vectorstore/17_ADW_doc_sync.md` | Documentation |
| 97 | New Agent Workflow | `workflows/97_ADW_NEW_AGENT_WORKFLOW.md` | Full agent build |
| 98 | Consolidation Workflow | `workflows/98_ADW_CONSOLIDATION_WORKFLOW.md` | System merge |
| 99 | System Upgrade Workflow | `workflows/99_ADW_SYSTEM_UPGRADE_WORKFLOW.md` | Upgrade path |
| 100 | Doc Sync Workflow | `workflows/100_ADW_DOC_SYNC_WORKFLOW.md` | Auto-sync docs |
| 104 | ISO Optimization | `workflows/104_ADW_ISO_VECTORSTORE_OPTIMIZATION.md` | Knowledge base |
| 201 | Feature Development | `workflows/201_ADW_FEATURE_DEVELOPMENT.md` | New features |
| 202 | Bug Fixing | `workflows/202_ADW_BUG_FIXING.md` | Debug workflow |
| 203 | Parallel Orchestration | `workflows/203_ADW_PARALLEL_ORCHESTRATION.md` | Multi-agent |
| 204 | Product Reform | `workflows/204_ADW_INTEGRATED_PRODUCT_REFORM.md` | Batch updates |
| 205 | Knowledge Enrichment | `workflows/205_ADW_KNOWLEDGE_ENRICHMENT.md` | Context expansion |
| 206 | Subagent Construction | `workflows/206_ADW_SUBAGENT_CONSTRUCTION.md` | Build subagents |

---

## anuncio_agent (Listings)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Run Anuncio | `workflows/100_ADW_RUN_ANUNCIO.md` | Generate listings |

**Trigger**: `/anuncio`

---

## curso_agent (Courses)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 01 | Quick Course | `workflows/01_ADW_QUICK_COURSE.md` | Fast course |
| 02 | Full Module | `workflows/02_ADW_FULL_MODULE.md` | Complete module |
| 03 | Sales Package | `workflows/03_ADW_SALES_PACKAGE.md` | Sales materials |

**Trigger**: `/curso`

---

## marca_agent (Branding)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Run Marca | `workflows/100_ADW_RUN_MARCA.md` | Brand analysis |

**Trigger**: `/marca`

---

## pesquisa_agent (Research)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Run Pesquisa | `workflows/100_ADW_RUN_PESQUISA.md` | Market research |

**Trigger**: `/pesquisa`

---

## photo_agent (Images)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 14 | Orchestrator v2 | `iso_vectorstore/14_ADW_orchestrator.md` | Updated flow |
| 100 | Run Photo | `workflows/100_ADW_RUN_PHOTO.md` | Photo generation |
| 110 | Image to Image | `workflows/110_ADW_IMAGE_TO_IMAGE.md` | Style transfer |

**Trigger**: `/photo`

---

## video_agent (Videos)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Run Video | `workflows/100_ADW_RUN_VIDEO.md` | Video creation |

**Trigger**: `/video`

---

## voice_agent (Audio)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Voice Interaction | `workflows/100_ADW_VOICE_INTERACTION.md` | Voice I/O |

**Trigger**: `/voice`

---

## mentor_agent (Guidance)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 13 | Mentor Workflow | `iso_vectorstore/13_ADW_mentor_workflow.md` | Guidance flow |
| 100 | Run Mentor | `workflows/100_ADW_RUN_MENTOR.md` | Mentorship |

**Trigger**: `/mentor`

---

## scout_agent (Discovery)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Discovery Workflow | `workflows/100_ADW_DISCOVERY_WORKFLOW.md` | Find files |

**Trigger**: `mcp__scout__discover`

---

## qa_gato3_agent (QA)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | QA Workflow | `workflows/100_ADW_QA_WORKFLOW.md` | Quality assurance |

---

## ronronalda_agent (Personality)

| ID | Name | Path | Purpose |
|----|------|------|---------|
| 11 | Orchestrator | `iso_vectorstore/11_ADW_orchestrator.md` | Entry point |
| 100 | Ronronalda | `workflows/100_ADW_RONRONALDA.md` | Cat persona |

---

## ADW Template

When creating new ADWs, use this structure:

```markdown
# {NUMBER}_ADW_{NAME}

**ID**: {NUMBER}_ADW_{NAME}
**Version**: 1.0.0
**Type**: ADW (Agentic Developer Workflow)

## INPUT_CONTRACT
- $input_1: description
- $input_2: description

## PHASES
1. Phase 1: Description (duration)
2. Phase 2: Description (duration)
...

## OUTPUT_CONTRACT
- $output_1: description

## VALIDATION
- Quality gate: ≥7.0/10.0
- Validation criteria

## TRIGGER
- Command: /command-name
- Condition: when X happens
```

---

## Summary

| Category | Count |
|----------|-------|
| Global | 1 |
| codexa_agent | 16 |
| Domain Agents | 24 |
| **Total ADWs** | **41** |

---

## See Also

- [CLAUDE.md](../CLAUDE.md) - LAW 4: Agentic Design
- [QUICK_START_ADW.md](../codexa.app/QUICK_START_ADW.md) - Quick start guide
