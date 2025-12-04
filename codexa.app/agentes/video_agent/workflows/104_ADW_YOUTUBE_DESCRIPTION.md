# ADW-104: YouTube Description Optimizer Workflow

**Version**: 1.0.0
**Duration**: 30-60 seconds
**Phases**: 3 (Research → Generate → Validate)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_youtube_description",
  "workflow_name": "YouTube Description Optimizer Workflow",
  "agent": "video_agent",
  "version": "1.0.0",
  "context_strategy": "minimal",
  "failure_handling": "retry_then_fallback",
  "min_llm_model": "claude-sonnet-4+",
  "required_capabilities": {
    "description_optimization": true,
    "seo_analysis": true,
    "brand_alignment": true,
    "timestamp_generation": true
  },
  "phases": [
    {"phase_id": "phase_1_research", "phase_name": "Research & Strategy", "duration": "~10s", "description": "Extract signals, determine content strategy and length"},
    {"phase_id": "phase_2_generate", "phase_name": "Description Generation", "duration": "~15s", "description": "Generate 5-section description with optimized content"},
    {"phase_id": "phase_3_validate", "phase_name": "Scoring & Validation", "duration": "~10s", "description": "Score with 4D system, ensure quality gate"}
  ]
}
```

---

## OVERVIEW

This ADW orchestrates YouTube description optimization with SEO-focused generation:

```
Research → Generate → Validate → Optimized Description + Scoring
```

**Key Features**:
- 5-section structure (Hook, Value Prop, Timestamps, Links/CTAs, Hashtags)
- 4D scoring system (Engagement 35%, SEO 30%, Brand 20%, Technical 15%)
- Quality gate: minimum score >= 7.5
- Integration with title_optimizer pipeline or standalone
- Automatic timestamp generation for videos >= 3 minutes

---

## PRE-REQUISITES

### Required
- [ ] Anthropic API key (Claude Sonnet 4+)
- [ ] video_brief OR direct input

### Optional (Recommended)
- [ ] title_optimizer_output from 60_title_optimizer (for consistency)
- [ ] brand_profile from marca_agent
- [ ] seo_keywords from pesquisa_agent
- [ ] video_chapters for timestamp generation

### Input Schema
```json
{
  "video_brief": {
    "title_final": "string, required, from title_optimizer or working title",
    "topic": "string, required, primary keyword",
    "target_audience": "string, required",
    "key_benefit": "string, required",
    "video_duration": "string, required, MM:SS or HH:MM:SS"
  },
  "title_optimizer_output": "object, optional, from 60_title_optimizer",
  "brand_profile": "object, optional, from marca_agent",
  "seo_keywords": "array, optional, max 15 items",
  "video_chapters": "array, optional, timestamp + title pairs",
  "channel_context": {
    "channel_name": "string, optional",
    "default_cta": "string, optional",
    "social_links": "object, optional"
  }
}
```

---

## INTEGRATION MODES

### Mode 1: Pipeline Integration (Post Title Optimizer)

```
┌─────────────────────────────────────────────────────────────┐
│  VIDEO_AGENT PIPELINE                                        │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: concept_planner → $video_brief                    │
│  Phase 2: script_writer → $script                           │
│  Phase 3: visual_prompter → $visual_prompts                 │
│  Phase 4: production_runner → $video_clips                  │
│  Phase 5: editor_assembler → $final_video                   │
│  ────────────────────────────────────────────────────────   │
│  Phase 6+: TITLE OPTIMIZER (103_ADW)                        │
│           Output: $youtube_titles                           │
│                          ↓                                   │
│  Phase 6++: DESCRIPTION OPTIMIZER (this ADW)                │
│           Input: $video_brief + $youtube_titles             │
│           Output: $youtube_description                      │
│                          ↓                                   │
│  YouTube Upload (external)                                   │
└─────────────────────────────────────────────────────────────┘
```

**Trigger**: Automatic after title_optimizer completion
**Input**: `$video_brief` + `$title_optimizer_output` from pipeline
**Output**: Appends `youtube_description` to video_output.json

### Mode 2: Standalone Execution

**Trigger**: `/youtube-description` command or direct API call
**Input**: User-provided brief
**Output**: Standalone `description.json`

---

## PHASE 1: RESEARCH (Strategy Definition)

**Objective**: Extract optimization signals and determine content strategy

**Duration**: ~10 seconds

**HOP Reference**: `prompts/61_description_optimizer_HOP.md` (Phase 1)

### Steps

1. **Parse Video Brief**
   - Extract primary_keyword from `$video_brief.topic`
   - Extract title_final for keyword consistency
   - Parse video_duration for timestamp decision
   - Infer audience needs from target_audience

2. **Load Title Optimizer Context** (if available)
   - Extract keywords used in winning title
   - Maintain psychological angle consistency
   - Echo emotional triggers

3. **Determine Content Strategy**
   ```yaml
   length_decision:
     video < 5min: 300-500 chars (minimal)
     video 5-15min: 500-1000 chars (standard)
     video 15-60min: 1000-2000 chars (detailed)
     video 60min+: 1500-2500 chars (comprehensive)

   timestamp_decision:
     video >= 3min: include timestamps
     video >= 10min: detailed chapters
     video >= 30min: comprehensive TOC
   ```

4. **Load Brand Context** (if available)
   - Parse tone for description style
   - Extract CTA preferences
   - Load social links and boilerplate

### Output

```json
{
  "research_summary": {
    "primary_keyword": "ChatGPT programacao",
    "secondary_keywords": ["prompts", "ia para devs", "produtividade"],
    "core_value_proposition": "Acelerar desenvolvimento com IA",
    "audience_pain_points": ["tempo perdido", "codigo repetitivo"],
    "title_consistency": {
      "keywords_to_echo": ["ChatGPT", "prompts", "dev"],
      "angle_to_maintain": "number",
      "tone_to_match": "energetico"
    },
    "content_strategy": {
      "target_length": 800,
      "include_timestamps": true,
      "timestamp_count": 8,
      "cta_style": "medium",
      "template": "detailed"
    }
  }
}
```

### Quality Gate
- [ ] primary_keyword extracted
- [ ] video_duration parsed correctly
- [ ] content_strategy defined
- [ ] target_length appropriate for video length

---

## PHASE 2: GENERATE (Description Creation)

**Objective**: Generate complete 5-section description

**Duration**: ~15 seconds

**HOP Reference**: `prompts/61_description_optimizer_HOP.md` (Phase 2)

**Config Reference**: `config/youtube_description_rules.json`

### Section Structure

| Section | Purpose | Char Limit | Required |
|---------|---------|------------|----------|
| **Hook** | Above-fold scroll-stopper | 100-150 | Yes |
| **Value Proposition** | What viewer gets | 150-300 | Yes |
| **Timestamps** | Navigation + watch time | Variable | If >= 3min |
| **Links & CTAs** | Conversions, engagement | 200-400 | Yes |
| **Hashtags/Keywords** | Discoverability | 50-100 | Yes |

### Steps

1. **Generate Hook (Above Fold)** 🎯 CRITICAL
   ```
   Position: First 100-150 characters (visible in search)
   Formula: [Keyword] + [Curiosity/Value Hook] + [Promise]

   Banned Openings:
   - "Neste video..."
   - "Ola pessoal..."
   - "E ai galera..."
   ```

2. **Generate Value Proposition**
   ```
   Structure:
   📌 O QUE VOCÊ VAI APRENDER:
   • [Benefit 1]
   • [Benefit 2]
   • [Benefit 3]

   👤 PARA QUEM É:
   • [Audience descriptor]
   ```

3. **Generate Timestamps** (if applicable)
   ```
   Requirements:
   - First timestamp MUST be 00:00
   - Minimum 3 chapters for YouTube feature
   - Ascending order
   - Max 50 chars per title

   Structure:
   ⏱️ CAPÍTULOS:
   00:00 - Introducao
   02:34 - [Chapter 2]
   05:12 - [Chapter 3]
   ```

4. **Generate Links & CTAs**
   ```
   Structure:
   🔗 RECURSOS:
   • [Resource]: [URL]

   📱 ME SIGA:
   • Instagram: [URL]

   🔔 Inscreva-se e ative o sininho!
   ```

5. **Generate Hashtags & Keywords**
   ```
   Structure:
   [Natural keyword sentence]

   #Tag1 #Tag2 #Tag3 #Tag4 #Tag5

   Rules:
   - 3-5 hashtags max
   - Mix: 1 broad + 2-3 specific + 1 branded
   - Natural keyword sentence (not list)
   ```

### Output

```json
{
  "description_generated": {
    "full_text": "ChatGPT para programação: os 7 prompts que vão revolucionar seu workflow...",
    "char_count": 847,
    "sections": {
      "hook": {
        "content": "ChatGPT para programação: os 7 prompts que vão revolucionar seu workflow. Depois de testar 50+ prompts, esses são os que realmente funcionam.",
        "char_count": 142
      },
      "value_proposition": {
        "content": "📌 O QUE VOCÊ VAI APRENDER:\n• Prompt para debug...",
        "char_count": 245
      },
      "timestamps": {
        "content": "⏱️ CAPÍTULOS:\n00:00 - Introdução...",
        "chapters": [
          {"timestamp": "00:00", "title": "Introdução"},
          {"timestamp": "01:45", "title": "Prompt #1: Debug"}
        ],
        "char_count": 180
      },
      "links_ctas": {
        "content": "🔗 RECURSOS:\n• PDF: [link]...",
        "links_count": 4,
        "char_count": 180
      },
      "hashtags_keywords": {
        "content": "Este tutorial de ChatGPT...\n\n#ChatGPT #Programacao #IA",
        "hashtags": ["#ChatGPT", "#Programacao", "#IA", "#DevTips"],
        "char_count": 100
      }
    },
    "keyword_analysis": {
      "primary_keyword": "ChatGPT programacao",
      "occurrences": 3,
      "density": "2.1%",
      "first_position": 0
    }
  }
}
```

### Quality Gate
- [ ] All required sections present
- [ ] Hook <= 150 chars
- [ ] Total <= 5000 chars
- [ ] Keyword in first 25 words
- [ ] Timestamps start at 00:00 (if included)
- [ ] 3-5 hashtags included
- [ ] No banned patterns detected

---

## PHASE 3: VALIDATE (4D Scoring)

**Objective**: Score description, ensure quality gate

**Duration**: ~10 seconds

**HOP Reference**: `prompts/61_description_optimizer_HOP.md` (Phase 3)

### 4D Scoring System

```yaml
dimensions:
  engagement_potential:
    weight: 0.35
    factors:
      - hook_quality (0-3.0): compelling above-fold
      - cta_effectiveness (0-2.0): clear action
      - scanability (0-2.0): bullets, sections
      - value_clarity (0-2.0): clear promise
      - emotional_trigger (0-1.0): curiosity, urgency

  seo_alignment:
    weight: 0.30
    factors:
      - primary_keyword_present (+3.0)
      - keyword_in_first_25_words (+2.0)
      - secondary_keywords (+0.5 each, max 2.0)
      - keyword_density_optimal (+2.0): 1-3%
      - no_keyword_stuffing (+1.0)

  brand_alignment:
    weight: 0.20
    factors:
      - tone_consistency (0-4.0): with title/brand
      - voice_markers (+1.0 each, max 3.0)
      - professional_formatting (0-2.0)
      - cta_style_match (0-1.0)

  technical_compliance:
    weight: 0.15
    factors:
      - char_count_valid (+3.0): under 5000
      - above_fold_optimized (+2.0): 100-150 compelling
      - timestamps_valid (+2.0): if applicable
      - proper_formatting (+2.0)
      - mobile_friendly (+1.0)
