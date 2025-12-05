# ADW-111: Multi-Variant Shorts Generation (Parallel Orchestration)

**Version**: 1.0.0
**Duration**: 90-180 seconds (parallel execution)
**Pattern**: 1 Brief → N Shorts (spawn-based parallelism)
**Mode**: Standalone OR Orchestrated (callable by 200_ADW)

---

## ORCHESTRATION INTERFACE

> **CRITICAL**: Spawn-based parallel execution pattern - reusable by 200_ADW

```json
{
  "adw_id": "111_adw_shorts_multi_variant",
  "adw_name": "Multi-Variant Shorts Generation",
  "agent": "video_agent",
  "version": "1.0.0",

  "orchestration": {
    "callable_by": ["200_ADW_FULL_VIDEO_PRODUCTION"],
    "calls": ["110_ADW_RUN_SHORTS"],
    "spawn_pattern": "parallel_fan_out",
    "max_parallel_instances": 5,
    "consolidation_pattern": "merge_to_batch"
  },

  "input_contract": {
    "required": {
      "$product_brief": {
        "type": "object",
        "fields": ["produto", "objetivo", "target_audience", "key_benefit"]
      },
      "$variant_count": {
        "type": "integer",
        "min": 1,
        "max": 10,
        "default": 5
      }
    },
    "optional": {
      "$angles": {
        "type": "array",
        "description": "Specific angles to generate. If not provided, auto-selects best N angles"
      },
      "$duration_target": {
        "type": "integer",
        "enum": [15, 30, 45, 60],
        "default": 30
      },
      "$brand_profile": "object - from marca_agent",
      "$extraction_source": "object - if extracting from long-form video",
      "$batch_id": "string - override batch ID"
    }
  },

  "output_contract": {
    "primary_outputs": {
      "batch_directory": "outputs/shorts/{batch_id}/",
      "batch_manifest": "outputs/shorts/{batch_id}/BATCH_MANIFEST.json",
      "batch_report": "outputs/shorts/{batch_id}/BATCH_REPORT.md",
      "consolidated_llm": "outputs/shorts/{batch_id}/ALL_SHORTS.llm.json"
    },
    "individual_outputs": {
      "per_short": "{batch_id}/{short_id}.mp4 + .llm.json + .meta.json"
    },
    "chaining_data": {
      "$batch_manifest": "array of short manifests",
      "$best_performer": "short with highest predicted engagement",
      "$total_cost": "sum of all generation costs"
    }
  }
}
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_shorts_multi_variant",
  "workflow_name": "Multi-Variant Shorts Generation",
  "agent": "video_agent",
  "version": "1.0.0",
  "execution_mode": "parallel_spawn",
  "spawn_config": {
    "target_adw": "110_ADW_RUN_SHORTS",
    "max_parallel": 5,
    "timeout_per_instance": 180000,
    "failure_mode": "continue_on_partial"
  },
  "phases": [
    {"phase_id": "phase_1_plan", "phase_name": "Variant Planning", "duration": "~5s", "parallel": false},
    {"phase_id": "phase_2_spawn", "phase_name": "Parallel Generation", "duration": "~90s", "parallel": true},
    {"phase_id": "phase_3_collect", "phase_name": "Result Collection", "duration": "~5s", "parallel": false},
    {"phase_id": "phase_4_consolidate", "phase_name": "Batch Consolidation", "duration": "~10s", "parallel": false}
  ]
}
```

---

## OVERVIEW

