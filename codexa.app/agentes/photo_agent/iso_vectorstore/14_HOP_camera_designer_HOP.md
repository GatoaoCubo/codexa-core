<!-- iso_vectorstore -->
<!--
  Source: 20_camera_designer_HOP.md
  Agent: photo_agent
  Synced: 2025-12-02
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 20_camera_designer_HOP.md | photo_agent - Camera & Lighting Design

**Version**: 2.0.0
**Type**: HOP (Higher-Order Prompt)
**Status**: Integrated with ADW Workflow v2.0.0
**Last Updated**: 2025-11-17
**Integrated with**: workflows/100_ADW_RUN_PHOTO.md

**Purpose**: Design technical camera specifications and lighting setups for all 9 scenes
**Input**: Phase 1 output (9-scene grid + style + configurations loaded)
**Output**: Complete camera specs (lens, aperture, ISO, shutter) + lighting design per scene
**Estimated Duration**: 3-7 minutes

---

## OBJECTIVE

Design professional camera specifications and lighting setups for each of the 9 scenes from Phase 1. Ensure technical accuracy, alignment with photography style, and marketplace compliance (e.g., Mercado Livre white background requirements).

---

## CONTEXT REQUIREMENTS

**Before executing this prompt, ensure:**
- Phase 1 completed: 9-scene grid defined with angles/purposes
- `config/camera_profiles.json` loaded (reference camera presets)
- `config/photography_styles.json` loaded (style-specific lighting requirements)
- Photography style selected (minimalist, lifestyle, commercial, etc.)
- Product type known (determines lens choice: macro for details, wide for context)

---

## INSTRUCTIONS

### Step 1: Design Camera Specifications for Each Scene

**For each of the 9 scenes, define the following camera settings:**

#### **A. Lens Selection (Focal Length)**

**Purpose**: Control perspective, depth, and field of view

**Lens Types & Use Cases:**
- **35mm (wide angle)**: Lifestyle scenes (4-6), environmental context, storytelling
  - Example: Scene 4 (mug on desk with background), Scene 5 (person using product)

- **50mm (standard)**: Hero shots (1-3), natural perspective, versatile
  - Example: Scene 1 (front view), Scene 2 (45° angle), Scene 3 (top-down)

- **85mm (portrait)**: Product portraits, shallow depth of field, subject isolation
  - Example: Scene 6 (scale reference with hand)

- **100mm macro**: Detail shots (7-9), extreme close-ups, texture/feature focus
  - Example: Scene 7 (texture), Scene 8 (feature detail), Scene 9 (logo)

**Selection Criteria:**
- **Hero shots (1-3)**: 50mm (standard perspective, no distortion)
- **Context shots (4-6)**: 35mm (wider view for environment) OR 85mm (human interaction)
- **Detail shots (7-9)**: 100mm macro (magnification for textures/features)

---

#### **B. Aperture (f-stop)**

**Purpose**: Control depth of field (DOF) and background blur

**Aperture Values & Effects:**
- **f/1.8 - f/2.8** (wide open): Shallow DOF, blurred background, subject isolation
  - Use for: Lifestyle shots (Scene 4-5), portrait-style product shots
  - Effect: "Bokeh" background blur, draws eye to subject

- **f/4 - f/5.6** (moderate): Balanced DOF, some background detail visible
  - Use for: General product shots (Scene 1-2-6), context with slight blur
  - Effect: Subject sharp, background softly defined

- **f/8 - f/11** (narrow): Deep DOF, everything in focus (front to back)
  - Use for: Hero shots with white bg (Scene 1), detail shots (Scene 7-8-9)
  - Effect: Maximum sharpness, no blur (critical for e-commerce)

- **f/16+** (very narrow): Maximum DOF, entire scene sharp
  - Use for: Flat lay (Scene 3), technical specs requiring full focus
  - Effect: Every element crisp (used sparingly, requires more light)

**Selection Criteria:**
- **Mercado Livre compliance (Scene 1)**: f/8+ (white bg, everything sharp)
- **Lifestyle/emotional (Scene 4-5)**: f/2.8 - f/4 (subject isolated, mood)
- **Technical/detail (Scene 7-9)**: f/5.6 - f/8 (feature sharp, context minimized)

---

#### **C. ISO (Light Sensitivity)**

