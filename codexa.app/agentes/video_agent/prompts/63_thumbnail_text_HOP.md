# HOP: YouTube Thumbnail Text Optimizer | video_agent Stage 6+++

## MODULE_METADATA
```yaml
id: video_agent_thumbnail_text_optimizer
version: 1.0.0
purpose: Generate CTR-optimized thumbnail text variants (3-5 words max)
dependencies: [anthropic_api, youtube_thumbnail_rules.json]
category: youtube_optimization
stage: 6+++
integration: post_tags_optimizer OR standalone
```

## INPUT_CONTRACT
```yaml
required:
  $title_final:
    type: string
    source: title_optimizer output
    description: Final YouTube title for message alignment

  $video_brief:
    type: object
    description: Video brief from previous stages
    structure:
      topic: string (primary keyword)
      key_benefit: string (main value proposition)
      target_audience: string
      video_duration: string (MM:SS)

optional:
  $brand_profile:
    type: object
    description: Brand voice, tone, colors for consistency
    structure:
      tone_scale: object
      primary_color: string (hex)
      archetypes: array
      voice_markers: array

  $thumbnail_context:
    type: object
    description: Existing thumbnail design elements
    structure:
      background_color: string
      has_product_image: boolean
      text_position: enum["top", "center", "bottom"]
      design_style: enum["minimalist", "bold", "luxury", "playful"]

  $competitor_thumbnails:
    type: array
    description: Analysis of competitor text patterns
    max_items: 5
```

## OUTPUT_CONTRACT
```yaml
primary:
  thumbnail_texts.json:
    type: object
    structure:
      variants: array[ThumbnailVariant]
      recommended: ThumbnailVariant
      scoring_breakdown: object
      design_integration: object
      metadata: object

ThumbnailVariant:
  type: object
  structure:
    text: string (3-5 words, max 40 chars)
    word_count: integer (3-5)
    char_count: integer (max 40)
    angle: enum[hook, benefit, curiosity, urgency, transformation]
    score_total: float (0-10)
    score_breakdown:
      readability: float (weight: 0.30)
      message_consistency: float (weight: 0.25)
      psychology_impact: float (weight: 0.25)
      typography_fit: float (weight: 0.20)
    design_spec:
      font_size_px: integer (20-40)
      font_weight: enum["semi-bold", "bold", "extra-bold"]
      case: enum["title_case", "all_caps", "mixed"]
      contrast_category: enum["high", "medium", "flexible"]
      all_caps_recommended: boolean
    ctr_multiplier: float
```

## TASK

**Role**: YouTube Thumbnail Text Optimization Specialist

**Objective**: Generate 3-5 high-CTR thumbnail text variants using psychological angles, score using 4D system, and ensure message consistency with title while maximizing visual impact.

**Standards**:
- ALWAYS generate exactly 3 core variants (one per primary angle)
- ALWAYS stay within 3-5 word limit (max 40 characters)
- ALWAYS reinforce (not duplicate) title message
- NEVER use same emotional angle as title
- NEVER exceed readability limits for mobile thumbnails
- APPLY psychological triggers appropriate to angle

**Constraints**:
- Word count: 3-5 words (optimal: 4)
- Character limit: 40 max
- Quality gate: overall score >= 7.5/10
- Message consistency: topic overlap >= 70% with title
- Angle differentiation: must differ from title angle

---

## PHASES

### PHASE 1: ANALYZE (10s)
**Objective**: Extract optimization signals from title and brief

```yaml
analysis_extraction:
  from_title:
    - primary_keyword: main topic from title
    - title_angle: psychological angle used (question, number, etc.)
    - title_emotion: primary emotional register
    - title_benefit: value proposition stated

  from_video_brief:
    - topic: core subject matter
    - key_benefit: main transformation/result
    - audience: who thumbnail speaks to

  from_brand_profile:
    - tone_match: formal vs casual scale
    - color_palette: contrast recommendations
    - design_style: minimalist, bold, etc.

  consistency_requirements:
    - topic_must_align: thumbnail reinforces title topic
    - angle_must_differ: different psychological trigger
    - emotion_must_complement: not duplicate
```

**Output Phase 1**:
```json
{
  "analysis_summary": {
    "title_primary_keyword": "string",
    "title_angle": "enum",
    "title_emotion": "string",
    "title_benefit": "string",
    "recommended_thumbnail_angles": ["hook", "benefit", "urgency"],
    "forbidden_angle": "number (same as title)"
  }
}
```

---

### PHASE 2: GENERATE (15s)
**Objective**: Create 3-5 thumbnail text variants using different psychological angles

#### PSYCHOLOGICAL ANGLES