```
INPUT: 1 Product Brief + N Variants
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: VARIANT PLANNING (~5s)                                             │
│  Select N angles based on product type and objetivo                          │
│  Generate batch_id and spawn configuration                                   │
│  Output: $spawn_plan                                                         │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: PARALLEL GENERATION via /spawn (~90s)                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  /spawn (max 5 parallel)                                                │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │ │
│  │  │110_ADW   │ │110_ADW   │ │110_ADW   │ │110_ADW   │ │110_ADW   │      │ │
│  │  │question  │ │number    │ │howto     │ │contrast  │ │social    │      │ │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │ │
│  │       │            │            │            │            │             │ │
│  │       ▼            ▼            ▼            ▼            ▼             │ │
│  │  short_01.mp4 short_02.mp4 short_03.mp4 short_04.mp4 short_05.mp4      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│  Output: N individual short manifests                                        │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: RESULT COLLECTION (~5s)                                            │
│  Collect all spawn results                                                   │
│  Validate success rate                                                       │
│  Handle partial failures                                                     │
│  Output: $spawn_results                                                      │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: BATCH CONSOLIDATION (~10s)                                         │
│  Generate unified batch manifest                                             │
│  Create human-readable report                                                │
│  Create LLM-optimized consolidated JSON                                      │
│  Identify best performer                                                     │
│  Output: Batch directory with all outputs + reports                          │
└──────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
OUTPUT: Complete Batch Package
        outputs/shorts/{batch_id}/
        ├── short_01.mp4, .llm.json, .meta.json
        ├── short_02.mp4, .llm.json, .meta.json
        ├── ... (N shorts)
        ├── BATCH_MANIFEST.json    (orchestrator-readable)
        ├── BATCH_REPORT.md        (human-readable summary)
        └── ALL_SHORTS.llm.json    (LLM-optimized consolidated)
```

---

## PHASE 1: VARIANT PLANNING

**Objective**: Select optimal angles and configure spawn plan

**Duration**: ~5 seconds

### Angle Selection Strategy

```python
# Angle performance by product type
ANGLE_PERFORMANCE = {
    "educational": {
        "best": ["number", "howto", "mistake", "secret"],
        "good": ["question", "curiosity"],
        "avoid": ["challenge", "visual"]
    },
    "product": {
        "best": ["contrast", "social_proof", "benefit"],
        "good": ["question", "shock"],
        "avoid": ["challenge"]
    },
    "service": {
        "best": ["howto", "social_proof", "problem"],
        "good": ["question", "number"],
        "avoid": ["visual"]
    },
    "entertainment": {
        "best": ["curiosity", "challenge", "shock"],
        "good": ["visual", "contrast"],
        "avoid": ["howto"]
    }
}

def select_angles(product_brief, variant_count, custom_angles=None):
    if custom_angles:
        return custom_angles[:variant_count]

    product_type = classify_product(product_brief)
    performance = ANGLE_PERFORMANCE[product_type]

    # Select best angles first, then good
    selected = performance["best"][:variant_count]
    if len(selected) < variant_count:
        selected += performance["good"][:variant_count - len(selected)]

    return selected[:variant_count]
```

### Spawn Plan Generation

```python
def generate_spawn_plan(product_brief, angles, duration_target, batch_id=None):
    batch_id = batch_id or f"batch_{product_brief.produto}_{timestamp()}"

    spawn_plan = {
        "batch_id": batch_id,
        "variant_count": len(angles),
        "duration_target": duration_target,
        "spawn_instances": []
    }

    for i, angle in enumerate(angles):
        instance = {
            "instance_id": f"spawn_{i+1}",
            "short_id": f"short_{product_brief.produto}_{angle}_{duration_target}s_{i+1:03d}",
            "adw": "110_ADW_RUN_SHORTS",
            "input": {
                "$product_brief": product_brief,
                "$duration_target": duration_target,
                "$angle": angle,
                "$batch_id": batch_id
            }
        }
        spawn_plan["spawn_instances"].append(instance)

    return spawn_plan
```

### Output → $spawn_plan

```json
{
  "batch_id": "batch_codexa_20251205_143022",
  "variant_count": 5,
  "duration_target": 30,
  "product_type": "service",
  "angles_selected": ["howto", "social_proof", "problem", "question", "number"],
  "spawn_instances": [
    {
      "instance_id": "spawn_1",
      "short_id": "short_codexa_howto_30s_001",
      "adw": "110_ADW_RUN_SHORTS",
      "input": {
        "$product_brief": {...},
        "$duration_target": 30,
        "$angle": "howto",
        "$batch_id": "batch_codexa_20251205_143022"
      }
    },
    // ... 4 more instances
  ],
  "estimated_time_seconds": 95,
  "estimated_cost_usd": 4.00
}
```

---

## PHASE 2: PARALLEL GENERATION (/spawn)

**Objective**: Execute N instances of 110_ADW in parallel

**Duration**: ~90 seconds (limited by slowest instance)

### Spawn Execution Pattern

