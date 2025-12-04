# ADW-103: YouTube Title Optimizer Workflow

**Version**: 1.0.0
**Duration**: 30-60 seconds
**Phases**: 3 (Research → Generate → Validate)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_youtube_title",
  "workflow_name": "YouTube Title Optimizer Workflow",
  "agent": "video_agent",
  "version": "1.0.0",
  "context_strategy": "minimal",
  "failure_handling": "retry_then_fallback",
  "min_llm_model": "claude-sonnet-4+",
  "required_capabilities": {
    "title_optimization": true,
    "seo_analysis": true,
    "brand_alignment": true
  },
  "phases": [
    {"phase_id": "phase_1_research", "phase_name": "Research Extraction", "duration": "~10s", "description": "Extract optimization signals from input"},
    {"phase_id": "phase_2_generate", "phase_name": "Title Generation", "duration": "~15s", "description": "Generate 5 title candidates using psychological formulas"},
    {"phase_id": "phase_3_validate", "phase_name": "Scoring & Validation", "duration": "~10s", "description": "Score all titles with 4D system, select winner"}
  ]
}
```

---

## OVERVIEW

This ADW orchestrates YouTube title optimization with CTR-focused generation:

```
Research → Generate → Validate → Recommended Title + Alternatives
```

**Key Features**:
- 5 psychological title angles (Question, Number, Social Proof, How-To, Comparison)
- 4D scoring system (CTR 35%, SEO 30%, Brand 20%, Technical 15%)
- Quality gate: minimum score >= 7.5
- Integration with video_agent pipeline (post Phase 6) or standalone

---

## PRE-REQUISITES

### Required
- [ ] Anthropic API key (Claude Sonnet 4+)
- [ ] video_brief OR direct input

### Optional
- [ ] brand_profile from marca_agent
- [ ] seo_keywords from pesquisa_agent
- [ ] competitor_titles for gap analysis

### Input Schema
```json
{
  "video_brief": {
    "title_working": "string, required, 5-100 chars",
    "topic": "string, required, primary keyword",
    "target_audience": "string, required",
    "key_benefit": "string, required"
  },
  "brand_profile": "object, optional, from marca_agent",
  "seo_keywords": "array, optional, max 10 items",
  "competitor_titles": "array, optional, max 5 items",
  "channel_context": {
    "subscriber_count": "integer, optional",
    "niche": "string, optional",
    "avg_ctr": "float, optional"
  }
}
```

---

## INTEGRATION MODES

### Mode 1: Pipeline Integration (Post Phase 6)

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
│                          ↓                                   │
│  Phase 6+: TITLE OPTIMIZER (this ADW)                       │
│           Input: $video_brief from Phase 1                  │
│           Output: $youtube_titles                           │
│                          ↓                                   │
│  YouTube Upload (external)                                   │
└─────────────────────────────────────────────────────────────┘
```

**Trigger**: Automatic after Phase 5 completion
**Input**: `$video_brief` from pipeline context
**Output**: Appends `youtube_titles` to video_output.json

### Mode 2: Standalone Execution

**Trigger**: `/youtube-title` command or direct API call
**Input**: User-provided brief
**Output**: Standalone `titles.json`

---

## PHASE 1: RESEARCH (Signal Extraction)

**Objective**: Extract optimization signals from all available inputs

**Duration**: ~10 seconds

**HOP Reference**: `prompts/60_title_optimizer_HOP.md` (Phase 1)

### Steps

1. **Parse Video Brief**
   - Extract primary_keyword from `$video_brief.topic`
   - Infer secondary keywords from topic context
   - Extract core_benefit from `$video_brief.key_benefit`
   - Infer audience_pain from `$video_brief.target_audience`

2. **Load Brand Context** (if available)
   - Parse tone_scale for title style mapping
   - Extract voice_markers for PT-BR patterns
   - Identify archetypal triggers

3. **Analyze Competitors** (if available)
   - Identify successful patterns
   - Note overused/banned patterns
   - Find gap opportunities

4. **Extract Channel Context** (if available)
   - Note performance baseline (avg_ctr)
   - Understand niche conventions
   - Identify audience familiarity level

### Output

```json
{
  "research_summary": {
    "primary_keyword": "Marketing Digital",
    "secondary_keywords": ["marketing online", "vendas online", "estrategia digital"],
    "core_benefit": "Aumentar vendas em 30 dias",
    "audience_pain": "Frustração com resultados lentos",
    "tone_target": "energetico",
    "competitor_gaps": ["no one addresses timeline specifically"],
    "brand_voice_markers": ["direto", "prático", "resultados"]
  }
}
```

### Quality Gate
- [ ] primary_keyword extracted
- [ ] core_benefit identified
- [ ] audience_pain inferred
- [ ] tone_target set (default: energetico)

---

## PHASE 2: GENERATE (Title Creation)

**Objective**: Generate exactly 5 title candidates, one per psychological angle

**Duration**: ~15 seconds

**HOP Reference**: `prompts/60_title_optimizer_HOP.md` (Phase 2)

**Config Reference**: `config/youtube_title_rules.json`

### Title Formulas

