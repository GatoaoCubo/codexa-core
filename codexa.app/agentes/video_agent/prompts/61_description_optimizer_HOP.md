# HOP: YouTube Description Optimizer | video_agent Stage 6+

## MODULE_METADATA
```yaml
id: video_agent_description_optimizer
version: 1.0.0
purpose: Generate SEO-optimized YouTube descriptions with structured sections
dependencies: [anthropic_api, youtube_description_rules.json]
category: youtube_optimization
stage: 6+
integration: post_title_optimizer OR standalone
```

## INPUT_CONTRACT
```yaml
required:
  $video_brief:
    type: object
    description: Video brief from previous stages OR direct input
    structure:
      title_final: string  # From title_optimizer or working title
      topic: string
      target_audience: string
      key_benefit: string
      video_duration: string  # For timestamp generation

optional:
  $title_optimizer_output:
    type: object
    description: Output from 60_title_optimizer for consistency
    structure:
      recommended: TitleCandidate
      keywords_used: array
  $brand_profile:
    type: object
    description: Brand voice guidelines (from marca_agent)
    structure:
      tone_scale: object
      archetypes: array
      voice_markers: array
      social_links: object
  $seo_keywords:
    type: array
    description: Target keywords from pesquisa_agent
    max_items: 15
  $video_chapters:
    type: array
    description: Chapter markers for timestamps
    structure:
      - timestamp: string (MM:SS or HH:MM:SS)
        title: string
  $channel_context:
    type: object
    description: Channel-specific context
    structure:
      channel_name: string
      default_cta: string
      social_links: object
      playlist_links: array
```

## OUTPUT_CONTRACT
```yaml
primary:
  description.json:
    type: object
    structure:
      description_full: string (max 5000 chars)
      description_preview: string (first 150 chars)
      sections: DescriptionSections
      scoring_breakdown: object
      metadata: object

DescriptionSections:
  type: object
  structure:
    hook:
      content: string (100-150 chars)
      purpose: "Above-fold hook visible in search"
    value_proposition:
      content: string (150-300 chars)
      purpose: "What viewer will learn/get"
    timestamps:
      content: string (variable)
      chapters: array[Chapter]
      purpose: "Navigation + watch time boost"
    links_ctas:
      content: string (200-400 chars)
      links: array[Link]
      purpose: "Conversion + engagement"
    hashtags_keywords:
      content: string (50-100 chars)
      hashtags: array (3-5)
      keywords: array (embedded naturally)
      purpose: "Discoverability"

Chapter:
  type: object
  structure:
    timestamp: string (MM:SS)
    title: string (max 50 chars)

Link:
  type: object
  structure:
    label: string
    url: string
    type: enum[social, website, affiliate, related_video, playlist]
```

## TASK

**Role**: YouTube Description Optimization Specialist

**Objective**: Generate a complete, SEO-optimized YouTube description with 5 structured sections, score using 4D system, and ensure above-fold hook maximizes engagement.

**Standards**:
- ALWAYS include all 5 sections in correct order
- ALWAYS place primary keyword within first 25 words
- ALWAYS ensure first 100-150 chars are compelling (above-fold)
- NEVER exceed 5000 character total limit
- NEVER keyword-stuff (max 3% keyword density)
- APPLY natural language that reads conversationally
- INCLUDE timestamps if video > 3 minutes

**Constraints**:
- Total limit: 5000 characters
- Above-fold: 100-150 chars (visible before "show more")
- Recommended length: 500-1500 chars (balanced)
- Keyword density: 1-3% (natural integration)
- Hashtags: 3-5 maximum (at end)
- Quality gate: overall score >= 7.5/10

---

## PHASES

### PHASE 1: RESEARCH (10s)
**Objective**: Extract optimization signals and structure content strategy

