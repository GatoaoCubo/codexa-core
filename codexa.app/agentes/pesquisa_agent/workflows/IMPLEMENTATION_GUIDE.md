# ADW IMPLEMENTATION GUIDE | Replicating Workflow Pattern to Other Agents

**Purpose**: Step-by-step guide to implement complete execution workflows for any CODEXA agent
**Audience**: Developers/LLMs replicating this pattern in new terminal sessions
**Reference Implementation**: pesquisa_agent (100_ADW_RUN_PESQUISA.md)
**Version**: 1.0.0 | **Date**: 2025-11-17

---

## OVERVIEW

This guide enables you to **replicate the ADW pattern** from `pesquisa_agent` to any other CODEXA agent:
- anuncio_agent
- marca_agent
- mentor_agent
- photo_agent
- codexa_agent (if needed)
- Any new agent created with `/codexa-build_agent`

**What You'll Create**:
1. `workflows/` directory in target agent
2. `100_ADW_RUN_{AGENT}.md` - Complete execution workflow
3. `ADW_TEMPLATE.md` - Template for future workflows
4. `README_WORKFLOWS.md` - Workflow documentation
5. Update `sync_iso_vectorstore.py` to include workflows
6. Sync to `iso_vectorstore/` for portability

**Estimated Time**: 30-45 minutes per agent

---

## PREREQUISITES

**Before starting:**

1. **Reference Implementation Available**:
   - Path: `codexa.app/agentes/pesquisa_agent/workflows/`
   - Files: `100_ADW_RUN_PESQUISA.md`, `ADW_TEMPLATE.md`, `IMPLEMENTATION_GUIDE.md` (this file)

2. **Target Agent Exists**:
   - Has `PRIME.md` with clearly defined steps
   - Has `README.md`, `INSTRUCTIONS.md`, `SETUP.md`
   - Has clear input/output contracts

3. **Tools Available**:
   - Terminal access to `codexa.app/agentes/`
   - Text editor or LLM with file write capabilities
   - Python 3.8+ (for sync script)

---

## PHASE 1: DISCOVERY (5-10 minutes)

**Objective**: Understand target agent structure

### Step 1.1: Read Agent Documentation

```bash
cd codexa.app/agentes/{target_agent}/

# Read in this order:
# 1. PRIME.md - Extract workflow steps
# 2. README.md - Understand structure
# 3. INSTRUCTIONS.md - Understand operations
# 4. config/*.json - Understand configuration
```

**Extract from PRIME.md**:
- How many steps/phases does the agent have?
- What are the inputs (required/optional)?
- What are the outputs (primary/secondary)?
- What capabilities are required (web_search, vision, etc.)?
- What validation rules exist?

**Document**:
```markdown
# {TARGET_AGENT} Workflow Analysis

**Steps**: {N} steps identified
**Inputs**: {list}
**Outputs**: {list}
**Capabilities**: {list}
**Duration**: {estimated}
```

### Step 1.2: Identify Workflow Pattern

**Common Patterns**:

**Pattern 1: Sequential Execution** (like pesquisa_agent):
- Input → Phase 1 → Phase 2 → ... → Phase N → Output
- Each phase depends on previous
- Linear flow

**Pattern 2: Parallel + Merge**:
- Input → [Phase 1a, Phase 1b, Phase 1c] (parallel) → Merge → Phase 2 → Output
- Some phases can run in parallel
- Merge results before next phase

**Pattern 3: Conditional Branching**:
- Input → Phase 1 → Decision Point → [Branch A OR Branch B] → Phase 3 → Output
- Workflow path depends on conditions
- Multiple execution paths

**Identify**: Which pattern fits your target agent?

---

## PHASE 2: PREPARATION (5 minutes)

**Objective**: Set up directories and copy templates

### Step 2.1: Create Workflows Directory

```bash
cd codexa.app/agentes/{target_agent}/

# Create workflows directory
mkdir -p workflows

# Verify creation
ls -la workflows/
```

### Step 2.2: Copy Templates

```bash
# Copy ADW_TEMPLATE.md from pesquisa_agent
cp ../pesquisa_agent/workflows/ADW_TEMPLATE.md ./workflows/

# Copy IMPLEMENTATION_GUIDE.md (this file) for reference
cp ../pesquisa_agent/workflows/IMPLEMENTATION_GUIDE.md ./workflows/

# Verify files
ls -la workflows/
# Should see: ADW_TEMPLATE.md, IMPLEMENTATION_GUIDE.md
```

