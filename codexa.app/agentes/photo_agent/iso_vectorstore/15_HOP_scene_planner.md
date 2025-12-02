# 10_scene_planner_HOP.md | photo_agent - Input Processing & Scene Planning

**Version**: 2.0.0
**Type**: HOP (Higher-Order Prompt)
**Status**: Integrated with ADW Workflow v2.0.0
**Last Updated**: 2025-11-17
**Integrated with**: workflows/100_ADW_RUN_PHOTO.md

**Purpose**: Parse product/style input and design 9-scene photography grid (3x3 matrix)
**Estimated Duration**: 2-5 minutes

---

## INPUT_CONTRACT

**Required**:
- `$subject` (string): Product description (e.g., "ceramic mug 350ml")
- Type: String, non-empty, descriptive

**Optional**:
- `$style` (enum): Photography style → Default: "commercial"
- `$brand_guidelines` (object): {colors, personality, marketplace}
- Type: JSON object

**Validation**:
- ✅ Subject must be non-empty
- ✅ Style must exist in config OR default to "commercial"

---

## OUTPUT_CONTRACT

**Primary**:
- `$scene_grid` (object): 9-scene grid definition
  - Structure: `{ scene_1: {angle, purpose, marketplace}, ..., scene_9: {...} }`
  - Format: JSON object

**Secondary**:
- `$loaded_configs` (array): Loaded configuration files
  - Files: [photography_styles.json, camera_profiles.json, pnl_triggers.json]

**Consumed By**: Phase 2 (Camera Designer HOP)

---

## OBJECTIVE

Parse user input to extract product subject and photography style, then design a strategic 9-scene grid (3x3 matrix) optimized for e-commerce marketplaces (Mercado Livre, Shopee, TikTok). Load all required configuration files to enable subsequent phases.

---

## CONTEXT REQUIREMENTS

**Before executing this prompt, ensure:**
- Access to `config/camera_profiles.json` (camera specifications database)
- Access to `config/photography_styles.json` (style definitions: minimalist, lifestyle, commercial, etc.)
- Access to `config/pnl_triggers.json` (psychological triggers for visual persuasion)
- User has provided: `subject` (product description) and `style` (photography approach)
- LLM model: GPT-4+ or Claude Sonnet 4+ (required for multi-modal understanding)

---

## INSTRUCTIONS

### Step 1: Parse User Input

**Extract the following from user request:**
1. **Subject (Product)**:
   - Product type (e.g., "ceramic mug", "wireless earbuds", "yoga mat")
   - Key features (e.g., "matte finish", "LED indicators", "eco-friendly material")
   - Physical attributes (size, color, texture, material)

2. **Style (Photography Approach)**:
   - Declared style (e.g., "minimalist", "lifestyle", "commercial", "editorial")
   - If not specified → default to "commercial"
   - Validate against `config/photography_styles.json`

3. **Brand Guidelines (Optional)**:
   - Brand colors (hex codes or descriptors)
   - Brand personality (modern, playful, luxury, eco-conscious)
   - Specific marketplace targets (Mercado Livre, Shopee, TikTok)

**Validation:**
- ✅ Subject is clearly defined (not vague)
- ✅ Style exists in config OR defaulted to "commercial"
- ✅ Brand guidelines captured (if provided)

**Error Handling:**
- If subject missing → **HALT**: "No product/subject specified. Please provide product description to generate photo prompts. Example: 'subject=ceramic mug, style=minimalist'"
- If style invalid → **WARN**: "Style '[X]' not found in config. Available styles: [list from config]. Defaulting to 'commercial'."

---

### Step 2: Design 9-Scene Grid (3x3 Matrix)

**Define 9 distinct scenes organized in a strategic grid:**

#### **Row 1: Hero Shots (Primary Product Views)**
1. **Scene 1 - Front View**:
   - Angle: Straight-on (0° horizontal)
   - Purpose: Show main product face/branding
   - Marketplace: Mercado Livre main image (white bg requirement)

2. **Scene 2 - 45° Angle**:
   - Angle: 45° from front-right
   - Purpose: Reveal depth and dimension
   - Marketplace: Shopee thumbnail (engaging angle)

3. **Scene 3 - Top-Down**:
   - Angle: 90° overhead (flat lay)
   - Purpose: Show full layout and scale
   - Marketplace: Instagram/Pinterest optimization

#### **Row 2: Context Shots (Lifestyle & Use Case)**
4. **Scene 4 - Lifestyle Context**:
   - Setting: Product in natural environment (e.g., mug on desk, earbuds in hand)
   - Purpose: Emotional connection + relatability
   - Marketplace: Shopee lifestyle images (9-image carousel)

