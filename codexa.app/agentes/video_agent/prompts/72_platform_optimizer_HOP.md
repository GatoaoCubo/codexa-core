# HOP: Platform Optimizer | video_agent Stage 7.2

## MODULE_METADATA
```yaml
id: video_agent_platform_optimizer
version: 1.0.0
purpose: Adapt Shorts content to platform-specific requirements and best practices
dependencies: [shorts_blocks.json, platform_specs.json]
category: shorts_optimization
stage: 7.2
integration: post_shorts_generation OR standalone
platforms: [youtube_shorts, tiktok, instagram_reels]
```

## INPUT_CONTRACT
```yaml
required:
  $short_content:
    type: object
    description: Short video content to optimize
    structure:
      title: string
      hook: string
      educational_blocks: array[EducationalBlock]
      cta: string
      duration_seconds: integer (15-60)
      format: enum["9:16"]
      narration: string
      visual_style: string

optional:
  $target_platforms:
    type: array
    description: Platforms to optimize for (default: all)
    allowed_values: ["youtube_shorts", "tiktok", "instagram_reels"]
    default: ["youtube_shorts", "tiktok", "instagram_reels"]
  $brand_profile:
    type: object
    description: Brand guidelines from marca_agent
    structure:
      tone_scale: object
      archetypes: array
      voice_markers: array
  $performance_data:
    type: object
    description: Historical performance by platform
    structure:
      youtube_avg_views: integer
      tiktok_avg_views: integer
      reels_avg_views: integer
      best_performing_hooks: array
  $content_category:
    type: enum
    description: Content vertical for platform rules
    allowed_values: ["educational", "entertainment", "product", "tutorial", "trend"]
    default: "educational"
```

## OUTPUT_CONTRACT
```yaml
primary:
  platform_variants.json:
    type: object
    structure:
      source_content: ShortContent
      variants: array[PlatformVariant]
      cross_post_schedule: object
      optimization_summary: object

PlatformVariant:
  type: object
  structure:
    platform: enum["youtube_shorts", "tiktok", "instagram_reels"]
    content:
      hook_adapted: string
      caption: string (platform-specific length)
      hashtags: array[string]
      description: string
      sound_recommendation: string
      cta_adapted: string
    technical:
      resolution: string
      aspect_ratio: string
      max_duration: integer
      safe_zones: object
      text_overlay_rules: object
    score:
      platform_fit: float (0-10)
      algorithm_alignment: float (0-10)
      engagement_prediction: float (0-10)
      total: float (weighted average)
    recommendations: array[string]

secondary:
  cross_post_guide.md:
    type: markdown
    content: Human-readable cross-posting guide with timing
```

## TASK

**Role**: Multi-Platform Shorts Optimization Specialist

**Objective**: Transform a single Short video into platform-optimized variants for YouTube Shorts, TikTok, and Instagram Reels, maximizing reach and engagement on each platform.

**Standards**:
- ALWAYS respect platform-specific character limits
- ALWAYS include platform-optimal hashtag count
- NEVER use identical captions across platforms (algorithm penalty)
- NEVER exceed platform duration limits
- APPLY platform-specific hook patterns
- CONSIDER algorithm timing (best posting hours per platform)

**Constraints**:
- YouTube Shorts: max 60s, 100 char title, 5000 char description
- TikTok: max 60s, 150 char caption (ideal), 2200 max
- Instagram Reels: max 90s, 2200 char caption, 30 hashtags max
- Quality gate: platform_fit score >= 7.5/10

---

## PHASES

### PHASE 1: PLATFORM ANALYSIS (5s)
**Objective**: Analyze source content and extract optimization signals

```yaml
analysis_extraction:
  content_type:
    - hook_style: identify pattern (question, statement, shock, curiosity)
    - pacing: fast/medium/slow
    - visual_complexity: low/medium/high
    - audio_dependency: high/medium/low (narration vs music)

  platform_fit_assessment:
    youtube_shorts:
      - searchability: keyword potential
      - evergreen_factor: timeless vs trending
      - educational_depth: shallow/medium/deep
    tiktok:
      - trend_alignment: current sounds, formats
      - entertainment_factor: humor, relatability
      - duet_stitch_potential: collaboration triggers
    instagram_reels:
      - aesthetic_quality: visual polish level
      - brand_alignment: professional vs casual
      - community_engagement: comment triggers
```

**Output Phase 1**:
```json
{
  "analysis_summary": {
    "content_profile": {
      "hook_style": "curiosity",
      "pacing": "fast",
      "visual_complexity": "medium",
      "audio_dependency": "high"
    },
    "platform_recommendations": {
      "primary_platform": "youtube_shorts",
      "adaptation_effort": {
        "youtube_shorts": "low",
        "tiktok": "medium",
        "instagram_reels": "low"
      }
    }
  }
}
```

