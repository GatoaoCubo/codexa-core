# 201_ADW_FEATURE_DEVELOPMENT | Complete Feature Development Workflow

**Version**: 2.0.0 | **Created**: 2025-11-24
**Type**: 5-Phase ADW (Two-Phase Planning + Execution + Verification)
**Duration**: 45-90 minutes (depends on feature complexity)
**Pattern**: Planning Agent (read-only) -> Execution Agent (write access)

---

## MODULE_METADATA

```yaml
id: 201_ADW_FEATURE_DEVELOPMENT
version: 2.0.0
category: development-workflows
type: ADW (Agentic Developer Workflow)
execution_mode: two_phase_planning
dependencies:
  - builders/adw_modules/task_boundary.py
  - validators/13_code_quality_validator.py
  - prompts/layers/05_code_conventions.md
status: production_ready
created: 2025-11-24
platform_patterns:
  - Devin: two-phase planning, read-only exploration
  - Claude Code: task boundaries, progress visibility
  - Cursor: code research, high verbosity
  - Antigravity: artifact generation (plan, task, walkthrough)
  - Poke: parallel sub-task execution
  - Windsurf: boundary validation, defensive programming
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "feature_development",
  "workflow_name": "Complete Feature Development Workflow",
  "version": "2.0.0",
  "context_strategy": "two_phase",
  "failure_handling": "stop_and_rollback",

  "agents": {
    "planning_agent": {"access": "read_only", "phase": 1},
    "execution_agent": {"access": "write", "phase": 2},
    "verification_agent": {"access": "read_only", "phase": 3}
  },

  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "feature_development"},
    {"phase_id": "phase_1_research", "phase_name": "Research & Understanding", "agent": "planning_agent", "duration": "10-20min"},
    {"phase_id": "phase_2_planning", "phase_name": "Implementation Planning", "agent": "planning_agent", "duration": "5-10min"},
    {"phase_id": "phase_3_execution", "phase_name": "Feature Implementation", "agent": "execution_agent", "duration": "20-40min"},
    {"phase_id": "phase_4_verification", "phase_name": "Testing & Validation", "agent": "verification_agent", "duration": "5-10min"},
    {"phase_id": "phase_5_documentation", "phase_name": "Artifact Generation", "agent": "execution_agent", "duration": "5-10min"}
  ],

  "artifacts": {
    "implementation_plan": "Required - Generated in Phase 2",
    "task_checklist": "Required - Living document, updated throughout",
    "walkthrough": "Optional - For complex features with screenshots"
  }
}
```

---

## CORE PRINCIPLE: TWO-PHASE PLANNING

### Why Two Phases?

**Phase 1 (Planning Agent - READ ONLY)**:
- Explore codebase without risk of accidental changes
- Build complete mental model before writing code
- Identify patterns, dependencies, potential conflicts
- Devin pattern: "Understand before you act"

**Phase 2 (Execution Agent - WRITE ACCESS)**:
- Execute with confidence after thorough research
- Task boundaries ensure controlled changes
- Progress visible at each step
- Claude Code pattern: "Show what you're doing"

### Agent Boundaries

```yaml
PLANNING_AGENT:
  permissions:
    - read_files: true
    - search_codebase: true
    - analyze_dependencies: true
    - generate_plans: true
    - create_artifacts: true
    - write_files: FALSE  # Critical constraint
    - execute_commands: false
  tools:
    - Glob, Grep, Read
    - WebSearch (for research)
    - AskUserQuestion (for clarification)

EXECUTION_AGENT:
  permissions:
    - read_files: true
    - write_files: true
    - execute_commands: true (with task_boundary)
    - run_tests: true
  tools:
    - All tools
    - TaskBoundary (required for each major operation)
  constraints:
    - Must follow implementation_plan from Phase 2
    - Each file change requires task_boundary declaration
    - Tests must pass before moving to next step

VERIFICATION_AGENT:
  permissions:
    - read_files: true
    - run_tests: true
    - analyze_output: true
    - write_files: FALSE
  tools:
    - Bash (test commands only)
    - Read, Glob, Grep
    - validators/13_code_quality_validator.py
```

