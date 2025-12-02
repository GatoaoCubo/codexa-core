<!-- iso_vectorstore -->
<!--
  Source: 96_meta_orchestrate_HOP.md
  Agent: codexa_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 96_meta_orchestrate_HOP | Multi-Phase Workflow Orchestrator

**ID**: meta_orchestrate_HOP | **Version**: 2.0.0 | **Created**: 2025-11-13 | **Updated**: 2025-11-24
**Purpose**: Orchestrate multi-phase ADW workflows with $arguments chaining and context management
**Dependencies**: None (orchestrates other HOPs/scripts) | **Category**: orchestrator | **Framework**: TAC-7
**Usage**: Complex multi-phase workflows | Agent construction | System automation

---

## PROMPT_LAYER_COMPOSITION

This HOP composes the following prompt layers for orchestration:

| Layer | Purpose | Usage in HOP |
|-------|---------|--------------|
| `01_identity_layer.md` | Agent identity & role | Defines orchestrator personality |
| `02_operating_modes.md` | 7 operating modes | Uses ORCHESTRATION mode (manages phases) |
| `03_tool_usage_layer.md` | Tool definitions | All tools for phase execution |
| `08_workflows.md` | Workflow patterns | Multi-phase ADW pattern |

**Composition Type**: `ORCHESTRATION_AGENT` (Identity + Modes + Tools + Workflows)

**Runtime Composition**:
```python
from src.runtime import PromptLoader, CompositionType

loader = PromptLoader()
base_prompt = loader.load_composition(CompositionType.ORCHESTRATION_AGENT)
hop_prompt = loader.load_hop("96_meta_orchestrate_HOP")
full_prompt = base_prompt + "\n\n" + hop_prompt
```

---

## TASK_BOUNDARY

**Mode**: ORCHESTRATION (manages multi-phase execution)

**Mode Transitions**:
```
IDLE → ORCHESTRATION (on workflow_spec received)
ORCHESTRATION → PLANNING (Phase 1: validate deps)
PLANNING → EXECUTION (Phase N: run phase)
EXECUTION → VERIFICATION (Phase N: validate outputs)
VERIFICATION → EXECUTION (next phase or retry)
VERIFICATION → ORCHESTRATION (phase complete)
ORCHESTRATION → IDLE (all phases complete)
```

**Constraints**:
- Sequential phase execution (no parallel phases)
- Dependency-ordered execution (topological sort)
- Context management per strategy
- Failure handling per workflow_spec

**Progress Communication**:
```python
from builders.task_boundary import TaskBoundary, AgentMode

boundary = TaskBoundary(mode=AgentMode.ORCHESTRATION, workflow_name="ADW Workflow")
# Dynamic tasks based on workflow phases
for phase in workflow_spec.phases:
    boundary.add_task(
        f"Execute {phase.name}",
        f"Executing {phase.name}",
        estimated_min=phase.estimated_duration
    )
```

---

## SRC_INTEGRATION

This HOP integrates with the following `src/` modules:

**Orchestrator** (`src/orchestrator.py`):
```python
from src.orchestrator import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator(workflow_spec)
result = await orchestrator.execute()
```

**Workflow Executor** (`src/workflow_executor.py`):
```python
from src.workflow_executor import WorkflowExecutor, WorkflowState

executor = WorkflowExecutor()
state = WorkflowState(workflow_id=workflow_spec.workflow_id)

for phase in sorted_phases:
    state = await executor.execute_phase(phase, state)
```

**Multi-Agent Coordination** (`builders/multi_agent_orchestrator.py`):
```python
from builders.multi_agent_orchestrator import MultiAgentOrchestrator

# For workflows involving multiple agents
orchestrator = MultiAgentOrchestrator(agents=[agent1, agent2])
result = await orchestrator.coordinate(workflow_spec)
```

---

## INPUT_CONTRACT

