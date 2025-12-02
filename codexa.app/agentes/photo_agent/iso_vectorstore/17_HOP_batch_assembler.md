<!-- iso_vectorstore -->
<!--
  Source: 50_batch_assembler_HOP.md
  Agent: photo_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 50_batch_assembler_HOP.md | photo_agent - Batch Assembly & QA

**Version**: 2.0.0
**Type**: HOP (Higher-Order Prompt)
**Status**: Integrated with ADW Workflow v2.0.0
**Last Updated**: 2025-11-17
**Integrated with**: workflows/100_ADW_RUN_PHOTO.md

**Purpose**: Compile 9 individual prompts + 1 batch block into Trinity format (.md + .llm.json + .meta.json)
**Input**: Phase 4 output (validated 9 AI prompts + quality score ≥7.0)
**Output**: Trinity files (.md human-readable, .llm.json structured, .meta.json metadata)
**Estimated Duration**: 2-5 minutes

---

## OBJECTIVE

Assemble all 9 validated AI prompts into a complete deliverable package with:
1. **9 Individual Prompts**: Separate code blocks for single-image generation
2. **1 Batch Block**: All 9 prompts concatenated for bulk processing
3. **Trinity Output Format**: .md (human-readable), .llm.json (structured data), .meta.json (workflow metadata)
4. **Final QA**: Verify completeness, validate JSON syntax, ensure usability

---

## CONTEXT REQUIREMENTS

**Before executing this prompt, ensure:**
- Phase 4 completed: All 9 prompts validated (quality score ≥7.0/10)
- Brand consistency confirmed
- Marketplace compliance verified (ML, Shopee, TikTok)
- Technical requirements met (resolution, camera specs, lighting)
- No critical blockers from validation phase

---

## INSTRUCTIONS

### Step 1: Compile 9 Individual Prompts

**Organize all prompts with clear scene headers and copy-paste ready format:**

````markdown
## 📸 INDIVIDUAL PROMPTS (Scenes 1-9)
*Use these for single-image generation in Midjourney, DALL-E, or Stable Diffusion*

---

### Scene 1: Front View (Hero Shot - Mercado Livre Main Image)
**Purpose**: Main listing image (white bg, ML compliance)
**Platform**: Mercado Livre
**Format**: Square (1:1) or standard (4:3)

```
[Full 80+ word AI prompt for Scene 1]
```

**Camera**: 50mm, f/8, ISO 100, 1/125s
**Lighting**: Soft box, front, 5500K cool daylight
**Marketplace**: Mercado Livre compliant (white bg, no watermarks)

---

### Scene 2: 45° Angle (Hero Shot - Shopee Thumbnail)
**Purpose**: Engaging angled view (dimensional depth)
**Platform**: Shopee
**Format**: Square (1:1)

```
[Full 80+ word AI prompt for Scene 2]
```

**Camera**: 50mm, f/5.6, ISO 200, 1/125s
**Lighting**: 3-point, 45° side, 5000K neutral
**Marketplace**: Shopee thumbnail optimized

---

[Continue for all 9 scenes with same structure...]

---

### Scene 9: Branding/Logo (Authentication Shot)
**Purpose**: Brand authenticity and anti-counterfeit
**Platform**: All marketplaces
**Format**: Square (1:1) or close-up crop

```
[Full 80+ word AI prompt for Scene 9]
```

**Camera**: 100mm macro, f/8, ISO 200, 1/125s
**Lighting**: Macro ring, front, 5500K cool
**Marketplace**: Universal (trust-building)
````

**Validation for Step 1:**
- ✅ All 9 scenes present (no missing prompts)
- ✅ Each scene has: purpose, platform, format, prompt, camera, lighting, marketplace
- ✅ Prompts wrapped in ```code blocks``` for easy copy-paste
- ✅ Clear visual separation (--- dividers between scenes)

---

### Step 2: Generate Batch Block (All 9 Concatenated)

**Create a single concatenated prompt for bulk/batch processing:**

