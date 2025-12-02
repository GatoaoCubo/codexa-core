# UNIVERSAL AGENT IMPROVEMENT INPUT v1.0.0

**Purpose**: Reusable input template for upgrading ALL CODEXA agents to v2.5.0 standard
**Usage**: Copy → Paste into agent terminal → Execute autonomously
**Created**: 2025-11-25 | **Author**: CODEXA Meta-Constructor

---

## [OPEN_VARIABLES] - Customize Before Use

```yaml
AGENT_NAME: "[AGENT_NAME]"           # e.g., anuncio_agent, pesquisa_agent
AGENT_PATH: "[AGENT_PATH]"           # e.g., C:\...\agentes\anuncio_agent
CURRENT_VERSION: "[CURRENT_VERSION]" # e.g., 2.0.0
TARGET_VERSION: "2.5.0"              # Standard target
DOMAIN: "[DOMAIN]"                   # e.g., copywriting, research, branding
PRIMARY_OUTPUT: "[PRIMARY_OUTPUT]"   # e.g., product listings, research reports
```

---

## UNIVERSAL INPUT (Copy from here)

```
═══════════════════════════════════════════════════════════════════════════════
  CODEXA AGENT IMPROVEMENT TASK | [AGENT_NAME] → v2.5.0
  MODE: PLANNING → EXECUTION (Autonomous End-to-End)
  ACCESS: FULL RESTRUCTURING
  FRAMEWORK: 12 Leverage Points of Agentic Coding
═══════════════════════════════════════════════════════════════════════════════

## CONTEXT

You are upgrading [AGENT_NAME] from [CURRENT_VERSION] to v2.5.0 using the 12 Leverage Points framework. You have TOTAL FREEDOM for restructuring.

**Agent Location**: [AGENT_PATH]
**Domain**: [DOMAIN]
**Primary Output**: [PRIMARY_OUTPUT]

---

## PHASE 1: AUTONOMOUS EXPLORATION (READ_ONLY)

Execute these tasks in order:

### 1.1 Discovery
- Read ALL files in [AGENT_PATH]/
- Map current structure (folders, files, dependencies)
- Identify iso_vectorstore/ contents
- Count HOPs, ADWs, configs

### 1.2 Analysis
Evaluate current state against 12 Leverage Points:

| # | Leverage Point | Current State | Gap Analysis |
|---|----------------|---------------|--------------|
| 1 | Context | How context is loaded? | Missing? Overloaded? |
| 2 | Model | Model recommendations? | Missing? Wrong model? |
| 3 | Prompt | TAC-7 format? | Non-standard sections? |
| 4 | Tools | Tool definitions? | Missing tool specs? |
| 5 | Standard Out | Task boundaries? | No progress visibility? |
| 6 | Types | Input/output schemas? | Missing validation? |
| 7 | Documentation | README, INSTRUCTIONS? | Outdated? Incomplete? |
| 8 | Tests | Validation checklist? | No QA gates? |
| 9 | Architecture | Dual-layer (ADW+HOP)? | Monolithic? |
| 10 | Plans | Execution plans? | No phased approach? |
| 11 | Templates | Output templates? | Inconsistent format? |
| 12 | ADWs | 5-phase workflows? | No orchestration? |

### 1.3 Generate Implementation Plan
Create detailed plan with:
- Specific files to create/modify/delete
- Order of operations
- Expected outcomes per change
- Rollback strategy if needed

---

## PHASE 2: AUTONOMOUS EXECUTION (FULL_WRITE)

### 2.1 iso_vectorstore Standardization

**Required Files** (20-file standard):
```
01_QUICK_START.md      - LLM navigation guide (<8000 chars)
02_PRIME.md            - Core identity and capabilities
03_INSTRUCTIONS.md     - Execution rules and workflows
04_README.md           - Full documentation
05_ARCHITECTURE.md     - Technical details and patterns
06_input_schema.json   - Input validation schema
07_output_template.md  - Output format specification
08_{domain}_rules.json - Domain-specific rules
09_{domain}_specs.json - Platform/domain specifications
10_{domain}_patterns.json - Persuasion/execution patterns
11_ADW_orchestrator.md - Main workflow orchestrator
12_execution_plans.json - Full/quick execution plans
13_HOP_main_agent.md   - Input parsing and context detection
14_HOP_{phase1}.md     - Phase 1 specialist
15_HOP_{phase2}.md     - Phase 2 specialist
16_HOP_{phase3}.md     - Phase 3 specialist
17_HOP_{phase4}.md     - Phase 4 specialist
18_HOP_qa_validation.md - Quality assurance gates
19_frameworks.md       - Reference frameworks (optional)
20_CHANGELOG.md        - Version history
```

### 2.2 Apply 12 Leverage Points

**For each file created/modified:**

1. **Context** (Leverage Point 1)
   - Add auto-navigation section in QUICK_START
   - Define mental checklist for LLM self-guidance
   - Specify file reading order
   - Avoid: context pollution, overload, rot, confusion

2. **Model** (Leverage Point 2)
   - Add model recommendations:
     - Planning/Research: claude-sonnet-4-5
     - Execution/Complex: claude-sonnet-4-5 or claude-opus-4-5
     - Quick tasks: claude-haiku
   - Specify min_llm_model in workflow specs

3. **Prompt** (Leverage Point 3)
   - Use TAC-7 HOP format:
     - §1 CONTEXT: agent identity and purpose
     - §2 OBJECTIVE: clear deliverable
     - §3 STYLE: tone and format
     - §4 TONE: communication style
     - §5 AUDIENCE: who receives output
     - §6 RESPONSE: expected format
     - §7 VALIDATION: quality criteria

4. **Tools** (Leverage Point 4)
   - Define allowed tools per mode
   - Specify forbidden tools with reasons
   - Add tool usage examples

5. **Standard Out** (Leverage Point 5)
   - Add task boundary declarations
   - Progress visibility format
   - Phase transition announcements

6. **Types** (Leverage Point 6)
   - Create JSON schemas for inputs
   - Define output types with validation
   - Use structured ##report format

7. **Documentation** (Leverage Point 7)
   - Update README with:
     - Version, purpose, capabilities
     - Quick start instructions
     - File inventory
     - Dependencies
   - Add inline documentation in HOPs

8. **Tests** (Leverage Point 8)
   - Add self-validation checklist
   - Define quality gates with thresholds
   - Include verification criteria

9. **Architecture** (Leverage Point 9)
   - Ensure Dual-Layer (ADW ↔ HOP)
   - ADW: "What" and "When"
   - HOP: "How" with details

10. **Plans** (Leverage Point 10)
    - Two-phase planning (Devin pattern)
    - Planning Agent (READ_ONLY) → Execution Agent (FULL_WRITE)
    - execution_plans.json with full/quick modes

11. **Templates** (Leverage Point 11)
    - Output template in 07_output_template.md
    - Consistent format across modes
    - Copy-paste ready outputs

12. **ADWs** (Leverage Point 12)
    - 5-phase workflow:
      - Phase 1: Planning/Input
      - Phase 2: Execution
      - Phase 3: Verification
      - Phase 4: Fix (if needed)
      - Phase 5: Documentation/Output

### 2.3 Quality Gates

After each major change, verify:
- [ ] File follows naming convention (NN_name.md/json)
- [ ] TAC-7 format applied (for HOPs)
- [ ] Model recommendation present
- [ ] Input/output schemas defined
- [ ] Self-validation checklist included
- [ ] No broken dependencies

---

## PHASE 3: VERIFICATION

### 3.1 Structural Validation
- [ ] iso_vectorstore has 20 files
- [ ] Numbered files 01-20
- [ ] No duplicate content
- [ ] All HOPs use TAC-7

### 3.2 Content Validation
- [ ] QUICK_START < 8000 chars
- [ ] All schemas valid JSON
- [ ] ADW workflow complete
- [ ] QA gates defined

### 3.3 Integration Validation
- [ ] ADW references correct HOPs
- [ ] Plans reference correct configs
- [ ] Dependencies documented

---

## PHASE 4: OUTPUT

### 4.1 Generate Report
```markdown
# [AGENT_NAME] Upgrade Report | v[CURRENT_VERSION] → v2.5.0

