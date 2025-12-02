# Multi-Agent Upgrade Process | Documentation

**Purpose**: Reusable workflow for upgrading ALL CODEXA agents simultaneously
**Created**: 2025-11-25 | **Version**: 1.0.0

---

## OVERVIEW

This document describes the process for upgrading multiple CODEXA agents in parallel using a universal input template with [OPEN_VARIABLES].

### Components
| File | Purpose |
|------|---------|
| `UNIVERSAL_AGENT_IMPROVEMENT_INPUT.md` | Full template with detailed instructions |
| `COPY_PASTE_INPUT.md` | Compact copy-paste ready version |
| `MULTI_AGENT_UPGRADE_PROCESS.md` | This documentation |

---

## AGENTS TO UPGRADE

| # | Agent | Domain | Current | Target |
|---|-------|--------|---------|--------|
| 1 | anuncio_agent | E-commerce Copywriting | v2.0.0 | v2.5.0 |
| 2 | pesquisa_agent | Market Research | v2.1.0 | v2.5.0 |
| 3 | marca_agent | Brand Strategy | v2.0.0 | v2.5.0 |
| 4 | mentor_agent | Onboarding & QA | v2.0.0 | v2.5.0 |
| 5 | photo_agent | AI Photography | v2.0.0 | v2.5.0 |
| 6 | video_agent | AI Video | v1.0.0 | v2.5.0 |
| 7 | curso_agent | Educational Content | v2.0.0 | v2.5.0 |

**Note**: codexa_agent already at v2.5.0 (upgraded separately)

---

## 12 LEVERAGE POINTS FRAMEWORK

The upgrade applies all 12 Leverage Points of Agentic Coding:

```yaml
1_context:
  what: "Information & perspective building"
  apply: "Auto-navigation, mental checklist, file reading order"
  avoid: "Context pollution, overload, rot, confusion"

2_model:
  what: "AI model selection"
  apply: "Model recommendations per task type"
  patterns: "Sonnet for planning, Opus for complex orchestration"

3_prompt:
  what: "Prompt engineering"
  apply: "TAC-7 HOP format (7 sections)"
  patterns: "OPOP - One Agent One Prompt One Purpose"

4_tools:
  what: "Tool definitions"
  apply: "Allowed/forbidden tools per mode"
  patterns: "Read before write, no destructive ops"

5_standard_out:
  what: "Progress visibility"
  apply: "Task boundaries, phase transitions"
  patterns: "═══ MODE: X | TASK: Y/Z | PROGRESS: N% ═══"

6_types:
  what: "Structured data"
  apply: "JSON schemas, ##report format"
  patterns: "Input validation, output schemas"

7_documentation:
  what: "Self-documentation"
  apply: "README, INSTRUCTIONS, inline docs"
  patterns: "QUICK_START < 8000 chars"

8_tests:
  what: "Self-validation"
  apply: "Quality gates, verification checklists"
  patterns: "11-point QA criteria"

9_architecture:
  what: "System design"
  apply: "Dual-Layer ADW + HOP"
  patterns: "ADW = what/when, HOP = how"

10_plans:
  what: "Execution planning"
  apply: "Two-phase planning (Devin pattern)"
  patterns: "READ_ONLY planning → FULL_WRITE execution"

11_templates:
  what: "Output templates"
  apply: "07_output_template.md standard"
  patterns: "Copy-paste ready outputs"

12_adws:
  what: "Orchestration workflows"
  apply: "5-phase ADW pattern"
  patterns: "Plan → Execute → Verify → Fix → Document"
```

---

## iso_vectorstore STANDARD (20 Files)

Every agent must have these 20 numbered files:

```
01_QUICK_START.md       # LLM navigation guide (<8000 chars)
02_PRIME.md             # Core identity
03_INSTRUCTIONS.md      # Execution rules
04_README.md            # Full documentation
05_ARCHITECTURE.md      # Technical details
06_input_schema.json    # Input validation
07_output_template.md   # Output format
08_{domain}_rules.json  # Domain rules
09_{domain}_specs.json  # Domain specs
10_{domain}_patterns.json # Persuasion/exec patterns
11_ADW_orchestrator.md  # Main workflow
12_execution_plans.json # Full/quick plans
13_HOP_main_agent.md    # Input parsing
14_HOP_{phase1}.md      # Phase 1 specialist
15_HOP_{phase2}.md      # Phase 2 specialist
16_HOP_{phase3}.md      # Phase 3 specialist
17_HOP_{phase4}.md      # Phase 4 specialist
18_HOP_qa_validation.md # QA gates
19_frameworks.md        # Reference frameworks
20_CHANGELOG.md         # Version history
```

---

## EXECUTION WORKFLOW

### Step 1: Open Multiple Terminals
```bash
# Terminal 1
cd C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\anuncio_agent
claude

# Terminal 2
cd C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\pesquisa_agent
claude

# Terminal 3
cd C:\Users\Dell\Documents\GitHub\lm.codexa\codexa.app\agentes\marca_agent
claude

# ... repeat for all agents
```

### Step 2: Prime Each Terminal
In each terminal, run:
```
/prime-codexa
```

### Step 3: Paste Input
Copy from `COPY_PASTE_INPUT.md`, replace [VARIABLES], paste in terminal.

### Step 4: Monitor Progress
Each terminal executes autonomously. Watch for:
- Phase transitions (═══ announcements)
- Task completions (✅ marks)
- Error handling (❌ marks)

### Step 5: Collect Reports
Each agent generates:
- Upgrade report (files changed, quality score)
- Updated iso_vectorstore
- Version bump to 2.5.0

---

## EXPECTED OUTCOMES

### Per Agent
- [ ] iso_vectorstore standardized (20 files)
- [ ] 12 Leverage Points applied
- [ ] Version updated to 2.5.0
- [ ] Quality score ≥ 85/100
- [ ] Upgrade report generated

### System-wide
- [ ] All 7 agents at v2.5.0
- [ ] Consistent iso_vectorstore format
- [ ] Unified TAC-7 HOP format
- [ ] Dual-Layer architecture verified

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Agent doesn't start | Check /prime-codexa ran |
| Files not found | Verify [AGENT_PATH] is correct |
| Execution stops | Check for missing dependencies |
| Low quality score | Review specific failing checks |
| Version not updated | Manually update PRIME, README |

---

## REUSABILITY

### For Future Upgrades (v2.5.0 → v3.0.0)
1. Update `TARGET_VERSION` in template
2. Add new Leverage Points (if any)
3. Update iso_vectorstore standard (if changed)
4. Run same process

### For New Agents
1. Copy template from existing agent
2. Replace [VARIABLES]
3. Run upgrade process
4. Verify output

---

## AXIOMS APPLIED

- **"One Agent, One Prompt, One Purpose"** (OPOP): Each agent has single responsibility
- **"Build the system that builds the system"**: Meta-construction pattern
- **"Trust but verify"**: Feedback loops in every phase
- **"$arguments Chaining"**: Phase N output → Phase N+1 input
- **"Context is everything, but too much is nothing"**: Optimized context loading

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-25 | Initial documentation |

---

**Status**: Production Ready
**Maintainer**: CODEXA Meta-Constructor
**Axiom**: "Build the system that builds the system"