**Purpose**: Control image brightness and grain/noise

**ISO Values & Effects:**
- **ISO 100**: Cleanest image, zero grain, requires strong lighting
  - Use for: Studio shots (Scene 1-3), white background, controlled lighting

- **ISO 200-400**: Slight noise (negligible), good balance
  - Use for: Most scenes (Scene 2, 6, 7-9), standard product photography

- **ISO 800-1600**: Visible grain, but acceptable for lifestyle
  - Use for: Natural light scenes (Scene 4-5), ambient/moody shots

- **ISO 3200+**: Heavy grain, avoid for e-commerce (quality loss)
  - Avoid unless: Intentional artistic effect (rarely used)

**Selection Criteria:**
- **Hero shots (1-3)**: ISO 100-200 (maximum quality for main images)
- **Context shots (4-6)**: ISO 400-800 (natural light scenarios)
- **Detail shots (7-9)**: ISO 200-400 (balance quality + flexibility)

---

#### **D. Shutter Speed (Motion Control)**

**Purpose**: Freeze motion or create motion blur

**Shutter Speed Values:**
- **1/1000s - 1/2000s**: Freeze fast action (splashes, movement)
  - Use for: Scene 5 (pouring coffee, product in motion)

- **1/125s - 1/250s**: Standard product photography (handhold safe)
  - Use for: Most scenes (1-4, 6-9), static product shots

- **1/60s - 1/30s**: Slower, requires tripod (low light)
  - Use for: Moody lifestyle (Scene 4 with ambient light)

- **1s+**: Long exposure, motion blur backgrounds (creative)
  - Rarely used for e-commerce (experimental only)

**Selection Criteria:**
- **Static product (Scene 1-3, 7-9)**: 1/125s (standard, sharp)
- **Action/demo (Scene 5)**: 1/500s - 1/1000s (freeze motion)
- **Lifestyle/ambient (Scene 4, 6)**: 1/125s - 1/250s (balanced)

---

### Step 2: Design Lighting Setup for Each Scene

**For each of the 9 scenes, define lighting configuration:**

#### **A. Lighting Type**

**Lighting Setups:**

1. **3-Point Lighting** (Studio Standard)
   - Components: Key light (main), Fill light (shadows), Rim light (separation)
   - Use for: Hero shots (Scene 1-2-3), commercial style
   - Effect: Professional, dimensional, e-commerce standard

2. **Natural Light** (Window/Ambient)
   - Components: Single window source + reflector
   - Use for: Lifestyle shots (Scene 4-5), authentic/warm feel
   - Effect: Soft, organic, relatable (Shopee/TikTok preferred)

3. **Soft Box** (Diffused Studio)
   - Components: Large diffused light source (one or two lights)
   - Use for: Minimalist shots (Scene 1), white background
   - Effect: Even illumination, no harsh shadows (ML compliance)

4. **Overhead Lighting** (Top-Down)
   - Components: Light directly above subject
   - Use for: Flat lay (Scene 3), overhead shots
   - Effect: Even coverage, no side shadows

5. **Rembrandt Lighting** (Dramatic)
   - Components: Single key light at 45°, creates triangle shadow on cheek
   - Use for: Editorial/luxury products (high-end ceramics, jewelry)
   - Effect: Artistic, dimensional (use sparingly for e-commerce)

**Selection Criteria:**
- **Hero/white bg (Scene 1)**: Soft box OR 3-point (ML compliance)
- **Angled hero (Scene 2)**: 3-point lighting (dimension + shadows)
- **Flat lay (Scene 3)**: Overhead lighting (even coverage)
- **Lifestyle (Scene 4-5)**: Natural light (authenticity)
- **Detail (Scene 7-9)**: Soft box OR macro ring light (even, no shadows)

---

#### **B. Lighting Direction**

**Light Angles & Effects:**
- **Front Lighting**: Flat, even, no shadows (white bg shots - Scene 1)
- **Side Lighting (45° - 90°)**: Creates depth, dimension, texture (Scene 2, 7)
- **Back Lighting**: Rim light, halo effect, separation (luxury products)
- **Top-Down**: Overhead, flat lay illumination (Scene 3)
- **Rembrandt (45° high)**: Dramatic, artistic (editorial only)

