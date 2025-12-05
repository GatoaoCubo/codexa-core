<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: video_agent
  Synced: 2025-12-05
  Version: 3.0.0
  Package: iso_vectorstore (export package)
-->

# PRIME: video_agent

**AI Assistant Entry Point** - Navigation guide for video production specialist

**Version**: 3.0.0 | **Status**: Production-Ready | **Type**: Specialist Agent + Master Orchestrator

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

> **LAW 9**: Scout-First Consolidation | Toda tarefa começa com scouts → CRUD Priority: Delete > Update > Read > Create

---

## 1. IDENTITY

`video_agent` transforms product briefs into professional e-commerce videos (15-60s) using AI video generation APIs, optimized for social media platforms.

**Output**: Final MP4 video + Trinity metadata (.md, .llm.json, .meta.json)

**Capabilities**:
- Storyboard generation (6-8 shots with narrative arc)
- Script writing (narration + text overlays + timing)
- Runway/Pika prompt engineering
- Async video clip generation
- FFmpeg editing (timeline, audio mixing, text overlays)
- TTS narration (ElevenLabs)
- **Shorts generation** (modular blocks: Hook + Educational + CTA)
- **Multi-variant parallel** (1 brief → N shorts via /spawn)
- **Platform optimization** (YouTube Shorts, TikTok, Instagram Reels)
- **Full production orchestration** (200_ADW master workflow)

**Model Configuration**:
- Reasoning: Claude Sonnet 4 (concept, script)
- Fast: Claude Haiku (visual prompts, validation)
- Video: Runway Gen-3 (primary), Pika 1.5 (fallback)
- TTS: ElevenLabs Multilingual v2

---

## 2. WHEN TO USE

**USE video_agent for**:
- Video ads (Instagram Reels, TikTok, YouTube Shorts)
- Product demos and showcases
- Brand campaign videos
- Social media content at scale
- E-commerce product videos

**DON'T USE for**:
- Static images (use photo_agent)
- Long-form content (>60s)
- Live editing or real-time processing
- Complex VFX or motion graphics
- Videos requiring human actors

---

## 3. NAVIGATION MAP

```
Entry Points:
├── PRIME.md (this file) ──► Start here for AI assistants
├── COMMAND_GUIDE.md ──► LLM vs Humano: como comandar criação
├── README.md ──► Overview, architecture, quick start
├── INSTRUCTIONS.md ──► Step-by-step workflows
└── SETUP.md ──► Configuration and API setup

Execution:
├── workflows/100_ADW_RUN_VIDEO.md ──► Complete 5-phase workflow
├── workflows/103_ADW_YOUTUBE_TITLE.md ──► Title optimization workflow
├── workflows/104_ADW_YOUTUBE_DESCRIPTION.md ──► Description optimization workflow
├── workflows/105_ADW_YOUTUBE_FULL_METADATA.md ──► Full YouTube metadata suite
├── workflows/110_ADW_RUN_SHORTS.md ──► Single short generation
├── workflows/111_ADW_SHORTS_MULTI_VARIANT.md ──► Parallel N shorts (/spawn)
├── workflows/200_ADW_FULL_VIDEO_PRODUCTION.md ──► MASTER ORCHESTRATOR
└── prompts/*.md ──► Detailed HOP prompts per stage

Implementation:
├── src/video_agent.py ──► Main orchestrator
├── builders/01-05_*.py ──► Stage builders
├── validators/*.py ──► Quality gates
└── schemas/*.json ──► Input/output contracts
```

---

## 4. WORKFLOWS

### 4.1 Standard Video (15-30s)
```
Input: Brief (produto, duracao, tom, objetivo)
Process: Concept → Script → Visual → Render → Edit
Output: final_video.mp4 + metadata
Duration: 3-5 minutes
```

### 4.2 Brand-Aligned Campaign
```
Input: Brief + brand_profile (colors, tone, logo)
Process: Load brand → Align storyboard → Generate → Validate brand
Output: Brand-compliant video
```

### 4.3 Multi-Product Batch
```
Input: products.json (list of briefs)
Process: Parallel generation (up to 5 concurrent)
Output: batch_results/ directory
```

### 4.4 Custom Storyboard
```
Input: Manual storyboard (skip concept stage)
Process: Script → Visual → Render → Edit
Output: Video from custom storyboard
```

### 4.5 YouTube Title Optimization
```
Input: Video brief OR post Phase 5 completion
Process: Research → Generate (5 angles) → Validate (4D scoring)
Output: 5 CTR-optimized titles + recommended winner
Duration: ~35 seconds
Command: /youtube-title (standalone)
```