**Use Case**: Some AI generators support batch processing (generate all 9 images from one prompt)

**Format**: Concatenate all 9 prompts with clear separators

````markdown
## 🎬 BATCH BLOCK (All 9 Scenes Combined)
*Copy this entire block for batch processing in AI image generators that support multi-prompt input*

```
---SCENE 1: FRONT VIEW---
[Scene 1 full prompt text]

---SCENE 2: 45° ANGLE---
[Scene 2 full prompt text]

---SCENE 3: TOP-DOWN---
[Scene 3 full prompt text]

---SCENE 4: LIFESTYLE CONTEXT---
[Scene 4 full prompt text]

---SCENE 5: USE CASE DEMO---
[Scene 5 full prompt text]

---SCENE 6: SCALE REFERENCE---
[Scene 6 full prompt text]

---SCENE 7: TEXTURE CLOSE-UP---
[Scene 7 full prompt text]

---SCENE 8: FEATURE DETAIL---
[Scene 8 full prompt text]

---SCENE 9: BRANDING/LOGO---
[Scene 9 full prompt text]
```

**Batch Instructions:**
1. Copy the entire code block above
2. Use AI platforms with batch support (ComfyUI, Automatic1111, API batch endpoints)
3. Each scene separator (---SCENE X---) will trigger new image generation
4. Expect 9 output images (one per scene)
5. Total estimated time: 5-15 minutes (depending on AI service)
````

**Validation for Step 2:**
- ✅ All 9 prompts concatenated in correct order (1→9)
- ✅ Clear separators between scenes (`---SCENE X---`)
- ✅ Batch block wrapped in single ```code block```
- ✅ Usage instructions provided (how to use batch block)

---

### Step 3: Assemble Trinity Output (.md + .llm.json + .meta.json)

**Create three interconnected files for complete deliverable:**

#### **File 1: .md (Human-Readable Markdown)**

**Purpose**: Primary human-readable output with all prompts, usage guide, metadata

**Structure:**

````markdown
# 📸 AI Product Photography Prompts | [Product Name]

**Generated**: [Date/Time]
**Product**: [Product description]
**Style**: [Photography style]
**Quality Score**: [X.X/10]
**Marketplace Targets**: Mercado Livre, Shopee, TikTok
**Total Scenes**: 9 (3x3 grid: Hero → Context → Detail)

---

## 📋 QUICK REFERENCE

| Scene | Type | Platform | Format | Word Count |
|-------|------|----------|--------|------------|
| 1 | Front View | Mercado Livre | 1:1 | 112 |
| 2 | 45° Angle | Shopee | 1:1 | 98 |
| 3 | Top-Down | Instagram | 1:1 | 105 |
| 4 | Lifestyle | Shopee | 1:1 | 115 |
| 5 | Use Case | TikTok | 9:16 | 121 |
| 6 | Scale Ref | Mercado Livre | 1:1 | 94 |
| 7 | Texture | Universal | 1:1 | 102 |
| 8 | Feature | Universal | 1:1 | 108 |
| 9 | Branding | Universal | 1:1 | 96 |

**Total Prompts**: 9 individual + 1 batch block
**Total Word Count**: 1,051 words (avg 117 words/prompt)

---

## 📸 INDIVIDUAL PROMPTS (Scenes 1-9)
[Insert all 9 individual prompts from Step 1]

---

## 🎬 BATCH BLOCK (All 9 Combined)
[Insert batch block from Step 2]

---

## 🛠️ USAGE GUIDE

### For Midjourney Users
1. Copy individual scene prompts (from "Individual Prompts" section)
2. Paste into Midjourney Discord: `/imagine prompt: [paste prompt]`
3. Add parameters: `--ar 1:1` (square) or `--ar 9:16` (vertical for Scene 5)
4. Optional: `--quality 2` (higher quality), `--style raw` (photographic)

