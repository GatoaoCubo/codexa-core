# PHASE 0: KNOWLEDGE LOADING | Universal Pre-Task Context Module

**Version**: 1.0.0 | **Created**: 2025-12-02
**Type**: ADW Module (Reusable Phase)
**Duration**: 1-3min
**Pattern**: Detect → Route → Load → Validate → Store

---

## MODULE_METADATA

```yaml
id: PHASE_0_KNOWLEDGE_LOADING
version: 1.0.0
category: pre-task
type: ADW_module
execution_mode: sequential_blocking
dependencies:
  - knowledge_graph.json
  - knowledge_router_HOP.md
  - mcp__scout__discover
  - mcp__scout__smart_context
status: production_ready
created: 2025-12-02
reusable: true
```

---

## PURPOSE

**Phase 0** is a universal pre-task module that loads cross-agent knowledge BEFORE executing any workflow. It ensures agents have access to relevant documentation, patterns, and context from other domains to improve output quality.

### When to Include Phase 0

Include this phase in any ADW when:
- Task spans multiple domains (e.g., creating subagent needs prompt engineering knowledge)
- Task requires specialized knowledge from another agent
- Output quality depends on following established patterns
- Cross-agent learning would improve results

### When to Skip Phase 0

Skip this phase when:
- Task is purely mechanical (e.g., file operations)
- All required knowledge is agent-native
- Task is time-critical and context is already loaded
- User explicitly requests minimal context

---

## PHASE SPECIFICATION

```json
{
  "phase_id": "phase_0_knowledge_loading",
  "phase_name": "Knowledge Loading (Pre-Task)",
  "duration": "1-3min",
  "blocking": true,
  "optional": false,
  "output_required": "$loaded_knowledge"
}
```

---

## EXECUTION FLOW

### Step 0.1: Detect Task Type

**Objective**: Identify what type of task is being executed

**Actions**:

```
0.1.1. Analyze task description/user request:
       - Extract keywords and triggers
       - Match against known task types
       - Calculate confidence score

0.1.2. Load knowledge graph:
       Read: mentor_agent/FONTES/knowledge_graph.json

0.1.3. Match task type:
       For each task_type in knowledge_graph.task_types:
         - Check if any trigger matches request
         - Calculate confidence (0.0-1.0)
         - Select highest confidence match

0.1.4. Validate detection:
       If confidence < 0.5:
         - Fall back to generic knowledge
         - Warn user about uncertainty
       If confidence >= 0.5:
         - Proceed with detected type
```

**Task Type Triggers** (from knowledge_graph.json):

| Task Type | Triggers | Confidence Boosters |
|-----------|----------|-------------------|
| `create_subagent` | subagent, build agent, Task tool, spawn | "Claude Code", "meta" |
| `create_agent` | novo agente, new agent, from scratch | "complete", "full" |
| `create_hop` | HOP, Higher-Order Prompt, TAC-7 | "meta-prompt", "template" |
| `create_adw` | ADW, workflow, Agentic Developer | "phases", "orchestration" |
| `create_anuncio` | anuncio, listing, produto, marketplace | "Mercado Livre", "SEO" |
| `market_research` | pesquisa, research, concorrencia | "analysis", "competitors" |
| `brand_strategy` | marca, brand, identidade, arquetipo | "positioning", "visual" |
| `photo_prompt` | foto, photo, imagem, Midjourney | "product photography" |
| `video_creation` | video, script, storyboard, Runway | "animation", "tutorial" |
| `course_creation` | curso, aula, tutorial, Hotmart | "learning", "workbook" |
| `quality_validation` | QA, qualidade, validacao, review | "check", "validate" |
| `knowledge_processing` | conhecimento, processar, RASCUNHO | "structure", "index" |

**Output**:

```yaml
$task_detection:
  detected_type: "create_subagent"
  confidence: 0.95
  matched_triggers: ["subagent", "build agent"]
  primary_agent: "codexa_agent"
```

---

### Step 0.2: Load Prerequisites from Knowledge Graph