```markdown
## /spawn Command

Execute 5 parallel agents for shorts generation:

/spawn
1. video_agent: Generate short with "howto" angle for CODEXA brief (30s)
2. video_agent: Generate short with "social_proof" angle for CODEXA brief (30s)
3. video_agent: Generate short with "problem" angle for CODEXA brief (30s)
4. video_agent: Generate short with "question" angle for CODEXA brief (30s)
5. video_agent: Generate short with "number" angle for CODEXA brief (30s)
```

### Implementation (Programmatic)

```python
async def spawn_shorts_generation(spawn_plan):
    """
    Execute parallel shorts generation using spawn pattern.

    This is the core parallel execution that 200_ADW will also use.
    """

    # Configure spawn
    spawn_config = {
        "max_parallel": min(5, spawn_plan["variant_count"]),
        "timeout_ms": 180000,  # 3 minutes per instance
        "failure_mode": "continue_on_partial",
        "consolidation_key": "short_id"
    }

    # Launch all instances
    tasks = []
    for instance in spawn_plan["spawn_instances"]:
        task = launch_adw(
            adw_id=instance["adw"],
            input_data=instance["input"],
            instance_id=instance["instance_id"]
        )
        tasks.append(task)

    # Wait for all to complete (or timeout)
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    spawn_results = []
    for i, result in enumerate(results):
        instance = spawn_plan["spawn_instances"][i]

        if isinstance(result, Exception):
            spawn_results.append({
                "instance_id": instance["instance_id"],
                "short_id": instance["short_id"],
                "status": "failed",
                "error": str(result)
            })
        else:
            spawn_results.append({
                "instance_id": instance["instance_id"],
                "short_id": instance["short_id"],
                "status": "success",
                "manifest": result["consolidation_manifest"],
                "quality_score": result["quality_score"]
            })

    return spawn_results
```

### Progress Tracking

```
[spawn_1] 110_ADW_RUN_SHORTS (howto)      ████████████████████ 100% - 92s - Score: 8.7
[spawn_2] 110_ADW_RUN_SHORTS (social)     ████████████████████ 100% - 88s - Score: 8.4
[spawn_3] 110_ADW_RUN_SHORTS (problem)    ████████████████████ 100% - 95s - Score: 8.2
[spawn_4] 110_ADW_RUN_SHORTS (question)   ████████████████████ 100% - 91s - Score: 8.5
[spawn_5] 110_ADW_RUN_SHORTS (number)     ████████████████████ 100% - 89s - Score: 8.9

Total: 5/5 completed | Max time: 95s | Avg score: 8.54
```

### Output → $spawn_results

```json
{
  "batch_id": "batch_codexa_20251205_143022",
  "spawn_completed": 5,
  "spawn_failed": 0,
  "total_time_seconds": 95,
  "results": [
    {
      "instance_id": "spawn_1",
      "short_id": "short_codexa_howto_30s_001",
      "status": "success",
      "angle": "howto",
      "quality_score": 8.7,
      "file_path": "outputs/shorts/batch_codexa_20251205_143022/short_codexa_howto_30s_001.mp4",
      "cost_usd": 0.82
    },
    // ... 4 more results
  ],
  "total_cost_usd": 4.05
}
```

---

## PHASE 3: RESULT COLLECTION

**Objective**: Collect and validate all spawn results

**Duration**: ~5 seconds

### Steps

1. **Collect All Manifests**
   ```python
   manifests = []
   for result in spawn_results["results"]:
       if result["status"] == "success":
           manifest_path = f"{batch_dir}/{result['short_id']}.manifest.json"
           manifests.append(load_json(manifest_path))
   ```

2. **Validate Success Rate**
   ```python
   success_count = len([r for r in spawn_results["results"] if r["status"] == "success"])
   success_rate = success_count / spawn_plan["variant_count"]

   if success_rate < 0.6:  # Less than 60% success
       raise PartialFailureError(f"Only {success_rate*100}% shorts generated")
   ```

3. **Handle Partial Failures**
   ```python
   failed = [r for r in spawn_results["results"] if r["status"] == "failed"]
   for failure in failed:
       log_error(f"Short {failure['short_id']} failed: {failure['error']}")
       # Continue with successful shorts - don't block batch
   ```

4. **Rank by Quality**
   ```python
   successful = [r for r in spawn_results["results"] if r["status"] == "success"]
   ranked = sorted(successful, key=lambda x: x["quality_score"], reverse=True)
   best_performer = ranked[0]
   ```

---

## PHASE 4: BATCH CONSOLIDATION

