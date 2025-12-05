# ADW-110: Single Short Generation Workflow

**Version**: 1.0.0
**Duration**: 60-120 seconds
**Phases**: 6 (Block Selection → Script → Visual → Production → Editing → Validation)
**Mode**: Standalone OR Orchestrated (callable by 200_ADW)

---

## ORCHESTRATION INTERFACE

> **CRITICAL**: This section enables composition by 200_ADW_FULL_VIDEO_PRODUCTION

```json
{
  "adw_id": "110_adw_run_shorts",
  "adw_name": "Single Short Generation",
  "agent": "video_agent",
  "version": "1.0.0",

  "orchestration": {
    "callable_by": ["200_ADW_FULL_VIDEO_PRODUCTION", "111_ADW_SHORTS_MULTI_VARIANT"],
    "spawn_compatible": true,
    "max_parallel_instances": 5,
    "isolated_execution": true,
    "consolidation_key": "short_id"
  },

  "input_contract": {
    "required": {
      "$product_brief": {
        "type": "object",
        "fields": ["produto", "objetivo", "target_audience", "key_benefit"]
      },
      "$duration_target": {
        "type": "integer",
        "enum": [15, 30, 45, 60],
        "default": 30
      },
      "$angle": {
        "type": "string",
        "enum": ["question", "problem", "curiosity", "number", "contrast", "shock", "social_proof", "howto", "mistake", "secret", "challenge", "visual"],
        "description": "Hook angle to use"
      }
    },
    "optional": {
      "$brand_profile": "object - from marca_agent",
      "$hook_override": "string - custom hook text",
      "$cta_override": "string - custom CTA text",
      "$extraction_source": "object - if extracting from long-form video",
      "$batch_id": "string - for multi-variant grouping"
    },
    "inherited": {
      "$knowledge_context": "from Phase 0 if running in orchestrated mode"
    }
  },

  "output_contract": {
    "primary_outputs": {
      "short_video": "{batch_id}/{short_id}.mp4",
      "short_metadata": "{batch_id}/{short_id}.meta.json",
      "short_llm": "{batch_id}/{short_id}.llm.json"
    },
    "chaining_data": {
      "$shorts_script": "script object for downstream",
      "$visual_prompts": "prompts array for reference",
      "$quality_score": "float 0-10",
      "$platform_variants": "if platform optimization ran"
    },
    "consolidation_manifest": {
      "short_id": "string",
      "batch_id": "string",
      "angle": "string",
      "duration": "integer",
      "quality_score": "float",
      "file_paths": "array"
    }
  },

  "failure_handling": {
    "strategy": "retry_then_skip",
    "max_retries": 2,
    "fallback": "template_based_generation",
    "report_to_orchestrator": true
  }
}
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_run_shorts",
  "workflow_name": "Single Short Generation",
  "agent": "video_agent",
  "version": "1.0.0",
  "context_strategy": "minimal_focused",
  "failure_handling": "retry_phase_then_fallback",
  "min_llm_model": "claude-sonnet-4+",
  "execution_mode": "sequential_with_parallel_clips",
  "required_capabilities": {
    "block_library": true,
    "video_generation": true,
    "tts_narration": true,
    "ffmpeg_editing": true
  },
  "phases": [
    {"phase_id": "phase_1_blocks", "phase_name": "Block Selection", "duration": "~5s", "description": "Select hook, educational, CTA blocks"},
    {"phase_id": "phase_2_script", "phase_name": "Script Generation", "duration": "~10s", "description": "Fill templates, generate narration"},
    {"phase_id": "phase_3_visual", "phase_name": "Visual Prompting", "duration": "~10s", "description": "Generate platform prompts"},
    {"phase_id": "phase_4_production", "phase_name": "Video Production", "duration": "~60s", "description": "Generate clips via API"},
    {"phase_id": "phase_5_editing", "phase_name": "Final Editing", "duration": "~15s", "description": "Assemble with audio/text"},
    {"phase_id": "phase_6_validation", "phase_name": "Validation", "duration": "~5s", "description": "Quality gates + output"}
  ]
}
```