---

## PHASE 3: ADW CREATION (20-30 minutes)

**Objective**: Create complete execution workflow

### Step 3.1: Create ADW File

```bash
cd workflows/

# Create ADW file (replace {TARGET_AGENT} with actual name)
touch 100_ADW_RUN_{TARGET_AGENT}.md
```

**Example**: For anuncio_agent → `100_ADW_RUN_ANUNCIO.md`

### Step 3.2: Fill ADW Header

Use this template:

```markdown
# 100_ADW_RUN_{AGENT} | {One-line description}

**Purpose**: {End-to-end goal}
**Type**: {N}-Phase ADW (Agentic Developer Workflow) | **Duration**: {estimated}
**Output**: {primary outputs}
**Status**: Production-Ready | **Version**: 1.0.0

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "{agent}_complete_execution",
  "workflow_name": "{Agent} Complete Execution",
  "agent": "{agent_name}",
  "version": "1.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4o / claude-sonnet-3.5+",

  "required_capabilities": {
    "{capability}": true/false
  },

  "phases": [
    {
      "phase_id": "phase_1_{name}",
      "phase_name": "{Phase Name}",
      "duration": "{X}min",
      "prime_step": "Step 1",
      "description": "{What this phase does}"
    }
  ]
}
```
```

### Step 3.3: Map PRIME.md Steps to ADW Phases

**For each step in PRIME.md**:

1. **Extract Step Information**:
   - Step number
   - Step objective
   - Step actions (numbered list)
   - Step inputs (what it needs)
   - Step outputs (what it produces)
   - Step validation (success criteria)

2. **Create ADW Phase Section**:

```markdown
## PHASE {N}: {Phase Name}

**Objective**: {Clear objective from PRIME.md}

**Actions**:
1. {Action 1 from PRIME.md}
2. {Action 2 from PRIME.md}
3. {Action 3 from PRIME.md}
... (copy all actions)

**Input**:
- `$variable_from_previous_phase` (type) - {description}
- `$config_reference` (JSON) - {description}

**Output**:
- `$output_variable_1` (type) - {description}
- `$output_variable_2` (type) - {description}

**Validation**:
- ✅ {Validation check 1}
- ✅ {Validation check 2}
- ✅ {Validation check 3}

**Error Handling**:
- If {condition} → {action}
- If {condition} → {action}
```

3. **Repeat for all PRIME.md steps**

### Step 3.4: Add Prerequisites Section

```markdown
## PREREQUISITES

**Before starting, ensure:**

1. **Context Loaded**:
   - Read `PRIME.md` (agent instructions)
   - Read `{config_file}.json` (configuration)
   - Read `templates/{template}.md` (if applicable)

2. **Capabilities Available**:
   - `{capability_1}`: {REQUIRED / Optional}
   - `{capability_2}`: {REQUIRED / Optional}

3. **User Input Ready**:
   - {Required input 1} (type) - {description}
   - {Required input 2} (type) - {description}
   - Optional: {optional input} (type) - {description}
```

### Step 3.5: Add Execution Instructions

```markdown
## EXECUTION INSTRUCTIONS

### For AI Assistants (Conversational Mode)

**Step 1: Load Context**
```
Read the following files in order:
1. {agent}/PRIME.md (complete instructions)
2. {agent}/{relevant_config}.json (configuration)
3. {agent}/templates/{template}.md (if applicable)
4. This file (100_ADW_RUN_{AGENT}.md) for workflow steps
```

**Step 2: Obtain User Input**
```
Ask user for {agent-specific input} with minimum fields:
- {Required field 1}
- {Required field 2}
- {Required field 3}

Optional:
- {Optional field 1}
- {Optional field 2}
```

**Step 3: Execute Workflow**
```
Follow phases 1-{N} sequentially:
- Announce phase start: "Starting Phase X: {phase_name}"
- Execute phase actions as detailed above
- Validate phase outputs
- If validation fails → report error + suggest fix
- Announce phase completion: "Phase X complete. Moving to Phase Y."
```

