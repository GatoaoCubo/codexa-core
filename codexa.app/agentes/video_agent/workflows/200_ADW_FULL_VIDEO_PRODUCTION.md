# ADW-200: Full Video Production Pipeline (Master Orchestrator)

**Version**: 1.0.0
**Duration**: 8-15 minutes (spawn-optimized)
**Pattern**: 1 Brief → Complete Multi-Platform Content Package
**Mode**: Master Orchestrator (calls multiple ADWs via /spawn)

---

## EXECUTIVE SUMMARY

> **The Ultimate video_agent Workflow**: From a single product brief to a complete content package ready for YouTube, TikTok, Instagram, and more.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    200_ADW_FULL_VIDEO_PRODUCTION                            │
│                    "1 Brief → Complete Content Empire"                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INPUT: Product Brief                                                       │
│                                                                             │
│  OUTPUT:                                                                    │
│  ├── 1x Long-form video (15-60s)                                           │
│  ├── 5x YouTube-optimized metadata                                         │
│  ├── 5x Midjourney thumbnail prompts                                       │
│  ├── 5x Short videos (multi-angle)                                         │
│  ├── 15x Platform variants (YT/TikTok/IG)                                  │
│  ├── Cross-post schedule                                                   │
│  └── Unified documentation (USER + LLM)                                    │
│                                                                             │
│  TOTAL: ~20+ production-ready assets                                       │
│  TIME: 8-15 minutes (vs ~45min sequential)                                 │
│  COST: ~$8-12 USD                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ORCHESTRATION ARCHITECTURE

### ADW Dependency Graph

```
200_ADW_FULL_VIDEO_PRODUCTION (this)
│
├── STAGE A: 100_ADW_RUN_VIDEO (long-form production)
│   └── Sequential: Must complete first
│
├── STAGE B: /spawn PARALLEL ─────────────────────────────┐
│   ├── B.1: 105_ADW_YOUTUBE_FULL_METADATA               │
│   ├── B.2: photo_agent thumbnail prompts               │ PARALLEL
│   └── B.3: 111_ADW_SHORTS_MULTI_VARIANT (5 shorts)     │
│       └── Internally spawns 5x 110_ADW_RUN_SHORTS      │
│                                                         │
├── STAGE C: 72_platform_optimizer_HOP (per short) ──────┘
│   └── Sequential after B.3 completes
│
└── STAGE D: CONSOLIDATION
    └── Merge all outputs → Unified package
```

### Spawn Efficiency

| Stage | Mode | Time Sequential | Time Parallel | Speedup |
|-------|------|-----------------|---------------|---------|
| A | Sequential | 180s | 180s | 1x |
| B.1 | Parallel | 90s | - | - |
| B.2 | Parallel | 30s | 90s total | 1.3x |
| B.3 | Parallel | 475s | - | - |
| C | Sequential | 50s | 50s | 1x |
| D | Sequential | 30s | 30s | 1x |
| **TOTAL** | **Mixed** | **855s (~14min)** | **~350s (~6min)** | **2.4x** |

---

## WORKFLOW SPECIFICATION