---

## OVERVIEW

```
INPUT: Product Brief + Duration + Angle
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PHASE 1: BLOCK SELECTION (~5s)                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Hook Block  │  │ Edu Blocks  │  │ CTA Block   │          │
│  │ (by angle)  │  │ (by count)  │  │ (by goal)   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│  Output: $block_composition                                  │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PHASE 2: SCRIPT GENERATION (~10s)                           │
│  Fill templates with $product_brief data                     │
│  Generate narration + timing                                 │
│  Output: $shorts_script                                      │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PHASE 3: VISUAL PROMPTING (~10s)                            │
│  Transform script → Runway/Veo prompts                       │
│  Add camera, lighting, style                                 │
│  Output: $visual_prompts                                     │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PHASE 4: VIDEO PRODUCTION (~60s)                            │
│  Generate clips via API (parallel)                           │
│  Fallback chain: Runway → Pika → Templates                   │
│  Output: $video_clips                                        │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PHASE 5: EDITING (~15s)                                     │
│  Assemble clips + TTS + music + text overlays                │
│  Safe zones by platform                                      │
│  Output: $final_short                                        │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PHASE 6: VALIDATION (~5s)                                   │
│  Quality gates (8-point checklist)                           │
│  Trinity output generation                                   │
│  Consolidation manifest for orchestrator                     │
│  Output: short.mp4 + .meta.json + .llm.json                  │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
OUTPUT: Complete Short + Metadata + Chaining Data
```

---

## PHASE 1: BLOCK SELECTION

**Objective**: Select appropriate blocks from library based on angle and duration

**Duration**: ~5 seconds

**Config**: `config/shorts_blocks.json`

### Steps

1. **Load Block Library**
   ```python
   blocks = load_json("config/shorts_blocks.json")
   ```

2. **Select Hook by Angle**
   ```python
   hook = blocks["hooks"]["templates"].find(t => t.pattern.lower() == angle)
   if hook_override:
       hook.template = hook_override
   ```

3. **Calculate Educational Block Count**
   ```python
   assembly = blocks["assembly_rules"]["duration_formulas"][f"{duration}s"]
   edu_count = assembly["structure"].count("educational")
   ```

4. **Select Educational Blocks**
   ```python
   # Select blocks that match product context
   selected_edu = select_relevant_blocks(
       blocks["educational_blocks"]["templates"],
       product_brief,
       count=edu_count
   )
   ```

5. **Select CTA by Goal**
   ```python
   goal_to_cta = {
       "conversion": "cta_link_bio",
       "growth": "cta_subscribe",
       "urgency": "cta_urgency",
       "engagement": "cta_soft",
       "virality": "cta_challenge"
   }
   cta = blocks["cta_blocks"]["templates"].find(goal_to_cta[product_brief.objetivo])
   if cta_override:
       cta.template = cta_override
   ```

### Output → $block_composition

```json
{
  "short_id": "short_codexa_question_30s_001",
  "duration_target": 30,
  "angle": "question",
  "structure": {
    "hook": {
      "id": "hook_question",
      "template": "Voce sabia que {{ESTATISTICA}}?",
      "duration": 3
    },
    "educational": [
      {"id": "edu_tip_numbered", "template": "Dica #{{N}}: {{CONTEUDO}}", "duration": 7},
      {"id": "edu_benefit", "template": "Com {{ACAO}}, voce ganha {{BENEFICIO}}", "duration": 6},
      {"id": "edu_comparison", "template": "{{OPCAO_A}}: {{RESULTADO_A}} | {{OPCAO_B}}: {{RESULTADO_B}}", "duration": 8}
    ],
    "cta": {
      "id": "cta_value",
      "template": "{{BENEFICIO}} - teste gratis {{DURACAO}}",
      "duration": 5
    }
  },
  "total_duration": 29,
  "shot_count": 5
}
```