5. **Scene 5 - Use Case Demonstration**:
   - Action: Product being used (e.g., pouring coffee, wearing earbuds)
   - Purpose: Show functionality and benefits
   - Marketplace: TikTok video stills (vertical 9:16)

6. **Scene 6 - Scale Reference**:
   - Comparison: Product next to familiar object (coin, hand, ruler)
   - Purpose: Clarify size and dimensions
   - Marketplace: Mercado Livre detail images

#### **Row 3: Detail Shots (Features & Craftsmanship)**
7. **Scene 7 - Texture Close-Up**:
   - Focus: Material surface (ceramic glaze, fabric weave, metal finish)
   - Purpose: Highlight quality and craftsmanship
   - Marketplace: All platforms (trust-building)

8. **Scene 8 - Feature Detail**:
   - Focus: Key product feature (button, logo, stitching, LED indicator)
   - Purpose: Technical specification visualization
   - Marketplace: Mercado Livre spec compliance

9. **Scene 9 - Branding/Logo**:
   - Focus: Brand mark, packaging, or product label
   - Purpose: Brand recognition and authenticity
   - Marketplace: All platforms (anti-counterfeit)

---

### Step 3: Load Configuration Files

**Read and store the following configs:**

1. **`config/camera_profiles.json`**:
   ```json
   {
     "hero_shot": {"lens": "50mm", "aperture": "f/2.8", "iso": 100},
     "lifestyle": {"lens": "35mm", "aperture": "f/4", "iso": 400},
     "macro_detail": {"lens": "100mm macro", "aperture": "f/5.6", "iso": 200}
   }
   ```
   - Load all profiles for Phase 2 (camera design)

2. **`config/photography_styles.json`**:
   ```json
   {
     "minimalist": {"bg_color": "white", "props": "none", "lighting": "soft"},
     "lifestyle": {"bg_color": "natural", "props": "contextual", "lighting": "ambient"},
     "commercial": {"bg_color": "gradient", "props": "minimal", "lighting": "3-point"}
   }
   ```
   - Validate user's selected style exists

3. **`config/pnl_triggers.json`**:
   ```json
   {
     "trust": ["professional", "clean", "sharp", "high-quality"],
     "desire": ["luxurious", "exclusive", "premium", "elegant"],
     "urgency": ["dynamic", "energetic", "bold", "vivid"]
   }
   ```
   - Store for Phase 3 (prompt generation)

**Validation:**
- ✅ All 3 config files loaded successfully
- ✅ Selected style found in `photography_styles.json`
- ✅ Camera profiles available for all scene types

**Error Handling:**
- If config file missing → **HALT**: "Configuration file '[filename]' not found. Required for workflow execution. Check: agentes/photo_agent/config/"
- If config file malformed → **HALT**: "Cannot parse '[filename]'. JSON syntax error at line [X]. Fix: [error details]"

---

### Step 4: Validate Scene Grid

**Perform final validation:**
1. **Scene count = 9** (exactly, no more/less)
2. **Each scene has**:
   - Scene number (1-9)
   - Scene name (descriptive)
   - Angle/perspective defined
   - Purpose/marketplace target clear
3. **Grid structure**:
   - Row 1: Hero shots (3 scenes)
   - Row 2: Context shots (3 scenes)
   - Row 3: Detail shots (3 scenes)

**Validation:**
- ✅ Exactly 9 scenes defined
- ✅ Each scene has all required attributes
- ✅ Grid follows 3x3 structure (Hero → Context → Detail)

**Error Handling:**
- If scene_count ≠ 9 → **RETRY**: "Scene count: [X]. Must be exactly 9 (3x3 grid). Missing scenes: [list]. Add scenes for: [suggested shots]."
- If scene missing attribute → **RETRY**: "Scene [X] incomplete. Missing: [attributes]. Add: angle, purpose, marketplace target."

---

## OUTPUT FORMAT

**Structured output for next phases:**

```markdown
## PHASE 1 OUTPUT: Scene Grid Defined

### Input Summary
- **Subject**: [product name/type]
- **Style**: [photography style from config]
- **Brand Guidelines**: [if provided, else "None specified - using defaults"]
- **Target Marketplaces**: [Mercado Livre, Shopee, TikTok, etc.]

### 9-Scene Grid (3x3 Matrix)

#### Row 1: Hero Shots
1. **Scene 1 - Front View**: [angle], [purpose], [marketplace]
2. **Scene 2 - 45° Angle**: [angle], [purpose], [marketplace]
3. **Scene 3 - Top-Down**: [angle], [purpose], [marketplace]

#### Row 2: Context Shots
4. **Scene 4 - Lifestyle Context**: [setting], [purpose], [marketplace]
5. **Scene 5 - Use Case Demo**: [action], [purpose], [marketplace]
6. **Scene 6 - Scale Reference**: [comparison], [purpose], [marketplace]

#### Row 3: Detail Shots
7. **Scene 7 - Texture Close-Up**: [focus], [purpose], [marketplace]
8. **Scene 8 - Feature Detail**: [focus], [purpose], [marketplace]
9. **Scene 9 - Branding/Logo**: [focus], [purpose], [marketplace]

### Configuration Files Loaded
- ✅ `config/camera_profiles.json` (X profiles loaded)
- ✅ `config/photography_styles.json` (Y styles available)
- ✅ `config/pnl_triggers.json` (Z trigger categories loaded)

### Validation Status
- ✅ Scene count: 9/9
- ✅ All scenes have required attributes
- ✅ Grid structure: 3x3 (Hero → Context → Detail)
- ✅ Style validated: [style name]
- ✅ Ready for Phase 2: Camera & Lighting Design

---
**Phase 1 Duration**: [X minutes]
**Status**: ✅ COMPLETE
**Next Phase**: Phase 2 - Camera & Lighting Design (use 20_camera_designer_HOP.md)
```

