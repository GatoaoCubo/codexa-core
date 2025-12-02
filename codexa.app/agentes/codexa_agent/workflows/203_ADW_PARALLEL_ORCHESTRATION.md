# 203_ADW_PARALLEL_ORCHESTRATION | Multi-Agent Parallel Execution

**Version**: 2.0.0 | **Created**: 2025-11-24
**Type**: Meta-ADW (Orchestrates other ADWs in parallel)
**Duration**: Varies (parallel execution reduces total time)
**Pattern**: Independent Task Batching + Parallel Agents + Result Aggregation

---

## MODULE_METADATA

```yaml
id: 203_ADW_PARALLEL_ORCHESTRATION
version: 2.0.0
category: meta-workflows
type: ADW (Agentic Developer Workflow)
execution_mode: parallel_with_sync_points
dependencies:
  - builders/adw_modules/multi_agent_orchestrator.py
  - builders/adw_modules/task_boundary.py
status: production_ready
created: 2025-11-24
platform_patterns:
  - Poke: parallel agent coordination, independent batching
  - Claude Code: multiple tool calls in single response
  - Devin: task decomposition, parallel execution
  - Windsurf: conflict detection, merge strategies
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "parallel_orchestration",
  "workflow_name": "Multi-Agent Parallel Orchestration",
  "version": "2.0.0",
  "context_strategy": "distributed",
  "failure_handling": "isolate_and_continue",

  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "parallel_orchestration"},
    {"phase_id": "phase_1_decompose", "phase_name": "Task Decomposition", "duration": "2-5min"},
    {"phase_id": "phase_2_dependency", "phase_name": "Dependency Analysis", "duration": "1-3min"},
    {"phase_id": "phase_3_batch", "phase_name": "Batch Formation", "duration": "1-2min"},
    {"phase_id": "phase_4_execute", "phase_name": "Parallel Execution", "duration": "varies"},
    {"phase_id": "phase_5_aggregate", "phase_name": "Result Aggregation", "duration": "2-5min"}
  ],

  "parallelization": {
    "max_concurrent_agents": 5,
    "conflict_resolution": "first_wins_with_merge",
    "failure_isolation": true,
    "sync_points": ["after_each_batch", "before_aggregation"]
  }
}
```

---

## CORE CONCEPT: PARALLELIZATION STRATEGY

### When to Parallelize

**PARALLELIZE** when:
- Tasks are independent (no shared state)
- Tasks modify different files
- Tasks can be verified independently
- Time savings justify coordination overhead

**DON'T PARALLELIZE** when:
- Tasks have dependencies (A must complete before B)
- Tasks modify same files
- Strict ordering required
- Single task is faster than coordination overhead

### Dependency Graph Example

```
Task A (utils/helper.py)    Task B (utils/format.py)    Task C (config/settings.py)
         \                           |                           /
          \                          |                          /
           v                         v                         v
                    Task D (core/main.py - depends on A, B, C)
                                     |
                                     v
                           Task E (tests/test_main.py)
```

**Execution Plan**:
- Batch 1 (parallel): A, B, C
- Sync point: wait for all
- Batch 2 (sequential): D
- Batch 3: E

---

## PHASE DETAILS

### PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `parallel_orchestration`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### PHASE 1: Task Decomposition

**Objective**: Break complex work into atomic tasks

**Task Boundary Declaration**:
```
TASK_BOUNDARY: DECOMPOSITION
ACCESS: read_only
SCOPE: Analyze work and identify discrete tasks
```

**Actions**:
1.1. **Identify All Tasks**
   - List all changes needed
   - Break into file-level tasks
   - Identify cross-cutting concerns

1.2. **Define Task Boundaries**
   For each task:
   ```yaml
   task_id: "task_001"
   description: "Update validation logic in utils/validator.py"
   files_affected:
     - "utils/validator.py"
   estimated_duration: "5min"
   risk_level: "low|medium|high"
   ```

1.3. **Categorize Tasks**
   - File modifications
   - New file creations
   - Test additions
   - Documentation updates
   - Configuration changes

**Input**: Complex work request (e.g., "Implement authentication system")
**Output**: `$task_list`
```yaml
$task_list:
  tasks:
    - id: "task_001"
      description: str
      files: []
      estimated: str
    - id: "task_002"
      ...
  total_tasks: int
  estimated_total_time_sequential: str
```

**Validation**:
- Each task is atomic (one logical change)
- Each task has defined file scope
- No task too large (>30min estimated)

---

### PHASE 2: Dependency Analysis

**Objective**: Identify task dependencies and conflicts

**Task Boundary Declaration**:
```
TASK_BOUNDARY: DEPENDENCY_ANALYSIS
ACCESS: read_only
SCOPE: Map dependencies between tasks
```

**Actions**:
2.1. **File Conflict Detection**
   - Which tasks modify same files?
   - Mark as conflict if overlapping

