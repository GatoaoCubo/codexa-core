# Multi-Agent System Architecture
**Version**: 2.0.0
**Created**: 2025-11-24
**Phase**: 2 (Day 5-7)
**Status**: Design Complete → Implementation Ready

---

## 🎯 EXECUTIVE SUMMARY

**Purpose**: Design and implement a robust multi-agent orchestration system for CODEXA that enables:
- Specialized agents working in parallel or sequential workflows
- Two-phase planning workflows (Devin pattern)
- Parallel orchestration (Poke pattern)
- Agent handoffs and state management
- Fault-tolerant execution with rollback capabilities

**Key Principles**:
1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Composability**: Agents are composed from prompt layers using the composer
3. **State Isolation**: Agents communicate through artifacts, not shared memory
4. **Fault Tolerance**: System handles agent failures gracefully
5. **Observability**: Every agent action is logged and traceable

---

## 🏗️ SYSTEM OVERVIEW

### Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                  USER INTERFACE                         │
│           (CLI, API, Web UI, Voice)                     │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                ORCHESTRATOR LAYER                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Workflow   │  │   Task       │  │   Agent        │ │
│  │  Scheduler  │  │  Dispatcher  │  │   Registry     │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                 AGENT POOL LAYER                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Planning │  │Execution │  │Verification│             │
│  │  Agent   │  │  Agent   │  │   Agent    │             │
│  └──────────┘  └──────────┘  └──────────┘              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   Fix    │  │ Research │  │Specialized│             │
│  │  Agent   │  │  Agent   │  │  Agents   │             │
│  └──────────┘  └──────────┘  └──────────┘              │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│             COMMUNICATION LAYER                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │   Artifact  │  │   Message    │  │    Event       │ │
│  │   Storage   │  │     Bus      │  │   Logger       │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│              EXECUTION LAYER                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │   LLM       │  │    Tools     │  │   Knowledge    │ │
│  │  Provider   │  │   (Read/     │  │     Base       │ │
│  │             │  │   Write/     │  │                │ │
│  │             │  │   Bash/etc)  │  │                │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 AGENT TYPES

### 1. Planning Agent
**Preset**: `planning`
**Mode**: PLANNING (read-only)
**Layers**: identity, operating_modes, tool_usage, communication

**Responsibilities**:
- Analyze user requirements
- Explore codebase (read-only)
- Generate implementation plan
- Identify dependencies and risks
- Create task breakdown
- Estimate complexity

**Input**: User request + context
**Output**: `plan.md` + `task.json`

**Tools Available**:
- ✅ Read, Glob, Grep (file exploration)
- ✅ WebSearch, WebFetch (research)
- ✅ Task (spawn sub-agents for exploration)
- ❌ NO Write, Edit, Bash (no modifications)

**Example**:
```yaml
agent:
  type: planning
  input: "Add user authentication feature"
  output:
    plan: specs/auth_plan.md
    tasks:
      - id: 1
        description: "Create user model"
        files: [models/user.py]
        risk: low
      - id: 2
        description: "Implement JWT middleware"
        files: [middleware/auth.py]
        risk: medium
```

---

### 2. Execution Agent
**Preset**: `execution`
**Mode**: EXECUTION (write access)
**Layers**: identity, operating_modes, tool_usage, communication

**Responsibilities**:
- Implement features from plan
- Modify existing files
- Create new files
- Run builds and tests
- Fix issues during implementation

**Input**: `plan.md` + `task.json`
**Output**: Code artifacts + execution report

**Tools Available**:
- ✅ All Read tools (Glob, Grep, Read)
- ✅ All Write tools (Write, Edit)
- ✅ Bash (for building, testing)
- ✅ Task (spawn Fix agents if needed)

**Example**:
```yaml
agent:
  type: execution
  input:
    plan: specs/auth_plan.md
    task_id: 1
  output:
    artifacts:
      - models/user.py (created)
      - tests/test_user.py (created)
    status: success
```

---

### 3. Verification Agent
**Preset**: `verification`
**Mode**: VERIFICATION (read + test execution)
**Layers**: identity, operating_modes, tool_usage, communication

