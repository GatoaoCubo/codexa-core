# HOP-30 | SPAWNER - Execute via Task Tool

> **Module**: SPAWNER
> **Version**: 1.0.0
> **Layer**: Execution

---

## IDENTITY

```
┌─────────────────────────────────────────────────────────┐
│  SPAWNER - "Eu spawno. Eu monitoro. Eu coleto."         │
│                                                         │
│  INPUT:  Execution plan from PLANNER                    │
│  OUTPUT: Task results from all spawned agents           │
│                                                         │
│  USES: Claude Code Task tool for parallel spawning      │
└─────────────────────────────────────────────────────────┘
```

---

## INPUT_CONTRACT

```yaml
$execution_plan:
  type: object
  from: HOP-20 PLANNER
  required:
    - plan_id
    - phases
    - spawn_pattern
```

---

## OUTPUT_CONTRACT

```yaml
$spawn_results:
  type: object
  schema:
    plan_id: string
    phases_completed: number
    total_phases: number
    tasks_completed: number
    total_tasks: number
    results: array
      - task_id: string
        agent: string
        phase: number
        status: string        # "completed", "failed", "retrying"
        quality_score: number
        output_file: string
        execution_time_ms: number
        error: string         # If failed
    aggregated_quality: number
    total_time_ms: number
```

---

## SPAWN IMPLEMENTATION

### Task Tool Pattern

```javascript
// Spawn a single agent task
Task({
  subagent_type: "general-purpose",
  description: `${agent} - ${task_description}`,
  prompt: buildAgentPrompt(agent, context, input)
});
```

### Build Agent Prompt

```javascript
function buildAgentPrompt(agent, context, input) {
  return `
# AGENT ACTIVATION: ${agent}

## YOUR CONTEXT
${context.must_read.join('\n')}

## YOUR TASK
${input.task_description}

## YOUR INPUT
${JSON.stringify(input.data, null, 2)}

## OUTPUT FORMAT
Return a JSON report:
{
  "status": "completed",
  "quality_score": 8.5,
  "output": {
    "file": "path/to/output.md",
    "summary": "Brief summary of what was done"
  },
  "metrics": {
    "items_processed": 1,
    "execution_time_ms": 45000
  }
}

## IMPORTANT
- Follow your PRIME.md identity
- Apply quality gates (≥7.0)
- Save output to specified destination
- Report back with structured JSON
`;
}
```

---

## EXECUTION PATTERNS

### Pattern A: Sequential Pipeline

```javascript
async function executeSequential(plan) {
  const results = [];

  for (const phase of plan.phases) {
    console.log(`Phase ${phase.phase_number}: ${phase.phase_name}`);

    const phaseResults = await executePhase(phase);
    results.push(...phaseResults);

    // Validate before next phase
    if (!validatePhaseResults(phaseResults)) {
      throw new Error(`Phase ${phase.phase_number} failed validation`);
    }

    // Pass outputs to next phase
    updateInputsForNextPhase(plan, phase, phaseResults);
  }

  return results;
}
```

### Pattern B: Parallel Batch

```javascript
async function executeParallel(phase) {
  const { tasks, max_concurrent = 5 } = phase;
  const results = [];

  // Split into batches
  const batches = chunk(tasks, max_concurrent);

  for (const batch of batches) {
    // Spawn all in batch simultaneously
    const batchResults = await Promise.all(
      batch.map(task => spawnTask(task))
    );
    results.push(...batchResults);
  }

  return results;
}
```

### Pattern C: Fan-out / Fan-in

```javascript
async function executeFanOutFanIn(plan) {
  // Phase 1: Fan-out (parallel)
  const fanOutResults = await executeParallel(plan.phases[0]);

  // Merge point: Aggregate results
  const mergedData = mergeResults(fanOutResults);

  // Phase 2: Process merged (sequential or parallel)
  const processedResults = await executePhase(plan.phases[1], mergedData);

  // Phase 3: Fan-out again if needed
  // ...

  return allResults;
}
```

---

## SPAWN TASK FUNCTION

```javascript
async function spawnTask(task) {
  const { agent, prompt_template, input_source, output_destination } = task;

  // 1. Load context via Scout
  const context = await mcp__scout__smart_context({
    agent: agent,
    task: prompt_template
  });

  // 2. Load input data
  const inputData = await loadInput(input_source);

  // 3. Build prompt
  const prompt = buildAgentPrompt(agent, context, {
    task_description: prompt_template,
    data: inputData,
    output_destination: output_destination
  });

  // 4. Spawn via Task tool
  const result = await Task({
    subagent_type: "general-purpose",
    description: `${agent} - ${prompt_template}`,
    prompt: prompt
  });

  // 5. Parse result
  return {
    task_id: generateUUID(),
    agent: agent,
    status: result.status || "completed",
    quality_score: result.quality_score || 0,
    output_file: result.output?.file,
    execution_time_ms: result.metrics?.execution_time_ms || 0
  };
}
```

---

## RETRY LOGIC

```javascript
async function spawnWithRetry(task, maxRetries = 1) {
  let attempts = 0;
  let lastError = null;

  while (attempts <= maxRetries) {
    try {
      const result = await spawnTask(task);

      // Check quality gate
      if (result.quality_score >= 7.0) {
        return result;
      }

      // Quality too low, retry
      console.log(`Quality ${result.quality_score} < 7.0, retrying...`);
      attempts++;

    } catch (error) {
      lastError = error;
      attempts++;
      console.log(`Attempt ${attempts} failed: ${error.message}`);
    }
  }

  return {
    ...task,
    status: "failed",
    error: lastError?.message || "Quality gate not met after retries"
  };
}
```

---

## MONITORING

During execution, track:

```javascript
const monitor = {
  plan_id: plan.plan_id,
  started_at: Date.now(),
  current_phase: 1,
  tasks_completed: 0,
  tasks_total: plan.total_tasks,
  tasks_failed: 0,
  avg_quality: 0
};

// Update after each task
function updateMonitor(result) {
  monitor.tasks_completed++;
  if (result.status === "failed") {
    monitor.tasks_failed++;
  }
  monitor.avg_quality = calculateAvgQuality(results);
}
```

---

## VALIDATION

Before passing to COLLECTOR:

1. **All phases completed** - Or error with details
2. **Quality gates passed** - avg ≥7.0
3. **Outputs exist** - Files written successfully
4. **No critical failures** - Max 10% failure rate

---

## NEXT MODULE

Pass `$spawn_results` to **HOP-40 COLLECTOR**

---

**Created**: 2025-12-02
**Depends**: Claude Code Task tool, Scout MCP
