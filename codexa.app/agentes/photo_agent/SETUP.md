# SETUP: photo_agent Configuration Guide

**Version**: 1.0.0
**Audience**: Users and AI Assistants
**Purpose**: Configuration and customization instructions

---

## Quick Start Setup

### Minimal Configuration (Default Settings)

```json
{
  "subject": "Your subject description here"
}
```

That's it! The agent will use intelligent defaults:
- Style: Editorial
- Scenes: 9 (full narrative arc)
- Output: Grid 3x3
- AI Model: Midjourney
- Camera/Lighting: Automatic based on style

### Recommended Configuration

```json
{
  "subject": "Luxury leather handbag with gold hardware",
  "style": "editorial",
  "scenes": 9,
  "ai_model": "midjourney",
  "output_format": "grid_3x3"
}
```

---

## Configuration Parameters

### 1. Subject (Required)

**Type**: String
**Required**: Yes
**Description**: Main subject to photograph (product, person, scene, concept)

**Examples**:
```json
"subject": "Ceramic coffee mug with matte white glaze"
"subject": "Male model wearing black leather jacket"
"subject": "Minimalist home office desk setup"
"subject": "Abstract concept of digital transformation"
```

**Guidelines**:
- Be specific about key visual features
- Include materials if relevant (leather, ceramic, wood, fabric)
- Mention distinctive characteristics (matte, glossy, textured)
- Avoid subjective adjectives (beautiful, stunning, amazing)

---

### 2. Style (Optional)

**Type**: Enum
**Default**: `editorial`
**Options**: `minimalist | dramatic | lifestyle | editorial | commercial`

**Preset Details**:

#### Minimalist
```json
"style": "minimalist"
```
- **Background**: White, light gray, soft pastels
- **Lighting**: Soft even, no harsh shadows
- **Composition**: Centered, rule of thirds, negative space
- **Color**: Muted, desaturated, monochromatic
- **Best for**: Skincare, home decor, stationery, minimal tech

#### Dramatic
```json
"style": "dramatic"
```
- **Background**: Dark, textured, atmospheric
- **Lighting**: Low-key, strong shadows, high contrast
- **Composition**: Diagonal, asymmetric, bold
- **Color**: Rich saturated, cinematic grading
- **Best for**: Luxury goods, automotive, fashion, spirits

#### Lifestyle
```json
"style": "lifestyle"
```
- **Background**: Real-world contexts (homes, cafes, outdoors)
- **Lighting**: Natural light, golden hour, window light
- **Composition**: Candid, authentic moments
- **Color**: Warm tones (2800-4000K)
- **Best for**: Consumer products, food, wellness, apparel

#### Editorial
```json
"style": "editorial"
```
- **Background**: Studio or controlled environments
- **Lighting**: Precision 3-point lighting
- **Composition**: Magazine-quality balanced
- **Color**: Neutral, accurate representation
- **Best for**: Fashion editorials, beauty, professional gear

