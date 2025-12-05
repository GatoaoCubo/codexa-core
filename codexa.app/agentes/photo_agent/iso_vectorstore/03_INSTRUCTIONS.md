<!--
ISO_VECTORSTORE EXPORT
Source: photo_agent/INSTRUCTIONS.md
Synced: 2025-12-05
Version: 2.6.0
-->

# INSTRUCTIONS: photo_agent Operations

**Version**: 2.6.0
**Audience**: AI Assistants operating photo_agent
**Purpose**: Step-by-step operational guidance for v3.2.0 dual-input workflow

---

## Overview

This document provides operational instructions for AI assistants using `photo_agent` to generate professional photography prompts. Follow these workflows systematically to ensure quality output.

**Key Change in v3.2.0**: All prompts now use `{user_image} {seed:[RANDOM]}` prefix for dual-input workflow, ensuring maximum product fidelity while enabling controlled variations through seeds and `[OPEN_VARIABLES]`.

---

## Workflow 1: Standard 9-Scene Generation

### Input Requirements
- **Required**: Subject description (string, non-empty)
- **Optional**: Style preset, brand profile, PNL triggers, technical overrides

### Steps

**Step 1: Validate Input**
```
1. Check subject description is non-empty
2. Verify style preset is valid enum (or default to "editorial")
3. Validate scenes count is 1-9 (default 9)
4. Parse brand_profile if provided (colors, mood, target_audience)
5. Validate technical_overrides (no impossible combinations like f/1.2 + full focus)
```

**Step 2: Load Configuration**
```
1. Read config/photography_styles.json for style preset
2. Read config/camera_profiles.json for camera defaults
3. Read config/pnl_triggers.json for emotional anchors
4. Merge user overrides with defaults
```

**Step 3: Generate Scene Specifications**
```
For each scene (1-9):
  1. Determine scene role (hero, lifestyle, macro, detail, etc.)
  2. Select camera profile (focal length, aperture, shutter, ISO)
  3. Select lighting setup (high-key, low-key, 3-point, natural)
  4. Define composition rule (rule of thirds, golden ratio, centered)
  5. Choose background (white #FFFFFF, context, bokeh)
  6. Select PNL trigger (match scene emotion)
  7. Apply brand profile (if provided): color grading, mood alignment
```

**Step 4: Assemble Prompts (v3.2.0 Format)**
```
PROMPT 1: Grid 3x3 Master (single image with all 9 scenes)
  1. Start with dual-input prefix:
     "{user_image} {seed:[RANDOM]} Professional photography grid..."

  2. Add 9-scene composition:
     "3x3 grid showing [SUBJECT] in 9 different scenes..."

  3. Add technical specs for master shot:
     "camera: 50mm f/8, uniform lighting across grid..."

  4. Add [OPEN_VARIABLES] for controlled randomization
  5. Add compliance + generation commands

PROMPT 2: Individual Prompts (9 separate images)
  For each scene (1-9):
  1. Start with dual-input prefix:
     "{user_image} {seed:[RANDOM]} Professional [STYLE] photography..."

  2. Add scene-specific technical specs:
     "camera: [FOCAL] [APERTURE], lighting: [TYPE]..."

  3. Add composition & background:
     "background: [SPEC], composition: [RULE]..."

  4. Add PNL trigger:
     "[EMOTIONAL_ANCHOR] [OPTIONS]..."

  5. Add [OPEN_VARIABLES] placeholders
  6. Add compliance instructions
  7. Add generation commands at end
```

