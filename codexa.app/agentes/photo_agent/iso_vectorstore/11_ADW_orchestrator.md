<!-- iso_vectorstore -->
<!--
  Source: 100_ADW_RUN_PHOTO.md
  Agent: photo_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 100_ADW_RUN_PHOTO | photo Agent Execution Workflow

**Architecture**: Dual-Layer (ADW + HOP Integration)
**Purpose**: End-to-end execution workflow for photo_agent
**Type**: 5-Phase ADW | **Duration**: ~15-30min
**Output**: "grid_3x3", 9 individual prompts + 1 batch block (all 9 concatenated) in Trinity format (.md + .llm.json + .meta.json) (trinity)
**Status**: Dual-Layer Integrated (v2.0.0)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_run_photo",
  "workflow_name": "photo Agent Execution",
  "agent": "photo_agent",
  "version": "2.0.0",
  "architecture": "dual_layer_adw_hop",
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4+ or claude-sonnet-4+",
  "required_capabilities": {
    "multi-format output (.md + .json)": true,
    "compliance validation": true
  },
  "phases": [
    {
      "phase_id": "phase_1_input_processing_&_scene_planning",
      "phase_name": "Input Processing & Scene Planning",
      "duration": "2-5min",
      "description": "Parse subject/style and define 9-scene grid (3x3)"
    },
    {
      "phase_id": "phase_2_camera_&_lighting_design",
      "phase_name": "Camera & Lighting Design",
      "duration": "3-7min",
      "description": "Design camera specs and lighting setups for each scene"
    },
    {
      "phase_id": "phase_3_prompt_generation_(scenes_1-9)",
      "phase_name": "Prompt Generation (Scenes 1-9)",
      "duration": "5-10min",
      "description": "Generate detailed AI prompts with composition + PNL triggers"
    },
    {
      "phase_id": "phase_4_brand_&_compliance_validation",
      "phase_name": "Brand & Compliance Validation",
      "duration": "3-7min",
      "description": "Validate brand consistency and marketplace compliance"
    },
    {
      "phase_id": "phase_5_batch_assembly_&_qa",
      "phase_name": "Batch Assembly & QA",
      "duration": "2-5min",
      "description": "Compile 9 individual prompts + 1 batch block in Trinity format"
    }
  ]
}
```

---

## ARCHITECTURE: DUAL-LAYER INTEGRATION

This workflow implements a **Dual-Layer Architecture** combining:

### Layer 1: ADW (Agentic Developer Workflow)
- **Purpose**: High-level orchestration and phase management
- **Scope**: Defines WHAT to do and WHEN to do it
- **Components**: 5 phases with clear objectives, inputs, outputs, and validation criteria
- **Flexibility**: Adaptable to different products, styles, and marketplace requirements

### Layer 2: HOP (Higher-Order Prompts)
- **Purpose**: Detailed execution instructions with examples and best practices
- **Scope**: Defines HOW to do it with step-by-step guidance
- **Components**: 5 modular HOP prompts (one per phase)
- **Depth**: Comprehensive instructions, error handling, validation checklists, and examples

### Integration Points

Each ADW phase links to its corresponding HOP prompt:

| Phase | ADW (What/When) | HOP (How) | File |
|-------|-----------------|-----------|------|
| 1 | Input Processing & Scene Planning | Parse input → Design 9-scene grid | `prompts/10_scene_planner_HOP.md` |
| 2 | Camera & Lighting Design | Design camera specs + lighting setups | `prompts/20_camera_designer_HOP.md` |
| 3 | Prompt Generation (Scenes 1-9) | Generate 9 AI prompts (≥80 words each) | `prompts/30_prompt_generator_HOP.md` |
| 4 | Brand & Compliance Validation | Validate brand + marketplace compliance | `prompts/40_brand_validator_HOP.md` |
| 5 | Batch Assembly & QA | Compile Trinity output (.md + .json files) | `prompts/50_batch_assembler_HOP.md` |

### Benefits of Dual-Layer Design

1. **Separation of Concerns**: ADW manages workflow logic, HOPs handle execution details
2. **Modularity**: Each HOP is independently updatable without changing ADW structure
3. **Reusability**: HOPs can be used standalone or referenced by multiple workflows
4. **Clarity**: Clear distinction between orchestration (ADW) and implementation (HOP)
5. **Scalability**: Easy to add new phases or modify existing ones without breaking integration

### Usage Pattern

**For AI Assistants**:
1. Read this ADW file to understand overall workflow structure
2. Execute each phase by following its "HOP Implementation" section
3. Use HOP prompts for detailed step-by-step guidance
4. Return to ADW for validation criteria and next phase transition

**For Human Developers**:
1. ADW provides the roadmap (phases, objectives, success criteria)
2. HOPs provide the playbook (detailed instructions, examples, error handling)
3. Modify HOPs for execution refinements without touching ADW logic

---

## PREREQUISITES

**Before starting, ensure:**

1. **Context Loaded**:
   - Read `PRIME.md` (agent instructions)
   - Read `README.md` (agent structure)
   - `config/camera_profiles.json`
   - `config/photography_styles.json`
   - `config/pnl_triggers.json`

2. **Capabilities Available**:
   - LLM: gpt-4+ or claude-sonnet-4+
   - Tools: multi-format output (.md + .json), compliance validation

3. **User Input Ready**:
   - subject="Ceramic mug", style="minimalist"

---

## PHASE 1: Input Processing & Scene Planning

**Objective**: Parse subject/style and define 9-scene grid (3x3)

**Actions**:
1. **Parse input**: Extract subject (product), style (minimalist/lifestyle/etc), brand guidelines (if provided)
2. **Define 9-scene grid (3x3 matrix)**:
3.   - Row 1: Hero shots (angles: front, 45°, top)
4.   - Row 2: Context shots (lifestyle, use case, scale)
5.   - Row 3: Detail shots (texture, features, branding)
6. **Load configuration files**: `config/camera_profiles.json`, `config/photography_styles.json`, `config/pnl_triggers.json`
7. **Validate input**: Subject defined, style valid (from config), scene count = 9

**Input**:
- `$user_input`
- `$config_files`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Subject extracted successfully
- ✅ Style validated (exists in config)
- ✅ 9-scene grid defined (3x3 matrix)
- ✅ Configuration files loaded

**Error Handling**:
- If subject missing → HALT: 'No product/subject specified. Provide product description to generate prompts.'
- If style invalid → WARN: 'Style "[X]" not in config. Available: [list]. Defaulting to "commercial".'
- If grid ≠9 scenes → RETRY: 'Scene count: [X]. Must be exactly 9 (3x3 grid). Generate: [list missing scenes].'

**HOP Implementation:**
```
For detailed step-by-step instructions, execute:
📖 READ: agentes/photo_agent/prompts/10_scene_planner_HOP.md