**Objective**: Create unified batch package with all outputs

**Duration**: ~10 seconds

### Output Structure

```
outputs/shorts/{batch_id}/
│
├── videos/
│   ├── short_codexa_howto_30s_001.mp4
│   ├── short_codexa_social_30s_002.mp4
│   ├── short_codexa_problem_30s_003.mp4
│   ├── short_codexa_question_30s_004.mp4
│   └── short_codexa_number_30s_005.mp4
│
├── metadata/
│   ├── short_codexa_howto_30s_001.llm.json
│   ├── short_codexa_howto_30s_001.meta.json
│   └── ... (all individual metadata)
│
├── BATCH_MANIFEST.json      # Orchestrator-readable
├── BATCH_REPORT.md          # Human-readable summary
├── ALL_SHORTS.llm.json      # LLM-optimized consolidated
└── README.md                # Quick navigation guide
```

### BATCH_MANIFEST.json (For Orchestrator)

```json
{
  "manifest_version": "1.0.0",
  "manifest_type": "shorts_batch",
  "batch_id": "batch_codexa_20251205_143022",
  "created_at": "2025-12-05T14:30:22Z",

  "summary": {
    "total_shorts": 5,
    "successful": 5,
    "failed": 0,
    "success_rate": 1.0,
    "total_duration_seconds": 147,
    "total_cost_usd": 4.05,
    "avg_quality_score": 8.54
  },

  "shorts": [
    {
      "short_id": "short_codexa_howto_30s_001",
      "angle": "howto",
      "duration": 29,
      "quality_score": 8.7,
      "predicted_engagement": "high",
      "files": {
        "video": "videos/short_codexa_howto_30s_001.mp4",
        "llm_json": "metadata/short_codexa_howto_30s_001.llm.json",
        "meta_json": "metadata/short_codexa_howto_30s_001.meta.json"
      }
    },
    // ... 4 more shorts
  ],

  "best_performer": {
    "short_id": "short_codexa_number_30s_005",
    "angle": "number",
    "quality_score": 8.9,
    "reason": "Highest CTR multiplier (1.36x) + highest quality score"
  },

  "chaining_data": {
    "$batch_manifest": "self",
    "$best_performer": "short_codexa_number_30s_005",
    "$all_short_ids": ["short_codexa_howto_30s_001", ...],
    "$total_cost": 4.05
  },

  "ready_for": {
    "platform_optimization": true,
    "cross_post_scheduling": true,
    "200_adw_consolidation": true
  }
}
```

### BATCH_REPORT.md (For Humans)

```markdown
# Shorts Batch Report

**Batch ID**: batch_codexa_20251205_143022
**Generated**: 2025-12-05 14:30:22
**Product**: CODEXA - IA para E-commerce

---

## Summary

| Metric | Value |
|--------|-------|
| Total Shorts | 5 |
| Success Rate | 100% |
| Total Time | 95 seconds |
| Total Cost | $4.05 |
| Avg Quality | 8.54/10 |

---

## Shorts Generated

| # | Angle | Duration | Score | Engagement |
|---|-------|----------|-------|------------|
| 1 | howto | 29s | 8.7 | High |
| 2 | social_proof | 30s | 8.4 | Medium |
| 3 | problem | 29s | 8.2 | Medium |
| 4 | question | 30s | 8.5 | High |
| 5 | number | 29s | **8.9** | **Highest** |

---

## Best Performer

**short_codexa_number_30s_005** (Number angle)
- Quality Score: 8.9/10
- CTR Multiplier: 1.36x
- Recommended for: First publish, A/B test control

---

## Quick Actions

- [ ] Review best performer
- [ ] Run platform optimization (/platform-optimize)
- [ ] Schedule cross-posting (/cross-post-schedule)
- [ ] Publish to YouTube Shorts

---

## Files

All shorts available in: `outputs/shorts/batch_codexa_20251205_143022/`
```

### ALL_SHORTS.llm.json (For LLM Processing)

