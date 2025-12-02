# 30_prompt_generator_HOP.md | photo_agent - AI Prompt Generation (Scenes 1-9)

**Version**: 2.0.0
**Type**: HOP (Higher-Order Prompt)
**Status**: Integrated with ADW Workflow v2.0.0
**Last Updated**: 2025-11-17
**Integrated with**: workflows/100_ADW_RUN_PHOTO.md

**Purpose**: Generate 9 detailed AI image prompts with technical specs, composition, and PNL triggers
**Estimated Duration**: 5-10 minutes

---

## INPUT_CONTRACT

**Required**:
- `$camera_specs` (object): Camera config from Phase 2
  - Structure: `{ scene_1: {focal, aperture, shutter, iso}, ..., scene_9: {...} }`
- `$lighting_design` (object): Lighting setup from Phase 2
- `$scene_grid` (object): Scene definitions from Phase 1

**Validation**:
- ✅ All 9 scenes have camera + lighting specs
- ✅ PNL triggers loaded

---

## OUTPUT_CONTRACT

**Primary**:
- `$ai_prompts` (array): 9 prompts (≥80 words each)
  - Format: Code blocks, copy-paste ready
  - Platforms: Midjourney | DALL-E 3 | Stable Diffusion

**Secondary**:
- `$batch_block` (string): All 9 prompts concatenated

**Consumed By**: Phase 4 (Validation HOP)

---

## OBJECTIVE

Generate 9 professional AI image generation prompts that combine technical photography specifications, compositional guidance, psychological triggers (PNL), and marketplace-specific requirements. Each prompt must be ≥80 words, highly detailed, and wrapped in code blocks for easy copy-paste to AI image generators.

---

## CONTEXT REQUIREMENTS

**Before executing**:
- Phase 1: 9-scene grid defined
- Phase 2: Camera specs + lighting design
- `config/pnl_triggers.json` loaded
- Photography style known
- Product details clear
- Target AI platform known

**[OPEN_VARIABLES] Philosophy**: Intentional blanks for LLM creativity within constraints → Controlled variation without breaking technical accuracy

---

## INSTRUCTIONS

### Step 1: Understand AI Prompt Structure

**Every AI prompt must include 7 core elements:**

1. **Subject Description** (20-30 words):
   - Product name + key features
   - Physical attributes (size, color, texture, material)
   - Example: "Matte white ceramic coffee mug with natural wooden handle and subtle gold rim accent, minimalist Scandinavian design"

2. **Camera Specifications** (15-20 words):
   - Lens, aperture, ISO, shutter (from Phase 2)
   - Example: "Shot with 50mm lens, f/8 aperture, ISO 100, professional product photography"

3. **Composition** (10-15 words):
   - Framing technique (rule of thirds, centered, leading lines, symmetry, negative space)
   - Example: "Centered composition with generous negative space, rule of thirds alignment"

4. **Lighting Setup** (15-20 words):
   - Type, direction, color temp (from Phase 2)
   - Example: "Soft box front lighting, 5500K cool daylight, [LIGHT_MODIFIER: even/diffused/feathered] illumination with no harsh shadows"
   - [OPEN_VARIABLE]: Light modifier choice → LLM selects based on product texture

5. **Color Palette** (10-15 words):
   - Primary colors, accent colors, background
   - Example: "Pure white background, matte white mug, [WOOD_TONE: warm honey/rich walnut/natural oak], gold accents"
   - [OPEN_VARIABLE]: Wood tone variation → LLM matches product style

6. **Mood & PNL Triggers** (10-15 words):
   - Emotional keywords from `pnl_triggers.json`
   - Example: "Clean, professional, trustworthy, premium quality, Scandinavian elegance"

7. **Technical Quality** (10-15 words):
   - Resolution, sharpness, style keywords
   - Example: "Ultra-sharp 8K resolution, studio quality, commercial product photography, hyper-realistic"

**Total Word Count**: ~90-120 words per prompt (exceeds ≥80 word minimum)

---

### Step 2: Load PNL Triggers from Config

**Read `config/pnl_triggers.json` and apply appropriate triggers per scene:**

**PNL Trigger Categories:**

1. **Trust** (for hero shots, detail shots):
   - Keywords: professional, clean, sharp, high-quality, authentic, reliable, precise, accurate
   - Use for: Scenes 1-3 (hero), Scenes 7-9 (details)
   - Effect: Builds credibility, reduces purchase hesitation