**Step 4: Report Completion**
```
Upon completion, report:
- Duration: {actual_minutes} minutes
- Quality score: {score}/{max}
- Completeness: {percentage}%
- Files saved: {output_dir}/{files}
- Next step: {downstream action or agent}
```

### For Python Automation (Future - Phase B)

**Script location**: `{agent}/workflows/run_{agent}.py`

**Usage**:
```bash
python run_{agent}.py \
  --input "{user_input}" \
  --output {output_dir}/ \
  --model {model_name}
```

**Note**: Python automation script to be implemented in Phase B.
```

### Step 3.6: Add Success Criteria

```markdown
## SUCCESS CRITERIA

### Workflow Level
- ✅ All {N} phases completed without errors
- ✅ Duration ≤{max} minutes (target: {target} min)
- ✅ No phase validation failures

### Output Level
- ✅ {Primary output} generated with all required blocks/sections
- ✅ {Secondary output 1} generated (e.g., metadata.json)
- ✅ {Secondary output 2} generated (e.g., quality report)
- ✅ Quality score ≥{threshold}
- ✅ Completeness ≥{percentage}%

### Quality Level
- ✅ {Quality metric 1 specific to agent}
- ✅ {Quality metric 2 specific to agent}
- ✅ {Quality metric 3 specific to agent}
```

### Step 3.7: Add Troubleshooting

```markdown
## TROUBLESHOOTING

### Phase {N} Issues
**Error**: "{common_error_message}"
→ **Solution**: {solution_steps}

**Warning**: "{common_warning_message}"
→ **Solution**: {solution_steps}

### Common Issues Across Phases
**Error**: "{cross-phase_error}"
→ **Solution**: {solution}
```

### Step 3.8: Add Related Files & Version History

```markdown
## RELATED FILES

**Core Documentation**:
- `PRIME.md` - Agent instructions (entry point)
- `README.md` - Agent structure and navigation
- `SETUP.md` - Platform-specific setup guides
- `INSTRUCTIONS.md` - Operational instructions

**Configuration**:
- `config/{config_file}.json` - {description}

**Templates**:
- `templates/{template}.md` - {description}

**Output Directory**:
- `{output_dir}/` - All outputs saved here

---

## VERSION HISTORY

**v1.0.0** ({date}):
- Initial ADW creation
- {N}-phase workflow (mapped from PRIME.md Steps 1-{N})
- Complete validation gates
- Quality scoring system
- Conversational execution mode
- Python automation stub (Phase B prep)

---

## NEXT STEPS

**Immediate** (Phase A):
1. Test this ADW with sample input
2. Validate outputs against quality gates
3. Document any issues or improvements

**Phase B** (Python Automation):
1. Create `run_{agent}.py` script
2. Implement LLM API integration (Anthropic/OpenAI)
3. Add CLI arguments for input
4. Add batch processing mode
5. Add CI/CD integration hooks

**Replication** (Other Agents):
1. Use this ADW as template for remaining agents
2. Follow IMPLEMENTATION_GUIDE.md
3. Document agent-specific adaptations

---

**Status**: Production-Ready (Phase A) | Phase B pending
**Maintainer**: CODEXA Meta-Constructor
**Contact**: See agentes/README.md for system navigation
```

---

## PHASE 4: DOCUMENTATION (5 minutes)

**Objective**: Create workflow documentation

### Step 4.1: Create README_WORKFLOWS.md

```bash
cd workflows/

touch README_WORKFLOWS.md
```

**Content Template**:

```markdown
# Workflows Documentation | {AGENT_NAME}

**Agent**: {agent_name}
**Version**: {version}
**Workflows Available**: {count}

---

## AVAILABLE WORKFLOWS

### 100_ADW_RUN_{AGENT}.md ⭐ PRIMARY

**Purpose**: Complete {agent purpose} execution
**Duration**: {X-Y} minutes
**Input**: {brief description}
**Output**: {brief description}
**Status**: Production-Ready

**When to use**:
- {Use case 1}
- {Use case 2}
- {Use case 3}

**How to execute**:
```
1. Load PRIME.md + this workflow
2. Provide {input}
3. Follow {N} phases sequentially
4. Validate outputs
```

---

## WORKFLOW PATTERNS

**Pattern Used**: {Sequential / Parallel / Conditional}

