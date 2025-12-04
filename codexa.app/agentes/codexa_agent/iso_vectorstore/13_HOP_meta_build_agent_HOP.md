<!-- iso_vectorstore -->
<!--
  Source: 91_meta_build_agent_HOP.md
  Agent: codexa_agent
  Synced: 2025-12-02
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 91_meta_build_agent_HOP | Meta-Construction Agent Builder

**ID**: meta_build_agent_HOP | **Version**: 2.0.0 | **Created**: 2025-11-13 | **Updated**: 2025-11-24
**Purpose**: Guide autonomous agent construction (5-phase meta-constructor workflow)
**Dependencies**: 02_agent_meta_constructor.py | **Category**: builder | **Framework**: TAC-7
**Usage**: Execution plans | Workflow orchestration | Autonomous agent creation

---

## PROMPT_LAYER_COMPOSITION

This HOP composes the following prompt layers for agent construction:

| Layer | Purpose | Usage in HOP |
|-------|---------|--------------|
| `01_identity_layer.md` | Agent identity & role | Defines meta-constructor personality |
| `02_operating_modes.md` | 7 operating modes | Uses PLANNING → EXECUTION → VERIFICATION flow |
| `03_tool_usage_layer.md` | Tool definitions | References Read, Glob, Grep, Write for artifact creation |
| `08_workflows.md` | Workflow patterns | 5-phase ADW pattern (Plan→Build→Test→Review→Document) |

**Composition Type**: `EXECUTION_AGENT` (Identity + Modes + Tools + Code + Workflows)

**Runtime Composition**:
```python
from src.runtime import PromptLoader, CompositionType

loader = PromptLoader()
base_prompt = loader.load_composition(CompositionType.EXECUTION_AGENT)
hop_prompt = loader.load_hop("91_meta_build_agent_HOP")
full_prompt = base_prompt + "\n\n" + hop_prompt
```

---

## TASK_BOUNDARY

**Mode**: EXECUTION (with PLANNING sub-phase)

**Mode Transitions**:
```
IDLE → PLANNING (Phase 1: Strategic Planning)
PLANNING → EXECUTION (Phase 2-3: Artifact Construction + Testing)
EXECUTION → VERIFICATION (Phase 4: Critical Review)
VERIFICATION → EXECUTION (if fixes needed)
VERIFICATION → DOCUMENTATION (Phase 5: Final docs)
DOCUMENTATION → IDLE (workflow complete)
```

**Constraints**:
- READ_ONLY in PLANNING phase (no file writes)
- WRITE_ENABLED in EXECUTION phase (artifact creation)
- READ_ONLY in VERIFICATION phase (analysis only)
- WRITE_ENABLED in DOCUMENTATION phase (final files)

**Progress Communication** (using TaskBoundary):
```python
from builders.task_boundary import TaskBoundary, AgentMode

boundary = TaskBoundary(mode=AgentMode.EXECUTION, workflow_name="Agent Construction")
boundary.add_task("Create strategic plan", "Creating strategic plan", estimated_min=10)
boundary.add_task("Generate artifacts", "Generating artifacts", estimated_min=30)
# ... continue for all 5 phases
```

---

## SRC_INTEGRATION

This HOP integrates with the following `src/` modules:

**LLM Providers** (`src/llm/`):
```python
from src import ProviderFactory, ModelType

# Use Opus for meta-construction (complex reasoning)
provider = ProviderFactory.create_provider(model=ModelType.CLAUDE_OPUS)
result = await provider.complete(messages=[...])
```

**Tool Execution** (`src/tools/`):
```python
from src import ToolExecutor, FileTools

executor = ToolExecutor()
files = await FileTools.glob("agents/*/agent-artifacts/*.md")
content = await FileTools.read(file_path)
await FileTools.write(output_path, content)
```

**Runtime** (`src/runtime/`):
```python
from src import AgentRuntime, AgentConfig, PromptLoader

loader = PromptLoader()
prompt = loader.load_hop("91_meta_build_agent_HOP")

config = AgentConfig(
    agent_id="meta-constructor",
    system_prompt=prompt,
    llm_provider=provider,
    tool_executor=executor
)
runtime = AgentRuntime(config=config)
```

**Auth & Rate Limiting** (`src/auth/`):
```python
from src import check_rate_limit, audit_log

await check_rate_limit("claude")  # Before API calls
audit_log("agent_construction", {"agent_name": agent_name})
```

---

## INPUT_CONTRACT

### Required
- **$agent_description** (string) - Clear 1-3 sentence description | Format: NL (purpose, domain, capabilities) | Validation: Non-empty, 20-500 chars, clear purpose + domain | Ex: `"Sentiment analysis agent analyzing product reviews, generating scores (positive/neutral/negative) + justifications"`

