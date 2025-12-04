# HOP: YouTube Title Optimizer | video_agent Stage 6+

## MODULE_METADATA
```yaml
id: video_agent_title_optimizer
version: 1.0.0
purpose: Generate CTR-optimized YouTube titles with 4D scoring
dependencies: [anthropic_api, youtube_title_rules.json]
category: youtube_optimization
stage: 6+
integration: post_editor_assembler OR standalone
```

## INPUT_CONTRACT
```yaml
required:
  $video_brief:
    type: object
    description: Video brief from previous stages OR direct input
    structure:
      title_working: string
      topic: string
      target_audience: string
      key_benefit: string

optional:
  $brand_profile:
    type: object
    description: Brand voice guidelines (from marca_agent)
    structure:
      tone_scale: object
      archetypes: array
      voice_markers: array
  $seo_keywords:
    type: array
    description: Target keywords from pesquisa_agent
    max_items: 10
  $competitor_titles:
    type: array
    description: Competitor title analysis
    max_items: 5
  $channel_context:
    type: object
    description: Channel-specific context
    structure:
      subscriber_count: integer
      niche: string
      avg_ctr: float
```

## OUTPUT_CONTRACT
```yaml
primary:
  titles.json:
    type: object
    structure:
      titles: array[TitleCandidate]
      recommended: TitleCandidate
      scoring_breakdown: object
      metadata: object

TitleCandidate:
  type: object
  structure:
    text: string (50-70 chars)
    angle: enum[question, number, social_proof, how_to, comparison]
    score_total: float (0-10)
    score_breakdown:
      ctr: float (weight: 0.35)
      seo: float (weight: 0.30)
      brand: float (weight: 0.20)
      technical: float (weight: 0.15)
    keyword_position: integer (target: <40)
    char_count: integer
    ctr_multiplier: float
```

## TASK

**Role**: YouTube Title Optimization Specialist

**Objective**: Generate 5 high-CTR title candidates using psychological formulas, score them with 4D system, and recommend the optimal choice.

**Standards**:
- ALWAYS generate exactly 5 titles (one per angle)
- ALWAYS place primary keyword within first 40 characters
- ALWAYS stay within 50-70 character limit
- NEVER use clickbait that doesn't deliver
- NEVER use ALL CAPS (except for emphasis of 1-2 words max)
- APPLY psychological triggers appropriate to angle

**Constraints**:
- Character limit: 50-70 (optimal: 55-65)
- Keyword position: within first 40 chars
- Quality gate: overall score >= 7.5/10
- Mobile preview: first 45 chars must be compelling

---

## PHASES

### PHASE 1: RESEARCH (10s)
**Objective**: Extract optimization signals from input

```yaml
research_extraction:
  from_video_brief:
    - primary_keyword: $video_brief.topic
    - secondary_keywords: inferred from topic
    - core_benefit: $video_brief.key_benefit
    - audience_pain: inferred from target_audience

  from_brand_profile:
    - tone_match: map to title style
    - voice_markers: PT-BR patterns
    - archetypes: emotional triggers

  from_competitors:
    - patterns_to_use: successful elements
    - patterns_to_avoid: overused/banned
    - gap_opportunities: unaddressed angles

  from_channel:
    - performance_baseline: avg_ctr
    - niche_conventions: expected format
    - audience_expectations: familiarity level
```

**Output Phase 1**:
```json
{
  "research_summary": {
    "primary_keyword": "string",
    "secondary_keywords": ["array"],
    "core_benefit": "string",
    "audience_pain": "string",
    "tone_target": "string",
    "competitor_gaps": ["array"]
  }
}
```

---

### PHASE 2: GENERATE (15s)
**Objective**: Create 5 title candidates using psychological formulas

#### TITLE FORMULAS

