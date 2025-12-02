# 206_ADW_SUBAGENT_CONSTRUCTION | Claude Code Subagent System Builder

**Version**: 1.0.0 | **Created**: 2025-12-02
**Type**: ADW (Agentic Developer Workflow)
**Duration**: 15-30min for full system | 5min per individual agent
**Pattern**: Discovery → Template → Generate → Validate → Document

---

## MODULE_METADATA

```yaml
id: 206_ADW_SUBAGENT_CONSTRUCTION
version: 1.0.0
category: meta-construction
type: ADW
execution_mode: sequential_with_parallel_generation
dependencies:
  - 95_meta_build_subagent_HOP.md
  - .claude/agents/TEMPLATE_subagent.md
  - SubagentStop hook
status: production_ready
created: 2025-12-02
distilled_from: Voice-guided implementation session
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "subagent_construction",
  "workflow_name": "Claude Code Subagent System Builder",
  "version": "1.0.0",
  "context_strategy": "discovery_first",

  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "create_subagent"},
    {"phase_id": "phase_1_discovery", "phase_name": "Agent Discovery", "duration": "2-3min"},
    {"phase_id": "phase_2_template", "phase_name": "Template Preparation", "duration": "1-2min"},
    {"phase_id": "phase_3_generate", "phase_name": "Subagent Generation", "duration": "5-15min"},
    {"phase_id": "phase_4_hooks", "phase_name": "Hook Integration", "duration": "2-3min"},
    {"phase_id": "phase_5_validate", "phase_name": "Validation & Testing", "duration": "3-5min"},
    {"phase_id": "phase_6_document", "phase_name": "Documentation", "duration": "2-3min"}
  ]
}
```

---

## USE CASE

### When to Use

- Setting up Claude Code subagent system for a new project
- Adding new agents to existing subagent infrastructure
- Migrating existing agents to Claude Code subagent types
- Creating parallel execution capabilities

### When NOT to Use

- Simple single-agent tasks
- Agents without established PRIME.md
- Projects not using Claude Code

---

## PHASE 0: Knowledge Loading (Cross-Agent)

**Objective**: Load prompt engineering knowledge from mentor_agent before construction

### Task Boundary
```
TASK_BOUNDARY: KNOWLEDGE_LOADING
ACCESS: read_only
SCOPE: Load cross-agent knowledge for better subagent construction
MODULE: builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md
```

### Actions

```
0.1. Detect task type:
     task_type = "create_subagent" (from task_hint or auto-detect)

0.2. Load knowledge graph:
     Read: mentor_agent/FONTES/knowledge_graph.json
     Get: task_types["create_subagent"]

0.3. Load required knowledge:
     - codexa_agent/iso_vectorstore/23_subagent_patterns.md
     - mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md

0.4. Load recommended knowledge (if context allows):
     - mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md
     - mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_task_management_20251201.md
     - mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_advanced_techniques_20251202.md

0.5. Store in context:
     $loaded_knowledge = {patterns, playbook, techniques}
```

### Output

```yaml
$knowledge_context:
  task_type: create_subagent
  loaded_files: 5
  cross_agent_sources: [mentor_agent]
  patterns_available:
    - tool_calling
    - task_management
    - advanced_techniques
  ready_for_construction: true
```

### Apply in Subsequent Phases

Use loaded knowledge to:
- **Phase 3**: Apply tool_calling pattern when defining subagent tools
- **Phase 3**: Apply task_management pattern for CRITICAL section
- **Phase 5**: Validate against prompt engineering best practices

---

## PHASE 1: Agent Discovery

**Objective**: Identify all agents that need subagent type definitions

### Task Boundary
```
TASK_BOUNDARY: DISCOVERY
ACCESS: read_only
SCOPE: List all agents, check existing subagent types
```

### Actions

```
1.1. List all agents in project:
     glob: **/agentes/*/PRIME.md

1.2. List existing subagent types:
     ls: .claude/agents/*.md

1.3. Identify gaps:
     - Agents without subagent types
     - Outdated subagent definitions

1.4. Prioritize by usage:
     - Core domain agents first
     - Support agents second
```

### Output

```yaml
$agent_inventory:
  total_agents: 12
  existing_subagents: 6
  missing_subagents:
    - curso_agent
    - photo_agent
    - video_agent
    - scout_agent
    - ronronalda_agent
    - voice_agent
  priority_order: [...]
```

