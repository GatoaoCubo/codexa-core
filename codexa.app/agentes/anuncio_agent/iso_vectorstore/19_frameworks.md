# CODEXA & HOP Frameworks | Meta-Construction & Hierarchical Prompts

**Version**: 3.2.0 | **Purpose**: Framework foundations for anuncio_agent
**Context**: Advanced reference (read last) | **Max Lines**: 200

---

## 🎯 CODEXA FRAMEWORK

### Core Philosophy
**Meta-Construction**: Build the thing that builds the thing
**OPOP**: One-Prompt-One-Purpose (1 HOP = 1 task)
**Trinity Output**: .md + .llm.json + .meta.json

### 8 Core Principles
1. **Meta > Instance** - Build builders, not artifacts
2. **OPOP** - One prompt, one purpose, compose don't duplicate
3. **[OPEN_VARIABLES]** - Intentional blanks for LLM creativity
4. **$arguments-chaining** - Explicit data flow (phase N → phase N+1)
5. **Isolation** - Self-contained agents, zero hidden dependencies
6. **Trinity Output** - Human (.md) + LLM (.json) + Metadata (.meta.json)
7. **Information-Dense** - Keywords > sentences, MAX 1000 lines/file
8. **ADW Pattern** - Plan → Code → Test → Review → Document

### Architecture Pillars

**4 IN-AGENT Pillars** (Construction):
- **Contexto**: Domain knowledge, codebase, requirements
- **Modelo**: LLM (GPT-4o+, Sonnet 4.5+), reasoning
- **Tools**: Functions, integrations, validators
- **Prompts**: HOPs, instructions, meta-formats

**8 OUT-AGENT Pillars** (Artifacts):
- **Templates**: Reusable with [VARIABLES]
- **Standard Output**: Trinity format
- **Types**: Information flow schemas
- **Documentation**: AI_DOCS + internal
- **Tests**: Self-validating loops
- **Architecture**: Easy navigation
- **Plans**: Detailed ADW workflows
- **ADWs**: 1-shot solutions

---

## 📋 HOP FRAMEWORK (TAC-7)

### What is HOP?
**Hierarchical-Oriented-Prompts**: Modular, composable, single-purpose prompts
**TAC-7 Standard**: 7-section structure for all HOPs

### TAC-7 Structure (7 Sections)

```
1. MODULE_METADATA
   - id, version, purpose, dependencies, category

2. INPUT_CONTRACT
   - $variables (type: string/object/array)
   - description, validation, example

3. OUTPUT_CONTRACT
   - $outputs (type: object)
   - format, structure, validation

4. TASK
   - Role, objective, quality standards, constraints

5. STEPS
   - 3-7 numbered steps (H3 headers)
   - Actionable, sequential, clear

6. VALIDATION
   - Quality gates (score ≥7.0/10.0)
   - Compliance checks, output validation

7. CONTEXT
   - $arguments chaining, assumptions, fallback
```

### HOP Principles

**Modularity**: Each HOP = standalone, reusable, composable
**Chaining**: Output variables become input for next HOP
**Validation**: Every HOP validates inputs + outputs
**Isolation**: Zero hidden dependencies, explicit contracts

### Example HOP Flow (Anuncio Agent)

```
HOP 13 (main_agent) → $head_terms, $diferenciais
  ↓
HOP 14 (titulo_generator) → $titulos_list
  ↓
HOP 15 (keywords_expander) → $keywords_blocks
  ↓
HOP 16 (bullet_points) → $bullets_list
  ↓
HOP 17 (descricao_builder) → $descricao_text
  ↓
HOP 18 (qa_validation) → $qa_report, $compliance_score
```

---

## 🔄 ADW PATTERN (Agent Development Workflow)

### 5-Phase Meta-Construction

```
Phase 1: PLAN
→ Strategic planning with [OPEN_VARIABLES]
→ Output: $plan, $specifications

Phase 2: BUILD
→ Artifact construction using $plan
→ Output: $artifacts (8 files)

Phase 3: TEST
→ Validation + quality gates
→ Output: $test_results, $issues

Phase 4: REVIEW
→ Analysis + optimization
→ Output: $review_report, $improvements

Phase 5: DOCUMENT
→ Complete documentation
→ Output: $final_docs, $metadata
```

### Orchestration Rules

**Sequential Execution**: Phases run in order
**$arguments Chaining**: Phase N output → Phase N+1 input
**Quality Gates**: Each phase validates before proceeding
**Fallback**: On failure, retry or graceful degradation

---

## 🎨 PRACTICAL APPLICATION (Anuncio Agent)

### How anuncio_agent Uses These Frameworks

**CODEXA Principles Applied**:
- Meta-Construction: Builds ads from templates, not manual writing
- OPOP: 6 specialized HOPs (13-18), each with 1 purpose
- Trinity Output: .md (human) + .llm.json (LLM) + .meta.json (metadata)
- Information-Dense: Compressed copy (3,300+ chars with max keywords)

**HOP Implementation**:
- 6 modular HOPs in sequential pipeline
- $arguments chaining throughout (e.g., $head_terms → $titulos_list → $keywords_blocks)
- TAC-7 structure in all HOPs (metadata, contracts, task, steps, validation, context)
- Validation gates: 11-criteria compliance check (HOP 18)

**ADW Orchestration**:
- ADW_orchestrator.md (file 11) manages 6-HOP pipeline
- Sequential execution with parallel potential (future optimization)
- Error handling + quality gates at each step
- Final Trinity output assembly

---

## 📚 REFERENCE

**Full CODEXA Docs**: agentes/codexa-agent/
**HOP Examples**: All HOPs in this vectorstore (13-18)
**Meta-Constructor**: builders/02_agent_meta_constructor.py (outside vectorstore)

**When to Reference This File**:
- Understanding framework philosophy
- Debugging HOP execution flow
- Extending agent with new HOPs
- Architectural questions

**Not Needed For**:
- Normal execution (HOPs self-contained)
- Basic usage (read QUICK_START + PRIME)
- Direct ad generation (use ADW orchestrator)

---

**Status**: Reference Only | **Context**: Advanced | **Read**: Last (after all other files)
**Purpose**: Explain "why" and "how" behind anuncio_agent architecture
