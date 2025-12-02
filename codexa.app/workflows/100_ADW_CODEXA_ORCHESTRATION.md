# ADW-100 | CODEXA.app Orchestration Workflow

> **Version**: 1.0.0
> **Type**: Primary Orchestration
> **Status**: ACTIVE

---

## OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ADW-100: CODEXA.app ORCHESTRATION                         │
│                                                                              │
│  4-Phase workflow for natural language → execution → report                 │
│                                                                              │
│  LISTEN ──▶ PLAN ──▶ SPAWN ──▶ COLLECT                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: LISTEN

**HOP**: `prompts/10_listener_HOP.md`
**Duration**: ~5 seconds

### Input
```yaml
$user_input: string  # Natural language or voice transcription
$voice_mode: boolean # Whether from voice
```

### Process
1. Parse natural language intent
2. Extract action, quantity, scope, target
3. Match keywords to agents via NAVIGATION_MAP
4. Parse flags (--dry-run, --auto, --voice, etc.)

### Output
```yaml
$parsed_intent:
  action: string
  quantity: number
  scope: string
  target: string
  agents_hint: array
  flags: object
  confidence: number
```

### Quality Gate
- Confidence ≥ 0.7 to proceed
- If < 0.7, ask user for clarification

---

## PHASE 2: PLAN

**HOP**: `prompts/20_planner_HOP.md`
**Duration**: ~10 seconds

### Input
```yaml
$parsed_intent: object  # From Phase 1
```

### Process
1. Load NAVIGATION_MAP.json
2. Query Scout MCP for agent contexts
3. Select spawn pattern (sequential, parallel, fan-out)
4. Decompose into phases and tasks
5. Estimate time and cost
6. Determine if confirmation needed

### Output
```yaml
$execution_plan:
  plan_id: string
  phases: array
  total_tasks: number
  estimated_time_ms: number
  estimated_cost_usd: number
  requires_confirmation: boolean
  spawn_pattern: string
```

### Quality Gate
- All agents must exist
- No circular dependencies
- Valid spawn pattern

### Confirmation Point
If `requires_confirmation: true`:
- Display plan to user
- Wait for Y/n confirmation
- If N: Exit workflow
- If --auto flag: Skip confirmation

---

## PHASE 3: SPAWN

**HOP**: `prompts/30_spawner_HOP.md`
**Duration**: Variable (depends on tasks)

### Input
```yaml
$execution_plan: object  # From Phase 2
```

### Process
1. For each phase in plan:
   a. Load agent contexts via Scout
   b. Build agent prompts
   c. Spawn via Task tool (parallel or sequential)
   d. Monitor progress
   e. Apply retry logic if quality < 7.0
2. Collect results from all tasks

### Output
```yaml
$spawn_results:
  plan_id: string
  results: array
    - task_id: string
      agent: string
      status: string
      quality_score: number
      output_file: string
  aggregated_quality: number
  total_time_ms: number
```

### Quality Gates
- Per-task: quality_score ≥ 7.0
- Retry up to 1x if failed
- Phase fails if > 50% tasks fail

### Parallel Execution
```javascript
// Example: 5 concurrent tasks
Task.parallel([
  Task(pesquisa_agent, product_1),
  Task(pesquisa_agent, product_2),
  Task(pesquisa_agent, product_3),
  Task(pesquisa_agent, product_4),
  Task(pesquisa_agent, product_5)
], { max_concurrent: 5 });
```

---

## PHASE 4: COLLECT

**HOP**: `prompts/40_collector_HOP.md`
**Duration**: ~30 seconds

### Input
```yaml
$spawn_results: object  # From Phase 3
```

### Process
1. Aggregate all task results
2. Consolidate outputs by agent and phase
3. Generate summary (success/partial/failed)
4. Create markdown report
5. Save JSON report
6. Generate voice summary if --voice
7. Suggest next steps

### Output
```yaml
$final_report:
  plan_id: string
  status: string
  summary: string
  metrics: object
  outputs:
    files: array
    reports: string
  voice_report: string
  next_steps: array
```

### Deliverables
1. **Console output**: Summary and next steps
2. **Voice output**: Spoken summary (if --voice)
3. **Report file**: `outputs/reports/{plan_id}_report.md`
4. **JSON data**: `outputs/reports/{plan_id}_report.json`
5. **Archived outputs**: `outputs/batch_{date}/`

---

## COMPLETE FLOW