### Optional
- **$model** (string) - AI model for construction | Default: "opus" | Validation: ["opus", "sonnet"] | Ex: "opus"
- **$target_dir** (string) - Artifacts save directory | Default: "agents/{adw_id}/agent-artifacts/" | Validation: Valid path (created if needed) | Ex: "agents/sentiment-agent-v1/"
- **$verbose** (boolean) - Verbose logging | Default: false | Validation: Boolean | Ex: true

---

## OUTPUT_CONTRACT

### Primary
- **$agent_artifacts** (object) - Complete deployment-ready artifacts
  - Format: Directory structure (MD + JSON files)
  - Structure: `{adw_id, agent_name, target_directory, artifacts: {MASTER_INSTRUCTIONS.md (2000-5000 words), AGENT_CONFIGURATION.json (OpenAI config), VECTOR_STORE_MANIFEST.md, OUTPUT_SCHEMA.md, README.md, DEPLOYMENT_GUIDE.md, EXAMPLES.md, META_CONSTRUCTION_LOG.md}, workflow_summary}`
  - Validation: All 8 artifacts present | MASTER_INSTRUCTIONS 2000-5000 words | Valid JSON config | README complete | No [VARIABLE] placeholders

### Secondary
- **$workflow_log** (array) - 5-phase execution log | Structure: `[{phase, duration_seconds, inputs, outputs, status}]` for all phases
- **$extracted_variables** (object) - Key construction variables | Structure: `{$agent_name, $agent_purpose, $model_choice, $tools_enabled[], $reasoning_mode}`

---

## TASK

**Role**: Agent Meta-Constructor Module (CODEXA system)

**Objective**: Orchestrate construction of complete, production-ready AI agent via 5-phase meta-construction workflow

**Quality Standards**: All artifacts complete + validated | MASTER_INSTRUCTIONS 2000-5000 words comprehensive | Valid config for target platform | Clear actionable docs | Full traceability (META_CONSTRUCTION_LOG)

**Constraints**: Use only $agent_description (no additional gathering) | Strict 5-phase workflow (no skipping) | Pass context via $arguments | Isolation principle (self-contained agent) | Automatic generation (no manual intervention)

**Input**: $agent_description + optional ($model, $target_dir, $verbose)
**Output**: $agent_artifacts (complete directory structure + all files)

---

## STEPS

### STEP 1: Validate Inputs
**Verify**: $agent_description (non-empty, sufficient detail, clear purpose, domain mentioned) | Prerequisites (Python ≥3.10, uv, 02_agent_meta_constructor.py, ANTHROPIC_API_KEY) | **Prepare**: Generate ADW ID | Create target_dir | Init logging

### STEP 2: Phase 1 - Strategic Planning
**Purpose**: Create strategic plan with [OPEN_VARIABLES] for creative freedom
**Actions**: Invoke `/agent_plan` → Pass $agent_description → Create spec (Agent name [AGENT_NAME], Purpose, Model gpt-4o/gpt-5, Reasoning [REASONING_ENABLED], Capabilities 3-5)
**Outputs**: $plan, $agent_name, $specifications | **Validation**: Non-empty plan | Name extracted | Spec has purpose/model/capabilities

### STEP 2.5: Infuse Operational Patterns (Agent Architecture)
**Pattern Injection**: Apply proven architectural patterns from operational knowledge base

**Communication Protocol**:
- Agent-to-agent messaging via typed payloads (source_agent, target_agent, message_type, payload, timestamp)
- Message routing: Explicit agent roles (AgentRole enum) + target specification
- Payload structure: Typed dict with validation (BaseModel inheritance recommended)

**Axiom-Driven Behavior**:
- Define agent axioms: Core decision rules as computational constraints
- Axiom alignment scoring: Track adherence via entropy measurement `entropy = -σ p(axiom_i) * log(p(axiom_i))`
- Degradation detection: Monitor entropy increases → trigger grace protocols

**Knowledge Integration**:
- Vector store embedding: Agent knowledge as versículos (semantic units)
- Entropy classification: Tag content (purely-contextual <30, actionable 30-60, theoretical >60)
- Semantic retrieval: Enable agent queries via embeddings (cosine similarity)

**Recovery Mechanisms (Grace Protocol)**:
- Failure states: Define explicit failure modes per agent capability
- Fallback strategies: Primary path → secondary path → graceful degradation
- State preservation: Checkpoint agent state before risky operations
- Recovery triggers: Automatic (entropy threshold) + manual (user/orchestrator intervention)

