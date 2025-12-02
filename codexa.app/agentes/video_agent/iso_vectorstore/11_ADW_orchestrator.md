<!-- iso_vectorstore -->
<!--
  Source: 100_ADW_RUN_VIDEO.md
  Agent: video_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# ADW-100: Complete Video Generation Workflow

**Version**: 2.0.0
**Duration**: 3-7 minutes
**Phases**: 5 + Pre-flight + Post-validation

---

## OVERVIEW

This ADW orchestrates the complete video generation pipeline with intelligent mode selection and voice integration:

```
Pre-flight → Concept → Script → Visual → Production → Editing → Post-validation → Final Video
```

**New in v2.0.0**:
- Pre-flight phase with video_mode auto-selection (overlay/clean)
- Voice auto-selection from 8 pt-BR voices
- Video mode aware Script and Visual phases
- Post-validation with 11-point quality checklist
- ISO vectorstore sync (22 files)
- PROCESSADOS catalog integration

---

## PRE-REQUISITES

### Required
- [ ] Anthropic API key (Claude Sonnet 4.5)
- [ ] Runway/Veo/Sora API key (video generation)
- [ ] FFmpeg installed
- [ ] ElevenLabs API key (TTS narration - 8 voices)

### Optional
- [ ] Pika API key (fallback)
- [ ] AWS S3 credentials (cloud storage)

### Input Validation
```json
{
  "produto": "string, required, 3-200 chars",
  "duracao": "integer, required, 15-60",
  "formato": "enum: 9:16, 16:9, 1:1",
  "tom": "string, optional, default: energético",
  "objetivo": "string, required, 10-500 chars",
  "platforms": "array, optional, ['instagram', 'tiktok', 'youtube']",
  "international": "boolean, optional, default: false",
  "preco": "number, optional",
  "gender_preference": "enum: feminina, masculina, optional"
}
```

---

## ISO VECTORSTORE REFERENCE

This ADW synchronizes with 22 knowledge files:

```
iso_vectorstore/
├── 01_QUICK_START.md           # Quick start guide
├── 02_PRIME.md                 # Prime directive
├── 03_INSTRUCTIONS.md          # Core instructions
├── 04_README.md                # Overview
├── 05_SETUP.md                 # Setup guide
├── 06_input_schema.json        # Brief validation
├── 07_video_styles.json        # Style presets
├── 08_ADW_orchestrator.md      # This workflow (portable)
├── 09_platform_veo3.md         # Google Veo 3
├── 10_platform_sora2.md        # OpenAI Sora 2
├── 11_platform_kling.md        # Kling AI
├── 12_platform_hailuo.md       # Hailuo MiniMax
├── 13_platform_runway.md       # Runway Gen-3
├── 14_platform_pika.md         # Pika 2.0
├── 15_prompt_anatomy.md        # Prompt structure
├── 16_camera_vocabulary.md     # Camera movements
├── 17_lighting_vocabulary.md   # Lighting setups
├── 18_magic_words.md           # Quality enhancers
├── 19_brand_alignment.md       # Brand guidelines
├── 20_HOP_visual_prompter.md   # Visual HOP
├── 21_voice_library_ptbr.md    # 8 voices pt-BR
└── 22_video_modes.md           # Overlay vs Clean
```

---

## PRE-FLIGHT PHASE (NEW)

**Objective**: Validate inputs and configure execution mode

**Duration**: ~2 seconds

**Config Files**:
- `config/voice_config.json` - 8 voices pt-BR
- `config/video_modes.json` - Mode selection rules

### Steps

1. **Validate Brief Schema**
   - Check required fields (produto, duracao, objetivo)
   - Validate ranges and enums
   - Load from `iso_vectorstore/06_input_schema.json`

2. **Auto-Select Video Mode**
   - Parse brief fields (objective, platforms, international, tom, preco)
   - Apply rules from `config/video_modes.json`
   - Decision logic:
     ```python
     # CLEAN when:
     if any([
         brief.get("international", False),
         brief.get("tom") in ["premium", "cinematografico", "sofisticado"],
         brief.get("objective") == "brand_awareness",
         brief.get("repurpose", False),
         "youtube" in brief.get("platforms", [])
     ]):
         video_mode = "clean"

     # OVERLAY when:
     elif any([
         brief.get("objective") == "conversao",
         "instagram" in brief.get("platforms", []),
         "tiktok" in brief.get("platforms", []),
         brief.get("preco") is not None,
         brief.get("cta_required", True)
     ]):
         video_mode = "overlay"

     else:
         video_mode = "overlay"  # Default
     ```