```yaml
research_extraction:
  from_video_brief:
    - primary_keyword: $video_brief.topic
    - secondary_keywords: inferred from topic + title
    - core_value: $video_brief.key_benefit
    - audience_needs: inferred from target_audience
    - duration: $video_brief.video_duration

  from_title_optimizer:
    - title_keywords: keywords used in winning title
    - title_angle: psychological angle (for consistency)
    - title_tone: emotional register

  from_brand_profile:
    - voice_style: formal/casual scale
    - cta_style: soft/direct preference
    - social_links: platforms to include
    - boilerplate: standard channel description

  from_seo_data:
    - primary_search_terms: what people search for
    - related_queries: long-tail opportunities
    - competitor_gaps: what others miss

content_strategy:
  length_decision:
    - short_video (<5min): 300-500 chars
    - medium_video (5-15min): 500-1000 chars
    - long_video (15min+): 1000-2000 chars
    - tutorial/course: 1500-2500 chars (detailed)

  timestamp_decision:
    - if duration >= 3min: include timestamps
    - if duration >= 10min: detailed chapters
    - if duration >= 30min: comprehensive TOC
```

**Output Phase 1**:
```json
{
  "research_summary": {
    "primary_keyword": "string",
    "secondary_keywords": ["array"],
    "core_value_proposition": "string",
    "audience_pain_points": ["array"],
    "title_consistency": {
      "keywords_to_echo": ["array"],
      "angle_to_maintain": "string"
    },
    "content_strategy": {
      "target_length": 800,
      "include_timestamps": true,
      "cta_style": "soft"
    }
  }
}
```

---

### PHASE 2: GENERATE (15s)
**Objective**: Create 5-section description with optimized content

#### SECTION FORMULAS

**SECTION 1 - HOOK (Above Fold)** 🎯 CRITICAL
```
Purpose: Stop the scroll, create curiosity
Position: First 100-150 characters (visible in search/browse)
Formula: [Keyword] + [Curiosity/Value Hook] + [Promise]

Psychology:
  - Pattern interrupt (unexpected opening)
  - Value preview (what they'll get)
  - Curiosity gap (incomplete loop)

Examples PT-BR:
  ✅ "ChatGPT para programação: 7 prompts que vão mudar sua forma de codar. Neste vídeo, você vai aprender..."
  ✅ "Cansei de perder 2 horas por anúncio. Descobri um método que cria 22 em 18 minutos. Funciona assim..."
  ✅ "90% dos devs usam ChatGPT errado. Aqui está o que os melhores fazem diferente..."

Triggers: curiosity, value_preview, pattern_interrupt
Character Limit: 100-150 (hard cap at 150)

Banned:
  - Starting with "Neste vídeo..." (generic)
  - Starting with "Olá pessoal..." (wasted characters)
  - Generic greetings (save for video itself)
```

**SECTION 2 - VALUE PROPOSITION** 📦
```
Purpose: Expand on what viewer will learn/achieve
Position: After hook, before timestamps
Formula: [What You'll Learn] + [Why It Matters] + [Who It's For]

Structure:
  📌 O que você vai aprender:
  • [Benefit 1]
  • [Benefit 2]
  • [Benefit 3]

  👤 Para quem é este vídeo:
  • [Audience descriptor]

Examples PT-BR:
  "📌 Neste vídeo você vai descobrir:
  • Como usar prompts avançados de ChatGPT
  • 7 técnicas que economizam 5h por semana
  • O erro #1 que trava iniciantes

  Perfeito para devs que querem acelerar o workflow sem sacrificar qualidade."

Character Limit: 150-300
Use: Bullet points for scanability
```

**SECTION 3 - TIMESTAMPS** ⏱️
```
Purpose: Enable navigation + boost watch time
Position: Middle section, clearly labeled
Formula: [MM:SS] [Chapter Title]

Rules:
  - Start at 00:00 (required for YouTube chapters)
  - Minimum 3 timestamps for chapter feature
  - Max 50 chars per chapter title
  - Use descriptive, keyword-rich titles

Structure:
  ⏱️ CAPÍTULOS:
  00:00 - Introdução
  01:23 - [Chapter 2 Title]
  04:56 - [Chapter 3 Title]
  ...

YouTube Chapter Requirements:
  - First timestamp MUST be 00:00
  - At least 3 timestamps
  - Minimum 10 seconds between chapters
  - Timestamps in ascending order

Character Budget: Variable (10-50 chars per chapter)
```