```json
{
  "adw_id": "200_adw_full_video_production",
  "adw_name": "Full Video Production Pipeline",
  "agent": "video_agent",
  "version": "1.0.0",

  "orchestration": {
    "type": "master_orchestrator",
    "spawn_enabled": true,
    "max_parallel_stages": 3,
    "consolidation_pattern": "unified_package"
  },

  "calls": {
    "adws": [
      "100_ADW_RUN_VIDEO",
      "105_ADW_YOUTUBE_FULL_METADATA",
      "111_ADW_SHORTS_MULTI_VARIANT"
    ],
    "hops": [
      "72_platform_optimizer_HOP"
    ],
    "agents": [
      "photo_agent"
    ]
  },

  "input_contract": {
    "required": {
      "$product_brief": {
        "type": "object",
        "fields": ["produto", "duracao", "formato", "tom", "objetivo", "target_audience", "key_benefit"]
      }
    },
    "optional": {
      "$brand_profile": "object - from marca_agent",
      "$seo_keywords": "array - from pesquisa_agent",
      "$shorts_count": "integer - default 5",
      "$skip_stages": "array - stages to skip ['shorts', 'thumbnail', 'platform']",
      "$output_dir": "string - custom output directory"
    }
  },

  "output_contract": {
    "package_directory": "outputs/production/{production_id}/",
    "structure": {
      "video/": "Long-form video + Trinity metadata",
      "youtube/": "Title, description, tags, chapters",
      "thumbnails/": "5 Midjourney prompts",
      "shorts/": "5 short videos + metadata",
      "platforms/": "15 platform variants (YT/TT/IG)",
      "docs/": "Reports and guides",
      "MANIFEST.json": "Complete package manifest",
      "README.md": "Human navigation guide"
    }
  },

  "phases": [
    {"phase_id": "stage_a", "phase_name": "Long-Form Production", "duration": "~180s", "parallel": false},
    {"phase_id": "stage_b", "phase_name": "Parallel Generation", "duration": "~90s", "parallel": true},
    {"phase_id": "stage_c", "phase_name": "Platform Optimization", "duration": "~50s", "parallel": false},
    {"phase_id": "stage_d", "phase_name": "Consolidation", "duration": "~30s", "parallel": false}
  ]
}
```

---

## STAGE A: LONG-FORM VIDEO PRODUCTION

**ADW**: `100_ADW_RUN_VIDEO`
**Mode**: Sequential (foundation for all other stages)
**Duration**: ~180 seconds

### Execution

```python
# Stage A must complete before Stage B can start
stage_a_result = await execute_adw(
    adw="100_ADW_RUN_VIDEO",
    input={
        "$product_brief": product_brief,
        "$brand_profile": brand_profile
    }
)

# Extract outputs for downstream stages
long_form_video = stage_a_result["outputs"]["video_path"]
video_script = stage_a_result["chaining_data"]["$script"]
video_brief = stage_a_result["chaining_data"]["$video_brief"]
```

### Output → $stage_a

```json
{
  "status": "success",
  "video_path": "outputs/production/{id}/video/main_video.mp4",
  "duration_actual": 30,
  "quality_score": 8.5,
  "chaining_data": {
    "$video_brief": {...},
    "$script": {...},
    "$visual_prompts": [...]
  }
}
```

### Quality Gate
- [ ] Video file exists and playable
- [ ] Quality score >= 7.0
- [ ] Trinity output complete

---

## STAGE B: PARALLEL GENERATION (/spawn)

**Mode**: Parallel spawn of 3 independent workflows
**Duration**: ~90 seconds (limited by slowest)

### Spawn Command

```markdown
## /spawn (Stage B - Parallel Generation)

Execute 3 parallel workflows after Stage A completes:

/spawn
1. video_agent (105_ADW): Generate YouTube full metadata from $video_brief
2. photo_agent: Generate 5 thumbnail prompts from $video_brief + title
3. video_agent (111_ADW): Generate 5 shorts variants from $video_brief (parallel internally)
```

### Implementation

```python
async def stage_b_parallel(stage_a_result, product_brief, brand_profile):
    """
    Spawn 3 parallel workflows.
    Each is independent and can run simultaneously.
    """

    # Configure spawn
    spawn_tasks = [
        # B.1: YouTube Metadata
        {
            "id": "b1_youtube_metadata",
            "adw": "105_ADW_YOUTUBE_FULL_METADATA",
            "input": {
                "$video_brief": stage_a_result["chaining_data"]["$video_brief"],
                "$script": stage_a_result["chaining_data"]["$script"],
                "$brand_profile": brand_profile
            }
        },

        # B.2: Thumbnail Prompts (photo_agent)
        {
            "id": "b2_thumbnail_prompts",
            "agent": "photo_agent",
            "task": "generate_thumbnail_prompts",
            "input": {
                "$video_brief": stage_a_result["chaining_data"]["$video_brief"],
                "$title": None,  # Will use B.1 output if available
                "$prompt_count": 5,
                "$style": "youtube_thumbnail"
            }
        },

        # B.3: Shorts Multi-Variant (spawns 5 internal parallel)
        {
            "id": "b3_shorts_batch",
            "adw": "111_ADW_SHORTS_MULTI_VARIANT",
            "input": {
                "$product_brief": product_brief,
                "$variant_count": 5,
                "$duration_target": 30,
                "$batch_id": f"{production_id}_shorts"
            }
        }
    ]

    # Execute all in parallel
    results = await spawn_parallel(spawn_tasks, timeout=180000)

    return results
```