**ANGLE A - HOOK** (Pattern Interrupt) | CTR: 1.18x
```
Purpose: Stop the scroll with unexpected statement
Psychology: Novelty, attention-capture, pattern interrupt
Formula: [Surprising Adjective] + [Noun] OR [Emotion] + [Benefit]

Examples PT-BR:
  - "Revelação Chocante"
  - "Método Proibido"
  - "Erro Comum"
  - "Descobri Isso"

Word Count: 2-4 words
Best For: Myth-busting, exposés, controversial angles
```

**ANGLE B - BENEFIT** (Value Proposition) | CTR: 1.32x ⭐ BEST
```
Purpose: Communicate clear transformation/result
Psychology: Clarity, aspiration, outcome focus
Formula: [Verb] + [Quantity/Time] + [Result]

Examples PT-BR:
  - "Ganhe R$10k"
  - "2x Produtividade"
  - "Perca 10kg"
  - "Salve 5 Horas"

Word Count: 2-4 words
Best For: Educational, self-improvement, results-focused
```

**ANGLE C - CURIOSITY** (Intrigue) | CTR: 1.25x
```
Purpose: Create information gap
Psychology: Incompleteness, mystery, open loop
Formula: [Unexpected Pairing] OR [Unfinished Promise]

Examples PT-BR:
  - "Ninguém Sabia..."
  - "Segredo Revelado"
  - "Você Fazia Errado"
  - "Antes vs Depois"

Word Count: 2-4 words
Best For: Comparisons, reveals, tutorials
```

**ANGLE D - URGENCY** (Scarcity/Time) | CTR: 1.20x
```
Purpose: Drive immediate action
Psychology: FOMO, scarcity, deadline pressure
Formula: [Time/Quantity] + [Resource] OR [Action] + [Now]

Examples PT-BR:
  - "Últimas 48h"
  - "Vagas Limitadas"
  - "Clique Agora"
  - "Não Perca"

Word Count: 2-3 words (shorter = more urgent)
Best For: Promotions, limited offers, time-bound content
⚠️ Only if video has genuine urgency
```

**ANGLE E - TRANSFORMATION** (Before/After) | CTR: 1.28x
```
Purpose: Show concrete progression/results
Psychology: Progress, achievement, aspiration
Formula: [Starting Point] → [End Result] OR [Problem] ✓ [Solution]

Examples PT-BR:
  - "Iniciante → Expert"
  - "Caótico ✓ Organizado"
  - "0 → 100k"
  - "Perdido ✓ Encontrado"

Word Count: 3-5 words (with symbol)
Best For: Tutorials, success stories, step-by-step
```

#### GENERATION RULES

```yaml
character_rules:
  word_count_min: 3
  word_count_max: 5
  word_count_optimal: 4
  char_count_max: 40
  char_count_optimal: 25-32

consistency_rules:
  topic_overlap_min: 0.70
  angle_must_differ_from_title: true
  emotion_must_complement: true
  no_title_duplication: true

typography_rules:
  font_size_tiers:
    - chars_0_20: "32-40px (large)"
    - chars_21_30: "28-32px (standard)"
    - chars_31_40: "20-27px (minimum)"
  mobile_minimum_effective: "14px"
  font_weight_minimum: "semi-bold (600)"

case_recommendations:
  hook: "ALL CAPS or Title Case"
  benefit: "Mixed with numeric"
  curiosity: "Title Case"
  urgency: "ALL CAPS (2-3 words only)"
  transformation: "Mixed with symbol"

banned_patterns:
  - title_exact_copy: "Wastes opportunity"
  - all_caps_5_words: "Unreadable"
  - generic_cta: "Clique Aqui (no value)"
  - emoji_overload: "Max 1 emoji"
```

**Output Phase 2**:
```json
{
  "variants_generated": [
    {
      "variant_id": "A",
      "text": "Hack Secreto",
      "word_count": 2,
      "char_count": 12,
      "angle": "hook",
      "ctr_multiplier": 1.18,
      "triggers_used": ["pattern_interrupt", "exclusivity"]
    },
    {
      "variant_id": "B",
      "text": "2x Mais Rápido",
      "word_count": 3,
      "char_count": 14,
      "angle": "benefit",
      "ctr_multiplier": 1.32,
      "triggers_used": ["specificity", "transformation"]
    },
    {
      "variant_id": "C",
      "text": "Ninguém Conta",
      "word_count": 2,
      "char_count": 13,
      "angle": "curiosity",
      "ctr_multiplier": 1.25,
      "triggers_used": ["information_gap", "exclusivity"]
    }
  ]
}
```

---

### PHASE 3: VALIDATE (10s)
**Objective**: Score all variants using 4D system, select winner

#### 4D SCORING SYSTEM

