# HOP: YouTube Tags Optimizer | video_agent Stage 6++

## MODULE_METADATA
```yaml
id: video_agent_tags_optimizer
version: 1.0.0
purpose: Generate SEO-optimized YouTube tags with keyword consistency
dependencies: [anthropic_api, youtube_tags_rules.json]
category: youtube_optimization
stage: 6++
integration: post_description_optimizer OR standalone
```

## INPUT_CONTRACT
```yaml
required:
  $video_brief:
    type: object
    description: Video brief from previous stages OR direct input
    structure:
      topic: string (primary keyword)
      target_audience: string
      key_benefit: string

optional:
  $title_optimizer_output:
    type: object
    description: Output from 60_title_optimizer for consistency
    structure:
      recommended: TitleCandidate
      keywords_used: array[string]
      angle: enum[question, number, social_proof, how_to, comparison]
  $description_optimizer_output:
    type: object
    description: Output from 61_description_optimizer for keyword alignment
    structure:
      description_full: string
      primary_keyword: string
      secondary_keywords: array[string]
      hashtags: array[string]
  $brand_profile:
    type: object
    description: Brand voice guidelines (from marca_agent)
    structure:
      voice_markers: array[string]
      archetypes: array[string]
  $seo_keywords:
    type: array
    description: Target keywords from pesquisa_agent
    max_items: 20
  $competitor_tags:
    type: array
    description: Competitor tag analysis
    max_items: 50
```

## OUTPUT_CONTRACT
```yaml
primary:
  tags.json:
    type: object
    structure:
      tags: array[TagCandidate]
      recommended_set: TagSet
      scoring_breakdown: object
      metadata: object
      consistency_analysis: object

TagCandidate:
  type: object
  structure:
    text: string (max 30 chars per tag)
    category: enum[primary, secondary, long_tail, semantic]
    rank: integer (1-50)
    search_volume_estimate: enum[low, medium, high]
    search_intent: enum[informational, navigational, commercial, transactional]
    consistency_with_title: boolean
    consistency_with_description: boolean
    score_total: float (0-10)

TagSet:
  type: object
  structure:
    primary_tags: array[TagCandidate] (3-5)
    secondary_tags: array[TagCandidate] (8-12)
    long_tail_tags: array[TagCandidate] (12-20)
    semantic_tags: array[TagCandidate] (5-8)
    total_tags: integer (30-50)
    total_char_count: integer (max 500)
    redundancy_score: float (0-1, lower is better)
```

## TASK

**Role**: YouTube Tags Optimization Specialist

**Objective**: Generate 30-50 SEO-optimized YouTube tags using 4 category strategies, score using 4D system, and ensure keyword consistency with title/description.

**Standards**:
- ALWAYS generate tags across all 4 categories (primary, secondary, long-tail, semantic)
- ALWAYS stay within 500 character total limit
- ALWAYS include primary keyword from title/topic
- NEVER duplicate tags (exact or near-synonym)
- NEVER use competitor brand names (unless comparison video)
- APPLY keyword consistency with upstream title/description

**Constraints**:
- Total character limit: 500 (including commas)
- Individual tag limit: 30 characters max
- Tag count: 30-50 (optimal: 40-45)
- Quality gate: overall score >= 7.5/10
- Redundancy tolerance: max 15% semantic overlap

---

## PHASES

### PHASE 1: RESEARCH (10s)
**Objective**: Extract optimization signals from input and upstream optimizers

```yaml
research_extraction:
  from_video_brief:
    - primary_keyword: $video_brief.topic
    - audience_keywords: inferred from target_audience
    - benefit_keywords: extracted from key_benefit

  from_title_optimizer:
    - title_keywords: all nouns/concepts from winning title
    - title_angle: psychological angle (intent signal)
    - title_modifiers: numbers, "how to", etc.

  from_description_optimizer:
    - description_keywords: from all sections
    - hashtags_to_convert: direct tag candidates
    - secondary_keywords: long-tail opportunities

  from_seo_data:
    - search_volume: estimate per keyword
    - keyword_difficulty: competition level
    - related_queries: expansion candidates

  from_competitors:
    - gap_opportunities: tags they miss
    - saturation_analysis: overused tags to avoid
```

**Output Phase 1**:
```json
{
  "research_summary": {
    "primary_keywords": ["array"],
    "audience_keywords": ["array"],
    "benefit_keywords": ["array"],
    "title_signals": {
      "angle": "string",
      "modifiers": ["array"]
    },
    "description_keywords": ["array"],
    "hashtags_for_conversion": ["array"],
    "competitor_gaps": ["array"],
    "seo_confidence": {
      "primary": 9.2,
      "secondary": 7.8,
      "long_tail": 8.1
    }
  }
}
```

---

### PHASE 2: GENERATE (15s)
**Objective**: Create tags across 4 categories using strategic formulas