**Responsibilities**:
- Run all tests
- Validate against specification
- Check code quality
- Generate walkthrough report
- Identify regressions

**Input**: Implementation artifacts + spec
**Output**: `walkthrough.md` + `##report`

**Tools Available**:
- ✅ All Read tools
- ✅ Bash (for test execution)
- ✅ Task (spawn explorers)
- ❌ NO Write, Edit (read-only verification)

**Example**:
```yaml
agent:
  type: verification
  input:
    spec: specs/auth_plan.md
    artifacts: [models/user.py, middleware/auth.py]
  output:
    walkthrough: docs/walkthrough_auth.md
    report:
      tests_passed: 45
      tests_failed: 2
      coverage: 87%
      issues: [...]
```

---

### 4. Fix Agent
**Preset**: `execution`
**Mode**: FIX (targeted modifications)
**Layers**: identity, operating_modes, tool_usage, communication

**Responsibilities**:
- Fix test failures
- Address specific errors
- Make targeted corrections
- Minimal scope modifications

**Input**: Error report + context
**Output**: Fixed artifacts

**Tools Available**:
- Same as Execution Agent
- Focus on minimal, targeted changes

**Example**:
```yaml
agent:
  type: fix
  input:
    error: "TypeError: User.email is None"
    file: models/user.py
    line: 45
  output:
    fixed_files: [models/user.py]
    changes: "Added email validation in __init__"
```

---

### 5. Research Agent
**Preset**: `planning`
**Mode**: RESEARCH (exploration + external search)
**Layers**: identity, operating_modes, tool_usage, communication

**Responsibilities**:
- Research external documentation
- Find similar patterns in codebase
- Gather technical information
- Analyze best practices
- Provide recommendations

**Input**: Research question + context
**Output**: Research report

**Tools Available**:
- ✅ All Read tools
- ✅ WebSearch, WebFetch
- ✅ Task (spawn explorers)
- ❌ NO Write, Edit

---

### 6. Orchestrator Agent
**Preset**: `orchestrator`
**Mode**: ORCHESTRATION (coordination)
**Layers**: identity, operating_modes, tool_usage, communication, workflows

**Responsibilities**:
- Coordinate multiple agents
- Manage parallel execution
- Handle agent handoffs
- Aggregate results
- Resolve conflicts
- Rollback on failures

**Input**: High-level workflow definition
**Output**: Orchestration report + aggregated artifacts

**Tools Available**:
- ✅ Task (spawn all agent types)
- ✅ TodoWrite (track orchestration progress)
- ✅ Read tools (validation)
- ❌ Generally NO direct file modifications

---

## 🔄 WORKFLOW PATTERNS

### Pattern 1: Two-Phase Workflow (Devin)

**Use Case**: Most feature development, medium-high complexity tasks

```
USER REQUEST
     ↓
┌────────────────────────────────┐
│  PHASE 1: PLANNING             │
│  Agent: Planning Agent         │
│  Duration: 2-5 minutes         │
│  Output: plan.md + task.json   │
└────────────┬───────────────────┘
             │ (handoff)
             ↓
┌────────────────────────────────┐
│  PHASE 2: EXECUTION            │
│  Agent: Execution Agent        │
│  Duration: 5-20 minutes        │
│  Input: $plan + $tasks         │
│  Output: code files            │
└────────────┬───────────────────┘
             │ (handoff)
             ↓
┌────────────────────────────────┐
│  PHASE 3: VERIFICATION         │
│  Agent: Verification Agent     │
│  Duration: 2-5 minutes         │
│  Input: $artifacts + $spec     │
│  Output: walkthrough.md        │
└────────────┬───────────────────┘
             │
             ↓ (if failures)
┌────────────────────────────────┐
│  PHASE 4: FIX (Optional)       │
│  Agent: Fix Agent              │
│  Duration: 2-10 minutes        │
│  Input: $error_report          │
│  Output: fixed files           │
└────────────────────────────────┘
             │
             ↓ (loop to verification)
```

