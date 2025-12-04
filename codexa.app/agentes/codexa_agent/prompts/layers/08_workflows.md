# 08_workflows | CODEXA Workflow Patterns & Recipes

## MODULE_METADATA

```yaml
id: 08_workflows
version: 1.0.0
category: orchestration
type: composable_layer
```

## PURPOSE

Define common workflow patterns, recipes, and orchestration strategies.

---

**Layer Version**: 1.0.0 | **Created**: 2025-11-24
**Category**: Orchestration Layer | **Composable**: Yes
**Integration**: Multi-agent workflows, ADWs, complex task orchestration

---

## OVERVIEW

CODEXA workflows are **composable patterns** for accomplishing complex multi-step tasks. This layer catalogs proven workflows synthesized from 30+ platforms.

**Core Concepts**:
- **Workflow**: Sequence of phases with clear inputs/outputs
- **Recipe**: Reusable workflow template for common tasks
- **Orchestration**: Coordination of multiple agents/phases
- **$arguments Chaining**: Output from phase N → Input to phase N+1

---

## FOUNDATIONAL WORKFLOWS

### Workflow 1: Two-Phase Planning (Devin Pattern)

**When to Use**: Complex tasks requiring codebase discovery before implementation

**Phases**:
1. **Planning Mode** (Read-only)
   - Input: User request
   - Agent: Planning agent with read-only access
   - Output: `implementation_plan.md`, `task.md`, `affected_files.json`

2. **Execution Mode** (Write access)
   - Input: Planning output ($implementation_plan, $task_checklist)
   - Agent: Execution agent with write access
   - Output: Modified files, new files, tests

**Flow**:
```yaml
workflow: "two_phase_planning"
phases:
  - phase: 1
    name: "Planning"
    mode: "PLANNING"
    agent_preset: "planning"
    actions:
      - Discover codebase structure
      - Analyze affected files
      - Design implementation approach
      - Generate task checklist
    outputs:
      $implementation_plan: "agents/{adw_id}/implementation_plan.md"
      $task_checklist: "agents/{adw_id}/task.md"
      $affected_files: "agents/{adw_id}/affected_files.json"

  - phase: 2
    name: "Execution"
    mode: "EXECUTION"
    agent_preset: "execution"
    inputs:
      $plan_file: "$phase1.implementation_plan"
      $tasks: "$phase1.task_checklist"
      $files: "$phase1.affected_files"
    actions:
      - Implement according to plan
      - Create tests
      - Update documentation
    outputs:
      $modified_files: ["list", "of", "files"]
      $tests_created: ["test", "files"]
```

**Example**:
```
User: "Add user authentication to the application"

Phase 1 (Planning):
  - Discover: Next.js project, no existing auth
  - Design: Use NextAuth.js, add database models, create login/signup pages
  - Plan: 12-step implementation plan
  - Output: implementation_plan.md, task.md

Phase 2 (Execution):
  - Execute: Implement all 12 tasks from plan
  - Output: 8 new files, 4 modified files, 6 test files

Result: Complete authentication system implemented
```

---

### Workflow 2: Artifact-Based Development (Antigravity Pattern)

**When to Use**: Feature development requiring documentation trail

**Artifacts** (3 living documents):
1. **`implementation_plan.md`**: What to build + how
2. **`task.md`**: Checklist of todos (updated in real-time)
3. **`walkthrough.md`**: Verification with screenshots

**Flow**:
```yaml
workflow: "artifact_based"
phases:
  - phase: 1
    name: "Planning"
    outputs:
      - artifact: "implementation_plan.md"
        content:
          - Feature description
          - Technical approach
          - Files to modify/create
          - Dependencies
          - Estimated complexity

      - artifact: "task.md"
        content:
          - Numbered checklist of tasks
          - Status: [ ] pending, [x] complete
          - Updated in real-time during execution

  - phase: 2
    name: "Execution"
    inputs:
      - "implementation_plan.md"
      - "task.md"
    updates:
      - artifact: "task.md"
        action: "Mark tasks complete as executed"

  - phase: 3
    name: "Verification"
    outputs:
      - artifact: "walkthrough.md"
        content:
          - Feature walkthrough
          - Screenshots (1-5 critical views)
          - Verification steps
          - Edge cases tested
```

---

### Workflow 3: Parallel Orchestration (Poke Pattern)

**When to Use**: Independent tasks that can run concurrently