**Phases**:
1. Phase 1: {name} ({duration})
2. Phase 2: {name} ({duration})
...
{N}. Phase {N}: {name} ({duration})

**Total Duration**: {sum}

---

## QUALITY GATES

All workflows include validation:
- ✅ {Quality metric 1}
- ✅ {Quality metric 2}
- ✅ {Quality metric 3}

**Minimum Quality Score**: {threshold}

---

## FUTURE WORKFLOWS (Planned)

### 101_ADW_QUICK_{AGENT}.md
- Abbreviated workflow (main steps only)
- Duration: {X} minutes
- Use case: {when to use}

### 102_ADW_{SPECIALTY}_{AGENT}.md
- Specialized workflow for {use case}
- Duration: {X} minutes

---

## PHASE B: PYTHON AUTOMATION

**Status**: Planned
**Script**: `run_{agent}.py`
**Features**:
- LLM API integration (Anthropic/OpenAI)
- CLI arguments for batch processing
- CI/CD hooks
- Quality reporting

---

## RELATED FILES

- `ADW_TEMPLATE.md` - Template for creating new workflows
- `IMPLEMENTATION_GUIDE.md` - Guide for replicating to other agents
- `../PRIME.md` - Agent instructions (source of workflow steps)

---

**Version**: 1.0.0 | **Updated**: {date}
```

---

## PHASE 5: INTEGRATION (10 minutes)

**Objective**: Integrate workflow into agent ecosystem

### Step 5.1: Update sync_iso_vectorstore.py

```bash
cd codexa.app/agentes/

# Open sync_iso_vectorstore.py
# Find: get_agent_specific_files() function
```

**Add workflow files to agent's specific files**:

```python
def get_agent_specific_files(agent_name: str) -> Dict[str, Tuple[str, str]]:
    """Get agent-specific files (configs, schemas, prompts, etc.)"""

    specific_files = {}

    if agent_name == "{target_agent}":
        specific_files = {
            # ... existing files ...
            "17_{agent}_workflow_adw.md": ("{agent}/workflows/100_ADW_RUN_{AGENT}.md", "Complete execution workflow"),
            # If file count >20, adjust numbering or consolidate
        }
```

**Example for pesquisa_agent** (already done):

```python
elif agent_name == "pesquisa_agent":
    specific_files = {
        "11_pesquisa_agent_config.json": ("pesquisa_agent/config/agent.json", "Agent configuration"),
        "12_pesquisa_brief_schema.json": ("pesquisa_agent/config/brief_schema.json", "Research brief schema"),
        "13_pesquisa_execution_plan_schema.json": ("pesquisa_agent/config/execution_plan_schema.json", "Execution plan schema"),
        "14_pesquisa_marketplaces.json": ("pesquisa_agent/config/marketplaces.json", "Marketplace configurations"),
        "15_pesquisa_main_hop.md": ("pesquisa_agent/prompts/main_agent_hop.md", "Main workflow HOP"),
        "16_pesquisa_competitor_analysis.md": ("pesquisa_agent/prompts/competitor_analysis.md", "Competitor analysis workflow"),
        "17_pesquisa_workflow_adw.md": ("pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md", "Complete execution workflow")
    }
```

### Step 5.2: Sync to iso_vectorstore

```bash
# Sync target agent
python sync_iso_vectorstore.py {target_agent}

# Example:
python sync_iso_vectorstore.py pesquisa_agent

# Verify sync
ls -la {target_agent}/iso_vectorstore/
# Should see: 17_{agent}_workflow_adw.md (or appropriate number)
```

### Step 5.3: Update Agent README

```bash
cd {target_agent}/

# Edit README.md
# Add workflows section:
```

**Add to README.md**:

```markdown
## 🔄 WORKFLOWS

**Complete Execution**: See `workflows/100_ADW_RUN_{AGENT}.md`
- {N}-phase automated workflow
- Duration: {X-Y} minutes
- Input: {brief description}
- Output: {brief description}

**Quick Start**:
```
1. Load workflows/100_ADW_RUN_{AGENT}.md
2. Provide {input}
3. Execute {N} phases
4. Validate outputs
```