3. **Auto-Select Voice**
   - Parse tom from brief (energetico/sofisticado/profissional/acolhedor)
   - Parse gender_preference (feminina/masculina, default: feminina)
   - Load voice map from `config/voice_config.json`
   - Select voice_id:
     ```python
     voice_map = {
         "energetico": {"feminina": "pMsXgVXv3BLzUgSXRplE", "masculina": "ErXwobaYiN019PkySvjV"},
         "sofisticado": {"feminina": "EXAVITQu4vr4xnSDxMaL", "masculina": "TX3LPaxmHKxFdv7VOQHJ"},
         "profissional": {"feminina": "XrExE9yKIg1WjnnlVkGX", "masculina": "VR6AewLTigWG4xSOukaG"},
         "acolhedor": {"feminina": "nPczCjzI2devNBz1zQrb", "masculina": "pNInz6obpgDQGcFmaJgB"}
     }
     gender = brief.get("gender_preference", "feminina")
     tom = brief.get("tom", "energetico")
     voice_id = voice_map[tom][gender]
     ```

4. **Load Context from PROCESSADOS**
   - Read `PROCESSADOS/catalogo.json`
   - Find similar videos by category
   - Load relevant knowledge cards (max 2)

5. **Determine Target Platform**
   - Parse platforms array from brief
   - Auto-select primary platform if not specified
   - Load platform-specific constraints from `iso_vectorstore/09-14_platform_*.md`

### Output

```json
{
  "validated_brief": {
    "produto": "Nike Air Max",
    "duracao": 30,
    "formato": "9:16",
    "tom": "energetico",
    "objetivo": "conversao",
    "platforms": ["instagram"]
  },
  "config": {
    "video_mode": "overlay",
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "voice_name": "Camila",
    "voice_gender": "feminina",
    "platform": "runway",
    "context_cards": ["PROCESSADOS/tenis_esportivo.md"]
  }
}
```

### Quality Gate
- [ ] All required fields present
- [ ] video_mode selected (overlay/clean)
- [ ] voice_id valid (8 options)
- [ ] Duration 15-60s
- [ ] Format valid (9:16, 16:9, 1:1)

---

## PHASE 1: CONCEPT (Storyboard Generation)

**Objective**: Generate 6-8 shot storyboard with narrative arc

**Duration**: ~5 seconds

**HOP**: `prompts/10_concept_planner_HOP.md`

**Builder**: `builders/01_concept_builder.py`

### Steps

1. **Validate Brief**
   - Check all required fields present
   - Validate duration range (15-60s)
   - Validate format (9:16, 16:9, 1:1)

2. **Calculate Shot Count**
   - 15s → 3 shots
   - 30s → 6 shots
   - 45s → 7 shots
   - 60s → 8 shots

3. **Generate Storyboard**
   - Call Claude Sonnet 4.5 with brief + config
   - Generate shots with narrative arc
   - Reference `iso_vectorstore/15_prompt_anatomy.md`
   - Output: concept.json

4. **Validate Storyboard**
   - First shot is "hook"
   - Last shot is "cta"
   - Total duration matches brief ±15%

### Output

```json
{
  "shots": [
    {
      "number": 1,
      "duration": 4,
      "description": "Close-up do tênis girando 360°",
      "composition": "Product shot, white background",
      "narrative": "hook"
    }
  ],
  "total_duration": 30,
  "narrative_arc": "Hook → Build → Benefit → CTA",
  "video_mode": "overlay"
}
```

### Quality Gate
- [ ] 3-8 shots generated
- [ ] Duration sums to brief ±15%
- [ ] All required fields present
- [ ] video_mode field present

---

## PHASE 2: SCRIPT (Narration + Timing) - UPDATED

**Objective**: Write narration script with video_mode awareness

**Duration**: ~3 seconds