```json
{
  "format": "llm_optimized",
  "version": "1.0.0",
  "batch_id": "batch_codexa_20251205_143022",

  "quick_reference": {
    "total": 5,
    "best": "short_codexa_number_30s_005",
    "avg_score": 8.54
  },

  "shorts": [
    {
      "id": "short_codexa_number_30s_005",
      "angle": "number",
      "score": 8.9,
      "hook": "5 razoes para automatizar seu e-commerce",
      "narration_summary": "Lists 5 benefits of automation with specific stats",
      "cta": "Link na bio - teste gratis 7 dias",
      "video_path": "videos/short_codexa_number_30s_005.mp4"
    },
    // ... more shorts (sorted by score)
  ],

  "usage_hints": {
    "for_platform_optimization": "Pass batch_id to 72_platform_optimizer_HOP",
    "for_scheduling": "Use cross_post_schedule endpoint",
    "for_200_adw": "Include in consolidation phase"
  }
}
```

---

## USAGE

### Standalone Mode

```bash
# Via slash command
/shorts-batch "Brief: CODEXA IA para e-commerce" --variants 5 --duration 30

# With specific angles
/shorts-batch "Brief: CODEXA" --angles question,number,howto --duration 30
```

### Orchestrated Mode (called by 200_ADW)

```python
# 200_ADW calls this workflow as part of full production
spawn_result = await execute_adw(
    adw="111_ADW_SHORTS_MULTI_VARIANT",
    input={
        "$product_brief": parent_brief,
        "$variant_count": 5,
        "$duration_target": 30,
        "$batch_id": f"{production_batch_id}_shorts"
    }
)

# 200_ADW receives consolidated batch manifest
batch_manifest = spawn_result["chaining_data"]["$batch_manifest"]
```

### Spawn Command (Direct)

```markdown
/spawn preset:shorts_batch
Brief: CODEXA - Sistema de IA para vendedores de e-commerce
Variants: 5
Duration: 30s
Angles: auto (best for service product)
```

---

## ERROR HANDLING

| Scenario | Handling |
|----------|----------|
| 1 instance fails | Continue with others, mark failed in manifest |
| >40% fail | Abort batch, return partial results |
| All fail | Retry batch once, then escalate |
| Timeout | Use partial results if >50% complete |
| Cost overrun | Stop spawning, consolidate what exists |

---

## METRICS

```json
{
  "batch_metrics": {
    "total_time_seconds": 95,
    "parallel_efficiency": 0.85,
    "spawn_overhead_seconds": 5,
    "consolidation_seconds": 8
  },
  "cost_metrics": {
    "per_short_avg_usd": 0.81,
    "total_usd": 4.05,
    "cost_vs_sequential": "-75%"
  },
  "quality_metrics": {
    "avg_score": 8.54,
    "min_score": 8.2,
    "max_score": 8.9,
    "std_dev": 0.26
  },
  "efficiency_vs_sequential": {
    "sequential_time_estimate": 475,
    "actual_time": 95,
    "speedup_factor": "5x"
  }
}
```

---

## CONFIGURATION

### Spawn Limits

```json
{
  "max_parallel_default": 5,
  "max_parallel_absolute": 10,
  "timeout_per_instance_ms": 180000,
  "batch_timeout_ms": 600000
}
```

### Cost Controls

```json
{
  "max_cost_per_short_usd": 1.50,
  "max_batch_cost_usd": 15.00,
  "cost_alert_threshold_usd": 10.00
}
```

---

## INTEGRATION WITH 200_ADW

This ADW is designed to be called by `200_ADW_FULL_VIDEO_PRODUCTION`:

```
200_ADW orchestration:
│
├── Stage A: 100_ADW_RUN_VIDEO (long-form)
│
├── Stage B: 105_ADW_YOUTUBE_FULL_METADATA (metadata)
│
├── Stage C: [111_ADW_SHORTS_MULTI_VARIANT] ← THIS ADW
│   └── Spawns 5x 110_ADW_RUN_SHORTS
│
├── Stage D: 72_platform_optimizer_HOP (for each short)
│
└── Stage E: Consolidation (merge all outputs)
```

The spawn pattern used here is the **same pattern** that 200_ADW uses for its own multi-stage parallelization.

---

## VERSION HISTORY

### v1.0.0 (2025-12-05)
- Initial implementation
- Spawn-based parallel generation
- Batch consolidation with unified outputs
- Integration interface for 200_ADW
- Quality ranking and best performer identification
- Human + LLM optimized output formats

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-05
**Status**: Production Ready
**Orchestration**: Callable by 200_ADW, uses spawn pattern
**Calls**: 110_ADW_RUN_SHORTS (N instances parallel)
