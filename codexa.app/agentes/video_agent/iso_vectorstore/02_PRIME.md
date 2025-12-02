<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: video_agent
  Synced: 2025-11-30
  Version: 2.5.0
  Package: iso_vectorstore (export package)
-->

# PRIME: video_agent

**AI Assistant Entry Point** - Navigation guide for video production specialist

**Version**: 2.5.0 | **Status**: Production-Ready | **Type**: Specialist Agent

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

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
├── README.md ──► Overview, architecture, quick start
├── INSTRUCTIONS.md ──► Step-by-step workflows
└── SETUP.md ──► Configuration and API setup

Execution:
├── workflows/100_ADW_RUN_VIDEO.md ──► Complete 5-phase workflow
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
| `PRIME.md` | AI entry point | ~250 |
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

---

## 12. VERSION HISTORY

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
**Last Updated**: 2025-11-29
**Quality Score**: 9.5/10.0 (production-ready)
**12 Leverage Points**: Fully Implemented