**Step 5: Validate Each Prompt (v3.2.0 - 13 Points)**
```
For each prompt, check 13-point validation:
  TECHNICAL (7 points):
  1. {user_image} {seed:[RANDOM]} prefix ✓
  2. [OPEN_VARIABLES] present ✓
  3. Camera specs realistic ✓
  4. Lighting physics correct ✓
  5. Word count: P1 500-800, P2 180-300 each ✓
  6. No impossible setups ✓
  7. Generation commands present ✓

  CONTENT (6 points):
  8. Scene 1 white #FFFFFF ✓
  9. Scene 9 white #FFFFFF (CRITICAL) ✓
  10. PNL triggers with [OPTIONS] ✓
  11. Brand colors (if provided) ✓
  12. No text/logos ✓
  13. Copy-paste ready ✓

Calculate validation score: (passed checks / 13)
Threshold: ≥0.85 (general) | ≥0.90 (marketplace)
If score < threshold: Auto-correct and retry once
If still below: Escalate to human review
```

**Step 6: Format Output (v3.2.0)**
```
Generate output with 2 prompts:

1. PROMPT 1: Grid 3x3 master
   - Single copyable block with {user_image} {seed:[RANDOM]} prefix
   - 500-800 words describing 9-scene grid
   - [OPEN_VARIABLES] for controlled randomization
   - Generation commands inline

2. PROMPT 2: 9 individual prompts
   - Each prompt 180-300 words
   - Each starts with {user_image} {seed:[RANDOM]}
   - Scenes 1+9 = white background #FFFFFF
   - [OPEN_VARIABLES] in each
   - Auto-PNG generation commands at end

3. Quality Report:
   - 13-point validation summary
   - Compliance status
   - Warnings/errors
```

**Step 7: Quality Assurance (v3.2.0)**
```
Final checks:
  - PROMPT 1 (Grid 3x3) generated ✓
  - PROMPT 2 (9 individual) generated ✓
  - All start with {user_image} {seed:[RANDOM]} ✓
  - [OPEN_VARIABLES] present in all ✓
  - Scenes 1+9 = white background ✓
  - Validation score ≥0.85 ✓
  - Generation commands included ✓
  - Copy-paste ready (no preprocessing needed) ✓
```

---

## Workflow 2: Brand-Aligned Generation

### When to Use
- Brand archetype is known (Hero, Caregiver, Explorer, Sage, etc.)
- Subject requires emotional consistency across brand identity
- PNL triggers must align with brand personality

### Steps

**Step 1: Identify Brand Archetype**
```
Parse brand_profile.archetype field or infer from brand description:
  - Hero: Courage, transformation, achievement
  - Caregiver: Nurturing, safety, comfort
  - Explorer: Freedom, discovery, adventure
  - Sage: Knowledge, wisdom, truth
  - Innocent: Simplicity, purity, optimism
  - Magician: Innovation, transformation, wonder
  - Ruler: Control, leadership, power
  - Creator: Imagination, creativity, expression
  - Jester: Joy, fun, entertainment
  - Everyman: Belonging, authenticity, community
  - Lover: Intimacy, passion, beauty
  - Rebel: Disruption, revolution, change
```

**Step 2: Load PNL Trigger Mapping**
```
Read config/pnl_triggers.json → brand_archetype_mapping
Match archetype to priority triggers:

Examples:
  - Hero → ["urgência", "transformação", "controle"]
  - Caregiver → ["conforto", "calma", "segurança"]
  - Lover → ["desejo", "prazer", "conforto"]
```

**Step 3: Override Default Scene Triggers**
```
For each scene (1-9):
  1. Check default scene trigger in scene_mapping_default
  2. If archetype triggers are specified:
     - Replace with archetype-aligned trigger
     - Maintain scene purpose (hero shot stays hero shot)
     - Prioritize archetype emotional consistency

Example:
  - Default Scene 2: "conforto" (lifestyle)
  - Hero Brand: Override to "transformação"
  - Result: Lifestyle scene showing transformation moment
```

**Step 4: Apply Brand Colors to Color Grading**
```
For scenes 2, 5, 7 (color grading opportunities):
  1. Parse brand_profile.colors (hex codes)
  2. Apply to lighting temperature and background tints
  3. Maintain technical fidelity (no color shift to product)

Example:
  - Brand colors: ["#8B7355", "#F5F5DC"]
  - Scene 5: "warm color grading with subtle #8B7355 tint in shadows"
```