**Documentation**: See `workflows/README_WORKFLOWS.md`
```

---

## PHASE 6: TESTING (10 minutes)

**Objective**: Validate workflow execution

### Step 6.1: Prepare Test Input

Create realistic test input for your agent:

**Example (pesquisa_agent)**:
```
Product: Garrafa térmica de aço inoxidável 1L
Category: Casa e Jardim > Cozinha > Utilidades Domésticas
Target Audience: Profissionais que trabalham fora, 25-45 anos
Price Range: R$ 89 - R$ 149
Marketplace: Mercado Livre (primary)
```

### Step 6.2: Execute Workflow Conversationally

**In LLM interface**:

```
Load the following files:
1. {agent}/PRIME.md
2. {agent}/workflows/100_ADW_RUN_{AGENT}.md
3. {agent}/templates/{template}.md (if applicable)

Execute the workflow with this input:
{paste test input}

Follow all {N} phases sequentially and report:
- Phase completion status
- Validation results
- Quality scores
- Output files generated
```

### Step 6.3: Validate Outputs

**Check**:
- ✅ All phases completed without errors
- ✅ Duration within target range
- ✅ All output files generated
- ✅ Quality score ≥ threshold
- ✅ Validation gates passed

**Document any issues**:
- Missing validations
- Unclear instructions
- Edge cases not handled
- Performance bottlenecks

### Step 6.4: Iterate if Needed

If issues found:
1. Update ADW file with fixes
2. Re-sync to iso_vectorstore
3. Re-test
4. Document changes in VERSION HISTORY

---

## PHASE 7: DOCUMENTATION (5 minutes)

**Objective**: Document implementation for future reference

### Step 7.1: Create Implementation Report

```bash
cd {target_agent}/workflows/

touch IMPLEMENTATION_REPORT_{DATE}.md
```

**Content**:

```markdown
# ADW Implementation Report | {AGENT_NAME}

**Date**: {date}
**Implemented by**: {name/LLM}
**Duration**: {actual time taken}

---

## SUMMARY

**Workflow Created**: 100_ADW_RUN_{AGENT}.md
**Phases**: {N}
**Target Duration**: {X-Y} minutes
**Status**: ✅ Tested & Validated

---

## IMPLEMENTATION NOTES

### Deviations from Template
- {Deviation 1 and reason}
- {Deviation 2 and reason}

### Agent-Specific Adaptations
- {Adaptation 1}
- {Adaptation 2}

### Challenges Encountered
- {Challenge 1} → {Solution}
- {Challenge 2} → {Solution}

---

## TEST RESULTS

**Test Input**: {brief description}
**Execution Duration**: {actual} minutes
**Quality Score**: {score}
**Completeness**: {percentage}%
**Validation**: ✅ Passed / ❌ Failed (details)

---

## NEXT STEPS

**Immediate**:
- [ ] Update PRIME.md to reference workflow
- [ ] Update INSTRUCTIONS.md to reference workflow
- [ ] Sync to iso_vectorstore

**Phase B** (Python Automation):
- [ ] Create run_{agent}.py
- [ ] Implement LLM API integration
- [ ] Add CI/CD hooks

---

## REPLICATION NOTES