### Required
- **$workflow_spec** (object) - Workflow orchestration specification | Format: `{workflow_id, workflow_name, phases: [{phase_id, phase_name, command_or_hop (path/command), inputs: {$var: source}, outputs: [$var1, $var2], depends_on: [phase_id], validation: {}}], context_strategy (full_history|last_step|custom), failure_handling (stop|continue|retry)}` | Validation: ≥3 phases | Dependencies resolvable (no cycles) | Input vars traceable | Valid context strategy

### Optional
- **$context_config** (object) - Custom context management | Default: Use workflow_spec.context_strategy | Structure: `{max_history: number|null, accumulate: boolean, selective_passing: {phase_N: [phase_ids]}}`
- **$validation_strict** (boolean) - Strict validation per phase | Default: true
- **$verbose** (boolean) - Detailed logging | Default: false

---

## OUTPUT_CONTRACT

### Primary
- **$workflow_result** (object) - Complete workflow execution result | Format: All phase outputs + metadata | Structure: `{workflow_id, status (success|partial|failure), phases_completed, total_phases, execution_time_seconds, phase_results: [{phase_id, phase_name, status, outputs: {}, duration_seconds, timestamp}], final_outputs: {}, context_chain: [], error_log: []}` | Validation: All phases executed/logged | Status accurate | Final outputs contain all phase outputs | Context chain documented

### Secondary
- **$execution_log** (array) - Detailed execution trace | Structure: `[{timestamp, phase_id, event_type, data}]`
- **$context_history** (object) - Full context passed between phases | Structure: `{phase_N: {all_context}}`

---

## TASK

**Role**: Multi-Phase Workflow Orchestrator (CODEXA)

**Objective**: Execute complex multi-phase workflows with explicit $arguments chaining between phases, context management, and failure handling

**Quality Standards**: All phases executed in dependency order | $arguments properly chained phase-to-phase | Context managed per strategy | Failures handled per spec | Full traceability | Validation at each phase

**Constraints**: Follow workflow_spec exactly | Respect phase dependencies | No parallel execution (sequential only) | Validate outputs before passing | Stop on failure (if failure_handling=stop)

**Input**: $workflow_spec + optional ($context_config, $validation_strict, $verbose)
**Output**: $workflow_result (complete execution result + metadata)

---

## STEPS

### STEP 1: Parse & Validate Workflow Specification
**Extract**: Workflow ID/name | All phases (≥3) | Phase dependencies | I/O mappings | Context strategy | Failure handling | **Validate**: No circular dependencies | All input sources exist | Commands/HOPs accessible | Context strategy valid

### STEP 2: Build Dependency Graph
**Create**: Phase execution order respecting depends_on | **Topological sort**: Phases in dependency order | **Validate**: No cycles detected | All dependencies resolvable | Execution plan valid

### STEP 3: Initialize Context Manager
**Setup**: Context storage based on $context_config or workflow_spec.context_strategy | **Strategies**: full_history (accumulate all), last_step (only previous), custom (selective) | **Initialize**: Empty context object for phase 1

### STEP 4: Execute Phases Sequentially
**For each phase** in dependency order:
1. **Prepare inputs**: Resolve $var sources from context/previous phases
2. **Pass context**: Apply context_strategy (full_history/last_step/custom)
3. **Execute**: Invoke command_or_hop with inputs + context
4. **Capture outputs**: Store phase outputs with $var names
5. **Apply Operational Patterns**: See STEP 4.5 below
6. **Validate**: If $validation_strict=true, check phase.validation rules
7. **Update context**: Add phase outputs to context manager
8. **Handle failures**: If phase fails, apply failure_handling (stop/continue/retry)
9. **Log**: Record phase execution (timestamp, duration, status, outputs)

### STEP 4.5: Apply Operational Orchestration Patterns
**Advanced Context Management**: Leverage proven patterns from operational knowledge base