**Step 5: Align Mood/Style to Archetype Personality**
```
Adjust photography style based on archetype:
  - Hero → dramatic, dynamic compositions
  - Caregiver → soft lighting, warm tones
  - Sage → clean, minimal, neutral
  - Rebel → bold, high-contrast, asymmetric
  - Lover → soft focus, warm, intimate

Maintain chosen photography style preset but adjust mood direction.
```

**Step 6: Validate Emotional Consistency**
```
Quality check:
  - All scenes use archetype-aligned triggers ✓
  - Brand colors integrated where appropriate ✓
  - Mood aligns with archetype personality ✓
  - Technical quality maintained ✓
```

---

## Workflow 3: Marketplace-Compliant Generation

### When to Use
- Subject is for Mercado Livre, Shopee, or Amazon BR listings
- Marketplace compliance is mandatory
- Product fidelity is critical (exact color, texture, form)

### Compliance Requirements

**MANDATORY for Mercado Livre / Shopee / Amazon BR:**
```
1. Scene 1: Pure white background (#FFFFFF)
2. Scene 9: Pure white background (#FFFFFF)
3. Resolution: Minimum 2000x2000px (recommended 2400x2400px)
4. Format: JPG or PNG
5. Fidelity weight: 5 (product MUST look identical across all scenes)
6. No text overlays
7. No watermarks
8. No third-party logos
```

### Steps

**Step 1: Load Marketplace Defaults**
```
Read config/photography_styles.json → commercial → marketplace_compliance_defaults

For Mercado Livre:
  - min_resolution: "2000x2000px"
  - recommended_resolution: "2400x2400px"
  - background_scenes_1_9: "#FFFFFF"
  - fidelity_weight: 5

For Shopee:
  - min_resolution: "1800x1800px"
  - aspect_ratios: ["1:1", "3:4"]
  - background_preference: "#FFFFFF"
  - fidelity_weight: 5
```

**Step 2: Override Style Preset**
```
Force style to "commercial" regardless of user input
Apply marketplace-specific overrides:
  1. Scene 1 background: "#FFFFFF"
  2. Scene 9 background: "#FFFFFF"
  3. Lighting: high-key, minimal shadows
  4. Composition: centered, product dominant
```

**Step 3: Apply Fidelity Weight**
```
For all scenes:
  - Fidelity weight: 5 (maximum)
  - Color accuracy: critical (no creative grading on product)
  - Texture accuracy: critical (show exact material)
  - Form accuracy: critical (no perspective distortion)

Add to each prompt:
  "product fidelity weight 5, exact color matching, accurate texture reproduction, no creative interpretation of product appearance"
```

**Step 4: Validate Compliance Checklist**
```
Pre-generation validation:
  [ ] Scene 1 has white background (#FFFFFF)
  [ ] Scene 9 has white background (#FFFFFF)
  [ ] Resolution ≥ 2000x2000px specified
  [ ] Fidelity weight = 5 in all prompts
  [ ] No text overlay instructions
  [ ] No watermark instructions
  [ ] No third-party logo instructions
  [ ] Product appearance consistent across all scenes

If any check fails: Auto-correct and retry
If still fails: Escalate to human review
```

**Step 5: Post-Generation Verification**
```
After prompt generation:
  1. Verify all 9 prompts contain compliance keywords
  2. Check Scene 1 and Scene 9 explicitly state "#FFFFFF background"
  3. Confirm no creative color grading on product (only on background/context)
  4. Validate resolution specification present

Generate compliance report in .meta.json:
  {
    "marketplace_compliant": true,
    "marketplace": "mercadolivre",
    "compliance_checks_passed": 8,
    "compliance_checks_total": 8
  }
```