```

### Steps

1. **Score Each Dimension**
   - Calculate engagement potential score
   - Calculate SEO alignment score
   - Calculate brand alignment score
   - Calculate technical compliance score
   - Apply weights and sum

2. **Apply Quality Gate**
   - Check if total score >= 7.5
   - If below: identify weakest dimension
   - Regenerate weakest section
   - If still below: flag for human review

3. **Generate Optimization Notes**
   - Highlight strengths
   - Note areas for improvement
   - Suggest A/B test variations

### Output

```json
{
  "description_scored": {
    "full_text": "...",
    "char_count": 847,
    "scores": {
      "engagement": 8.5,
      "seo": 8.2,
      "brand": 7.8,
      "technical": 9.0
    },
    "score_total": 8.35,
    "above_quality_gate": true
  },
  "optimization_notes": [
    "Hook is strong - curiosity gap established",
    "Consider adding 1 more secondary keyword",
    "Timestamps properly formatted for chapters"
  ],
  "preview": {
    "above_fold": "ChatGPT para programação: os 7 prompts que vão revolucionar...",
    "char_count_preview": 142,
    "truncation_safe": true
  }
}
```

### Quality Gate
- [ ] Total score >= 7.5
- [ ] Hook score >= 7.0
- [ ] SEO score >= 7.0
- [ ] No critical issues flagged

---

## SUCCESS CRITERIA

### All Phases Complete
- [ ] Phase 1: research_summary with content_strategy
- [ ] Phase 2: 5-section description generated
- [ ] Phase 3: scores calculated, quality gate passed

### Quality Thresholds
- [ ] Total score >= 7.5
- [ ] Total chars <= 5000
- [ ] Hook <= 150 chars (compelling)
- [ ] Keyword density 1-3%
- [ ] Timestamps valid (if applicable)

### Output Complete
- [ ] description.json or pipeline integration
- [ ] Scoring breakdown
- [ ] Optimization notes
- [ ] Above-fold preview

---

## ERROR HANDLING

### Phase 1 Failure
- **Cause**: Missing required brief fields
- **Action**: Return validation error with missing fields

### Phase 2 Failure
- **Cause**: Unable to generate section
- **Action**: Use template fallback, flag section

### Phase 3 Failure
- **Cause**: Score below threshold
- **Action**:
  1. Identify weakest dimension
  2. Regenerate that section
  3. If still below 7.5: flag for human review
  4. Return best available with warning

### Recovery
- Phases are stateless, can retry any phase
- Section-level regeneration supported

---

## USAGE EXAMPLES

### Example 1: Pipeline Integration (Post Title Optimizer)

```python
# After title_optimizer completes
from video_agent import description_optimizer

