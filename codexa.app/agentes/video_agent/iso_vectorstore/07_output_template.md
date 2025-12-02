# Output Template | video_agent

**Version**: 2.5.0
**Purpose**: Trinity output format specification for all video_agent outputs

---

## TRINITY OUTPUT FORMAT

Every video_agent execution produces 3 files:

```
outputs/
├── {product}_{duration}s.mp4       # Final video
├── {product}_{duration}s.llm.json  # LLM-readable metadata
└── {product}_{duration}s.meta.json # Human-readable metadata
```

---

## FILE 1: Video (.mp4)

### Technical Specs

| Property | Value |
|----------|-------|
| Codec | H.264 (libx264) |
| Container | MP4 |
| Resolution | 1080p minimum |
| Frame Rate | 30fps (default), 24fps/60fps optional |
| Bitrate | 8M video, 192k audio |
| Faststart | Enabled (streaming) |

### Aspect Ratios

| Format | Resolution | Platform |
|--------|------------|----------|
| 9:16 | 1080x1920 | Instagram Reels, TikTok, Shorts |
| 16:9 | 1920x1080 | YouTube, Facebook |
| 1:1 | 1080x1080 | Instagram Feed |

---

## FILE 2: LLM Metadata (.llm.json)

Structured data for LLM consumption and downstream processing.

```json
{
  "$schema": "video_output.json",
  "video_id": "nike_air_max_30s_20251125",
  "generated_at": "2025-11-25T10:30:00Z",
  "agent_version": "2.5.0",

  "brief": {
    "produto": "Nike Air Max 2024",
    "duracao": 30,
    "formato": "9:16",
    "tom": "energetico",
    "objetivo": "destacar amortecimento Air"
  },

  "config": {
    "video_mode": "overlay",
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "voice_name": "Camila",
    "platform": "runway",
    "style_preset": "energetic"
  },

  "storyboard": {
    "shots_count": 6,
    "narrative_arc": "Hook -> Build -> Benefit -> CTA",
    "shots": [
      {
        "number": 1,
        "duration": 4,
        "type": "hook",
        "description": "Close-up do tenis girando"
      }
    ]
  },

  "script": {
    "narration_segments": 5,
    "text_overlays": [
      {"text": "NIKE AIR MAX", "start": 1, "end": 4},
      {"text": "R$ 599 | Compre agora", "start": 27, "end": 30}
    ],
    "music_track": "music/upbeat.mp3"
  },

  "production": {
    "clips_generated": 6,
    "clips_successful": 6,
    "platform_used": "runway",
    "total_cost_usd": 0.97
  },

  "quality": {
    "score": 8.5,
    "checks_passed": 11,
    "checks_failed": 0,
    "mode_compliance": true
  }
}
```

---

## FILE 3: Human Metadata (.meta.json)

Human-readable metadata with performance metrics.

```json
{
  "title": "Nike Air Max 2024 - Video Ad 30s",
  "description": "Video promocional energetico para Instagram Reels",
  "created_at": "2025-11-25T10:30:00Z",
  "created_by": "video_agent v2.5.0",

  "video_info": {
    "file_path": "outputs/nike_air_max_30s.mp4",
    "file_size_mb": 12.5,
    "duration_seconds": 30,
    "resolution": "1080x1920",
    "format": "9:16"
  },

  "production_info": {
    "total_time_seconds": 245,
    "phases_completed": 7,
    "video_mode": "overlay",
    "voice_used": "Camila (pt-BR)"
  },

  "cost_breakdown": {
    "llm_calls_usd": 0.07,
    "video_generation_usd": 0.90,
    "storage_usd": 0.001,
    "total_usd": 0.97
  },

  "quality_metrics": {
    "quality_score": 8.5,
    "brand_compliance": 9.0,
    "technical_score": 8.0,
    "recommendation": "Ready for publish"
  },

  "tags": ["nike", "tenis", "esportivo", "instagram", "reels"],

  "files_generated": [
    "outputs/nike_air_max_30s.mp4",
    "outputs/nike_air_max_30s.llm.json",
    "outputs/nike_air_max_30s.meta.json"
  ]
}
```

---

## NAMING CONVENTION

```
{produto_slug}_{duracao}s.{ext}
```

**Rules**:
- produto_slug: lowercase, underscores, no special chars
- duracao: integer seconds
- ext: mp4 | llm.json | meta.json

**Examples**:
- `nike_air_max_30s.mp4`
- `fone_bluetooth_premium_15s.llm.json`
- `curso_codexa_45s.meta.json`

---

## VALIDATION

Trinity output is valid when:
- [ ] All 3 files exist
- [ ] .mp4 is playable
- [ ] .llm.json is valid JSON
- [ ] .meta.json is valid JSON
- [ ] Filenames match convention
- [ ] quality_score >= 7.0

---

**File**: 07_output_template.md
**Category**: output_specification
**Last Updated**: 2025-11-25
