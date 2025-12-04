<!-- iso_vectorstore -->
<!--
  Source: 10_concept_planner_HOP.md
  Agent: video_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Concept Planner | video_agent Stage 1

## MODULE_METADATA
```yaml
id: video_agent_concept_planner
version: 1.0.0
purpose: Generate storyboard with 6-8 shots and narrative arc
dependencies: [anthropic_api]
category: video_production
stage: 1
```

## INPUT_CONTRACT
```yaml
required:
  $produto:
    type: string
    min_length: 3
    max_length: 200
    description: Product name/description
  $duracao:
    type: integer
    min: 15
    max: 60
    description: Video duration in seconds
  $objetivo:
    type: string
    min_length: 10
    max_length: 500
    description: Main video objective
optional:
  $tom:
    type: string
    default: "energetico"
    description: Video tone (energetico, calmo, dramatico, minimal, cinematico)
  $formato:
    type: string
    enum: ["9:16", "16:9", "1:1"]
    default: "9:16"
    description: Aspect ratio
  $brand_profile:
    type: object
    description: Brand guidelines (colors, tone, logo)
```

## OUTPUT_CONTRACT
```yaml
primary:
  concept.json:
    type: object
    structure:
      shots: array[Shot]
      total_duration: integer
      narrative_arc: string
      style_preset: string
secondary:
  concept_summary.md:
    type: markdown
    description: Human-readable storyboard summary
```

## TASK

**Role**: Storyboard Generator

**Objective**: Create a compelling video storyboard that maximizes engagement through proven narrative structures.

**Standards**:
- ALWAYS start with a "hook" shot (0-3s)
- ALWAYS end with a "cta" (call-to-action) shot
- Use 4-5 second average shot duration
- Match style preset to tone
- Consider platform (vertical for Reels/TikTok)

**Constraints**:
- 3-8 shots maximum
- Total duration must match $duracao +/-15%
- Each shot needs: number, duration, description, composition, narrative role

## STEPS

### Step 1: Parse Input
```python
# Validate required fields
assert len($produto) >= 3, "Product name too short"
assert 15 <= $duracao <= 60, "Duration must be 15-60s"
assert len($objetivo) >= 10, "Objective too short"

# Calculate shot count
shot_count = {
    15: 3,
    30: 6,
    45: 7,
    60: 8
}.get($duracao, max(3, $duracao // 5))
```

### Step 2: Select Style Preset
```python
style_map = {
    "energetico": {
        "camera": "dynamic tracking",
        "lighting": "high contrast",
        "pacing": "fast cuts (2-3s)"
    },
    "calmo": {
        "camera": "slow, smooth",
        "lighting": "soft, warm",
        "pacing": "slow dissolves (4-5s)"
    },
    "dramatico": {
        "camera": "cinematic",
        "lighting": "low-key",
        "pacing": "variable"
    }
}
style = style_map.get($tom, style_map["energetico"])
```

### Step 3: Generate Narrative Arc
```python
# Standard e-commerce narrative structure
narrative = {
    "hook": "0-3s - Attention grabber (problem or intrigue)",
    "build": "3-12s - Product introduction, features",
    "benefit": "12-20s - Key value proposition",
    "proof": "20-25s - Social proof or demonstration",
    "cta": "25-30s - Call to action, price, urgency"
}
```

### Step 4: Generate Shots
```python
shots = []
cumulative_time = 0

for i in range(shot_count):
    # Determine narrative role based on position
    if i == 0:
        role = "hook"
        duration = 3
    elif i == shot_count - 1:
        role = "cta"
        duration = 4
    elif i <= shot_count // 3:
        role = "build"
        duration = 4
    elif i <= 2 * shot_count // 3:
        role = "benefit"
        duration = 5
    else:
        role = "proof"
        duration = 4

    shot = {
        "number": i + 1,
        "duration": duration,
        "description": generate_description($produto, role, style),
        "composition": get_composition(role, style),
        "narrative": role
    }
    shots.append(shot)
    cumulative_time += duration
```

### Step 5: Validate and Adjust
```python
# Ensure total duration matches
total = sum(s["duration"] for s in shots)
target = $duracao
tolerance = target * 0.15

if abs(total - target) > tolerance:
    # Adjust middle shots
    diff = target - total
    adjustment = diff // (shot_count - 2)
    for shot in shots[1:-1]:
        shot["duration"] += adjustment
```

### Step 6: Output
```json
{
  "shots": [
    {
      "number": 1,
      "duration": 3,
      "description": "Close-up do $produto com movimento 360 graus, fundo branco clean",
      "composition": "Product shot, eye-level, white background, soft lighting",
      "narrative": "hook"
    },
    {
      "number": 2,
      "duration": 4,
      "description": "Detalhe do material e textura, câmera em macro",
      "composition": "Macro detail shot, revealing texture and quality",
      "narrative": "build"
    }
  ],
  "total_duration": 30,
  "narrative_arc": "Hook -> Build -> Benefit -> Proof -> CTA",
  "style_preset": "energetico"
}
```

## VALIDATION

Quality Gates:
- [ ] 3-8 shots generated
- [ ] First shot is "hook"
- [ ] Last shot is "cta"
- [ ] Total duration = $duracao +/-15%
- [ ] All shots have: number, duration, description, composition, narrative
- [ ] Style matches $tom preset

Thresholds:
- Minimum shots: 3
- Maximum shots: 8
- Duration tolerance: 15%

## CONTEXT

**Usage**: Called by video_agent.py as first pipeline stage

**Upstream**: User brief (direct input)

**Downstream**:
- $shots -> 02_script_builder.py (narration timing)
- $shots -> 03_visual_builder.py (Runway prompts)

**$arguments chaining**:
```
concept.json.shots -> script_builder($shots)
concept.json.style_preset -> visual_builder($style)
```

**Assumptions**:
- User provides valid product information
- Tone exists in style_map (fallback to energetico)
- Platform is social media (vertical-first thinking)

---

**Version**: 1.0.0
**Created**: 2025-11-24
**Builder**: builders/01_concept_builder.py