---

## PHASE DETAILS

### PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `feature_development`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### PHASE 1: Research & Understanding (Planning Agent)

**Objective**: Build complete mental model of codebase area to modify

**Task Boundary Declaration**:
```
TASK_BOUNDARY: RESEARCH
AGENT: planning_agent
ACCESS: read_only
SCOPE: Understand feature context before any changes
```

**Actions**:
1.1. **Requirement Clarification**
   - Understand feature request completely
   - Use AskUserQuestion for any ambiguity
   - Document acceptance criteria

1.2. **Codebase Exploration**
   - Scan relevant directories (Glob)
   - Search for related patterns (Grep)
   - Read existing implementations (Read)
   - Identify similar features to learn from

1.3. **Dependency Analysis**
   - Map dependencies (imports, calls, data flow)
   - Identify affected files
   - Check for potential conflicts
   - Note integration points

1.4. **Pattern Recognition**
   - Identify existing patterns to follow
   - Note code conventions in use
   - Find reusable components
   - Document anti-patterns to avoid

**Input**: Feature request (user description)
**Output**: `$research_report`
```yaml
$research_report:
  feature_understanding:
    requirements: []
    acceptance_criteria: []
    edge_cases: []
  codebase_context:
    relevant_files: []
    existing_patterns: []
    dependencies: []
  implementation_hints:
    similar_implementations: []
    reusable_components: []
    integration_points: []
  risks_and_concerns:
    potential_conflicts: []
    complexity_areas: []
    unknowns: []
```

**Validation**:
- All requirements documented
- At least 5 relevant files identified
- Dependencies mapped
- No unknowns remaining (or explicitly documented)

---

### PHASE 2: Implementation Planning (Planning Agent)

**Objective**: Create detailed implementation plan (artifact generation)

**Task Boundary Declaration**:
```
TASK_BOUNDARY: PLANNING
AGENT: planning_agent
ACCESS: read_only
SCOPE: Generate implementation plan artifact
```

**Actions**:
2.1. **Architecture Decision**
   - Choose implementation approach
   - Document trade-offs
   - Get user approval if multiple valid approaches

2.2. **Generate Implementation Plan** (ARTIFACT)
   - Following `templates/docs/implementation_plan_template.md`
   - Include all files to create/modify
   - Step-by-step implementation order
   - Test strategy

2.3. **Generate Task Checklist** (ARTIFACT)
   - Following `templates/docs/task_checklist_template.md`
   - Living document format
   - Checkboxes for each step
   - Links to relevant files

2.4. **User Approval Gate**
   - Present plan to user
   - Allow modifications
   - Explicit approval required to proceed

**Input**: `$research_report`
**Output**: `$implementation_plan`, `$task_checklist`

**Implementation Plan Structure**:
```markdown
# Implementation Plan: [Feature Name]

## Overview
[Brief description of what will be built]

## Approach
[Chosen approach and why]

## Files to Modify
1. `path/to/file.py` - [What changes]
2. `path/to/another.ts` - [What changes]

## Files to Create
1. `path/to/new_file.py` - [Purpose]

## Implementation Steps
1. [ ] Step 1: [Description]
2. [ ] Step 2: [Description]
...

## Test Strategy
- Unit tests: [List]
- Integration tests: [List]

## Rollback Plan
[How to undo if needed]
```

**Validation**:
- Plan is complete and actionable
- All files identified
- Test strategy defined
- User approved plan

---

### PHASE 3: Feature Implementation (Execution Agent)

**Objective**: Implement feature following approved plan

**Task Boundary Declaration**:
```
TASK_BOUNDARY: IMPLEMENTATION
AGENT: execution_agent
ACCESS: write
SCOPE: Implement feature per approved plan
PLAN_REFERENCE: $implementation_plan
```

