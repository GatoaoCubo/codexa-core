# ADW_TEMPLATE | Replicable Agent Workflow Pattern

**Purpose**: Template for creating complete execution workflows for any CODEXA agent
**Type**: Meta-Template (build workflows for other agents)
**Version**: 1.0.0 | **Based on**: 100_ADW_RUN_PESQUISA.md

---

## WHEN TO USE THIS TEMPLATE

Use this template to create ADWs (Agentic Developer Workflows) for:

1. **Existing agents** that lack automated workflows:
   - anuncio_agent → Ad copy generation
   - marca_agent → Brand strategy
   - mentor_agent → Mentoring/onboarding
   - photo_agent → Photo generation

2. **New agents** built using `/codexa-build_agent`:
   - After agent creation, use this to build execution workflow

3. **Specialized workflows** for existing agents:
   - Quick workflows (abbreviated steps)
   - Specialized workflows (specific use cases)

---

## TEMPLATE STRUCTURE

### File Naming Convention

```
{agent_name}/workflows/
├── 100_ADW_RUN_{AGENT}.md        # Complete execution workflow
├── 101_ADW_QUICK_{AGENT}.md      # Quick workflow (main steps only)
├── 102_ADW_{SPECIALTY}_{AGENT}.md # Specialized workflow
├── ADW_TEMPLATE.md                # This template (copy to each agent)
└── README_WORKFLOWS.md            # Workflow documentation
```

**Numbering**:
- 100-109: Complete execution workflows
- 110-119: Quick workflows
- 120-139: Specialized workflows
- 140-149: Integration workflows (multi-agent)

### Workflow Document Structure

```markdown
# {NUMBER}_ADW_{WORKFLOW_NAME} | {One-line description}

**Purpose**: {End-to-end goal}
**Type**: {N}-Phase ADW | **Duration**: {estimated time}
**Output**: {primary outputs}
**Status**: {Production-Ready / In-Development / Experimental}

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "{unique_id}",
  "workflow_name": "{descriptive_name}",
  "agent": "{agent_name}",
  "version": "1.0.0",
  "context_strategy": "full_history / rolling_window / isolated",
  "failure_handling": "stop_and_report / retry / skip_and_continue",
  "min_llm_model": "{minimum model required}",

  "required_capabilities": {
    "{capability_1}": true/false,
    "{capability_2}": true/false
  },

  "phases": [
    {
      "phase_id": "phase_{N}_{short_name}",
      "phase_name": "{Descriptive Phase Name}",
      "duration": "{estimated_minutes}min",
      "prime_step": "Step {N}",
      "description": "{What this phase does}"
    }
  ]
}
```

---

## PREREQUISITES

**Before starting, ensure:**

1. **Context Loaded**:
   - Read `PRIME.md` (agent instructions)
   - Read relevant config files
   - Read templates (if applicable)

2. **Capabilities Available**:
   - {List required capabilities}
   - {List optional capabilities}

3. **User Input Ready**:
   - {List required inputs}
   - {List optional inputs}

---

## PHASE {N}: {Phase Name}

**Objective**: {Clear objective}

**Actions**:
1. {Action 1}
2. {Action 2}
3. {Action 3}

**Input**:
- `$variable_from_previous_phase`
- `$config_file_reference`

**Output**:
- `$output_variable_1`
- `$output_variable_2`

**Validation**:
- ✅ {Validation check 1}
- ✅ {Validation check 2}
- ✅ {Validation check 3}

**Error Handling**:
- If {condition} → {action}
- If {condition} → {action}

---

## EXECUTION INSTRUCTIONS

### For AI Assistants (Conversational Mode)

**Step 1: Load Context**
```
Read the following files:
1. {agent}/PRIME.md
2. {agent}/{relevant_config}.json
3. This workflow (ADW file)
```

**Step 2: Obtain User Input**
```
Ask user for:
- {Required input 1}
- {Required input 2}
- Optional: {Optional input}
```

**Step 3: Execute Workflow**
```
Follow phases sequentially:
- Announce phase start
- Execute phase actions
- Validate outputs
- Report completion
```

**Step 4: Report Completion**
```
Report:
- Duration
- Quality metrics
- Outputs saved
- Next steps
```

### For Python Automation (Phase B)

**Script location**: `{agent}/workflows/run_{agent}.py`

**Usage**:
```bash
python run_{agent}.py \
  --input "{user_input}" \
  --output {output_dir} \
  --model {model_name}
```

---

## SUCCESS CRITERIA

### Workflow Level
- ✅ All phases completed
- ✅ Duration within target
- ✅ No validation failures

### Output Level
- ✅ {Output 1} generated
- ✅ {Output 2} generated
- ✅ Quality score ≥{threshold}

### Quality Level
- ✅ {Quality metric 1}
- ✅ {Quality metric 2}

---

## TROUBLESHOOTING

### Phase {N} Issues
**Error**: "{error_message}"
→ **Solution**: {solution}

**Warning**: "{warning_message}"
→ **Solution**: {solution}

---

## RELATED FILES

**Core Documentation**:
- `PRIME.md` - Agent instructions
- `README.md` - Agent structure
- `INSTRUCTIONS.md` - Operations

**Configuration**:
- `config/{relevant}.json` - Config files

**Templates**:
- `templates/{relevant}.md` - Output templates

---

## VERSION HISTORY

**v1.0.0** ({date}):
- Initial workflow creation
- {N}-phase structure
- {Key features}

---

## NEXT STEPS

**Phase A** (Conversational):
1. Test with sample input
2. Validate outputs
3. Document improvements

**Phase B** (Automation):
1. Create Python script
2. Implement LLM API integration
3. Add CI/CD hooks

**Replication**:
1. Use as template for other agents
2. Document adaptations
3. Maintain consistency

---

**Status**: {Status}
**Maintainer**: CODEXA Meta-Constructor