2.2. **Import/Call Dependency**
   - If task A modifies function that task B calls
   - Task B depends on task A

2.3. **Build Dependency Graph**
   ```yaml
   dependencies:
     task_001: []  # No dependencies - can run first
     task_002: []  # No dependencies - can run first
     task_003: ["task_001"]  # Depends on task_001
     task_004: ["task_001", "task_002"]  # Depends on both
   ```

2.4. **Identify Independent Tasks**
   - Tasks with no dependencies
   - Tasks whose dependencies are complete
   - These form parallel batches

**Input**: `$task_list`
**Output**: `$dependency_graph`
```yaml
$dependency_graph:
  tasks: {}  # task_id -> [dependency_ids]
  conflicts: []  # pairs of conflicting tasks
  independent_tasks: []  # can run anytime
  critical_path: []  # longest dependency chain
```

**Validation**:
- No circular dependencies
- All dependencies resolvable
- Critical path identified

---

### PHASE 3: Batch Formation

**Objective**: Group independent tasks into parallel batches

**Task Boundary Declaration**:
```
TASK_BOUNDARY: BATCH_FORMATION
ACCESS: read_only
SCOPE: Create optimal parallel batches
```

**Actions**:
3.1. **Topological Sort**
   - Order tasks by dependencies
   - Group tasks at same level into batches

3.2. **Form Batches**
   ```yaml
   batch_1:
     parallel: true
     tasks: ["task_001", "task_002", "task_005"]
     sync_after: true

   batch_2:
     parallel: true
     tasks: ["task_003", "task_006"]
     sync_after: true

   batch_3:
     parallel: false  # Single critical task
     tasks: ["task_004"]
     sync_after: true
   ```

3.3. **Optimize Batch Sizes**
   - Max 5 concurrent tasks (configurable)
   - Balance load across batches
   - Minimize total batches

3.4. **Calculate Time Savings**
   ```
   Sequential time: sum(all task times)
   Parallel time: sum(max(batch times)) + sync overhead
   Savings: Sequential - Parallel
   ```

**Input**: `$dependency_graph`
**Output**: `$execution_plan`
```yaml
$execution_plan:
  batches:
    - batch_id: 1
      parallel: true
      tasks: []
      estimated_time: str
    - batch_id: 2
      ...
  total_batches: int
  estimated_parallel_time: str
  estimated_sequential_time: str
  time_savings: str
```

**Validation**:
- All tasks assigned to batches
- Dependencies respected
- No conflicts within batches

---

### PHASE 4: Parallel Execution

**Objective**: Execute batches with parallel agents

**Task Boundary Declaration**:
```
TASK_BOUNDARY: PARALLEL_EXECUTION
ACCESS: write (distributed)
SCOPE: Execute all batches according to plan
```

**Actions**:
4.1. **For Each Batch**
   ```
   BATCH_START: batch_N
   PARALLEL: [task_ids]
   ```

4.2. **Spawn Parallel Agents**
   - One agent per task in batch
   - Each agent has isolated context
   - Each agent follows task specification

4.3. **Agent Execution Pattern**
   ```python
   async def execute_batch(batch):
       tasks = []
       for task in batch.tasks:
           agent = spawn_agent(task)
           tasks.append(agent.execute())

       results = await asyncio.gather(*tasks, return_exceptions=True)
       return process_results(results)
   ```

4.4. **Sync Point After Each Batch**
   - Wait for all agents to complete
   - Collect results
   - Check for failures
   - Proceed only if batch successful

4.5. **Handle Failures**
   - Isolate failed task
   - Continue other tasks (if independent)
   - Retry failed task (max 2 attempts)
   - Report failures for manual review

**Input**: `$execution_plan`
**Output**: `$batch_results`
```yaml
$batch_results:
  batches:
    - batch_id: 1
      status: "complete|partial|failed"
      tasks:
        - task_id: "task_001"
          status: "success|failed"
          result: {}
          error: null
      duration: str
  overall_status: str
  failures: []
  retries: []
```

**Validation**:
- All batches attempted
- Sync points honored
- Failures isolated and reported

---

### PHASE 5: Result Aggregation

**Objective**: Combine parallel results into cohesive output

**Task Boundary Declaration**:
```
TASK_BOUNDARY: AGGREGATION
ACCESS: write
SCOPE: Merge results, resolve conflicts, generate report
```

**Actions**:
5.1. **Collect All Results**
   - Gather outputs from all agents
   - Verify all expected outputs present

5.2. **Conflict Resolution** (if any)
   - Detect overlapping changes
   - Apply merge strategy:
     - `first_wins`: Keep first agent's changes
     - `last_wins`: Keep last agent's changes
     - `manual`: Flag for human review
     - `smart_merge`: Git-style merge attempt

5.3. **Validate Combined State**
   - Run all tests
   - Run all validators
   - Verify no regressions