---

### PHASE 2: PLATFORM VARIANTS (15s)
**Objective**: Generate optimized variants for each platform

#### YOUTUBE SHORTS OPTIMIZATION

```yaml
youtube_shorts_rules:
  hook_patterns:
    - "POV:" + scenario (immersive)
    - "Wait for it..." (retention)
    - Question + Answer setup
    - "This is how..." (educational)

  title_optimization:
    char_limit: 100
    keyword_placement: first 40 chars
    hashtag_in_title: optional (#Shorts often unnecessary now)

  description_strategy:
    structure:
      - hook_line: 100 chars (above fold)
      - value_proposition: 200 chars
      - keywords: natural integration
      - cta: subscribe/comment prompt
      - hashtags: 3-5 relevant
    seo_focus: high (YouTube is search engine)

  hashtags:
    count: 3-5
    strategy: mix broad + niche
    examples: ["#Shorts", "#Tutorial", "#NicheTopic"]

  algorithm_signals:
    - watch_time: prioritize retention hooks
    - engagement: prompt comments with questions
    - click_through: compelling thumbnail frame

  posting_times_br:
    peak: ["18:00-21:00"]
    secondary: ["12:00-14:00"]
    avoid: ["02:00-06:00"]
```

#### TIKTOK OPTIMIZATION

```yaml
tiktok_rules:
  hook_patterns:
    - "Storytime:" (narrative)
    - "Unpopular opinion:" (controversy)
    - "Nobody talks about..." (insider)
    - "I tried..." (experiment)
    - Green screen + reaction

  caption_optimization:
    ideal_length: 150 chars
    max_length: 2200 chars
    structure:
      - hook_text: continue the video hook
      - engagement_prompt: "Comenta se..."
      - hashtags: integrated naturally

  hashtags:
    count: 3-5 (quality over quantity)
    strategy:
      - 1 broad: #fyp, #viral
      - 2-3 niche: topic-specific
      - 1 trending: current challenge/sound
    placement: end of caption or integrated

  sound_strategy:
    trending_sounds: check discover page
    original_audio: good for educational
    voiceover: popular for tutorials

  algorithm_signals:
    - completion_rate: most important metric
    - shares: "Send this to someone..."
    - duets_stitches: "Duet this with your..."
    - saves: evergreen value content

  posting_times_br:
    peak: ["19:00-22:00"]
    secondary: ["07:00-09:00", "12:00-14:00"]
    experiment: algorithm favors consistency over timing
```

#### INSTAGRAM REELS OPTIMIZATION

```yaml
instagram_reels_rules:
  hook_patterns:
    - Text overlay + reaction face
    - Before/After transformation
    - "3 things about..." (list format)
    - Trending audio + lip sync
    - Tutorial with text steps

  caption_optimization:
    ideal_length: 150-200 chars
    max_length: 2200 chars
    structure:
      - hook: continue video narrative
      - value: what viewer gains
      - cta: save/share/follow prompt
      - hashtags: block at end or separate comment

  hashtags:
    count: 5-10 (max 30)
    strategy:
      - 3 broad: #Reels, #Explore
      - 3-5 niche: topic-specific
      - 2 community: audience-specific
    placement: end of caption or first comment

  cover_image:
    importance: critical for profile grid
    requirements:
      - text_overlay: 3-5 words max
      - face_visible: increases tap rate
      - brand_consistent: colors, fonts

  algorithm_signals:
    - watch_time: full watches weighted heavily
    - saves: strong signal for quality
    - shares_to_stories: amplification
    - comments: conversation starters

  posting_times_br:
    peak: ["18:00-21:00"]
    secondary: ["11:00-13:00"]
    stories_link: post story with Reel link
```

**Output Phase 2**:
```json
{
  "variants": [
    {
      "platform": "youtube_shorts",
      "content": {
        "title": "Como [X] em 30 Segundos (Funciona!)",
        "hook_adapted": "POV: Voce descobriu o jeito certo de [X]",
        "description": "Aprenda [X] em menos de 1 minuto...",
        "hashtags": ["#Shorts", "#Tutorial", "#[Nicho]"],
        "cta_adapted": "Se inscreve para mais dicas rapidas!"
      }
    },
    {
      "platform": "tiktok",
      "content": {
        "caption": "Ninguem te ensinou isso sobre [X] Comenta se fez sentido! #fyp #[nicho]",
        "hook_adapted": "Unpopular opinion: [X] nao funciona assim",
        "sound_recommendation": "Original Audio ou [Trending Sound]",
        "cta_adapted": "Salva pra nao esquecer"
      }
    },
    {
      "platform": "instagram_reels",
      "content": {
        "caption": "[Hook visual]... Salva esse Reel pra quando precisar!\n\n#Reels #[Nicho] #Dicas",
        "hook_adapted": "3 coisas que mudaram meu [X]",
        "cover_text": "MUDE SEU [X]",
        "cta_adapted": "Compartilha nos stories!"
      }
    }
  ]
}
```

