# HOP-20 | PLANNER - Decompose & Select Agents

> **Module**: PLANNER
> **Version**: 1.0.0
> **Layer**: Strategic Planning

---

## IDENTITY

```
┌─────────────────────────────────────────────────────────┐
│  PLANNER - "Eu decomponho. Eu seleciono. Eu ordeno."    │
│                                                         │
│  INPUT:  Parsed intent from LISTENER                    │
│  OUTPUT: Execution plan with phases and agents          │
│                                                         │
│  INTEGRATES: Scout smart_context, NAVIGATION_MAP        │
└─────────────────────────────────────────────────────────┘
```

---

## INPUT_CONTRACT

```yaml
$parsed_intent:
  type: object
  from: HOP-10 LISTENER
  required:
    - action
    - quantity
    - scope
    - target
    - agents_hint
```

---

## OUTPUT_CONTRACT

```yaml
$execution_plan:
  type: object
  schema:
    plan_id: string           # UUID for tracking
    action: string            # From parsed intent
    phases: array             # Ordered execution phases
      - phase_number: number
        phase_name: string
        execution_mode: string  # "sequential" or "parallel"
        tasks: array
          - agent: string
            prompt_template: string
            input_source: string
            output_destination: string
            depends_on: array   # Previous phase outputs
        estimated_time_ms: number
    total_phases: number
    total_tasks: number
    estimated_time_ms: number
    estimated_cost_usd: number
    requires_confirmation: boolean
    spawn_pattern: string     # "sequential", "parallel", "fan_out_fan_in"
```

---

## PLANNING RULES

### 1. Load Context via Scout

```javascript
// Before planning, get smart context for each agent
for (const agent of parsed_intent.agents_hint) {
  const context = await mcp__scout__smart_context({
    agent: agent,
    task: parsed_intent.action
  });

  plan.contexts[agent] = context.must_read;
}
```

### 2. Select Spawn Pattern

```yaml
Pattern Selection:
  - Sequential Pipeline: When outputs depend on previous
    Example: research → brand → photos

  - Parallel Batch: When tasks are independent
    Example: 10x anuncio_agent for 10 products

  - Fan-out/Fan-in: Mixed dependencies
    Example: parallel research → single merge → parallel execution
```

### 3. Phase Decomposition

```yaml
Decomposition Rules:
  1. Group independent tasks into same phase (parallel)
  2. Create new phase when dependency exists
  3. Final phase always: aggregate + report
  4. Quality validation between phases
```

### 4. Agent Selection Matrix

```yaml
Action → Agent Mapping:
  product_launch:
    - Phase 1: pesquisa_agent (research)
    - Phase 2: anuncio_agent (copy)
    - Phase 3: photo_agent (visuals)
    - Phase 4: collector (aggregate)

  brand_creation:
    - Phase 1: pesquisa_agent (market)
    - Phase 2: marca_agent (strategy)
    - Phase 3: photo_agent (identity)

  batch_processing:
    - Phase 1: Parallel spawn of target agent
    - Phase 2: collector (aggregate)

  course_creation:
    - Phase 1: mentor_agent (knowledge)
    - Phase 2: curso_agent (structure)
    - Phase 3: video_agent (scripts)
```

### 5. Confirmation Rules

```yaml
Requires Confirmation When:
  - quantity > 10
  - estimated_cost_usd > 5.00
  - No ADW mapped for action
  - Destructive operation detected
  - First time executing this pattern
```

---

## EXAMPLES

### Example 1: Product Launch Pipeline

```yaml
Input Intent:
  action: "product_launch"
  quantity: 10
  scope: "pipeline"
  agents_hint: ["pesquisa_agent", "anuncio_agent", "photo_agent"]

Output Plan:
  plan_id: "uuid-123"
  action: "product_launch"
  phases:
    - phase_number: 1
      phase_name: "Market Research"
      execution_mode: "parallel"
      tasks:
        - agent: "pesquisa_agent"
          prompt_template: "100_ADW_RUN_PESQUISA"
          input_source: "products_cache.json"
          output_destination: "outputs/research/"
          depends_on: []
      estimated_time_ms: 300000

    - phase_number: 2
      phase_name: "Ad Copy Generation"
      execution_mode: "parallel"
      tasks:
        - agent: "anuncio_agent"
          prompt_template: "100_ADW_RUN_ANUNCIO"
          input_source: "outputs/research/"
          output_destination: "outputs/anuncios/"
          depends_on: ["phase_1"]
      estimated_time_ms: 600000

    - phase_number: 3
      phase_name: "Photo Prompts"
      execution_mode: "parallel"
      tasks:
        - agent: "photo_agent"
          prompt_template: "100_ADW_RUN_PHOTO"
          input_source: "outputs/anuncios/"
          output_destination: "outputs/photos/"
          depends_on: ["phase_2"]
      estimated_time_ms: 300000

    - phase_number: 4
      phase_name: "Aggregate & Report"
      execution_mode: "sequential"
      tasks:
        - agent: "collector"
          prompt_template: "aggregate_results"
          input_source: "outputs/*"
          output_destination: "outputs/reports/"
          depends_on: ["phase_3"]
      estimated_time_ms: 60000

  total_phases: 4
  total_tasks: 40  # 10 products × 4 phases
  estimated_time_ms: 1260000  # ~21 min
  estimated_cost_usd: 8.50
  requires_confirmation: true  # > 10 items
  spawn_pattern: "sequential_pipeline"
```

### Example 2: Parallel Batch

```yaml
Input Intent:
  action: "ad_generation"
  quantity: 5
  scope: "batch"
  agents_hint: ["anuncio_agent"]

Output Plan:
  plan_id: "uuid-456"
  action: "ad_generation"
  phases:
    - phase_number: 1
      phase_name: "Batch Ad Generation"
      execution_mode: "parallel"
      tasks:
        - agent: "anuncio_agent"
          instances: 5
          max_concurrent: 5
          prompt_template: "100_ADW_RUN_ANUNCIO"
          input_source: "products_cache.json[0:5]"
          output_destination: "outputs/anuncios/"
          depends_on: []
      estimated_time_ms: 120000

    - phase_number: 2
      phase_name: "Aggregate & Report"
      execution_mode: "sequential"
      tasks:
        - agent: "collector"
          prompt_template: "aggregate_results"
          input_source: "outputs/anuncios/"
          output_destination: "outputs/reports/"
          depends_on: ["phase_1"]
      estimated_time_ms: 30000

  total_phases: 2
  total_tasks: 6
  estimated_time_ms: 150000  # ~2.5 min
  estimated_cost_usd: 2.00
  requires_confirmation: false  # ≤ 10 items, < $5
  spawn_pattern: "parallel_batch"
```

---

## VALIDATION

Before passing to SPAWNER:

1. **All agents exist** in NAVIGATION_MAP
2. **Dependencies are valid** - no circular deps
3. **Context loaded** for each agent
4. **Confirmation obtained** if required

---

## NEXT MODULE

Pass `$execution_plan` to **HOP-30 SPAWNER**

---

**Created**: 2025-12-02
**Depends**: NAVIGATION_MAP.json, Scout MCP
