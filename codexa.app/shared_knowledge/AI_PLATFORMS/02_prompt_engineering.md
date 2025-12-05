# Prompt Engineering | shared_knowledge

**Purpose**: Universal prompting patterns for AI generation platforms
**Version**: 1.0.0 | **Updated**: 2025-12-05
**Quality Score**: 0.88/1.00

---

## OVERVIEW

This knowledge card provides universal prompt engineering patterns that work across AI image and video generation platforms. Learn the core anatomy, platform adaptations, and optimization techniques.

**Philosophy**: Master the universal formula, then adapt to platform-specific syntax.

---

## UNIVERSAL PROMPT ANATOMY

### Core Formula (All Platforms)

```
[SUBJECT] + [STYLE] + [TECHNICAL] + [MODIFIERS]
```

### Expanded Formula (7 Elements)

```
[Camera] + [Subject] + [Action] + [Environment] + [Lighting] + [Style] + [Audio*]
```

*Audio only for platforms with native support (Veo 3, Sora 2)

---

## THE 7 ESSENTIAL ELEMENTS

### 1. CAMERA (How We See)

Defines perspective and visual movement.

**Angles**:
```
low angle       - power, dominance
high angle      - vulnerability, overview
eye level       - neutral, relatable
overhead        - product showcase, patterns
dutch angle     - tension, unease
```

**Movements**:
```
dolly in/out    - emotional emphasis
pan left/right  - reveal, environment
tracking        - follow subject
crane           - grand reveal
static          - stability, focus
orbit           - product showcase
push in         - intimate approach
pull back       - context reveal
```

**Lenses**:
```
wide angle      - environment, space
35mm            - cinematic standard
50mm            - natural, eye-like
85mm            - portraits, products
telephoto       - compression, isolation
macro           - detail shots
```

**Framing**:
```
extreme wide    - establishing shot
wide shot       - full environment
medium shot     - waist up
close-up        - face, product detail
extreme close-up - eyes, texture
```

**Example**:
```
"Low angle dolly forward, 35mm lens, medium shot"
```

---

### 2. SUBJECT (Who/What)

The primary focus of the scene.

**People**:
```
[age] [ethnicity] [gender] [expression] [clothing] [action]
"Confident Brazilian woman, 30s, wearing navy blazer"
```

**Products**:
```
[product name] [material] [color] [finish] [positioning]
"Premium wireless earbuds in matte black finish"
```

**Objects**:
```
[object] [key characteristics] [state]
"Vintage leather journal with worn edges"
```

---

### 3. ACTION (What Happens)

Movement or activity of the subject.

**Movement Verbs**:
```
walking, running, turning, rotating, floating
gesturing, typing, speaking, demonstrating
```

**Transitions**:
```
appearing, dissolving, transforming
morphing, fading, emerging
```

**Speeds**:
```
slowly, smoothly, dynamically, rapidly
gracefully, deliberately
```

**Example**:
```
"slowly rotating 360 degrees, revealing all angles"
```

---

### 4. ENVIRONMENT (Where)

Spatial context of the scene.

**Locations**:
```
studio, office, outdoor, home, abstract
urban, nature, industrial, futuristic
```

**Backgrounds**:
```
pure white (#FFFFFF), seamless, gradient
blurred city, bokeh lights, natural landscape
```

**Atmosphere**:
```
clean, minimal, busy, cozy, professional
futuristic, vintage, rustic, modern
```

**Example**:
```
"modern glass-walled office with city skyline visible"
```

---

### 5. LIGHTING (How It Illuminates)

Defines mood and visual quality.

**Types**:
```
natural light   - soft, realistic
studio light    - controlled, professional
dramatic        - high contrast
soft            - diffused, flattering
rim light       - edge definition
```

**Directions**:
```
front           - flat, informative
side            - dimensional, dramatic
back            - silhouette, rim
overhead        - even, studio
three-point     - professional standard
```

**Temperature**:
```
warm (golden)   - cozy, inviting
cool (blue)     - modern, tech
neutral         - balanced, accurate
```