**Title Angles**:
| Angle | CTR Multiplier | Best For |
|-------|----------------|----------|
| Question | 1.25x | Educational |
| Number | 1.36x ⭐ | Lists, tutorials |
| Social Proof | 1.18x | Case studies |
| How-To | 1.22x | Guides |
| Comparison | 1.30x | Reviews |

### 4.6 YouTube Description Optimization (NEW)
```
Input: Video brief + title_optimizer_output (optional)
Process: Research → Generate (5 sections) → Validate (4D scoring)
Output: SEO-optimized description with timestamps
Duration: ~35 seconds
Command: /youtube-description (standalone)
```

**Description Sections**:
| Section | Purpose | Char Limit |
|---------|---------|------------|
| Hook | Above-fold scroll-stopper | 100-150 |
| Value Prop | What viewer gets | 150-300 |
| Timestamps | Navigation + watch time | Variable |
| Links/CTAs | Conversions | 200-400 |
| Hashtags | Discoverability | 50-100 |

### 4.7 YouTube Tags Optimization (NEW)
```
Input: Video brief + title_output + description_output
Process: Research → Generate (4 categories) → Validate (4D scoring)
Output: 30-50 SEO-optimized tags (max 500 chars)
Duration: ~35 seconds
Command: /youtube-tags (standalone)
```

**Tag Categories**:
| Category | Count | Purpose |
|----------|-------|---------|
| Primary | 3-5 | Core keywords, high relevance |
| Secondary | 8-12 | Commercial intent, modifiers |
| Long-tail | 12-20 | Discovery, low competition |
| Semantic | 5-8 | Context signals, related topics |

### 4.8 YouTube Thumbnail Text Optimization (NEW)
```
Input: Title final + video brief
Process: Analyze → Generate (3-5 variants) → Validate (4D scoring)
Output: CTR-optimized text variants (3-5 words max)
Duration: ~35 seconds
Command: /youtube-thumbnail-text (standalone)
```

**Psychological Angles**:
| Angle | CTR Multiplier | Best For |
|-------|----------------|----------|
| Hook | 1.18x | Myth-busting, exposés |
| Benefit | 1.32x ⭐ | Educational, results |
| Curiosity | 1.25x | Comparisons, reveals |
| Urgency | 1.20x | Limited offers |
| Transformation | 1.28x | Tutorials, success |

### 4.9 YouTube Chapters Generation (NEW)
```
Input: Script OR transcript OR outline + duration
Process: Analyze → Generate → Validate (5D scoring)
Output: 5-10 timestamped chapters
Duration: ~35 seconds
Command: /youtube-chapters (standalone)
```

**Chapter Requirements**:
| Rule | Requirement |
|------|-------------|
| First chapter | MUST be 00:00 |
| Minimum chapters | 3 (YouTube requirement) |
| Minimum gap | 10 seconds between chapters |
| Max title length | 50 characters |
| Style | Action-oriented verbs |

### 4.10 Single Short Generation (NEW)
```
Input: Product brief + duration (15-60s) + angle
Process: Block Selection → Script → Visual → Production → Edit → Validate
Output: 1 short video (9:16) + Trinity metadata
Duration: ~90 seconds
Command: /run-short --angle question --duration 30
ADW: 110_ADW_RUN_SHORTS.md
```

**Block Library** (`config/shorts_blocks.json`):
| Block Type | Count | Purpose |
|------------|-------|---------|
| Hooks | 12 | Attention capture (0-3s) |
| Educational | 30 | Value delivery (middle) |
| CTAs | 8 | Conversion (final) |

**Hook Angles**:
| Angle | CTR Multiplier | Template |
|-------|----------------|----------|
| Question | 1.19x | "Voce sabia que {{STAT}}?" |
| Number | 1.36x | "{{N}} razoes para {{ACAO}}" |
| Curiosity | 1.25x | "O segredo que ninguem conta..." |
| Contrast | 1.28x | "{{ANTES}} vs {{DEPOIS}}" |
| Problem | 1.18x | "Cansado de {{PROBLEMA}}?" |

### 4.11 Multi-Variant Shorts (/spawn) (NEW)
```
Input: 1 Product brief + variant count (1-10)
Process: Plan → /spawn N parallel 110_ADW → Collect → Consolidate
Output: N shorts + batch manifest + report
Duration: ~90s (parallel) vs ~7min (sequential)
Command: /shorts-batch --variants 5 --duration 30
ADW: 111_ADW_SHORTS_MULTI_VARIANT.md
```