| Angle | Formula | CTR Multiplier | Best For |
|-------|---------|----------------|----------|
| **A - Question** | `[Keyword] + [Question]?` | 1.25x | Educational, myth-busting |
| **B - Number** | `[N] + [Benefit] + [Keyword]` | 1.36x ⭐ | Lists, tutorials |
| **C - Social Proof** | `[Keyword] + [Transformation]` | 1.18x | Case studies, results |
| **D - How-To** | `Como + [Action] + [Keyword]` | 1.22x | Tutorials, guides |
| **E - Comparison** | `[A] vs [B] + [Decision]` | 1.30x | Reviews, comparisons |

### Generation Rules

```yaml
character_rules:
  total_limit: 50-70
  optimal_range: 55-65
  keyword_position: <= 40 chars from start
  mobile_preview: first 45 chars must hook

formatting_rules:
  capitalization: Title Case
  connectors_max: 2
  numbers_format: digits (7 not "sete")
  question_ending: "?"
```

### Steps

1. **Generate Title A (Question)**
   - Apply question formula with research.primary_keyword
   - Inject curiosity gap trigger
   - Target 50-60 chars

2. **Generate Title B (Number)**
   - Select optimal number (3, 5, 7, 10, 15)
   - Apply number formula
   - Include specificity trigger

3. **Generate Title C (Social Proof)**
   - Apply transformation formula
   - Include authority trigger
   - Reference results if available

4. **Generate Title D (How-To)**
   - Apply utility formula
   - Include action verb
   - Add qualifier for specificity

5. **Generate Title E (Comparison)**
   - Identify comparison opportunity
   - Apply decision-helper formula
   - Create completeness trigger

### Output

```json
{
  "titles_generated": [
    {
      "angle": "question",
      "text": "Marketing Digital: Você Está Cometendo Esses 5 Erros?",
      "char_count": 54,
      "keyword_position": 0,
      "ctr_multiplier": 1.25,
      "triggers_used": ["curiosity", "self_assessment"]
    },
    {
      "angle": "number",
      "text": "7 Estratégias de Marketing Digital Que Triplicam Vendas",
      "char_count": 56,
      "keyword_position": 17,
      "ctr_multiplier": 1.36,
      "triggers_used": ["specificity", "transformation"]
    },
    {
      "angle": "social_proof",
      "text": "Marketing Digital: O Método Que Me Deu R$100k em 30 Dias",
      "char_count": 57,
      "keyword_position": 0,
      "ctr_multiplier": 1.18,
      "triggers_used": ["authority", "specificity", "transformation"]
    },
    {
      "angle": "how_to",
      "text": "Como Fazer Marketing Digital Que Realmente Converte",
      "char_count": 51,
      "keyword_position": 11,
      "ctr_multiplier": 1.22,
      "triggers_used": ["utility", "clarity"]
    },
    {
      "angle": "comparison",
      "text": "Tráfego Pago vs Orgânico: Qual Estratégia Escolher em 2024",
      "char_count": 59,
      "keyword_position": 0,
      "ctr_multiplier": 1.30,
      "triggers_used": ["decision_relief", "curiosity"]
    }
  ]
}
```

### Quality Gate
- [ ] Exactly 5 titles generated
- [ ] All unique angles represented
- [ ] All within 50-70 char limit
- [ ] Keyword in first 40 chars for all
- [ ] No banned patterns detected

---

## PHASE 3: VALIDATE (4D Scoring)

**Objective**: Score all titles, select winner, provide alternatives

**Duration**: ~10 seconds

**HOP Reference**: `prompts/60_title_optimizer_HOP.md` (Phase 3)

### 4D Scoring System

```yaml
dimensions:
  ctr_prediction:
    weight: 0.35
    factors:
      - angle_multiplier (1.0-1.36)
      - power_words (+0.5 each, max 1.5)
      - curiosity_gap (+1.0)
      - specificity (+0.5)
      - mobile_hook (+0.5)

  seo_alignment:
    weight: 0.30
    factors:
      - primary_keyword_present (+3.0)
      - keyword_position <= 40 (+2.0)
      - secondary_keywords (+0.5 each)
      - search_intent_match (+2.0)
      - differentiation (+1.0)

  brand_alignment:
    weight: 0.20
    factors:
      - tone_match (0-4.0)
      - voice_markers (+1.0 each)
      - archetype_alignment (+2.0)
      - audience_fit (+1.0)

  technical_compliance:
    weight: 0.15
    factors:
      - char_count_valid (+3.0)
      - optimal_range (+1.0)
      - no_banned_patterns (+3.0)
      - proper_formatting (+2.0)
      - mobile_safe (+1.0)
```

### Steps

1. **Score Each Title**
   - Calculate CTR prediction score
   - Calculate SEO alignment score
   - Calculate brand alignment score
   - Calculate technical compliance score
   - Apply weights and sum

2. **Apply Quality Gate**
   - Check if max score >= 7.5
   - If all below: trigger enhancement pass
   - If still below: flag for human review

3. **Rank and Select**
   - Sort by total score descending
   - Select highest as recommended
   - Include all >= 7.0 as alternatives