#### TAG CATEGORY STRATEGIES

**CATEGORY A - PRIMARY TAGS** (3-5 tags, ~50 chars)
```
Purpose: Core keyword coverage, highest relevance
Source: Topic, title primary keyword, main benefit
Strategy: Exact-match and close variants

Examples:
  Topic: "ChatGPT programação"
  → Tags: ["ChatGPT", "programação", "IA", "inteligência artificial"]

Rules:
  - Max 5 tags
  - Must include topic keyword
  - High search volume terms
  - Broad reach, high competition acceptable
```

**CATEGORY B - SECONDARY TAGS** (8-12 tags, ~180 chars)
```
Purpose: Commercial intent, specific topic coverage
Source: Title keywords, description sections, benefit phrases
Strategy: Keyword + modifier combinations

Formulas:
  - [Primary] + [Action]: "ChatGPT tutorial"
  - [Primary] + [Audience]: "ChatGPT para devs"
  - [Primary] + [Year]: "ChatGPT 2024"
  - [Benefit] + [Topic]: "produtividade programação"

Examples:
  → Tags: ["ChatGPT tutorial", "programar com IA", "ChatGPT dicas",
           "IA desenvolvimento", "prompts ChatGPT", "ChatGPT para devs"]

Rules:
  - 8-12 tags
  - 2-3 words each
  - Medium search volume
  - Commercial/transactional intent
```

**CATEGORY C - LONG-TAIL TAGS** (12-20 tags, ~200 chars)
```
Purpose: Discovery, low competition, specific queries
Source: Questions, specific use cases, niche phrases
Strategy: 3+ word specific phrases

Formulas:
  - "como [action] [topic]": "como usar ChatGPT programar"
  - "[topic] para [audience]": "ChatGPT para iniciantes"
  - "[topic] [specific use case]": "ChatGPT debug código"
  - "[benefit] com [topic]": "acelerar código com IA"

Examples:
  → Tags: ["como usar ChatGPT para programar", "ChatGPT para iniciantes",
           "prompts ChatGPT programação", "debug com ChatGPT",
           "acelerar desenvolvimento com IA", "IA para desenvolvedores"]

Rules:
  - 12-20 tags
  - 3-5 words each
  - Low competition
  - Informational intent
  - High specificity
```

**CATEGORY D - SEMANTIC TAGS** (5-8 tags, ~110 chars)
```
Purpose: Context signals, related concepts, category coverage
Source: Topic modeling, related fields, broader concepts
Strategy: Adjacent topics and YouTube categories

Examples:
  Topic: "ChatGPT programação"
  → Tags: ["machine learning", "produtividade", "tecnologia",
           "desenvolvimento software", "automação", "ferramentas dev"]

Rules:
  - 5-8 tags
  - Related but not duplicate
  - Category/niche signals
  - Help YouTube understand content context
```

#### GENERATION RULES

```yaml
character_rules:
  total_limit: 500
  per_tag_max: 30
  separator: comma
  calculation: sum(len(tag)) + (num_tags - 1)

count_rules:
  total_min: 30
  total_max: 50
  total_optimal: 40-45
  primary_count: 3-5
  secondary_count: 8-12
  long_tail_count: 12-20
  semantic_count: 5-8

consistency_rules:
  title_keyword_required: true
  description_keywords_target: 85%
  hashtag_conversion_target: 90%
  no_contradicting_intent: true

banned_patterns:
  - exact_duplicates: same tag twice
  - near_synonyms: "ChatGPT" and "Chat GPT" (pick one)
  - competitor_brands: unless comparison video
  - misleading_tags: unrelated to content
  - adult_content_terms: YouTube policy
  - trademark_abuse: brand impersonation
```

**Output Phase 2**:
```json
{
  "tags_generated": {
    "primary": [
      {"text": "ChatGPT", "char_count": 7, "category": "primary"},
      {"text": "programação", "char_count": 11, "category": "primary"}
    ],
    "secondary": [],
    "long_tail": [],
    "semantic": [],
    "total_count": 43,
    "total_chars": 498
  }
}
```

---

### PHASE 3: VALIDATE (10s)
**Objective**: Score all tags using 4D system, ensure quality gate

#### 4D SCORING SYSTEM