**Spawn Pattern**:
```
/spawn (max 5 parallel)
├── 110_ADW: angle=question
├── 110_ADW: angle=number
├── 110_ADW: angle=howto
├── 110_ADW: angle=contrast
└── 110_ADW: angle=social_proof
```

**Output Structure**:
```
outputs/shorts/{batch_id}/
├── videos/*.mp4          # N short videos
├── metadata/*.json       # Per-short metadata
├── BATCH_MANIFEST.json   # LLM-optimized
├── BATCH_REPORT.md       # Human-readable
└── ALL_SHORTS.llm.json   # Consolidated
```

### 4.12 Full Video Production (MASTER) (NEW)
```
Input: 1 Product Brief
Output: Complete multi-platform content package (~26 assets)
Duration: 6-15 minutes
Command: /full-video-production "Brief: ..."
ADW: 200_ADW_FULL_VIDEO_PRODUCTION.md
```

**Orchestration Architecture**:
```
200_ADW (Master Orchestrator)
│
├── STAGE A: 100_ADW_RUN_VIDEO (sequential)
│   └── Long-form video production
│
├── STAGE B: /spawn PARALLEL ─────────────────┐
│   ├── 105_ADW: YouTube metadata suite       │
│   ├── photo_agent: 5 thumbnail prompts      │ 2.4x speedup
│   └── 111_ADW: 5 shorts (spawn interno)     │
│                                              │
├── STAGE C: 72_platform_optimizer_HOP ───────┘
│   └── 15 platform variants (YT/TikTok/IG)
│
└── STAGE D: Consolidation
    └── Unified package + docs
```

**Output Package**:
```
outputs/production/{id}/
├── video/              # 1 long-form
├── youtube/            # Metadata suite
├── thumbnails/         # 5 Midjourney prompts
├── shorts/             # 5 videos + metadata
├── platforms/          # 15 variants
├── docs/               # Reports
├── MANIFEST.json       # LLM-friendly
└── README.md           # USER-friendly
```

**Performance**:
| Metric | Sequential | With /spawn | Gain |
|--------|-----------|-------------|------|
| Time | ~14 min | ~6 min | 2.4x |
| Assets | 26 | 26 | - |
| Cost | $10-12 | $10-12 | - |

---

## 5. QUICK START

### Minimal Input
```json
{
  "produto": "Tênis Nike Air Max 2024",
  "duracao": 30,
  "formato": "9:16",
  "tom": "energético, esportivo",
  "objetivo": "destacar amortecimento Air e design moderno"
}
```

### Expected Output
```
outputs/
├── tenis_nike_air_max_2024_30s.mp4  (final video)
├── tenis_nike_air_max_2024_30s.llm.json  (structured data)
└── tenis_nike_air_max_2024_30s.meta.json  (metadata)
```

### CLI Usage
```bash
python src/video_agent.py \
  --produto "Tênis Nike Air Max 2024" \
  --duracao 30 \
  --formato "9:16" \
  --tom "energético" \
  --objetivo "destacar amortecimento"
```

---

## 6. QUALITY GATES

### 11-Point Validation Checklist
1. Duration: 15-60s
2. Resolution: ≥1080p
3. Frame rate: ≥24fps
4. Audio sync: ±100ms tolerance
5. Text overlays: visible and readable
6. Brand compliance: colors, tone
7. No artifacts or glitches
8. File size: <50MB/minute
9. Codec: H.264 compatible
10. Aspect ratio: correct for platform
11. Metadata: complete

### Thresholds
- **Quality Score**: ≥7.0/10.0
- **Brand Compliance**: ≥8.0/10.0
- **Clip Success Rate**: ≥80%

---

## 7. KNOWLEDGE REFERENCE

### Style Presets
| Style | Camera | Lighting | Pacing | Use Case |
|-------|--------|----------|--------|----------|
| Energetic | Dynamic tracking | High contrast | Fast cuts | Sports, tech |
| Calm | Slow, smooth | Soft, warm | Slow dissolves | Wellness, luxury |
| Dramatic | Cinematic | Low-key | Variable | Premium, fashion |
| Minimal | Static | Clean | Measured | Design, modern |
| Cinematic | Smooth tracking | Golden hour | Narrative | Brand campaigns |

### Narrative Arc
```
Hook (0-3s) → Build (3-12s) → Benefit (12-20s) → Proof (20-25s) → CTA (25-30s)
```

### Audio Layers
1. **Narration**: ElevenLabs TTS, volume 1.0
2. **Music**: Background, volume 0.3
3. **SFX**: Optional, volume 0.5

---

## 8. TROUBLESHOOTING