**Selection Criteria:**
- **Hero shot (Scene 1)**: Front lighting (eliminate shadows for ML)
- **Angled shot (Scene 2)**: 45° side lighting (reveal form)
- **Flat lay (Scene 3)**: Top-down (even coverage)
- **Lifestyle (Scene 4-5)**: Natural direction (window side/back)
- **Detail (Scene 7-9)**: Front-slight side (show texture without harsh shadows)

---

#### **C. Color Temperature (Kelvin)**

**Light Color & Mood:**
- **2700K - 3000K (Warm)**: Cozy, inviting, sunset glow
  - Use for: Lifestyle (Scene 4), home goods, comfort products

- **4000K - 5000K (Neutral)**: Balanced, natural daylight
  - Use for: Most scenes (Scene 2, 6, 7-9), true color representation

- **5500K - 6500K (Cool/Daylight)**: Crisp, clean, professional
  - Use for: Hero shots (Scene 1-3), tech products, minimalist style

- **7000K+ (Blue/Cold)**: Clinical, high-tech, medical
  - Use for: Tech gadgets (only if brand aesthetic)

**Selection Criteria:**
- **Minimalist style**: 5500K-6500K (cool, clean)
- **Lifestyle style**: 3000K-4000K (warm, inviting)
- **Commercial style**: 5000K-5500K (neutral, accurate)
- **Editorial style**: Variable (creative choice)

---

### Step 3: Validate Technical Specifications

**Run these validation checks:**

#### **Validation A: Completeness**
- ✅ All 9 scenes have camera specs (lens, aperture, ISO, shutter)
- ✅ All 9 scenes have lighting design (type, direction, color temp)
- ✅ No missing values (no "TBD" or placeholders)

#### **Validation B: Technical Accuracy**
- ✅ Aperture values exist (e.g., f/0.5 impossible, minimum ~f/1.2)
- ✅ ISO within reasonable range (100-3200 for e-commerce)
- ✅ Shutter speed safe for handhold (≥1/125s unless tripod specified)
- ✅ Lens focal length appropriate for scene type

#### **Validation C: Style Alignment**
- ✅ Camera/lighting match selected style from Phase 1:
  - **Minimalist**: Clean lighting (soft box, cool temp), sharp focus (f/8+)
  - **Lifestyle**: Natural light (warm temp), shallow DOF (f/2.8-f/4)
  - **Commercial**: 3-point lighting (neutral temp), balanced DOF (f/5.6)

#### **Validation D: Marketplace Compliance**
- ✅ **Mercado Livre** (Scene 1 main image):
  - White background lighting (soft box, front-facing)
  - Deep DOF (f/8+) for full sharpness
  - Clean ISO (100-200) for no grain

- ✅ **Shopee** (Scene 2 thumbnail, Scene 4-5 carousel):
  - Engaging angles (45°, lifestyle)
  - Moderate DOF (f/4-f/5.6) for subject pop

- ✅ **TikTok** (Scene 5 vertical):
  - Natural light preferred (authentic feel)
  - Action-ready shutter (1/500s+)

---

### Step 4: Document Specifications in Structured Format

**Create camera/lighting spec sheet for all 9 scenes:**

```markdown
## PHASE 2 OUTPUT: Camera & Lighting Specifications

### Scene 1: Front View (Hero Shot)
**Camera Specs:**
- Lens: 50mm (standard perspective)
- Aperture: f/8 (deep DOF, all sharp)
- ISO: 100 (clean, zero grain)
- Shutter: 1/125s (standard, handhold safe)

**Lighting Setup:**
- Type: Soft box (diffused, even)
- Direction: Front-facing (eliminate shadows)
- Color Temp: 5500K (cool daylight, white bg)
- Notes: Mercado Livre compliance - white bg, no shadows

---

### Scene 2: 45° Angle (Hero Shot)
**Camera Specs:**
- Lens: 50mm (standard)
- Aperture: f/5.6 (balanced DOF)
- ISO: 200 (clean)
- Shutter: 1/125s (standard)

**Lighting Setup:**
- Type: 3-point lighting (key + fill + rim)
- Direction: 45° side (reveal dimension)
- Color Temp: 5000K (neutral)
- Notes: Shopee thumbnail - engaging angle, slight shadows for depth

---

[Continue for all 9 scenes...]
```

---