**Example Workflow File**:
```yaml
# workflows/two_phase_feature.yml
name: "Two-Phase Feature Development"
description: "Planning → Execution → Verification workflow"

phases:
  - id: planning
    agent_type: planning
    mode: PLANNING
    timeout: 300  # 5 minutes
    input:
      user_request: "${user_request}"
      context_files: []
    output:
      plan: specs/${feature_name}_plan.md
      tasks: specs/${feature_name}_tasks.json

  - id: execution
    agent_type: execution
    mode: EXECUTION
    depends_on: [planning]
    timeout: 1200  # 20 minutes
    input:
      plan: "${planning.output.plan}"
      tasks: "${planning.output.tasks}"
    output:
      artifacts: []  # Dynamic
      report: outputs/execution_report.json

  - id: verification
    agent_type: verification
    mode: VERIFICATION
    depends_on: [execution]
    timeout: 300  # 5 minutes
    input:
      spec: "${planning.output.plan}"
      artifacts: "${execution.output.artifacts}"
    output:
      walkthrough: docs/walkthrough_${feature_name}.md
      report: outputs/verification_report.json

  - id: fix
    agent_type: fix
    mode: FIX
    depends_on: [verification]
    condition: "${verification.output.report.tests_failed > 0}"
    timeout: 600  # 10 minutes
    max_iterations: 3
    input:
      errors: "${verification.output.report.failures}"
      spec: "${planning.output.plan}"
    output:
      fixed_files: []  # Dynamic
```

---

### Pattern 2: Parallel Orchestration (Poke)

**Use Case**: Independent tasks, maximum parallelism

```
USER REQUEST
     ↓
┌────────────────────────────────┐
│  ORCHESTRATOR                  │
│  Decomposes into parallel      │
│  independent tasks             │
└────┬─────┬─────┬────────────────┘
     │     │     │
     │     │     └────────────────┐
     │     │                      │
     │     └─────────┐            │
     │               │            │
     ↓               ↓            ↓
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Agent 1 │   │ Agent 2 │   │ Agent 3 │
│Frontend │   │ Backend │   │  Tests  │
│ (Exec)  │   │ (Exec)  │   │ (Exec)  │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     │             │             │
     └─────────────┼─────────────┘
                   │
                   ↓
          ┌────────────────┐
          │  AGGREGATOR    │
          │  (Verifier)    │
          │  Combines all  │
          │  outputs       │
          └────────────────┘
```

**Example Workflow File**:
```yaml
# workflows/parallel_feature.yml
name: "Parallel Feature Development"
description: "Frontend + Backend + Tests in parallel"

orchestration:
  type: parallel
  aggregation: required

  parallel_agents:
    - id: frontend
      agent_type: execution
      mode: EXECUTION
      timeout: 900
      input:
        spec: specs/frontend_spec.md
      output:
        artifacts: [components/*, pages/*]

    - id: backend
      agent_type: execution
      mode: EXECUTION
      timeout: 900
      input:
        spec: specs/backend_spec.md
      output:
        artifacts: [api/*, models/*]

    - id: tests
      agent_type: execution
      mode: EXECUTION
      timeout: 600
      input:
        spec: specs/test_spec.md
      output:
        artifacts: [tests/*]

  aggregation_phase:
    agent_type: verification
    mode: VERIFICATION
    timeout: 300
    input:
      frontend_artifacts: "${frontend.output.artifacts}"
      backend_artifacts: "${backend.output.artifacts}"
      test_artifacts: "${tests.output.artifacts}"
    output:
      integration_report: outputs/integration_report.md
```

---

### Pattern 3: Simple Execution (Skip Planning)

**Use Case**: Trivial tasks, exact location known, low risk

```
USER REQUEST (simple, low-risk)
     ↓
┌────────────────────────────────┐
│  SINGLE EXECUTION AGENT        │
│  Directly implements change    │
│  No planning phase             │
│  Duration: 1-3 minutes         │
└────────────┬───────────────────┘
             │
             ↓
     DONE (artifacts)
```

**Conditions for Simple Execution**:
- ✅ Single file modification
- ✅ Exact location known
- ✅ No architectural changes
- ✅ Low risk of side effects
- ✅ Clear, unambiguous request