| Symptom | Cause | Solution |
|---------|-------|----------|
| Workflow unclear | Missing context | Read `INSTRUCTIONS.md` |
| API timeout | Runway overload | Check retry settings, use Pika fallback |
| Audio desync | TTS timing off | Verify script timing, regenerate |
| Text not visible | Font missing | Check FFmpeg font path in config |
| Low quality clips | API issue | Increase quality setting, retry |
| Clips failed | API key invalid | Verify keys in `.env` |

---

## 9. RULES

### Limits
- Duration: 15-60 seconds
- Resolution: 1080p minimum
- Latency target: <350 seconds
- Cost target: <$1.00/video

### NEVER
- Skip storyboard validation
- Hardcode API keys in code
- Ignore brand guidelines
- Proceed with failed quality gates
- Generate without brief validation

### ALWAYS
- Generate storyboard first (concept before production)
- Validate each clip before assembly
- Mix audio layers (narration + music)
- Save Trinity output (.md, .llm.json, .meta.json)
- Log costs and timing

---

## 10. INTEGRATION

### Standalone
`video_agent` runs independently with 0 dependencies on other CODEXA agents.

### With Other Agents
```
marca_agent ──► Brand profile ──► video_agent (style alignment)
video_agent ──► Final video ──► anuncio_agent (ad copy sync)
pesquisa_agent ──► Competitor analysis ──► video_agent (differentiation)
```

### API Dependencies
- **Required**: Anthropic (Claude), Runway Gen-3
- **Optional**: Pika 1.5 (fallback), ElevenLabs (TTS), AWS S3 (storage)

---

## 11. FILES REFERENCE

### Core Files
| File | Purpose | Lines |
|------|---------|-------|
| `README.md` | Overview, quick start | ~350 |
| `PRIME.md` | AI entry point | ~450 |
| `COMMAND_GUIDE.md` | LLM vs Humano commands | ~350 |
| `INSTRUCTIONS.md` | Workflows | ~700 |
| `SETUP.md` | Configuration | ~700 |

### Builders (builders/)
| File | Stage | Purpose |
|------|-------|---------|
| `01_concept_builder.py` | 1 | Storyboard generation |
| `02_script_builder.py` | 2 | Narration + timing |
| `03_visual_builder.py` | 3 | Runway prompts |
| `04_production_builder.py` | 4 | API calls |
| `05_editing_builder.py` | 5 | FFmpeg assembly |

### HOPs (prompts/)
| File | Stage | Content |
|------|-------|---------|
| `10_concept_planner_HOP.md` | 1 | Storyboard instructions |
| `20_script_writer_HOP.md` | 2 | Script writing guide |
| `30_visual_prompter_HOP.md` | 3 | Prompt engineering |
| `40_production_runner_HOP.md` | 4 | API orchestration |
| `50_editor_assembler_HOP.md` | 5 | Editing workflow |
| `60_title_optimizer_HOP.md` | 6+ | YouTube title optimization (CTR-focused) |
| `61_description_optimizer_HOP.md` | 6++ | YouTube description optimization (SEO-focused) |
| `62_tags_optimizer_HOP.md` | 6+++ | YouTube tags optimization (SEO consistency) |
| `63_thumbnail_text_HOP.md` | 6++++ | Thumbnail text variants (CTR psychology) |
| `64_chapters_generator_HOP.md` | 6.5 | Chapter timestamps (navigation + SEO) |
| `72_platform_optimizer_HOP.md` | 7.2 | **Multi-platform optimization (YT/TikTok/IG)** |

### Configs (config/)
| File | Purpose |
|------|---------|
| `shorts_blocks.json` | **Block library: 12 hooks, 30 edu, 8 CTAs** |
| `voice_config.json` | 8 pt-BR voices (ElevenLabs) |
| `video_modes.json` | Overlay vs clean mode rules |
| `video_styles.json` | Style presets (energetic, calm, etc.) |
| `youtube_*.json` | YouTube optimization rules |

---

## 12. VERSION HISTORY

- **v3.0.0** (2025-12-05): Shorts & Master Orchestration
  - Added 72_platform_optimizer_HOP.md (multi-platform: YT/TikTok/IG)
  - Added 110_ADW_RUN_SHORTS.md (single short generation)
  - Added 111_ADW_SHORTS_MULTI_VARIANT.md (parallel N shorts via /spawn)
  - Added **200_ADW_FULL_VIDEO_PRODUCTION.md** (MASTER ORCHESTRATOR)
  - Added config/shorts_blocks.json (12 hooks, 30 educational, 8 CTAs)
  - Block-based modular Shorts architecture
  - /spawn parallel execution (2.4x speedup)
  - Unified output packages (MANIFEST.json + README.md)
  - Complete production pipeline: 1 brief → 26+ assets
  - Cross-platform optimization (YouTube Shorts, TikTok, Instagram Reels)
  - Integration with photo_agent for thumbnail prompts

