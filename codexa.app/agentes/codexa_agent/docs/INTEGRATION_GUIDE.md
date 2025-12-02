# INTEGRATION_GUIDE | CODEXA v2.0 Features Usage

**Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Guide for using all CODEXA v2.0 features
**Audience**: Developers, AI assistants, system integrators

---

## QUICK START

### Choose Your Workflow

| Task | Recommended ADW | Duration |
|------|-----------------|----------|
| New feature | 201_ADW_FEATURE_DEVELOPMENT | 45-90min |
| Bug fix | 202_ADW_BUG_FIXING | 15-45min |
| Multiple tasks | 203_ADW_PARALLEL_ORCHESTRATION | Varies |
| New agent | 97_ADW_NEW_AGENT_WORKFLOW | 20-40min |
| Code cleanup | 98_ADW_CONSOLIDATION_WORKFLOW | 15-30min |
| System upgrade | 99_ADW_SYSTEM_UPGRADE_WORKFLOW | 30-60min |
| Doc sync | 100_ADW_DOC_SYNC_WORKFLOW | 10-30min |

---

## 1. TWO-PHASE PLANNING

### Concept

Split development into distinct phases with different capabilities:

```
Phase 1: Planning Agent (READ-ONLY)
├── Explore codebase
├── Understand patterns
├── Generate implementation plan
└── NO write operations

Phase 2: Execution Agent (WRITE)
├── Follow approved plan
├── Task boundaries per operation
├── Incremental commits
└── Quality validation
```

### Usage

**For Feature Development**:
```bash
# Start feature development workflow
uv run workflows/201_ADW_FEATURE_DEVELOPMENT.py "Add user authentication"

# Or manually:
# Phase 1: Research (read-only)
# - Use Read, Glob, Grep to explore
# - Generate implementation_plan.md
# - Get user approval

# Phase 2: Implementation (write)
# - Follow plan step-by-step
# - Declare task boundaries
# - Validate quality
```

**For Bug Fixing**:
```bash
# Systematic bug fixing
uv run workflows/202_ADW_BUG_FIXING.py --issue "#123" "Login fails with special chars"
```

### Implementation Plan Artifact

Generated in Phase 2 of planning:

```markdown
# Implementation Plan: [Feature Name]

## Overview
Brief description of what will be built

## Approach
Chosen approach and trade-offs

## Files to Modify
1. `path/to/file.py` - What changes

## Files to Create
1. `path/to/new.py` - Purpose

## Implementation Steps
1. [ ] Step 1: Description
2. [ ] Step 2: Description

## Test Strategy
- Unit tests: List
- Integration tests: List

## Rollback Plan
How to undo if needed
```

---

## 2. TASK BOUNDARIES

### Concept

Every write operation declares its scope explicitly:

```yaml
TASK_BOUNDARY: descriptive_name
AGENT: planning_agent | execution_agent | verification_agent
ACCESS: read_only | write
SCOPE: What this operation does
FILES: List of files affected
ROLLBACK: How to undo
```

### Usage

**In ADW Execution**:
```python
# Before any write operation
print("""
TASK_BOUNDARY: UPDATE_AUTH_MODULE
AGENT: execution_agent
ACCESS: write
SCOPE: Add JWT token validation
FILES: src/auth/validator.py
ROLLBACK: git revert HEAD
""")

# Perform operation
edit_file("src/auth/validator.py", changes)

# After operation
print("TASK_BOUNDARY_COMPLETE: UPDATE_AUTH_MODULE")
```

**In Builders**:
```python
from builders.adw_modules.task_boundary import TaskBoundary

with TaskBoundary("CREATE_AGENT", "execution_agent", ["agentes/new_agent/"]) as tb:
    # All operations within this boundary
    create_agent_files()
    tb.add_artifact("MASTER_INSTRUCTIONS.md")
# Boundary auto-closes with completion status
```

### Benefits

1. **Visibility**: Know exactly what's happening
2. **Rollback**: Clear undo points
3. **Audit**: Full trace of operations
4. **Safety**: Controlled write access

---

## 3. PARALLEL ORCHESTRATION

### Concept

Execute independent tasks simultaneously with multiple agents:

```
Task Decomposition → Dependency Analysis → Batch Formation → Parallel Execution → Aggregation
```

### Usage

**Basic Parallel Execution**:
```bash
# Execute multiple bug fixes in parallel
uv run workflows/203_ADW_PARALLEL_ORCHESTRATION.py \
  --workflow 202_ADW_BUG_FIXING \
  --tasks "bug1.yaml,bug2.yaml,bug3.yaml" \
  --max-parallel 3
```

**Custom Task Batching**:
```yaml
# tasks.yaml
orchestration:
  tasks:
    - id: task_1
      file: "src/utils/helper.py"
      operation: "add_logging"
    - id: task_2
      file: "src/utils/format.py"
      operation: "add_logging"
    - id: task_3
      file: "src/core/main.py"
      depends_on: ["task_1", "task_2"]
      operation: "integrate_logging"

  batches:
    - parallel: [task_1, task_2]  # Run simultaneously
    - sequential: [task_3]        # After dependencies complete
```

