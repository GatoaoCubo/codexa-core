# ADW-105: YouTube Full Metadata Optimizer

**Version**: 1.0.0
**Duration**: 90-150 seconds (parallel execution)
**Phases**: 4 (Title → Parallel[Description, Thumbnail, Chapters] → Tags → Consolidate)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_youtube_full_metadata",
  "workflow_name": "YouTube Full Metadata Optimizer",
  "agent": "video_agent",
  "version": "1.0.0",
  "context_strategy": "chain_all_outputs",
  "failure_handling": "retry_phase_then_continue",
  "min_llm_model": "claude-sonnet-4+",
  "execution_mode": "hybrid_parallel",
  "required_capabilities": {
    "title_optimization": true,
    "description_optimization": true,
    "tags_optimization": true,
    "thumbnail_text_generation": true,
    "chapters_generation": true
  },
  "phases": [
    {"phase_id": "phase_1_title", "phase_name": "Title Optimization", "duration": "~30s", "parallel": false, "description": "Generate CTR-optimized title (base for all)"},
    {"phase_id": "phase_2_parallel", "phase_name": "Parallel Generation", "duration": "~40s", "parallel": true, "description": "Description + Thumbnail + Chapters in parallel"},
    {"phase_id": "phase_3_tags", "phase_name": "Tags Optimization", "duration": "~30s", "parallel": false, "description": "SEO tags with full context"},
    {"phase_id": "phase_4_consolidate", "phase_name": "Consolidation", "duration": "~10s", "parallel": false, "description": "Merge, validate, format output"}
  ]
}
```

---

## OVERVIEW

This ADW orchestrates the complete YouTube metadata optimization suite in a single execution:

```
                    ┌─────────────────┐
                    │   VIDEO_BRIEF   │
                    └────────┬────────┘
                             ↓
              ┌──────────────────────────────┐
              │  PHASE 1: TITLE OPTIMIZER    │
              │  HOP-60 | ~30s | Sequential  │
              │  → 5 angles → 4D scoring     │
              └──────────────┬───────────────┘
                             ↓
         ┌───────────────────┼───────────────────┐
         ↓                   ↓                   ↓
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ DESCRIPTION     │ │ THUMBNAIL TEXT  │ │ CHAPTERS        │
│ HOP-61 | ~30s   │ │ HOP-63 | ~20s   │ │ HOP-64 | ~25s   │
│ 5 sections      │ │ 3 variants      │ │ 5-10 chapters   │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         └───────────────────┼───────────────────┘
                             ↓
              ┌──────────────────────────────┐
              │  PHASE 3: TAGS OPTIMIZER     │
              │  HOP-62 | ~30s | Sequential  │
              │  → 30-50 tags, 4 categories  │
              └──────────────┬───────────────┘
                             ↓
              ┌──────────────────────────────┐
              │  PHASE 4: CONSOLIDATION      │
              │  Merge + Validate + Format   │
              └──────────────┬───────────────┘
                             ↓
              ┌──────────────────────────────┐
              │  youtube_metadata.json       │
              │  + copy_paste_ready.txt      │
              └──────────────────────────────┘