### For DALL-E 3 Users (ChatGPT/API)
1. Copy individual scene prompts
2. Paste into ChatGPT: "Generate this image: [paste prompt]"
3. DALL-E auto-formats to square (1024x1024) or landscape (1792x1024)
4. For Scene 5 (TikTok): Request portrait format (1024x1792)

### For Stable Diffusion Users (Local/Cloud)
1. Copy individual scene prompts
2. Use prompt as positive prompt in WebUI (Automatic1111, ComfyUI, etc.)
3. Recommended settings:
   - Model: Realistic Vision, Dreamshaper, or product photography fine-tune
   - Steps: 30-50
   - CFG Scale: 7-9
   - Sampler: DPM++ 2M Karras or Euler a
4. For Scene 5 (vertical): Set resolution to 512x912 or 768x1368

### For Batch Processing
1. Use batch block (all 9 scenes concatenated)
2. Platforms: ComfyUI (batch queue), Automatic1111 (txt2img batch), API batch endpoints
3. Process all 9 images in one run (faster for complete sets)

---

## 📊 QUALITY ASSURANCE

### Validation Checklist
- ✅ 9 individual prompts (all ≥80 words)
- ✅ 1 batch block (all 9 concatenated)
- ✅ Brand consistency (colors, style, personality)
- ✅ Marketplace compliance (ML white bg, Shopee lifestyle, TikTok vertical)
- ✅ Technical requirements (camera specs, lighting, resolution)
- ✅ Quality score: [X.X/10] (≥7.0 minimum)