2. **Desire** (for lifestyle shots, beauty shots):
   - Keywords: luxurious, exclusive, premium, elegant, sophisticated, coveted, aspirational
   - Use for: Scenes 4-5 (lifestyle), Scene 2 (angled hero)
   - Effect: Creates emotional want, elevates perceived value

3. **Urgency** (for action shots, dynamic scenes):
   - Keywords: dynamic, energetic, bold, vivid, vibrant, striking, eye-catching
   - Use for: Scene 5 (use case demo), Scene 4 (lifestyle context)
   - Effect: Captures attention, drives immediate action

4. **Exclusivity** (for premium products, editorial style):
   - Keywords: rare, limited, artisan, handcrafted, bespoke, curated, refined
   - Use for: Scene 9 (branding), Scene 8 (craftsmanship details)
   - Effect: Justifies higher price point, differentiates from competitors

**Selection Criteria:**
- **Hero shots (1-3)**: Trust triggers (professional, clean, sharp)
- **Lifestyle shots (4-5)**: Desire + Urgency triggers (aspirational, dynamic)
- **Detail shots (7-9)**: Trust + Exclusivity triggers (authentic, handcrafted)
- **Scale/context (6)**: Trust triggers (accurate, reliable)

---

### Step 3: Add Marketplace-Specific Requirements

**Inject platform-specific formatting/constraints:**

