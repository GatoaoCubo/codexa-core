# HOP: YouTube Chapters Generator | video_agent Stage 6.5

## MODULE_METADATA
```yaml
id: video_agent_chapters_generator
version: 1.0.0
purpose: Generate timestamp-marked chapters from video content
dependencies: [anthropic_api, youtube_chapters_rules.json]
category: youtube_optimization
stage: 6.5
integration: post_description_optimizer OR standalone
```

## INPUT_CONTRACT
```yaml
required:
  $video_brief:
    type: object
    description: Core video information
    structure:
      video_duration: string (MM:SS or HH:MM:SS, must be >= 180s)
      topic: string (primary topic)
      target_audience: string
      content_type: enum[tutorial, review, educational, promotional, vlog]

  # ONE of these three input modes:
  input_mode: enum[transcript, script, outline]

  $transcript:  # Mode 1
    type: string
    description: Full video transcript or auto-generated captions
    condition: if input_mode == "transcript"

  $script:  # Mode 2
    type: object
    description: Script from Stage 2 (script_writer)
    condition: if input_mode == "script"
    structure:
      narration_segments: array[NarrationSegment]
      total_duration: integer (seconds)

  $outline:  # Mode 3
    type: array
    description: Manual content outline
    condition: if input_mode == "outline"
    structure:
      - title: string
        description: string
        estimated_duration: string (MM:SS)

optional:
  $title_final:
    type: string
    description: Final YouTube title for keyword consistency

  $description_chapters:
    type: array
    description: Pre-defined chapters from description_optimizer
    structure:
      - timestamp: string (MM:SS)
        title: string

  $key_points:
    type: array
    description: Key learning outcomes or benefits
    max_items: 10
```

## OUTPUT_CONTRACT
```yaml
primary:
  chapters.json:
    type: object
    structure:
      chapters: array[Chapter]
      metadata: ChaptersMetadata
      scoring_breakdown: object
      validation_results: object
      formatted_output: string

Chapter:
  type: object
  structure:
    timestamp: string (MM:SS or HH:MM:SS)
    title: string (max 50 chars)
    duration: string (chapter duration)
    keywords: array[string]

ChaptersMetadata:
  type: object
  structure:
    chapter_count: integer (recommended: 5-10)
    total_duration: string
    input_mode: enum[transcript, script, outline]
    auto_generated: boolean
    confidence_score: float (0-10)

ValidationResults:
  type: object
  structure:
    first_chapter_valid: boolean (must be 00:00)
    all_ascending: boolean
    min_10s_gaps: boolean
    max_50_chars: boolean
    no_duplicates: boolean
    quality_gate_pass: boolean
```

## TASK

**Role**: YouTube Chapters Generation Specialist

**Objective**: Generate 5-10 timestamp-marked chapters from video content, using action-oriented naming conventions, and ensuring YouTube chapter feature requirements.

**Standards**:
- ALWAYS start first chapter at 00:00
- ALWAYS use action verbs in chapter titles
- ALWAYS ensure minimum 10 seconds between chapters
- NEVER exceed 50 characters per chapter title
- NEVER generate more than 15 chapters (cognitive overload)
- APPLY keyword consistency with title/description

**Constraints**:
- First timestamp: MUST be 00:00
- Minimum chapters: 3 (YouTube requirement)
- Maximum chapters: 15 (usability)
- Optimal chapters: 5-10
- Minimum gap: 10 seconds between chapters
- Title length: max 50 characters
- Quality gate: overall score >= 7.5/10

---

## PHASES

### PHASE 1: ANALYZE (12s)
**Objective**: Parse input and identify natural content sections