This HOP provides:
- Complete input parsing strategy (subject, style, brand)
- Detailed 9-scene grid design (3x3 matrix: Hero → Context → Detail)
- Configuration loading instructions (camera_profiles, photography_styles, pnl_triggers)
- Comprehensive validation checklist
- Error handling scenarios with solutions
- 2 complete examples (minimalist mug, lifestyle earbuds)

Expected HOP output: 9-scene grid defined + configs loaded + validation passed
```

---
## PHASE 2: Camera & Lighting Design

**Objective**: Design camera specs and lighting setups for each scene

**Actions**:
1. **For each scene (1-9), design camera specs**:
2.   - Lens: Focal length (e.g., 50mm, 85mm, 100mm macro)
3.   - Aperture: f-stop (f/1.8 = shallow DOF, f/8 = sharp detail)
4.   - ISO: Sensitivity (100-400 = clean, 800+ = grain)
5.   - Shutter speed: Motion control (1/125 = standard, 1/1000 = freeze action)
6. **Design lighting setup per scene**:
7.   - Type: 3-point (key+fill+rim), natural (window), studio (soft box)
8.   - Direction: Front, side, back, top-down, Rembrandt
9.   - Color temp: Warm (3000K), neutral (5500K), cool (7000K)
10. **Validate specs**: Technical accuracy, alignment with style, marketplace compliance

**Input**:
- `$phase_1_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Camera specs designed for all 9 scenes
- ✅ Lighting setups defined for all 9 scenes
- ✅ Technical specs accurate (lens, aperture, ISO, shutter)
- ✅ Specs align with style requirements

**Error Handling**:
- If camera_specs incomplete → RETRY: 'Scene [X] missing camera specs. Need: lens + aperture + ISO + shutter.'
- If lighting_setup incomplete → RETRY: 'Scene [X] missing lighting. Need: type + direction + color temp.'
- If specs technically incorrect → FAIL: 'Invalid specs: [issue]. Fix: (e.g., f/0.5 impossible, max f/1.2; ISO >12800 = noise)'

**HOP Implementation:**
```
For detailed step-by-step instructions, execute:
📖 READ: agentes/photo_agent/prompts/20_camera_designer_HOP.md

This HOP provides:
- Complete camera specs guide (lens selection, aperture, ISO, shutter speed)
- Lighting setup design (3-point, natural, soft box, overhead, Rembrandt)
- Technical validation criteria (accuracy, style alignment, marketplace compliance)
- Marketplace-specific requirements (ML white bg, Shopee lifestyle, TikTok vertical)
- Comprehensive error handling
- 2 complete examples with full specs (minimalist mug, lifestyle earbuds)

Expected HOP output: Camera specs + lighting design for all 9 scenes
```