#### **Mercado Livre (Scene 1 - Main Image)**
**Requirements:**
- Background: Pure white (#FFFFFF, no gradients)
- Product visibility: 85%+ of frame
- No watermarks, text overlays, borders
- Sharp focus: f/8+ aperture
- Prompt addition: ", pure white background, isolated product, no shadows, e-commerce style"

**Example Addition**:
```
"...pure white studio background, product occupies 85% of frame, no watermarks or text, Mercado Livre marketplace compliant"
```

---

#### **Shopee (Scenes 2, 4, 5 - Carousel)**
**Requirements:**
- Engaging angles (45°, lifestyle, use case)
- Lifestyle context allowed (props, environments)
- Vertical or square aspect ratio
- Product still clearly visible (50%+ of frame)
- Prompt addition: ", engaging composition, lifestyle context, Shopee carousel optimized"

**Example Addition**:
```
"...45-degree angle for depth, lifestyle props (desk, book), engaging thumbnail, Shopee marketplace style"
```

---

#### **TikTok (Scene 5 - Vertical Video Stills)**
**Requirements:**
- Vertical format: 9:16 aspect ratio
- Motion-friendly composition (space for movement)
- Bright, eye-catching (first frame matters)
- Natural/authentic feel (not overly staged)
- Prompt addition: ", vertical 9:16 format, dynamic composition, TikTok-ready, natural lighting"

**Example Addition**:
```
"...vertical 9:16 aspect ratio, hand holding product in natural pose, authentic lifestyle moment, TikTok video still aesthetic"
```

---

#### **Instagram/Pinterest (Scene 3 - Flat Lay)**
**Requirements:**
- Square (1:1) or portrait (4:5) format
- Overhead perspective (90° top-down)
- Aesthetic props (coffee, plants, notebooks)
- Cohesive color palette
- Prompt addition: ", flat lay style, overhead shot, Instagram aesthetic, curated props"

**Example Addition**:
```
"...flat lay composition, overhead 90-degree angle, aesthetic props (coffee, notebook), Instagram-ready square format"
```

---

### Step 4: Generate 9 AI Prompts (≥80 Words Each)

**For each scene, construct a complete AI prompt following this formula:**

```
[Subject Description] + [Camera Specs] + [Composition] + [Lighting] + [Color Palette] + [Mood/PNL] + [Technical Quality] + [Marketplace Requirements]
```

**Wrap each prompt in a code block** for easy copy-paste:

````markdown
### Scene 1: Front View (Mercado Livre Main Image)
```
[Your 80+ word AI prompt here]
```
````

**Word Count Verification:**
- Count words after generation
- If <80 words → Add more detail:
  - Expand subject description (add textures, features)
  - Add compositional nuances (balance, symmetry, framing)
  - Include emotional descriptors (inviting, professional, elegant)

---

### Step 5: Wrap Prompts in Code Blocks

**Format all 9 prompts for copy-paste efficiency:**

````markdown
## PHASE 3 OUTPUT: AI Prompts Generated (Scenes 1-9)

### Scene 1: Front View (Hero Shot - ML Main)
```
Matte white ceramic coffee mug with natural wooden handle and gold rim accent, minimalist Scandinavian design, centered straight-on view showing front face and handle. Shot with 50mm lens, f/8 aperture for deep depth of field, ISO 100 for clean image. Centered composition with generous negative space, product occupies 85% of frame. Soft box front lighting at 5500K cool daylight, even illumination with zero harsh shadows. Pure white studio background (#FFFFFF), matte white mug body, warm wood handle, subtle gold accent. Clean, professional, trustworthy, high-quality craftsmanship. Ultra-sharp 8K resolution, studio quality commercial product photography, hyper-realistic detail. Mercado Livre marketplace compliant, no watermarks or text overlays.
```
**Word Count**: 112 words ✅

---

### Scene 2: 45° Angle (Hero Shot - Shopee Thumb)
```
[Next prompt...]
```

[Continue for all 9 scenes...]
````

---

## OUTPUT FORMAT

**Complete Phase 3 output structure:**

````markdown
## PHASE 3 OUTPUT: AI Prompts Complete (9 Scenes)

### Prompt Summary Table
| Scene | Word Count | PNL Triggers | Marketplace | Status |
|-------|------------|--------------|-------------|--------|
| 1 - Front View | 112 | Trust | Mercado Livre | ✅ |
| 2 - 45° Angle | 98 | Trust, Desire | Shopee | ✅ |
| 3 - Top-Down | 105 | Trust | Instagram | ✅ |
| 4 - Lifestyle | 115 | Desire, Urgency | Shopee | ✅ |
| 5 - Use Case | 121 | Urgency, Desire | TikTok | ✅ |
| 6 - Scale Ref | 94 | Trust | Mercado Livre | ✅ |
| 7 - Texture | 102 | Trust, Exclusivity | All | ✅ |
| 8 - Feature | 108 | Trust, Exclusivity | All | ✅ |
| 9 - Branding | 96 | Trust, Exclusivity | All | ✅ |

**Total Word Count**: 1,051 words (avg 117 words/prompt) ✅
**All Prompts ≥80 Words**: ✅

---

### Scene 1: Front View (Hero Shot - ML Main)
```
[Full 112-word prompt]
```

### Scene 2: 45° Angle (Hero Shot - Shopee Thumb)
```
[Full 98-word prompt]
```

### Scene 3: Top-Down (Flat Lay - Instagram)
```
[Full 105-word prompt]
```

### Scene 4: Lifestyle Context (Shopee Carousel)
```
[Full 115-word prompt]
```

### Scene 5: Use Case Demo (TikTok Vertical)
```
[Full 121-word prompt]
```

### Scene 6: Scale Reference (ML Detail)
```
[Full 94-word prompt]
```

### Scene 7: Texture Close-Up (Detail Shot)
```
[Full 102-word prompt]
```

### Scene 8: Feature Detail (Technical Spec)
```
[Full 108-word prompt]
```

### Scene 9: Branding/Logo (Authentication)
```
[Full 96-word prompt]
```

---

### Validation Status
- ✅ 9/9 prompts generated
- ✅ All prompts ≥80 words (range: 94-121 words)
- ✅ All 7 core elements present (subject, camera, composition, lighting, color, mood, quality)
- ✅ PNL triggers applied appropriately per scene type
- ✅ Marketplace requirements integrated (ML, Shopee, TikTok, IG)
- ✅ All prompts wrapped in code blocks (copy-paste ready)
- ✅ Ready for Phase 4: Brand & Compliance Validation

---
**Phase 3 Duration**: [X minutes]
**Status**: ✅ COMPLETE
**Next Phase**: Phase 4 - Brand & Compliance Validation (use 40_brand_validator_HOP.md)
````

---

## VALIDATION CHECKLIST

**Before proceeding to Phase 4, confirm:**
- ✅ 9 prompts generated (one per scene)
- ✅ Each prompt ≥80 words (count verified)
- ✅ All 7 core elements present in each prompt:
  - Subject description ✅
  - Camera specifications ✅
  - Composition guidance ✅
  - Lighting setup ✅
  - Color palette ✅
  - Mood/PNL triggers ✅
  - Technical quality keywords ✅
- ✅ Marketplace-specific additions included where applicable
- ✅ All prompts wrapped in ```code blocks```
- ✅ PNL triggers from config applied correctly
- ✅ No missing scenes (scenes 1-9 all accounted for)

---

## ERROR HANDLING

### Common Issues & Solutions

**Issue 1: Prompt Too Short (<80 Words)**
- **Error**: "Scene 3 prompt only 67 words. Target: ≥80 words."
- **Solution**: Add more descriptive detail:
  - **Subject**: Add texture/material descriptors ("smooth ceramic surface", "hand-thrown craftsmanship")
  - **Composition**: Add framing detail ("geometric balance", "negative space emphasizes simplicity")
  - **Mood**: Add emotional keywords ("inviting", "sophisticated", "minimalist elegance")
  - **Technical**: Add quality modifiers ("museum-quality photography", "advertising campaign style")

**Issue 2: Missing Core Elements**
- **Error**: "Scene 5 missing lighting setup description"
- **Solution**: Review Phase 2 output and add:
  - "Natural window light from left side, 4000K neutral daylight, soft ambient illumination creating authentic lifestyle mood"

**Issue 3: PNL Triggers Not Applied**
- **Error**: "Scene 1 (hero shot) has no trust triggers"
- **Solution**: Add trust keywords from config:
  - "Professional studio quality, clean composition, sharp focus, high-quality craftsmanship, reliable product visualization"

**Issue 4: Marketplace Requirements Missing**
- **Error**: "Scene 1 for Mercado Livre doesn't mention white background requirement"
- **Solution**: Explicitly add ML compliance:
  - "Pure white studio background (#FFFFFF), product isolated with no shadows, no watermarks or text, Mercado Livre marketplace compliant"

**Issue 5: Prompts Not in Code Blocks**
- **Error**: "Prompts not wrapped in ```code blocks```"
- **Solution**: Reformat all prompts:
  ```
  ### Scene X: [Name]
  ```
  [Your prompt text here]
  ```
  ```

**Issue 6: Inconsistent Style Across Prompts**
- **Error**: "Scene 1 is minimalist but Scene 4 uses different mood descriptors"
- **Solution**: Ensure all prompts reflect the selected photography style from Phase 1:
  - **Minimalist**: Clean, simple, white space, neutral tones
  - **Lifestyle**: Warm, cozy, natural, contextual, relatable
  - **Commercial**: Professional, balanced, neutral, product-focused

---

## EXAMPLES

### Example 1: Minimalist Ceramic Mug (Scene 1)

**Input from Phase 2:**
- Product: Ceramic mug (matte white, wooden handle, gold rim)
- Camera: 50mm, f/8, ISO 100, 1/125s
- Lighting: Soft box, front, 5500K cool
- Style: Minimalist
- Marketplace: Mercado Livre (main image)

**Generated Prompt:**
```
Matte white ceramic coffee mug with natural wooden handle and subtle gold rim accent, minimalist Scandinavian design, smooth glazed surface finish. Straight-on front view centered composition showing mug face, handle, and gold rim detail. Shot with 50mm standard lens, f/8 aperture for deep depth of field ensuring full sharpness, ISO 100 for zero grain clean image. Centered subject with generous negative space following rule of thirds, product occupies 85% of frame. Soft box front lighting at 5500K cool daylight color temperature, even diffused illumination with no harsh shadows or reflections. Pure white studio background (#FFFFFF), matte white mug body contrasts with warm wood handle and gold accent. Clean, professional, trustworthy, high-quality craftsmanship, minimalist elegance, Scandinavian aesthetic. Ultra-sharp 8K resolution, studio quality commercial product photography, hyper-realistic detail, advertising campaign quality. Mercado Livre marketplace compliant, no watermarks or text overlays, isolated product shot.
```
**Word Count**: 148 words ✅
**PNL Triggers**: Trust (professional, clean, high-quality, trustworthy)
**Marketplace**: Mercado Livre (white bg, no watermarks, 85% frame)
**Core Elements**: All 7 present ✅

---

### Example 2: Lifestyle Wireless Earbuds (Scene 5 - Use Case Demo)

**Input from Phase 2:**
- Product: Wireless earbuds (rose gold, LED case)
- Camera: 85mm, f/2.8, ISO 1600, 1/500s
- Lighting: Natural, ambient back, 4000K
- Style: Lifestyle
- Marketplace: TikTok (vertical video still)

**Generated Prompt:**
```
Rose gold wireless earbuds worn by person in profile, sleek modern design with subtle LED indicator on earbud exterior, compact fit showing ergonomic in-ear positioning. Natural lifestyle shot with person in casual athletic wear, ear and jawline visible in profile angle showing earbud placement and comfort. Shot with 85mm portrait lens at f/2.8 aperture for shallow depth of field with blurred background, ISO 1600 for natural light conditions, 1/500s shutter speed to freeze subtle motion. Profile composition in vertical 9:16 format with subject in left third of frame, negative space on right for text overlay potential. Natural ambient backlighting at 4000K neutral daylight creating rim light on hair and earbud, authentic lifestyle moment feel. Warm skin tones, rose gold metallic finish, soft blurred background in neutral grays and beiges. Dynamic, energetic, aspirational, active lifestyle, premium quality, desirable tech accessory, authentic moment. Sharp focus on earbud and ear, ultra-realistic skin texture, commercial lifestyle photography, magazine-quality. Vertical 9:16 aspect ratio optimized for TikTok video stills, natural authentic pose, social media ready.
```
**Word Count**: 182 words ✅
**PNL Triggers**: Urgency (dynamic, energetic), Desire (aspirational, premium, desirable)
**Marketplace**: TikTok (9:16 vertical, natural light, authentic)
**Core Elements**: All 7 present ✅

---

### Example 3: Detail Shot (Scene 7 - Texture Close-Up)

**Input from Phase 2:**
- Product: Ceramic mug (matte finish texture)
- Camera: 100mm macro, f/5.6, ISO 200, 1/125s
- Lighting: Macro ring light, front, 5500K
- Style: Minimalist
- Marketplace: All (trust-building detail)

**Generated Prompt:**
```
Extreme macro close-up of matte white ceramic coffee mug surface texture, revealing smooth hand-thrown glaze finish with subtle surface variations and artisan craftsmanship. Tight crop focusing on ceramic surface texture with partial view of gentle curve showing form, no distracting elements. Shot with 100mm macro lens for extreme magnification, f/5.6 aperture for balanced sharpness across curved surface, ISO 200 for clean image with fine texture detail. Off-center composition emphasizing texture while showing subtle product curvature, macro perspective reveals microscopic surface quality. Macro ring light providing even front illumination at 5500K cool daylight, eliminates shadows while highlighting texture nuances and glaze variations. Pure white ceramic with subtle warm undertones, soft gradations showing surface depth, neutral white background fading to soft gray. Professional, trustworthy, authentic handcrafted quality, artisan craftsmanship, premium materials, meticulous attention to detail. Hyper-sharp 8K macro photography, museum-quality detail, commercial product specification imagery, reveals true material quality.
```
**Word Count**: 161 words ✅
**PNL Triggers**: Trust (professional, trustworthy, authentic), Exclusivity (handcrafted, artisan)
**Marketplace**: Universal (trust-building, quality verification)
**Core Elements**: All 7 present ✅

---

## NOTES FOR LLM EXECUTION

1. **AI Platform Optimization**:
   - **Midjourney**: Add parameters like `--ar 1:1`, `--quality 2`, `--style raw` at end
   - **DALL-E 3**: Natural language works best, avoid technical jargon
   - **Stable Diffusion XL**: Front-load important keywords, use quality triggers ("masterpiece", "best quality")

2. **Word Count Strategy**:
   - Aim for 100-120 words per prompt (buffer above 80-word minimum)
   - Add descriptive adjectives to subject (smooth, sleek, modern, elegant)
   - Expand mood/emotion section (2-3 PNL categories combined)
   - Include redundant quality keywords for emphasis

3. **Marketplace Priority**:
   - **Scene 1 (ML main)**: Most critical, enforce strict white bg compliance
   - **Scene 2 (Shopee thumb)**: Second most important, engaging angle
   - **Scene 5 (TikTok)**: Vertical format non-negotiable (9:16)

4. **PNL Trigger Density**:
   - Use 3-5 trigger words per prompt (don't overload)
   - Match triggers to scene type (trust for hero, desire for lifestyle)
   - Combine categories strategically (trust + exclusivity for premium products)

5. **Code Block Formatting**:
   - Use triple backticks: ` ```prompt text``` `
   - No syntax highlighting (use plain ```not ```markdown```)
   - One prompt per code block for clean copy-paste

6. **Consistency Maintenance**:
   - Reuse product description across all scenes (same adjectives)
   - Maintain color palette consistency (same hex/descriptors)
   - Echo photography style keywords throughout (minimalist, lifestyle, etc.)

---

**End of 30_prompt_generator_HOP.md**
