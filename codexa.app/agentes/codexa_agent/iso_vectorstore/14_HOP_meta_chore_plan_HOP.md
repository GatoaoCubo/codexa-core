<!-- iso_vectorstore -->
<!--
  Source: 92_meta_chore_plan_HOP.md
  Agent: codexa_agent
  Synced: 2025-12-02
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 92_meta_chore_plan_HOP | Chore Planning & Task Specification

**ID**: meta_chore_plan_HOP | **Version**: 2.0.0 | **Created**: 2025-11-24 | **Updated**: 2025-11-24
**Purpose**: Generate detailed task plans following CODEXA chore planning standards
**Dependencies**: None | **Category**: planner | **Framework**: TAC-7
**Usage**: Task planning | Chore specifications | Routine work orchestration

---

## PROMPT_LAYER_COMPOSITION

This HOP composes the following prompt layers for planning tasks:

| Layer | Purpose | Usage in HOP |
|-------|---------|--------------|
| `01_identity_layer.md` | Agent identity & role | Defines planner personality |
| `02_operating_modes.md` | 7 operating modes | Uses PLANNING mode exclusively (READ_ONLY) |
| `03_tool_usage_layer.md` | Tool definitions | References Glob, Grep, Read for discovery |
| `08_workflows.md` | Workflow patterns | Two-phase planning (Devin pattern) |

**Composition Type**: `PLANNING_AGENT` (Identity + Modes + Tools + Communication)

**Runtime Composition**:
```python
from src.runtime import PromptLoader, CompositionType

loader = PromptLoader()
base_prompt = loader.load_composition(CompositionType.PLANNING_AGENT)
hop_prompt = loader.load_hop("92_meta_chore_plan_HOP")
full_prompt = base_prompt + "\n\n" + hop_prompt
```

---

## TASK_BOUNDARY

**Mode**: PLANNING (READ_ONLY - no file writes)

**Mode Transitions**:
```
IDLE → PLANNING (on chore description received)
PLANNING → RESEARCH (if codebase exploration needed)
RESEARCH → PLANNING (when files discovered)
PLANNING → IDLE (plan generated, await execution approval)
```

**Constraints**:
- READ_ONLY throughout entire workflow (no file modifications)
- Output is the PLAN, not the execution
- Requires explicit handoff to EXECUTION mode for implementation

**Progress Communication**:
```python
from builders.task_boundary import TaskBoundary, AgentMode

boundary = TaskBoundary(mode=AgentMode.PLANNING, workflow_name="Chore Planning")
boundary.add_task("Parse requirements", "Parsing requirements", estimated_min=2)
boundary.add_task("Discover files", "Discovering relevant files", estimated_min=5)
boundary.add_task("Plan steps", "Planning step-by-step tasks", estimated_min=10)
boundary.add_task("Define validation", "Defining validation commands", estimated_min=3)
boundary.add_task("Generate plan", "Generating plan file", estimated_min=2)
```

---

## SRC_INTEGRATION

This HOP integrates with the following `src/` modules:

**Tool Execution** (`src/tools/`):
```python
from src import ToolExecutor, FileTools

executor = ToolExecutor()

# Discovery phase - READ_ONLY tools
files = await FileTools.glob("agentes/*/README.md")
content = await FileTools.read("README.md")
matches = await FileTools.grep("deployment", "agentes/")
```

**Runtime** (`src/runtime/`):
```python
from src import AgentRuntime, AgentConfig, PromptLoader

loader = PromptLoader()
prompt = loader.load_hop("92_meta_chore_plan_HOP")

config = AgentConfig(
    agent_id="chore-planner",
    system_prompt=prompt,
    llm_provider=provider,
    permission=Permission(level=PermissionLevel.READ_ONLY)  # No writes
)
runtime = AgentRuntime(config=config)
```

---

## INPUT_CONTRACT

### Required
- **$chore_description** (string) - Clear description of task/chore to be completed | Format: NL (what needs to be done, why, scope) | Validation: Non-empty, 20-500 chars, actionable task | Ex: `"Update all agent READMEs to include new deployment section for Claude Code CLI"`

### Optional
- **$relevant_files** (array) - Pre-identified files relevant to chore | Default: [] (discover automatically) | Validation: Valid paths exist | Ex: `["agentes/*/README.md"]`
- **$validation_commands** (array) - Pre-specified validation commands | Default: [] (auto-generate) | Validation: Executable commands | Ex: `["pytest", "npm test"]`
- **$output_file** (string) - Where to save plan | Default: "specs/chore_{timestamp}.md" | Validation: Valid writable path | Ex: "specs/update_readmes_20251124.md"