# Automatic extraction from pipeline context
result = description_optimizer.run(
    video_brief=pipeline.video_brief,
    title_optimizer_output=pipeline.youtube_titles,
    brand_profile=pipeline.brand_profile  # if available
)

# Result appended to video_output.json
pipeline.video_output["youtube_description"] = result
```

### Example 2: Standalone Command

```bash
# Via slash command
/youtube-description "7 Prompts de ChatGPT, duracao 12:34, publico devs iniciantes, beneficio acelerar desenvolvimento"
```

### Example 3: Direct API

```json
{
  "mode": "description_optimizer",
  "input": {
    "video_brief": {
      "title_final": "7 Prompts de ChatGPT Que Todo Dev Precisa",
      "topic": "ChatGPT programacao",
      "target_audience": "Desenvolvedores iniciantes",
      "key_benefit": "Acelerar desenvolvimento",
      "video_duration": "12:34"
    },
    "video_chapters": [
      {"timestamp": "00:00", "title": "Introducao"},
      {"timestamp": "01:45", "title": "Prompt #1"},
      {"timestamp": "03:22", "title": "Prompt #2"}
    ]
  }
}
```

---

## METRICS TO TRACK

```json
{
  "workflow_metrics": {
    "total_time_seconds": 35,
    "phases_completed": 3,
    "quality_score": 8.35
  },
  "generation_metrics": {
    "total_chars": 847,
    "sections_generated": 5,
    "timestamps_count": 8,
    "hashtags_count": 4
  },
  "scoring_breakdown": {
    "engagement_score": 8.5,
    "seo_score": 8.2,
    "brand_score": 7.8,
    "technical_score": 9.0
  },
  "seo_metrics": {
    "keyword_density": "2.1%",
    "keyword_position": 0,
    "secondary_keywords_used": 3
  }
}
```

---

## CONFIGURATION FILES

### config/youtube_description_rules.json
Complete configuration with section formulas, scoring weights, templates, and power phrases.

### prompts/61_description_optimizer_HOP.md
Core HOP with 3-phase execution logic.

### schemas/description_optimizer_input.json
Input validation schema.

---

## VERSION HISTORY

### v1.0.0 (2025-12-04)
- Initial ADW implementation
- 3-phase workflow (Research → Generate → Validate)
- 5-section description structure
- 4D scoring system
- Pipeline and standalone modes
- Timestamp generation support

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-04
**Status**: Production Ready
**HOP Reference**: prompts/61_description_optimizer_HOP.md
**Predecessor**: 103_ADW_YOUTUBE_TITLE.md