## OUTPUT FORMAT

**Complete Phase 2 output structure:**

```markdown
## PHASE 2 OUTPUT: Camera & Lighting Design Complete

### Camera Specifications Summary
| Scene | Lens | Aperture | ISO | Shutter | Purpose |
|-------|------|----------|-----|---------|---------|
| 1 - Front View | 50mm | f/8 | 100 | 1/125s | ML main (white bg) |
| 2 - 45° Angle | 50mm | f/5.6 | 200 | 1/125s | Shopee thumb |
| 3 - Top-Down | 50mm | f/11 | 100 | 1/125s | Flat lay (IG) |
| 4 - Lifestyle | 35mm | f/2.8 | 400 | 1/250s | Context (Shopee) |
| 5 - Use Case | 35mm | f/4 | 800 | 1/500s | Action (TikTok) |
| 6 - Scale Ref | 85mm | f/4 | 400 | 1/125s | Size comparison |
| 7 - Texture | 100mm macro | f/5.6 | 200 | 1/125s | Material detail |
| 8 - Feature | 100mm macro | f/8 | 200 | 1/125s | Tech spec |
| 9 - Branding | 100mm macro | f/8 | 200 | 1/125s | Logo/auth |

### Lighting Setup Summary
| Scene | Type | Direction | Color Temp | Notes |
|-------|------|-----------|------------|-------|
| 1 | Soft box | Front | 5500K | ML white bg compliance |
| 2 | 3-point | 45° side | 5000K | Dimensional, Shopee |
| 3 | Overhead | Top-down | 5500K | Even flat lay |
| 4 | Natural | Window side | 3000K | Warm, cozy lifestyle |
| 5 | Natural | Ambient | 4000K | Authentic use case |
| 6 | Soft box | Slight side | 5000K | Neutral, clear scale |
| 7 | Macro ring | Front | 5500K | Even texture, no shadow |
| 8 | Soft box | Front-slight | 5500K | Feature clarity |
| 9 | Macro ring | Front | 5500K | Logo sharp, branding |

### Detailed Specifications (All 9 Scenes)

[Full spec sheet for each scene with camera + lighting + notes]

### Validation Status
- ✅ All 9 scenes have complete camera specs
- ✅ All 9 scenes have complete lighting design
- ✅ Technical accuracy verified (no impossible settings)
- ✅ Style alignment confirmed: [style name]
- ✅ Marketplace compliance checked (ML, Shopee, TikTok)
- ✅ Ready for Phase 3: AI Prompt Generation

---
**Phase 2 Duration**: [X minutes]
**Status**: ✅ COMPLETE
**Next Phase**: Phase 3 - Prompt Generation (use 30_prompt_generator_HOP.md)
```

---

## VALIDATION CHECKLIST

**Before proceeding to Phase 3, confirm:**
- ✅ 9/9 scenes have camera specs (lens, aperture, ISO, shutter)
- ✅ 9/9 scenes have lighting design (type, direction, color temp)
- ✅ No technical impossibilities (e.g., f/0.5, ISO 50000)
- ✅ Settings align with photography style from Phase 1
- ✅ Marketplace compliance met (especially ML white bg for Scene 1)
- ✅ Output formatted as structured tables + detailed specs
- ✅ Ready to generate AI prompts with technical precision

---

## ERROR HANDLING

### Common Issues & Solutions

**Issue 1: Incomplete Camera Specs**
- **Error**: "Scene 3 missing shutter speed"
- **Solution**: Add missing spec based on scene type:
  - Static product → 1/125s (standard)
  - Action/demo → 1/500s+ (freeze motion)
  - Low light → 1/60s (tripod required)

**Issue 2: Incomplete Lighting Setup**
- **Error**: "Scene 5 missing color temperature"
- **Solution**: Infer from lighting type + style:
  - Natural light + lifestyle → 3000K-4000K (warm)
  - Studio + commercial → 5000K-5500K (neutral)
  - Minimalist + soft box → 5500K-6500K (cool)

**Issue 3: Technically Impossible Settings**
- **Error**: "Scene 1 has f/0.7 aperture (impossible for 50mm standard lens)"
- **Solution**: Correct to realistic values:
  - 50mm lens: minimum f/1.2 (high-end) or f/1.8 (common)
  - Recommend: f/1.8 (shallow DOF) or f/8 (deep DOF for e-commerce)