### Quality Gate
- [ ] Hook selected matches angle
- [ ] Educational block count matches duration formula
- [ ] CTA matches objetivo
- [ ] Total duration within ±2s of target

---

## PHASE 2: SCRIPT GENERATION

**Objective**: Fill block templates with product data, generate narration

**Duration**: ~10 seconds

**HOP Reference**: `prompts/20_script_writer_HOP.md` (adapted for Shorts)

### Steps

1. **Extract Variables from Brief**
   ```python
   variables = {
       "PRODUTO": product_brief.produto,
       "BENEFICIO": product_brief.key_benefit,
       "PROBLEMA": infer_problem(product_brief),
       "ESTATISTICA": get_relevant_stat(product_brief),
       "NUMERO": count_features(product_brief),
       "TEMA": product_brief.topic,
       # ... more extractions
   }
   ```

2. **Fill Hook Template**
   ```python
   hook_text = fill_template(block_composition.hook.template, variables)
   # "Voce sabia que 90% dos sellers pagam mais do que precisam?"
   ```

3. **Fill Educational Templates**
   ```python
   edu_texts = []
   for i, edu_block in enumerate(block_composition.educational):
       variables["N"] = i + 1
       edu_texts.append(fill_template(edu_block.template, variables))
   ```

4. **Fill CTA Template**
   ```python
   cta_text = fill_template(block_composition.cta.template, variables)
   ```

5. **Generate Narration Timing**
   ```python
   narration = []
   current_time = 0
   for segment in [hook_text] + edu_texts + [cta_text]:
       segment_duration = estimate_speech_duration(segment)
       narration.append({
           "start": current_time,
           "end": current_time + segment_duration,
           "text": segment
       })
       current_time += segment_duration
   ```

6. **Define Text Overlays**
   ```python
   text_overlays = generate_captions(narration, style="bold_impact")
   ```

### Output → $shorts_script

```json
{
  "short_id": "short_codexa_question_30s_001",
  "narration": [
    {"start": 0, "end": 3, "text": "Voce sabia que 90% dos sellers pagam mais do que precisam?", "type": "hook"},
    {"start": 3, "end": 10, "text": "Dica 1: Pesquisa de mercado com IA custa R$2, nao R$500", "type": "educational"},
    {"start": 10, "end": 16, "text": "Com automacao, voce ganha 15 horas por semana", "type": "educational"},
    {"start": 16, "end": 24, "text": "Manual: 4 horas | Automatizado: 15 minutos", "type": "educational"},
    {"start": 24, "end": 29, "text": "Economize 80% do seu tempo - teste gratis 7 dias", "type": "cta"}
  ],
  "text_overlays": [
    {"start": 0, "end": 3, "text": "90% PAGAM MAIS", "position": "center", "style": "impact"},
    {"start": 3, "end": 10, "text": "R$2 vs R$500", "position": "bottom", "style": "comparison"},
    {"start": 24, "end": 29, "text": "7 DIAS GRATIS", "position": "bottom", "style": "cta"}
  ],
  "music": {
    "track": "upbeat_short.mp3",
    "volume": 0.25
  },
  "voice_config": {
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "voice_name": "Camila",
    "style": "energetico"
  },
  "total_duration": 29
}
```

### Quality Gate
- [ ] All templates filled (no {{VARIABLE}} remaining)
- [ ] Narration fits duration ±2s
- [ ] Text overlays <= 5 words each
- [ ] Voice config valid

---

## PHASE 3: VISUAL PROMPTING

**Objective**: Generate video generation prompts for each shot

**Duration**: ~10 seconds

**HOP Reference**: `prompts/30_visual_prompter_HOP.md`

**Config**: `iso_vectorstore/15_prompt_anatomy.md`, `iso_vectorstore/18_magic_words.md`

### Steps

