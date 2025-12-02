# INSTRUCTIONS | video_agent

**Version**: 2.5.0
**Purpose**: Instructions for AI assistants / Agent builders to use video_agent
**Type**: HOP (Higher-Order Prompt) for LLM execution
**Updated**: 2025-11-25

---

## CORE PURPOSE

`video_agent` transforms product briefs into professional AI-generated e-commerce videos (15-60s) using a 7-phase pipeline with multiple AI video APIs, optimized for Instagram Reels, TikTok, and YouTube Shorts.

**Use this agent when**: You need to create product videos for social media at scale with minimal human intervention.

**Output**: Final MP4 video + Trinity metadata (.md, .llm.json, .meta.json)

---

## 12 LEVERAGE POINTS IMPLEMENTATION

### 4 IN-AGENT Pillars (Internal Construction)

**1. Context**: E-commerce video production for Brazilian market
- Product briefs, brand guidelines, platform requirements
- Social media video best practices (hooks, CTAs, pacing)
- Mental checklist in 01_QUICK_START.md

**2. Model**: Claude Sonnet 4 (reasoning) + Claude Haiku (validation)
- Concept and script: extended reasoning for narrative structure
- Prompt engineering and validation: fast model for throughput

**3. Tools**: Mode-aware builders (overlay/clean)
- FFmpeg, Runway Gen-3, Pika 1.5, ElevenLabs TTS
- Video generation APIs (async, parallel)
- Local video processing (concatenation, audio mixing, text overlays)

**4. Prompts**: 5 HOPs (one per pipeline stage) in TAC-7 format
- 10_concept_planner_HOP.md (storyboard)
- 20_script_writer_HOP.md (narration)
- 30_visual_prompter_HOP.md (platform prompts)
- 40_production_runner_HOP.md (API orchestration)
- 50_editor_assembler_HOP.md (FFmpeg editing)

### 8 OUT-AGENT Pillars (External Artifacts)

**5. Standard Output**: Trinity format + Task Boundaries
- .mp4 (video) + .llm.json (structured) + .meta.json (metadata)
- Task boundary pattern: `PHASE [N]: [NAME] | [STATUS]`

**6. Types**: JSON schemas for pipeline data flow
- 06_input_schema.json, 08_video_rules.json
- 09_platform_specs.json, 10_production_patterns.json
- 12_execution_plans.json

**7. Documentation**: Complete (01-05, 20)
- QUICK_START, PRIME, INSTRUCTIONS, README, SETUP, CHANGELOG

**8. Tests**: Quality validators per stage
- 11-point validation checklist
- video_quality_validator.py, schema_validator.py

**9. Architecture**: Dual-Layer ADW+HOP
- 5 builders (builders/), 5 HOPs (prompts/)
- config/ (styles, APIs, voices, modes)

**10. Plans**: 12_execution_plans.json
- Full, Quick, Batch, Campaign plans

**11. Templates**: 07_output_template.md
- Trinity output specification

**12. ADWs**: 11_ADW_orchestrator.md
- 7-phase workflow with task boundaries

---

## AI ASSISTANT INSTRUCTIONS

**IMPORTANT**: Execute the ADW workflow with task boundaries.

### Discovery-First Workflow

**Pattern**: Read ADW -> Select Plan -> Follow phases -> Validate outputs

```bash
# 1. SCAN: Understand pipeline
READ: iso_vectorstore/11_ADW_orchestrator.md
READ: iso_vectorstore/12_execution_plans.json

# 2. SELECT PLAN: Choose execution plan
PLAN: full | quick | batch | campaign

# 3. EXECUTE: Run with task boundaries
PHASE 0: PRE-FLIGHT | STARTING
PHASE 1: CONCEPT | IN_PROGRESS
...
PHASE 6: VALIDATION | COMPLETE

# 4. VERIFY: Check outputs
CHECK: Trinity output (.mp4, .llm.json, .meta.json)
VALIDATE: quality_score >= 7.0
```

### Task Boundary Pattern

Always announce phase transitions:
```
PHASE [N]: [NAME] | [STATUS] - [Detail]

Example:
PHASE 0: PRE-FLIGHT | STARTING - Validating brief
PHASE 1: CONCEPT | IN_PROGRESS - Generating 6-shot storyboard
PHASE 2: SCRIPT | COMPLETE - Mode: overlay, Voice: Camila
PHASE 4: PRODUCTION | IN_PROGRESS - Clip 3/6
PHASE 6: VALIDATION | COMPLETE - Score: 8.5/10
```

### When to Use

**USE this agent for**:
- Product demo videos (15-60s)
- Instagram Reels / TikTok / YouTube Shorts
- E-commerce product showcases
- Brand campaign videos
- Social media content at scale

**DO NOT use for**:
- Static images (use photo_agent)
- Long-form content (>60 seconds)
- Videos requiring human actors
- Complex VFX or motion graphics
- Real-time editing or live processing

### Execution Plans