**TITLE A - QUESTION ANGLE** (CTR Multiplier: 1.25x)
```
Formula: "[Keyword] + [Provocative Question]?"
Psychology: Curiosity gap, pattern interrupt
Examples:
  - "Marketing Digital: Você Está Cometendo Esses 5 Erros?"
  - "Python para Iniciantes: Por Que 90% Desistem?"

Triggers: curiosity, self-assessment, FOMO
Best for: Educational, tutorial, myth-busting content
```

**TITLE B - NUMBER ANGLE** (CTR Multiplier: 1.36x) ⭐ BEST CTR
```
Formula: "[N] + [Benefit/Reason] + [Keyword]"
Psychology: Specificity, scanability, promise of structure
Examples:
  - "7 Técnicas de Vendas Que Triplicaram Meu Faturamento"
  - "15 Atalhos do Excel Que Vão Mudar Sua Vida"

Triggers: specificity, completeness, efficiency
Best for: Lists, tutorials, compilations
Numbers: 3, 5, 7, 10, 15, 21 (odd numbers outperform)
```

**TITLE C - SOCIAL PROOF ANGLE** (CTR Multiplier: 1.18x)
```
Formula: "[Keyword] + [Transformation/Result Statement]"
Psychology: Authority, credibility, aspirational
Examples:
  - "Design Thinking: O Método Que Usei Para 10x Minha Criatividade"
  - "Copywriting: A Técnica de R$10M em Vendas"

Triggers: authority, transformation, credibility
Best for: Case studies, expert content, results-focused
```

**TITLE D - HOW-TO ANGLE** (CTR Multiplier: 1.22x)
```
Formula: "Como + [Action Verb] + [Keyword] + [Qualifier]"
Psychology: Direct utility, immediate value promise
Examples:
  - "Como Criar Landing Pages Que Convertem 47%+"
  - "Como Editar Vídeos no Premiere em 10 Minutos"

Triggers: utility, clarity, achievability
Best for: Tutorials, step-by-step, practical guides
```

**TITLE E - COMPARISON ANGLE** (CTR Multiplier: 1.30x)
```
Formula: "[A] vs [B] + [Decision Helper]"
Psychology: Decision anxiety relief, completeness
Examples:
  - "ChatGPT vs Claude: Qual IA Usar Para Cada Tarefa"
  - "React vs Vue em 2024: A Verdade Que Ninguém Conta"

Triggers: completeness, decision relief, curiosity
Best for: Reviews, comparisons, debates
```

#### GENERATION RULES

```yaml
character_rules:
  total_limit: 50-70
  optimal_range: 55-65
  keyword_position: <= 40 chars from start
  mobile_preview: first 45 chars must hook

formatting_rules:
  capitalization: Title Case (except connectors)
  connectors_allowed: ["de", "para", "em", "e", "ou", "que", "como"]
  connectors_limit: max 2 per title
  numbers: use digits (7 not "sete")
  punctuation: end with ? for questions, no period otherwise

banned_patterns:
  - ALL CAPS titles
  - Excessive punctuation (!!!, ???)
  - Clickbait without payoff ("Você não vai acreditar...")
  - Generic superlatives ("O melhor", "Incrível")
  - Year for evergreen content unless dated

power_words_ptbr:
  urgency: ["Agora", "Hoje", "Rápido", "Imediato"]
  exclusivity: ["Segredo", "Revelado", "Escondido", "Poucos Sabem"]
  transformation: ["Transforme", "Mude", "Revolucione"]
  specificity: ["Exato", "Passo a Passo", "Comprovado"]
  emotional: ["Chocante", "Surpreendente", "Emocionante"]
```

**Output Phase 2**:
```json
{
  "titles_generated": [
    {
      "angle": "question",
      "text": "string (50-70 chars)",
      "char_count": 58,
      "keyword_position": 0,
      "ctr_multiplier": 1.25,
      "triggers_used": ["curiosity", "self-assessment"]
    },
    // ... 4 more titles
  ]
}
```

---

### PHASE 3: VALIDATE (10s)
**Objective**: Score all titles using 4D system, select winner