**Objective**: Get the list of required and recommended knowledge files

**Actions**:

```
0.2.1. Extract knowledge requirements:
       From knowledge_graph.task_types[$detected_type]:
         - required_knowledge[]
         - recommended_knowledge[]
         - estimated_tokens

0.2.2. Identify cross-agent sources:
       For each knowledge path:
         - Parse agent name from path
         - If agent != current_agent:
           - Add to cross_agent_sources[]

0.2.3. Check auto-inject rules:
       For each rule in knowledge_graph.auto_inject_rules:
         - Evaluate condition
         - If matches, add to required/recommended

0.2.4. Calculate total context load:
       - Sum estimated_tokens from all files
       - Warn if exceeds 50K tokens
```

**Output**:

```yaml
$knowledge_requirements:
  required_files:
    - path: codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md
      source_agent: codexa_agent
      estimated_tokens: 5000
      reason: "Subagent construction patterns"

    - path: codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md
      source_agent: mentor_agent
      estimated_tokens: 8000
      reason: "Prompt engineering best practices"

  recommended_files:
    - path: codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md
      source_agent: mentor_agent
      estimated_tokens: 2000
      reason: "Tool usage patterns"

  cross_agent_sources: ["mentor_agent"]
  total_estimated_tokens: 15000
```

---

### Step 0.3: Load Required Knowledge

**Objective**: Read all required knowledge files into context

**Actions**:

```
0.3.1. Use Scout for intelligent discovery:
       If source_agent != current_agent:
         mcp__scout__smart_context(agent=source_agent)

0.3.2. Read required files:
       For each file in $knowledge_requirements.required_files:
         Read(file_path=file.path)
         Store content in $loaded_knowledge.required[file.path]

0.3.3. Validate loaded content:
       For each loaded file:
         - Check file exists and is readable
         - Verify content length > 0
         - Confirm file type matches expectation
         - Flag any loading errors

0.3.4. Handle loading failures:
       If any required file fails to load:
         - Log error with file path
         - Attempt fallback (e.g., PRIME.md)
         - Continue if possible, abort if critical
```

**Output**:

```yaml
$loaded_knowledge:
  required:
    "codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md":
      status: loaded
      size: 5234
      tokens: ~5000

    "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md":
      status: loaded
      size: 8912
      tokens: ~8000

  recommended: {}

  loading_errors: []
  total_files_loaded: 2
  total_tokens_loaded: 13000
```

---

### Step 0.4: Load Recommended Knowledge (Conditional)

**Objective**: Load additional knowledge if context budget allows

**Actions**:

```
0.4.1. Check context budget:
       current_tokens = $loaded_knowledge.total_tokens_loaded
       remaining_budget = 100000 - current_tokens - estimated_task_tokens

       If remaining_budget < 5000:
         - Skip recommended files
         - Log reason: "Context budget exhausted"

0.4.2. Load recommended files (if budget allows):
       For each file in $knowledge_requirements.recommended_files:
         If remaining_budget >= file.estimated_tokens:
           Read(file_path=file.path)
           Store in $loaded_knowledge.recommended[file.path]
           remaining_budget -= file.estimated_tokens

0.4.3. Prioritize by importance:
       If cannot load all recommended:
         - Sort by relevance score
         - Load highest priority first
         - Stop when budget exhausted
```

**Output**:

```yaml
$loaded_knowledge:
  # ... (required files from 0.3)

  recommended:
    "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md":
      status: loaded
      size: 2145
      tokens: ~2000

  skipped_recommended:
    - path: "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_advanced_techniques_20251202.md"
      reason: "Context budget limit reached"

  total_files_loaded: 3
  total_tokens_loaded: 15000
```

---

### Step 0.5: Store Knowledge Context

**Objective**: Make loaded knowledge available for subsequent phases

**Actions**:

```
0.5.1. Create knowledge summary:
       - List all loaded files with paths
       - Summarize key concepts from each
       - Extract actionable patterns/templates
       - Note any warnings or constraints

0.5.2. Generate loading report:
       Format: Markdown table
       Columns: File | Source Agent | Purpose | Status

0.5.3. Store in workflow state:
       $workflow_state.knowledge_context = {
         loaded_files: [...],
         key_patterns: [...],
         constraints: [...],
         cross_agent_sources: [...]
       }

0.5.4. Prepare for Phase 1:
       - Set context_loaded flag = true
       - Log total tokens consumed
       - Proceed to next phase
```

**Output**:

```markdown
## Phase 0 Complete: Knowledge Loaded

### Loaded Files (3 total, ~15K tokens)

| File | Source | Purpose | Status |
|------|--------|---------|--------|
| 23_subagent_patterns.md | codexa_agent | Subagent construction patterns | ✓ Loaded |
| playbook_prompt_engineering_20251201.md | mentor_agent | Prompt engineering best practices | ✓ Loaded |
| pattern_tool_calling_20251201.md | mentor_agent | Tool usage patterns | ✓ Loaded |

### Key Patterns Extracted

1. **Subagent Structure** (from 23_subagent_patterns.md):
   - YAML frontmatter with name, description, tools, model, permissionMode
   - CRITICAL section with context loading instructions
   - Scout integration for domain knowledge access

2. **Prompt Quality** (from playbook_prompt_engineering_20251201.md):
   - Clear instructions with examples
   - Structured output schemas
   - Error handling patterns

3. **Tool Calling** (from pattern_tool_calling_20251201.md):
   - Parallel vs sequential execution
   - Parameter validation
   - Error recovery

### Cross-Agent Knowledge

This task uses knowledge from: **mentor_agent**

### Context Budget

- Tokens loaded: 15,000
- Tokens remaining: ~85,000
- Ready for Phase 1: ✓

---

Proceeding to Phase 1...
```

---

## INTEGRATION EXAMPLES

### Example 1: Adding Phase 0 to Subagent Construction ADW

**Original ADW** (206_ADW_SUBAGENT_CONSTRUCTION.md):

```json
{
  "phases": [
    {"phase_id": "phase_1_discovery", "phase_name": "Agent Discovery"},
    {"phase_id": "phase_2_template", "phase_name": "Template Preparation"},
    // ...
  ]
}
```

**With Phase 0**:

```json
{
  "phases": [
    {"phase_id": "phase_0_knowledge_loading", "phase_name": "Knowledge Loading", "module": "PHASE_0_KNOWLEDGE_LOADING"},
    {"phase_id": "phase_1_discovery", "phase_name": "Agent Discovery"},
    {"phase_id": "phase_2_template", "phase_name": "Template Preparation"},
    // ...
  ]
}
```

**Modified Phase 1** (now uses loaded knowledge):

```markdown
## PHASE 1: Agent Discovery

**Objective**: Identify all agents that need subagent type definitions

**Pre-Loaded Knowledge** (from Phase 0):
- Subagent patterns from codexa_agent
- Prompt engineering playbook from mentor_agent

### Actions

1.1. List all agents in project:
     glob: **/agentes/*/PRIME.md

     **Apply Pattern**: Use subagent_patterns.md detection rules

1.2. List existing subagent types:
     ls: .claude/agents/*.md

     **Apply Pattern**: Validate against playbook quality standards

// ... rest of phase uses loaded patterns
```

---

### Example 2: Adding Phase 0 to HOP Creation Workflow

```markdown
# 204_ADW_HOP_CONSTRUCTION | Higher-Order Prompt Builder

## WORKFLOW SPECIFICATION

```json
{
  "phases": [
    {
      "phase_id": "phase_0_knowledge_loading",
      "phase_name": "Knowledge Loading",
      "module": "PHASE_0_KNOWLEDGE_LOADING",
      "task_hint": "create_hop"
    },
    {
      "phase_id": "phase_1_requirements",
      "phase_name": "Requirements Analysis"
    },
    // ...
  ]
}
```

**Phase 0 Configuration**:
- Detected task type: `create_hop`
- Required knowledge:
  - TAC-7 specification (from codexa_agent)
  - Task management patterns (from mentor_agent)
- Recommended knowledge:
  - Advanced techniques (from mentor_agent)

**Phase 1 then uses**:
- TAC-7 categories from loaded spec
- Task management patterns for structuring HOP
- Quality standards for validation
```