### Dependency Graph

```
Independent tasks (Batch 1 - parallel)
├── task_1: utils/helper.py
├── task_2: utils/format.py
└── task_3: utils/validate.py

Dependent task (Batch 2 - after Batch 1)
└── task_4: core/main.py (depends on 1,2,3)

Final task (Batch 3 - after Batch 2)
└── task_5: tests/test_main.py
```

### Conflict Resolution

```yaml
conflict_strategies:
  same_file:
    strategy: "sequential_within_batch"
    action: "Remove from parallel batch, execute in order"

  dependency:
    strategy: "dependency_order"
    action: "Later batch for dependent task"

  semantic:
    strategy: "human_review"
    action: "Flag for manual merge decision"
```

---

## 4. ARTIFACT GENERATION

### Types

| Artifact | Purpose | Generated By |
|----------|---------|--------------|
| `implementation_plan.md` | Strategic plan | Phase 2 of planning |
| `task_checklist.md` | Living progress tracker | Throughout execution |
| `walkthrough.md` | Step-by-step guide | Phase 5 (optional) |
| `##report` | Structured results | All builders/validators |

### Task Checklist (Living Document)

```markdown
# Task Checklist: Add Authentication

## Status: In Progress
Last Updated: 2025-11-24 10:30:00

## Tasks
- [x] Research existing auth patterns
- [x] Create implementation plan
- [ ] **IN PROGRESS** Add JWT validation
- [ ] Add middleware
- [ ] Add tests
- [ ] Update documentation

## Notes
- Found existing token utils in src/utils/token.py
- Using HS256 algorithm for JWT
```

### ##report Standard

All builders and validators generate structured reports:

```yaml
##report:
  module: "builder_name"
  version: "2.0.0"
  timestamp: "2025-11-24T10:30:00Z"
  status: "success|warning|error"
  metrics:
    files_processed: 10
    issues_found: 2
    quality_score: 0.92
  details:
    - category: "naming"
      count: 1
      severity: "warning"
  artifacts:
    - "path/to/artifact.md"
```

---

## 5. CODE QUALITY VALIDATION

### Usage

```bash
# Validate single file
python validators/13_code_quality_validator.py src/auth/validator.py

# Validate directory
python validators/13_code_quality_validator.py src/

# With report output
python validators/13_code_quality_validator.py src/ --output reports/
```

### What It Checks

| Check | Python | TypeScript | Weight |
|-------|--------|------------|--------|
| Type annotations | `def foo(x: int) -> str` | `function foo(x: number): string` | 25% |
| Docstrings | Required for public | JSDoc for exports | 20% |
| Naming conventions | snake_case / PascalCase | camelCase / PascalCase | - |
| Function length | Max 50 lines | Max 50 lines | 10% |
| File length | Max 600 lines | Max 600 lines | - |
| No errors | Critical issues | Critical issues | 30% |
| No warnings | Style issues | Style issues | 15% |

### Quality Score Calculation

```python
score = (
    type_coverage * 0.25 +      # % of typed parameters/returns
    docstring_coverage * 0.20 + # % of documented public functions
    (1 - error_rate) * 0.30 +   # Inverse of error count
    (1 - warning_rate) * 0.15 + # Inverse of warning count
    structure_compliance * 0.10  # Line limits respected
)
# Passing threshold: >= 0.85
```

---

## 6. PROMPT LAYER COMPOSITION

### Available Layers

| Layer | File | Purpose |
|-------|------|---------|
| 01 | `01_identity_layer.md` | Agent identity definition |
| 02 | `02_operating_modes.md` | Planning/Execution/Verification modes |
| 03 | `03_tool_usage_layer.md` | Tool definitions and usage |
| 04 | `04_memory_context.md` | Context management patterns |
| 05 | `05_code_conventions.md` | Code style guide |
| 06 | `06_design_system.md` | UI design tokens |
| 07 | `07_steering_hooks.md` | Behavior modification hooks |
| 08 | `08_workflows.md` | ADW workflow patterns |

### Composing Prompts

```python
from src.runtime import PromptLoader

loader = PromptLoader()

# For code generation agent
code_agent_prompt = loader.compose([
    "01_identity_layer",
    "03_tool_usage_layer",
    "05_code_conventions",
])

# For UI generation agent
ui_agent_prompt = loader.compose([
    "01_identity_layer",
    "03_tool_usage_layer",
    "05_code_conventions",
    "06_design_system",
])

# For planning agent
planning_prompt = loader.compose([
    "01_identity_layer",
    "02_operating_modes",  # Set to PLANNING
    "03_tool_usage_layer",
])
```

### Layer Configuration

```yaml
# config/prompt_layers.yml
compositions:
  code_agent:
    layers: [01, 03, 05]
    mode: execution

  ui_agent:
    layers: [01, 03, 05, 06]
    mode: execution

  planning_agent:
    layers: [01, 02, 03]
    mode: planning
    constraints:
      write_access: false
```

---

## 7. DESIGN SYSTEM INTEGRATION

### Using Design Tokens