#### 4D SCORING SYSTEM

```yaml
scoring_dimensions:
  ctr_prediction:
    weight: 0.35
    factors:
      - angle_multiplier: 1.0-1.36
      - power_words_count: +0.5 per word (max 1.5)
      - curiosity_gap: +1.0 if present
      - specificity: +0.5 if numbers/stats
      - mobile_hook: +0.5 if first 45 chars compelling
    max_score: 10.0

  seo_alignment:
    weight: 0.30
    factors:
      - primary_keyword_present: +3.0
      - keyword_position: +2.0 if <= 40 chars
      - secondary_keywords: +0.5 each (max 2.0)
      - search_intent_match: +2.0
      - competition_differentiation: +1.0
    max_score: 10.0

  brand_alignment:
    weight: 0.20
    factors:
      - tone_match: 0-4.0 (based on tone_scale)
      - voice_markers: +1.0 per marker (max 3.0)
      - archetype_alignment: +2.0 if matches
      - audience_fit: +1.0 if demographic match
    max_score: 10.0

  technical_compliance:
    weight: 0.15
    factors:
      - char_count: +3.0 if 50-70
      - optimal_range: +1.0 if 55-65
      - no_banned_patterns: +3.0
      - proper_formatting: +2.0
      - mobile_truncation_safe: +1.0
    max_score: 10.0
```

#### SCORING CALCULATION

```python
def calculate_4d_score(title: TitleCandidate, context: dict) -> float:
    scores = {
        "ctr": score_ctr_prediction(title, context),
        "seo": score_seo_alignment(title, context),
        "brand": score_brand_alignment(title, context),
        "technical": score_technical_compliance(title)
    }

    weights = {"ctr": 0.35, "seo": 0.30, "brand": 0.20, "technical": 0.15}

    total = sum(scores[dim] * weights[dim] for dim in scores)
    return round(total, 2)
```

#### QUALITY GATE

```yaml
quality_gate:
  minimum_score: 7.5
  actions:
    if_all_below_threshold:
      - regenerate_lowest_scoring
      - apply_enhancement_pass
      - if_still_below: flag_for_human_review
    if_any_above_threshold:
      - recommend_highest_scorer
      - provide_alternatives_above_7.0
```

**Output Phase 3**:
```json
{
  "titles_scored": [
    {
      "text": "7 Técnicas de Vendas Que Triplicaram Meu Faturamento",
      "angle": "number",
      "char_count": 52,
      "keyword_position": 16,
      "scores": {
        "ctr": 9.2,
        "seo": 8.5,
        "brand": 7.8,
        "technical": 9.5
      },
      "score_total": 8.72,
      "ctr_multiplier": 1.36
    }
    // ... 4 more
  ],
  "recommended": {
    "index": 0,
    "text": "7 Técnicas de Vendas Que Triplicaram Meu Faturamento",
    "score_total": 8.72,
    "rationale": "Highest CTR multiplier (number angle), strong keyword position, excellent technical compliance"
  },
  "alternatives": [
    // titles with score >= 7.0
  ]
}
```

---

## VALIDATION

### Quality Gates

```yaml
quality_gates:
  - name: title_count
    check: len(titles) == 5
    action: regenerate_if_missing

  - name: char_limits
    check: all(50 <= t.char_count <= 70 for t in titles)
    action: truncate_or_expand

  - name: keyword_position
    check: all(t.keyword_position <= 40 for t in titles)
    action: reorder_if_needed

  - name: minimum_score
    check: max(t.score_total for t in titles) >= 7.5
    action: enhance_or_flag

  - name: unique_angles
    check: len(set(t.angle for t in titles)) == 5
    action: replace_duplicate_angle

  - name: no_banned_patterns
    check: no_banned_patterns_detected(titles)
    action: sanitize
```

### Thresholds