---

## PHASE 2: Template Preparation

**Objective**: Ensure template and infrastructure are ready

### Task Boundary
```
TASK_BOUNDARY: PREPARATION
ACCESS: read_write
SCOPE: Verify/create template and directory structure
```

### Actions

```
2.1. Verify .claude/agents/ directory exists
     mkdir -p .claude/agents/

2.2. Check TEMPLATE_subagent.md exists
     If not: Create from knowledge base

2.3. Verify SubagentStop hook is configured
     Check: .claude/settings.json SubagentStop entry

2.4. Prepare placeholder reference:
     - {{AGENT_NAME}}
     - {{AGENT_DESCRIPTION}}
     - {{AGENT_ID}}
     - {{PROJECT_PATH}}
     - {{MODEL}}
     - {{PERMISSION_MODE}}
     - {{TOOLS}}
     - {{CRITICAL_FILES}}
     - {{WORKFLOW_FILE}}
```

### Output

```yaml
$infrastructure:
  directory_ready: true
  template_ready: true
  hook_configured: true
  placeholders_documented: true
```

---

## PHASE 3: Subagent Generation

**Objective**: Create subagent type definitions for all identified agents

### Task Boundary
```
TASK_BOUNDARY: GENERATION
ACCESS: write
SCOPE: Create .claude/agents/{name}-agent.md files
```

### Actions

For each agent in `$agent_inventory.missing_subagents`:

```
3.1. Read agent PRIME.md:
     - Extract purpose, capabilities
     - Identify tools used
     - Note model recommendations
     - Find quality standards

3.2. Determine configuration:
     Model selection:
       opus:   marca_agent, photo_agent (creative)
       sonnet: pesquisa_agent, anuncio_agent, curso_agent, video_agent, mentor_agent, ronronalda_agent
       haiku:  qa_agent, scout_agent, voice_agent (fast/simple)

     Permission mode:
       default:     read-heavy agents
       acceptEdits: write-heavy agents

3.3. Compose description:
     Format: "Use for [action1], [action2], and [action3]. Ideal for [context]."
     Include: Domain keywords for auto-detection

3.4. Generate CRITICAL section:
     1. mcp__scout__smart_context call
     2. PRIME.md path
     3. Critical iso_vectorstore files
     4. Workflow file reference

3.5. Write subagent file:
     Path: .claude/agents/{agent_name without _agent}-agent.md
```

### Parallel Execution Option

If generating multiple subagents, can parallelize:
```
Batch 1 (parallel): pesquisa, anuncio, marca
Batch 2 (parallel): curso, photo, video
Batch 3 (parallel): scout, mentor, qa
Batch 4 (parallel): ronronalda, voice
```

### Output

```yaml
$generated_subagents:
  - path: .claude/agents/pesquisa-agent.md
    status: created
    size: 2.5KB
  - path: .claude/agents/anuncio-agent.md
    status: created
    size: 2.4KB
  # ...
```

---

## PHASE 4: Hook Integration

**Objective**: Configure SubagentStop hook for metrics and notifications

### Task Boundary
```
TASK_BOUNDARY: INTEGRATION
ACCESS: write
SCOPE: Update hooks and settings
```

### Actions

```
4.1. Update subagent_stop.py:
     - Add new agent types to SUBAGENT_TYPES list
     - Ensure type detection patterns work
     - Configure TTS messages for new types

4.2. Update settings.json:
     - Verify SubagentStop hook entry
     - Add --notify flag if not present

4.3. Test hook invocation (dry run):
     - Simulate subagent completion
     - Verify metrics logging
     - Test TTS announcement
```

### Output

```yaml
$hook_integration:
  subagent_types_updated: true
  settings_configured: true
  tts_messages_added: true
```

---

## PHASE 5: Validation & Testing

**Objective**: Verify all subagent definitions are valid and functional

### Task Boundary
```
TASK_BOUNDARY: VALIDATION
ACCESS: read_only
SCOPE: Syntax check, structure validation, integration test
```

### Actions