```

**Key Features**:
- Single input → Complete YouTube upload package
- Parallel execution where dependencies allow (~40% faster)
- Keyword consistency enforced across all outputs
- Consolidated quality score (weighted average)
- Copy-paste ready output for YouTube Studio

---

## PRE-REQUISITES

### Required
- [ ] Anthropic API key (Claude Sonnet 4+)
- [ ] video_brief with core fields

### Optional (Enhances Quality)
- [ ] $script from script_writer (for accurate chapters)
- [ ] $brand_profile from marca_agent
- [ ] $seo_keywords from pesquisa_agent
- [ ] $competitor_data for gap analysis

### Input Schema
```json
{
  "video_brief": {
    "title_working": "string, required, working title",
    "topic": "string, required, primary keyword",
    "target_audience": "string, required",
    "key_benefit": "string, required",
    "video_duration": "string, required, MM:SS or HH:MM:SS"
  },
  "script": "object, optional, from script_writer (enables accurate chapters)",
  "brand_profile": "object, optional, from marca_agent",
  "seo_keywords": "array, optional, max 20 items",
  "channel_context": {
    "channel_name": "string, optional",
    "subscriber_count": "integer, optional",
    "default_cta": "string, optional",
    "social_links": "object, optional"
  },
  "execution_options": {
    "skip_chapters": "boolean, default false, skip if video < 3min",
    "skip_thumbnail": "boolean, default false",
    "parallel_mode": "boolean, default true"
  }
}
```

---

## PHASE 1: TITLE OPTIMIZATION (Sequential)

**Objective**: Generate CTR-optimized title - foundation for all other phases

**Duration**: ~30 seconds

**HOP Reference**: `prompts/60_title_optimizer_HOP.md`

**Config Reference**: `config/youtube_title_rules.json`

### Execution

1. **Research Extraction** (~10s)
   - Extract primary_keyword from topic
   - Infer secondary keywords
   - Extract core_benefit
   - Analyze competitor titles (if available)

2. **Title Generation** (~15s)
   - Generate exactly 5 titles (one per psychological angle):
     - A: Question (1.25x CTR)
     - B: Number (1.36x CTR) ⭐
     - C: Social Proof (1.18x CTR)
     - D: How-To (1.22x CTR)
     - E: Comparison (1.30x CTR)

3. **4D Scoring & Selection** (~5s)
   - Score: CTR (35%) + SEO (30%) + Brand (20%) + Technical (15%)
   - Select winner (score >= 7.5)
   - Prepare alternatives

### Output → $title_output

```json
{
  "recommended": {
    "text": "7 Prompts de ChatGPT Que Todo Dev Precisa",
    "angle": "number",
    "score_total": 8.72,
    "char_count": 42
  },
  "alternatives": [...],
  "keywords_extracted": ["ChatGPT", "prompts", "dev"],
  "angle_used": "number"
}
```

### Quality Gate
- [ ] Score >= 7.5
- [ ] Char count 50-70
- [ ] Keyword in first 40 chars

---

## PHASE 2: PARALLEL GENERATION

**Objective**: Execute Description, Thumbnail Text, and Chapters simultaneously

**Duration**: ~40 seconds (parallel) vs ~75s (sequential)

**Execution Mode**: `/spawn` with 3 parallel agents

### Agent Spawn Configuration

```yaml
spawn_config:
  agents:
    - id: description_agent
      hop: prompts/61_description_optimizer_HOP.md
      config: config/youtube_description_rules.json
      input:
        - $video_brief
        - $title_output
        - $brand_profile (optional)
      output: $description_output
      priority: high

    - id: thumbnail_agent
      hop: prompts/63_thumbnail_text_HOP.md
      config: config/youtube_thumbnail_rules.json
      input:
        - $title_output.recommended.text
        - $video_brief
        - $brand_profile (optional)
      output: $thumbnail_output
      priority: medium

    - id: chapters_agent
      hop: prompts/64_chapters_generator_HOP.md
      config: config/youtube_chapters_rules.json
      input:
        - $video_brief
        - $script (if available)
        - $title_output (for keyword consistency)
      output: $chapters_output
      priority: medium
      skip_condition: video_duration < 180 seconds

  timeout: 45000
  failure_mode: continue_on_partial