#### Commercial
```json
"style": "commercial"
```
- **Background**: White (#FFFFFF) or brand colors
- **Lighting**: High-key bright, optimistic
- **Composition**: Product hero 80-90% frame
- **Color**: Brand palette integration
- **Best for**: E-commerce, marketplace listings, ads

---

### 3. Scenes (Optional)

**Type**: Integer
**Range**: 1-9
**Default**: 9
**Description**: Number of scenes to generate

**Scene Count Guide**:
```
1 scene  → Single hero shot (no narrative)
3 scenes → Essential 3-act (establish, demonstrate, convert)
5 scenes → Expanded story (establish, use, detail, quality, convert)
9 scenes → Full narrative arc (complete emotional journey)
```

**Recommended by Use Case**:
- **E-commerce listing**: 9 scenes (full story, grid 3x3)
- **Social media post**: 1 scene (single hero)
- **Instagram carousel**: 5 scenes (swipeable story)
- **Product catalog**: 3 scenes (hero + context + detail)

---

### 4. Brand Profile (Optional)

**Type**: Object
**Default**: None
**Description**: Brand visual identity settings

**Full Specification**:
```json
"brand_profile": {
  "colors": ["#F5F5DC", "#8B7355", "#FFFFFF"],
  "mood": "serene zen minimal aesthetic",
  "target_audience": "interior design enthusiasts 30-45"
}
```

**Field Details**:

#### colors (array of hex codes)
```json
"colors": ["#000000", "#8B0000", "#FFFFFF"]
```
- Primary brand color
- Secondary/accent colors
- Background color preferences
- Applied to: color grading, background selection, prop colors

#### mood (string)
```json
"mood": "luxury elegant sophisticated"
```
- Brand tone/personality
- Applied to: lighting temperature, composition style, scene emotion
- Examples: "playful energetic", "professional trustworthy", "edgy rebellious"

#### target_audience (string)
```json
"target_audience": "urban millennials 25-35"
```
- Demographics and psychographics
- Applied to: lifestyle scene contexts, prop selection, visual references
- Examples: "busy parents", "fitness enthusiasts", "luxury consumers"

---

### 5. PNL Triggers (Optional)

**Type**: Array of strings
**Default**: Auto-selected per scene
**Description**: Programação neurolinguística emotional anchors

**Available Triggers**:
```json
"pnl_triggers": ["confiança", "conforto", "clareza"]
```

**Full Trigger Library**:
| Trigger | Portuguese | English Translation | Use Case |
|---------|-----------|---------------------|----------|
| `confiança` | Acabamento que inspira confiança durável | Finish that inspires lasting confidence | Quality products, durability |
| `conforto` | Toque seguro, superfície que convida | Secure touch, inviting surface | Comfort products, textiles |
| `clareza` | Visão total — nada escondido, decisão fácil | Total vision — nothing hidden, easy decision | Hero shots, transparency |
| `calma` | Ambiente sereno, temperatura ideal | Serene environment, ideal temperature | Wellness, home products |
| `desejo` | Brilho na medida, qualidade visível | Right amount of shine, visible quality | Luxury, beauty products |
| `urgência` | Momento certo, escolha agora | Right moment, choose now | Limited offers, FOMO |
| `pertencimento` | Encaixa na sua rotina sem atrito | Fits your routine without friction | Lifestyle integration |
| `transformação` | Antes cansado, agora descansado | Before tired, now rested | Before/after benefits |
| `segurança` | Sempre pronto, zero preocupação | Always ready, zero worry | Reliability, safety |
| `prazer` | Satisfação imediata, resultado que se vê | Immediate satisfaction, visible result | Instant gratification |

**Auto-Selection Logic** (when not specified):
- Scene 1 (Hero) → `clareza`
- Scene 2 (Lifestyle) → `conforto`
- Scene 3 (Macro) → `confiança`
- Scene 4 (Routine) → `pertencimento`
- Scene 5 (Benefit) → `prazer`
- Scene 6 (Functional) → `segurança`
- Scene 7 (Context) → `pertencimento`
- Scene 8 (Material) → `confiança`
- Scene 9 (Commercial) → `clareza`

---

### 6. Technical Overrides (Optional)

**Type**: Object
**Default**: Auto-calculated per scene and style
**Description**: Manual camera and lighting overrides

**Full Specification**:
```json
"technical_overrides": {
  "focal_length": "85mm",
  "aperture": "f/4",
  "lighting": "Rembrandt"
}
```

**Field Details**:

#### focal_length (string)
```json
"focal_length": "85mm"
```
- **Valid options**: 24mm, 35mm, 50mm, 85mm, 100mm, 135mm, 200mm
- **Use cases**:
  - 24mm: Wide environmental shots, architecture
  - 50mm: Standard product photography, versatile
  - 85mm: Portrait, beauty, editorial
  - 100mm: Macro detail, close-ups
  - 135mm+: Telephoto compression, fashion

#### aperture (string)
```json
"aperture": "f/4"
```
- **Valid range**: f/1.2 to f/16
- **Depth of field guide**:
  - f/1.2-f/2.8: Ultra shallow (strong bokeh, portrait)
  - f/4-f/5.6: Moderate shallow (lifestyle, editorial)
  - f/8-f/11: Deep focus (product, architecture)
  - f/16+: Maximum depth (landscape, group shots)
- **Compatibility checks**:
  - f/1.2-f/2.8 incompatible with "full focus" requirement
  - f/8-f/16 incompatible with "bokeh" requirement

#### lighting (string)
```json
"lighting": "Rembrandt"
```
- **Valid options**:
  - `high-key`: Bright even, minimal shadows, white background
  - `low-key`: Dramatic shadows, dark background, selective lighting
  - `3-point`: Classic key/fill/rim setup
  - `Rembrandt`: 45° key creating triangle on cheek
  - `Butterfly`: Frontal key creating shadow under nose
  - `Loop`: Slight angle key creating loop shadow
  - `natural`: Window/daylight simulation
  - `golden-hour`: Warm directional 5500K

---

### 7. AI Model (Optional)

**Type**: Enum
**Default**: `midjourney`
**Options**: `midjourney | dalle3 | stable_diffusion | imagen`

**Model-Specific Notes**:

#### Midjourney
```json
"ai_model": "midjourney"
```
- Prompts optimized for v6+ syntax
- Add parameters: `--ar 1:1 --q 2` for best results
- Supports detailed technical specs (camera, lighting)
- Best for: Photorealistic product photography

#### DALL-E 3
```json
"ai_model": "dalle3"
```
- Prompts work directly (no parameter flags)
- Natural language processing handles technical specs
- Best for: Conceptual imagery, creative interpretations

#### Stable Diffusion
```json
"ai_model": "stable_diffusion"
```
- Prompts compatible with SD 1.5, 2.1, SDXL
- Add negative prompt: "watermark, text, logo, low quality"
- Adjust sampling steps: 30-50 for quality
- Best for: High control, local generation

#### Imagen
```json
"ai_model": "imagen"
```
- Google's model, strong with realistic lighting
- Prompts emphasize lighting and composition
- Best for: Natural photography, outdoor scenes

---

### 8. Output Format (Optional)

**Type**: Enum
**Default**: `grid_3x3`
**Options**: `grid_3x3 | sequential_9`

#### Grid 3x3
```json
"output_format": "grid_3x3"
```
- **Output**: 1 single PNG (2000x2000px)
- **Layout**: 9 scenes in 3x3 grid (666x666px per scene)
- **Use case**: Quick marketplace upload, single-image story
- **Example**:
```
┌─────────┬─────────┬─────────┐
│ Scene 1 │ Scene 2 │ Scene 3 │
│ Hero    │ Use     │ Macro   │
├─────────┼─────────┼─────────┤
│ Scene 4 │ Scene 5 │ Scene 6 │
│ Routine │ Benefit │ Top-down│
├─────────┼─────────┼─────────┤
│ Scene 7 │ Scene 8 │ Scene 9 │
│ Context │ Quality │ Hero    │
└─────────┴─────────┴─────────┘
```

#### Sequential 9
```json
"output_format": "sequential_9"
```
- **Output**: 9 separate PNGs (2000x2000px each)
- **File naming**: `subject_scene_01_hero_white.png` ... `subject_scene_09_commercial_hero.png`
- **Use case**: A/B testing, carousel ads, independent scene optimization

---

## Configuration Files

### photography_styles.json

**Location**: `config/photography_styles.json`
**Purpose**: Define photography style presets

**Structure**:
```json
{
  "minimalist": {
    "name": "Minimalist",
    "description": "Clean backgrounds, soft lighting, muted colors",
    "default_camera": "50mm_f8",
    "default_lighting": "high-key",
    "background_preference": "white_light_gray",
    "color_palette": "muted_desaturated",
    "composition_style": "centered_negative_space"
  },
  "dramatic": { ... },
  "lifestyle": { ... },
  "editorial": { ... },
  "commercial": { ... }
}
```

**Customization**:
To add a new style preset:
1. Open `config/photography_styles.json`
2. Add new object with style name as key
3. Follow structure above
4. Save and restart agent

---

### camera_profiles.json

**Location**: `config/camera_profiles.json`
**Purpose**: Camera technical specifications

**Structure**:
```json
{
  "50mm_f8": {
    "focal_length": "50mm",
    "aperture": "f/8",
    "shutter_speed": "1/160s",
    "iso": 100,
    "depth_of_field": "deep",
    "use_case": "Full focus product hero"
  },
  "85mm_f4": {
    "focal_length": "85mm",
    "aperture": "f/4",
    "shutter_speed": "1/160s",
    "iso": 400,
    "depth_of_field": "moderate_shallow",
    "use_case": "Lifestyle editorial portrait"
  },
  "100mm_f28": { ... }
}
```

---

### pnl_triggers.json

**Location**: `config/pnl_triggers.json`
**Purpose**: Programação neurolinguística emotional anchors

**Structure**:
```json
{
  "confiança": {
    "portuguese": "acabamento que inspira confiança durável",
    "english": "finish that inspires lasting confidence",
    "use_cases": ["quality", "durability", "trust"],
    "recommended_scenes": [3, 8]
  },
  "conforto": { ... },
  "clareza": { ... }
}
```

**Customization**:
To add custom PNL triggers:
1. Open `config/pnl_triggers.json`
2. Add new trigger with key (Portuguese word)
3. Provide Portuguese phrase, English translation, use cases
4. Save and use in `pnl_triggers` input array

---

## Advanced Configuration Examples

### Example 1: E-commerce Product with Marketplace Compliance

```json
{
  "subject": "Wireless Bluetooth headphones matte black",
  "style": "commercial",
  "scenes": 9,
  "brand_profile": {
    "colors": ["#000000", "#FFFFFF", "#0066CC"],
    "mood": "professional modern tech",
    "target_audience": "professionals home office 25-45"
  },
  "pnl_triggers": ["confiança", "segurança", "clareza"],
  "ai_model": "midjourney",
  "output_format": "grid_3x3"
}
```

**Result**: 9-scene grid with white backgrounds (scenes 1, 9), professional studio lighting, tech-focused lifestyle contexts, brand colors integrated.

---

### Example 2: Fashion Editorial with Custom Camera Settings

```json
{
  "subject": "Female model wearing floral summer dress",
  "style": "editorial",
  "scenes": 5,
  "brand_profile": {
    "colors": ["#FFE4E1", "#98D8C8", "#FFFFFF"],
    "mood": "romantic feminine ethereal",
    "target_audience": "women fashion 20-35"
  },
  "pnl_triggers": ["desejo", "pertencimento", "transformação"],
  "technical_overrides": {
    "focal_length": "85mm",
    "aperture": "f/2.8",
    "lighting": "natural"
  },
  "ai_model": "midjourney",
  "output_format": "sequential_9"
}
```

**Result**: 5 separate high-resolution images with portrait focal length, shallow DOF for bokeh, natural lighting, romantic color grading.

---

### Example 3: Food Photography Lifestyle

```json
{
  "subject": "Artisan sourdough bread fresh from oven",
  "style": "lifestyle",
  "scenes": 9,
  "brand_profile": {
    "colors": ["#D2691E", "#F5DEB3", "#8B4513"],
    "mood": "rustic artisanal warm comfort",
    "target_audience": "home bakers food enthusiasts"
  },
  "pnl_triggers": ["prazer", "conforto", "calma"],
  "technical_overrides": {
    "lighting": "golden-hour"
  },
  "ai_model": "dalle3",
  "output_format": "grid_3x3"
}
```

**Result**: Warm rustic food photography with golden hour lighting, artisanal contexts, comfort-focused emotional triggers.

---

### Example 4: Abstract Concept Visualization

```json
{
  "subject": "Digital transformation concept - old analog to new digital",
  "style": "dramatic",
  "scenes": 5,
  "pnl_triggers": ["transformação", "clareza", "urgência"],
  "technical_overrides": {
    "lighting": "low-key"
  },
  "ai_model": "stable_diffusion",
  "output_format": "sequential_9"
}
```

**Result**: Conceptual metaphor visualization with dramatic contrasts, symbolic representation of analog-to-digital transition, urgency in visual storytelling.

---

## Environment Setup

### File Structure (After Setup)

```
photo_agent/
├── README.md                    # User documentation
├── PRIME.md                     # AI assistant entry point
├── INSTRUCTIONS.md              # Operational guide
├── SETUP.md                     # This file
│
├── prompts/
│   └── 60_prompt_generator.md  # Main HOP
│
├── config/
│   ├── photography_styles.json # 5 style presets
│   ├── camera_profiles.json    # Camera technical specs
│   └── pnl_triggers.json       # Emotional triggers
│
└── schemas/
    ├── photo_input.json        # Input validation schema
    └── photo_output.json       # Output structure schema
```

### Dependencies

**None** - `photo_agent` is fully standalone.

All photography knowledge is embedded in:
- Configuration files (`config/*.json`)
- Main HOP prompt (`prompts/60_prompt_generator.md`)
- Validation schemas (`schemas/*.json`)

---

## Troubleshooting

### Issue: Validation failing (<0.85 score)

**Cause**: Generated prompts missing required elements
**Solution**: Check that input subject description is detailed enough. Add specific visual features.

**Before** (fails validation):
```json
{"subject": "shoe"}
```

**After** (passes validation):
```json
{"subject": "White leather sneaker with red swoosh logo"}
```

---

### Issue: Prompts too generic

**Cause**: Insufficient subject detail or using overly broad categories
**Solution**: Be specific about materials, colors, distinctive features

**Before**:
```json
{"subject": "Coffee mug"}
```

**After**:
```json
{"subject": "Handcrafted ceramic coffee mug with matte blue glaze and wooden handle"}
```

---

### Issue: Style doesn't match expectation

**Cause**: Style preset may not suit subject type
**Solution**: Try different style or use custom technical overrides

**Example**: Product looks too dark (dramatic style applied to skincare)
**Fix**:
```json
{
  "subject": "Skincare serum bottle",
  "style": "minimalist",  // Changed from "dramatic"
}
```

---

### Issue: Brand colors not visible in output

**Cause**: Brand profile may conflict with style preset backgrounds
**Solution**: Use technical overrides to force brand integration

```json
{
  "brand_profile": {
    "colors": ["#FF6B6B", "#4ECDC4"]
  },
  "technical_overrides": {
    "lighting": "high-key"  // Ensures colors visible
  }
}
```

---

### Issue: Output format not as expected

**Cause**: AI model interpreting grid layout differently
**Solution**: Specify output format explicitly + add grid instruction to prompt

```json
{
  "output_format": "grid_3x3"
}
```

For Midjourney, manually add: `--ar 1:1 --tile` to encourage grid interpretation

---

## Performance Tuning

### Optimize for Speed
- Use fewer scenes (3-5 instead of 9)
- Use default style presets (avoid custom overrides)
- Use simpler subjects (avoid abstract concepts)

### Optimize for Quality
- Use 9 scenes for full narrative
- Provide detailed brand profile
- Specify custom PNL triggers aligned with brand
- Use technical overrides for manual control

### Optimize for Marketplace Compliance
- Use "commercial" style preset
- Ensure scenes count includes 1 and 9 (white backgrounds)
- Avoid dramatic/low-key styles
- Set `ai_model: "midjourney"` for best marketplace images

---

## Next Steps

1. **Review Documentation**:
   - Read `README.md` for capabilities overview
   - Check `PRIME.md` for AI assistant interaction
   - Study `INSTRUCTIONS.md` for workflow details

2. **Start Simple**:
   - Try minimal configuration (subject only)
   - Experiment with different style presets
   - Add brand profile once comfortable

3. **Iterate**:
   - Generate initial prompts
   - Review validation scores
   - Adjust input parameters based on results

4. **Customize**:
   - Edit configuration files for custom styles
   - Add custom PNL triggers for brand voice
   - Create technical override templates for repeated use

---

**Version**: 1.0.0
**Last Updated**: 2025-11-14
**Maintained by**: CODEXA Meta-Construction Framework