```yaml
scoring_dimensions:
  readability:
    weight: 0.30
    description: Visual clarity at thumbnail scale
    factors:
      - word_count_optimal: +3.0 (4 words ideal)
      - char_count_efficient: +2.0 (25-32 chars)
      - font_size_feasible: +2.0 (28px+ achievable)
      - case_appropriate: +2.0 (matches angle)
      - no_truncation_risk: +1.0 (mobile safe)
    max_score: 10.0

  message_consistency:
    weight: 0.25
    description: Alignment with title without duplication
    factors:
      - topic_overlap: +3.0 (70%+ alignment)
      - angle_differentiation: +3.0 (different from title)
      - benefit_reinforcement: +2.0 (same core promise)
      - no_contradiction: +2.0 (consistent message)
    max_score: 10.0

  psychology_impact:
    weight: 0.25
    description: Click-through potential
    factors:
      - ctr_multiplier: +3.0 (based on angle)
      - trigger_count: +2.0 (emotional triggers used)
      - power_word_presence: +2.0 (from power words list)
      - conflict_or_contrast: +2.0 (transformation angle)
      - specificity: +1.0 (numbers, stats)
    max_score: 10.0

  typography_fit:
    weight: 0.20
    description: Design implementation feasibility
    factors:
      - case_matches_angle: +3.0
      - font_weight_feasible: +2.0 (bold achievable)
      - contrast_appropriate: +2.0 (high/medium/flexible)
      - symbol_optimization: +2.0 (for transformation)
      - mobile_preview_safe: +1.0
    max_score: 10.0
```

#### SCORING CALCULATION

```python
def calculate_4d_score(variant: ThumbnailVariant, context: dict) -> float:
    scores = {
        "readability": score_readability(variant),
        "consistency": score_message_consistency(variant, context),
        "psychology": score_psychology_impact(variant),
        "typography": score_typography_fit(variant)
    }

    weights = {"readability": 0.30, "consistency": 0.25, "psychology": 0.25, "typography": 0.20}

    total = sum(scores[dim] * weights[dim] for dim in scores)
    return round(total, 2)
```

#### QUALITY GATE

```yaml
quality_gate:
  minimum_score: 7.5
  actions:
    if_all_below_threshold:
      - regenerate_weakest_variant
      - try_alternative_angle
      - if_still_below: flag_for_human_review
    if_any_above_threshold:
      - recommend_highest_scorer
      - provide_alternatives_above_7.0
```

**Output Phase 3**:
```json
{
  "variants_scored": [
    {
      "variant_id": "B",
      "text": "2x Mais Rápido",
      "angle": "benefit",
      "scores": {
        "readability": 9.2,
        "consistency": 8.8,
        "psychology": 8.6,
        "typography": 8.0
      },
      "score_total": 8.72,
      "ctr_multiplier": 1.32
    }
  ],
  "recommended": {
    "variant_id": "B",
    "text": "2x Mais Rápido",
    "score_total": 8.72,
    "rationale": "Benefit angle (1.32x CTR) + clear numeric outcome + high readability",
    "design_spec": {
      "font_size_px": 32,
      "font_weight": "semi-bold",
      "case": "Mixed",
      "contrast": "high",
      "position": "center"
    }
  },
  "alternatives": [
    {
      "variant_id": "A",
      "text": "Hack Secreto",
      "score_total": 8.45,
      "reason": "Good hook angle if more intrigue desired"
    }
  ]
}
```

---

## VALIDATION

### Quality Gates

```yaml
quality_gates:
  - name: word_count
    check: 3 <= word_count <= 5
    action: trim_or_expand

  - name: char_count
    check: char_count <= 40
    action: shorten_or_abbreviate

  - name: topic_alignment
    check: topic_overlap >= 0.70
    action: regenerate_with_title_reference

  - name: angle_differentiation
    check: angle != title_angle
    action: switch_to_different_angle

  - name: minimum_score
    check: score_total >= 7.5
    action: enhance_or_flag

  - name: variant_count
    check: len(variants) >= 3
    action: generate_more_variants

  - name: no_title_duplication
    check: text != title_text[:len(text)]
    action: regenerate
```

### Thresholds

```yaml
thresholds:
  score_excellent: 9.0
  score_good: 7.5
  score_acceptable: 6.5
  score_reject: < 6.5

  word_count_min: 3
  word_count_max: 5
  word_count_optimal: 4

  char_count_max: 40
  char_count_optimal_min: 25
  char_count_optimal_max: 32

  topic_overlap_min: 0.70
  font_size_min_px: 20
```

---

## CONTEXT

**Usage**:
- Called by video_agent after tags_optimizer for complete YouTube metadata
- Can be invoked standalone via `/youtube-thumbnail-text` command