```css
/* From prompts/layers/06_design_system.md */

/* Colors - Semantic, not literal */
--color-primary: hsl(221, 83%, 53%);
--color-background: hsl(0, 0%, 100%);
--color-text: hsl(222, 47%, 11%);
--color-error: hsl(0, 72%, 51%);
--color-success: hsl(142, 71%, 45%);

/* Spacing - 8px base */
--space-1: 4px;
--space-2: 8px;
--space-4: 16px;
--space-8: 32px;

/* Typography */
--text-base: 16px;
--text-lg: 18px;
--font-sans: 'Inter', system-ui, sans-serif;
```

### Component Patterns

```jsx
// Button following design system
<button className="
  bg-[hsl(var(--color-primary))]
  text-[hsl(var(--color-background))]
  px-[var(--space-4)]
  py-[var(--space-2)]
  rounded-[var(--radius-md)]
  text-[var(--text-base)]
">
  Primary Button
</button>
```

---

## 8. WORKFLOW CHAINING

### Sequential Workflows

```bash
# Create agent → Sync docs → Validate
uv run workflows/97_ADW_NEW_AGENT_WORKFLOW.py "Sentiment agent"
uv run workflows/100_ADW_DOC_SYNC_WORKFLOW.py --agents sentiment_agent
uv run validators/09_readme_validator.py agentes/sentiment_agent/README.md
```

### Integrated Workflows

```yaml
# workflow_chain.yaml
chain:
  - workflow: 201_ADW_FEATURE_DEVELOPMENT
    args:
      feature: "Add sentiment analysis"
    on_success: continue
    on_failure: stop

  - workflow: 100_ADW_DOC_SYNC
    args:
      target: "affected_agents"
    on_success: continue

  - workflow: 99_ADW_SYSTEM_UPGRADE
    args:
      scope: "validators"
      type: "patch"
```

---

## 9. MULTI-AGENT COORDINATION

### Agent Types

| Agent | Access | Purpose |
|-------|--------|---------|
| Planning Agent | read_only | Research, analysis, planning |
| Execution Agent | write | Implementation, changes |
| Verification Agent | read_only + tests | Testing, validation |
| Orchestrator | coordination | Multi-agent management |

### Coordination Pattern

```yaml
orchestration:
  agents:
    - id: planner
      type: planning_agent
      phase: 1
      output: implementation_plan

    - id: executor
      type: execution_agent
      phase: 2
      input: implementation_plan
      output: changes

    - id: verifier
      type: verification_agent
      phase: 3
      input: changes
      output: verification_report

  sync_points:
    - after: planner
      gate: user_approval
    - after: executor
      gate: tests_pass
```

---

## 10. VALIDATION PIPELINE

### Running All Validators

```bash
# Full validation suite
python validators/07_hop_sync_validator.py prompts/*.md
python validators/09_readme_validator.py README.md
python validators/10_taxonomy_validator.py
python validators/12_doc_sync_validator.py --all
python validators/13_code_quality_validator.py src/
```

### Validator Integration in ADWs

```yaml
# In any ADW, Phase 4 (Verification)
verification:
  validators:
    - name: code_quality
      path: validators/13_code_quality_validator.py
      threshold: 0.85
      on_failure: retry_once

    - name: hop_sync
      path: validators/07_hop_sync_validator.py
      on_failure: report_warning

    - name: doc_sync
      path: validators/12_doc_sync_validator.py
      on_failure: auto_fix
```

---

## COMMON PATTERNS

### Pattern 1: Feature with Tests

```bash
# 1. Plan feature
# Phase 1: Research existing code
# Phase 2: Generate implementation_plan.md

# 2. Implement
# Phase 3: Code with task boundaries

# 3. Test
# Phase 4: Run validators + tests

# 4. Document
# Phase 5: Generate walkthrough
```

### Pattern 2: Bug Fix

```bash
# 1. Reproduce
# Create failing test

# 2. Analyze
# Find root cause (not symptom)

# 3. Fix
# Minimal change only

# 4. Verify
# Test passes, no regressions

# 5. Document
# Commit with issue reference
```

### Pattern 3: Parallel Refactoring

```bash
# 1. Identify independent files
# 2. Create parallel batches
# 3. Execute changes simultaneously
# 4. Aggregate results
# 5. Run integration tests
```

---

## TROUBLESHOOTING

### Two-Phase Planning Issues

| Issue | Solution |
|-------|----------|
| Planning takes too long | Focus scope, set time limits |
| Plan rejected | Revise approach, ask for feedback |
| Execution diverges from plan | Update plan, document deviation |

### Parallel Execution Issues

| Issue | Solution |
|-------|----------|
| Conflicts detected | Move to sequential batch |
| Task fails | Isolate, continue others, retry |
| Results don't merge | Use conflict resolution strategy |

### Quality Validation Issues

| Issue | Solution |
|-------|----------|
| Score too low | Add types, docstrings |
| False positives | Check validator config |
| Slow validation | Run on changed files only |

---

**Version**: 1.0.0
**Status**: Complete Reference
**Related**: PLATFORM_ANALYSIS.md, MIGRATION_GUIDE.md, BEST_PRACTICES.md
**Maintainer**: CODEXA Team
