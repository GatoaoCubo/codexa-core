<!-- iso_vectorstore -->
<!--
  Source: 40_production_runner_HOP.md
  Agent: video_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Production Runner | video_agent Stage 4

## MODULE_METADATA
```yaml
id: video_agent_production_runner
version: 1.0.0
purpose: Orchestrate async video generation via Runway/Pika APIs
dependencies: [visual_prompts.json, api_config.json]
category: video_production
stage: 4
```

## INPUT_CONTRACT
```yaml
required:
  $visual_prompts:
    type: array
    source: visual_prompts.json
    description: Prompts from Stage 3
optional:
  $primary_api:
    type: string
    enum: ["runway", "pika"]
    default: "runway"
    description: Primary video generation API
  $fallback_api:
    type: string
    enum: ["runway", "pika", "none"]
    default: "pika"
    description: Fallback API if primary fails
  $max_concurrent:
    type: integer
    default: 5
    description: Max parallel API calls
  $max_retries:
    type: integer
    default: 3
    description: Max retry attempts per clip
```

## OUTPUT_CONTRACT
```yaml
primary:
  clips:
    type: array
    structure:
      - shot_number: integer
        clip_path: string
        success: boolean
        api_used: string
        cost_usd: number
        generation_time_s: number
        error: string | null
secondary:
  production_report.json:
    type: object
    structure:
      total_clips: integer
      successful_clips: integer
      failed_clips: integer
      total_cost_usd: number
      total_time_s: number
```

## TASK

**Role**: API Orchestrator

**Objective**: Generate all video clips efficiently using parallel async API calls with retry logic and fallback handling.

**Standards**:
- Use async/await for parallel generation
- Implement exponential backoff for retries
- Track costs per clip and total
- Validate clips before saving (resolution, duration)
- Use fallback API only after primary fails

**Constraints**:
- Max 5 concurrent API calls (rate limiting)
- Max 3 retries per clip
- Timeout: 300s per clip
- Total budget: $2.00 max

## STEPS

### Step 1: Initialize Connections
```python
import asyncio
import httpx
from pathlib import Path

# Load API config
api_config = load_config("config/api_config.json")

# Initialize clients
runway_client = RunwayClient(
    api_key=os.getenv("RUNWAY_API_KEY"),
    base_url=api_config["runway"]["base_url"],
    timeout=api_config["runway"]["timeout_seconds"]
)

pika_client = PikaClient(
    api_key=os.getenv("PIKA_API_KEY"),
    base_url=api_config["pika"]["base_url"],
    timeout=api_config["pika"]["timeout_seconds"]
)

# Create output directory
output_dir = Path("outputs/clips")
output_dir.mkdir(parents=True, exist_ok=True)
```

### Step 2: Define Generation Task
```python
async def generate_clip(prompt_data, api_client, semaphore):
    """Generate single clip with retry logic"""

    async with semaphore:  # Limit concurrent calls
        for attempt in range($max_retries):
            try:
                # Call API
                result = await api_client.generate(
                    prompt=prompt_data["runway_prompt"],
                    duration=prompt_data["duration"],
                    aspect_ratio="9:16"
                )

                # Wait for completion
                video_url = await api_client.wait_for_completion(
                    job_id=result["job_id"],
                    timeout=300
                )

                # Download clip
                clip_path = output_dir / f"clip_{prompt_data['shot_number']:03d}.mp4"
                await download_video(video_url, clip_path)

                # Validate clip
                if not validate_clip(clip_path):
                    raise ValueError("Clip validation failed")

                return {
                    "shot_number": prompt_data["shot_number"],
                    "clip_path": str(clip_path),
                    "success": True,
                    "api_used": api_client.name,
                    "cost_usd": api_client.get_cost(prompt_data["duration"]),
                    "generation_time_s": result["generation_time"],
                    "error": None
                }

            except Exception as e:
                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s")
                await asyncio.sleep(wait_time)

        # All retries failed
        return {
            "shot_number": prompt_data["shot_number"],
            "clip_path": None,
            "success": False,
            "api_used": api_client.name,
            "cost_usd": 0,
            "generation_time_s": 0,
            "error": str(e)
        }
```