---

### Example 3: Conditional Phase 0 (Skip if Context Pre-Loaded)

```markdown
## PHASE 0: Knowledge Loading (Conditional)

**Check if knowledge already loaded**:

```python
if workflow_state.get("knowledge_context", {}).get("context_loaded"):
    print("✓ Knowledge already loaded in previous workflow")
    print(f"  Files: {len(workflow_state.knowledge_context.loaded_files)}")
    print(f"  Tokens: {workflow_state.knowledge_context.total_tokens}")
    print("  Skipping Phase 0...")
    proceed_to_phase_1()
else:
    execute_phase_0()
```

This pattern is useful for multi-stage workflows where Phase 0 runs once at the beginning and subsequent workflows reuse the loaded context.
```

---

## TASK BOUNDARY

```
TASK_BOUNDARY: KNOWLEDGE_LOADING
ACCESS: read_only (loads but doesn't modify)
SCOPE: Read knowledge_graph.json, load prerequisite files
OUTPUT: $loaded_knowledge (stored in workflow state)
DURATION: 1-3min
BLOCKING: Yes (subsequent phases depend on loaded knowledge)
```

---

## SUCCESS CRITERIA

Phase 0 is successful when:

```yaml
success_criteria:
  task_type_detected: true
  confidence_score: >= 0.5
  required_files_loaded: 100%
  loading_errors: 0
  knowledge_summary_created: true
  workflow_state_updated: true

quality_gates:
  - All required files exist and are readable
  - Cross-agent sources identified
  - Context budget not exceeded
  - Key patterns extracted and documented
```

---

## FAILURE MODES & RECOVERY

### Failure Mode 1: Task Type Not Detected

**Symptoms**: Confidence < 0.5 or no task type match

**Recovery**:
```
1. Use fallback knowledge:
   - Current agent's PRIME.md
   - mentor_agent/PRIME.md
   - Generic quality standards

2. Warn user:
   "Could not detect task type. Using generic knowledge.
    For better results, specify task type explicitly."

3. Proceed with reduced context
```

---

### Failure Mode 2: Required File Not Found

**Symptoms**: File path invalid or file not readable

**Recovery**:
```
1. Try fallback paths:
   - Replace file with agent PRIME.md
   - Use parent directory README.md
   - Skip if no fallback available

2. Log error:
   "WARNING: Required file not found: [path]
    Using fallback: [fallback_path]"

3. Continue with available knowledge
   Set flag: $loaded_knowledge.incomplete = true
```

---

### Failure Mode 3: Context Budget Exceeded

**Symptoms**: total_tokens_loaded > safe_limit

**Recovery**:
```
1. Prioritize required files:
   - Load smallest required files first
   - Skip all recommended files
   - Truncate large files if needed

2. Warn user:
   "Context budget tight. Loaded required files only.
    Recommended files skipped: [list]"

3. Proceed with core knowledge
```

---

### Failure Mode 4: Knowledge Graph Missing

**Symptoms**: knowledge_graph.json not found

**Recovery**:
```
1. Fall back to heuristic detection:
   - Extract keywords from task description
   - Match against known agents' PRIME.md files
   - Load agent-specific context only

2. Warn maintainers:
   "Knowledge graph not found. Using heuristic detection.
    Install knowledge graph: mentor_agent/FONTES/"

3. Proceed with reduced intelligence
```

---

## VALIDATION CHECKLIST