4. **Generate Rationale**
   - Explain why recommended title won
   - Note strengths and tradeoffs
   - Provide A/B testing suggestions

### Output

```json
{
  "titles_scored": [
    {
      "text": "7 Estratégias de Marketing Digital Que Triplicam Vendas",
      "angle": "number",
      "char_count": 56,
      "keyword_position": 17,
      "scores": {
        "ctr": 9.2,
        "seo": 8.5,
        "brand": 7.8,
        "technical": 9.5
      },
      "score_total": 8.72,
      "ctr_multiplier": 1.36
    },
    {
      "text": "Tráfego Pago vs Orgânico: Qual Estratégia Escolher em 2024",
      "angle": "comparison",
      "char_count": 59,
      "scores": {
        "ctr": 8.8,
        "seo": 8.0,
        "brand": 7.5,
        "technical": 9.0
      },
      "score_total": 8.38,
      "ctr_multiplier": 1.30
    }
    // ... 3 more
  ],
  "recommended": {
    "index": 0,
    "text": "7 Estratégias de Marketing Digital Que Triplicam Vendas",
    "score_total": 8.72,
    "rationale": "Number angle (1.36x CTR multiplier) + strong keyword position + transformation trigger. Best predicted CTR among all candidates."
  },
  "alternatives": [
    {
      "text": "Tráfego Pago vs Orgânico: Qual Estratégia Escolher em 2024",
      "score_total": 8.38,
      "use_case": "Good for comparison/decision content"
    }
  ],
  "ab_test_suggestion": {
    "variant_a": "7 Estratégias de Marketing Digital Que Triplicam Vendas",
    "variant_b": "Tráfego Pago vs Orgânico: Qual Estratégia Escolher em 2024",
    "hypothesis": "Number angle should outperform by ~5% CTR"
  }
}
```

### Quality Gate
- [ ] At least 1 title >= 7.5 score
- [ ] Recommended title selected
- [ ] Rationale provided
- [ ] A/B suggestion included

---

## SUCCESS CRITERIA

### All Phases Complete
- [ ] Phase 1: research_summary generated
- [ ] Phase 2: 5 titles generated (all angles)
- [ ] Phase 3: scores calculated, winner selected

### Quality Thresholds
- [ ] Recommended title score >= 7.5
- [ ] All titles within 50-70 chars
- [ ] Keyword position <= 40 for all
- [ ] No banned patterns detected

### Output Complete
- [ ] titles.json or pipeline integration
- [ ] recommended title with rationale
- [ ] alternatives list
- [ ] A/B test suggestion

---

## ERROR HANDLING

### Phase 1 Failure
- **Cause**: Missing required brief fields
- **Action**: Return validation error with missing fields

### Phase 2 Failure
- **Cause**: Unable to generate valid title for angle
- **Action**: Retry with alternative approach, skip angle if impossible

### Phase 3 Failure
- **Cause**: All scores below threshold
- **Action**:
  1. Run enhancement pass on lowest scorer
  2. If still below 7.5: flag for human review
  3. Return best available with warning

### Recovery
- Phases are stateless, can retry any phase
- No intermediate state to recover

---

## USAGE EXAMPLES

### Example 1: Pipeline Integration

```python
# After Phase 5 (editor_assembler) completes
from video_agent import title_optimizer

# Automatic extraction from pipeline context
result = title_optimizer.run(
    video_brief=pipeline.video_brief,
    brand_profile=pipeline.brand_profile  # if available
)

# Result appended to video_output.json
pipeline.video_output["youtube_titles"] = result
```

### Example 2: Standalone Command

```bash
# Via slash command
/youtube-title "Como usar ChatGPT para programar, público devs iniciantes, benefício acelerar desenvolvimento"
```

### Example 3: Direct API

```json
{
  "mode": "title_optimizer",
  "input": {
    "video_brief": {
      "title_working": "Review do Fone XYZ",
      "topic": "Fone Bluetooth",
      "target_audience": "Tech enthusiasts",
      "key_benefit": "40h bateria, ANC"
    }
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
    "quality_score": 8.72
  },
  "generation_metrics": {
    "titles_generated": 5,
    "titles_above_threshold": 4,
    "best_angle": "number",
    "best_ctr_multiplier": 1.36
  },
  "scoring_breakdown": {
    "avg_ctr_score": 8.5,
    "avg_seo_score": 8.0,
    "avg_brand_score": 7.6,
    "avg_technical_score": 9.0
  }
}
```

---

## CONFIGURATION FILES

### config/youtube_title_rules.json
Complete configuration with formulas, scoring weights, banned patterns, and power words.

### prompts/60_title_optimizer_HOP.md
Core HOP with 3-phase execution logic.

---

## VERSION HISTORY

### v1.0.0 (2025-12-04)
- Initial ADW implementation
- 3-phase workflow (Research → Generate → Validate)
- 5 psychological title angles
- 4D scoring system
- Pipeline and standalone modes
- A/B testing suggestions

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-04
**Status**: Production Ready
**HOP Reference**: prompts/60_title_optimizer_HOP.md