```yaml
analysis_by_input_mode:
  transcript_mode:
    - identify_topic_changes: detect subject shifts
    - extract_key_phrases: important concepts
    - estimate_timing: infer timestamps from text position
    - find_natural_breaks: pauses, transitions

  script_mode:
    - parse_narration_segments: extract start/end times
    - identify_narrative_arc: hook, build, benefit, proof, cta
    - map_shot_boundaries: visual transition points
    - extract_keywords: from narration text

  outline_mode:
    - calculate_cumulative_timing: from estimated durations
    - validate_section_structure: logical flow
    - identify_major_sections: chapter candidates
    - refine_timing: adjust to video_duration

content_strategy:
  chapter_count_by_duration:
    - "3-5min": 2-3 chapters
    - "5-10min": 4-6 chapters
    - "10-20min": 6-8 chapters
    - "20-60min": 8-12 chapters
    - "60min+": 10-15 chapters
```

**Output Phase 1**:
```json
{
  "analysis_summary": {
    "total_duration": "22:45",
    "input_mode": "script",
    "identified_sections": [
      {
        "topic": "Introduction",
        "start_est": "00:00",
        "end_est": "01:45",
        "confidence": 0.95
      }
    ],
    "narrative_structure": {
      "hook": "00:00-01:30",
      "build": "01:30-08:00",
      "benefit": "08:00-15:00",
      "proof": "15:00-18:00",
      "cta": "18:00-22:45"
    },
    "recommended_chapter_count": 8,
    "natural_break_points": ["00:00", "01:45", "04:15", "07:30", "10:15", "15:45", "19:45", "22:15"]
  }
}
```

---

### PHASE 2: GENERATE (15s)
**Objective**: Create chapter titles with timestamps

#### CHAPTER NAMING CONVENTIONS

**Action-Oriented Structure** (Primary)
```
Formula: [Action Verb] + [Topic/Subject] + [Optional Benefit]

Power Verbs PT-BR:
  Discovery:    Descobrindo, Explorando, Revelando, Analisando
  Learning:     Aprendendo, Entendendo, Dominando, Compreendendo
  Building:     Construindo, Criando, Desenvolvendo, Montando
  Optimizing:   Otimizando, Melhorando, Acelerando, Refinando
  Solving:      Resolvendo, Corrigindo, Eliminando, Superando
  Implementing: Implementando, Aplicando, Executando, Integrando

Examples:
  ✓ Good:
    - "Introdução e Visão Geral"
    - "Configurando o Ambiente"
    - "Debugando Erros Comuns"
    - "Deploy em Produção"
    - "Otimizando Performance"

  ✗ Avoid:
    - "Introdução" (too vague, add context)
    - "Parte 2" (number without meaning)
    - "Mais Conteúdo" (generic)
    - "Continuação" (unhelpful)
```

**Benefit-Focused Structure** (Secondary, for longer videos)
```
Formula: [Action] + [Topic] + [Outcome/Result]

Examples:
  ✓ Good:
    - "Setup Rápido para Deploy Imediato"
    - "Error Handling Que Previne Crashes"
    - "Testes Que Encontram Bugs Cedo"
```

#### GENERATION RULES

```yaml
timestamp_rules:
  format: "MM:SS" or "HH:MM:SS"
  first_chapter: "00:00" (mandatory)
  zero_padding: true (02:15 not 2:15)
  ascending_order: true
  min_gap_seconds: 10
  no_duplicates: true

title_rules:
  max_chars: 50
  style: "action_oriented"
  case: "Title Case"
  language: "match video language"
  parallel_structure: true (consistent verb tense across chapters)

chapter_structure:
  intro_chapter:
    position: first (00:00)
    purpose: "Set expectation for video"
    examples: ["Introdução e Overview", "O Que Você Vai Aprender"]

  content_chapters:
    position: middle
    purpose: "Main content sections"
    naming: "Action verb + specific topic"

  conclusion_chapter:
    position: last
    purpose: "Wrap up, next steps"
    examples: ["Resumo e Próximos Passos", "Conclusão"]
    min_duration: 30 seconds

banned_patterns:
  - "Part 1", "Part 2" (use descriptive titles)
  - Numbers without context ("1:23")
  - Generic ("More content", "Continuation")
  - ALL CAPS titles
  - Promotional language only
```