**HOP**: `prompts/20_script_writer_HOP.md` (v2.0.0)

**Builder**: `builders/02_script_builder.py`

### Steps

1. **Analyze Storyboard + Config**
   - Read shot descriptions
   - Read video_mode from config
   - Read voice_id from config
   - Calculate cumulative timing

2. **Write Narration**
   - 5-10 words per segment
   - Align with shot timing
   - Leave breathing room
   - Adapt to voice characteristics (reference `iso_vectorstore/21_voice_library_ptbr.md`)

3. **Define Text Overlays (MODE-AWARE)**
   - **IF video_mode == "overlay"**:
     - Product name (shot 1-2)
     - Key benefits (middle shots)
     - Price + CTA (final shot)
     - Min 1 overlay required
   - **IF video_mode == "clean"**:
     - text_overlays = []
     - Narration carries ALL messaging
     - Reference `iso_vectorstore/22_video_modes.md`

4. **Select Music**
   - Match tone from brief
   - Set volume (0.3 background)

### Output

**Overlay Mode**:
```json
{
  "video_mode": "overlay",
  "voice_id": "pMsXgVXv3BLzUgSXRplE",
  "voice_name": "Camila",
  "narration": [
    {"start": 0, "end": 3, "text": "Conheça o futuro do conforto"}
  ],
  "text_overlays": [
    {"start": 1, "end": 4, "text": "NIKE AIR MAX", "position": "bottom"},
    {"start": 27, "end": 30, "text": "R$ 599 | Compre agora", "position": "bottom"}
  ],
  "music": {
    "track": "music/upbeat.mp3",
    "volume": 0.3
  }
}
```

**Clean Mode**:
```json
{
  "video_mode": "clean",
  "voice_id": "pMsXgVXv3BLzUgSXRplE",
  "voice_name": "Camila",
  "narration": [
    {"start": 0, "end": 3, "text": "Conheça o Nike Air Max"},
    {"start": 4, "end": 8, "text": "O futuro do conforto está aqui"},
    {"start": 27, "end": 30, "text": "Apenas quinhentos e noventa e nove reais"}
  ],
  "text_overlays": [],
  "music": {
    "track": "music/upbeat.mp3",
    "volume": 0.3
  }
}
```

### Quality Gate
- [ ] Narration doesn't exceed video duration
- [ ] No overlapping segments
- [ ] IF overlay: at least 1 text overlay
- [ ] IF clean: text_overlays == []
- [ ] voice_id matches config

---

## PHASE 3: VISUAL (Prompt Engineering) - UPDATED

**Objective**: Create platform prompts with composition mode awareness

**Duration**: ~10 seconds

**HOP**: `prompts/30_visual_prompter_HOP.md` (v2.1.0)

**Builder**: `builders/03_visual_builder.py`

### Steps

1. **Determine Style**
   - Parse tone from brief
   - Select style preset from `iso_vectorstore/07_video_styles.json`
   - Load camera/lighting templates:
     - `iso_vectorstore/16_camera_vocabulary.md`
     - `iso_vectorstore/17_lighting_vocabulary.md`

2. **Generate Prompts (MODE-AWARE)**
   - For each shot:
     - **IF video_mode == "overlay"**:
       - Reserve bottom 20% for text
       - Focus composition on top 80%
       - Safe zone: upper frame
     - **IF video_mode == "clean"**:
       - Use full frame composition
       - No text considerations
       - Cinematic framing
     - Build detailed platform prompt
     - Specify camera movement
     - Define lighting setup
     - Add style qualifiers from `iso_vectorstore/18_magic_words.md`

3. **Define Transitions**
   - Match transitions to style
   - Hook: hard cut
   - Build: dissolve or cut
   - CTA: fade

### Output

**Overlay Mode**:
```json
[
  {
    "shot_number": 1,
    "duration": 4,
    "video_mode": "overlay",
    "composition_mode": "safe_zone_top_80",
    "runway_prompt": "Nike sneaker rotating 360 degrees on white seamless background, product photography, studio lighting, focus on upper 80% of frame...",
    "camera": {"angle": "eye-level", "movement": "static"},
    "transition": "cut"
  }
]
```