**Actions**:
3.1. **Environment Preparation**
   - Verify clean git state
   - Create feature branch (if applicable)
   - Verify dependencies available

3.2. **Incremental Implementation** (with task boundaries)
   - For each step in `$implementation_plan`:
     ```
     STEP_BOUNDARY: step_N
     FILE: path/to/file
     OPERATION: create|modify|delete
     DESCRIPTION: What this change does
     ```
   - Make change
   - Update `$task_checklist` (mark complete)
   - Run relevant tests
   - Commit if step is complete

3.3. **Code Quality Validation** (per file)
   - Run `validators/13_code_quality_validator.py`
   - Ensure naming conventions followed
   - Verify type annotations present
   - Check docstrings for public functions

3.4. **Integration Verification**
   - Run affected tests after each major change
   - Verify no regressions
   - Check imports resolve correctly

**Input**: `$implementation_plan`, `$task_checklist`
**Output**: `$implementation_results`
```yaml
$implementation_results:
  files_created: []
  files_modified: []
  tests_added: []
  commits: []
  quality_score: float  # from code quality validator
  issues_encountered: []
  deviations_from_plan: []  # if any
```

**Validation**:
- All plan steps completed
- All tests pass
- Code quality score >= 0.85
- No unintended changes
- Task checklist fully checked

---

### PHASE 4: Testing & Validation (Verification Agent)

**Objective**: Comprehensive testing and quality assurance

**Task Boundary Declaration**:
```
TASK_BOUNDARY: VERIFICATION
AGENT: verification_agent
ACCESS: read_only
SCOPE: Validate implementation quality and correctness
```

**Actions**:
4.1. **Test Execution**
   - Run full test suite
   - Run new tests added for feature
   - Run integration tests
   - Check test coverage

4.2. **Code Review Simulation**
   - Verify code follows conventions
   - Check for anti-patterns
   - Verify edge cases handled
   - Check error handling

4.3. **Validator Execution**
   - `validators/13_code_quality_validator.py` (code quality)
   - `validators/07_hop_sync_validator.py` (if HOPs involved)
   - Any domain-specific validators

4.4. **Acceptance Criteria Verification**
   - Check each criterion from Phase 1
   - Document pass/fail for each
   - Identify any gaps

**Input**: `$implementation_results`
**Output**: `$verification_report`
```yaml
$verification_report:
  test_results:
    total_tests: int
    passed: int
    failed: int
    coverage: float
  code_quality:
    score: float
    issues: []
    recommendations: []
  acceptance_criteria:
    - criterion: str
      status: "pass|fail"
      notes: str
  final_verdict: "approved|needs_work|rejected"
  issues_to_fix: []
```

**Validation**:
- All tests pass
- Code quality >= 0.85
- All acceptance criteria met
- No critical issues

**If Issues Found**:
- Return to Phase 3 with specific fix instructions
- Maximum 2 retry loops
- If still failing, escalate to user

---

### PHASE 5: Artifact Generation (Execution Agent)

**Objective**: Generate final documentation artifacts

**Task Boundary Declaration**:
```
TASK_BOUNDARY: DOCUMENTATION
AGENT: execution_agent
ACCESS: write
SCOPE: Generate walkthrough and update documentation
```

**Actions**:
5.1. **Update Task Checklist**
   - Mark all items complete
   - Add completion timestamp
   - Add final notes

5.2. **Generate Walkthrough** (ARTIFACT - optional for complex features)
   - Following `templates/docs/walkthrough_template.md`
   - Step-by-step guide with examples
   - Include usage code snippets
   - Screenshots if UI involved

5.3. **Update Related Documentation**
   - README if needed
   - API documentation
   - Changelog entry

5.4. **Generate ##report**
   - Structured JSON + MD report
   - Include all metrics
   - Include artifacts generated

**Input**: `$verification_report`, `$implementation_results`
**Output**: `$artifacts`, `$final_report`