**Output Phase 2**:
```json
{
  "chapters_generated": [
    {
      "timestamp": "00:00",
      "title": "Introdução e Visão Geral",
      "duration_estimate": "01:45",
      "source_section": "hook",
      "keywords": ["introdução", "overview"]
    },
    {
      "timestamp": "01:45",
      "title": "Configurando o Ambiente",
      "duration_estimate": "02:30",
      "source_section": "build",
      "keywords": ["setup", "configuração"]
    }
  ],
  "chapter_count": 8,
  "total_coverage": 0.98
}
```

---

### PHASE 3: VALIDATE (10s)
**Objective**: Score chapters using 5D system, ensure quality gate

#### 5D SCORING SYSTEM

```yaml
scoring_dimensions:
  naming_quality:
    weight: 0.25
    description: Clarity and action orientation
    factors:
      - action_verb_present: +3.0
      - clear_subject: +2.0
      - benefit_implied: +2.0
      - proper_length: +2.0 (< 50 chars)
      - no_jargon: +1.0
    max_score: 10.0

  timing_accuracy:
    weight: 0.25
    description: Proper spacing and format
    factors:
      - first_chapter_00_00: +3.0 (mandatory)
      - ascending_order: +2.0
      - min_10s_gaps: +2.0
      - proper_format: +2.0
      - aligns_with_content: +1.0
    max_score: 10.0

  coverage:
    weight: 0.20
    description: All major sections represented
    factors:
      - intro_present: +2.0
      - main_content_covered: +4.0
      - conclusion_present: +2.0
      - key_points_included: +2.0
    max_score: 10.0

  engagement_potential:
    weight: 0.20
    description: Viewer appeal and navigation value
    factors:
      - curiosity_inducing: +2.0
      - scannable_memorable: +2.0
      - logical_flow: +2.0
      - pacing_appropriate: +2.0
      - action_verbs_engaging: +2.0
    max_score: 10.0

  seo_alignment:
    weight: 0.10
    description: Keyword inclusion and searchability
    factors:
      - primary_keyword_present: +2.0
      - secondary_keywords: +2.0
      - chapter_titles_searchable: +2.0
      - no_keyword_stuffing: +2.0
      - natural_language: +2.0
    max_score: 10.0
```

#### SCORING CALCULATION

```python
def calculate_5d_score(chapters: list, context: dict) -> float:
    scores = {
        "naming": score_naming_quality(chapters),
        "timing": score_timing_accuracy(chapters),
        "coverage": score_coverage(chapters, context),
        "engagement": score_engagement_potential(chapters),
        "seo": score_seo_alignment(chapters, context)
    }

    weights = {"naming": 0.25, "timing": 0.25, "coverage": 0.20, "engagement": 0.20, "seo": 0.10}

    total = sum(scores[dim] * weights[dim] for dim in scores)
    return round(total, 2)
```

#### QUALITY GATE

```yaml
quality_gate:
  minimum_score: 7.5
  validation_checks:
    - first_chapter == "00:00"
    - all_timestamps_ascending
    - all_gaps >= 10 seconds
    - all_titles <= 50 chars
    - no_duplicate_titles
    - 3 <= chapter_count <= 15

  actions:
    if_validation_fails:
      - auto_fix_first_timestamp
      - merge_too_close_chapters
      - truncate_long_titles
    if_score_below_threshold:
      - regenerate_weak_titles
      - rebalance_chapter_distribution
      - if_still_below: flag_for_human_review
```

**Output Phase 3**:
```json
{
  "chapters_final": [
    {
      "timestamp": "00:00",
      "title": "Introdução e Visão Geral",
      "duration": "01:45",
      "keywords": ["introdução", "overview"]
    }
  ],
  "validation_results": {
    "first_chapter_valid": true,
    "all_ascending": true,
    "min_10s_gaps": true,
    "max_50_chars": true,
    "no_duplicates": true,
    "quality_gate_pass": true
  },
  "scoring_breakdown": {
    "naming_quality": 8.5,
    "timing_accuracy": 9.0,
    "coverage": 8.2,
    "engagement_potential": 8.0,
    "seo_alignment": 8.5,
    "overall_score": 8.42
  },
  "formatted_output": "⏱️ CAPÍTULOS:\n00:00 - Introdução e Visão Geral\n01:45 - Configurando o Ambiente\n..."
}
```