```

### 2A: Description Agent

**HOP**: `61_description_optimizer_HOP.md`

**Steps**:
1. Parse video_brief + title_output for consistency
2. Determine content strategy by duration:
   - < 5min: 300-500 chars
   - 5-15min: 500-1000 chars
   - 15-60min: 1000-2000 chars
   - 60min+: 1500-2500 chars
3. Generate 5 sections:
   - Hook (100-150 chars, above fold)
   - Value Proposition (150-300 chars)
   - Timestamps (from chapters_agent or generate)
   - Links & CTAs (200-400 chars)
   - Hashtags (50-100 chars, 3-5 tags)
4. Score with 4D system

**Output → $description_output**:
```json
{
  "full_text": "...",
  "char_count": 847,
  "sections": {...},
  "score_total": 8.35,
  "hashtags": ["#ChatGPT", "#Programacao", "#IA"]
}
```

### 2B: Thumbnail Text Agent

**HOP**: `63_thumbnail_text_HOP.md`

**Steps**:
1. Analyze title angle (must differ for thumbnail)
2. Generate 3 variants using different angles:
   - Hook (pattern interrupt) - 1.18x CTR
   - Benefit (value prop) - 1.32x CTR ⭐
   - Curiosity (intrigue) - 1.25x CTR
3. Score with 4D system (readability, consistency, psychology, typography)
4. Provide design specs (font size, weight, case)

**Constraints**:
- 3-5 words max
- 40 characters max
- Must complement (not duplicate) title

**Output → $thumbnail_output**:
```json
{
  "recommended": {
    "text": "2x Dev Speed",
    "angle": "benefit",
    "score_total": 8.72,
    "design_spec": {
      "font_size_px": 32,
      "font_weight": "semi-bold",
      "case": "Mixed",
      "contrast": "high"
    }
  },
  "alternatives": [...]
}
```

### 2C: Chapters Agent

**HOP**: `64_chapters_generator_HOP.md`

**Skip Condition**: `video_duration < 180 seconds`

**Input Modes**:
1. Script mode (preferred): Use $script timing
2. Outline mode: Use manual outline
3. Inference mode: Estimate from brief

**Steps**:
1. Analyze content structure
2. Determine chapter count by duration:
   - 3-5min: 2-3 chapters
   - 5-10min: 4-6 chapters
   - 10-20min: 6-8 chapters
   - 20-60min: 8-12 chapters
3. Generate action-oriented chapter titles
4. Validate: first = 00:00, ascending, min 10s gaps

**Output → $chapters_output**:
```json
{
  "chapters": [
    {"timestamp": "00:00", "title": "Introdução e Overview"},
    {"timestamp": "01:45", "title": "Configurando o Ambiente"},
    ...
  ],
  "chapter_count": 8,
  "formatted_output": "⏱️ CAPÍTULOS:\n00:00 - Introdução...",
  "score_total": 8.42
}
```

### Parallel Sync Point

Wait for all 3 agents to complete (or timeout after 45s).

**Partial Failure Handling**:
- If description fails: Block (critical)
- If thumbnail fails: Continue without
- If chapters fails: Continue without (use description timestamps)

---

## PHASE 3: TAGS OPTIMIZATION (Sequential)

**Objective**: Generate SEO-optimized tags with full context from all previous phases

**Duration**: ~30 seconds

**HOP Reference**: `prompts/62_tags_optimizer_HOP.md`

**Config Reference**: `config/youtube_tags_rules.json`

### Why Sequential?

Tags optimizer needs context from:
- $title_output → keywords to include
- $description_output → hashtags to convert, secondary keywords
- $chapters_output → section keywords

This maximizes keyword consistency across all metadata.

### Execution

1. **Research Aggregation** (~10s)
   - Collect keywords from title
   - Extract hashtags from description
   - Parse chapter titles for keywords
   - Load SEO data (if available)

2. **Tag Generation** (~15s)
   - Generate 30-50 tags across 4 categories:
     - Primary (3-5): Core keywords, broad
     - Secondary (8-12): Commercial intent
     - Long-tail (12-20): Discovery, low competition
     - Semantic (5-8): Context signals

3. **4D Scoring** (~5s)
   - SEO Relevance (40%)
   - Keyword Consistency (35%)
   - Discoverability Coverage (15%)
   - Technical Compliance (10%)

### Output → $tags_output

```json
{
  "recommended_set": {
    "primary_tags": ["ChatGPT", "programação", "IA"],
    "secondary_tags": ["ChatGPT tutorial", "prompts dev", ...],
    "long_tail_tags": ["como usar ChatGPT programar", ...],
    "semantic_tags": ["machine learning", "produtividade", ...],
    "total_tags": 43,
    "total_char_count": 498
  },
  "score_total": 8.92,
  "consistency_analysis": {
    "title_coverage": "100%",
    "description_coverage": "95%",
    "hashtag_coverage": "100%"
  }
}
```

### Quality Gate
- [ ] 30-50 tags total
- [ ] <= 500 characters total
- [ ] Score >= 7.5
- [ ] Title keyword present
- [ ] No duplicates

---

## PHASE 4: CONSOLIDATION

**Objective**: Merge all outputs, validate consistency, format for YouTube Studio

**Duration**: ~10 seconds

### Steps

1. **Merge Outputs**
   - Combine all phase outputs into single object
   - Cross-reference keywords for consistency

2. **Calculate Consolidated Score**
   ```python
   consolidated_score = (
     title_score * 0.30 +
     description_score * 0.25 +
     tags_score * 0.20 +
     thumbnail_score * 0.15 +
     chapters_score * 0.10
   )
   ```

3. **Generate Copy-Paste Ready Output**
   - Title: ready for title field
   - Description: full formatted text
   - Tags: comma-separated list
   - Thumbnail text: with design specs

4. **Validation Summary**
   - All quality gates passed?
   - Keyword consistency score
   - Character limits respected
   - Platform compliance

### Output → youtube_metadata.json

```json
{
  "metadata_version": "1.0.0",
  "generated_at": "2025-12-05T10:30:00Z",
  "execution_time_seconds": 95,

  "title": {
    "text": "7 Prompts de ChatGPT Que Todo Dev Precisa",
    "char_count": 42,
    "angle": "number",
    "score": 8.72
  },

  "description": {
    "full_text": "ChatGPT para programação: os 7 prompts que vão...",
    "char_count": 847,
    "sections": {
      "hook": "ChatGPT para programação...",
      "value_proposition": "📌 O QUE VOCÊ VAI APRENDER...",
      "timestamps": "⏱️ CAPÍTULOS:\n00:00 - Introdução...",
      "links_ctas": "🔗 RECURSOS:\n...",
      "hashtags_keywords": "#ChatGPT #Programacao..."
    },
    "score": 8.35
  },

  "tags": {
    "all_tags": ["ChatGPT", "programação", "IA", ...],
    "tag_count": 43,
    "char_count": 498,
    "comma_separated": "ChatGPT,programação,IA,...",
    "score": 8.92
  },

  "thumbnail_text": {
    "recommended": "2x Dev Speed",
    "alternatives": ["Hack Secreto", "Ninguém Conta"],
    "design_spec": {
      "font_size_px": 32,
      "font_weight": "semi-bold",
      "case": "Mixed"
    },
    "score": 8.72
  },

  "chapters": {
    "list": [
      {"timestamp": "00:00", "title": "Introdução e Overview"},
      {"timestamp": "01:45", "title": "Configurando o Ambiente"}
    ],
    "chapter_count": 8,
    "formatted": "00:00 - Introdução e Overview\n01:45 - ...",
    "score": 8.42
  },

  "consolidated": {
    "overall_score": 8.62,
    "keyword_consistency": 0.96,
    "quality_gates_passed": 5,
    "quality_gates_total": 5,
    "warnings": [],
    "ready_for_upload": true
  },

  "copy_paste_ready": {
    "title": "7 Prompts de ChatGPT Que Todo Dev Precisa",
    "description": "[full formatted description]",
    "tags": "ChatGPT,programação,IA,prompts,..."
  }
}
```

---

## SUCCESS CRITERIA

### All Phases Complete
- [ ] Phase 1: Title generated (score >= 7.5)
- [ ] Phase 2A: Description generated (score >= 7.5)
- [ ] Phase 2B: Thumbnail text generated (score >= 7.0)
- [ ] Phase 2C: Chapters generated (score >= 7.0) OR skipped
- [ ] Phase 3: Tags generated (score >= 7.5)
- [ ] Phase 4: Consolidation complete

### Quality Thresholds
- [ ] Consolidated score >= 7.5
- [ ] Keyword consistency >= 85%
- [ ] All character limits respected
- [ ] No duplicate content across sections

### Output Complete
- [ ] youtube_metadata.json generated
- [ ] copy_paste_ready section populated
- [ ] All scores documented

---

## ERROR HANDLING

### Phase 1 Failure (Title)
- **Severity**: CRITICAL (blocks all)
- **Action**: Retry up to 2x, then fail workflow
- **Reason**: All other phases depend on title

### Phase 2A Failure (Description)
- **Severity**: CRITICAL
- **Action**: Retry up to 2x, then fail workflow
- **Reason**: Core metadata for upload

### Phase 2B Failure (Thumbnail)
- **Severity**: LOW
- **Action**: Continue without thumbnail text
- **Fallback**: Use title-based suggestion

### Phase 2C Failure (Chapters)
- **Severity**: LOW
- **Action**: Continue without chapters
- **Fallback**: Use "timestamps not available" in description

### Phase 3 Failure (Tags)
- **Severity**: MEDIUM
- **Action**: Retry up to 2x
- **Fallback**: Generate minimal tag set from title keywords

### Timeout Handling
```yaml
timeouts:
  phase_1: 45s
  phase_2_parallel: 50s
  phase_3: 45s
  phase_4: 15s
  total_workflow: 180s