**For next agent implementation**:
- {Lesson learned 1}
- {Lesson learned 2}
- {Improvement suggestion 1}
```

---

## CHECKLIST: Complete Implementation

Use this checklist when implementing ADW for any agent:

### Discovery Phase
- [ ] Read PRIME.md and extract workflow steps
- [ ] Identify input/output contracts
- [ ] Determine required capabilities
- [ ] Document workflow pattern (sequential/parallel/conditional)

### Preparation Phase
- [ ] Create workflows/ directory
- [ ] Copy ADW_TEMPLATE.md
- [ ] Copy IMPLEMENTATION_GUIDE.md

### Creation Phase
- [ ] Create 100_ADW_RUN_{AGENT}.md
- [ ] Fill header with workflow specification (JSON)
- [ ] Map all PRIME.md steps to ADW phases
- [ ] Add prerequisites section
- [ ] Add execution instructions (conversational + Python stub)
- [ ] Add success criteria
- [ ] Add troubleshooting section
- [ ] Add related files & version history

### Documentation Phase
- [ ] Create README_WORKFLOWS.md
- [ ] Update agent README.md with workflow section

### Integration Phase
- [ ] Update sync_iso_vectorstore.py with workflow files
- [ ] Sync to iso_vectorstore/
- [ ] Verify files in iso_vectorstore/

### Testing Phase
- [ ] Prepare test input
- [ ] Execute workflow conversationally
- [ ] Validate outputs against success criteria
- [ ] Document issues and iterate if needed

### Final Documentation
- [ ] Create IMPLEMENTATION_REPORT_{DATE}.md
- [ ] Document deviations, adaptations, challenges
- [ ] Document test results
- [ ] Document lessons learned for next agent

---

## QUICK REFERENCE: Agent-Specific Variations

### anuncio_agent
**Workflow Pattern**: Sequential
**Phases**: ~5-7 (copy intake → research lookup → copy generation → validation → formatting)
**Key Differences**: Heavy reliance on pesquisa_agent outputs, persuasion patterns, marketplace specs

### marca_agent
**Workflow Pattern**: Sequential with conditional branching
**Phases**: ~4-6 (brand audit → strategy → identity → guidelines → validation)
**Key Differences**: Strategic depth, brand positioning, visual identity generation

### mentor_agent
**Workflow Pattern**: Conditional branching (different paths for different queries)
**Phases**: ~3-5 (query analysis → knowledge retrieval → guidance synthesis → validation)
**Key Differences**: Knowledge base navigation, context-aware responses

### photo_agent
**Workflow Pattern**: Sequential
**Phases**: ~6-8 (brief intake → scene planning → camera setup → lighting → composition → rendering → post-processing → validation)
**Key Differences**: Visual generation, technical specifications, quality assessment

---

## TROUBLESHOOTING GUIDE

### Issue: "PRIME.md doesn't have clear steps"

**Solution**:
1. Look for numbered sections, headers, or action lists
2. If workflow is implicit, infer from:
   - INPUT_CONTRACT → OUTPUT_CONTRACT flow
   - STEPS section in TAC-7 format
   - Examples showing execution order
3. Consult INSTRUCTIONS.md for operational details
4. Create logical phases based on transformation: input → processing → output

### Issue: "Too many steps (>10 phases)"

**Solution**:
1. Group related steps into phases (e.g., steps 2-4 → Phase 2: Data Collection)
2. Target 5-9 phases for optimal workflow
3. Create sub-phases within phases if needed
4. Consider creating 101_ADW_QUICK_{AGENT}.md for abbreviated workflow

### Issue: "Agent has multiple workflows (different use cases)"

**Solution**:
1. Create 100_ADW_RUN_{AGENT}.md for most common/complete use case
2. Create 101_ADW_{USE_CASE}_{AGENT}.md for variant workflows
3. Document differences in README_WORKFLOWS.md

### Issue: "iso_vectorstore file count exceeds 20"

**Solution**:
1. Consolidate smaller files
2. Prioritize workflow file inclusion (high value)
3. Consider embedding workflow content in INSTRUCTIONS.md as appendix
4. Or increase limit if justified (discuss with team)

---

## REPLICATION RECORD

**Track implementations across agents**:

| Agent | Status | Date | Duration | Notes |
|-------|--------|------|----------|-------|
| pesquisa_agent | ✅ Complete | 2025-11-17 | 45min | Reference implementation |
| anuncio_agent | ⏳ Pending | - | - | Next target |
| marca_agent | ⏳ Pending | - | - | - |
| mentor_agent | ⏳ Pending | - | - | - |
| photo_agent | ⏳ Pending | - | - | - |

**Update this table** as you implement each agent.

---

## CONTACT & SUPPORT

**Questions?**
- See `codexa.app/agentes/README.md` for system navigation
- See `codexa.app/agentes/codexa-agent/PRIME.md` for meta-construction principles
- Use `/codexa-when_to_use` for decision trees

**Improvements?**
- Update this guide with lessons learned
- Document edge cases in TROUBLESHOOTING section
- Share patterns in agent-specific IMPLEMENTATION_REPORT

---

**Version**: 1.0.0
**Created**: 2025-11-17
**Maintainer**: CODEXA Meta-Constructor
**Reference**: pesquisa_agent implementation
**License**: Internal use only (EcomLM Codexa system)

---

> 🎯 **Goal**: Make ADW replication a 30-45 minute task for any agent
> 📚 **Principle**: Build the system that makes it easy to build workflows
> ✅ **Success**: When any developer/LLM can replicate this pattern without guidance