---

## VALIDATION

### Quality Gates

```yaml
quality_gates:
  - name: first_timestamp
    check: chapters[0].timestamp == "00:00"
    action: fix_to_00_00
    severity: critical

  - name: ascending_order
    check: all timestamps in ascending order
    action: reorder_chapters
    severity: critical

  - name: minimum_gap
    check: all gaps >= 10 seconds
    action: merge_too_close_chapters
    severity: critical

  - name: title_length
    check: all titles <= 50 chars
    action: truncate_with_ellipsis
    severity: high

  - name: no_duplicates
    check: all titles unique
    action: differentiate_titles
    severity: high

  - name: chapter_count
    check: 3 <= count <= 15
    action: adjust_chapter_count
    severity: medium

  - name: minimum_score
    check: overall_score >= 7.5
    action: regenerate_or_flag
    severity: medium
```

### Thresholds

```yaml
thresholds:
  score_excellent: 9.0
  score_good: 7.5
  score_acceptable: 6.5
  score_reject: < 6.5

  chapter_count_min: 3
  chapter_count_max: 15
  chapter_count_optimal_min: 5
  chapter_count_optimal_max: 10

  title_max_chars: 50
  gap_min_seconds: 10
  gap_practical_min_seconds: 30
  gap_recommended_min_seconds: 60

  video_duration_min_seconds: 180
```

---

## CONTEXT

**Usage**:
- Called by video_agent as part of description_optimizer (timestamps section)
- Can be invoked standalone via `/youtube-chapters` command
- Accepts transcript, script, or outline as input

**Upstream**:
- $video_brief from 10_concept_planner_HOP
- $script from 14_script_writer_HOP (script mode)
- $title_final from 60_title_optimizer_HOP (optional)
- $description_optimizer_output from 61_description_optimizer_HOP (may have pre-defined chapters)

**Downstream**:
- YouTube upload metadata (chapter field)
- Video description (timestamps section)
- Video SEO report

**$arguments chaining**:
```
script_writer.$script -> chapters_generator($script)
description_optimizer.timestamps -> chapters_generator.validate($existing_chapters)
chapters_generator.formatted_output -> description_optimizer.timestamps_section
```

**Integration Modes**:
```yaml
mode_integrated:
  trigger: as part of description_optimizer flow
  input: $script OR $outline
  output: appends to video_output.json

mode_standalone:
  trigger: /youtube-chapters command
  input: transcript/script/outline + duration
  output: standalone chapters.json

mode_refinement:
  trigger: existing chapters provided
  input: description_optimizer.timestamps
  output: validated/improved chapters
```

---

## EXAMPLES

### Example 1: Tech Tutorial (Script Input)

**Input**:
```json
{
  "video_brief": {
    "video_duration": "22:45",
    "topic": "React Hooks Avançados",
    "target_audience": "Desenvolvedores intermediários",
    "content_type": "tutorial"
  },
  "input_mode": "script",
  "script": {
    "narration_segments": [
      {"text": "Bem-vindos ao tutorial de React Hooks...", "start": 0, "end": 105},
      {"text": "Vamos começar com useReducer...", "start": 105, "end": 255}
    ],
    "total_duration": 1365
  }
}
```