**SECTION 4 - LINKS & CTAs** 🔗
```
Purpose: Drive conversions, engagement, subscriptions
Position: After timestamps
Formula: [CTA] + [Organized Links]

Structure:
  🔗 LINKS MENCIONADOS:
  • [Resource Name]: [URL]

  📱 ME SIGA:
  • Instagram: [URL]
  • LinkedIn: [URL]

  🔔 Inscreva-se e ative o sininho para mais conteúdo!

  📧 Contato comercial: [email]

CTA Psychology:
  - Soft CTA: "Se curtiu, deixa o like 👍"
  - Medium CTA: "Inscreva-se para não perder os próximos"
  - Strong CTA: "CLIQUE NO LINK para [benefit]"

Link Priority:
  1. Resources mentioned in video
  2. Related videos/playlists
  3. Social media
  4. Website/newsletter
  5. Affiliate/sponsored (with disclosure)

Character Limit: 200-400
```

**SECTION 5 - HASHTAGS & KEYWORDS** #️⃣
```
Purpose: Discoverability without keyword stuffing
Position: End of description
Formula: 3-5 relevant hashtags + natural keyword sentence

Structure:
  [Natural keyword-rich sentence about the video topic]

  #Hashtag1 #Hashtag2 #Hashtag3

Rules:
  - Max 5 hashtags (YouTube recommendation)
  - First 3 hashtags appear above title
  - Mix: 1 broad + 2-3 specific + 1 branded
  - Keywords in sentence, not as hashtag list

Example:
  "Este tutorial de ChatGPT para programadores faz parte da série sobre IA para desenvolvedores."

  #ChatGPT #Programação #IA #DevTips #TechBrasil

Character Limit: 50-100
```

#### GENERATION RULES

```yaml
character_rules:
  total_limit: 5000
  recommended_range: 500-1500
  above_fold: 100-150
  minimum_viable: 200

section_order:
  1: hook (required)
  2: value_proposition (required)
  3: timestamps (if video >= 3min)
  4: links_ctas (required)
  5: hashtags_keywords (required)

formatting_rules:
  line_breaks: use blank lines between sections
  emojis: 1-2 per section header (optional)
  bullets: • for lists (not -)
  dividers: optional (━━━ or blank lines)
  caps: section headers only

keyword_integration:
  density_target: 1-3%
  primary_keyword:
    - in hook (first 25 words)
    - in value prop
    - in closing sentence
  secondary_keywords:
    - distributed naturally
    - max 1 per section

banned_patterns:
  - keyword_stuffing: repeating same keyword 5+ times
  - fake_urgency: "LAST CHANCE" without real deadline
  - excessive_caps: more than 2 words in ALL CAPS
  - spam_links: more than 10 links
  - empty_promises: claims video can't deliver
  - wall_of_text: no sections/breaks for 500+ chars

power_phrases_ptbr:
  hooks:
    - "Você já se perguntou..."
    - "O segredo que ninguém conta..."
    - "Pare de fazer isso errado..."
    - "Em X minutos você vai aprender..."
  ctas:
    - "Se esse vídeo te ajudou, deixa o like!"
    - "Inscreva-se para mais conteúdo como esse"
    - "Compartilha com quem precisa ver isso"
    - "Me conta nos comentários..."
  transitions:
    - "Vamos lá?"
    - "Bora começar!"
    - "Assista até o final para..."
```

**Output Phase 2**:
```json
{
  "description_generated": {
    "full_text": "string (complete description)",
    "char_count": 847,
    "sections": {
      "hook": {
        "content": "string",
        "char_count": 142
      },
      "value_proposition": {
        "content": "string",
        "char_count": 245
      },
      "timestamps": {
        "content": "string",
        "chapters": [
          {"timestamp": "00:00", "title": "Introdução"},
          {"timestamp": "02:34", "title": "..."}
        ]
      },
      "links_ctas": {
        "content": "string",
        "links_count": 4
      },
      "hashtags_keywords": {
        "content": "string",
        "hashtags": ["#tag1", "#tag2", "#tag3"]
      }
    },
    "keyword_analysis": {
      "primary_keyword": "ChatGPT programação",
      "occurrences": 3,
      "density": "2.1%",
      "first_position": 0
    }
  }
}
```