**Example**:
```yaml
# Simple task - skip planning
name: "Add docstring to function"
workflow: simple_execution
agent: execution
input:
  file: utils/helpers.py
  function: calculate_total
  action: add_docstring
```

---

## 📡 COMMUNICATION PROTOCOLS

### Artifact-Based Communication

**Key Principle**: Agents communicate through artifacts (files), not shared memory.

```python
# Artifact structure
class Artifact:
    id: str                # Unique identifier
    type: str              # plan, code, report, data
    producer: str          # Agent that created it
    created_at: datetime   # Timestamp
    path: str              # File path
    metadata: Dict         # Additional context
    dependencies: List[str]  # Other artifact IDs
```

**Artifact Types**:
1. **Plan Artifacts** (`plan.md`, `task.json`)
   - Produced by: Planning Agent
   - Consumed by: Execution Agent
   - Format: Markdown + JSON

2. **Code Artifacts** (`.py`, `.js`, `.ts`, etc.)
   - Produced by: Execution Agent, Fix Agent
   - Consumed by: Verification Agent
   - Format: Source code files

3. **Report Artifacts** (`walkthrough.md`, `report.json`)
   - Produced by: Verification Agent
   - Consumed by: Fix Agent, Orchestrator
   - Format: Markdown + JSON

4. **Data Artifacts** (`.json`, `.yml`)
   - Produced by: Any agent
   - Consumed by: Any agent
   - Format: Structured data

---

### Message Bus

**Purpose**: Real-time communication between Orchestrator and Agents

```python
class Message:
    type: str           # command, status, result, error
    sender: str         # Agent ID
    receiver: str       # Agent ID or "orchestrator"
    payload: Dict       # Message content
    timestamp: datetime
    correlation_id: str # For tracking related messages
```

**Message Types**:
1. **Command**: Orchestrator → Agent
   ```json
   {
     "type": "command",
     "sender": "orchestrator",
     "receiver": "planning_agent_001",
     "payload": {
       "action": "create_plan",
       "input": {...}
     }
   }
   ```

2. **Status**: Agent → Orchestrator
   ```json
   {
     "type": "status",
     "sender": "planning_agent_001",
     "receiver": "orchestrator",
     "payload": {
       "status": "in_progress",
       "progress": 0.45,
       "message": "Analyzing codebase..."
     }
   }
   ```

3. **Result**: Agent → Orchestrator
   ```json
   {
     "type": "result",
     "sender": "planning_agent_001",
     "receiver": "orchestrator",
     "payload": {
       "status": "success",
       "artifacts": ["specs/plan.md"],
       "metadata": {...}
     }
   }
   ```

4. **Error**: Agent → Orchestrator
   ```json
   {
     "type": "error",
     "sender": "execution_agent_001",
     "receiver": "orchestrator",
     "payload": {
       "error_type": "timeout",
       "message": "Build exceeded timeout",
       "can_retry": true
     }
   }
   ```

---

### Agent Handoff Protocol

**Handoff**: Transfer of control from one agent to another

```python
class Handoff:
    from_agent: str         # Source agent ID
    to_agent: str           # Target agent ID
    artifacts: List[str]    # Artifact paths to pass
    context: Dict           # Additional context
    instructions: str       # Specific instructions for next agent
    success_criteria: List[str]  # What defines success
```

**Handoff Example** (Planning → Execution):
```json
{
  "from_agent": "planning_agent_001",
  "to_agent": "execution_agent_001",
  "artifacts": [
    "specs/auth_plan.md",
    "specs/auth_tasks.json"
  ],
  "context": {
    "feature_name": "user_authentication",
    "priority": "high",
    "estimated_duration": "15min"
  },
  "instructions": "Implement all tasks in auth_tasks.json according to auth_plan.md. Focus on security best practices.",
  "success_criteria": [
    "All files in task list created",
    "Tests pass",
    "No security vulnerabilities"
  ]
}
```

---

## 🧠 STATE MANAGEMENT

### Workflow State

