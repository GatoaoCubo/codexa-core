# COPY-PASTE INPUT | Agent Improvement v2.5.0

**Instructions**: Replace [VARIABLES] → Paste in agent terminal → Execute

---

## COMPACT INPUT (Copy Below)

```
/prime-codexa

═══════════════════════════════════════════════════════════════════════════════
CODEXA AGENT UPGRADE | [AGENT_NAME] → v2.5.0
MODE: AUTONOMOUS (Plan + Execute)
FRAMEWORK: 12 Leverage Points
═══════════════════════════════════════════════════════════════════════════════

## TASK

Upgrade [AGENT_NAME] to v2.5.0 applying the 12 Leverage Points framework.
You have TOTAL FREEDOM for restructuring. Execute autonomously end-to-end.

## VARIABLES
- Agent: [AGENT_NAME]
- Path: [AGENT_PATH]
- Domain: [DOMAIN]
- Current: [CURRENT_VERSION]

## EXECUTION PHASES

### PHASE 1: EXPLORE (READ_ONLY)
1. Read ALL files in agent directory
2. Map: iso_vectorstore, configs, HOPs, ADWs
3. Analyze against 12 Leverage Points:
   - Context: auto-navigation, mental checklist?
   - Model: recommendations present?
   - Prompt: TAC-7 format?
   - Tools: defined per mode?
   - Standard Out: task boundaries?
   - Types: JSON schemas?
   - Documentation: complete README?
   - Tests: validation checklist?
   - Architecture: Dual-Layer ADW+HOP?
   - Plans: execution_plans.json?
   - Templates: output format?
   - ADWs: 5-phase workflow?
4. Generate implementation plan

### PHASE 2: EXECUTE (FULL_WRITE)
1. Standardize iso_vectorstore (20 files numbered 01-20)
2. Apply all 12 Leverage Points
3. Create/update files as needed:
   - 01_QUICK_START.md (<8000 chars, LLM navigation)
   - 02_PRIME.md (identity, capabilities)
   - 03_INSTRUCTIONS.md (workflow rules)
   - 06_input_schema.json (validation)
   - 07_output_template.md (format)
   - 11_ADW_orchestrator.md (5-phase)
   - 12_execution_plans.json (full/quick)
   - HOPs with TAC-7 format
4. Use task boundaries for progress visibility

### PHASE 3: VERIFY
1. Validate structure (20 files, numbered)
2. Validate content (schemas valid, HOPs TAC-7)
3. Validate integration (ADW→HOP references)

### PHASE 4: OUTPUT
Generate upgrade report:
- Files changed summary
- 12 Leverage Points status (✅/❌)
- Quality score
- Recommendations

## RULES
- Execute without asking questions mid-task
- Read before write ALWAYS
- Announce phase transitions
- Update version to 2.5.0 in PRIME, README, CHANGELOG

## AXIOMS
- "One Agent, One Prompt, One Purpose"
- "Build the system that builds the system"
- "$arguments Chaining": Phase N → Phase N+1

BEGIN EXECUTION. Report progress with task boundaries.
═══════════════════════════════════════════════════════════════════════════════
```

---

## QUICK REFERENCE - Variable Values

### anuncio_agent
```
[AGENT_NAME] = anuncio_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\anuncio_agent
[DOMAIN] = e-commerce copywriting
[CURRENT_VERSION] = 2.0.0
```

### pesquisa_agent
```
[AGENT_NAME] = pesquisa_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\pesquisa_agent
[DOMAIN] = market research
[CURRENT_VERSION] = 2.1.0
```

### marca_agent
```
[AGENT_NAME] = marca_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\marca_agent
[DOMAIN] = brand strategy
[CURRENT_VERSION] = 2.0.0
```

### mentor_agent
```
[AGENT_NAME] = mentor_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\mentor_agent
[DOMAIN] = onboarding and QA
[CURRENT_VERSION] = 2.0.0
```

### photo_agent
```
[AGENT_NAME] = photo_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\photo_agent
[DOMAIN] = AI product photography
[CURRENT_VERSION] = 2.0.0
```

### video_agent
```
[AGENT_NAME] = video_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\video_agent
[DOMAIN] = AI product video
[CURRENT_VERSION] = 1.0.0
```

### curso_agent
```
[AGENT_NAME] = curso_agent
[AGENT_PATH] = C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\curso_agent
[DOMAIN] = educational content
[CURRENT_VERSION] = 2.0.0
```

---

## WORKFLOW

```
Terminal 1 (anuncio)    Terminal 2 (pesquisa)    Terminal 3 (marca)
       ↓                       ↓                       ↓
   cd [path]               cd [path]               cd [path]
       ↓                       ↓                       ↓
    claude                   claude                  claude
       ↓                       ↓                       ↓
 paste input            paste input             paste input
       ↓                       ↓                       ↓
   (executes)             (executes)             (executes)
       ↓                       ↓                       ↓
   report.md              report.md               report.md
```

All agents upgrade in PARALLEL. Each terminal runs autonomously.