---

### PHASE 3: VALIDATE (10s)
**Objective**: Score description using 4D system, ensure quality gate

#### 4D SCORING SYSTEM

```yaml
scoring_dimensions:
  engagement_potential:
    weight: 0.35
    factors:
      - hook_quality: 0-3.0 (compelling above-fold)
      - cta_effectiveness: 0-2.0 (clear action)
      - scanability: 0-2.0 (bullets, sections)
      - value_clarity: 0-2.0 (clear promise)
      - emotional_trigger: 0-1.0 (curiosity, urgency)
    max_score: 10.0

  seo_alignment:
    weight: 0.30
    factors:
      - primary_keyword_present: +3.0
      - keyword_in_first_25_words: +2.0
      - secondary_keywords: +0.5 each (max 2.0)
      - keyword_density_optimal: +2.0 (1-3%)
      - no_keyword_stuffing: +1.0
    max_score: 10.0

  brand_alignment:
    weight: 0.20
    factors:
      - tone_consistency: 0-4.0 (with title/brand)
      - voice_markers: +1.0 per marker (max 3.0)
      - professional_formatting: 0-2.0
      - cta_style_match: 0-1.0
    max_score: 10.0

  technical_compliance:
    weight: 0.15
    factors:
      - char_count_valid: +3.0 (under 5000)
      - above_fold_optimized: +2.0 (100-150 compelling)
      - timestamps_valid: +2.0 (if applicable)
      - proper_formatting: +2.0
      - mobile_friendly: +1.0
    max_score: 10.0
```

#### SCORING CALCULATION

```python
def calculate_4d_score(description: Description, context: dict) -> float:
    scores = {
        "engagement": score_engagement_potential(description, context),
        "seo": score_seo_alignment(description, context),
        "brand": score_brand_alignment(description, context),
        "technical": score_technical_compliance(description)
    }

    weights = {"engagement": 0.35, "seo": 0.30, "brand": 0.20, "technical": 0.15}

    total = sum(scores[dim] * weights[dim] for dim in scores)
    return round(total, 2)
```

#### QUALITY GATE

```yaml
quality_gate:
  minimum_score: 7.5
  actions:
    if_below_threshold:
      - identify_weakest_dimension
      - enhance_specific_sections
      - regenerate_hook_if_engagement_low
      - if_still_below: flag_for_human_review
    if_above_threshold:
      - finalize_description
      - generate_alternatives (optional)
```

**Output Phase 3**:
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
    "above_fold": "ChatGPT para programação: 7 prompts que vão mudar sua forma de codar. Neste vídeo, você vai aprender...",
    "char_count_preview": 142
  }
}
```

---

## VALIDATION

### Quality Gates

```yaml
quality_gates:
  - name: total_char_limit
    check: char_count <= 5000
    action: truncate_with_ellipsis

  - name: above_fold_quality
    check: hook.char_count <= 150 AND hook.score >= 7.0
    action: rewrite_hook_if_fail

  - name: keyword_present
    check: primary_keyword in first_25_words
    action: inject_keyword_naturally

  - name: keyword_density
    check: 1% <= density <= 3%
    action: adjust_occurrences

  - name: timestamps_valid
    check: first_timestamp == "00:00" AND len >= 3
    action: fix_timestamp_format

  - name: minimum_score
    check: score_total >= 7.5
    action: enhance_or_flag

  - name: section_presence
    check: all required sections present
    action: add_missing_sections

  - name: no_banned_patterns
    check: no_banned_patterns_detected
    action: sanitize
