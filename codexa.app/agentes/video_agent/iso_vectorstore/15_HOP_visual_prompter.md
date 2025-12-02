<!-- iso_vectorstore -->
<!--
  Source: 30_visual_prompter_HOP.md
  Agent: video_agent
  Synced: 2025-11-30
  Version: 2.1.0
  Package: iso_vectorstore (export package)
-->

# HOP: Visual Prompter | video_agent Stage 3

## MODULE_METADATA
```yaml
id: video_agent_visual_prompter
version: 2.0.0
purpose: Generate platform-optimized prompts for AI video generation
dependencies: [concept.json, brand_profile (optional)]
category: video_production
stage: 3
knowledge_base: knowledge/platforms/*.md, knowledge/prompt_engineering/*.md
```

## INPUT_CONTRACT
```yaml
required:
  $concept:
    type: object
    source: concept.json
    description: Storyboard from Stage 1
optional:
  $brand_profile:
    type: object
    description: Brand colors, tone, values for alignment
  $platform:
    type: string
    enum: ["veo3", "sora2", "kling", "hailuo", "runway", "pika", "auto"]
    default: "auto"
    description: Target platform (auto selects best for use case)
  $video_mode:
    type: string
    enum: ["overlay", "clean"]
    default: "overlay"
    description: |
      - "overlay": Video will have text overlays (compose shots avoiding text areas)
      - "clean": NO TEXT in video (--NO TEXT mode) - maximize visual impact
  $style_override:
    type: object
    description: Custom style settings (overrides preset)
```

## OUTPUT_CONTRACT
```yaml
primary:
  visual_prompts.json:
    type: object
    structure:
      platform: string
      prompts: array
        - shot_number: integer
          duration: number
          prompt: string
          negative_prompt: string
          camera: CameraConfig
          lighting: LightingConfig
          transition: string
          platform_params: object
secondary:
  prompts_copyable.md:
    type: markdown
    description: Prompts ready to copy/paste into platform UI
```

## KNOWLEDGE_BASE

Before generating prompts, consult:
```
knowledge/
├── platforms/
│   ├── veo3.md         # Google Veo 3 syntax, JSON prompting
│   ├── sora2.md        # OpenAI cinematography, physics
│   ├── kling.md        # Kuaishou movement, parameters
│   ├── hailuo.md       # MiniMax emphasis markers, VFX
│   ├── runway.md       # Camera control, structure
│   └── pika.md         # Features (Pikadditions, etc.)
├── prompt_engineering/
│   ├── anatomy.md      # Universal prompt structure
│   ├── camera_vocabulary.md
│   ├── lighting_vocabulary.md
│   └── magic_words.md  # Quality boosters
└── brand_alignment/
    └── brand_to_video.md  # Translating brand to visual
```

## TASK

**Role**: Expert AI Video Prompt Engineer

**Objective**: Create platform-specific, brand-aligned prompts that generate professional-quality video clips.

**Core Principles**:
1. **Platform-Aware**: Each platform has unique syntax and strengths
2. **Brand-Aligned**: Prompts reflect brand colors, tone, values
3. **Cinematographically Sound**: Proper camera/lighting vocabulary
4. **Consistency**: Visual coherence across all shots
5. **Mode-Aware**: Adapt composition for overlay vs clean mode

## VIDEO MODE CONSIDERATIONS

### Mode: "overlay" (Default)
When text overlays will be added:
- Reserve bottom 20% of frame for text (avoid key subjects there)
- Keep product/subject centered or in upper 2/3
- Allow breathing room for CTA overlay in final shots

### Mode: "clean" (--NO TEXT)
When NO text will be in video:
- Full frame composition - maximize visual impact
- Product can occupy any area of frame
- More cinematic compositions allowed
- Focus on visual storytelling (no text support)
- Include more detail in prompts since narration carries message

```python
def adjust_composition_for_mode(shot, video_mode):
    """
    Adjust prompt composition based on video_mode
    """
    if video_mode == "clean":
        # Full frame - maximize visual impact
        return {
            "composition_note": "full frame composition, cinematic",
            "subject_position": "any",
            "reserve_space": None
        }
    else:
        # Reserve space for text overlays
        return {
            "composition_note": "leave bottom 20% clear for text",
            "subject_position": "center or upper",
            "reserve_space": "bottom"
        }
```

## PLATFORM SELECTION