---
## PHASE 3: Prompt Generation (Scenes 1-9)

**Objective**: Generate detailed AI prompts with composition + PNL triggers

**Actions**:
1. **For each scene (1-9), generate AI prompt (≥80 words each)**:
2.   - Subject description (detailed physical attributes)
3.   - Camera specs (lens, aperture, ISO, shutter)
4.   - Composition (rule of thirds, leading lines, symmetry, negative space)
5.   - Lighting setup (type, direction, color temp)
6.   - Color palette (primary, accent, background)
7.   - Mood/emotion (PNL triggers: trust, desire, urgency, exclusivity)
8.   - Technical quality (ultra-sharp, 8K, professional, commercial)
9. **Add marketplace-specific requirements**: Mercado Livre (white bg), Shopee (lifestyle), TikTok (vertical 9:16)
10. **Wrap prompts in code blocks**: For easy copy-paste

**Input**:
- `$phase_2_output`
- `$accumulated_context`

**Output**:
- `$generated_content`
- `$metadata`

**Validation**:
- ✅ 9 AI prompts generated
- ✅ Each prompt ≥80 words
- ✅ All elements present (subject, camera, composition, lighting, color, mood, quality)
- ✅ Marketplace requirements added
- ✅ Prompts wrapped in code blocks

**Error Handling**:
- If prompt_count ≠9 → HALT: 'Only [X] prompts generated. Need exactly 9. Missing: scenes [list].'
- If prompt_length <80 words → RETRY: 'Scene [X] too brief ([Y] words). Add: composition details, lighting nuances, mood descriptors. Target: ≥80 words.'
- If missing elements → RETRY: 'Scene [X] incomplete. Missing: [list]. Add all: subject, camera, composition, lighting, color, mood, quality.'
- If not in code blocks → RETRY: 'Wrap all prompts in ```markdown code blocks for easy copy-paste.'

**HOP Implementation:**
```
For detailed step-by-step instructions, execute:
📖 READ: agentes/photo_agent/prompts/30_prompt_generator_HOP.md

This HOP provides:
- 7-element AI prompt structure (subject, camera, composition, lighting, color, mood, quality)
- PNL trigger integration (trust, desire, urgency, exclusivity from config)
- Marketplace-specific formatting (ML white bg, Shopee lifestyle, TikTok 9:16)
- Code block formatting for copy-paste efficiency
- Word count validation (≥80 words per prompt)
- 3 complete examples with 80-180 word prompts (mug, earbuds, texture detail)

Expected HOP output: 9 AI prompts (≥80 words each) in code blocks
```

---
## PHASE 4: Brand & Compliance Validation

**Objective**: Validate brand consistency and marketplace compliance

**Actions**:
1. **Check brand consistency**: Colors match brand palette, style aligns with brand personality
2. **Validate marketplace compliance**:
3.   - Mercado Livre: No watermarks, white background for main shot, no text overlays
4.   - Shopee: Max 9 images, lifestyle allowed, clear product visibility
5.   - TikTok: Vertical format preferred, engaging first frame, motion encouraged
6. **Verify technical requirements**: Resolution ≥1200px, file size <5MB, format (JPG/PNG)
7. **Calculate quality score**: Technical (0-10) + Composition (0-10) + Brand (0-10) → Average ≥7.0

**Input**:
- `$phase_3_output`
- `$accumulated_context`

**Output**:
- `$validated_data`
- `$quality_score`

**Validation**:
- ✅ Brand consistency checked
- ✅ Marketplace compliance validated (specific rules per marketplace)
- ✅ Technical requirements verified (resolution, size, format)
- ✅ Quality score calculated (≥7.0)

**Error Handling**:
- If brand_mismatch → WARN: 'Colors/style don't match brand guidelines. Adjust: [specific changes]'
- If compliance_failed → HALT: 'Marketplace compliance failed: [issues]. Fix: (e.g., ML needs white bg for main shot, no watermarks).'
- If quality_score <7.0 → RETRY: 'Quality too low ([X]/10). Improve: [list specific areas: technical, composition, brand].'

**HOP Implementation:**
```
For detailed step-by-step instructions, execute:
📖 READ: agentes/photo_agent/prompts/40_brand_validator_HOP.md

This HOP provides:
- Brand consistency checklist (colors, style, personality alignment)
- Marketplace compliance rules (ML, Shopee, TikTok specific requirements)
- Technical requirements validation (resolution, ISO, aperture, format)
- Quality scoring rubric (Technical 0-10, Composition 0-10, Brand 0-10)
- Comprehensive error handling with specific fixes
- 2 complete examples (full validation report + validation with issues requiring fixes)

Expected HOP output: Validated prompts + quality score (≥7.0/10) + compliance report
```