```

### Thresholds

```yaml
thresholds:
  score_excellent: 9.0
  score_good: 7.5
  score_acceptable: 6.5
  score_reject: < 6.5

  char_total_max: 5000
  char_above_fold: 150
  char_recommended_min: 200
  char_recommended_max: 1500

  keyword_density_min: 1.0
  keyword_density_max: 3.0
  keyword_first_position: 25  # words

  hashtags_min: 3
  hashtags_max: 5

  timestamps_min_chapters: 3
  timestamps_min_duration: 180  # seconds (3 min)
```

---

## CONTEXT

**Usage**:
- Called by video_agent after title_optimizer for complete YouTube metadata
- Can be invoked standalone via `/youtube-description` command

**Upstream**:
- $video_brief from 10_concept_planner_HOP
- $title_optimizer_output from 60_title_optimizer_HOP (recommended)
- $brand_profile from marca_agent (optional)
- $seo_keywords from pesquisa_agent (optional)

**Downstream**:
- YouTube upload metadata
- Video tags generator (62_tags_optimizer)
- Thumbnail text optimizer (63_thumbnail_text)

**$arguments chaining**:
```
video_brief -> title_optimizer -> description_optimizer($title_output)
description_optimizer.description_full -> youtube_upload($description)
description_optimizer.timestamps -> video_chapters($chapters)
```

**Integration Modes**:
```yaml
mode_integrated:
  trigger: after title_optimizer completion
  input: $video_brief + $title_optimizer_output
  output: appends to video_output.json

mode_standalone:
  trigger: /youtube-description command
  input: direct user brief
  output: standalone description.json