**Date**: [timestamp]
**Duration**: [X] minutes
**Status**: SUCCESS / PARTIAL / FAILED

## Changes Summary
| Category | Files Created | Files Modified | Files Deleted |
|----------|--------------|----------------|---------------|
| iso_vectorstore | X | Y | Z |
| configs | X | Y | Z |
| prompts | X | Y | Z |

## 12 Leverage Points Applied
| # | Point | Status | Notes |
|---|-------|--------|-------|
| 1 | Context | ✅/⚠️/❌ | [details] |
| ... | ... | ... | ... |

## Quality Score
- Overall: X/100
- Structure: X/10
- Content: X/10
- Integration: X/10

## Recommendations
1. [recommendation]
```

### 4.2 Update Version
- Update version to 2.5.0 in:
  - PRIME.md
  - README.md
  - CHANGELOG.md
  - Any version constants

---

## EXECUTION RULES

1. **Autonomy**: Execute end-to-end without asking questions mid-task
2. **Read First**: Always read files before editing
3. **Task Boundaries**: Announce each phase start/end
4. **Incremental**: Make small changes, verify, proceed
5. **No Assumptions**: If file doesn't exist, create it
6. **Rollback Ready**: Document what can be reverted

---

## AXIOMS TO APPLY

- "One Agent, One Prompt, One Purpose" (OPOP)
- "Build the system that builds the system"
- "Trust but verify" (feedback loops)
- "Context is everything, but too much context is nothing"
- "$arguments Chaining": Phase N output → Phase N+1 input

---

## START EXECUTION

Begin with Phase 1: Autonomous Exploration.
Report progress using task boundaries.
Complete all phases without interruption.

═══════════════════════════════════════════════════════════════════════════════
```