---

## VALIDATION CHECKLIST

**Before proceeding to Phase 2, confirm:**
- ✅ Subject extracted and clearly defined
- ✅ Style validated (exists in config or defaulted)
- ✅ 9-scene grid designed (3x3: Hero → Context → Detail)
- ✅ All 3 config files loaded successfully
- ✅ Each scene has: number, name, angle, purpose, marketplace target
- ✅ Grid structure follows best practices (strategic shot variety)
- ✅ Output formatted correctly (readable markdown)

---

## ERROR HANDLING

### Common Issues & Solutions

**Issue 1: Vague Subject**
- **Example**: "subject=product"
- **Error**: "Subject too vague. Cannot design specific scenes."
- **Solution**: Ask user for specific product details: "Please specify product type and key features. Example: 'ceramic coffee mug with matte black finish and gold rim'"

**Issue 2: Style Not in Config**
- **Example**: "style=artistic"
- **Warning**: "Style 'artistic' not found in config. Available: minimalist, lifestyle, commercial, editorial, studio. Defaulting to 'commercial'."
- **Solution**: Continue with default style OR ask user to choose from available options

**Issue 3: Config File Missing**
- **Example**: `camera_profiles.json` not found
- **Error**: "Critical file missing: config/camera_profiles.json. Cannot proceed without camera specifications."
- **Solution**: HALT workflow and instruct: "Create missing config file at: agentes/photo_agent/config/camera_profiles.json (use template from other agents)"

**Issue 4: Scene Count Error**
- **Example**: Only 7 scenes defined
- **Error**: "Scene count: 7. Must be exactly 9 (3x3 grid). Missing: 2 scenes."
- **Solution**: Auto-generate missing scenes: "Adding Scene 8 (Feature Detail) and Scene 9 (Branding/Logo) to complete grid."

---

## EXAMPLES

### Example 1: Minimalist Product Photography

**Input:**
```
subject = "Ceramic coffee mug with matte white finish and wooden handle"
style = "minimalist"
brand = "Hygge Home Co."
marketplaces = ["Mercado Livre", "Shopee"]
```

**Output:**
```markdown
## PHASE 1 OUTPUT: Scene Grid Defined

### Input Summary
- **Subject**: Ceramic coffee mug (matte white, wooden handle)
- **Style**: minimalist (white bg, no props, soft lighting)
- **Brand Guidelines**: Hygge Home Co. (warm, Scandinavian aesthetic)
- **Target Marketplaces**: Mercado Livre (main), Shopee (secondary)

### 9-Scene Grid (3x3 Matrix)

#### Row 1: Hero Shots
1. **Scene 1 - Front View**: 0° straight-on, show mug face + handle, Mercado Livre main (white bg)
2. **Scene 2 - 45° Angle**: 45° from right, reveal depth + handle curve, Shopee thumbnail
3. **Scene 3 - Top-Down**: 90° overhead, show opening + handle from above, Instagram

#### Row 2: Context Shots
4. **Scene 4 - Lifestyle Context**: Mug on wooden table with book, cozy morning vibe, Shopee carousel
5. **Scene 5 - Use Case Demo**: Hand holding mug (steam visible), show ergonomics, TikTok vertical
6. **Scene 6 - Scale Reference**: Mug next to smartphone (size comparison), clarify capacity, ML detail

#### Row 3: Detail Shots
7. **Scene 7 - Texture Close-Up**: Matte ceramic surface macro, show quality finish, trust-building
8. **Scene 8 - Feature Detail**: Wooden handle grain + metal attachment, craftsmanship, spec compliance
9. **Scene 9 - Branding/Logo**: "Hygge Home Co." stamp on bottom, authenticity, anti-counterfeit

### Configuration Files Loaded
- ✅ `config/camera_profiles.json` (5 profiles: hero_shot, lifestyle, macro_detail, overhead, product_demo)
- ✅ `config/photography_styles.json` (6 styles available: minimalist selected)
- ✅ `config/pnl_triggers.json` (4 categories: trust, desire, urgency, exclusivity)

### Validation Status
- ✅ Scene count: 9/9
- ✅ All scenes have required attributes
- ✅ Grid structure: 3x3 (Hero → Context → Detail)
- ✅ Style validated: minimalist
- ✅ Ready for Phase 2: Camera & Lighting Design

---
**Phase 1 Duration**: 3 minutes
**Status**: ✅ COMPLETE
**Next Phase**: Phase 2 - Camera & Lighting Design (use 20_camera_designer_HOP.md)
```