5.4. **Generate Aggregate Report**
   ```yaml
   ##report:
     workflow: parallel_orchestration
     tasks_total: int
     tasks_succeeded: int
     tasks_failed: int
     parallel_efficiency: float  # actual_time / sequential_estimate
     batches_executed: int
     conflicts_resolved: int
     final_status: str
   ```

**Input**: `$batch_results`
**Output**: `$final_report`, combined changes

**Validation**:
- All successful results integrated
- Conflicts resolved
- Tests pass on combined state
- Report complete

---

## EXECUTION

### Command Line
```bash
# Parallel execution of multiple tasks
uv run workflows/203_ADW_PARALLEL_ORCHESTRATION.py \
  --tasks "task1.yaml,task2.yaml,task3.yaml" \
  --max-parallel 5

# Parallel bug fixing
uv run workflows/203_ADW_PARALLEL_ORCHESTRATION.py \
  --workflow 202_ADW_BUG_FIXING \
  --issues "#101,#102,#103"
```

### Integration with Other ADWs
```yaml
# Execute multiple feature developments in parallel
orchestration:
  workflow: 201_ADW_FEATURE_DEVELOPMENT
  instances:
    - feature: "Add dark mode"
      branch: "feature/dark-mode"
    - feature: "Add notifications"
      branch: "feature/notifications"
    - feature: "Add export"
      branch: "feature/export"
  parallel: true
  sync_point: "after_phase_3"  # Sync after implementation
```

---

## PARALLELIZATION PATTERNS

### Pattern 1: File-Based Parallelization
```yaml
# Different files = parallel
batch:
  - modify: "src/utils/helper.py"
  - modify: "src/utils/formatter.py"
  - modify: "src/utils/validator.py"
```

### Pattern 2: Module-Based Parallelization
```yaml
# Different modules = parallel
batch:
  - feature: "authentication"  # auth/ directory
  - feature: "notifications"   # notify/ directory
  - feature: "export"          # export/ directory
```

### Pattern 3: Test Parallelization
```yaml
# Tests are usually independent
batch:
  - test: "tests/unit/test_auth.py"
  - test: "tests/unit/test_notify.py"
  - test: "tests/unit/test_export.py"
```

### Pattern 4: Documentation Parallelization
```yaml
# Docs for different modules = parallel
batch:
  - doc: "docs/auth.md"
  - doc: "docs/notify.md"
  - doc: "docs/export.md"
```

---

## CONFLICT RESOLUTION STRATEGIES

### File-Level Conflicts
```yaml
conflict_type: same_file
resolution: sequential_within_batch
strategy: |
  If two tasks modify same file:
  1. Remove from parallel batch
  2. Execute sequentially
  3. Or split into non-overlapping changes
```

### Import/Dependency Conflicts
```yaml
conflict_type: dependency
resolution: dependency_order
strategy: |
  If task B depends on task A output:
  1. Task A in earlier batch
  2. Sync point
  3. Task B in later batch
```

### Semantic Conflicts
```yaml
conflict_type: semantic
resolution: human_review
strategy: |
  If changes conflict logically:
  1. Flag for review
  2. Present both versions
  3. Human decides merge
```

---

## PERFORMANCE METRICS

### Efficiency Calculation
```python
def calculate_efficiency(sequential_time, parallel_time):
    """
    Efficiency = sequential_time / parallel_time

    efficiency > 1: Parallelization helped
    efficiency = 1: No benefit (sequential bottleneck)
    efficiency < 1: Overhead exceeded gains
    """
    return sequential_time / parallel_time if parallel_time > 0 else 1
```

### Expected Improvements
| Task Count | Independent % | Expected Speedup |
|------------|---------------|------------------|
| 3 | 100% | 2.5-3x |
| 5 | 80% | 3-4x |
| 10 | 60% | 4-5x |
| 10 | 20% | 1.5-2x |

---

## SUCCESS CRITERIA

**Workflow Succeeds When**:
- All tasks completed (success or handled failure)
- Parallel efficiency > 1 (faster than sequential)
- No unresolved conflicts
- Combined state passes all tests
- Aggregate report generated

**Workflow Fails When**:
- Critical task fails (no retry success)
- Unresolvable conflicts
- Combined state breaks tests
- Parallel overhead exceeds benefits

---

## RELATED WORKFLOWS

- `201_ADW_FEATURE_DEVELOPMENT.md` - Individual feature workflow
- `202_ADW_BUG_FIXING.md` - Individual bug fix workflow
- `100_ADW_DOC_SYNC_WORKFLOW.md` - Can parallelize per-agent sync
- `96_meta_orchestrate_HOP.md` - Orchestration patterns

---

**Version**: 2.0.0
**Status**: Production-Ready
**Pattern**: Poke-inspired parallel orchestration
**Maintainer**: CODEXA Team