```markdown
## Phase 0 Validation

### Pre-Execution
- [ ] knowledge_graph.json exists
- [ ] Task description provided
- [ ] Current agent identified
- [ ] Context budget calculated

### Task Detection
- [ ] Task type detected (confidence >= 0.5)
- [ ] Triggers matched in knowledge graph
- [ ] Primary agent identified
- [ ] Cross-agent sources noted

### Knowledge Loading
- [ ] All required files loaded successfully
- [ ] Recommended files loaded (if budget allows)
- [ ] No loading errors (or handled gracefully)
- [ ] Total tokens within budget

### Output Generation
- [ ] $loaded_knowledge populated
- [ ] Loading report generated
- [ ] Key patterns extracted
- [ ] workflow_state updated

### Ready for Phase 1
- [ ] context_loaded = true
- [ ] Knowledge accessible to next phase
- [ ] No blocking errors
```

---

## METRICS TO TRACK

Track these metrics for Phase 0 performance analysis:

```yaml
phase_0_metrics:
  task_detection:
    - task_type
    - confidence_score
    - detection_time_ms

  knowledge_loading:
    - required_files_count
    - required_files_loaded
    - recommended_files_count
    - recommended_files_loaded
    - total_files_loaded
    - total_tokens_loaded
    - loading_time_ms

  cross_agent_learning:
    - cross_agent_sources_count
    - cross_agent_files_count
    - cross_agent_tokens_loaded

  errors:
    - task_detection_failures
    - file_not_found_errors
    - loading_errors
    - context_budget_exceeded

  quality:
    - key_patterns_extracted
    - constraints_identified
    - fallbacks_used
```

---

## RELATED FILES

| File | Purpose | Relationship |
|------|---------|--------------|
| `knowledge_graph.json` | Task→Knowledge mappings | **Consumed** by Phase 0 |
| `knowledge_router_HOP.md` | Task detection logic | **Implements** same algorithm |
| `ARCHITECTURE_KNOWLEDGE_DISSEMINATION.md` | System architecture | **Describes** knowledge flow |
| `206_ADW_SUBAGENT_CONSTRUCTION.md` | Example ADW using Phase 0 | **Integration** example |
| `mcp__scout__smart_context` | Agent context loader | **Used** for cross-agent discovery |
| `mcp__scout__discover` | File discovery tool | **Used** for finding knowledge |

---

## FUTURE ENHANCEMENTS

### Version 1.1 Planned Features

1. **Cached Knowledge**
   - Store loaded knowledge between sessions
   - Invalidate cache on file changes
   - Share cache across workflows

2. **Smart Prioritization**
   - ML-based relevance scoring
   - User feedback on knowledge quality
   - Adaptive loading based on success metrics

3. **Knowledge Compression**
   - Summarize large files
   - Extract only relevant sections
   - Reduce token consumption

4. **Scout Integration Enhancement**
   ```typescript
   // Future Scout function
   mcp__scout__load_prerequisites(task_type: string): LoadedKnowledge
   ```

5. **Interactive Mode**
   - Ask user to confirm detected task type
   - Let user select optional knowledge
   - Preview token costs before loading

---

## USAGE INSTRUCTIONS

### For ADW Authors

To add Phase 0 to your ADW:

```markdown
1. Add phase to workflow specification:
   {
     "phase_id": "phase_0_knowledge_loading",
     "phase_name": "Knowledge Loading",
     "module": "PHASE_0_KNOWLEDGE_LOADING",
     "task_hint": "your_task_type"  // optional, helps detection
   }

2. Reference loaded knowledge in subsequent phases:
   "**Apply Pattern**: Use [pattern] from loaded knowledge"

3. Include Phase 0 in execution checklist:
   - [ ] Phase 0: Knowledge loaded
   - [ ] Required files: N loaded
   - [ ] Cross-agent sources: [list]
```

### For LLM Agents

When executing an ADW with Phase 0:

```markdown
1. Execute Phase 0 steps sequentially:
   - Detect task type
   - Load prerequisites
   - Read required files
   - Read recommended files (if budget allows)
   - Store in workflow state

2. Use loaded knowledge in subsequent phases:
   - Reference patterns by name
   - Apply templates from loaded files
   - Follow constraints from loaded docs

3. Report Phase 0 completion:
   - Show loaded files table
   - List key patterns extracted
   - Note cross-agent sources
   - Confirm ready for Phase 1
```