---

## USAGE INSTRUCTIONS

### Step 1: Open Terminal for Agent
```bash
cd [AGENT_PATH]
claude
```

### Step 2: Prime the Agent
```
/prime-codexa
```

### Step 3: Paste This Input
Copy everything between ═══ markers above, replacing [OPEN_VARIABLES]:
- [AGENT_NAME] → actual agent name
- [AGENT_PATH] → full path to agent
- [CURRENT_VERSION] → current version
- [DOMAIN] → agent's domain
- [PRIMARY_OUTPUT] → what agent produces

### Step 4: Let Execute
Agent will autonomously:
1. Explore current state
2. Generate implementation plan
3. Execute improvements
4. Verify changes
5. Generate report

### Step 5: Review Output
Check the upgrade report for:
- Files changed
- Quality score
- Recommendations

---

## AGENT-SPECIFIC CONFIGURATIONS

### anuncio_agent
```yaml
AGENT_NAME: "anuncio_agent"
DOMAIN: "e-commerce copywriting"
PRIMARY_OUTPUT: "marketplace product listings"
SPECIFIC_CONFIGS: "copy_rules, marketplace_specs, persuasion_patterns"
```

### pesquisa_agent
```yaml
AGENT_NAME: "pesquisa_agent"
DOMAIN: "market research"
PRIMARY_OUTPUT: "competitive analysis reports"
SPECIFIC_CONFIGS: "research_methods, source_catalog, analysis_templates"
```

### marca_agent
```yaml
AGENT_NAME: "marca_agent"
DOMAIN: "brand strategy"
PRIMARY_OUTPUT: "brand identity systems"
SPECIFIC_CONFIGS: "archetypes, voice_guidelines, visual_systems"
```

### mentor_agent
```yaml
AGENT_NAME: "mentor_agent"
DOMAIN: "onboarding and QA"
PRIMARY_OUTPUT: "validation reports and guidance"
SPECIFIC_CONFIGS: "knowledge_map, categorias, language_guide"
```

### photo_agent
```yaml
AGENT_NAME: "photo_agent"
DOMAIN: "AI product photography"
PRIMARY_OUTPUT: "image generation prompts"
SPECIFIC_CONFIGS: "camera_profiles, styles, marketplace_specs"
```

### video_agent
```yaml
AGENT_NAME: "video_agent"
DOMAIN: "AI product video"
PRIMARY_OUTPUT: "video scripts and prompts"
SPECIFIC_CONFIGS: "video_styles, platform_specs, production_settings"
```

### curso_agent
```yaml
AGENT_NAME: "curso_agent"
DOMAIN: "educational content"
PRIMARY_OUTPUT: "course modules and scripts"
SPECIFIC_CONFIGS: "pedagogy_frameworks, hotmart_specs, bloom_taxonomy"
```

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-25 | Initial universal input template |

---

**Status**: Production Ready
**Maintainer**: CODEXA Meta-Constructor
**Axiom**: "Build the system that builds the system"