### Auto-Selection Logic
```python
def select_platform(use_case, requirements):
    """
    Veo 3: Best for dialogue, audio, realism
    Sora 2: Best for cinematography, narrative, physics
    Kling 1.6: Best for cost-efficiency, human animation
    Hailuo: Best for speed, VFX, dynamic movement
    Runway: Best for iteration, camera control
    Pika: Best for effects, transformations
    """
    if requirements.get("dialogue"):
        return "veo3"  # Native audio/dialogue
    elif requirements.get("cinematographic"):
        return "sora2"  # Best cinematography
    elif requirements.get("budget_conscious"):
        return "kling"  # Best value
    elif requirements.get("vfx_heavy"):
        return "hailuo"  # Best VFX
    elif requirements.get("needs_iteration"):
        return "runway"  # Fast iteration
    elif requirements.get("transformations"):
        return "pika"  # Unique features
    else:
        return "runway"  # Default fallback
```

## PROMPT STRUCTURES BY PLATFORM

### Veo 3 (Google)
```
[Camera movement]: [Establishing scene]. [Subject description]. [Action]. [Lighting]. [Style]. [Audio].
```
**Special**: Supports JSON prompting for granular control
**Audio**: `Character says: "[text]" (no subtitles)`

### Sora 2 (OpenAI)
```
LOOK: [visual style, color grade]
CAMERA: [lens, movement, angle]
LIGHTING: [key, fill, mood]
SOUNDSCAPE: [ambient, sfx, music]
ACTION: [subject movement, timing]
```
**Special**: Physics descriptions improve realism

### Kling 1.6 (Kuaishou)
```
[Subject], [subject description], [subject movement], [scene]. [Scene description]. [Camera, lighting, atmosphere].
```
**Special**: `motion blur enabled`, `60fps` for fluidity

### Hailuo/MiniMax
```
[Camera Shot + Motion] + [Subject + Description] + [Action] + [Scene + Description] + [Lighting] + [Style/Mood]
```
**Special**: `((element))` for emphasis/priority

### Runway Gen-3
```
[camera movement]: [establishing scene]. [additional details].
```
**Special**: Camera Control feature, simple structure

### Pika 2.0
```
[Style] + [Subject] + [Action] + [Environment] + [Lighting] + [Camera]
```
**Special**: `--camera [movement]`, Pikadditions/Pikaswaps

## STEPS

### Step 1: Brand Alignment Translation
```python
def translate_brand_to_video(brand_profile):
    """
    Convert brand elements to video language
    Reference: knowledge/brand_alignment/brand_to_video.md
    """
    if not brand_profile:
        return default_style()

    translation = {
        "color_grading": {
            "dominant": color_name(brand_profile["cores"]["primaria"]),
            "shadows": color_name(brand_profile["cores"]["secundaria"]),
            "highlights": color_name(brand_profile["cores"].get("acento", "#ffffff"))
        },
        "lighting_keywords": derive_lighting_from_values(brand_profile["valores"]),
        "camera_style": derive_camera_from_personality(brand_profile["personalidade"]),
        "pacing": derive_pacing_from_tom(brand_profile["tom"]),
        "atmosphere_keywords": derive_atmosphere_from_values(brand_profile["valores"])
    }
    return translation
```

### Step 2: Camera Configuration
```python
def get_camera_for_narrative(narrative_role, brand_style):
    """
    Reference: knowledge/prompt_engineering/camera_vocabulary.md
    """
    base_camera = {
        "hook": {
            "movement": "slow dolly forward",
            "angle": "eye level",
            "effect": "draw viewer in"
        },
        "build": {
            "movement": "tracking shot",
            "angle": "3/4 view",
            "effect": "explore subject"
        },
        "benefit": {
            "movement": "slow orbit",
            "angle": "eye level to low angle",
            "effect": "showcase value"
        },
        "proof": {
            "movement": "static or subtle push",
            "angle": "eye level",
            "effect": "credibility"
        },
        "cta": {
            "movement": "slow zoom in",
            "angle": "centered",
            "effect": "focus attention"
        }
    }

    camera = base_camera.get(narrative_role, base_camera["build"])

    # Apply brand camera style
    if brand_style.get("camera_style"):
        camera["movement"] = f"{brand_style['camera_style']} {camera['movement']}"

    return camera
```