**E-commerce Optimization** (if domain = e-commerce):
- API integration patterns: Brazilian marketplaces (ML, Shopee, Magalu)
- Data extraction workflows: Product data, reviews, competitor pricing
- Automation hooks: Inventory updates, price adjustments, review responses

**Validation Enhancement**:
- Agent axiom completeness: All decision points mapped to axioms
- Communication protocol compliance: Message structure validated
- Entropy baseline established: Initial agent state entropy < 30
- Recovery paths tested: Grace protocol triggers functional

### STEP 3: Phase 2 - Artifact Construction
**Purpose**: Build artifacts using $plan
**Actions**: Invoke `/agent_build` → Pass $plan → Generate MASTER_INSTRUCTIONS.md (2000-5000 words: personality, workflow, compliance, output format, tools), AGENT_CONFIGURATION.json (model, tools, params), VECTOR_STORE_MANIFEST.md, OUTPUT_SCHEMA.md
**Outputs**: $artifacts, $agent_configuration | **Validation**: 4 core artifacts | MASTER_INSTRUCTIONS 2000-5000 words | Valid JSON | No [PLACEHOLDER]

### STEP 4: Phase 3 - Testing & Validation
**Purpose**: Validate completeness + create test scenarios
**Actions**: Invoke `/agent_test` → Pass $artifacts → Validate (files present, MASTER_INSTRUCTIONS complete, config valid, vector store docs) → Create 3-5 test scenarios (use cases, behaviors, edge cases)
**Outputs**: $test_results, $test_scenarios | **Validation**: All checks passed | ≥3 realistic diverse scenarios

### STEP 5: Phase 4 - Critical Review
**Purpose**: Identify improvements + refinement opportunities
**Actions**: Invoke `/agent_review` → Pass $test_results → Review (completeness, missing elements, improvements, consistency) → Generate notes (strengths, improvements, refinements, quality score 1-10)
**Outputs**: $review_notes, $quality_score, $improvement_suggestions | **Validation**: Comprehensive notes | Score + justification | ≥3 suggestions

### STEP 6: Phase 5 - Documentation Generation
**Purpose**: Create complete docs using all previous context
**Actions**: Invoke `/agent_document` → Pass $all_context → Generate README.md (overview, features, quick start), DEPLOYMENT_GUIDE.md (step-by-step to OpenAI), EXAMPLES.md (test scenarios), META_CONSTRUCTION_LOG.md (all 5 phases, inputs/outputs, decisions, variables, timestamps)
**Outputs**: $documentation, $deployment_ready | **Validation**: All 4 docs | README complete | DEPLOYMENT_GUIDE step-by-step | EXAMPLES ≥3 | LOG has all phases

### STEP 7: Compile Final Output
**Actions**: Collect all artifacts → Organize in $target_dir (8 files: MASTER_INSTRUCTIONS, AGENT_CONFIGURATION, VECTOR_STORE_MANIFEST, OUTPUT_SCHEMA, README, DEPLOYMENT_GUIDE, EXAMPLES, META_CONSTRUCTION_LOG) → Create workflow summary JSON `{adw_id, agent_name, created, phases_completed: 5, quality_score, artifacts_count: 8, ready_for_deployment}` → Return $agent_artifacts

---

## VALIDATION

**Quality Gates** (before returning $agent_artifacts):
- ✅ **Phase Completion**: All 5 phases executed | Verify: Workflow log has all phases | Fix: Re-run failed phase (verbose)
- ✅ **Artifact Completeness**: All 8 files present | Verify: List $target_dir, count=8 | Fix: Re-run relevant phase
- ✅ **MASTER_INSTRUCTIONS Quality**: 2000-5000 words comprehensive | Verify: Word count + sections | Fix: Re-run Phase 2 (expand)
- ✅ **Configuration Validity**: Valid JSON + required fields | Verify: Parse AGENT_CONFIGURATION.json | Fix: Re-run Phase 2 (schema validation)
- ✅ **Documentation Complete**: README, DEPLOYMENT_GUIDE, EXAMPLES present + non-empty | Verify: Check files exist | Fix: Re-run Phase 5
- ✅ **No Placeholders**: No [VARIABLE] or [PLACEHOLDER] remains | Verify: Grep `\[.*\]` | Fix: Re-run phase (fill all)
- ✅ **Traceability**: META_CONSTRUCTION_LOG documents all phases | Verify: Log has 5 sections | Fix: Regenerate from summary

**Quality Score** (1-10): Completeness 30% | Quality 30% | Documentation 20% | Traceability 20% | **Min acceptable: 7.0** | If <7.0: Re-run weakest area

---