**Moods**:
```
high-key        - bright, optimistic
low-key         - moody, dramatic
golden hour     - warm, cinematic
blue hour       - cool, atmospheric
```

**Example**:
```
"warm golden hour light streaming through windows, soft shadows"
```

---

### 6. STYLE (Aesthetic)

Quality qualifiers and visual aesthetic.

**Quality**:
```
4K, 8K, cinematic, professional, high-end
ultra-realistic, photorealistic
```

**Aesthetics**:
```
minimal, luxury, tech, editorial
raw, polished, vintage, modern
```

**Effects**:
```
shallow depth of field, motion blur
lens flare, film grain, bokeh
```

**References**:
```
shot on 35mm, Pixar-style, film noir
National Geographic, Vogue editorial
```

**Example**:
```
"cinematic 4K quality, shallow depth of field, shot on 35mm"
```

---

### 7. AUDIO (What We Hear) *

*Only for Veo 3 and Sora 2

**Dialogue**:
```
Character says: "Your text here" (no subtitles)
```

**Sound Effects**:
```
satisfying click, subtle whoosh, ambient hum
```

**Ambient**:
```
quiet office atmosphere, distant traffic
nature sounds, bustling city
```

**Music**:
```
upbeat corporate, cinematic score
ambient electronic, subtle piano
```

---

## PLATFORM-SPECIFIC SYNTAX

### Midjourney v6

```
[Subject], [style descriptors], [lighting], [composition] --ar 16:9 --v 6 --style raw --stylize 100
```

**Parameters**:
- `--ar 1:1` (square), `--ar 16:9` (landscape), `--ar 9:16` (portrait)
- `--v 6` or `--v 6.1` (version)
- `--style raw` (photographic), `--style default` (artistic)
- `--stylize 0-1000` (artistic interpretation)
- `--chaos 0-100` (variation)
- `--no [element]` (negative prompts)

### DALL-E 3

```
Detailed natural language description. Be specific about what you want to see, including composition, colors, lighting, and style.
```

**API Parameters**:
```json
{
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "hd",
  "style": "natural"
}
```

### Google Imagen 3

```
Professional [type] photography, [subject description], [background], [lighting setup], [style qualifiers], 8K quality
```

**Optimal Structure**:
```
[Subject], [environment], [lighting], [camera angle], [style], [quality]
```

### Runway Gen-3

```
[camera movement]: [establishing scene]. [additional details].
```

**Simple and direct. Front-load important elements.**

### Veo 3 (Google)

```
[Camera movement]: [Scene]. [Subject]. [Action]. [Lighting]. [Style]. [Audio].
```

### Sora 2 (OpenAI)

```
LOOK: [visual style, color grade]
CAMERA: [lens, movement, angle]
LIGHTING: [key, fill, mood]
SOUNDSCAPE: [ambient, sfx, music]
ACTION: [subject movement, timing]
```

### Pika 2.0

```
[Style] + [Subject] + [Action] + [Environment] + [Lighting] + [Camera] --camera [movement]
```

### Kling 1.6

```
[Subject], [description], [movement], [scene]. [Camera, lighting, atmosphere].
```

### Hailuo/MiniMax

```
[Camera Shot + Motion] + [Subject] + [Action] + [Scene] + [Lighting] + [Style/Mood]
```

**Emphasis**: `((important element))` for priority

---

## MAGIC WORDS (Quality Boosters)

### Universal Quality

```
4K, 8K, ultra-detailed, high-resolution
masterpiece, professional quality
photorealistic, hyper-realistic
```

### Photography Style

```
shot on Canon EOS R5, 85mm f/1.4
Hasselblad medium format
National Geographic style
editorial photography
```

### Lighting Magic

```
golden hour, blue hour
Rembrandt lighting, butterfly lighting
cinematic lighting, studio lighting
natural window light
```

### Mood/Atmosphere

```
moody, atmospheric, dreamy
clean, minimalist, elegant
dramatic, intense, serene
```

### Video Specific