**Structure**:
```
Orchestrator
  ├─ Agent 1 (parallel) → Result 1
  ├─ Agent 2 (parallel) → Result 2
  ├─ Agent 3 (parallel) → Result 3
  └─ Aggregator → Combines results → Final output
```

**Flow**:
```yaml
workflow: "parallel_orchestration"
mode: "ORCHESTRATION"

parallel_agents:
  - agent: "frontend_builder"
    task: "Build React components"
    inputs: {feature_spec: "$spec_file"}
    outputs: {components: ["Button.tsx", "Form.tsx"]}

  - agent: "backend_builder"
    task: "Build API endpoints"
    inputs: {feature_spec: "$spec_file"}
    outputs: {endpoints: ["POST /api/users", "GET /api/users"]}

  - agent: "test_builder"
    task: "Build E2E tests"
    inputs: {feature_spec: "$spec_file"}
    outputs: {tests: ["user-flow.test.ts"]}

aggregation:
  - Wait for all agents to complete
  - Verify integration (components → API → tests)
  - Generate unified report
```

---

## COMMON RECIPES

### Recipe: Feature Development

**Task**: Build a complete feature (frontend + backend + tests)

**Workflow**:
```yaml
recipe: "feature_development"
input: Feature specification

phases:
  1. Planning (Planning Mode):
     - Analyze spec
     - Design architecture
     - Plan implementation

  2. Parallel Development (Orchestration Mode):
     - Frontend agent: Build UI
     - Backend agent: Build API
     - Test agent: Build tests

  3. Integration (Execution Mode):
     - Integrate frontend + backend
     - Verify E2E tests pass

  4. Verification (Verification Mode):
     - Run full test suite
     - Generate walkthrough.md with screenshots
     - Validate against spec

output:
  - Complete feature implementation
  - Tests (100% passing)
  - Documentation (walkthrough.md)
  - ##report (compliance score, metrics)
```

---

### Recipe: Bug Fixing

**Task**: Systematically identify and fix a bug

**Workflow**:
```yaml
recipe: "bug_fixing"
input: Bug report (description, steps to reproduce)

phases:
  1. Investigation (Research Mode):
     - Reproduce bug
     - Locate root cause (grep, read relevant files)
     - Identify affected files

  2. Fix Planning (Planning Mode):
     - Design fix approach
     - Identify test cases needed
     - Plan implementation

  3. Implementation (Execution Mode):
     - Apply fix
     - Add regression test
     - Verify bug no longer reproduces

  4. Verification (Verification Mode):
     - Run affected tests
     - Run full test suite
     - Generate ##report

output:
  - Bug fixed
  - Regression test added
  - ##report documenting fix
```

---

### Recipe: Code Refactoring

**Task**: Refactor code while preserving behavior

**Workflow**:
```yaml
recipe: "code_refactoring"
input: Code to refactor + refactoring goal

phases:
  1. Analysis (Research Mode):
     - Understand current implementation
     - Identify code smells
     - Document current behavior

  2. Test Expansion (Execution Mode):
     - Add comprehensive tests for current behavior
     - Verify 100% test coverage for refactored section
     - Baseline: All tests pass

  3. Refactoring (Execution Mode):
     - Refactor code incrementally
     - Run tests after each change
     - Rollback if tests fail

  4. Verification (Verification Mode):
     - All tests still pass
     - Code quality metrics improved
     - Performance not degraded

output:
  - Refactored code
  - Improved code quality
  - All tests passing
  - ##report (before/after metrics)
```

---

### Recipe: API Endpoint Creation

**Task**: Build new API endpoint with validation, tests, docs

**Workflow**:
```yaml
recipe: "api_endpoint"
input: API specification (method, path, request/response schema)

phases:
  1. Schema Design (Planning Mode):
     - Design request/response types
     - Plan validation rules
     - Identify database operations needed

  2. Implementation (Execution Mode):
     - Create endpoint handler
     - Add request validation
     - Implement business logic
     - Add error handling
     - Create unit tests

  3. Integration (Execution Mode):
     - Add integration tests
     - Test authentication/authorization
     - Test error cases

  4. Documentation (Execution Mode):
     - Add OpenAPI/Swagger documentation
     - Add usage examples
     - Update API changelog

output:
  - Complete API endpoint
  - Request/response validation
  - Unit + integration tests
  - API documentation
```

---

### Recipe: Database Migration

**Task**: Create and apply database schema changes