**Upstream**:
- $title_final from 60_title_optimizer_HOP (required)
- $video_brief from 10_concept_planner_HOP
- $brand_profile from marca_agent (optional)

**Downstream**:
- Thumbnail designer/template system
- Photo_agent for thumbnail generation
- YouTube upload metadata

**$arguments chaining**:
```
title_optimizer.recommended -> thumbnail_text_optimizer($title_final)
thumbnail_text_optimizer.recommended -> thumbnail_designer($text_spec)
thumbnail_text_optimizer.design_spec -> photo_agent($text_overlay)
```

**Integration Modes**:
```yaml
mode_integrated:
  trigger: after tags_optimizer completion
  input: $title_final + $video_brief + $brand_profile
  output: appends to video_output.json

mode_standalone:
  trigger: /youtube-thumbnail-text command
  input: direct title + brief
  output: standalone thumbnail_texts.json
```

---

## EXAMPLES

### Example 1: Tech Tutorial

**Input**:
```json
{
  "title_final": "7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer",
  "video_brief": {
    "topic": "ChatGPT programação",
    "key_benefit": "Acelerar desenvolvimento com IA",
    "target_audience": "Desenvolvedores"
  }
}
```

**Output**:
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
    },
    "rationale": "Title uses NUMBER angle (7 prompts), thumbnail uses BENEFIT angle (speed) - complementary"
  },
  "alternatives": [
    {
      "text": "Hack Secreto",
      "angle": "hook",
      "score_total": 8.45
    },
    {
      "text": "Código Mais Rápido",
      "angle": "transformation",
      "score_total": 8.32
    }
  ]
}
```

### Example 2: Product Review

**Input**:
```json
{
  "title_final": "iPhone 15 Pro: 40h de Bateria é Real? (Teste Completo)",
  "video_brief": {
    "topic": "iPhone 15 Pro review",
    "key_benefit": "Decisão de compra informada",
    "target_audience": "Consumidores tech-savvy"
  }
}
```

**Output**:
```json
{
  "recommended": {
    "text": "Vale a Pena?",
    "angle": "curiosity",
    "score_total": 8.65,
    "design_spec": {
      "font_size_px": 36,
      "font_weight": "bold",
      "case": "Title Case",
      "contrast": "high"
    },
    "rationale": "Title uses QUESTION angle, thumbnail uses CURIOSITY - creates double intrigue"
  }
}
```

---

## DESIGN INTEGRATION GUIDE

### Font Size Reference

| Character Count | Font Size | Readability |
|-----------------|-----------|-------------|
| 0-20 chars | 32-40px | Excellent |
| 21-30 chars | 28-32px | Good |
| 31-40 chars | 20-27px | Acceptable |
| 40+ chars | <20px | Poor (avoid) |

### Case Recommendations by Angle

| Angle | Recommended Case | Example |
|-------|------------------|---------|
| Hook | ALL CAPS (2-3 words) | "HACK SECRETO" |
| Benefit | Mixed with numeric | "2x Mais Rápido" |
| Curiosity | Title Case | "Ninguém Sabia" |
| Urgency | ALL CAPS | "ÚLTIMAS 48H" |
| Transformation | Mixed + symbol | "Iniciante → Expert" |

### Contrast Requirements

| Category | When to Use | Background Recommendation |
|----------|-------------|---------------------------|
| High | Hook, Urgency | Dark semi-transparent overlay |
| Medium | Benefit, Transform | Gradient or brand color |
| Flexible | Curiosity | Depends on image |

---

## INTEGRATION WITH VIDEO_AGENT PIPELINE

```
┌─────────────────────────────────────────────────────────────┐
│  VIDEO_AGENT PIPELINE                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1-5: Video Production Pipeline                       │
│                                                              │
│  ────────────────────────────────────────────────────────   │
│                          ↓                                   │
│  Phase 6+: TITLE OPTIMIZER                                  │
│           Output: $youtube_titles                           │
│                          ↓                                   │
│  Phase 6++: DESCRIPTION OPTIMIZER                           │
│           Output: $youtube_description                      │
│                          ↓                                   │
│  Phase 6+++: TAGS OPTIMIZER                                 │
│           Output: $youtube_tags                             │
│                          ↓                                   │
│  Phase 6++++: THUMBNAIL TEXT OPTIMIZER (this HOP)           │
│           Input: $title_final, $video_brief                 │
│           Output: $thumbnail_texts                          │
│                          ↓                                   │
│  Phase 7: YouTube Upload + Thumbnail Design                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0
**Created**: 2025-12-04
**Author**: codexa_agent (meta-construction)
**Config**: config/youtube_thumbnail_rules.json
**Predecessor**: 62_tags_optimizer_HOP.md