### Step 3: Run Parallel Generation
```python
async def generate_all_clips(visual_prompts):
    """Generate all clips in parallel with rate limiting"""

    semaphore = asyncio.Semaphore($max_concurrent)
    primary_client = runway_client if $primary_api == "runway" else pika_client
    fallback_client = pika_client if $fallback_api == "pika" else runway_client

    # First pass: primary API
    tasks = [
        generate_clip(vp, primary_client, semaphore)
        for vp in visual_prompts
    ]
    results = await asyncio.gather(*tasks)

    # Second pass: fallback for failures
    if $fallback_api != "none":
        failed_indices = [
            i for i, r in enumerate(results) if not r["success"]
        ]

        if failed_indices:
            print(f"Retrying {len(failed_indices)} clips with fallback API")

            fallback_tasks = [
                generate_clip(visual_prompts[i], fallback_client, semaphore)
                for i in failed_indices
            ]
            fallback_results = await asyncio.gather(*fallback_tasks)

            for i, result in zip(failed_indices, fallback_results):
                results[i] = result

    return results
```

### Step 4: Validate Clips
```python
def validate_clip(clip_path):
    """Validate generated clip meets quality standards"""

    # Check file exists
    if not clip_path.exists():
        return False

    # Check file size (>100KB)
    if clip_path.stat().st_size < 100_000:
        return False

    # Check video properties with ffprobe
    probe = ffprobe(clip_path)

    # Resolution check (>=720p)
    width = probe["streams"][0]["width"]
    height = probe["streams"][0]["height"]
    if min(width, height) < 720:
        return False

    # Duration check
    duration = float(probe["format"]["duration"])
    if duration < 1.0:
        return False

    return True
```

### Step 5: Track Costs
```python
def calculate_costs(results):
    """Calculate total generation costs"""

    cost_per_second = {
        "runway": 0.05,
        "pika": 0.03
    }

    total_cost = sum(r["cost_usd"] for r in results if r["success"])

    return {
        "total_cost_usd": total_cost,
        "clips_generated": len([r for r in results if r["success"]]),
        "budget_remaining": 2.00 - total_cost
    }
```

### Step 6: Output
```python
# Run generation
results = await generate_all_clips($visual_prompts)

# Calculate metrics
costs = calculate_costs(results)
success_rate = len([r for r in results if r["success"]]) / len(results)

# Generate report
report = {
    "total_clips": len(results),
    "successful_clips": len([r for r in results if r["success"]]),
    "failed_clips": len([r for r in results if not r["success"]]),
    "success_rate": success_rate,
    "total_cost_usd": costs["total_cost_usd"],
    "total_time_s": sum(r["generation_time_s"] for r in results),
    "clips": results
}

# Output
output = results  # Array of clip results
```

## OUTPUT EXAMPLE
```json
[
  {
    "shot_number": 1,
    "clip_path": "outputs/clips/clip_001.mp4",
    "success": true,
    "api_used": "runway",
    "cost_usd": 0.15,
    "generation_time_s": 45.2,
    "error": null
  },
  {
    "shot_number": 2,
    "clip_path": "outputs/clips/clip_002.mp4",
    "success": true,
    "api_used": "runway",
    "cost_usd": 0.20,
    "generation_time_s": 52.1,
    "error": null
  },
  {
    "shot_number": 3,
    "clip_path": "outputs/clips/clip_003.mp4",
    "success": true,
    "api_used": "pika",
    "cost_usd": 0.12,
    "generation_time_s": 38.5,
    "error": null
  }
]
```

## VALIDATION

Quality Gates:
- [ ] Success rate >= 80%
- [ ] All successful clips >= 720p
- [ ] Total cost <= $2.00
- [ ] All clips downloaded and validated
- [ ] Production report generated

Thresholds:
- Success rate: >= 80%
- Resolution: >= 720p
- Budget: <= $2.00
- Timeout: 300s per clip

## CONTEXT

**Usage**: Called by video_agent.py as fourth pipeline stage

**Upstream**:
- visual_prompts.json from Stage 3
- api_config.json from config

**Downstream**:
- clips/*.mp4 -> 05_editing_builder.py (assembly)

**$arguments chaining**:
```
clips[].clip_path -> editing_builder($clips)
clips[].success -> editing_builder (filter failed)
```

**Assumptions**:
- API keys are set in environment
- Network connectivity available
- Sufficient API quota
- FFprobe available for validation

---

**Version**: 1.0.0
**Created**: 2025-11-24
**Builder**: builders/04_production_builder.py