- **v2.8.0** (2025-12-04): YouTube Optimization Suite Expansion
  - Added 62_tags_optimizer_HOP.md (Phase 6+++)
  - Added 63_thumbnail_text_HOP.md (Phase 6++++)
  - Added 64_chapters_generator_HOP.md (Phase 6.5)
  - Added youtube_tags_rules.json, youtube_thumbnail_rules.json, youtube_chapters_rules.json
  - Added tags_optimizer_input.json schema
  - 4 tag categories (Primary, Secondary, Long-tail, Semantic) with 500 char limit
  - 5 psychological thumbnail angles with CTR multipliers (Benefit 1.32x best)
  - 3 chapter input modes (transcript, script, outline) with 5D scoring
  - Complete YouTube metadata pipeline: Title → Description → Tags → Thumbnail → Chapters

- **v2.7.0** (2025-12-04): YouTube Description Optimizer
  - Added 61_description_optimizer_HOP.md (Phase 6++)
  - Added 104_ADW_YOUTUBE_DESCRIPTION.md workflow
  - Added youtube_description_rules.json config
  - Added description_optimizer_input.json schema
  - 5-section structure (Hook, Value Prop, Timestamps, Links, Hashtags)
  - 4D scoring system (Engagement 35%, SEO 30%, Brand 20%, Technical 15%)
  - Auto-timestamps for videos >= 3 minutes
  - Keyword density analysis (1-3% target)

- **v2.6.0** (2025-12-04): YouTube Title Optimizer
  - Added 60_title_optimizer_HOP.md (Phase 6+)
  - Added 103_ADW_YOUTUBE_TITLE.md workflow
  - Added youtube_title_rules.json config
  - Added title_optimizer_input.json schema
  - 5 psychological title angles (Question, Number, Social Proof, How-To, Comparison)
  - 4D scoring system (CTR 35%, SEO 30%, Brand 20%, Technical 15%)

- **v2.5.0** (2025-11-25): 12 Leverage Points Implementation
  - Restructured iso_vectorstore (22 -> 20 files)
  - Added execution_plans.json (4 plans: full, quick, batch, campaign)
  - Added production_patterns.json (scripts, hooks, transitions)
  - Added video_rules.json (production methodology)
  - Added output_template.md (Trinity specification)
  - Added CHANGELOG.md
  - Consolidated platform specs (6 files -> 1 JSON)
  - Task boundaries pattern for progress visibility
  - Mental checklist in QUICK_START

- **v2.0.0** (2025-11-25): Production Release
  - Pre-flight phase with auto-selection logic
  - Post-validation phase with 11-point checklist
  - Video modes: "overlay" (text) vs "clean" (--NO TEXT narration only)
  - PT-BR voice library (8 ElevenLabs voices)
  - Complete test suite with fixtures
  - Production templates (brand_story, product_demo, social_ad)
  - Trinity output example
  - PROCESSADOS/ knowledge cards
  - iso_vectorstore enriched (22 files)

- **v1.0.0** (2025-11-24): Initial release
  - 5-stage pipeline implementation
  - Runway/Pika integration
  - FFmpeg editing with TTS and text overlays
  - Trinity output format

---

## SHARED PRINCIPLES

> See full details: [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md)

### Tasks vs Roles (Sub-agents)
- ❌ "You are a video producer" → ✅ "Generate 8-shot storyboard for [product_brief]"
- ❌ "Create a video" → ✅ "Write narration script for 30s social ad, PT-BR"

### Human Ownership (Before Publish)
```markdown
- [ ] Video matches storyboard (all shots present)
- [ ] Audio sync correct (narration + music)
- [ ] Text overlays readable (contrast, timing)
- [ ] Brand voice consistent
- [ ] Platform specs met (aspect ratio, duration)
```

### Value Function (Video Confidence)
| Element | Confidence Check |
|---------|------------------|
| Storyboard | Narrative arc clear? 6-8 shots? |
| Script | Timing feasible? Triggers present? |
| Clips | API generation success? Quality OK? |
| Edit | Audio sync? Text readable? |

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-05
**Quality Score**: 9.8/10.0 (production-ready + master orchestration)
**12 Leverage Points**: Fully Implemented
**Orchestration**: 200_ADW Master + /spawn parallelism