**Issue 4: Style Misalignment**
- **Error**: "Minimalist style but Scene 1 has warm 3000K lighting"
- **Solution**: Align lighting with style requirements:
  - Minimalist → 5500K-6500K (cool, clean)
  - Lifestyle → 3000K-4000K (warm, cozy)
  - Commercial → 5000K-5500K (neutral, accurate)

**Issue 5: Marketplace Non-Compliance**
- **Error**: "Mercado Livre main image (Scene 1) has f/2.8 (shallow DOF + potential bg blur)"
- **Solution**: Enforce ML rules:
  - Aperture: f/8+ (deep DOF, all sharp)
  - Lighting: Soft box, front-facing (no shadows)
  - Background: White, evenly lit (no gradients)

---

## EXAMPLES

### Example 1: Minimalist Ceramic Mug

**Input (from Phase 1):**
- Product: Ceramic mug (matte white, wooden handle)
- Style: Minimalist (white bg, soft lighting, clean)
- Scenes: 9-scene grid defined

**Output:**

```markdown
## PHASE 2 OUTPUT: Camera & Lighting Design

### Scene 1: Front View (ML Main Image)
**Camera**: 50mm, f/8, ISO 100, 1/125s
**Lighting**: Soft box (front, 5500K cool)
**Notes**: ML compliance - white bg, deep DOF, zero shadows

### Scene 2: 45° Angle (Shopee Thumb)
**Camera**: 50mm, f/5.6, ISO 200, 1/125s
**Lighting**: 3-point (45° side, 5000K neutral)
**Notes**: Dimensional reveal, handle curve visible

### Scene 3: Top-Down (Flat Lay)
**Camera**: 50mm, f/11, ISO 100, 1/125s
**Lighting**: Overhead (top-down, 5500K cool)
**Notes**: Opening + handle visible, Instagram-ready

### Scene 4: Lifestyle (Desk Context)
**Camera**: 35mm, f/2.8, ISO 400, 1/250s
**Lighting**: Natural (window side, 3000K warm)
**Notes**: Cozy morning vibe, background blur (book, table)

### Scene 5: Use Case (Hand Holding)
**Camera**: 85mm, f/4, ISO 800, 1/250s
**Lighting**: Natural (ambient, 4000K neutral)
**Notes**: Ergonomics, steam visible (if applicable)

### Scene 6: Scale Reference (Phone Comparison)
**Camera**: 50mm, f/5.6, ISO 400, 1/125s
**Lighting**: Soft box (slight side, 5000K neutral)
**Notes**: Size clarity, both objects sharp

### Scene 7: Texture (Ceramic Surface)
**Camera**: 100mm macro, f/5.6, ISO 200, 1/125s
**Lighting**: Macro ring light (front, 5500K cool)
**Notes**: Matte finish detail, no harsh shadows

### Scene 8: Feature (Wooden Handle Grain)
**Camera**: 100mm macro, f/8, ISO 200, 1/125s
**Lighting**: Soft box (front-slight side, 5500K cool)
**Notes**: Wood texture + metal attachment visible

### Scene 9: Branding (Bottom Stamp)
**Camera**: 100mm macro, f/8, ISO 200, 1/125s
**Lighting**: Macro ring light (front, 5500K cool)
**Notes**: "Hygge Home Co." logo sharp, authenticity

---

### Validation Status
- ✅ 9/9 scenes complete (camera + lighting)
- ✅ Style: Minimalist (cool lighting, deep DOF for sharpness)
- ✅ ML compliance: Scene 1 (white bg, f/8, soft box front)
- ✅ Technical accuracy: All settings realistic
- ✅ Ready for Phase 3: AI Prompt Generation

**Phase 2 Duration**: 4 minutes
**Status**: ✅ COMPLETE
```

---

### Example 2: Lifestyle Wireless Earbuds

**Input (from Phase 1):**
- Product: Wireless earbuds (LED case, rose gold)
- Style: Lifestyle (natural light, contextual, warm)
- Scenes: 9-scene grid defined

**Output:**