## CONTEXT

**Usage**: Execution plans (automated agent creation) | Workflow orchestration scripts | CLI agent builders (/codexa-build_agent) | Meta-construction pipelines

**Upstream**: User provides $agent_description | Prerequisites: Python, uv, ANTHROPIC_API_KEY, meta-constructor script | Optional: $model, $target_dir

**Downstream**: $agent_artifacts → Deploy to OpenAI Agent Builder | $workflow_log → Analysis/improvement of process | $extracted_variables → AGENT_REGISTRY.json

**Argument Chaining**: Typically **first module** in agent creation | Pattern: `[User Input] → meta_build_agent_HOP → $agent_artifacts → [Deploy/Register]`
Example execution plan: `step_1: {hop_module: "91_meta_build_agent_HOP.md", inputs: {$agent_description, $model: "opus"}, outputs: [$agent_artifacts]} → step_2: {depends_on: [step_1], inputs: {$artifacts: $step_1.agent_artifacts}}`

**Assumptions**: Environment (Python 3.10+, uv, ANTHROPIC_API_KEY) | Files (02_agent_meta_constructor.py at builders/, dependencies, executable) | Agent Isolation (self-contained, no external deps beyond OpenAI) | Platform (OpenAI Agent Builder, gpt-4o/gpt-5, Vector Store + Code Interpreter) | User Input ($agent_description sufficient, no additional gathering, accepts automated [OPEN_VARIABLES])

---

## ARTIFACT_OUTPUTS

This HOP generates the following artifacts:

### Primary Artifacts (8 files)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `MASTER_INSTRUCTIONS.md` | Complete agent instructions (2000-5000 words) | `agents/{agent_name}/agent-artifacts/` |
| `AGENT_CONFIGURATION.json` | OpenAI/platform config | `agents/{agent_name}/agent-artifacts/` |
| `VECTOR_STORE_MANIFEST.md` | Knowledge base spec | `agents/{agent_name}/agent-artifacts/` |
| `OUTPUT_SCHEMA.md` | Output format definition | `agents/{agent_name}/agent-artifacts/` |
| `README.md` | Agent documentation | `agents/{agent_name}/` |
| `DEPLOYMENT_GUIDE.md` | Step-by-step deployment | `agents/{agent_name}/agent-artifacts/` |
| `EXAMPLES.md` | Usage examples | `agents/{agent_name}/agent-artifacts/` |
| `META_CONSTRUCTION_LOG.md` | Build traceability | `agents/{agent_name}/agent-artifacts/` |

### Secondary Artifacts (##report)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `{execution_id}_report.md` | Human-readable execution report | `outputs/` |
| `{execution_id}_report.json` | Machine-parsable execution data | `outputs/` |

**Report Generation**:
```python
from artifacts.generators.report_generator import ExecutionReportBuilder, ReportGenerator

# Build report data
report_data = (ExecutionReportBuilder()
    .with_feature_name(agent_name)
    .with_metrics({
        "phases_completed": 5,
        "artifacts_created": 8,
        "quality_score": quality_score
    })
    .with_files({
        "created": created_files,
        "modified": []
    })
    .build())

# Generate report
generator = ReportGenerator()
generator.generate_execution_report(report_data, output_path)
```

---

## FEEDBACK_LOOP

**Pattern**: Execute → Validate → Fix → Repeat (Closing the Loop)

**Implementation**:
```python
def agent_construction_loop(agent_description, max_attempts=3):
    for attempt in range(max_attempts):
        # Execute construction
        artifacts = execute_construction(agent_description)

        # Validate
        validation = validate_artifacts(artifacts)

        if validation.success and validation.score >= 7.0:
            return artifacts

        # Apply feedback for next iteration
        agent_description = refine_description(agent_description, validation.feedback)

    raise Exception(f"Failed after {max_attempts} attempts")
```

**Quality Gates**:
- Phase 1 (Planning): Plan completeness ≥ 90%
- Phase 2 (Build): All 8 artifacts present
- Phase 3 (Test): All test scenarios pass
- Phase 4 (Review): Quality score ≥ 7.0/10
- Phase 5 (Document): No [PLACEHOLDER] remaining

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Related**: 91_codexa_build_agent.md (command) | 02_agent_meta_constructor.py (implementation)

**Changelog v2.0.0**:
- Added PROMPT_LAYER_COMPOSITION section
- Added TASK_BOUNDARY section with mode transitions
- Added SRC_INTEGRATION section with code examples
- Added ARTIFACT_OUTPUTS section with ##report integration
- Added FEEDBACK_LOOP section (Closing the Loop pattern)
- Updated all code examples to use src/ modules