```

---

## USAGE

### Trigger: Slash Command

```bash
/youtube-metadata "Brief: Tutorial ChatGPT para devs, 15min, público iniciantes"
```

### Trigger: Pipeline Integration

```python
# After video production (Phase 5)
from video_agent import youtube_metadata_optimizer

result = youtube_metadata_optimizer.run(
    video_brief=pipeline.video_brief,
    script=pipeline.script,  # optional, improves chapters
    brand_profile=pipeline.brand_profile  # optional
)

# Result contains complete upload package
youtube_upload(
    title=result.copy_paste_ready.title,
    description=result.copy_paste_ready.description,
    tags=result.copy_paste_ready.tags
)
```

### Trigger: Direct API

```json
{
  "mode": "youtube_full_metadata",
  "input": {
    "video_brief": {
      "title_working": "Review iPhone 15 Pro",
      "topic": "iPhone 15 Pro",
      "target_audience": "Tech enthusiasts",
      "key_benefit": "Decisão de compra informada",
      "video_duration": "18:30"
    },
    "execution_options": {
      "parallel_mode": true
    }
  }
}
```

---

## METRICS

```json
{
  "workflow_metrics": {
    "total_time_seconds": 95,
    "parallel_efficiency": 0.63,
    "phases_completed": 5,
    "phases_skipped": 0,
    "retries": 0
  },
  "quality_metrics": {
    "title_score": 8.72,
    "description_score": 8.35,
    "tags_score": 8.92,
    "thumbnail_score": 8.72,
    "chapters_score": 8.42,
    "consolidated_score": 8.62
  },
  "consistency_metrics": {
    "keyword_consistency": 0.96,
    "title_to_description": 1.0,
    "title_to_tags": 1.0,
    "description_to_chapters": 0.92
  }
}
```

---

## CONFIGURATION FILES

| File | Purpose |
|------|---------|
| `config/youtube_title_rules.json` | Title formulas, scoring weights |
| `config/youtube_description_rules.json` | Section templates, length rules |
| `config/youtube_tags_rules.json` | Category strategies, limits |
| `config/youtube_thumbnail_rules.json` | Text formulas, design specs |
| `config/youtube_chapters_rules.json` | Naming conventions, timing |

---

## HOP REFERENCES

| HOP | Stage | Purpose |
|-----|-------|---------|
| `60_title_optimizer_HOP.md` | Phase 1 | CTR-optimized title |
| `61_description_optimizer_HOP.md` | Phase 2A | 5-section description |
| `62_tags_optimizer_HOP.md` | Phase 3 | 30-50 SEO tags |
| `63_thumbnail_text_HOP.md` | Phase 2B | 3-5 word thumbnail text |
| `64_chapters_generator_HOP.md` | Phase 2C | Timestamp chapters |

---

## VERSION HISTORY

### v1.0.0 (2025-12-05)
- Initial unified ADW implementation
- Hybrid parallel/sequential execution
- 5 optimizer modules integrated
- Consolidated output format
- Copy-paste ready output
- Quality gate consolidation

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-05
**Status**: Production Ready
**Execution Mode**: Hybrid Parallel
**Predecessors**: 103_ADW_YOUTUBE_TITLE.md, 104_ADW_YOUTUBE_DESCRIPTION.md