| Plan | Use Case | Phases |
|------|----------|--------|
| **full** | Production delivery | All 7 phases |
| **quick** | Draft/testing | 5 phases (no video gen) |
| **batch** | Product catalog | Parallel processing |
| **campaign** | Multi-format | 6 output variants |

---

## WORKFLOW (7 Phases)

```
INPUT: Video Brief
    |
    v
[PHASE 0: PRE-FLIGHT] --> config.json
    | (~2s)                 video_mode, voice_id, platform
    v
[PHASE 1: CONCEPT] ------> concept.json
    | (~5s)                 6-8 shots with narrative arc
    v
[PHASE 2: SCRIPT] -------> script.json
    | (~3s)                 narration + text overlays (mode-aware)
    v
[PHASE 3: VISUAL] -------> visual_prompts.json
    | (~10s)                Platform prompts (mode-aware)
    v
[PHASE 4: PRODUCTION] ---> clips/*.mp4
    | (120-300s async)      Parallel video generation
    v
[PHASE 5: EDITING] ------> final_video.mp4
    | (~15s)                FFmpeg assembly + TTS + text
    v
[PHASE 6: VALIDATION] ---> validation_report.json
    | (~5s)                 11-point checklist
    v
OUTPUT: Trinity (video + metadata)
```

---

## KEY FILES

### Core Documentation
| File | Purpose |
|------|---------|
| 01_QUICK_START.md | LLM navigation, mental checklist |
| 02_PRIME.md | Identity, 12 Leverage Points |
| 03_INSTRUCTIONS.md | This file |
| 11_ADW_orchestrator.md | Main workflow |

### JSON Schemas
| File | Purpose |
|------|---------|
| 06_input_schema.json | Input validation |
| 08_video_rules.json | Production methodology |
| 09_platform_specs.json | 6 AI + 5 social platforms |
| 10_production_patterns.json | Scripts, hooks, transitions |
| 12_execution_plans.json | 4 execution plans |

### Configuration
| File | Purpose |
|------|---------|
| 13_voice_library.md | 8 PT-BR voices |
| 14_video_modes.md | Overlay vs Clean |

---

## VALIDATION

### Quality Gates (per phase)

**Phase 0 - Pre-flight**:
- Brief has required fields (produto, duracao, objetivo)
- video_mode selected (overlay/clean)
- voice_id valid (8 options)

**Phase 1 - Concept**:
- 3-8 shots generated
- Narrative arc complete (hook -> cta)
- Duration sums to brief +/-15%

**Phase 2 - Script**:
- Narration doesn't exceed duration
- IF overlay: text_overlays >= 1
- IF clean: text_overlays == []

**Phase 3 - Visual**:
- Prompt length 20-500 chars
- All shots have prompts
- Prompts in English

**Phase 4 - Production**:
- Clip success rate >= 80%
- All clips >= 720p
- Total cost <= $2.00

**Phase 5 - Editing**:
- File exists and playable
- Duration matches brief +/-10%
- Audio present

**Phase 6 - Validation**:
- 11-point checklist passed
- quality_score >= 7.0
- Trinity output complete

---

## INTEGRATION

### Upstream Dependencies
None - video_agent runs independently.

### Optional Inputs
- `marca_agent` -> brand_profile.json
- `pesquisa_agent` -> competitor_analysis.json

### Downstream Consumers
- `anuncio_agent` -> Video for ad copy sync
- User -> Ready-to-post content

---

## PERFORMANCE METRICS

**Timing** (per phase):
- Pre-flight: ~2s
- Concept: ~5s
- Script: ~3s
- Visual: ~10s
- Production: 120-300s (async)
- Editing: ~15s
- Validation: ~5s
- **Total**: 3-7 minutes

**Cost**: ~$0.97/video (6 shots, Runway)

**Token Efficiency**: ~2000 tokens/video

---

## BEST PRACTICES

1. **Storyboard First**: Never skip concept stage
2. **Validate Clips**: Check each clip before assembly
3. **Audio Layers**: Always mix narration + music
4. **Text Visibility**: High contrast for mobile
5. **Mode Compliance**: Respect overlay/clean rules
6. **Task Boundaries**: Always announce phase transitions
7. **Trinity Output**: Save all 3 files

---

## CHANGELOG

### v2.5.0 (2025-11-25)
- 12 Leverage Points implementation
- Task boundaries pattern
- 4 execution plans
- Restructured iso_vectorstore (20 files)

### v2.0.0 (2025-11-25)
- Pre-flight + Post-validation phases
- Video modes (overlay/clean)
- 8 PT-BR voices

### v1.0.0 (2025-11-24)
- Initial release
- 5-stage pipeline

---

**Status**: Production-Ready | **Version**: 2.5.0 | **Type**: Specialist Agent
**Dependencies**: FFmpeg, Runway/Pika API | **Quality Score**: 9.5/10.0
**12 Leverage Points**: Fully Implemented

---

> TIP: Always use task boundaries for progress visibility
> GOAL: Generate professional e-commerce videos with 0 human edits
> READY: Full 7-phase pipeline operational