**Clean Mode**:
```json
[
  {
    "shot_number": 1,
    "duration": 4,
    "video_mode": "clean",
    "composition_mode": "full_frame",
    "runway_prompt": "Nike sneaker rotating 360 degrees on white seamless background, cinematic product shot, studio lighting, full frame composition...",
    "camera": {"angle": "eye-level", "movement": "static"},
    "transition": "cut"
  }
]
```

### Quality Gate
- [ ] Prompt length 20-500 chars
- [ ] All shots have prompts
- [ ] Prompts in English
- [ ] composition_mode matches video_mode
- [ ] IF overlay: "upper frame" or "top 80%" in prompt
- [ ] IF clean: "full frame" or "cinematic" in prompt

---

## PHASE 4: PRODUCTION (Video Generation)

**Objective**: Generate video clips via platform APIs

**Duration**: 120-300 seconds (async)

**HOP**: `prompts/40_production_runner_HOP.md`

**Builder**: `builders/04_production_builder.py`

### Steps

1. **Initialize Connections**
   - Validate API keys
   - Select primary platform from config
   - Set up rate limiting (5 concurrent)
   - Reference platform docs:
     - `iso_vectorstore/09_platform_veo3.md` (Google Veo 3)
     - `iso_vectorstore/10_platform_sora2.md` (OpenAI Sora 2)
     - `iso_vectorstore/13_platform_runway.md` (Runway Gen-3)
     - Others: Kling, Hailuo, Pika

2. **Generate Clips (Parallel)**
   - For each prompt:
     - Call platform API
     - Wait for completion (polling)
     - Download clip
   - Retry failed clips (3 attempts)
   - Fallback chain: Runway → Pika → Templates

3. **Validate Clips**
   - Check resolution (≥1080p)
   - Check duration (±0.5s tolerance)
   - Check for artifacts
   - Validate composition matches mode

4. **Track Costs**
   - Runway: $0.05/second
   - Pika: $0.03/second
   - Veo/Sora: pricing varies

### Output

```json
[
  {
    "shot_number": 1,
    "clip_path": "outputs/clips/clip_001.mp4",
    "platform": "runway",
    "success": true,
    "cost_usd": 0.20,
    "resolution": "1080x1920",
    "video_mode": "overlay"
  }
]
```

### Quality Gate
- [ ] ≥80% clips successful
- [ ] All clips ≥720p
- [ ] Total cost ≤$2.00
- [ ] Resolution matches formato

---

## PHASE 5: EDITING (Final Assembly)

**Objective**: Assemble final video with audio and text (mode-aware)

**Duration**: ~15 seconds

**HOP**: `prompts/50_editor_assembler_HOP.md`

**Builder**: `builders/05_editing_builder.py`

### Steps

1. **Concatenate Clips**
   - Sort by shot number
   - Create FFmpeg concat list
   - Merge clips with transitions

2. **Generate TTS (ElevenLabs)**
   - Read voice_id from config
   - Concatenate narration text
   - Call ElevenLabs API with settings:
     ```json
     {
       "voice_id": "pMsXgVXv3BLzUgSXRplE",
       "model_id": "eleven_multilingual_v2",
       "voice_settings": {
         "stability": 0.5,
         "similarity_boost": 0.75,
         "style": 0.0,
         "use_speaker_boost": true
       }
     }
     ```
   - Save audio file

3. **Mix Audio**
   - Layer: narration (vol 1.0) + music (vol 0.3)
   - Sync with video timeline
   - Apply audio normalization

4. **Add Text Overlays (MODE-AWARE)**
   - **IF video_mode == "overlay"**:
     - Apply FFmpeg drawtext filter
     - Position: bottom (20% zone)
     - Timing from script
     - Font: Arial Bold, size 48
     - Color: white, stroke: black
   - **IF video_mode == "clean"**:
     - Skip text rendering entirely
     - No drawtext filters applied

5. **Export Final (Trinity Output)**
   - Scale to target format (9:16, 16:9, 1:1)
   - Encode H.264, CRF 23
   - Add faststart flag for streaming
   - Generate metadata files

### Output