**Artifacts Generated**:
```
outputs/
  [feature_name]/
    implementation_plan.md  # From Phase 2
    task_checklist.md       # Updated throughout
    walkthrough.md          # Optional, Phase 5
    report.json             # Structured data
    report.md               # Human-readable
```

**Validation**:
- All required artifacts generated
- Documentation consistent with implementation
- Report complete

---

## EXECUTION

### Command Line
```bash
# Full workflow execution
uv run workflows/201_ADW_FEATURE_DEVELOPMENT.py "Add user authentication system"

# With specific options
uv run workflows/201_ADW_FEATURE_DEVELOPMENT.py \
  --feature "Add dark mode toggle" \
  --generate-walkthrough \
  --branch "feature/dark-mode"
```

### Manual Execution (Recommended for Learning)
```bash
# Phase 1: Research (as Planning Agent)
# Use Read, Glob, Grep - NO writes

# Phase 2: Planning
# Generate implementation_plan.md and task_checklist.md

# User approval checkpoint

# Phase 3: Implementation (as Execution Agent)
# Follow plan step-by-step with task boundaries

# Phase 4: Verification
# Run tests, validators

# Phase 5: Documentation
# Generate artifacts
```

---

## SUCCESS CRITERIA

**Workflow Succeeds When**:
- All 5 phases complete
- All tests pass (100% of new tests, no regression)
- Code quality score >= 0.85
- All acceptance criteria met
- All required artifacts generated
- User approved implementation

**Workflow Fails When**:
- Tests fail after 2 retry attempts
- Code quality < 0.75 (cannot improve)
- Critical acceptance criteria unmet
- User rejects implementation

---

## PARALLEL EXECUTION OPPORTUNITIES

**Independent Tasks (can run in parallel)**:
- Multiple file modifications in same step (if no dependencies)
- Test execution across different modules
- Validator execution (all validators can run simultaneously)
- Documentation generation (plan, checklist, walkthrough)

**Sequential Tasks (must run in order)**:
- Research -> Planning (planning needs research)
- Planning -> Implementation (impl needs approved plan)
- Implementation -> Verification (verify needs impl)
- Phase 3 internal: files with dependencies

**Parallelization Pattern**:
```yaml
# From 203_ADW_PARALLEL_ORCHESTRATION
parallel_batch:
  - task_1: "Modify utils/helper.py"
  - task_2: "Modify utils/formatter.py"
  - task_3: "Modify utils/validator.py"
# Wait for all to complete
sequential:
  - task_4: "Modify core/main.py (depends on utils)"
```

---

## ARTIFACT TEMPLATES

### Implementation Plan (Phase 2 output)
See: `templates/docs/implementation_plan_template.md`

### Task Checklist (Living document)
See: `templates/docs/task_checklist_template.md`

### Walkthrough (Phase 5 optional output)
See: `templates/docs/walkthrough_template.md`

---

## TROUBLESHOOTING

**Phase 1 incomplete**: User requirements unclear -> AskUserQuestion | Codebase too large -> Focus on specific area
**Phase 2 plan rejected**: Revise approach based on feedback | Consider alternative patterns
**Phase 3 implementation fails**: Check dependencies | Verify imports | Run specific failing test
**Phase 4 tests fail**: Debug failing test | Check for regressions | Verify test setup
**Quality score low**: Add type annotations | Add docstrings | Fix naming conventions

---

## RELATED WORKFLOWS

- `202_ADW_BUG_FIXING.md` - For fixing bugs (simpler flow)
- `203_ADW_PARALLEL_ORCHESTRATION.md` - For parallel task execution
- `97_ADW_NEW_AGENT_WORKFLOW.md` - For creating new agents
- `100_ADW_DOC_SYNC_WORKFLOW.md` - For documentation updates

---

**Version**: 2.0.0
**Status**: Production-Ready
**Platform Patterns**: Devin (two-phase), Claude Code (boundaries), Cursor (research), Antigravity (artifacts), Poke (parallel)
**Maintainer**: CODEXA Team