---

### Example 2: Lifestyle Product Photography (Fast Fashion)

**Input:**
```
subject = "Wireless earbuds with LED charging case, rose gold finish"
style = "lifestyle"
brand = None
marketplaces = ["Shopee", "TikTok"]
```

**Output:**
```markdown
## PHASE 1 OUTPUT: Scene Grid Defined

### Input Summary
- **Subject**: Wireless earbuds (LED charging case, rose gold)
- **Style**: lifestyle (natural bg, contextual props, ambient lighting)
- **Brand Guidelines**: None specified - using generic e-commerce best practices
- **Target Marketplaces**: Shopee (primary), TikTok (video stills)

### 9-Scene Grid (3x3 Matrix)

#### Row 1: Hero Shots
1. **Scene 1 - Front View**: Case closed, front face + LED indicator, Shopee main image
2. **Scene 2 - 45° Angle**: Case open (earbuds visible), show functionality, Shopee thumbnail
3. **Scene 3 - Top-Down**: Case open + earbuds out (flat lay), full kit view, Instagram

#### Row 2: Context Shots
4. **Scene 4 - Lifestyle Context**: Earbuds on gym bag (active lifestyle), aspirational, Shopee carousel
5. **Scene 5 - Use Case Demo**: Person wearing earbuds (profile shot), show fit, TikTok vertical 9:16
6. **Scene 6 - Scale Reference**: Case next to credit card (size comparison), pocket-friendly, Shopee detail

#### Row 3: Detail Shots
7. **Scene 7 - Texture Close-Up**: Rose gold finish macro (reflections), premium feel, trust-building
8. **Scene 8 - Feature Detail**: LED indicator (charging status), tech feature, spec compliance
9. **Scene 9 - Branding/Logo**: Inside case (model number/logo), authenticity, warranty verification

### Configuration Files Loaded
- ✅ `config/camera_profiles.json` (5 profiles loaded)
- ✅ `config/photography_styles.json` (lifestyle style selected)
- ✅ `config/pnl_triggers.json` (4 categories loaded)

### Validation Status
- ✅ Scene count: 9/9
- ✅ All scenes have required attributes
- ✅ Grid structure: 3x3 (Hero → Context → Detail)
- ✅ Style validated: lifestyle
- ✅ Ready for Phase 2: Camera & Lighting Design

---
**Phase 1 Duration**: 2.5 minutes
**Status**: ✅ COMPLETE
**Next Phase**: Phase 2 - Camera & Lighting Design (use 20_camera_designer_HOP.md)
```

---

## NOTES FOR LLM EXECUTION

1. **Flexibility**: If user provides partial input (e.g., only subject), infer reasonable defaults for style and brand based on product category.

2. **Marketplace Optimization**: Prioritize scene types based on target marketplace:
   - **Mercado Livre**: Hero shots with white bg (Row 1) + detail shots (Row 3)
   - **Shopee**: Lifestyle context shots (Row 2) + engaging thumbnails (Scene 2)
   - **TikTok**: Vertical use cases (Scene 5) + dynamic angles (Scene 2)

3. **Scene Adaptability**: The 3x3 grid structure is a framework. Adapt specific scenes to product type:
   - **Fashion**: Add "model wearing" scenes in Row 2
   - **Electronics**: Add "port/button close-ups" in Row 3
   - **Food**: Add "ingredient spread" in Row 2

4. **Config File Defaults**: If config files are missing, proceed with these defaults:
   - **Camera Profiles**: hero_shot (50mm f/2.8), lifestyle (35mm f/4), macro (100mm f/5.6)
   - **Styles**: minimalist (white bg), lifestyle (natural bg), commercial (gradient bg)
   - **PNL Triggers**: trust (professional, clean), desire (luxurious, premium)

5. **Duration Estimation**: Phase 1 typically takes 2-5 minutes depending on:
   - Input clarity (clear = 2min, vague = 5min)
   - Config availability (pre-loaded = faster)
   - LLM model speed (GPT-4 Turbo faster than standard GPT-4)

---

**End of 10_scene_planner_HOP.md**