**Step 6: Quality Assurance**
```
Final marketplace-specific checks:
  - All compliance rules enforced ✓
  - Fidelity weight 5 confirmed ✓
  - White backgrounds on scenes 1 & 9 ✓
  - No prohibited elements (text/watermarks/logos) ✓
  - Resolution meets marketplace minimum ✓
  - Trinity output complete (.md + .llm.json + .meta.json) ✓
```

---

## Workflow 4: Custom Style with Brand Profile

### When to Use
- User provides explicit brand visual identity
- Subject requires brand consistency across scenes
- Target audience is brand-specific demographic

### Steps

**Step 1: Parse Brand Profile**
```json
{
  "colors": ["#HEX1", "#HEX2", "#HEX3"],     // Brand color palette
  "mood": "luxury minimal zen playful",      // Brand tone/mood
  "target_audience": "urban millennials 25-35" // Demographics
}
```

**Step 2: Apply Brand Constraints**
```
For each scene:
  1. Color Grading: Integrate brand colors into lighting/background
     - Example: "warm color grading matching brand palette #F5F5DC #8B7355"

  2. Mood Alignment: Adjust lighting temperature and composition
     - "luxury" → controlled studio, neutral grading, f/5.6 sharp
     - "playful" → bright colorful, dynamic angles, f/4 lifestyle
     - "minimal" → clean white, soft even light, f/8 full focus
     - "zen" → muted tones, natural light, calm composition

  3. Audience Context: Reflect in lifestyle scenes (2-8)
     - "urban millennials" → modern apartment, neutral props, contemporary aesthetic
     - "families" → warm home environment, safety emphasis, approachable
     - "luxury consumers" → premium materials, controlled studio, editorial polish
```

**Step 3: Validate Brand Compliance**
```
Additional checks:
  - Brand colors mentioned in color grading (if provided)
  - Mood/tone consistent across all scenes
  - Lifestyle scenes match target audience context
  - No conflicting visual elements (e.g., playful + dramatic low-key)
```

---

## Workflow 3: Technical Override Handling

### When to Use
- User has specific camera/lighting requirements
- Professional photographer wants manual control
- Replicating existing photography style

### Override Parameters
```json
{
  "technical_overrides": {
    "focal_length": "85mm",      // Override camera default
    "aperture": "f/4",           // Override aperture
    "lighting": "Rembrandt"      // Override lighting setup
  }
}
```

### Validation Rules
```
1. Focal Length: Must be valid (24mm, 35mm, 50mm, 85mm, 100mm, 135mm, 200mm)
2. Aperture: Must be realistic (f/1.2 to f/16)
3. Lighting: Must be known setup (high-key, low-key, 3-point, Rembrandt, Butterfly, Loop, natural)

Conflict Detection:
  - f/1.2-f/2.8 + "full focus" → INVALID (shallow DOF incompatible)
  - f/8-f/16 + "bokeh" → INVALID (deep DOF incompatible)
  - "high-key" + "dramatic shadows" → INVALID (contradictory)
  - "low-key" + "white background" → INVALID (contradictory)
```

### Override Application
```
Apply overrides to ALL scenes unless scene-specific logic conflicts:

Scene 1 (Hero White):
  - Aperture override OK (if ≥f/5.6 for sufficient focus)
  - Lighting override must be compatible with white background (high-key, 3-point)

Scene 3 (Macro Detail):
  - Focal length override must be ≥85mm for macro capability
  - Aperture override OK (wide apertures encouraged for bokeh)

Scene 6 (Top-down):
  - Focal length override should be ≤85mm (avoid perspective distortion)
  - Aperture override must provide sufficient DOF (≥f/5.6)
```

---

## Workflow 4: PNL Trigger Integration

### Purpose
Embed psychological anchors to influence viewer perception and emotional response.