```

---

## EXAMPLES

### Example 1: Tech Tutorial (Medium Length)

**Input**:
```json
{
  "video_brief": {
    "title_final": "7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer",
    "topic": "ChatGPT programação",
    "target_audience": "Desenvolvedores iniciantes/intermediários",
    "key_benefit": "Acelerar desenvolvimento com IA",
    "video_duration": "12:34"
  }
}
```

**Output**:
```json
{
  "description_full": "ChatGPT para programação: os 7 prompts que vão revolucionar seu workflow de desenvolvimento. Depois de testar 50+ prompts, esses são os que realmente funcionam.\n\n📌 O QUE VOCÊ VAI APRENDER:\n• Prompt para debug que encontra erros em segundos\n• Como pedir explicações de código complexo\n• Template para refatoração automática\n• Prompt para testes unitários instantâneos\n• Técnica para documentação que não dá preguiça\n\n👤 PARA QUEM É ESSE VÍDEO:\nDevs que querem usar IA de verdade no dia a dia, não só para \"hello world\".\n\n⏱️ CAPÍTULOS:\n00:00 - Por que 90% usa ChatGPT errado\n01:45 - Prompt #1: Debug Inteligente\n03:22 - Prompt #2: Explicação de Código\n05:10 - Prompt #3: Refatoração\n07:05 - Prompt #4: Testes Unitários\n08:50 - Prompt #5: Documentação\n10:15 - Prompt #6: Code Review\n11:30 - Prompt #7: Arquitetura\n12:00 - Resumo e Próximos Passos\n\n🔗 RECURSOS:\n• PDF com todos os prompts: [link]\n• Playlist IA para Devs: [link]\n\n📱 ME SIGA:\n• GitHub: [link]\n• LinkedIn: [link]\n\n🔔 Se esse vídeo te ajudou, deixa o like e se inscreve pro próximo!\n\nEsses prompts de ChatGPT para programação fazem parte da série sobre produtividade com IA para desenvolvedores.\n\n#ChatGPT #Programação #DesenvolvimentoDeSoftware #IA #DevTips",
  "char_count": 1247,
  "scores": {
    "engagement": 8.8,
    "seo": 8.5,
    "brand": 8.0,
    "technical": 9.2
  },
  "score_total": 8.62
}
```

### Example 2: Short Video (Minimal Description)

**Input**:
```json
{
  "video_brief": {
    "title_final": "Excel: 3 Atalhos Que Vão Mudar Sua Vida",
    "topic": "Atalhos Excel",
    "target_audience": "Profissionais de escritório",
    "key_benefit": "Economizar tempo",
    "video_duration": "02:45"
  }
}
```

**Output**:
```json
{
  "description_full": "3 atalhos de Excel que todo profissional deveria saber. Em menos de 3 minutos, você vai aprender truques que economizam HORAS por semana.\n\n📌 ATALHOS DO VÍDEO:\n• Ctrl+Shift+L: Filtro instantâneo\n• Alt+=: Soma automática\n• Ctrl+D: Preencher para baixo\n\n🔔 Gostou? Inscreva-se para mais dicas rápidas de produtividade!\n\n#Excel #Produtividade #Atalhos",
  "char_count": 347,
  "scores": {
    "engagement": 8.2,
    "seo": 7.8,
    "brand": 7.5,
    "technical": 9.5
  },
  "score_total": 8.22,
  "note": "No timestamps - video under 3 minutes"
}
```

### Example 3: Long Tutorial (Detailed Description)

**Input**:
```json
{
  "video_brief": {
    "title_final": "Curso Completo de React em 2024: Do Zero ao Projeto Final",
    "topic": "Curso React",
    "target_audience": "Iniciantes em programação web",
    "key_benefit": "Aprender React do básico ao avançado",
    "video_duration": "3:45:22"
  },
  "video_chapters": [
    {"timestamp": "00:00", "title": "Introdução e Setup"},
    {"timestamp": "15:30", "title": "Componentes Básicos"},
    {"timestamp": "45:00", "title": "Props e State"},
    {"timestamp": "1:20:00", "title": "Hooks Essenciais"},
    {"timestamp": "2:00:00", "title": "Projeto Prático"},
    {"timestamp": "3:00:00", "title": "Deploy"}
  ]
}
```

**Output**:
```json
{
  "description_full": "Curso completo de React 2024: aprenda do absoluto zero até deploy de um projeto real. Mais de 3 horas de conteúdo prático, atualizado com as últimas features.\n\n📌 O QUE VOCÊ VAI APRENDER:\n• Fundamentos de React (componentes, JSX)\n• Props, State e o ciclo de vida\n• Hooks: useState, useEffect, useContext, custom hooks\n• Projeto completo: do design ao deploy\n• Boas práticas e padrões modernos\n\n🎯 PRÉ-REQUISITOS:\n• HTML/CSS básico\n• JavaScript fundamentals\n• Vontade de aprender!\n\n👤 PARA QUEM É:\nIniciantes que querem entrar no mercado de front-end e devs que querem atualizar conhecimentos de React.\n\n⏱️ CAPÍTULOS:\n00:00 - Introdução e Setup do Ambiente\n15:30 - Seu Primeiro Componente\n45:00 - Props e State Explicados\n1:20:00 - Hooks Essenciais (useState, useEffect)\n1:55:00 - Context API e useContext\n2:00:00 - Projeto Prático: Início\n2:30:00 - Estilização com CSS Modules\n3:00:00 - Deploy na Vercel\n3:30:00 - Próximos Passos e Recursos\n\n🔗 RECURSOS:\n• Repositório do projeto: [link]\n• PDF com resumo: [link]\n• Playlist React Avançado: [link]\n\n📱 COMUNIDADE:\n• Discord: [link]\n• GitHub: [link]\n\n🔔 INSCREVA-SE para a parte 2 (React avançado com TypeScript)!\n\nEste curso de React foi criado para quem quer aprender desenvolvimento web moderno de forma prática e direta.\n\n#React #CursoReact #ProgramaçãoWeb #Frontend #JavaScript",
  "char_count": 1456,
  "score_total": 9.1
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
│  Phase 6++: DESCRIPTION OPTIMIZER (this HOP)                │
│           Input: $video_brief, $youtube_titles              │
│           Output: $youtube_description                      │
│                          ↓                                   │
│  Phase 6+++: Tags + Thumbnail (future HOPs)                 │
│                          ↓                                   │
│  Phase 7: YouTube Upload (external)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0
**Created**: 2025-12-04
**Author**: codexa_agent (meta-construction)
**Config**: config/youtube_description_rules.json
**Predecessor**: 60_title_optimizer_HOP.md