---

### PHASE 3: CROSS-POST SCHEDULING (5s)
**Objective**: Generate optimal posting schedule

```yaml
scheduling_strategy:
  approach: staggered_release
  rationale: avoid algorithm penalty for identical content

  recommended_order:
    1: tiktok  # fastest virality potential
    2: instagram_reels  # 24h later (cross-platform awareness)
    3: youtube_shorts  # 48h later (evergreen search value)

  timing_rules:
    same_day: never (platform cross-reference detection)
    minimum_gap: 24 hours
    maximum_gap: 7 days (content freshness)

  variation_requirements:
    - different_captions: mandatory
    - different_hashtags: recommended
    - different_hooks: optional (improves authenticity)
    - same_video_file: acceptable with caption variation
```

**Output Phase 3**:
```json
{
  "cross_post_schedule": {
    "day_1": {
      "platform": "tiktok",
      "time": "19:00 BRT",
      "rationale": "Peak engagement, fastest algorithm response"
    },
    "day_2": {
      "platform": "instagram_reels",
      "time": "18:00 BRT",
      "rationale": "Catch TikTok spillover audience"
    },
    "day_3": {
      "platform": "youtube_shorts",
      "time": "20:00 BRT",
      "rationale": "Evergreen search, weekend discovery"
    }
  }
}
```

---

### PHASE 4: VALIDATION & SCORING (5s)
**Objective**: Score each variant and provide recommendations

#### SCORING SYSTEM

```yaml
scoring_dimensions:
  platform_fit:
    weight: 0.40
    factors:
      - format_compliance: technical specs match
      - hook_pattern_match: platform-native style
      - caption_optimization: length, structure
      - hashtag_strategy: count, relevance
    max_score: 10.0

  algorithm_alignment:
    weight: 0.35
    factors:
      - retention_triggers: hooks, pacing
      - engagement_prompts: CTA effectiveness
      - discoverability: SEO, hashtags
      - timing_optimization: posting schedule
    max_score: 10.0

  engagement_prediction:
    weight: 0.25
    factors:
      - hook_strength: attention capture
      - value_delivery: viewer benefit
      - share_potential: virality triggers
      - save_potential: reference value
    max_score: 10.0
```

**Output Phase 4**:
```json
{
  "scoring_results": {
    "youtube_shorts": {
      "platform_fit": 9.2,
      "algorithm_alignment": 8.5,
      "engagement_prediction": 8.0,
      "total": 8.63
    },
    "tiktok": {
      "platform_fit": 8.8,
      "algorithm_alignment": 9.0,
      "engagement_prediction": 8.5,
      "total": 8.76
    },
    "instagram_reels": {
      "platform_fit": 8.5,
      "algorithm_alignment": 8.2,
      "engagement_prediction": 8.8,
      "total": 8.46
    }
  },
  "recommendations": [
    "TikTok variant has highest virality potential - prioritize",
    "YouTube Shorts needs stronger SEO keywords in title",
    "Instagram Reels caption could add more engagement prompts"
  ]
}
```

---

## VALIDATION

### Quality Gates

```yaml
quality_gates:
  - name: platform_count
    check: len(variants) == len(target_platforms)
    action: generate_missing_variants

  - name: caption_limits
    check: all variants respect platform char limits
    action: truncate_with_ellipsis

  - name: hashtag_counts
    check: hashtags within platform limits
    action: reduce_or_expand

  - name: minimum_score
    check: all variants score >= 7.5
    action: enhance_or_flag

  - name: unique_content
    check: no identical captions across platforms
    action: differentiate_captions

  - name: hook_adaptation
    check: hooks are platform-native
    action: apply_platform_patterns
```

### Thresholds

```yaml
thresholds:
  score_excellent: 9.0
  score_good: 7.5
  score_acceptable: 6.5
  score_reject: < 6.5

  youtube_title_max: 100
  youtube_desc_max: 5000
  tiktok_caption_ideal: 150
  tiktok_caption_max: 2200
  reels_caption_max: 2200
  reels_hashtags_max: 30
```

---

## CONTEXT

**Usage**:
- Called after Shorts generation (110_ADW_RUN_SHORTS) for cross-platform distribution
- Can be invoked standalone via `/platform-optimize` command