### Step 3: Lighting Configuration
```python
def get_lighting_for_shot(shot, brand_translation, narrative_arc_position):
    """
    Reference: knowledge/prompt_engineering/lighting_vocabulary.md
    """
    # Base lighting from brand
    base_lighting = brand_translation.get("lighting_keywords", "professional studio lighting")

    # Narrative lighting progression (problem → solution)
    if narrative_arc_position < 0.3:  # Early shots
        mood = "transitioning"
    elif narrative_arc_position < 0.7:  # Middle shots
        mood = "building"
    else:  # Final shots
        mood = "resolved, optimistic"

    # Color grading from brand
    color_grade = brand_translation.get("color_grading", {})

    lighting = {
        "setup": base_lighting,
        "color_grade": f"{color_grade.get('dominant', 'neutral')} tones, {color_grade.get('shadows', 'deep')} shadows",
        "mood": mood,
        "rim_light": f"{color_grade.get('highlights', 'white')} rim light"
    }

    return lighting
```

### Step 4: Generate Platform-Specific Prompts
```python
def generate_prompt(shot, platform, camera, lighting, brand_translation):
    """
    Generate prompt optimized for specific platform
    Reference: knowledge/platforms/{platform}.md
    """

    # Base elements
    subject = shot["description"]
    action = shot.get("action", "")
    environment = shot.get("environment", "")

    # Magic words for quality
    # Reference: knowledge/prompt_engineering/magic_words.md
    quality_words = "cinematic 4K quality, shallow depth of field"

    # Platform-specific formatting
    if platform == "veo3":
        prompt = f"{camera['movement']}: {environment}. {subject} {action}. {lighting['setup']}, {lighting['color_grade']}. {quality_words}."
        if shot.get("dialogue"):
            prompt += f" Character says: \"{shot['dialogue']}\" (no subtitles)."

    elif platform == "sora2":
        prompt = f"""LOOK: {quality_words}, {lighting['color_grade']}
CAMERA: {camera['movement']}, {camera['angle']}
LIGHTING: {lighting['setup']}, {lighting['mood']} mood
ACTION: {subject} {action}"""

    elif platform == "kling":
        prompt = f"{subject}, {action}, {environment}. {lighting['setup']}. {camera['movement']}, {camera['angle']}, {quality_words}, motion blur enabled."

    elif platform == "hailuo":
        # Use emphasis markers for key elements
        key_element = shot.get("key_element", subject.split()[0])
        prompt = f"{camera['movement']}: (({key_element})), {subject}, {action}. {environment}. {lighting['setup']}, {lighting['color_grade']}. {quality_words}."

    elif platform == "runway":
        prompt = f"{camera['movement']}: {subject} {action}. {environment}. {lighting['setup']}. {quality_words}."

    elif platform == "pika":
        prompt = f"{quality_words}, {subject}, {action}, {environment}, {lighting['setup']}, {camera['movement']}."

    return prompt
```

### Step 5: Generate Negative Prompts
```python
def generate_negative_prompt(platform, shot_type):
    """
    Platform-appropriate negative prompts
    """
    universal = "blurry, low quality, distorted, artifacts, glitches, watermark"

    if shot_type == "product":
        return f"{universal}, cluttered background, harsh shadows, overexposed"
    elif shot_type == "person":
        return f"{universal}, unnatural movement, distorted face, extra limbs"
    elif shot_type == "abstract":
        return f"{universal}, static, boring composition"
    else:
        return universal
```

### Step 6: Platform Parameters
```python
def get_platform_params(platform, shot):
    """
    Platform-specific technical parameters
    """
    params = {
        "veo3": {
            "duration": min(shot["duration"], 8),
            "resolution": "1080p",
            "audio": True
        },
        "sora2": {
            "duration": min(shot["duration"], 20),
            "resolution": "1080p",
            "style": "cinematic"
        },
        "kling": {
            "duration": 5,
            "aspect_ratio": "9:16",
            "fps": 60,
            "cfg_scale": 0.75
        },
        "hailuo": {
            "duration": 6,
            "resolution": "768p"
        },
        "runway": {
            "duration": min(shot["duration"], 10),
            "model": "gen3_alpha_turbo"
        },
        "pika": {
            "duration": min(shot["duration"], 8)
        }
    }
    return params.get(platform, params["runway"])
```