```yaml
scoring_dimensions:
  seo_relevance:
    weight: 0.40
    description: YouTube ranking and discovery potential
    factors:
      - keyword_search_volume: +3.0 (high/medium volume)
      - keyword_difficulty: +2.0 (difficulty <= 60)
      - semantic_fit_to_title: +2.0 (exact/phrase match)
      - semantic_fit_to_description: +1.0 (appears in description)
      - specificity_score: +1.0 (2-3 words, not too broad)
      - recency: +1.0 (trending topic)
    max_score: 10.0

  keyword_consistency:
    weight: 0.35
    description: Alignment with title and description
    factors:
      - title_keyword_present: +3.0 (primary keyword match)
      - description_keywords_coverage: +2.0 (secondary keywords)
      - hashtag_alignment: +2.0 (converted from description)
      - intent_alignment: +1.5 (same search intent)
      - no_contradictions: +1.5 (no conflicting terms)
    max_score: 10.0

  discoverability_coverage:
    weight: 0.15
    description: Breadth of discovery opportunities
    factors:
      - primary_tags_present: +2.0 (3-5 main keywords)
      - secondary_tags_present: +2.0 (8-12 commercial)
      - long_tail_coverage: +2.0 (12-20 discovery)
      - semantic_context: +2.0 (5-8 related concepts)
      - no_over_optimization: +2.0 (balanced, not spammy)
    max_score: 10.0

  technical_compliance:
    weight: 0.10
    description: YouTube platform requirements
    factors:
      - char_count_valid: +3.0 (≤500 total)
      - tag_count_valid: +2.0 (30-50 tags)
      - no_banned_patterns: +3.0
      - proper_formatting: +2.0
    max_score: 10.0
```

#### SCORING CALCULATION

```python
def calculate_4d_score(tag_set: TagSet, context: dict) -> float:
    scores = {
        "seo": score_seo_relevance(tag_set, context),
        "consistency": score_keyword_consistency(tag_set, context),
        "coverage": score_discoverability_coverage(tag_set),
        "technical": score_technical_compliance(tag_set)
    }

    weights = {"seo": 0.40, "consistency": 0.35, "coverage": 0.15, "technical": 0.10}

    total = sum(scores[dim] * weights[dim] for dim in scores)
    return round(total, 2)
```

#### QUALITY GATE

```yaml
quality_gate:
  minimum_score: 7.5
  actions:
    if_below_threshold:
      - identify_weakest_category
      - regenerate_weak_tags
      - rebalance_distribution
      - if_still_below: flag_for_human_review
    if_above_threshold:
      - finalize_tag_set
      - generate_alternatives (optional)
```

**Output Phase 3**:
```json
{
  "tags_scored": {
    "final_set": [
      {
        "text": "ChatGPT",
        "category": "primary",
        "rank": 1,
        "search_volume": "high",
        "scores": {
          "seo": 9.0,
          "consistency": 9.5,
          "coverage": 8.0,
          "technical": 10.0
        },
        "score_total": 9.08
      }
    ],
    "set_metrics": {
      "total_score": 8.35,
      "avg_tag_score": 8.12,
      "above_quality_gate": true,
      "tag_count": 43,
      "char_count": 498,
      "redundancy_score": 0.08
    }
  },
  "consistency_analysis": {
    "title_coverage": "100% - primary keyword present",
    "description_coverage": "95% - 5 secondary keywords captured",
    "hashtag_coverage": "87% - 3 of 4 hashtags tagged"
  },
  "optimization_notes": [
    "Tag set well-balanced across all 4 categories",
    "No synonyms or near-duplicates detected",
    "Character efficiency: 498/500 utilized"
  ]
}
```

---

## VALIDATION

### Quality Gates

```yaml
quality_gates:
  - name: char_limit
    check: total_char_count <= 500
    action: trim_lowest_priority_tags

  - name: tag_count_min
    check: len(tags) >= 30
    action: add_semantic_tags_if_below

  - name: tag_count_max
    check: len(tags) <= 50
    action: remove_lowest_scoring_tags

  - name: primary_presence
    check: len(primary_tags) >= 3
    action: enforce_minimum

  - name: title_consistency
    check: title_keyword in tags
    action: inject_title_keyword

  - name: no_duplicates
    check: len(tags) == len(set(tags))
    action: remove_exact_duplicates

  - name: no_synonyms
    check: semantic_similarity_max < 0.85
    action: remove_synonyms_keep_highest

  - name: minimum_score
    check: overall_score >= 7.5
    action: regenerate_or_flag
```

### Thresholds

```yaml
thresholds:
  score_excellent: 9.0
  score_good: 7.5
  score_acceptable: 6.5
  score_reject: < 6.5

  char_total_max: 500
  char_per_tag_max: 30

  tag_count_min: 30
  tag_count_max: 50
  tag_count_optimal: 40-45

  redundancy_max: 0.15
```

---

## CONTEXT

**Usage**:
- Called by video_agent after description_optimizer for complete YouTube metadata
- Can be invoked standalone via `/youtube-tags` command

**Upstream**:
- $video_brief from 10_concept_planner_HOP
- $title_optimizer_output from 60_title_optimizer_HOP (recommended)
- $description_optimizer_output from 61_description_optimizer_HOP (recommended)
- $seo_keywords from pesquisa_agent (optional)

**Downstream**:
- YouTube upload metadata
- Video SEO report
- Thumbnail text optimizer (63_thumbnail_text)