---

## TEMPLATE CODE

### Python Implementation (for Scout Integration)

```python
# Future: adw_modules/phase_0_loader.py

import json
from pathlib import Path
from typing import Dict, List, Optional

class Phase0KnowledgeLoader:
    def __init__(self, knowledge_graph_path: str):
        self.knowledge_graph = self._load_graph(knowledge_graph_path)
        self.loaded_knowledge = {
            "required": {},
            "recommended": {},
            "loading_errors": [],
            "total_tokens": 0
        }

    def detect_task_type(self, task_description: str) -> Dict:
        """Detect task type from description using trigger matching."""
        best_match = None
        best_confidence = 0.0

        for task_type, config in self.knowledge_graph["task_types"].items():
            confidence = self._calculate_confidence(
                task_description,
                config["triggers"]
            )

            if confidence > best_confidence:
                best_confidence = confidence
                best_match = task_type

        return {
            "detected_type": best_match,
            "confidence": best_confidence,
            "primary_agent": self.knowledge_graph["task_types"][best_match].get("primary_agent")
        }

    def load_prerequisites(self, task_type: str, context_budget: int = 50000) -> Dict:
        """Load required and recommended knowledge files."""
        config = self.knowledge_graph["task_types"].get(task_type)
        if not config:
            return self._fallback_loading()

        # Load required files
        for file_path in config["required_knowledge"]:
            self._load_file(file_path, category="required")

        # Load recommended files (if budget allows)
        remaining_budget = context_budget - self.loaded_knowledge["total_tokens"]
        for file_path in config["recommended_knowledge"]:
            estimated_tokens = self._estimate_tokens(file_path)
            if remaining_budget >= estimated_tokens:
                self._load_file(file_path, category="recommended")
                remaining_budget -= estimated_tokens

        return self.loaded_knowledge

    def _load_file(self, file_path: str, category: str):
        """Load a single knowledge file."""
        try:
            path = Path(file_path)
            content = path.read_text(encoding="utf-8")
            tokens = len(content) // 4  # rough estimate

            self.loaded_knowledge[category][file_path] = {
                "status": "loaded",
                "size": len(content),
                "tokens": tokens
            }
            self.loaded_knowledge["total_tokens"] += tokens

        except Exception as e:
            self.loaded_knowledge["loading_errors"].append({
                "file": file_path,
                "error": str(e)
            })

    def generate_report(self) -> str:
        """Generate markdown loading report."""
        report = "## Phase 0 Complete: Knowledge Loaded\n\n"
        report += f"### Loaded Files ({self._total_files_loaded()} total, "
        report += f"~{self.loaded_knowledge['total_tokens']/1000:.0f}K tokens)\n\n"
        # ... format table
        return report

    # ... helper methods
```

---

## DISTILLATION NOTES

This template follows **LAW 1: DISTILLATION PRINCIPLE**:

- ✓ No hardcoded agent names (uses placeholders)
- ✓ No hardcoded file paths (uses knowledge_graph.json)
- ✓ No hardcoded task types (loaded from graph)
- ✓ Universal pattern for ANY ADW
- ✓ Reusable across ANY project

To hydrate for a specific project:
1. Customize `knowledge_graph.json` with project-specific task types
2. Update file paths to match project structure
3. Configure context budget limits
4. Add project-specific fallback knowledge

---

**Version**: 1.0.0
**Status**: Production-Ready
**Reusable**: ✓ Universal ADW Module
**Dependencies**: knowledge_graph.json, knowledge_router_HOP.md, Scout MCP
**Duration**: 1-3min per execution
**Token Cost**: Variable (based on task type, typically 5K-20K)

---

## CHANGELOG

### v1.0.0 (2025-12-02)
- Initial release
- Task type detection with confidence scoring
- Required and recommended knowledge loading
- Context budget management
- Cross-agent knowledge discovery
- Integration examples for existing ADWs
- Failure recovery patterns
- Metrics tracking
- Python implementation template