### PNL Trigger Library (10 Core)
```
confiança     → "acabamento que inspira confiança durável"
conforto      → "toque seguro, superfície que convida"
clareza       → "visão total — nada escondido, decisão fácil"
calma         → "ambiente sereno, temperatura ideal"
desejo        → "brilho na medida, qualidade visível"
urgência      → "momento certo, escolha agora"
pertencimento → "encaixa na sua rotina sem atrito"
transformação → "antes cansado, agora descansado"
segurança     → "sempre pronto, zero preocupação"
prazer        → "satisfação imediata, resultado que se vê"
```

### Scene-to-Trigger Mapping (Default)
```
Scene 1 (Hero White)        → clareza (clear decision-making)
Scene 2 (Lifestyle Use)     → conforto (comfort in use)
Scene 3 (Macro Detail)      → confiança (trust in quality)
Scene 4 (User Routine)      → pertencimento (fits routine)
Scene 5 (Benefit Moment)    → prazer (immediate satisfaction)
Scene 6 (Top-down Functional) → segurança (always ready)
Scene 7 (Life Context)      → pertencimento (routine integration)
Scene 8 (Material Quality)  → confiança (trusted finish)
Scene 9 (Commercial Hero)   → clareza (simple reliable)
```

### Custom Trigger Assignment
```
User provides: "pnl_triggers": ["desejo", "urgência", "transformação"]

Algorithm:
  1. Distribute user triggers across scenes 2-8 (lifestyle/emotional scenes)
  2. Repeat triggers if fewer than 7 provided
  3. Always use "clareza" for scenes 1 & 9 (hero shots need clarity)

Example distribution:
  Scene 1 → clareza (default)
  Scene 2 → desejo
  Scene 3 → urgência
  Scene 4 → transformação
  Scene 5 → desejo (repeat)
  Scene 6 → urgência (repeat)
  Scene 7 → transformação (repeat)
  Scene 8 → desejo (repeat)
  Scene 9 → clareza (default)
```

### Trigger Embedding
```
Format: "PNL: '[EMOTIONAL_ANCHOR]'"

Example in full prompt:
"...natural diffused lighting, camera 85mm f/4, PNL: 'surface that invites touch', no watermarks..."
```

---

## Workflow 5: Multi-Scene Narrative Arc

### Story Structure (9 Scenes)
```
ACT 1: ESTABLISH (Scenes 1-3)
  Scene 1: Hero White Background → Introduce subject clearly
  Scene 2: Lifestyle Use → Show subject in ideal use
  Scene 3: Macro Detail → Prove quality/craftsmanship

ACT 2: DEMONSTRATE (Scenes 4-6)
  Scene 4: User Routine → Ease of use/integration
  Scene 5: Benefit Moment → Emotional transformation
  Scene 6: Top-down Functional → Practical functionality

ACT 3: CONVERT (Scenes 7-9)
  Scene 7: Life Context → Versatility in real world
  Scene 8: Material Quality → Perceived value
  Scene 9: Commercial Hero → Final call to action
```

### Narrative Coherence Rules
```
1. Consistent Lighting Temperature:
   - Scenes 1, 9: Neutral 5000-5400K (studio)
   - Scenes 2-8: Match style preset (warm lifestyle, cool editorial, dramatic varied)

2. Progressive Detail Zoom:
   - Scenes 1, 9: Full subject (80-90% frame)
   - Scenes 2, 4, 5, 6, 7: Medium shots (subject 30-70% frame)
   - Scenes 3, 8: Close-ups/macro (extreme detail focus)

3. Visual Variety:
   - No two consecutive scenes with identical angle
   - Alternate between subject hero (1, 9) and context hero (2-8)
   - Mix shallow DOF (3, 5) with deep DOF (1, 6, 9)

4. Emotional Arc:
   - Scenes 1-3: Cognitive (clarity, information)
   - Scenes 4-6: Emotional (comfort, belonging, relief)
   - Scenes 7-9: Confidence (trust, value, decision)
```

---

## Workflow 6: Intentional Gaps Strategy