1. **Determine Visual Style**
   ```python
   style = map_angle_to_style(angle)
   # question → "clean, professional, data visualization"
   # shock → "dynamic, high contrast, impactful"
   ```

2. **Generate Shot Prompts**
   ```python
   prompts = []
   for i, segment in enumerate(shorts_script.narration):
       prompt = generate_video_prompt(
           description=segment.text,
           style=style,
           duration=segment.end - segment.start,
           safe_zone="bottom_20_percent",  # for text overlays
           product=product_brief.produto
       )
       prompts.append(prompt)
   ```

3. **Add Camera & Lighting**
   ```python
   for prompt in prompts:
       prompt.camera = select_camera_movement(prompt.type)
       prompt.lighting = select_lighting(style)
       prompt.magic_words = ["cinematic", "4K", "professional"]
   ```

### Output → $visual_prompts

```json
{
  "short_id": "short_codexa_question_30s_001",
  "prompts": [
    {
      "shot_number": 1,
      "type": "hook",
      "duration": 3,
      "prompt": "Professional dashboard interface showing analytics, person looking surprised at screen, clean modern office, soft blue lighting, focus on upper 80% of frame, cinematic, 4K",
      "camera": {"movement": "slow_push_in", "angle": "eye_level"},
      "lighting": "soft_professional",
      "safe_zone": "bottom_20_percent"
    },
    {
      "shot_number": 2,
      "type": "educational",
      "duration": 7,
      "prompt": "Split screen comparison: left side showing expensive consultant ($500), right side showing AI interface ($2), price tags visible, clean infographic style, motion graphics, 4K",
      "camera": {"movement": "static", "angle": "front"},
      "lighting": "bright_clean"
    }
    // ... more shots
  ],
  "style_profile": {
    "overall": "clean_professional",
    "color_palette": "blue_teal_white",
    "pacing": "fast_cuts"
  }
}
```

### Quality Gate
- [ ] All shots have prompts
- [ ] Prompts in English
- [ ] Safe zones specified
- [ ] Duration matches script

---

## PHASE 4: VIDEO PRODUCTION

**Objective**: Generate video clips via AI platform APIs

**Duration**: ~60 seconds (parallel generation)

**HOP Reference**: `prompts/40_production_runner_HOP.md`

### Steps

1. **Initialize API Connections**
   ```python
   platform = select_platform(config)  # Runway, Veo, Pika
   rate_limiter = RateLimiter(max_concurrent=3)
   ```

2. **Generate Clips (Parallel)**
   ```python
   async def generate_clips(prompts):
       tasks = []
       for prompt in prompts:
           task = generate_clip(
               platform=platform,
               prompt=prompt.prompt,
               duration=prompt.duration,
               aspect_ratio="9:16"
           )
           tasks.append(task)
       return await asyncio.gather(*tasks)
   ```

3. **Validate Clips**
   ```python
   for clip in clips:
       validate_clip(clip, min_resolution="1080x1920")
   ```

4. **Fallback on Failure**
   ```python
   failed_clips = [c for c in clips if not c.success]
   for clip in failed_clips:
       clip = retry_with_fallback(clip, fallback_chain=["pika", "template"])
   ```

### Output → $video_clips

```json
{
  "short_id": "short_codexa_question_30s_001",
  "clips": [
    {
      "shot_number": 1,
      "path": "temp/clips/shot_001.mp4",
      "duration": 3.2,
      "resolution": "1080x1920",
      "platform": "runway",
      "cost_usd": 0.15,
      "success": true
    }
    // ... more clips
  ],
  "total_cost_usd": 0.75,
  "success_rate": 1.0,
  "generation_time_seconds": 58
}
```

### Quality Gate
- [ ] All clips generated (or fallback used)
- [ ] Resolution >= 1080x1920
- [ ] Success rate >= 80%
- [ ] Cost <= $1.50

---

## PHASE 5: FINAL EDITING