```
                    ┌────────────────────────┐
                    │   USER INPUT (NL)      │
                    │   "Lance 10 produtos"  │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   PHASE 1: LISTEN      │
                    │   Parse intent         │
                    │   Extract agents       │
                    └───────────┬────────────┘
                                │ $parsed_intent
                    ┌───────────▼────────────┐
                    │   PHASE 2: PLAN        │
                    │   Scout context        │
                    │   Build phases         │
                    └───────────┬────────────┘
                                │ $execution_plan
                    ┌───────────▼────────────┐
                    │   CONFIRMATION?        │
                    │   (if required)        │
                    └───────────┬────────────┘
                                │ Y
                    ┌───────────▼────────────┐
                    │   PHASE 3: SPAWN       │
                    │   Task() parallel      │
                    │   Monitor + retry      │
                    └───────────┬────────────┘
                                │ $spawn_results
                    ┌───────────▼────────────┐
                    │   PHASE 4: COLLECT     │
                    │   Aggregate results    │
                    │   Generate report      │
                    │   Voice summary        │
                    └───────────┬────────────┘
                                │ $final_report
                    ┌───────────▼────────────┐
                    │   USER OUTPUT          │
                    │   Report + Voice       │
                    │   Next steps           │
                    └────────────────────────┘
```

---

## EXAMPLE EXECUTION

### Input
```
/codexa "Lance os 10 produtos do catálogo com pesquisa e fotos"
```

### Phase 1 Output
```yaml
$parsed_intent:
  action: "product_launch"
  quantity: 10
  scope: "pipeline"
  target: "produtos do catálogo"
  agents_hint: ["pesquisa_agent", "anuncio_agent", "photo_agent"]
  flags: {}
  confidence: 0.95
```

### Phase 2 Output
```yaml
$execution_plan:
  plan_id: "uuid-2024-12-02-001"
  phases:
    - phase: 1, name: "Research", mode: "parallel", agent: "pesquisa_agent"
    - phase: 2, name: "Ad Copy", mode: "parallel", agent: "anuncio_agent"
    - phase: 3, name: "Photos", mode: "parallel", agent: "photo_agent"
    - phase: 4, name: "Collect", mode: "sequential", agent: "collector"
  total_tasks: 31
  estimated_time_ms: 1260000
  estimated_cost_usd: 8.50
  requires_confirmation: true
  spawn_pattern: "sequential_pipeline"
```

### Confirmation Prompt
```
## CODEXA.app - Plano de Execução

### Entendimento
Lançar 10 produtos com pesquisa de mercado e geração de fotos.

### Fases
1. Research: 10× pesquisa_agent (parallel)
2. Ad Copy: 10× anuncio_agent (parallel)
3. Photos: 10× photo_agent (parallel)
4. Collect: Agregar resultados

### Estimativas
- Tempo: ~21min
- Tasks: 31
- Custo: ~$8.50

Confirmar execução? [Y/n]
```

### Phase 3 Progress
```
[Phase 1/4] Research...
  ✓ pesquisa_agent (1/10) - 8.2/10
  ✓ pesquisa_agent (2/10) - 8.5/10
  ...
  ✓ pesquisa_agent (10/10) - 8.0/10
[Phase 2/4] Ad Copy...
  ✓ anuncio_agent (1/10) - 8.7/10
  ...
```

### Phase 4 Output
```yaml
$final_report:
  status: "success"
  summary: "Executado product_launch: 30/30 tarefas completadas. Qualidade média: 8.4/10."
  metrics:
    completed: 30
    failed: 0
    avg_quality: 8.4
  voice_report: "Pronto! 30 tarefas completadas em 21 minutos. Qualidade 8.4 de 10. Sem falhas."
  next_steps:
    - "Revisar anúncios em outputs/anuncios/"
    - "Publicar com /codexa \"Publique anúncios aprovados\""
```

---

## INTEGRATION POINTS

### Scout MCP
```javascript
// Phase 2: Get context for agents
const ctx = await mcp__scout__smart_context({ agent, task });
```

### Voice
```javascript
// Phase 1: STT input
const text = await voice.stt.transcribe(audio);

// Phase 4: TTS output
await voice.tts.speak(report.voice_report);
```

### Task Tool
```javascript
// Phase 3: Spawn agents
await Task({
  subagent_type: "general-purpose",
  description: `${agent} - ${task}`,
  prompt: buildPrompt(agent, context, input)
});
```

---

## ERROR HANDLING

| Error | Phase | Action |
|-------|-------|--------|
| Low confidence | 1 | Ask user for clarification |
| Agent not found | 2 | Error with suggestion |
| Task failed | 3 | Retry 1x, then log failure |
| Quality < 7.0 | 3 | Retry 1x |
| > 50% failures | 3 | Abort phase, partial report |
| Voice unavailable | 4 | Skip voice, text only |

---

## METRICS

Track per execution:
- `total_time_ms`
- `tasks_completed`
- `tasks_failed`
- `avg_quality_score`
- `retries_count`
- `phases_completed`

---

**Created**: 2025-12-02
**Depends**: HOP-10, HOP-20, HOP-30, HOP-40, Scout MCP, Voice