```
outputs/
├── nike_air_max_30s.mp4              # Final video
├── nike_air_max_30s.llm.json         # LLM-readable metadata
└── nike_air_max_30s.meta.json        # Human-readable metadata
```

**nike_air_max_30s.llm.json**:
```json
{
  "video_id": "nike_air_max_30s_20251125",
  "produto": "Nike Air Max",
  "duracao": 30,
  "formato": "9:16",
  "video_mode": "overlay",
  "voice_id": "pMsXgVXv3BLzUgSXRplE",
  "voice_name": "Camila",
  "shots_count": 6,
  "narration_segments": 5,
  "text_overlays": 2,
  "cost_usd": 0.97,
  "quality_score": 8.5,
  "platform": "runway",
  "created_at": "2025-11-25T10:30:00Z"
}
```

### Quality Gate
- [ ] File exists and playable
- [ ] Duration matches brief ±10%
- [ ] Audio present and synced
- [ ] IF overlay: text overlays visible
- [ ] IF clean: no text present
- [ ] Trinity output complete (3 files)

---

## POST-VALIDATION PHASE (NEW)

**Objective**: Validate final video quality with 11-point checklist

**Duration**: ~5 seconds

**Validator**: `validators/quality_validator.py`

### 11-Point Quality Checklist

```python
quality_checks = {
    1: "Video file exists and is playable",
    2: "Duration matches brief ±10%",
    3: "Resolution meets minimum (720p+)",
    4: "Format matches brief (9:16, 16:9, 1:1)",
    5: "Audio present and properly mixed",
    6: "Narration synced with video",
    7: "No visual artifacts or glitches",
    8: "Transitions smooth and appropriate",
    9: "IF overlay: text overlays visible and readable",
    10: "IF clean: zero text present in video",
    11: "Trinity output complete (3 files)"
}
```

### Steps

1. **Run Quality Checks**
   - Execute all 11 validation points
   - Score each check (pass/fail)
   - Calculate quality_score (0-10)

2. **Validate Mode Compliance**
   - **IF overlay**: Check text_overlays >= 1
   - **IF clean**: Verify text_overlays == 0
   - Verify composition matches mode

3. **Generate Trinity Output**
   - Ensure .mp4 file exists
   - Generate .llm.json (LLM metadata)
   - Generate .meta.json (human metadata)

4. **Update PROCESSADOS Catalog**
   - IF quality_score >= 8.0:
     - Add entry to `PROCESSADOS/catalogo.json`
     - Generate knowledge card `PROCESSADOS/{produto}_{timestamp}.md`
     - Include: brief, config, prompts, results

### Output

```json
{
  "validation_report": {
    "checks_passed": 11,
    "checks_failed": 0,
    "quality_score": 9.2,
    "mode_compliance": true,
    "trinity_complete": true,
    "catalog_updated": true
  },
  "final_outputs": [
    "outputs/nike_air_max_30s.mp4",
    "outputs/nike_air_max_30s.llm.json",
    "outputs/nike_air_max_30s.meta.json",
    "PROCESSADOS/nike_air_max_20251125.md"
  ]
}
```

### Quality Gate
- [ ] All 11 checks passed
- [ ] quality_score >= 7.0
- [ ] Mode compliance verified
- [ ] Trinity output validated
- [ ] Catalog updated (if score >= 8.0)

---

## SUCCESS CRITERIA

### All Phases Complete
- [ ] Pre-flight: config generated
- [ ] Phase 1: concept.json exists
- [ ] Phase 2: script.json exists (mode-aware)
- [ ] Phase 3: visual_prompts.json exists (mode-aware)
- [ ] Phase 4: all clips generated
- [ ] Phase 5: Trinity output complete
- [ ] Post-validation: quality_score ≥7.0

### Mode Compliance
- [ ] IF overlay: text visible, bottom 20%
- [ ] IF clean: zero text, full frame

### Metadata Complete
- [ ] .mp4 playable
- [ ] .llm.json parseable
- [ ] .meta.json human-readable

---

## CLEANUP & METRICS

### Cleanup
- Remove temp files
- Archive source clips (optional)
- Compress logs

### Metrics to Track