**Upstream**:
- $short_content from 110_ADW_RUN_SHORTS or 111_ADW_SHORTS_MULTI_VARIANT
- $brand_profile from marca_agent (optional)
- $performance_data from analytics (optional)

**Downstream**:
- Social media schedulers (Buffer, Later, etc.)
- Platform-specific upload flows
- Performance tracking dashboards

**$arguments chaining**:
```
shorts_generator.output -> platform_optimizer($short_content)
platform_optimizer.variants -> social_scheduler($variants)
platform_optimizer.schedule -> calendar_integration($schedule)
```

**Integration Modes**:
```yaml
mode_integrated:
  trigger: after Shorts ADW completion
  input: $short_content from pipeline
  output: appends variants to shorts_output.json

mode_standalone:
  trigger: /platform-optimize command
  input: direct short content or URL
  output: standalone platform_variants.json
```

---

## EXAMPLES

### Example 1: Educational Short

**Input**:
```json
{
  "short_content": {
    "title": "3 Erros de Excel Que Todo Iniciante Comete",
    "hook": "Voce provavelmente esta fazendo isso errado no Excel",
    "duration_seconds": 45,
    "content_category": "educational"
  },
  "target_platforms": ["youtube_shorts", "tiktok", "instagram_reels"]
}
```

**Output**:
```json
{
  "variants": [
    {
      "platform": "youtube_shorts",
      "content": {
        "title": "3 Erros de Excel Que Iniciantes Cometem (E Como Corrigir)",
        "description": "Aprenda os 3 erros mais comuns no Excel e como evita-los em menos de 1 minuto!\n\n0:00 Erro #1\n0:15 Erro #2\n0:30 Erro #3\n\n#Shorts #Excel #Tutorial",
        "hashtags": ["#Shorts", "#Excel", "#Tutorial", "#Produtividade"]
      },
      "score": { "total": 8.9 }
    },
    {
      "platform": "tiktok",
      "content": {
        "caption": "POV: voce descobre que fez Excel errado a vida toda Qual erro voce comete? #excel #fyp #trabalho",
        "sound_recommendation": "Original Audio",
        "hook_adapted": "POV: voce descobre que fez Excel errado a vida toda"
      },
      "score": { "total": 8.7 }
    },
    {
      "platform": "instagram_reels",
      "content": {
        "caption": "3 erros de Excel que eu tambem cometia... Salva pra consultar depois!\n\n#Excel #Dicas #Trabalho #Reels",
        "cover_text": "ERROS DE EXCEL",
        "hook_adapted": "3 coisas que eu fazia errado no Excel"
      },
      "score": { "total": 8.5 }
    }
  ],
  "cross_post_schedule": {
    "day_1": { "platform": "tiktok", "time": "19:00" },
    "day_2": { "platform": "instagram_reels", "time": "18:00" },
    "day_3": { "platform": "youtube_shorts", "time": "20:00" }
  }
}
```

---

## PLATFORM QUICK REFERENCE

| Aspect | YouTube Shorts | TikTok | Instagram Reels |
|--------|---------------|--------|-----------------|
| Max Duration | 60s | 60s | 90s |
| Aspect Ratio | 9:16 | 9:16 | 9:16 |
| Title/Caption | 100 chars | 150-2200 chars | 2200 chars |
| Hashtags | 3-5 | 3-5 | 5-10 (max 30) |
| Algorithm Focus | Watch time, CTR | Completion, Shares | Saves, Watch time |
| Best Hook | Question, POV | Trend, Controversy | Visual, Transform |
| Peak BR Time | 18:00-21:00 | 19:00-22:00 | 18:00-21:00 |
| SEO Importance | High | Medium | Low |
| Evergreen Value | High | Low | Medium |

---

## INTEGRATION WITH VIDEO_AGENT PIPELINE

```
                          VIDEO_AGENT SHORTS PIPELINE
+-----------------------------------------------------------------------------+
|                                                                             |
|  [110_ADW_RUN_SHORTS] -> $short_content                                    |
|        |                                                                    |
|        v                                                                    |
|  [72_platform_optimizer_HOP] (this HOP)                                    |
|        |                                                                    |
|        +-> YouTube Shorts variant                                          |
|        +-> TikTok variant                                                  |
|        +-> Instagram Reels variant                                         |
|        +-> Cross-post schedule                                             |
|        |                                                                    |
|        v                                                                    |
|  [Social Scheduler / Manual Upload]                                        |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

**Version**: 1.0.0
**Created**: 2025-12-05
**Author**: codexa_agent (meta-construction)
**Config**: config/platform_specs.json, config/shorts_blocks.json