**Entropy-Driven Context Strategy**:
- Measure context entropy per phase: `entropy = -σ p(token_i) * log(p(token_i))` (token frequency)
- Dynamic strategy selection: If entropy >60 → last_step (reduce noise), <30 → full_history (maintain clarity)
- Context compression: High-entropy phases → extract key $vars only (selective_passing)

**Agent Coordination Protocol** (if workflow involves multiple agents):
- Message routing: Implement AgentMessage structure (source, target, type, payload, timestamp)
- Synchronization points: Define phase barriers where agents must sync state
- Handoff validation: Verify payload structure before phase transitions

**Axiom Alignment Tracking**:
- Workflow axioms: Define core quality principles (e.g., "All phases pass validation before proceeding")
- Phase-level entropy scoring: Track alignment with workflow axioms per phase
- Degradation detection: If phase entropy exceeds threshold → trigger grace protocol

**Grace Protocol Integration**:
- Failure taxonomy: Classify failures (validation, execution, timeout, resource)
- Recovery matrix: Map failure types to recovery strategies (retry, skip, fallback, abort)
- State checkpointing: Save workflow state before each phase (enable rollback)
- Partial success handling: If failure_handling=continue, track partial outputs + error context

**Knowledge Consolidation Across Phases**:
- Versiculo accumulation: If workflow generates knowledge, consolidate as versículos (semantic units)
- Entropy classification: Tag phase outputs by actionability (purely-contextual/actionable/theoretical)
- Vector store integration: Package final outputs for embedding + retrieval

**Validation Enhancement**:
- Axiom compliance per phase: Check phase outputs align with workflow axioms
- Entropy baseline validation: Warn if phase output entropy exceeds acceptable range
- Context chain integrity: Verify $var lineage traceable across all phases
- Recovery path validation: Test grace protocol triggers before production use

### STEP 5: Aggregate Final Outputs
**Collect**: All phase outputs from completed phases | **Merge**: Into $final_outputs object | **Document**: $context_chain showing data flow between phases

### STEP 6: Generate Execution Result
**Compile**: $workflow_result with status (success if all phases passed), phases_completed, execution_time, phase_results[], final_outputs, context_chain, error_log[] | **Return**: Complete $workflow_result object

---

## VALIDATION

**Quality Gates**:
- ✅ **Dependency Resolution**: All phase dependencies satisfied | Verify: Topological sort successful | Fix: Reorder phases, remove cycles
- ✅ **Phase Execution**: All phases executed in order | Verify: phases_completed = total_phases | Fix: Re-run failed phase
- ✅ **Arguments Chaining**: $vars properly passed between phases | Verify: Check context_chain | Fix: Correct input source mappings
- ✅ **Output Completeness**: All expected outputs present | Verify: Each phase outputs match spec | Fix: Re-execute phase
- ✅ **Validation Rules Passed**: If strict mode, all phase validations passed | Verify: No validation failures in log | Fix: Address failed validations
- ✅ **Context Management**: Context strategy applied correctly | Verify: Context size matches strategy | Fix: Adjust context_config
- ✅ **Error Handling**: Failures handled per failure_handling | Verify: Check status + error_log | Fix: Retry or adjust strategy
- ✅ **Traceability**: Full execution log available | Verify: $execution_log complete | Fix: Regenerate from phase_results

**Quality Score** (1-10): Execution success 40% | Chaining correctness 25% | Context management 15% | Validation passing 10% | Traceability 10% | **Min acceptable: 7.0** | If <7.0: Identify failed phases, review dependencies, re-execute

---

## CONTEXT

**Usage**: Complex multi-phase agent construction | System automation workflows | Meta-construction pipelines | ADW workflow execution

**Upstream**: User provides $workflow_spec (orchestration definition) | Phase executables (HOPs/scripts) available | Optional: $context_config for custom strategies

**Downstream**: $workflow_result → Analysis/reporting | Final outputs → Use in subsequent steps | Execution log → Debugging/optimization