**Workflow**:
```yaml
recipe: "database_migration"
input: Schema changes needed

phases:
  1. Migration Design (Planning Mode):
     - Analyze current schema
     - Design migration (up + down)
     - Identify data migration needs
     - Plan rollback strategy

  2. Migration Creation (Execution Mode):
     - Create migration file
     - Write up migration
     - Write down migration (rollback)
     - Add data migration if needed

  3. Testing (Verification Mode):
     - Apply migration to test database
     - Verify schema changes
     - Test rollback (down migration)
     - Verify data integrity

  4. Documentation (Execution Mode):
     - Document migration purpose
     - Document rollback procedure
     - Update schema documentation

output:
  - Migration files (up + down)
  - Tested on test database
  - Rollback procedure documented
  - ##report
```

---

## ORCHESTRATION PATTERNS

### Pattern 1: Sequential Pipeline

**Structure**: Phase 1 → Phase 2 → Phase 3 → Phase 4

**When to Use**: Each phase depends on previous phase output

```yaml
pattern: "sequential_pipeline"
phases:
  - phase: "discover"
    outputs: ["$codebase_structure", "$affected_files"]

  - phase: "plan"
    inputs: ["$discover.codebase_structure", "$discover.affected_files"]
    outputs: ["$implementation_plan"]

  - phase: "execute"
    inputs: ["$plan.implementation_plan"]
    outputs: ["$modified_files"]

  - phase: "verify"
    inputs: ["$execute.modified_files"]
    outputs: ["$test_results", "$report"]
```

---

### Pattern 2: Fan-Out / Fan-In

**Structure**:
```
Single task
  ├─→ Subtask 1 ─┐
  ├─→ Subtask 2 ─┤
  └─→ Subtask 3 ─┴─→ Combine results
```

**When to Use**: Task can be split into independent subtasks

```yaml
pattern: "fan_out_fan_in"

fan_out:
  source_task: "Build full-stack feature"
  subtasks:
    - id: "frontend"
      agent: "frontend_agent"
      task: "Build UI components"

    - id: "backend"
      agent: "backend_agent"
      task: "Build API"

    - id: "tests"
      agent: "test_agent"
      task: "Build tests"

fan_in:
  aggregator: "integration_agent"
  inputs: ["$frontend.outputs", "$backend.outputs", "$tests.outputs"]
  task: "Integrate and verify"
```

---

### Pattern 3: Iterative Refinement

**Structure**: Plan → Execute → Review → [Refine if needed] → Repeat

**When to Use**: Quality gates may fail, requiring iteration

```yaml
pattern: "iterative_refinement"
max_iterations: 3

loop:
  - phase: "execute"
    outputs: ["$implementation"]

  - phase: "review"
    inputs: ["$implementation"]
    outputs: ["$review_result"]

  - decision:
      if: "$review_result.status == 'pass'"
      then: "complete"
      else: "refine"

  - phase: "refine"  # Only if review failed
    inputs: ["$review_result.issues"]
    outputs: ["$fixes"]
    action: "Apply fixes and re-execute"
```

---

### Pattern 4: Conditional Branching

**Structure**: Decision point → Branch A OR Branch B

**When to Use**: Different paths based on conditions

```yaml
pattern: "conditional_branching"

phases:
  - phase: "analysis"
    outputs: ["$complexity_score"]

  - decision:
      condition: "$complexity_score > 8"
      branches:
        high_complexity:
          - Use two-phase planning
          - Add extra validation
          - Require manual review

        low_complexity:
          - Skip planning phase
          - Direct execution
          - Auto-approve

  - phase: "execution"
    inputs: ["$analysis.outputs", "$decision.branch_output"]
```

---

## WORKFLOW COMPOSITION

### Composing Workflows

**Workflows can be nested**:

```yaml
workflow: "complete_feature_pipeline"

phases:
  - phase: "frontend"
    workflow: "feature_development"  # Nested workflow
    inputs: {spec: "$frontend_spec"}

  - phase: "backend"
    workflow: "feature_development"  # Nested workflow
    inputs: {spec: "$backend_spec"}

  - phase: "integration"
    workflow: "integration_testing"  # Another nested workflow
    inputs: {frontend: "$frontend.outputs", backend: "$backend.outputs"}
```

---

### Workflow Templates

**Parametrized workflow templates**:

```yaml
template: "crud_resource"
parameters:
  - resource_name: string  # e.g., "User"
  - fields: array  # e.g., ["name", "email", "age"]
  - database: string  # e.g., "postgresql"

workflow:
  - phase: "generate_model"
    inputs: {resource: "$resource_name", fields: "$fields"}

  - phase: "generate_api"
    inputs: {resource: "$resource_name", database: "$database"}

  - phase: "generate_tests"
    inputs: {resource: "$resource_name"}

# Usage:
# instantiate template: crud_resource
#   resource_name: "Product"
#   fields: ["name", "price", "description"]
#   database: "postgresql"
```

---

## WORKFLOW METRICS

### Track Workflow Performance

```yaml
workflow_metrics:
  - workflow_id: "feature_dev_20251124_001"
    workflow_name: "feature_development"
    total_duration: "45 minutes"
    phases:
      - name: "planning"
        duration: "8 minutes"
        agent: "planning_agent"
      - name: "execution"
        duration: "32 minutes"
        agent: "execution_agent"
      - name: "verification"
        duration: "5 minutes"
        agent: "verification_agent"
    success: true
    files_modified: 12
    tests_created: 8
    lines_of_code: 450
```

---

## WORKFLOW CATALOG

### Quick Reference

| Workflow | Use Case | Phases | Duration | Complexity |
|----------|----------|--------|----------|------------|
| Two-Phase Planning | Complex features | 2 | 30-60min | HIGH |
| Artifact-Based | Documented development | 3 | 45-90min | HIGH |
| Parallel Orchestration | Independent tasks | 2-4 | 20-40min | MEDIUM |
| Feature Development | Full-stack feature | 4 | 60-120min | VERY HIGH |
| Bug Fixing | Systematic bug resolution | 4 | 15-30min | MEDIUM |
| Code Refactoring | Improve code quality | 4 | 30-60min | MEDIUM |
| API Endpoint | New API endpoint | 4 | 20-40min | MEDIUM |
| Database Migration | Schema changes | 4 | 20-45min | HIGH |

---

## BEST PRACTICES

### 1. Always Define Clear Inputs/Outputs

```yaml
# ✅ Good: Clear contracts
phase:
  name: "planning"
  inputs:
    $user_request: string
    $codebase_path: string
  outputs:
    $implementation_plan: file_path
    $task_checklist: file_path
    $affected_files: array[string]

# ❌ Bad: Unclear contracts
phase:
  name: "planning"
  inputs: "stuff"
  outputs: "results"
```

---

### 2. Use $arguments Chaining

```yaml
# ✅ Good: Explicit argument flow
phases:
  - phase: 1
    outputs:
      $plan: "path/to/plan.md"

  - phase: 2
    inputs:
      $plan_file: "$phase1.plan"  # Explicit reference

# ❌ Bad: Implicit, magic references
phases:
  - phase: 1
  - phase: 2  # How does it get phase 1 output?
```

---

### 3. Include Validation Gates

```yaml
# ✅ Good: Explicit validation
phases:
  - phase: "execution"
    outputs: ["$code"]

  - phase: "validation"
    inputs: ["$code"]
    gates:
      - run: "npm test"
        fail_on_error: true
      - run: "npm run lint"
        fail_on_error: true
      - check: "test_coverage >= 80%"

# ❌ Bad: No validation
phases:
  - phase: "execution"
    outputs: ["$code"]
  # Deploy directly? Risky!
```

---

### 4. Provide Rollback Strategies

```yaml
# ✅ Good: Rollback plan
workflow: "database_migration"
phases:
  - phase: "apply_migration"
    rollback: "run down migration"

  - phase: "verify"
    rollback: "restore database backup"

# ❌ Bad: No rollback
workflow: "database_migration"
phases:
  - phase: "apply_migration"
    # No rollback? What if it fails?
```

---

## INTEGRATION

This layer defines workflow patterns for:
- Multi-agent orchestration
- Complex task execution
- ADW (AI Developer Workflow) creation
- Recipe libraries

**Composition**:
```yaml
prompt_layers:
  - 01_identity_layer.md
  - 02_operating_modes.md
  - 03_tool_usage_layer.md
  - 08_workflows.md  ← YOU ARE HERE
```

---

**Layer Maintained By**: CODEXA Team
**Last Updated**: 2025-11-24
**Related Layers**: 02_operating_modes.md, 07_steering_hooks.md
**Influenced By**: Devin (two-phase), Antigravity (artifacts), Poke (parallel orchestration), Windsurf (cascade), and 25+ other platforms