**Objective**: Assemble clips with audio, text overlays, and effects

**Duration**: ~15 seconds

**HOP Reference**: `prompts/50_editor_assembler_HOP.md`

### Steps

1. **Concatenate Clips**
   ```python
   timeline = create_timeline(video_clips.clips)
   ```

2. **Generate TTS**
   ```python
   audio = generate_tts(
       text=shorts_script.narration,
       voice_id=shorts_script.voice_config.voice_id
   )
   ```

3. **Mix Audio**
   ```python
   final_audio = mix_audio(
       narration=audio,
       music=shorts_script.music.track,
       music_volume=shorts_script.music.volume
   )
   ```

4. **Add Text Overlays**
   ```python
   for overlay in shorts_script.text_overlays:
       add_text_overlay(
           timeline,
           text=overlay.text,
           position=overlay.position,
           start=overlay.start,
           end=overlay.end,
           style=overlay.style
       )
   ```

5. **Apply Safe Zones**
   ```python
   apply_safe_zones(timeline, platform="youtube_shorts")
   ```

6. **Export**
   ```python
   export_video(
       timeline,
       output_path=f"{batch_id}/{short_id}.mp4",
       codec="h264",
       quality="high"
   )
   ```

### Output → $final_short

```json
{
  "short_id": "short_codexa_question_30s_001",
  "file_path": "outputs/shorts/short_codexa_question_30s_001.mp4",
  "duration_actual": 29.4,
  "resolution": "1080x1920",
  "file_size_mb": 8.2,
  "has_audio": true,
  "has_captions": true,
  "safe_zones_applied": ["youtube_shorts"]
}
```

### Quality Gate
- [ ] Video file exists and playable
- [ ] Duration within ±1s of target
- [ ] Audio synced
- [ ] Text overlays visible
- [ ] Safe zones respected

---

## PHASE 6: VALIDATION & OUTPUT

**Objective**: Quality gates, Trinity output, consolidation manifest

**Duration**: ~5 seconds

### 8-Point Quality Checklist

```yaml
quality_checks:
  1_file_playable: "Video file exists and plays"
  2_duration_match: "Duration within ±2s of target"
  3_resolution: "Resolution >= 1080x1920"
  4_aspect_ratio: "Aspect ratio is 9:16"
  5_audio_sync: "Audio synced within 100ms"
  6_text_readable: "Text overlays visible and readable"
  7_safe_zones: "Content within safe zones"
  8_no_artifacts: "No visual glitches or artifacts"
```

### Trinity Output Generation

```python
# 1. Video file (already created)
# outputs/shorts/{batch_id}/{short_id}.mp4

# 2. LLM-readable metadata
llm_json = {
    "short_id": short_id,
    "batch_id": batch_id,
    "angle": angle,
    "duration": duration_actual,
    "hook_pattern": block_composition.hook.pattern,
    "educational_count": len(block_composition.educational),
    "cta_pattern": block_composition.cta.pattern,
    "narration_text": [n.text for n in shorts_script.narration],
    "quality_score": quality_score,
    "platforms_optimized": ["youtube_shorts"],
    "cost_usd": total_cost,
    "created_at": timestamp
}
save_json(f"{batch_id}/{short_id}.llm.json", llm_json)

# 3. Human-readable metadata
meta_json = {
    "title": generate_title(product_brief, angle),
    "description": generate_description(shorts_script),
    "duration": f"{duration_actual}s",
    "format": "9:16 vertical",
    "quality_score": f"{quality_score}/10",
    "ready_for": ["YouTube Shorts", "TikTok", "Instagram Reels"]
}
save_json(f"{batch_id}/{short_id}.meta.json", meta_json)
```

### Consolidation Manifest

> **For 200_ADW Orchestrator**: This manifest enables batch consolidation