```yaml
thresholds:
  score_excellent: 9.0
  score_good: 7.5
  score_acceptable: 6.5
  score_reject: < 6.5

  char_min: 50
  char_max: 70
  char_optimal_min: 55
  char_optimal_max: 65

  keyword_position_max: 40
  mobile_preview_chars: 45
```

---

## CONTEXT

**Usage**:
- Called by video_agent after Phase 6 (editor_assembler) for YouTube uploads
- Can be invoked standalone via `/youtube-title` command

**Upstream**:
- $video_brief from 10_concept_planner_HOP
- $brand_profile from marca_agent (optional)
- $seo_keywords from pesquisa_agent (optional)

**Downstream**:
- YouTube upload metadata
- Video description generator
- Thumbnail text optimizer

**$arguments chaining**:
```
video_brief.title_working -> title_optimizer($video_brief)
title_optimizer.recommended -> youtube_upload($title)
title_optimizer.titles -> ab_test_selector($variants)
```

**Integration Modes**:
```yaml
mode_integrated:
  trigger: after Phase 6 completion
  input: $video_brief from pipeline
  output: appends to video_output.json

mode_standalone:
  trigger: /youtube-title command
  input: direct user brief
  output: standalone titles.json
```

---

## EXAMPLES

### Example 1: Tech Tutorial

**Input**:
```json
{
  "video_brief": {
    "title_working": "Como usar o ChatGPT para programar",
    "topic": "ChatGPT programação",
    "target_audience": "Desenvolvedores iniciantes",
    "key_benefit": "Acelerar desenvolvimento com IA"
  }
}
```

**Output**:
```json
{
  "titles": [
    {
      "text": "ChatGPT Para Programação: Você Está Usando Errado?",
      "angle": "question",
      "score_total": 8.1
    },
    {
      "text": "7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer",
      "angle": "number",
      "score_total": 8.9
    },
    {
      "text": "ChatGPT: O Método Que Me Fez Codar 3x Mais Rápido",
      "angle": "social_proof",
      "score_total": 8.4
    },
    {
      "text": "Como Usar ChatGPT Para Programar em 2024 (Guia Completo)",
      "angle": "how_to",
      "score_total": 8.2
    },
    {
      "text": "ChatGPT vs Copilot: Qual Usar Para Programar",
      "angle": "comparison",
      "score_total": 8.6
    }
  ],
  "recommended": {
    "text": "7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer",
    "angle": "number",
    "score_total": 8.9,
    "rationale": "Number angle has highest CTR multiplier (1.36x), strong keyword position, appeals to completeness bias"
  }
}
```

### Example 2: E-commerce Product Video

**Input**:
```json
{
  "video_brief": {
    "title_working": "Review do Fone Bluetooth XYZ",
    "topic": "Fone Bluetooth",
    "target_audience": "Consumidores tech-savvy",
    "key_benefit": "40h de bateria, ANC"
  }
}
```

**Output**:
```json
{
  "recommended": {
    "text": "Fone Bluetooth XYZ: 40h de Bateria é Real? (Teste Completo)",
    "angle": "question",
    "score_total": 8.7
  }
}
```

---

## INTEGRATION WITH VIDEO_AGENT PIPELINE

```
┌─────────────────────────────────────────────────────────────┐
│  VIDEO_AGENT PIPELINE                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: concept_planner → $video_brief                    │
│  Phase 2: script_writer → $script                           │
│  Phase 3: visual_prompter → $visual_prompts                 │
│  Phase 4: production_runner → $video_clips                  │
│  Phase 5: editor_assembler → $final_video                   │
│                                                              │
│  ────────────────────────────────────────────────────────   │
│                          ↓                                   │
│  Phase 6+: TITLE OPTIMIZER (this HOP)                       │
│           Input: $video_brief, $brand_profile               │
│           Output: $youtube_titles                           │
│                          ↓                                   │
│  Phase 7: YouTube Upload (external)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0
**Created**: 2025-12-04
**Author**: codexa_agent (meta-construction)
**Config**: config/youtube_title_rules.json