### Philosophy
Leave secondary elements unspecified to allow AI model creativity while maintaining technical control.

### What to SPECIFY (Always)
```
✓ Main camera settings (focal length, aperture)
✓ Primary lighting type (high-key, low-key, natural)
✓ Background category (white, context, bokeh)
✓ Composition primary rule (rule of thirds, centered, golden ratio)
✓ Subject description and state
✓ Emotional tone (PNL trigger)
```

### What to LEAVE UNSPECIFIED (Intentional Gaps)
```
✗ Exact secondary light position (just mention "fill light" not "fill at 32° from right at 500 lumens")
✗ Minor prop details (say "neutral props" not "beige ceramic vase + gray linen napkin")
✗ Small angle variations (say "45° lateral" not "exactly 44.3° lateral")
✗ Background texture specifics (say "textured background" not "oak wood grain vertical pattern")
✗ Precise color hex codes for non-brand elements (say "warm neutral tones" not "#F5F5DC exact")
```

### Why This Works
```
1. Prevents over-tokenization (prompts stay under 350 chars)
2. Allows AI model to exercise learned photographic knowledge
3. Creates natural variation across generations (less robotic)
4. Focuses control on critical elements (camera, main light, composition)
5. Faster generation (less processing for model)
```

### Example Comparison
```
❌ OVERSPECIFIED (TOO DETAILED):
"Professional photography, ceramic mug, 50mm f/8 1/160s ISO 100, key light softbox 1000 lumens 45° from left, fill light 500 lumens 32° from right at -1.5EV, rim light 200 lumens 180° back, white background #FFFFFF exactly, centered on 9-grid with subject at intersection of middle thirds, beige ceramic vase 8cm tall as prop at 120° position 15cm from subject..."

✅ PROPERLY SPECIFIED (INTENTIONAL GAPS):
"Professional minimalist photography, ceramic mug, camera 50mm f/8, 3-point lighting (key softbox, fill -1.5EV, rim subtle), white background, centered composition rule of thirds, neutral props, 8K"
```

---

## Workflow 7: Validation & Auto-Correction

### 11-Point Validation Checklist

**Implementation**:
```python
def validate_prompt(prompt: str, scene_specs: dict) -> dict:
    score = 0
    errors = []

    # 1. Length check
    if 80 <= len(prompt) <= 350:
        score += 1
    else:
        errors.append(f"Length {len(prompt)} outside 80-350 range")

    # 2. Camera specified
    if re.search(r'\d{2,3}mm', prompt) and re.search(r'f/\d+\.?\d*', prompt):
        score += 1
    else:
        errors.append("Camera specs missing (focal + aperture)")

    # 3. Lighting described
    if any(term in prompt.lower() for term in ['lighting', 'light', 'lit']):
        score += 1
    else:
        errors.append("Lighting not described")

    # 4. Background mentioned
    if any(term in prompt.lower() for term in ['background', 'backdrop', '#ffffff']):
        score += 1
    else:
        errors.append("Background not mentioned")

    # 5. Composition defined
    if any(term in prompt.lower() for term in ['composition', 'centered', 'rule of thirds', 'golden ratio']):
        score += 1
    else:
        errors.append("Composition not defined")

    # 6. Resolution stated
    if '8K' in prompt or '8k' in prompt:
        score += 1
    else:
        errors.append("Resolution not stated")

    # 7-9. Compliance instructions
    if 'no watermark' in prompt.lower():
        score += 1
    else:
        errors.append("Missing 'no watermarks'")

    if 'no text' in prompt.lower():
        score += 1
    else:
        errors.append("Missing 'no text'")

    if 'no third-party logo' in prompt.lower() or 'brand/style lock' in prompt.lower():
        score += 1
    else:
        errors.append("Missing brand/logo compliance")

    # 10. PNL trigger
    if 'PNL:' in prompt or any(trigger in prompt for trigger in PNL_TRIGGERS):
        score += 1
    else:
        errors.append("PNL trigger missing")

    # 11. No impossible instructions
    impossible_patterns = [
        r'show (front and back|all sides) simultaneously',
        r'add text',
        r'include logo',
        r'(f/1\.\d.*full focus|f/8.*bokeh)',  # Impossible DOF
    ]
    if not any(re.search(pattern, prompt, re.IGNORECASE) for pattern in impossible_patterns):
        score += 1
    else:
        errors.append("Contains impossible instructions")

    validation_score = score / 11

    return {
        'score': validation_score,
        'passed': score,
        'failed': 11 - score,
        'errors': errors,
        'status': 'PASS' if validation_score >= 0.85 else 'FAIL'
    }
```