```
5.1. YAML frontmatter validation:
     For each subagent file:
       - Check required fields (name, description, tools, model, permissionMode)
       - Validate field types
       - Verify no syntax errors

5.2. Structure validation:
     - CRITICAL section present
     - Scout tools included
     - Context loading instructions clear
     - Language instructions present

5.3. Auto-detection test:
     For each subagent:
       - Review description keywords
       - Estimate detection likelihood
       - Flag ambiguous descriptions

5.4. Integration test (optional):
     - Spawn test subagent
     - Verify context loading
     - Check hook fires
     - Confirm metrics recorded
```

### Output

```yaml
$validation_results:
  total_files: 12
  yaml_valid: 12
  structure_valid: 12
  auto_detection_ready: 12
  integration_tested: true

  issues_found: []
```

---

## PHASE 6: Documentation

**Objective**: Document the subagent system for users and maintainers

### Task Boundary
```
TASK_BOUNDARY: DOCUMENTATION
ACCESS: write
SCOPE: Create/update architecture and usage docs
```

### Actions

```
6.1. Create/update SUBAGENT_ARCHITECTURE.md:
     - System overview diagram
     - Subagent types table
     - Usage instructions
     - Hook integration details
     - Constraints and limitations

6.2. Create implementation report:
     - Files created
     - Validation results
     - Metrics configuration
     - Next steps

6.3. Update codexa_agent PRIME.md:
     - Add subagent construction section
     - Reference new HOP and ADW
     - Document /spawn-agents command

6.4. Create spawn-agents command:
     - .claude/commands/spawn-agents.md
     - Define task types
     - Document parallel execution patterns
```

### Output

```yaml
$documentation:
  architecture_doc: .claude/SUBAGENT_ARCHITECTURE.md
  implementation_report: .claude/SUBAGENT_IMPLEMENTATION_REPORT.md
  command_doc: .claude/commands/spawn-agents.md
  prime_updated: true
```

---

## EXECUTION CHECKLIST

```markdown
## Subagent Construction Checklist

### Pre-Flight
- [ ] Project uses Claude Code
- [ ] Agents have PRIME.md files
- [ ] .claude/ directory exists

### Phase 1: Discovery
- [ ] Listed all agents
- [ ] Identified missing subagent types
- [ ] Prioritized generation order

### Phase 2: Preparation
- [ ] .claude/agents/ directory ready
- [ ] TEMPLATE_subagent.md available
- [ ] SubagentStop hook configured

### Phase 3: Generation
- [ ] All subagent files created
- [ ] YAML frontmatter valid
- [ ] CRITICAL sections present
- [ ] Scout tools included

### Phase 4: Hooks
- [ ] SUBAGENT_TYPES list updated
- [ ] settings.json configured
- [ ] TTS messages added

### Phase 5: Validation
- [ ] All files pass syntax check
- [ ] Structure validation passed
- [ ] Auto-detection reviewed
- [ ] Integration tested

### Phase 6: Documentation
- [ ] Architecture doc created
- [ ] Implementation report written
- [ ] Command documentation added
- [ ] PRIME.md updated
```

---

## SUCCESS CRITERIA

```yaml
workflow_success:
  all_agents_covered: true
  yaml_valid: 100%
  structure_valid: 100%
  hooks_integrated: true
  documentation_complete: true

metrics:
  subagent_files_created: N
  total_lines_added: ~1500
  validation_score: 100%
```

---

## RELATED WORKFLOWS

- `95_meta_build_subagent_HOP.md` - Individual subagent construction
- `203_ADW_PARALLEL_ORCHESTRATION.md` - Using subagents in parallel
- `97_ADW_NEW_AGENT_WORKFLOW.md` - Creating new domain agents

---

## LESSONS LEARNED

### From Voice-Guided Implementation

1. **Discovery-first approach essential**
   - Always inventory existing agents before generating
   - Check for existing subagent types to avoid duplicates

2. **Template + hydration pattern works**
   - TEMPLATE_subagent.md enables consistency
   - Placeholders make universal reuse possible

3. **Context loading is the key differentiator**
   - Without CRITICAL section, subagents are generic
   - Scout integration enables full domain knowledge

4. **Parallel generation saves time**
   - Batch independent agents together
   - 4 batches of 3 agents each = efficient

5. **Hook integration completes the system**
   - Metrics by type enable analytics
   - TTS notifications improve UX

---

**Version**: 1.0.0
**Status**: Production-Ready
**Distilled From**: Voice-guided implementation session (2025-12-02)
**Duration**: 15-30min for complete system