```python
class WorkflowState:
    workflow_id: str
    status: str  # pending, running, success, failed, rollback
    current_phase: str
    phases_completed: List[str]
    artifacts_created: List[str]
    agents_spawned: List[str]
    started_at: datetime
    completed_at: Optional[datetime]
    metadata: Dict
```

**State Transitions**:
```
pending → running → success
                 ↘ failed → rollback → failed_final
                          ↘ success (after rollback)
```

---

### Agent State

```python
class AgentState:
    agent_id: str
    agent_type: str  # planning, execution, etc.
    status: str  # idle, running, success, error
    current_task: Optional[str]
    artifacts_produced: List[str]
    tools_used: List[str]
    started_at: datetime
    duration: Optional[float]  # seconds
    metadata: Dict
```

---

## 🛡️ ERROR HANDLING & ROLLBACK

### Error Types

1. **Timeout**: Agent exceeds time limit
   - Action: Kill agent, report timeout
   - Retry: Yes (configurable max_retries)

2. **Tool Failure**: Tool call fails
   - Action: Retry with exponential backoff
   - Retry: Yes (max 3 retries)

3. **Verification Failure**: Tests fail
   - Action: Spawn Fix Agent
   - Retry: Yes (max 3 fix iterations)

4. **Critical Error**: Unrecoverable failure
   - Action: Rollback entire workflow
   - Retry: No

---

### Rollback Strategy

```python
class RollbackManager:
    def rollback(self, workflow_id: str):
        """
        Rollback all changes made during workflow.

        Steps:
        1. Get all artifacts created
        2. Delete new files
        3. Restore modified files from backup
        4. Update workflow state to "rollback"
        5. Notify user
        """
```

**Backup Strategy**:
- Before execution phase, create backup of all files to be modified
- Store backups in `.codexa/backups/{workflow_id}/`
- On success, delete backup
- On failure, restore from backup

---

## 📊 OBSERVABILITY & LOGGING

### Event Logging

All agent actions logged to:
- `logs/workflows/{workflow_id}.log`
- `logs/agents/{agent_id}.log`

**Log Entry Structure**:
```json
{
  "timestamp": "2025-11-24T14:30:45.123Z",
  "level": "INFO",
  "agent_id": "planning_agent_001",
  "workflow_id": "wf_abc123",
  "event": "tool_call",
  "tool": "Read",
  "file": "models/user.py",
  "duration_ms": 45,
  "status": "success"
}
```

---

### Metrics

**Workflow Metrics**:
- Total duration
- Phase durations
- Number of agents spawned
- Artifacts created
- Success rate
- Error rate

**Agent Metrics**:
- Tool call frequency
- Tool success rate
- Average task duration
- Error frequency

---

## 🚀 IMPLEMENTATION ROADMAP

### Phase 2.1: Core Infrastructure (Day 5)
- [ ] Implement Orchestrator class
- [ ] Implement Agent Registry
- [ ] Implement Artifact Storage
- [ ] Implement Message Bus
- [ ] Implement State Management

### Phase 2.2: Agent Implementation (Day 6)
- [ ] Generate specialized agents using composer
- [ ] Implement agent spawning system
- [ ] Implement handoff protocol
- [ ] Implement agent communication

### Phase 2.3: Workflow Implementation (Day 7)
- [ ] Implement Two-Phase Workflow
- [ ] Implement Parallel Orchestration
- [ ] Implement error handling & rollback
- [ ] Create workflow definition system
- [ ] Build workflow executor

### Phase 2.4: Testing & Validation
- [ ] Unit tests for each component
- [ ] Integration tests for workflows
- [ ] End-to-end tests with real scenarios
- [ ] Performance benchmarks

---

## 📚 NEXT STEPS

1. **Implement Core Orchestrator** (`src/orchestrator.py`)
2. **Generate Agent Artifacts** (using composer)
3. **Build Workflow Executor** (`src/workflow_executor.py`)
4. **Create Example Workflows** (`workflows/*.yml`)
5. **Test with Real Scenarios** (auth feature, API endpoints, etc.)

---

**Architecture Complete ✅**
**Ready for Implementation** 🚀