---

## OUTPUT_CONTRACT

### Primary
- **$chore_plan** (object) - Complete chore plan ready for execution
  - Format: Markdown file (specs/*.md)
  - Structure: `{chore_name, description, relevant_files: [{file, why_relevant}], step_by_step_tasks: [{step_number, task_title, actions: [], why_needed}], validation_commands: [{command, expected_output, success_criteria}], notes: [edge_cases, warnings]}`
  - Validation: All sections present | ≥3 step-by-step tasks | ≥2 validation commands | All files exist or marked [NEW] | Clear success criteria

### Secondary
- **$discovered_files** (array) - Files discovered during research | Structure: `[{path, relevance_score, reason}]`
- **$estimated_effort** (object) - Effort estimation | Structure: `{complexity: "low|medium|high", estimated_time: "minutes|hours", risk_level: "low|medium|high"}`

---

## TASK

**Role**: Chore Planning Module (CODEXA system)

**Objective**: Create detailed, executable task plan for routine chores/maintenance work that agents can follow systematically

**Quality Standards**: Thorough but simple | Precise file references | Clear actionable steps | Comprehensive validation | No ambiguity | All edge cases addressed

**Constraints**: Use discovery-first (research codebase before planning) | Focus on relevant files only | Must include validation commands | Plans must be executable without clarification | Respect existing architecture | No breaking changes unless explicitly required

**Input**: $chore_description + optional ($relevant_files, $validation_commands, $output_file)
**Output**: $chore_plan (complete specs/*.md file)

---

## STEPS

### STEP 1: Understand Chore Requirements
**Verify**: $chore_description clear and actionable | Prerequisites identified | Scope well-defined | Success criteria implicit or explicit
**Actions**: Parse description → Identify key verbs (update, add, fix, refactor) → Extract scope boundaries → Identify affected components → List prerequisites
**Output**: Chore understanding summary

### STEP 2: Discovery - Find Relevant Files
**Purpose**: Research codebase to identify all files that need changes
**Actions**:
- Read README.md from root (understand structure)
- If $relevant_files provided → Validate paths exist
- Else → Search codebase:
  - Glob patterns for file types (e.g., `**/*README.md` if updating READMEs)
  - Grep for keywords related to chore (e.g., search "deployment" if adding deployment docs)
  - Identify config files that may need updates
  - Find related tests/validators
- Analyze each file → Assess relevance (score 1-10) → Document why relevant
**Tools**: Glob, Grep, Read (selective)
**Output**: $discovered_files (sorted by relevance desc)
**Validation**: ≥1 relevant file found | All high-relevance files (≥7) included | No obviously missing files

### STEP 3: Plan Step-by-Step Tasks
**Purpose**: Break chore into ordered, actionable steps
**Actions**:
- Order tasks logically (dependencies first)
- For each step:
  - **H3 Header**: Clear task title (verb + object)
  - **Bullets**: Specific actions with file references
  - **Why**: Explain purpose/reasoning
  - **Risk**: Note potential issues
- Include setup steps if needed (backups, branch creation)
- Include cleanup steps (remove temp files, update indexes)
**Format**:
```markdown
### Step 1: Backup Existing Files
- Create `.bak` copies of all files to be modified
- Store in `backup_{timestamp}/` directory
- Verify backup integrity
**Why**: Safety net for rollback if issues occur
**Risk**: None (read-only operation)

### Step 2: Update README.md Files
- Read `agentes/*/README.md` (5 agents)
- Add new "Deployment" section after "Usage" section
- Follow template from `templates/docs/README_TEMPLATE.md`
- Preserve existing content
**Why**: Standardize deployment docs across all agents
**Risk**: May conflict with agent-specific content - preserve unique sections
```
**Output**: Ordered list of 3-10 steps (H3 headers + bullets)
**Validation**: Steps are ordered correctly | Each step has clear actions | File paths specific | No circular dependencies

### STEP 4: Define Validation Commands
**Purpose**: Specify how to validate chore completion with zero regressions
**Actions**:
- Identify validation types needed:
  - **Tests**: Unit tests, integration tests, e2e tests
  - **Linters**: Code style, format checkers
  - **Validators**: Custom validators (e.g., `validators/09_readme_validator.py`)
  - **Build**: Compilation, bundling
  - **Manual**: Visual checks, deployment verification
- For each command:
  - **Command**: Exact command to run (with working directory if needed)
  - **Expected**: What success looks like
  - **Success Criteria**: How to interpret results
**Format**:
```markdown
## Validation Commands
Execute all commands to validate that the chore is complete with zero regressions.

- `cd agentes/codexa-agent && python validators/09_readme_validator.py README.md` – Validate README structure and completeness (exit code 0)
- `git diff --check` – Ensure no trailing whitespace or merge conflicts (no output = success)
- `grep -r "FIXME\|TODO" agentes/*/README.md` – No new TODO markers added (empty output = success)
- **Manual**: Open each README.md in browser/viewer, verify new "Deployment" section renders correctly
```
**Output**: List of ≥2 validation commands
**Validation**: Commands are executable | Success criteria clear | Covers regressions | Includes manual steps if automation insufficient

### STEP 5: Document Notes & Edge Cases
**Purpose**: Capture warnings, edge cases, assumptions for task executor
**Actions**:
- List edge cases (unusual scenarios)
- Document warnings (potential pitfalls)
- Note assumptions (prerequisites, environment)
- Suggest improvements (optional enhancements)
**Format**:
```markdown
## Notes
- **Edge Case**: Some agents may have custom README structures - preserve unique sections
- **Warning**: Don't overwrite agent-specific deployment instructions if they exist
- **Assumption**: All agents follow standard directory structure (`agentes/*_agent/`)
- **Improvement**: Consider creating README linter to catch inconsistencies early
```
**Output**: ≥2 notes/warnings
**Validation**: Covers non-obvious scenarios | Helpful for executor

### STEP 6: Generate Plan File
**Purpose**: Write complete plan to specs/*.md
**Actions**:
- Use Plan Format (see below)
- Replace all [PLACEHOLDERS] with actual content
- Save to $output_file or auto-generated path
- Validate structure (all sections present)
**Output**: $chore_plan (file path + content)
**Validation**: File created | All sections filled | No [PLACEHOLDERS] remaining | Valid markdown

### STEP 7: Return $arguments for Next Phase
**Actions**: Prepare variables for execution phase:
- $plan_file_path: Where plan was saved
- $relevant_files: List of files to modify
- $validation_commands: Commands to run after execution
- $estimated_effort: Complexity assessment
**Output**: $arguments object for downstream consumption

---

## PLAN FORMAT (Template)

```markdown
# Chore: <chore_name>

**Created**: <timestamp>
**Estimated Effort**: <low|medium|high> (<time estimate>)
**Risk Level**: <low|medium|high>

## Descrição da Tarefa
<Descreva a tarefa em detalhes - o quê, por quê, escopo>

## Arquivos Relevantes
Use estes arquivos para resolver a tarefa:

<Para cada arquivo:>
- **`<file_path>`** - <Por que este arquivo é relevante>

<Se há novos arquivos a criar:>
- **`<file_path>`** [NEW] - <Propósito do novo arquivo>

## Passos Detalhados (Step by Step Tasks)
**IMPORTANTE**: Execute cada passo em ordem, de cima para baixo.

### Step 1: <Task Title>
- <Action 1 with file references>
- <Action 2 with file references>
- <Action N>

**Why**: <Explain purpose>
**Risk**: <Note potential issues or "None">

### Step 2: <Task Title>
...

### Step N: <Final Task Title>
...

## Comandos de Validação (Validation Commands)
Execute todos os comandos para validar que a tarefa está completa com zero regressões.

- `<command>` – <Expected output and success criteria>
- `<command>` – <Expected output and success criteria>
- **Manual**: <Manual verification steps>

## Notas
<Liste quaisquer notas adicionais, edge cases, warnings, ou assumptions>

- **Edge Case**: <Scenario>
- **Warning**: <Pitfall to avoid>
- **Assumption**: <Prerequisite>
- **Improvement**: <Optional enhancement>

---

**Plan Generated**: <timestamp>
**Ready for Execution**: ✅
```

---

## VALIDATION

**Quality Gates** (before returning $chore_plan):
- ✅ **Chore Description Clear**: Unambiguous task with clear success criteria | Verify: Re-read description, can executor understand? | Fix: Expand description with examples
- ✅ **Relevant Files Identified**: All necessary files discovered | Verify: Glob/Grep coverage complete | Fix: Research deeper, check related modules
- ✅ **Steps Actionable**: Each step has concrete actions | Verify: No vague instructions ("fix the bug" ❌, "Update line 42 in file.py to use new API" ✅) | Fix: Make specific with file:line references
- ✅ **Validation Complete**: ≥2 commands that prove completion | Verify: Commands actually test the work | Fix: Add test/lint/validator commands
- ✅ **No Ambiguity**: Zero interpretation needed | Verify: Ask "could agent execute without clarification?" | Fix: Add details, examples, file paths
- ✅ **Edge Cases Covered**: Notes address non-obvious scenarios | Verify: Think "what could go wrong?" | Fix: Document warnings
- ✅ **Follows Template**: All sections present and filled | Verify: Check Plan Format structure | Fix: Add missing sections

**Quality Score** (1-10): Completeness 30% | Clarity 30% | Actionability 20% | Validation 20% | **Min acceptable: 8.0** | If <8.0: Identify weak dimension → Expand that section

---

## CONTEXT

**Usage**: Chore planning (routine tasks) | Maintenance work | Refactoring | Documentation updates | Configuration changes | Simple bug fixes (non-research-heavy)

**Upstream**: User provides $chore_description | Optional: User provides $relevant_files (if already known) | Prerequisites: Codebase accessible, README.md exists

**Downstream**: $chore_plan → Execute phase (human or agent) | $validation_commands → Testing phase | $relevant_files → Change scope tracking

**Argument Chaining**: Typically **first module** in task execution | Pattern: `[User Input] → meta_chore_plan_HOP → $chore_plan → [Execute/Build] → $artifacts → [Validate]`
Example execution: `step_1: {hop_module: "92_meta_chore_plan_HOP.md", inputs: {$chore_description}, outputs: [$chore_plan]} → step_2: {depends_on: [step_1], inputs: {$plan: $step_1.chore_plan}, execute_tasks: true}`

**Assumptions**:
- Codebase structure documented (README.md available)
- Standard tools available (Glob, Grep, Read)
- Validation tools present (linters, tests, validators)
- Task is routine (not exploratory research)
- Success criteria can be defined upfront (not discovered through iteration)

---

## ARTIFACT_OUTPUTS

This HOP generates the following artifacts:

### Primary Artifacts (Plan Files)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `chore_{timestamp}.md` | Complete chore plan | `specs/` |
| `$discovered_files` | Files identified for modification | In-memory / returned |
| `$estimated_effort` | Complexity assessment | In-memory / returned |

### Secondary Artifacts (##report)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `{execution_id}_report.md` | Human-readable planning report | `outputs/` |
| `{execution_id}_report.json` | Machine-parsable planning data | `outputs/` |

**Report Generation**:
```python
from validators.report_generator import ValidatorReportGenerator

# After plan generation
reporter = ValidatorReportGenerator("chore_plan_generator", "2.0.0")

if quality_score >= 8.0:
    report = reporter.generate(
        target=chore_description,
        passed=1,
        failed=0,
        warnings=len(edge_cases),
        output_dir=Path("outputs")
    )
```

---

## FEEDBACK_LOOP

**Pattern**: Plan → Review → Refine → Approve (Two-Phase Planning)

**Implementation**:
```python
def two_phase_planning(chore_description, max_refinements=2):
    # Phase 1: Generate initial plan
    plan = generate_plan(chore_description)

    for refinement in range(max_refinements):
        # Review plan
        review = review_plan(plan)

        if review.quality_score >= 8.0 and review.actionability >= 90:
            return plan

        # Refine weak areas
        plan = refine_plan(plan, review.feedback)

    # Final approval gate
    if plan.quality_score < 7.0:
        raise Exception("Plan quality insufficient after refinements")

    return plan
```

**Quality Gates (Before Handoff to Execution)**:
- Quality Score ≥ 8.0/10 (Completeness + Clarity + Actionability + Validation)
- All file paths verified (exist or marked [NEW])
- Validation commands executable
- No ambiguous steps
- Edge cases documented

**Two-Phase Pattern** (Devin-style):
1. **Planning Phase**: READ_ONLY exploration, no file writes
2. **Approval Gate**: User reviews plan before execution
3. **Execution Phase**: Separate agent with WRITE access

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Related**: 91_meta_build_agent_HOP.md (agent building) | 94_meta_build_prompt_HOP.md (prompt creation)

**Changelog v2.0.0**:
- Added PROMPT_LAYER_COMPOSITION section
- Added TASK_BOUNDARY section with READ_ONLY mode
- Added SRC_INTEGRATION section with code examples
- Added ARTIFACT_OUTPUTS section with ##report integration
- Added FEEDBACK_LOOP section (Two-Phase Planning pattern)
- Updated all code examples to use src/ modules