```
smooth motion, fluid camera movement
cinematic pacing, dynamic action
seamless transition
```

---

## ANTI-PATTERNS (What to Avoid)

### Vague Descriptions

```
X "A nice photo of a product"
X "Beautiful lighting"
X "High quality image"
X "Someone doing something"

V "Premium wireless headphones floating against pure white background"
V "Warm golden hour rim lighting creating soft shadows"
V "Cinematic 4K, shallow depth of field, 35mm film look"
V "Confident entrepreneur gestures toward holographic dashboard"
```

### Negative Instructions

```
X "The camera doesn't move"
X "No background noise"
X "Don't show the face"

V "Static locked shot on tripod"
V "Quiet ambient atmosphere"
V "Subject shown from behind"
```

### Conflicting Instructions

```
X "Bright and moody, high-key dramatic"
X "Fast-paced slow motion"
X "Minimalist with lots of detail"
```

### Overloading

```
X "4K 8K HDR10+ high-definition ultra-realistic photorealistic professional"

V "Cinematic 4K quality, photorealistic"
```

---

## PROMPT TEMPLATES

### Product Photography (Marketplace)

```
Professional product photography, [PRODUCT_NAME] in [COLOR/MATERIAL],
centered on pure white background (#FFFFFF),
soft studio lighting from upper left, subtle shadows,
high-resolution, commercial quality, no text
```

### Lifestyle/Editorial

```
[PRODUCT_NAME] in real-world context, [LOCATION/SCENE],
[SUBJECT INTERACTION], natural lighting,
shallow depth of field, editorial style,
shot on 85mm, warm tones
```

### Video Product Showcase

```
Slow orbit shot: [PRODUCT_NAME] floating at eye level,
rotating smoothly revealing all angles,
pure white studio background,
soft key light creating dimensional shadows,
cinematic 4K, 3-second duration
```

### Video Brand Story

```
[Camera movement], [lens]: [Person description] in [environment].
[Action/expression]. [Lighting description], [mood].
[Style qualifiers].
```

### Before/After Transformation

```
[Initial state description], [transformation action],
[final state], smooth transition,
split-screen or morph effect,
upbeat energy
```

---

## PROMPT OPTIMIZATION CHECKLIST

Before submitting any prompt, verify:

- [ ] Camera/perspective defined
- [ ] Subject clearly described
- [ ] Action is specific (not vague)
- [ ] Environment/context included
- [ ] Lighting specified
- [ ] Style/quality qualifiers present
- [ ] Prompt in English
- [ ] Appropriate length (20-500 chars)
- [ ] No negative instructions ("don't", "no X")
- [ ] One primary camera movement (video)
- [ ] Most important element first

---

## DETAIL LEVELS

### Basic (Beginner)

```
A product rotating on white background, studio lighting.
```

### Intermediate

```
Slow orbit shot: Premium wireless headphones floating against
pure white background, soft studio lighting, shallow depth of field.
```

### Advanced

```
Smooth 360 orbit, 85mm telephoto lens: Premium wireless headphones
in matte black finish floating at eye level, rotating slowly
revealing design details. Pure white seamless studio background.
Soft key light from upper left, subtle fill from right, creating
dimensional shadows. Cinematic 4K, shallow depth of field isolating
product, 3-second loop.
```

---

## ITERATION STRATEGY

1. **Start Simple**: Core subject + basic style
2. **Add Specifics**: Camera, lighting, environment
3. **Refine Details**: Quality boosters, effects
4. **Test & Iterate**: Generate, evaluate, adjust
5. **Document Winners**: Save successful prompts

**Golden Rule**: Each iteration changes ONE element.

---

## INTEGRATION

**photo_agent**: Uses templates for 9-scene batches
**video_agent**: Adapts per platform requirements
**Cross-reference**: [platform_comparison.md](01_platform_comparison.md) for platform selection

---

**Package**: AI_PLATFORMS v1.0.0
**Card**: 02_prompt_engineering
**Quality**: 0.88/1.00
**Date**: 2025-12-05