**$arguments chaining**:
```
video_brief -> title_optimizer -> description_optimizer -> tags_optimizer($all_outputs)
tags_optimizer.recommended_set -> youtube_upload($tags)
tags_optimizer.tags -> seo_report($keyword_analysis)
```

**Integration Modes**:
```yaml
mode_integrated:
  trigger: after description_optimizer completion
  input: $video_brief + $title_output + $description_output
  output: appends to video_output.json

mode_standalone:
  trigger: /youtube-tags command
  input: direct user brief
  output: standalone tags.json
```

---

## EXAMPLES

### Example 1: Tech Tutorial

**Input**:
```json
{
  "video_brief": {
    "topic": "ChatGPT programação",
    "target_audience": "Desenvolvedores iniciantes",
    "key_benefit": "Acelerar desenvolvimento com IA"
  },
  "title_optimizer_output": {
    "recommended": {
      "text": "7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer"
    },
    "keywords_used": ["ChatGPT", "prompts", "dev"]
  },
  "description_optimizer_output": {
    "hashtags": ["#ChatGPT", "#Programação", "#IA", "#DevTips"]
  }
}
```

**Output**:
```json
{
  "recommended_set": {
    "primary_tags": [
      "ChatGPT", "programação", "inteligência artificial", "IA", "prompts"
    ],
    "secondary_tags": [
      "ChatGPT tutorial", "programar com IA", "ChatGPT dicas",
      "prompts ChatGPT", "ChatGPT para devs", "desenvolvimento com IA",
      "produtividade dev", "ferramentas programação", "ChatGPT 2024"
    ],
    "long_tail_tags": [
      "como usar ChatGPT para programar", "ChatGPT para iniciantes",
      "prompts ChatGPT programação", "debug com ChatGPT",
      "acelerar desenvolvimento com IA", "IA para desenvolvedores",
      "ChatGPT código", "automatizar código com IA",
      "melhores prompts ChatGPT", "ChatGPT desenvolvimento software",
      "aprender programar com IA", "ChatGPT refatorar código",
      "ChatGPT documentação", "ChatGPT testes unitários"
    ],
    "semantic_tags": [
      "machine learning", "produtividade", "tecnologia",
      "desenvolvimento software", "automação", "ferramentas dev",
      "coding", "tech"
    ],
    "total_tags": 36,
    "total_char_count": 487,
    "redundancy_score": 0.06
  },
  "scores": {
    "seo": 8.8,
    "consistency": 9.2,
    "coverage": 8.5,
    "technical": 9.5
  },
  "score_total": 8.92
}
```

### Example 2: Product Review

**Input**:
```json
{
  "video_brief": {
    "topic": "iPhone 15 Pro review",
    "target_audience": "Consumidores tech-savvy",
    "key_benefit": "Decisão de compra informada"
  }
}
```

**Output**:
```json
{
  "recommended_set": {
    "primary_tags": [
      "iPhone 15 Pro", "review", "Apple", "smartphone", "celular"
    ],
    "secondary_tags": [
      "iPhone 15 Pro review", "análise iPhone", "vale a pena iPhone",
      "iPhone 15 câmera", "iPhone 15 bateria", "iPhone 15 preço",
      "comparativo iPhone", "iPhone 2024", "melhor iPhone"
    ],
    "long_tail_tags": [
      "iPhone 15 Pro vale a pena comprar", "review completo iPhone 15",
      "iPhone 15 Pro vs iPhone 14 Pro", "câmera iPhone 15 Pro teste",
      "bateria iPhone 15 Pro duração", "iPhone 15 Pro Brasil preço",
      "unboxing iPhone 15 Pro", "iPhone 15 Pro primeiras impressões"
    ],
    "semantic_tags": [
      "tecnologia", "gadgets", "eletrônicos", "iOS", "Apple Watch",
      "AirPods", "celulares premium"
    ],
    "total_tags": 31,
    "total_char_count": 462
  },
  "score_total": 8.45
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
│  Phase 6+: TITLE OPTIMIZER                                  │
│           Output: $youtube_titles                           │
│                          ↓                                   │
│  Phase 6++: DESCRIPTION OPTIMIZER                           │
│           Output: $youtube_description                      │
│                          ↓                                   │
│  Phase 6+++: TAGS OPTIMIZER (this HOP)                      │
│           Input: $video_brief, $titles, $description        │
│           Output: $youtube_tags                             │
│                          ↓                                   │
│  Phase 6++++: Thumbnail Text (63_thumbnail_text_HOP)        │
│                          ↓                                   │
│  Phase 7: YouTube Upload (external)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0
**Created**: 2025-12-04
**Author**: codexa_agent (meta-construction)
**Config**: config/youtube_tags_rules.json
**Predecessor**: 61_description_optimizer_HOP.md