```json
{
  "workflow_metrics": {
    "total_time_seconds": 245,
    "cost_usd": 0.97,
    "phases_completed": 7,
    "quality_score": 8.5
  },
  "phase_metrics": {
    "preflight": 2,
    "concept": 5,
    "script": 3,
    "visual": 10,
    "production": 180,
    "editing": 15,
    "validation": 5
  },
  "generation_metrics": {
    "clips_requested": 6,
    "clips_successful": 6,
    "clips_retried": 0,
    "platform": "runway"
  },
  "configuration": {
    "video_mode": "overlay",
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "voice_name": "Camila"
  }
}
```

---

## ERROR HANDLING

### Pre-flight Failure
- **Cause**: Invalid brief schema
- **Action**: Return validation errors with field details

### Phase 1 Failure
- **Cause**: Claude API error
- **Action**: Retry 3x, use fallback template

### Phase 2 Failure
- **Cause**: Voice config missing
- **Action**: Use default voice (Camila - energetico/feminina)

### Phase 3 Failure
- **Cause**: Mode config missing
- **Action**: Default to overlay mode

### Phase 4 Failure
- **Cause**: Platform API timeout or quota
- **Action**: Fallback chain: Runway → Pika → Templates

### Phase 5 Failure
- **Cause**: FFmpeg error
- **Action**: Return video without text/audio, mark as partial

### Post-validation Failure
- **Cause**: Quality score < 7.0
- **Action**: Log issues, flag for manual review

### Recovery
All phases save intermediate outputs. On restart:
1. Check for config.json → skip Pre-flight
2. Check for concept.json → skip Phase 1
3. Check for script.json → skip Phase 2
4. Check for visual_prompts.json → skip Phase 3
5. Check for clips → skip Phase 4
6. Resume from last successful phase

---

## VALIDATION COMMANDS

```bash
# Test Pre-flight
python builders/00_preflight.py --brief examples/brief_overlay.json

# Test Phase 1
python builders/01_concept_builder.py --config outputs/config.json

# Test Phase 2 (overlay mode)
python builders/02_script_builder.py --mode overlay

# Test Phase 2 (clean mode)
python builders/02_script_builder.py --mode clean

# Test Phase 3 (overlay mode)
python builders/03_visual_builder.py --mode overlay

# Test Phase 3 (clean mode)
python builders/03_visual_builder.py --mode clean

# Test Phase 4 (mock mode)
VIDEO_AGENT_MOCK_API=true python builders/04_production_builder.py

# Test Phase 5 (overlay)
python builders/05_editing_builder.py --mode overlay

# Test Phase 5 (clean)
python builders/05_editing_builder.py --mode clean

# Test Post-validation
python validators/quality_validator.py --video outputs/test.mp4

# Test complete pipeline (overlay)
python src/video_agent.py --brief examples/brief_overlay.json --mock

# Test complete pipeline (clean)
python src/video_agent.py --brief examples/brief_clean.json --mock

# Validate voice config
python -m json.tool config/voice_config.json

# Validate mode config
python -m json.tool config/video_modes.json
```

---

## CONFIGURATION FILES

### config/voice_config.json
8 voices pt-BR (4 femininas, 4 masculinas) with auto-selection rules.

### config/video_modes.json
Rules for overlay vs clean mode selection with validation.

### iso_vectorstore/*.md
22 knowledge files for platform prompts, styles, and guidelines.

### PROCESSADOS/catalogo.json
Historical video catalog for context and learning.

---

## VERSION HISTORY

### v2.0.0 (2025-11-25)
- Added Pre-flight phase with video_mode + voice auto-selection
- Updated Phase 2 (Script) for video_mode awareness
- Updated Phase 3 (Visual) for composition by mode
- Added Post-validation phase with 11-point checklist
- Integrated 8 pt-BR voices (ElevenLabs)
- Added config files: voice_config.json, video_modes.json
- Synced with 22 iso_vectorstore files
- Added PROCESSADOS catalog integration
- Trinity output (.mp4, .llm.json, .meta.json)

### v1.0.0 (2025-11-24)
- Initial ADW with 5 phases
- Basic Runway integration
- Manual voice selection
- Single composition mode

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-11-25
**Status**: Production Ready
**Documentation**: iso_vectorstore/08_ADW_orchestrator.md