### Step 7: Compile and Validate
```python
def compile_visual_prompts(concept, platform, brand_profile=None):
    """
    Main compilation function
    """
    brand_translation = translate_brand_to_video(brand_profile)
    prompts = []

    total_shots = len(concept["shots"])

    for i, shot in enumerate(concept["shots"]):
        narrative_position = i / total_shots

        camera = get_camera_for_narrative(shot["narrative"], brand_translation)
        lighting = get_lighting_for_shot(shot, brand_translation, narrative_position)

        prompt = generate_prompt(shot, platform, camera, lighting, brand_translation)
        negative = generate_negative_prompt(platform, shot.get("type", "general"))
        params = get_platform_params(platform, shot)

        prompts.append({
            "shot_number": shot["number"],
            "duration": shot["duration"],
            "prompt": prompt,
            "negative_prompt": negative,
            "camera": camera,
            "lighting": lighting,
            "transition": get_transition(shot["narrative"]),
            "platform_params": params
        })

    # Validate
    for p in prompts:
        assert 20 <= len(p["prompt"]) <= 500, f"Shot {p['shot_number']}: Prompt length invalid"
        assert p["prompt"].isascii(), f"Shot {p['shot_number']}: Non-ASCII characters"

    return {
        "platform": platform,
        "prompts": prompts
    }
```

## OUTPUT EXAMPLE

### visual_prompts.json
```json
{
  "platform": "runway",
  "brand_aligned": true,
  "prompts": [
    {
      "shot_number": 1,
      "duration": 4,
      "prompt": "Slow dolly forward: Modern glass office at golden hour. Confident Brazilian entrepreneur reviews holographic dashboard with rising metrics. Warm golden accent lighting with deep navy shadows, professional cinematography. Cinematic 4K quality, shallow depth of field.",
      "negative_prompt": "blurry, low quality, distorted, artifacts, cluttered background",
      "camera": {
        "movement": "slow dolly forward",
        "angle": "eye level",
        "effect": "draw viewer in"
      },
      "lighting": {
        "setup": "warm golden accent lighting",
        "color_grade": "golden warm tones, deep navy shadows",
        "mood": "optimistic, confident",
        "rim_light": "clean white rim light"
      },
      "transition": "cut",
      "platform_params": {
        "duration": 4,
        "model": "gen3_alpha_turbo"
      }
    }
  ]
}
```

### prompts_copyable.md
```markdown
# Video Prompts - Ready to Copy

**Platform**: Runway Gen-3 Alpha
**Total Shots**: 8
**Brand**: CODEXA

---

## Shot 1 (4s) - Hook
```
Slow dolly forward: Modern glass office at golden hour. Confident Brazilian entrepreneur reviews holographic dashboard with rising metrics. Warm golden accent lighting with deep navy shadows, professional cinematography. Cinematic 4K quality, shallow depth of field.
```

**Negative**: `blurry, low quality, distorted, artifacts, cluttered background`

---

## Shot 2 (5s) - Build
...
```

## VALIDATION

Quality Gates:
- [ ] All prompts in English
- [ ] Prompt length 20-500 chars
- [ ] All shots have prompts
- [ ] Brand colors reflected in lighting/grading
- [ ] Camera vocabulary is platform-appropriate
- [ ] Negative prompts included
- [ ] Platform params set correctly

## PLATFORM COMPARISON

| Feature | Veo3 | Sora2 | Kling | Hailuo | Runway | Pika |
|---------|------|-------|-------|--------|--------|------|
| Max Duration | 8s | 20s | 5s | 6s | 10s | 8s |
| Native Audio | Yes | Yes | No | No | No | No |
| Best For | Dialogue | Cinema | Value | VFX | Iteration | Effects |
| Prompt Style | Structured | Detailed | Simple | Emphasis | Clean | Feature-rich |

## CONTEXT

**Knowledge Dependencies**:
```
knowledge/platforms/*.md       → Platform syntax
knowledge/prompt_engineering/* → Camera, lighting, magic words
knowledge/brand_alignment/*    → Brand translation
```

**Upstream**: concept.json, brand_profile (optional)
**Downstream**: production_builder (API calls)

---

**Version**: 2.1.0
**Created**: 2025-11-24
**Updated**: 2025-11-25
**Builder**: builders/03_visual_builder.py
**Knowledge Base**: 6 platforms, 4 prompt guides, 1 brand system
**Changes in 2.1.0**:
- Added: video_mode parameter ("overlay" vs "clean")
- Added: VIDEO MODE CONSIDERATIONS section
- Added: Composition adjustment for --NO TEXT mode
- Added: Mode-aware principle (#5)