### B.1: YouTube Full Metadata

**ADW**: `105_ADW_YOUTUBE_FULL_METADATA`

**Output → $youtube_metadata**:
```json
{
  "title": {
    "text": "7 Prompts de ChatGPT Que Todo Dev Precisa",
    "score": 8.72
  },
  "description": {
    "full_text": "...",
    "char_count": 847
  },
  "tags": {
    "all_tags": [...],
    "tag_count": 43
  },
  "thumbnail_text": {
    "recommended": "2x Dev Speed"
  },
  "chapters": [...]
}
```

### B.2: Thumbnail Prompts (photo_agent)

**Agent**: `photo_agent`
**Task**: Generate 5 Midjourney prompts for YouTube thumbnail

**Output → $thumbnail_prompts**:
```json
{
  "prompts": [
    {
      "id": 1,
      "angle": "benefit",
      "prompt": "YouTube thumbnail, split composition, left side frustrated person at computer, right side happy person with charts going up, text area on right, vibrant colors, professional photography, 16:9 aspect ratio --ar 16:9 --v 6",
      "text_overlay": "2x Dev Speed"
    },
    // ... 4 more prompts
  ],
  "design_specs": {
    "resolution": "1280x720",
    "text_safe_zone": "right_third",
    "face_placement": "left_third"
  }
}
```

### B.3: Shorts Multi-Variant

**ADW**: `111_ADW_SHORTS_MULTI_VARIANT`
**Internal**: Spawns 5x `110_ADW_RUN_SHORTS` in parallel

**Output → $shorts_batch**:
```json
{
  "batch_id": "production_001_shorts",
  "shorts": [
    {"short_id": "short_001", "angle": "howto", "score": 8.7},
    {"short_id": "short_002", "angle": "social_proof", "score": 8.4},
    {"short_id": "short_003", "angle": "problem", "score": 8.2},
    {"short_id": "short_004", "angle": "question", "score": 8.5},
    {"short_id": "short_005", "angle": "number", "score": 8.9}
  ],
  "best_performer": "short_005",
  "total_cost_usd": 4.05
}
```

### Spawn Sync Point

```python
# Wait for all Stage B tasks to complete
stage_b_results = await wait_for_spawn(spawn_tasks)

# Validate results
youtube_metadata = stage_b_results["b1_youtube_metadata"]
thumbnail_prompts = stage_b_results["b2_thumbnail_prompts"]
shorts_batch = stage_b_results["b3_shorts_batch"]

# Handle partial failures
if youtube_metadata.status == "failed":
    raise CriticalFailure("YouTube metadata is required")

if thumbnail_prompts.status == "failed":
    log_warning("Thumbnail prompts failed, using fallback")
    thumbnail_prompts = generate_fallback_thumbnails()

if shorts_batch.status == "failed":
    log_warning("Shorts batch failed, continuing without shorts")
```

---

## STAGE C: PLATFORM OPTIMIZATION

**HOP**: `72_platform_optimizer_HOP`
**Mode**: Sequential (processes each short)
**Duration**: ~50 seconds

### Execution

```python
async def stage_c_platform_optimization(shorts_batch):
    """
    Optimize each short for multiple platforms.
    Creates 3 variants per short (YT Shorts, TikTok, IG Reels).
    """

    platform_variants = []

    for short in shorts_batch["shorts"]:
        variant_result = await execute_hop(
            hop="72_platform_optimizer_HOP",
            input={
                "$short_content": short,
                "$target_platforms": ["youtube_shorts", "tiktok", "instagram_reels"]
            }
        )

        platform_variants.append({
            "short_id": short["short_id"],
            "variants": variant_result["variants"],
            "cross_post_schedule": variant_result["cross_post_schedule"]
        })

    return platform_variants
```

### Output → $platform_variants