**Output**:
```json
{
  "chapters": [
    {"timestamp": "00:00", "title": "Introdução e Setup", "duration": "01:45"},
    {"timestamp": "01:45", "title": "Entendendo useReducer", "duration": "02:30"},
    {"timestamp": "04:15", "title": "Custom Hooks na Prática", "duration": "03:15"},
    {"timestamp": "07:30", "title": "Otimização com useMemo", "duration": "02:45"},
    {"timestamp": "10:15", "title": "Exemplos de Produção", "duration": "05:30"},
    {"timestamp": "15:45", "title": "Erros Comuns e Soluções", "duration": "04:00"},
    {"timestamp": "19:45", "title": "Técnicas Avançadas", "duration": "02:30"},
    {"timestamp": "22:15", "title": "Resumo e Próximos Passos", "duration": "00:30"}
  ],
  "metadata": {
    "chapter_count": 8,
    "total_duration": "22:45",
    "input_mode": "script",
    "confidence_score": 8.7
  },
  "scoring_breakdown": {
    "naming_quality": 8.5,
    "timing_accuracy": 9.0,
    "coverage": 8.2,
    "engagement_potential": 8.0,
    "seo_alignment": 8.5,
    "overall_score": 8.42
  },
  "formatted_output": "⏱️ CAPÍTULOS:\n00:00 - Introdução e Setup\n01:45 - Entendendo useReducer\n04:15 - Custom Hooks na Prática\n07:30 - Otimização com useMemo\n10:15 - Exemplos de Produção\n15:45 - Erros Comuns e Soluções\n19:45 - Técnicas Avançadas\n22:15 - Resumo e Próximos Passos"
}
```

### Example 2: Product Review (Outline Input)

**Input**:
```json
{
  "video_brief": {
    "video_duration": "15:30",
    "topic": "iPhone 15 Pro Review",
    "target_audience": "Consumidores tech-savvy",
    "content_type": "review"
  },
  "input_mode": "outline",
  "outline": [
    {"title": "Unboxing", "description": "First impressions", "estimated_duration": "02:00"},
    {"title": "Design", "description": "Build quality and feel", "estimated_duration": "02:30"},
    {"title": "Camera", "description": "Photo and video tests", "estimated_duration": "04:00"},
    {"title": "Performance", "description": "Speed and gaming", "estimated_duration": "03:00"},
    {"title": "Battery", "description": "Real-world usage", "estimated_duration": "02:00"},
    {"title": "Verdict", "description": "Final thoughts", "estimated_duration": "02:00"}
  ]
}
```

**Output**:
```json
{
  "chapters": [
    {"timestamp": "00:00", "title": "Unboxing e Primeiras Impressões", "duration": "02:00"},
    {"timestamp": "02:00", "title": "Design e Qualidade de Construção", "duration": "02:30"},
    {"timestamp": "04:30", "title": "Câmera: Fotos e Vídeos Testados", "duration": "04:00"},
    {"timestamp": "08:30", "title": "Performance e Gaming", "duration": "03:00"},
    {"timestamp": "11:30", "title": "Bateria no Uso Real", "duration": "02:00"},
    {"timestamp": "13:30", "title": "Veredito Final: Vale a Pena?", "duration": "02:00"}
  ],
  "scoring_breakdown": {
    "overall_score": 8.65
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
│  Phase 2: script_writer → $script (with timing)             │
│  Phase 3-5: Production Pipeline                             │
│                                                              │
│  ────────────────────────────────────────────────────────   │
│                          ↓                                   │
│  Phase 6+: TITLE OPTIMIZER                                  │
│                          ↓                                   │
│  Phase 6++: DESCRIPTION OPTIMIZER                           │
│      ├── Section 3: Timestamps ← CHAPTERS GENERATOR         │
│      └── Uses $script or manual outline                     │
│                          ↓                                   │
│  Phase 6.5: CHAPTERS GENERATOR (this HOP)                   │
│           Can refine/validate existing chapters             │
│           OR generate from script/transcript/outline        │
│                          ↓                                   │
│  Phase 6+++: TAGS OPTIMIZER                                 │
│  Phase 6++++: THUMBNAIL TEXT                                │
│                          ↓                                   │
│  Phase 7: YouTube Upload                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0
**Created**: 2025-12-04
**Author**: codexa_agent (meta-construction)
**Config**: config/youtube_chapters_rules.json
**Integration**: Part of description_optimizer OR standalone