---
## PHASE 5: Batch Assembly & QA

**Objective**: Compile 9 individual prompts + 1 batch block in Trinity format

**Actions**:
1. **Compile 9 individual prompts**: Each in separate code block with scene number
2. **Generate 1 batch block**: All 9 prompts concatenated with separators (for bulk processing)
3. **Assemble Trinity Output** (.md human-readable + .llm.json structured + .meta.json metadata):
4.   - .md: Grid overview + 9 individual prompts + 1 batch block + usage instructions
5.   - .llm.json: Structured data (scene_grid, prompts_array, camera_specs, lighting_setups)
6.   - .meta.json: Workflow metadata (product, style, quality_score, marketplace_target)
7. **Run final QA**: All 9 prompts ≥80 words, batch block concatenates correctly, Trinity files valid

**Input**:
- `$phase_4_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ 9 individual prompts compiled
- ✅ 1 batch block generated (all 9 concatenated)
- ✅ Trinity files created (.md + .llm.json + .meta.json)
- ✅ All prompts ≥80 words
- ✅ Batch block concatenates correctly

**Error Handling**:
- If batch_block incorrect → RETRY: 'Batch concatenation error. Ensure all 9 prompts included with clear separators (---Scene X---).'
- If trinity_files incomplete → HALT: 'Missing files. Required: .md + .llm.json + .meta.json. Found: [list].'
- If JSON invalid → RETRY: '.llm.json or .meta.json not parseable. Error: [details]. Fix syntax.'

**HOP Implementation:**
```
For detailed step-by-step instructions, execute:
📖 READ: agentes/photo_agent/prompts/50_batch_assembler_HOP.md

This HOP provides:
- Individual prompt compilation strategy (9 scenes with headers, specs, code blocks)
- Batch block generation (all 9 concatenated with separators for bulk processing)
- Trinity output format (.md human-readable, .llm.json structured, .meta.json metadata)
- Final QA checklist (completeness, format, content, technical, usability)
- Comprehensive error handling (JSON syntax, missing files, concatenation errors)
- Complete example (Trinity output structure for ceramic mug with all 3 files)

Expected HOP output: Trinity files (.md + .llm.json + .meta.json) + final QA report
```

---

## EXECUTION INSTRUCTIONS

### For AI Assistants (Conversational Mode)

**Step 1: Load Context**
```
Read the following files:
1. {agent}/PRIME.md
2. {agent}/README.md
3. This workflow (ADW file)
```

**Step 2: Obtain User Input**
```
Ask user for required inputs
```

**Step 3: Execute Workflow**
```
Follow phases sequentially:
- Announce phase start
- Execute phase actions
- Validate outputs
- Report completion
```

**Step 4: Report Completion**
```
Report:
- Duration
- Quality metrics
- Outputs saved
- Next steps
```

---

## SUCCESS CRITERIA

### Workflow Level
- ✅ All 5 phases completed
- ✅ Duration within target
- ✅ No validation failures

### Output Level
- ✅ "grid_3x3", 9 individual prompts + 1 batch block (all 9 concatenated) in Trinity format (.md + .llm.json + .meta.json) generated
- ✅ Quality score ≥0.7
- ✅ Format: trinity

### Quality Level
- ✅ 11 validation criteria passed
- ✅ Compliance requirements met (if applicable)

---

## METADATA

**Created**: 2025-11-17
**Updated**: 2025-11-17 (Dual-Layer Integration)
**Generator**: CODEXA ADW Intelligent Constructor v1.0.0
**Architecture**: Dual-Layer (ADW + HOP)
**Agent**: photo_agent v2.0.0
**Domain**: AI Product Photography (E-commerce Marketplaces)
**Phases**: 5 (each with integrated HOP prompt)
**HOP Prompts**: 5 modular prompts (~50KB total)
**Auto-generated**: True (Base ADW v1.0.0) + Manual HOP Integration (v2.0.0)

---

**Status**: Dual-Layer Integrated
**Maintainer**: CODEXA Meta-Constructor
**Version**: 2.0.0

**Integration Details**:
- Base ADW: v1.0.0 (Auto-generated 2025-11-17)
- HOP Layer: v2.0.0 (Integrated 2025-11-17)
- HOP Files: 5 prompts (10_scene_planner, 20_camera_designer, 30_prompt_generator, 40_brand_validator, 50_batch_assembler)
- Total HOP Size: ~50KB (comprehensive step-by-step instructions)
- Pattern Source: Based on anuncio_agent POC (commit 5c5ceeb01)