```json
{
  "manifest_type": "short_completion",
  "short_id": "short_codexa_question_30s_001",
  "batch_id": "batch_codexa_20251205",
  "angle": "question",
  "duration": 29,
  "quality_score": 8.5,
  "status": "success",
  "file_paths": {
    "video": "outputs/shorts/batch_codexa_20251205/short_codexa_question_30s_001.mp4",
    "llm_json": "outputs/shorts/batch_codexa_20251205/short_codexa_question_30s_001.llm.json",
    "meta_json": "outputs/shorts/batch_codexa_20251205/short_codexa_question_30s_001.meta.json"
  },
  "chaining_data": {
    "$shorts_script": "...",
    "$visual_prompts": "...",
    "$quality_score": 8.5
  },
  "ready_for_consolidation": true
}
```

### Output Summary

```
outputs/shorts/{batch_id}/
├── {short_id}.mp4           # Final video
├── {short_id}.llm.json      # LLM-readable
├── {short_id}.meta.json     # Human-readable
└── {short_id}.manifest.json # For orchestrator
```

---

## USAGE

### Standalone Mode

```bash
# Via slash command
/run-short "Brief: CODEXA IA para e-commerce" --duration 30 --angle question

# Via Python
from video_agent import run_short

result = run_short(
    product_brief={"produto": "CODEXA", "objetivo": "conversion", ...},
    duration_target=30,
    angle="question"
)
```

### Orchestrated Mode (called by 200_ADW)

```python
# 200_ADW spawns this workflow
spawn_result = spawn(
    adw="110_ADW_RUN_SHORTS",
    input={
        "$product_brief": parent_brief,
        "$duration_target": 30,
        "$angle": "question",
        "$batch_id": "batch_full_production_001"
    }
)

# 200_ADW collects consolidation manifest
manifest = spawn_result.consolidation_manifest
```

### Multi-Variant Mode (called by 111_ADW)

```python
# 111_ADW spawns multiple 110_ADW instances in parallel
angles = ["question", "number", "howto", "contrast", "social_proof"]

spawn_parallel(
    adw="110_ADW_RUN_SHORTS",
    instances=[
        {"$angle": angle, "$batch_id": batch_id, ...}
        for angle in angles
    ],
    max_parallel=5
)
```

---

## ERROR HANDLING

| Phase | Error | Recovery |
|-------|-------|----------|
| Block Selection | Invalid angle | Default to "question" |
| Script | Template fill failure | Use fallback variables |
| Visual | Prompt too long | Truncate to 500 chars |
| Production | API timeout | Retry 2x, then Pika fallback |
| Production | All APIs fail | Use template video |
| Editing | FFmpeg error | Export without effects |
| Validation | Score < 7.0 | Flag for review, continue |

---

## METRICS

```json
{
  "execution_metrics": {
    "total_time_seconds": 95,
    "phase_times": {
      "block_selection": 4,
      "script": 8,
      "visual": 9,
      "production": 62,
      "editing": 10,
      "validation": 2
    }
  },
  "cost_metrics": {
    "video_generation_usd": 0.75,
    "tts_usd": 0.05,
    "total_usd": 0.80
  },
  "quality_metrics": {
    "quality_score": 8.5,
    "checks_passed": 8,
    "checks_total": 8
  }
}
```

---

## CONFIGURATION FILES

| File | Purpose |
|------|---------|
| `config/shorts_blocks.json` | Block library (hooks, edu, CTAs) |
| `config/voice_config.json` | Voice selection |
| `config/video_styles.json` | Style presets |
| `iso_vectorstore/15_prompt_anatomy.md` | Prompt structure |
| `iso_vectorstore/18_magic_words.md` | Quality enhancers |

---

## VERSION HISTORY

### v1.0.0 (2025-12-05)
- Initial implementation
- Orchestration interface for 200_ADW composition
- Block-based modular generation
- 6-phase workflow
- Trinity output + consolidation manifest
- Spawn-compatible architecture

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-05
**Status**: Production Ready
**Orchestration**: Callable by 200_ADW, spawn-compatible