```markdown
## PHASE 2 OUTPUT: Camera & Lighting Design

### Scene 1: Case Front (Shopee Main)
**Camera**: 50mm, f/5.6, ISO 200, 1/125s
**Lighting**: Soft box (front, 5000K neutral)
**Notes**: LED indicator visible, clean bg

### Scene 2: Case Open 45° (Shopee Thumb)
**Camera**: 50mm, f/4, ISO 200, 1/125s
**Lighting**: 3-point (45° side, 5000K neutral)
**Notes**: Earbuds in case visible, engaging angle

### Scene 3: Flat Lay (Full Kit)
**Camera**: 50mm, f/8, ISO 100, 1/125s
**Lighting**: Overhead (top-down, 5500K cool)
**Notes**: Case open + earbuds out, Instagram

### Scene 4: Gym Bag Context (Lifestyle)
**Camera**: 35mm, f/2.8, ISO 800, 1/250s
**Lighting**: Natural (window side, 3500K warm)
**Notes**: Active lifestyle, aspirational, Shopee carousel

### Scene 5: Person Wearing (Use Case)
**Camera**: 85mm, f/2.8, ISO 1600, 1/500s
**Lighting**: Natural (ambient back, 4000K neutral)
**Notes**: Profile shot, show fit, TikTok vertical 9:16

### Scene 6: Credit Card Scale (Size)
**Camera**: 50mm, f/5.6, ISO 400, 1/125s
**Lighting**: Soft box (slight side, 5000K neutral)
**Notes**: Pocket-friendly, both sharp

### Scene 7: Rose Gold Finish (Texture)
**Camera**: 100mm macro, f/5.6, ISO 200, 1/125s
**Lighting**: Macro ring (front, 5500K cool)
**Notes**: Premium feel, reflections visible

### Scene 8: LED Indicator (Feature)
**Camera**: 100mm macro, f/8, ISO 200, 1/125s
**Lighting**: Soft box (front, 5500K cool)
**Notes**: Charging status, tech feature

### Scene 9: Inside Case Logo (Branding)
**Camera**: 100mm macro, f/8, ISO 200, 1/125s
**Lighting**: Macro ring (front, 5500K cool)
**Notes**: Model number, authenticity

---

### Validation Status
- ✅ 9/9 scenes complete
- ✅ Style: Lifestyle (natural light, warm tones, moderate DOF)
- ✅ Shopee optimized: Scenes 2, 4, 5 (carousel + thumb)
- ✅ TikTok ready: Scene 5 (vertical, action)
- ✅ Ready for Phase 3

**Phase 2 Duration**: 5 minutes
**Status**: ✅ COMPLETE
```

---

## NOTES FOR LLM EXECUTION

1. **Camera/Lighting Pairing**: Certain camera settings demand specific lighting:
   - **Low ISO (100-200)** → Requires strong lighting (studio/soft box)
   - **High ISO (800+)** → Natural/ambient light scenarios (lifestyle)
   - **Wide aperture (f/2.8)** → Controlled lighting (avoid overexposure)
   - **Narrow aperture (f/8+)** → More light needed (longer exposure or brighter lights)

2. **Marketplace Priority Mapping**:
   - **Mercado Livre**: Scene 1 must comply (white bg, deep DOF, clean ISO)
   - **Shopee**: Scenes 2, 4, 5 (varied, engaging, carousel-ready)
   - **TikTok**: Scene 5 (vertical, natural light, action-oriented)

3. **Style-Specific Defaults**:
   - **Minimalist**: f/8+, ISO 100-200, 5500K+, soft box/front lighting
   - **Lifestyle**: f/2.8-f/4, ISO 400-800, 3000-4000K, natural light
   - **Commercial**: f/5.6, ISO 200-400, 5000K, 3-point lighting
   - **Editorial**: Variable (creative freedom, artistic choices)

4. **Lens Choice by Scene Type**:
   - **Hero (1-3)**: 50mm standard (no distortion, natural)
   - **Context (4-6)**: 35mm wide (environment) OR 85mm portrait (human interaction)
   - **Detail (7-9)**: 100mm macro (magnification, texture focus)

5. **Lighting Efficiency**: Reuse lighting setups where possible to reduce production time:
   - Scenes 1-3: Studio lighting (same setup, different angles)
   - Scenes 4-5: Natural light (same window, different positions)
   - Scenes 7-9: Macro ring light (same setup, different focus points)

---

**End of 20_camera_designer_HOP.md**