**Argument Chaining**: Core orchestrator in ADW patterns | Pattern: `[Define workflow_spec] → meta_orchestrate_HOP → $workflow_result → [Use final_outputs]`
Example 3-phase: `workflow_spec: {phases: [{id: plan, outputs: [$plan]}, {id: build, inputs: {$plan: phase.plan}, outputs: [$artifacts]}, {id: document, inputs: {$artifacts: phase.build}, outputs: [$docs]}]}` → Orchestrator chains $plan→build→document

**Assumptions**: Environment (Python 3.10+, uv if needed) | Executables (All phase commands/HOPs accessible + functional) | Dependencies (Phase deps correctly specified) | Context (Sufficient for all phases) | Phases (Idempotent, no side effects between phases)

---

## ARTIFACT_OUTPUTS

This HOP generates the following artifacts:

### Primary Artifacts (Workflow State)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `$workflow_result` | Complete execution result | In-memory / returned |
| `$execution_log` | Detailed execution trace | In-memory / returned |
| `wf_{id}_state.json` | Workflow state checkpoint | `src/.codexa/workspace/workflows/` |

### Secondary Artifacts (##report)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `{execution_id}_report.md` | Workflow execution report | `outputs/` |
| `{execution_id}_report.json` | Workflow execution data | `outputs/` |

**Report Generation**:
```python
from artifacts.generators.report_generator import ExecutionReportBuilder, ReportGenerator

report_data = (ExecutionReportBuilder()
    .with_feature_name(workflow_spec.workflow_name)
    .with_metrics({
        "phases_completed": phases_completed,
        "total_phases": total_phases,
        "execution_time_seconds": execution_time
    })
    .build())

generator = ReportGenerator()
generator.generate_execution_report(report_data, Path(f"outputs/{execution_id}_report.md"))
```

---

## FEEDBACK_LOOP

**Pattern**: Execute Phase → Validate → Fix/Retry → Continue (Per-Phase Loop)

**Implementation**:
```python
def orchestration_with_recovery(workflow_spec, max_retries_per_phase=2):
    results = []

    for phase in sorted_phases:
        for attempt in range(max_retries_per_phase):
            # Execute phase
            result = execute_phase(phase, context)

            # Validate phase output
            if validate_phase_output(result, phase.validation):
                results.append(result)
                update_context(context, result)
                break  # Phase success, continue to next

            # Retry logic
            if attempt < max_retries_per_phase - 1:
                log_retry(phase, attempt)
                continue

            # Max retries exceeded
            if workflow_spec.failure_handling == "stop":
                raise PhaseExecutionError(phase, result)
            elif workflow_spec.failure_handling == "continue":
                results.append({"status": "failed", "phase": phase.id})
                break

    return aggregate_results(results)
```

**Quality Gates (Per Phase)**:
- Phase dependencies satisfied
- Input $vars resolved from context
- Phase execution successful
- Output $vars captured
- Validation rules passed (if strict mode)

**Multi-Agent Orchestration Pattern**:
```python
from builders.multi_agent_orchestrator import MultiAgentOrchestrator

# For workflows with multiple specialized agents
orchestrator = MultiAgentOrchestrator(
    agents={
        "planner": planning_agent,
        "executor": execution_agent,
        "reviewer": review_agent
    },
    coordination_strategy="sequential"  # or "parallel", "handoff"
)

result = await orchestrator.execute_workflow(workflow_spec)
```

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Related**: 96_codexa_orchestrate.md (command) | workflows/*_ADW_*.md (workflow examples)

**Changelog v2.0.0**:
- Added PROMPT_LAYER_COMPOSITION section
- Added TASK_BOUNDARY section with ORCHESTRATION mode
- Added SRC_INTEGRATION section with orchestrator/executor examples
- Added ARTIFACT_OUTPUTS section with ##report integration
- Added FEEDBACK_LOOP section (Per-Phase recovery pattern)
- Added Multi-Agent Orchestration Pattern