```json
{
  "total_variants": 15,
  "by_short": [
    {
      "short_id": "short_001",
      "variants": [
        {"platform": "youtube_shorts", "caption": "...", "hashtags": [...]},
        {"platform": "tiktok", "caption": "...", "hashtags": [...]},
        {"platform": "instagram_reels", "caption": "...", "hashtags": [...]}
      ],
      "cross_post_schedule": {
        "day_1": {"platform": "tiktok", "time": "19:00"},
        "day_2": {"platform": "instagram_reels", "time": "18:00"},
        "day_3": {"platform": "youtube_shorts", "time": "20:00"}
      }
    }
    // ... 4 more shorts
  ],
  "unified_schedule": {
    "week_1": [...],
    "week_2": [...]
  }
}
```

---

## STAGE D: CONSOLIDATION

**Mode**: Sequential (final assembly)
**Duration**: ~30 seconds

### Output Package Structure

```
outputs/production/{production_id}/
│
├── video/
│   ├── main_video.mp4              # Long-form video
│   ├── main_video.llm.json         # LLM metadata
│   └── main_video.meta.json        # Human metadata
│
├── youtube/
│   ├── metadata.json               # Complete YouTube metadata
│   ├── title_variants.json         # 5 title options
│   ├── description.txt             # Copy-paste ready
│   ├── tags.txt                    # Comma-separated
│   └── chapters.txt                # Timestamp format
│
├── thumbnails/
│   ├── THUMBNAIL_PROMPTS.md        # Human-readable guide
│   ├── prompts.json                # Midjourney prompts
│   └── design_specs.json           # Specs for designer
│
├── shorts/
│   ├── videos/
│   │   ├── short_001.mp4
│   │   ├── short_002.mp4
│   │   ├── short_003.mp4
│   │   ├── short_004.mp4
│   │   └── short_005.mp4
│   ├── metadata/
│   │   └── ... (llm.json + meta.json per short)
│   └── SHORTS_REPORT.md
│
├── platforms/
│   ├── youtube_shorts/
│   │   └── ... (captions, hashtags per short)
│   ├── tiktok/
│   │   └── ... (captions, hashtags per short)
│   ├── instagram_reels/
│   │   └── ... (captions, hashtags per short)
│   └── CROSS_POST_SCHEDULE.md
│
├── docs/
│   ├── PRODUCTION_REPORT.md        # Full production report
│   ├── COST_BREAKDOWN.json         # Detailed costs
│   ├── QUALITY_METRICS.json        # All quality scores
│   └── USAGE_GUIDE.md              # How to use this package
│
├── MANIFEST.json                   # Complete package manifest (LLM)
└── README.md                       # Human navigation guide
```

### MANIFEST.json (LLM-Optimized)

```json
{
  "manifest_version": "1.0.0",
  "production_id": "prod_codexa_20251205_143022",
  "created_at": "2025-12-05T14:30:22Z",
  "product": "CODEXA - IA para E-commerce",

  "summary": {
    "total_assets": 26,
    "long_form_videos": 1,
    "shorts": 5,
    "platform_variants": 15,
    "thumbnail_prompts": 5,
    "total_duration_seconds": 350,
    "total_cost_usd": 10.82,
    "avg_quality_score": 8.47
  },

  "assets": {
    "long_form": {
      "path": "video/main_video.mp4",
      "duration": 30,
      "quality_score": 8.5
    },
    "youtube_metadata": {
      "title": "7 Prompts de ChatGPT Que Todo Dev Precisa",
      "path": "youtube/metadata.json"
    },
    "shorts": {
      "count": 5,
      "best_performer": "short_005",
      "path": "shorts/videos/"
    },
    "platform_variants": {
      "youtube_shorts": 5,
      "tiktok": 5,
      "instagram_reels": 5,
      "path": "platforms/"
    },
    "thumbnails": {
      "count": 5,
      "path": "thumbnails/prompts.json"
    }
  },

  "quick_actions": {
    "upload_youtube_long": {
      "video": "video/main_video.mp4",
      "title": "youtube/metadata.json#title",
      "description": "youtube/description.txt",
      "tags": "youtube/tags.txt"
    },
    "upload_youtube_shorts": {
      "videos": "shorts/videos/*.mp4",
      "captions": "platforms/youtube_shorts/"
    },
    "upload_tiktok": {
      "videos": "shorts/videos/*.mp4",
      "captions": "platforms/tiktok/"
    },
    "upload_instagram": {
      "videos": "shorts/videos/*.mp4",
      "captions": "platforms/instagram_reels/"
    }
  },

  "chaining_data": {
    "$production_id": "prod_codexa_20251205_143022",
    "$all_video_paths": [...],
    "$best_short": "short_005",
    "$total_cost": 10.82
  }
}
```