### Auto-Correction Logic

**When**: Validation score < 0.85

**How**:
```
1. Identify failed checks from errors list
2. Apply targeted corrections:

   Missing camera → Add "camera 50mm f/8"
   Missing lighting → Add "high-key lighting"
   Missing background → Add "white background"
   Missing composition → Add "centered composition"
   Missing resolution → Append ", 8K"
   Missing compliance → Append ", no watermarks, no text, brand/style lock"
   Missing PNL → Insert "PNL: '[default_trigger]'"

3. Re-validate corrected prompt
4. If still < 0.85 → Escalate to human review
5. If ≥ 0.85 → Accept with warning note
```

### Quality Report Generation
```markdown
## Quality Report

**Validation Summary**:
- Total Prompts: 9
- Passed (≥0.85): 9/9 (100%)
- Average Score: 0.94
- Status: ✅ PASS

**Compliance Checks**:
- ✅ All prompts 80-350 characters
- ✅ All prompts contain camera specs
- ✅ All prompts contain lighting description
- ✅ All prompts contain background spec
- ✅ All prompts contain composition rule
- ✅ All prompts state 8K resolution
- ✅ All prompts include "no watermarks"
- ✅ All prompts include "no text"
- ✅ All prompts include brand/logo compliance
- ✅ All prompts include PNL triggers
- ✅ No impossible instructions detected

**Warnings**: None
**Errors**: None
```

---

## Error Handling Protocols

### Error Level 1: Invalid Input (Block Execution)
```
Error: Subject description empty or missing
Action: Return error message, do not generate prompts
Message: "❌ ERROR: Subject description required. Please provide a description of what to photograph."

Error: Invalid style preset
Action: Default to "editorial" with warning
Message: "⚠️ WARNING: Style 'xyz' not recognized. Defaulting to 'editorial'. Valid styles: minimalist, dramatic, lifestyle, editorial, commercial."

Error: Impossible technical overrides
Action: Return error message with explanation
Message: "❌ ERROR: Aperture f/1.4 incompatible with 'full focus' requirement. Choose shallow DOF (f/1.4-f/2.8) OR full focus (f/8-f/16)."
```

### Error Level 2: Validation Failures (Auto-Correct)
```
Error: Prompt validation score < 0.85
Action: Auto-correct missing elements, retry validation once
Message: "⚠️ WARNING: Scene X score 0.73. Auto-correcting... ✅ Corrected score 0.91 PASS"

Error: Prompt length > 350 characters
Action: Compress by removing redundant descriptors
Message: "⚠️ WARNING: Scene X length 367 chars. Compressing... ✅ Reduced to 328 chars PASS"
```

### Error Level 3: Quality Warnings (Proceed with Note)
```
Warning: Unusual subject type (abstract concept)
Action: Proceed with generic visual metaphor approach
Message: "ℹ️ NOTE: Abstract subject detected. Using visual metaphor strategy for tangible representation."

Warning: Brand profile conflicts with style preset
Action: Prioritize brand profile over preset
Message: "ℹ️ NOTE: Brand mood 'playful' conflicts with style 'dramatic'. Adjusting to match brand profile."

Warning: Scenes count < 3
Action: Proceed but note narrative arc limitation
Message: "ℹ️ NOTE: Only 2 scenes requested. Story arc will be limited (establish + convert only)."
```