### Post-Generation Tips
1. **Mercado Livre (Scene 1)**: Verify white background (#FFFFFF), no shadows
2. **Shopee (Scenes 2,4,5)**: Check product visibility (50%+ of frame)
3. **TikTok (Scene 5)**: Confirm vertical format (9:16), bright/engaging
4. **Resolution**: Upscale if needed (min 1200px for ML, 1080px for TikTok)
5. **File Size**: Compress if >5MB (use TinyPNG, ImageOptim, or Photoshop export)

---

## 📝 WORKFLOW METADATA

**Agent**: photo_agent v2.0.0
**Workflow**: 100_ADW_RUN_PHOTO
**Phases Executed**:
1. Phase 1: Scene Planning (9-scene grid designed)
2. Phase 2: Camera & Lighting Design (specs for all 9 scenes)
3. Phase 3: AI Prompt Generation (9 prompts created)
4. Phase 4: Brand & Compliance Validation (quality score: [X.X/10])
5. Phase 5: Batch Assembly & QA (Trinity output generated)

**Duration**: [Total minutes]
**Quality Score**: [X.X/10]
**Status**: ✅ Complete

---

**Generated by**: EcomLM CODEXA photo_agent
**Documentation**: agentes/photo_agent/README.md
**Workflow Source**: agentes/photo_agent/workflows/100_ADW_RUN_PHOTO.md
````

---

#### **File 2: .llm.json (Structured Data for LLMs)**

**Purpose**: Machine-readable structured data for programmatic access, integrations, APIs

**JSON Structure:**

```json
{
  "metadata": {
    "agent": "photo_agent",
    "workflow": "100_ADW_RUN_PHOTO",
    "version": "2.0.0",
    "generated_at": "2025-11-17T15:30:00Z",
    "duration_minutes": 18,
    "quality_score": 8.9
  },
  "product": {
    "name": "Ceramic Coffee Mug",
    "description": "Matte white ceramic mug with natural wooden handle and gold rim accent",
    "category": "Home & Kitchen",
    "style": "minimalist",
    "brand": {
      "name": "Hygge Home Co.",
      "colors": ["#FFFFFF", "natural wood", "#D4AF37"],
      "personality": "Scandinavian, minimalist, professional"
    }
  },
  "scene_grid": {
    "total_scenes": 9,
    "structure": "3x3",
    "rows": {
      "row_1": "Hero Shots (Front, 45°, Top-Down)",
      "row_2": "Context Shots (Lifestyle, Use Case, Scale)",
      "row_3": "Detail Shots (Texture, Feature, Branding)"
    }
  },
  "prompts": [
    {
      "scene_id": 1,
      "scene_name": "Front View",
      "scene_type": "hero",
      "marketplace": "Mercado Livre",
      "format": "1:1 square",
      "word_count": 112,
      "prompt_text": "[Full Scene 1 prompt]",
      "camera_specs": {
        "lens": "50mm",
        "aperture": "f/8",
        "iso": 100,
        "shutter_speed": "1/125s"
      },
      "lighting_setup": {
        "type": "soft box",
        "direction": "front",
        "color_temp": "5500K"
      },
      "quality_score": {
        "technical": 10,
        "composition": 9,
        "brand": 10,
        "average": 9.7
      }
    },
    {
      "scene_id": 2,
      "scene_name": "45° Angle",
      "scene_type": "hero",
      "marketplace": "Shopee",
      "format": "1:1 square",
      "word_count": 98,
      "prompt_text": "[Full Scene 2 prompt]",
      "camera_specs": {
        "lens": "50mm",
        "aperture": "f/5.6",
        "iso": 200,
        "shutter_speed": "1/125s"
      },
      "lighting_setup": {
        "type": "3-point",
        "direction": "45° side",
        "color_temp": "5000K"
      },
      "quality_score": {
        "technical": 9,
        "composition": 9,
        "brand": 9,
        "average": 9.0
      }
    }
    // [Continue for all 9 scenes...]
  ],
  "batch_block": {
    "prompt_count": 9,
    "total_word_count": 1051,
    "separator": "---SCENE X---",
    "concatenated_text": "[Full batch block text with all 9 prompts]"
  },
  "validation": {
    "brand_consistency": true,
    "marketplace_compliance": {
      "mercado_livre": true,
      "shopee": true,
      "tiktok": true
    },
    "technical_requirements": true,
    "overall_quality_score": 8.9,
    "status": "validated"
  }
}
```

**Validation for .llm.json:**
- ✅ Valid JSON syntax (parseable)
- ✅ All 9 scenes included in `prompts` array
- ✅ Batch block included with full concatenated text
- ✅ Metadata complete (agent, workflow, version, duration, quality)
- ✅ Camera specs and lighting for each scene
- ✅ Quality scores per scene

---

#### **File 3: .meta.json (Workflow Metadata)**

**Purpose**: High-level workflow tracking, project metadata, version control

**JSON Structure:**

```json
{
  "project": {
    "name": "EcomLM CODEXA",
    "component": "photo_agent",
    "workflow_id": "adw_run_photo",
    "version": "2.0.0"
  },
  "execution": {
    "started_at": "2025-11-17T15:12:00Z",
    "completed_at": "2025-11-17T15:30:00Z",
    "duration_minutes": 18,
    "status": "completed_successfully"
  },
  "input": {
    "product": "Ceramic Coffee Mug (matte white, wooden handle, gold rim)",
    "style": "minimalist",
    "brand": "Hygge Home Co.",
    "marketplace_targets": ["Mercado Livre", "Shopee", "TikTok"]
  },
  "output": {
    "format": "trinity",
    "files_generated": [
      "ceramic_mug_prompts.md",
      "ceramic_mug_prompts.llm.json",
      "ceramic_mug_prompts.meta.json"
    ],
    "total_prompts": 9,
    "batch_block": true,
    "word_count": 1051
  },
  "quality_metrics": {
    "overall_score": 8.9,
    "technical_avg": 9.0,
    "composition_avg": 8.7,
    "brand_avg": 9.0,
    "validation_passed": true
  },
  "phases": [
    {
      "phase": 1,
      "name": "Scene Planning",
      "duration_minutes": 3,
      "status": "completed",
      "output": "9-scene grid (3x3: Hero → Context → Detail)"
    },
    {
      "phase": 2,
      "name": "Camera & Lighting Design",
      "duration_minutes": 4,
      "status": "completed",
      "output": "Camera specs + lighting for all 9 scenes"
    },
    {
      "phase": 3,
      "name": "AI Prompt Generation",
      "duration_minutes": 6,
      "status": "completed",
      "output": "9 AI prompts (avg 117 words each)"
    },
    {
      "phase": 4,
      "name": "Brand & Compliance Validation",
      "duration_minutes": 3,
      "status": "completed",
      "output": "Quality score: 8.9/10, all compliance checks passed"
    },
    {
      "phase": 5,
      "name": "Batch Assembly & QA",
      "duration_minutes": 2,
      "status": "completed",
      "output": "Trinity files generated (.md + .llm.json + .meta.json)"
    }
  ],
  "compliance": {
    "mercado_livre": {
      "white_background": true,
      "no_watermarks": true,
      "product_visibility_85_percent": true,
      "resolution_min_1200px": true
    },
    "shopee": {
      "max_9_images": true,
      "lifestyle_allowed": true,
      "product_visible": true
    },
    "tiktok": {
      "vertical_9_16": true,
      "natural_feel": true,
      "engaging": true
    }
  },
  "agent_info": {
    "agent_name": "photo_agent",
    "agent_version": "2.0.0",
    "workflow_source": "agentes/photo_agent/workflows/100_ADW_RUN_PHOTO.md",
    "documentation": "agentes/photo_agent/README.md"
  }
}
```

**Validation for .meta.json:**
- ✅ Valid JSON syntax
- ✅ Complete execution metadata (timestamps, duration, status)
- ✅ All 5 phases documented with durations
- ✅ Compliance checklist for all marketplaces
- ✅ Quality metrics summary
- ✅ File references (.md, .llm.json, .meta.json)

---

### Step 4: Run Final QA (Quality Assurance)

**Perform comprehensive final checks before delivery:**

#### **QA Checklist:**

**A. Completeness Check**
- ✅ 9 individual prompts present (Scenes 1-9)
- ✅ 1 batch block present (all 9 concatenated)
- ✅ All prompts ≥80 words (verify word count)
- ✅ Trinity files complete (.md + .llm.json + .meta.json)

**B. Format Validation**
- ✅ All prompts wrapped in ```code blocks```
- ✅ Scene separators in batch block (`---SCENE X---`)
- ✅ JSON files parseable (no syntax errors)
- ✅ Markdown renders correctly (headings, tables, code blocks)

**C. Content Verification**
- ✅ Camera specs included for each scene
- ✅ Lighting setup documented for each scene
- ✅ Marketplace targets specified (ML, Shopee, TikTok)
- ✅ Quality scores documented (per scene + overall)
- ✅ Usage guide included (.md file)

**D. Technical Accuracy**
- ✅ All camera specs realistic (no f/0.5, no ISO 50000)
- ✅ All lighting setups appropriate for scene type
- ✅ All prompts contain 7 core elements (subject, camera, composition, lighting, color, mood, quality)
- ✅ Marketplace compliance maintained (Scene 1 white bg, Scene 5 vertical)

**E. Usability Check**
- ✅ Prompts copy-paste ready (clean formatting)
- ✅ Batch block usable (clear separators)
- ✅ Usage guide clear (Midjourney, DALL-E, SD instructions)
- ✅ File naming logical (product_name_prompts.md/.llm.json/.meta.json)

**Final QA Result:**
```markdown
## ✅ FINAL QA REPORT

### Completeness: ✅ PASS
- 9/9 individual prompts present
- 1/1 batch block present
- 3/3 Trinity files generated

### Format: ✅ PASS
- All code blocks formatted correctly
- JSON files parseable (validated)
- Markdown renders correctly

### Content: ✅ PASS
- All camera/lighting specs included
- All marketplace targets specified
- Quality scores documented (avg: 8.9/10)

### Technical: ✅ PASS
- All settings realistic and accurate
- 7 core elements in each prompt
- Marketplace compliance maintained

### Usability: ✅ PASS
- Copy-paste ready (clean formatting)
- Usage guide complete (3 platforms)
- File naming logical

**OVERALL STATUS**: ✅ READY FOR DELIVERY
```

---

## OUTPUT FORMAT

**Final Trinity Output (3 files):**

1. **[product_name]_prompts.md** (Human-readable master file)
   - Quick reference table
   - 9 individual prompts with metadata
   - 1 batch block
   - Usage guide (Midjourney, DALL-E, SD)
   - QA checklist
   - Workflow metadata

2. **[product_name]_prompts.llm.json** (Structured data)
   - Product metadata
   - 9 scene objects (prompt, camera, lighting, quality scores)
   - Batch block text
   - Validation status

3. **[product_name]_prompts.meta.json** (Workflow tracking)
   - Execution timeline (start, end, duration)
   - Phase breakdown (5 phases with durations)
   - Quality metrics
   - Compliance report

**File Naming Convention:**
- Product: "Ceramic Coffee Mug" → Filename: `ceramic_coffee_mug_prompts`
- Extensions: `.md`, `.llm.json`, `.meta.json`

**Delivery Summary:**
```markdown
## 📦 DELIVERY PACKAGE

**Files Generated**:
1. `ceramic_coffee_mug_prompts.md` (12 KB)
2. `ceramic_coffee_mug_prompts.llm.json` (8 KB)
3. `ceramic_coffee_mug_prompts.meta.json` (4 KB)

**Total Size**: ~24 KB
**Format**: Trinity (MD + LLM.JSON + META.JSON)
**Status**: ✅ Complete & Validated

**Usage**:
- **For humans**: Open .md file (readable guide + prompts)
- **For LLMs/APIs**: Use .llm.json (structured data)
- **For tracking**: Check .meta.json (workflow history)

**Next Steps**:
1. Copy prompts from .md file into AI generator (Midjourney, DALL-E, etc.)
2. Generate 9 images (one per scene)
3. Review outputs against marketplace requirements
4. Post-process if needed (resize, compress, adjust white balance)
5. Upload to marketplaces (ML Scene 1, Shopee Scenes 2/4/5, etc.)
```

---

## VALIDATION CHECKLIST

**Before marking Phase 5 complete, confirm:**
- ✅ 9 individual prompts compiled (all ≥80 words)
- ✅ 1 batch block generated (all 9 concatenated with separators)
- ✅ Trinity files created (.md, .llm.json, .meta.json)
- ✅ .md file includes: prompts, batch block, usage guide, QA report
- ✅ .llm.json includes: product data, 9 scene objects, batch block, validation
- ✅ .meta.json includes: execution timeline, phases, quality metrics, compliance
- ✅ All JSON files parseable (no syntax errors)
- ✅ Final QA passed (completeness, format, content, technical, usability)
- ✅ Files named correctly (product_name_prompts.{md,llm.json,meta.json})
- ✅ Ready for delivery to user

---

## ERROR HANDLING

### Common Issues & Solutions

**Issue 1: Batch Block Concatenation Error**
- **Error**: "Batch block missing Scene 6 (only 8 prompts concatenated)"
- **Solution**: Verify all 9 prompts present, re-concatenate with separators:
  ```
  ---SCENE 1: FRONT VIEW---
  [Scene 1 prompt]

  ---SCENE 2: 45° ANGLE---
  [Scene 2 prompt]

  [... continue for all 9 ...]
  ```

**Issue 2: JSON Syntax Error**
- **Error**: ".llm.json line 47: Unexpected token '}' (missing comma)"
- **Solution**: Validate JSON syntax using online validator (jsonlint.com) or:
  ```bash
  python -m json.tool ceramic_mug_prompts.llm.json
  ```
- Fix: Add missing comma, escape quotes in prompt text, close all brackets

**Issue 3: Missing Trinity File**
- **Error**: "Only .md and .llm.json generated, .meta.json missing"
- **Solution**: Create .meta.json with minimal required fields:
  ```json
  {
    "project": {"name": "EcomLM CODEXA", "component": "photo_agent"},
    "execution": {"status": "completed", "duration_minutes": 18},
    "output": {"total_prompts": 9, "quality_score": 8.9}
  }
  ```

**Issue 4: Prompts Not Copy-Paste Ready**
- **Error**: "Scene prompts not in code blocks (formatting broken)"
- **Solution**: Wrap each prompt in triple backticks:
  ````
  ### Scene 1: Front View
  ```
  [Prompt text here]
  ```
  ````

**Issue 5: Incomplete Usage Guide**
- **Error**: "Usage guide missing Stable Diffusion instructions"
- **Solution**: Add SD section to .md file:
  ```markdown
  ### For Stable Diffusion Users
  1. Copy individual scene prompts
  2. Paste as positive prompt in WebUI
  3. Recommended: Realistic Vision model, 30-50 steps, CFG 7-9
  ```

---

## EXAMPLES

### Example: Trinity Output for Ceramic Mug

**File Structure:**
```
outputs/
├── ceramic_coffee_mug_prompts.md        (12 KB)
├── ceramic_coffee_mug_prompts.llm.json  (8 KB)
└── ceramic_coffee_mug_prompts.meta.json (4 KB)
```

**Sample .md Excerpt:**
````markdown
# 📸 AI Product Photography Prompts | Ceramic Coffee Mug

**Generated**: 2025-11-17T15:30:00Z
**Quality Score**: 8.9/10
**Total Scenes**: 9 (Hero → Context → Detail)

## 📋 QUICK REFERENCE
| Scene | Type | Platform | Format | Words |
|-------|------|----------|--------|-------|
| 1 | Front View | Mercado Livre | 1:1 | 112 |
[... table continues ...]

## 📸 INDIVIDUAL PROMPTS

### Scene 1: Front View
```
Matte white ceramic coffee mug with natural wooden handle...
[Full 112-word prompt]
```
**Camera**: 50mm, f/8, ISO 100, 1/125s

[... continues for all 9 scenes ...]

## 🎬 BATCH BLOCK
```
---SCENE 1: FRONT VIEW---
[Scene 1 prompt]

---SCENE 2: 45° ANGLE---
[Scene 2 prompt]

[... all 9 scenes ...]
```
````

**Sample .llm.json Excerpt:**
```json
{
  "metadata": {
    "agent": "photo_agent",
    "version": "2.0.0",
    "quality_score": 8.9
  },
  "prompts": [
    {
      "scene_id": 1,
      "prompt_text": "Matte white ceramic...",
      "camera_specs": {"lens": "50mm", "aperture": "f/8"},
      "quality_score": {"average": 9.7}
    }
    // [... 8 more scenes ...]
  ]
}
```

**Sample .meta.json Excerpt:**
```json
{
  "execution": {
    "duration_minutes": 18,
    "status": "completed_successfully"
  },
  "quality_metrics": {
    "overall_score": 8.9
  },
  "compliance": {
    "mercado_livre": true,
    "shopee": true,
    "tiktok": true
  }
}
```

---

## NOTES FOR LLM EXECUTION

1. **Trinity Format Philosophy**:
   - **.md**: Human-first (readable, usable, complete guide)
   - **.llm.json**: Machine-first (structured, queryable, integrations)
   - **.meta.json**: Tracking-first (workflow history, versioning)

2. **File Size Optimization**:
   - .md can be large (10-20 KB) - prioritize readability
   - .llm.json should be compact (5-10 KB) - remove redundancy
   - .meta.json minimal (2-5 KB) - only essential tracking data

3. **Batch Block Use Cases**:
   - ComfyUI: Queue multiple prompts
   - API batch: Single request, multiple outputs
   - Workflow automation: One-click 9-image generation

4. **JSON Validation**:
   - Always validate JSON syntax before delivery
   - Escape special characters in prompt text (quotes, backslashes)
   - Use JSON linters during development

5. **User-Friendly Defaults**:
   - Always include usage guide (3+ platforms)
   - Provide copy-paste ready formatting
   - Include troubleshooting tips in .md file

---

**End of 50_batch_assembler_HOP.md**