### README.md (Human-Optimized)

```markdown
# Production Package: CODEXA

**Generated**: 2025-12-05 14:30:22
**Production ID**: prod_codexa_20251205_143022

---

## Quick Start

### 1. Upload Long-Form to YouTube
1. Open `video/main_video.mp4`
2. Copy title from `youtube/metadata.json`
3. Paste description from `youtube/description.txt`
4. Add tags from `youtube/tags.txt`
5. Generate thumbnail using `thumbnails/THUMBNAIL_PROMPTS.md`

### 2. Upload Shorts
- **YouTube Shorts**: Use `platforms/youtube_shorts/` captions
- **TikTok**: Use `platforms/tiktok/` captions
- **Instagram Reels**: Use `platforms/instagram_reels/` captions

### 3. Follow Cross-Post Schedule
See `platforms/CROSS_POST_SCHEDULE.md` for optimal timing.

---

## What's Inside

| Folder | Contents | Count |
|--------|----------|-------|
| `video/` | Long-form video + metadata | 1 |
| `youtube/` | Title, description, tags, chapters | 5 files |
| `thumbnails/` | Midjourney prompts | 5 prompts |
| `shorts/` | Short videos | 5 videos |
| `platforms/` | Platform-specific variants | 15 variants |
| `docs/` | Reports and guides | 4 files |

---

## Quality Summary

| Asset | Score | Status |
|-------|-------|--------|
| Long-form | 8.5/10 | Ready |
| YouTube Metadata | 8.6/10 | Ready |
| Shorts (avg) | 8.5/10 | Ready |
| Thumbnails | N/A | Prompts ready |

**Best Performer**: `short_005` (Number angle, 8.9/10)

---

## Costs

| Stage | Cost |
|-------|------|
| Long-form production | $2.50 |
| Shorts (5x) | $4.05 |
| TTS/Audio | $0.50 |
| API calls | $3.77 |
| **Total** | **$10.82** |

---

## Need Help?

- Production issues: Check `docs/PRODUCTION_REPORT.md`
- Quality concerns: Check `docs/QUALITY_METRICS.json`
- Usage questions: Check `docs/USAGE_GUIDE.md`
```

---

## USAGE

### Slash Command

```bash
# Full production with all stages
/full-video-production "Brief: CODEXA - IA para e-commerce sellers" --shorts 5

# Skip specific stages
/full-video-production "Brief: ..." --skip shorts,thumbnail

# Custom output directory
/full-video-production "Brief: ..." --output outputs/custom/
```

### Programmatic

```python
from video_agent import full_video_production

result = await full_video_production(
    product_brief={
        "produto": "CODEXA",
        "duracao": 30,
        "formato": "9:16",
        "tom": "energetico",
        "objetivo": "conversion",
        "target_audience": "E-commerce sellers BR",
        "key_benefit": "Automate 80% of listing creation"
    },
    brand_profile=marca_agent_output,  # optional
    shorts_count=5,
    skip_stages=[]
)

# Access outputs
manifest = result["manifest"]
video_path = manifest["assets"]["long_form"]["path"]
```

### Spawn Pattern (Reusable)

The spawn pattern used in Stage B is **reusable** for any multi-ADW orchestration:

```python
# Generic spawn pattern
async def spawn_adws(adw_configs: list, timeout: int = 180000):
    """
    Execute multiple ADWs in parallel.
    Returns when all complete or timeout.
    """
    tasks = [execute_adw(**config) for config in adw_configs]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

---

## ERROR HANDLING

### Stage Failure Matrix

| Stage | Failure | Recovery | Severity |
|-------|---------|----------|----------|
| A | Video production fails | Abort entire workflow | CRITICAL |
| B.1 | YouTube metadata fails | Retry 2x, then basic metadata | HIGH |
| B.2 | Thumbnail prompts fail | Use title-based fallback | LOW |
| B.3 | Shorts batch fails | Continue without shorts | MEDIUM |
| C | Platform optimization fails | Use shorts without variants | LOW |
| D | Consolidation fails | Manual assembly | LOW |

### Partial Success Handling

```python
def handle_partial_success(stage_results):
    """
    Always produce a package, even if some stages fail.
    """
    package = {
        "status": "partial" if any_failed(stage_results) else "complete",
        "assets": {}
    }

    # Always include Stage A (required)
    package["assets"]["long_form"] = stage_results["stage_a"]

    # Include successful optional stages
    for stage, result in stage_results.items():
        if result.status == "success":
            package["assets"][stage] = result

    # Generate warnings for failed stages
    package["warnings"] = [
        f"{stage} failed: {result.error}"
        for stage, result in stage_results.items()
        if result.status == "failed"
    ]

    return package
```

---

## METRICS

```json
{
  "production_metrics": {
    "total_time_seconds": 350,
    "sequential_estimate_seconds": 855,
    "speedup_factor": 2.44,
    "parallel_efficiency": 0.85
  },

  "cost_metrics": {
    "stage_a_usd": 2.50,
    "stage_b_usd": 7.32,
    "stage_c_usd": 0.50,
    "stage_d_usd": 0.50,
    "total_usd": 10.82,
    "cost_per_asset_usd": 0.42
  },

  "quality_metrics": {
    "long_form_score": 8.5,
    "youtube_metadata_score": 8.6,
    "shorts_avg_score": 8.5,
    "overall_score": 8.53
  },

  "output_metrics": {
    "total_assets": 26,
    "video_minutes": 5.8,
    "text_files": 12,
    "json_files": 8,
    "package_size_mb": 145
  }
}
```

---

## SCALABILITY

### Batch Production

```python
# Process multiple products in parallel
products = ["Product A", "Product B", "Product C"]

batch_results = await spawn_parallel([
    {
        "adw": "200_ADW_FULL_VIDEO_PRODUCTION",
        "input": {"$product_brief": brief}
    }
    for brief in products
])

# Each product gets its own package directory
```

### Resource Limits

```json
{
  "max_concurrent_200_adw": 3,
  "max_total_spawns": 15,
  "memory_limit_gb": 8,
  "api_rate_limits": {
    "runway": 10,
    "elevenlabs": 5,
    "claude": 60
  }
}
```

---

## VERSION HISTORY

### v1.0.0 (2025-12-05)
- Initial master orchestrator implementation
- Spawn-based parallel Stage B
- Integration with 100, 105, 110, 111 ADWs
- photo_agent thumbnail integration
- 72_platform_optimizer_HOP integration
- Unified output package structure
- USER + LLM optimized documentation
- Partial failure handling
- Scalable batch support

---

## DEPENDENCIES

### ADWs Called
| ADW | Stage | Purpose |
|-----|-------|---------|
| 100_ADW_RUN_VIDEO | A | Long-form production |
| 105_ADW_YOUTUBE_FULL_METADATA | B.1 | YouTube metadata |
| 111_ADW_SHORTS_MULTI_VARIANT | B.3 | Shorts batch |
| 110_ADW_RUN_SHORTS | B.3 (internal) | Individual shorts |

### HOPs Used
| HOP | Stage | Purpose |
|-----|-------|---------|
| 72_platform_optimizer_HOP | C | Multi-platform variants |

### Agents Called
| Agent | Stage | Purpose |
|-------|-------|---------|
| photo_agent | B.2 | Thumbnail prompts |

### Config Files
| File | Purpose |
|------|---------|
| `config/shorts_blocks.json` | Block library for shorts |
| `config/voice_config.json` | TTS voice selection |
| `config/video_modes.json` | Overlay/clean modes |

---

**Created by**: CODEXA Meta-Constructor
**Last Updated**: 2025-12-05
**Status**: Production Ready
**Type**: Master Orchestrator
**Spawn Pattern**: Parallel fan-out, sequential consolidation