---

## Performance Optimization

### Target Benchmarks
- Input parsing: <1s
- Config loading: <1s
- Scene spec generation: <5s (9 scenes)
- Prompt assembly: <3s (9 prompts)
- Validation: <2s (9 prompts)
- Output formatting: <3s
- **Total: <15s**

### Optimization Techniques
```
1. Cache loaded configurations (photography_styles.json, camera_profiles.json, pnl_triggers.json)
2. Parallel prompt assembly (scenes are independent)
3. Batch validation (validate all 9 prompts in single pass)
4. Pre-compiled regex patterns for validation
5. Reuse template strings (avoid repeated string concatenation)
```

### Caching Strategy
```python
# Load once at agent initialization
CACHED_STYLES = load_json('config/photography_styles.json')
CACHED_CAMERAS = load_json('config/camera_profiles.json')
CACHED_PNL = load_json('config/pnl_triggers.json')

# Reuse across generations
def generate_prompts(input):
    style = CACHED_STYLES[input.style]  # O(1) lookup
    camera = CACHED_CAMERAS[style.default_camera]  # O(1) lookup
    # ... rest of logic
```

---

## Output Formatting Standards

### Markdown Output (.md)
```markdown
# Photo Prompts: [Subject Name]

## Metadata
- **Subject**: [subject]
- **Style**: [style_preset]
- **Total Prompts**: 9
- **Validation Status**: PASS (9/9)
- **Average Score**: 0.92
- **Generated**: 2025-11-14T15:30:00Z

---

## Scene 1: Hero White Background
**File**: subject_scene_01_hero_white.png
**Camera**: 50mm f/8 1/160s ISO 100
**Lighting**: High-key clean, soft uniform shadows
**Background**: #FFFFFF pure white
**Composition**: Centered, rule of thirds
**PNL**: "clareza imediata, decisão simples"

**Prompt**:
```
[Full prompt text here]
```

**Validation**: ✅ PASS (Score: 0.95, 142 chars)

---

[... scenes 2-9 ...]

---

## Quality Report
[Validation summary, compliance checks, warnings, errors]
```

### LLM JSON Output (.llm.json)
```json
{
  "prompts": [
    {
      "scene_number": 1,
      "scene_name": "Hero White Background",
      "file_name": "subject_scene_01_hero_white.png",
      "prompt": "Full prompt text",
      "technical_specs": {
        "camera": "50mm f/8 1/160s ISO 100",
        "lighting": "High-key clean, soft uniform shadows",
        "background": "#FFFFFF",
        "composition": "Centered, rule of thirds"
      },
      "pnl_trigger": "clareza imediata, decisão simples",
      "validation_score": 0.95,
      "character_count": 142
    }
  ]
}
```

### Meta JSON Output (.meta.json)
```json
{
  "metadata": {
    "agent": "photo_agent",
    "version": "1.0.0",
    "timestamp": "2025-11-14T15:30:00Z",
    "input_hash": "a3b2c1d4e5f6..."
  },
  "quality_report": {
    "total_prompts": 9,
    "validation_passed": 9,
    "validation_failed": 0,
    "avg_score": 0.92,
    "avg_length": 156,
    "compliance_status": "PASS",
    "warnings": [],
    "errors": []
  }
}
```

---

**Version**: 2.6.0
**Last Updated**: 2025-12-05
**Maintained by**: CODEXA Meta-Construction Framework

**Changelog v2.6.0**:
- Updated to v3.2.0 dual-input workflow (`{user_image}` + seeds)
- 13-point validation (was 11-point)
- 2 prompt output format (Grid + Individual)
- [OPEN_VARIABLES] support
- Task boundaries integration
- Execution modes (full/quick/single)
