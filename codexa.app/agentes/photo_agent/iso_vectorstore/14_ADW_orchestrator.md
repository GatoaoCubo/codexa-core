# ADW_RUN_PHOTO | photo_agent Execution Workflow v2.5.0

**Architecture**: Dual-Layer (ADW + HOP) | 12 Leverage Points
**Purpose**: End-to-end execution workflow for photo_agent
**Type**: 5-Phase ADW | **Duration**: ~10-20min (full) | ~3-5min (quick)
**Output**: 2 copyable prompts (Grid 3x3 + 9 Individual) with `{seed:[RANDOM]}` + `[OPEN_VARIABLES]`
**Status**: Production Ready (v2.5.0)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_run_photo_v2.5.0",
  "workflow_name": "photo Agent Execution",
  "agent": "photo_agent",
  "version": "2.5.0",
  "architecture": "dual_layer_adw_hop",
  "leverage_points": 12,
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4+ or claude-sonnet-4+",
  "execution_modes": {
    "full": {"scenes": 9, "duration": "10-20min"},
    "quick": {"scenes": 3, "duration": "3-5min"},
    "single": {"scenes": 1, "duration": "1-2min"}
  },
  "output_format": "2_copyable_prompts",
  "task_boundaries": true,
  "phases": [
    {
      "phase_id": "phase_1_scene_planning",
      "phase_name": "Scene Planning",
      "duration": "2-5min",
      "hop": "15_HOP_scene_planner.md",
      "task_boundary": "SCENE_PLANNING_COMPLETE"
    },
    {
      "phase_id": "phase_2_camera_design",
      "phase_name": "Camera & Lighting Design",
      "duration": "2-4min",
      "hop": "16_HOP_camera_designer.md",
      "task_boundary": "CAMERA_DESIGN_COMPLETE"
    },
    {
      "phase_id": "phase_3_prompt_generation",
      "phase_name": "Prompt Generation",
      "duration": "3-6min",
      "hop": "17_HOP_prompt_generator.md",
      "task_boundary": "PROMPTS_GENERATED"
    },
    {
      "phase_id": "phase_4_validation",
      "phase_name": "Brand & Compliance Validation",
      "duration": "2-4min",
      "hop": "18_HOP_brand_validator.md",
      "task_boundary": "VALIDATION_COMPLETE"
    },
    {
      "phase_id": "phase_5_assembly",
      "phase_name": "Output Assembly & QA",
      "duration": "1-3min",
      "hop": "19_HOP_batch_assembler.md",
      "task_boundary": "OUTPUT_READY"
    }
  ]
}
```

---

## TASK BOUNDARIES (Standard Out - Leverage Point #5)

Task boundaries communicate progress to external systems and users.

### Boundary Messages

| Phase | Boundary ID | Message Pattern |
|-------|-------------|-----------------|
| 1 | `SCENE_PLANNING_COMPLETE` | `[BOUNDARY] Phase 1 complete: 9-scene grid defined` |
| 2 | `CAMERA_DESIGN_COMPLETE` | `[BOUNDARY] Phase 2 complete: Camera specs for 9 scenes` |
| 3 | `PROMPTS_GENERATED` | `[BOUNDARY] Phase 3 complete: 9 prompts generated` |
| 4 | `VALIDATION_COMPLETE` | `[BOUNDARY] Phase 4 complete: Score {X}/13, {status}` |
| 5 | `OUTPUT_READY` | `[BOUNDARY] Phase 5 complete: 2 copyable prompts ready` |

### Progress Reporting Pattern

```
[PHASE 1/5] Scene Planning
├── Status: IN_PROGRESS
├── Input: subject="..." style="..."
└── ETA: ~3min

[BOUNDARY] Phase 1 complete: 9-scene grid defined
├── Scenes: 9/9
├── Style: commercial
└── Duration: 2.5min

[PHASE 2/5] Camera Design
├── Status: IN_PROGRESS
...
```

---

## ARCHITECTURE: DUAL-LAYER INTEGRATION

### Layer 1: ADW (What/When)
- High-level orchestration
- Phase management
- Task boundaries
- Error handling

### Layer 2: HOP (How)
- Detailed execution
- Step-by-step guidance
- Examples
- Validation checklists

### Integration Points

| Phase | ADW Objective | HOP File | Output |
|-------|--------------|----------|--------|
| 1 | Define 9-scene grid | `15_HOP_scene_planner.md` | `$scene_grid` |
| 2 | Design camera/lighting | `16_HOP_camera_designer.md` | `$camera_specs` |
| 3 | Generate AI prompts | `17_HOP_prompt_generator.md` | `$prompts_array` |
| 4 | Validate quality | `18_HOP_brand_validator.md` | `$quality_score` |
| 5 | Assemble output | `19_HOP_batch_assembler.md` | `$final_output` |

---

## PREREQUISITES

**Context Required**:
- `02_PRIME.md` (agent identity)
- `03_INSTRUCTIONS.md` (workflow rules)
- `09_camera_profiles.json` (12 camera profiles)
- `10_photography_styles.json` (7 styles)
- `11_pnl_triggers.json` (18 triggers)
- `12_output_template.md` (v3.2.0 format)

**Model**: GPT-4+ or Claude Sonnet 4+

**Input**: `subject` (required) + `style` (optional, default: commercial)

---

## PHASE 1: Scene Planning

**Objective**: Parse input and define 9-scene grid (3x3)

**$arguments IN**:
- `$subject`: Product description
- `$style`: Photography style (default: commercial)
- `$brand_profile`: Optional brand settings

**Actions**:
1. Parse subject → Extract product, features, materials
2. Load style from `10_photography_styles.json`
3. Define 3x3 grid:
   - Row 1: Hero shots (Scene 1-3)
   - Row 2: Context shots (Scene 4-6)
   - Row 3: Detail shots (Scene 7-9)
4. Map PNL triggers from `11_pnl_triggers.json`
5. Validate: 9 scenes, style valid, configs loaded

**$arguments OUT**:
- `$scene_grid`: 9-scene definitions
- `$loaded_configs`: Camera, styles, PNL

**Validation**:
- ✅ Subject extracted
- ✅ Style validated
- ✅ 9 scenes defined
- ✅ Configs loaded

**Error Handling**:
- Missing subject → HALT: "No product specified"
- Invalid style → WARN: "Defaulting to commercial"
- Scene count ≠9 → RETRY: "Add missing scenes"

**Task Boundary**:
```
[BOUNDARY] SCENE_PLANNING_COMPLETE
├── Scenes: 9/9 defined
├── Style: {style_name}
├── PNL: 9 triggers mapped
└── Duration: {X}min
```

**HOP**: → `15_HOP_scene_planner.md`

---

## PHASE 2: Camera & Lighting Design

**Objective**: Design camera specs and lighting for each scene

**$arguments IN**:
- `$scene_grid`: From Phase 1
- `$camera_profiles`: From `09_camera_profiles.json`

**Actions**:
1. For each scene (1-9):
   - Select lens (35mm-100mm)
   - Set aperture with [RANGE]: `[f/2.8-f/16]`
   - Set ISO with [RANGE]: `[100-800]`
   - Set shutter with [RANGE]: `[1/60-1/500s]`
2. Design lighting with [OPTIONS]:
   - Type: `[high-key|3-point|natural|soft-diffused]`
   - Direction: `[front|side|back|overhead]`
   - Temperature: `[5200K-5500K]`
3. Validate technical accuracy

**$arguments OUT**:
- `$camera_specs`: 9 camera configurations with [OPEN_VARIABLES]
- `$lighting_setups`: 9 lighting designs with [OPTIONS]

**Validation**:
- ✅ Camera specs for 9 scenes
- ✅ Lighting for 9 scenes
- ✅ [OPEN_VARIABLES] applied
- ✅ No impossible combinations

**Task Boundary**:
```
[BOUNDARY] CAMERA_DESIGN_COMPLETE
├── Camera: 9/9 specs with [RANGES]
├── Lighting: 9/9 setups with [OPTIONS]
└── Duration: {X}min
```

**HOP**: → `16_HOP_camera_designer.md`

---

## PHASE 3: Prompt Generation

**Objective**: Generate 9 AI prompts with seeds and [OPEN_VARIABLES]

**$arguments IN**:
- `$scene_grid`: From Phase 1
- `$camera_specs`: From Phase 2
- `$lighting_setups`: From Phase 2
- `$output_template`: From `12_output_template.md`

**Actions**:
1. For each scene (1-9), generate prompt with:
   - Prefix: `{user_image} {seed:[RANDOM]} [SCENE_X_OF_9]`
   - Subject description
   - Camera specs with [RANGES]
   - Lighting with [OPTIONS]
   - Composition with [OPTIONS]
   - PNL triggers with [OPTIONS]
   - Quality specs (8K, no watermarks, etc.)
2. Scene 1: White background #FFFFFF
3. Scene 9: White background #FFFFFF (CRITICAL)
4. Add generation commands at end

**$arguments OUT**:
- `$prompts_array`: 9 prompts with seeds + [OPEN_VARIABLES]

**Validation**:
- ✅ 9 prompts generated
- ✅ Each has `{user_image} {seed:[RANDOM]}`
- ✅ Each has `[OPEN_VARIABLES]`
- ✅ Scene 1+9 have #FFFFFF background
- ✅ Word count: 180-300 words each

**Task Boundary**:
```
[BOUNDARY] PROMPTS_GENERATED
├── Prompts: 9/9 generated
├── Seeds: {seed:[RANDOM]} applied
├── [OPEN_VARIABLES]: Present in all
├── Scene 1+9: White #FFFFFF
└── Duration: {X}min
```

**HOP**: → `17_HOP_prompt_generator.md`

---

## PHASE 4: Brand & Compliance Validation

**Objective**: Validate quality and marketplace compliance

**$arguments IN**:
- `$prompts_array`: From Phase 3
- `$brand_profile`: Optional

**Actions**:
1. Run 13-point validation:
   - Technical (7 points): seeds, variables, camera, lighting, length, specs, commands
   - Content (6 points): scene 1 white, scene 9 white, PNL, brand, no text, copy-ready
2. Calculate quality score: passed/13
3. Check marketplace compliance (ML/Shopee/Amazon)
4. Apply brand alignment (if provided)

**$arguments OUT**:
- `$validated_prompts`: Prompts with validation status
- `$quality_score`: X/13 (threshold: ≥0.85)
- `$compliance_report`: Marketplace status

**Validation**:
- ✅ Score ≥11/13 (0.85)
- ✅ Scene 1+9 white background
- ✅ No compliance failures
- ✅ Brand aligned (if applicable)

**Error Handling**:
- Score <11/13 → RETRY: Auto-correct + revalidate
- Scene 9 not white → HALT: "Marketplace compliance failed"
- Brand mismatch → WARN: "Adjust colors/mood"

**Task Boundary**:
```
[BOUNDARY] VALIDATION_COMPLETE
├── Score: {X}/13 ({percentage}%)
├── Status: {PASS|WARN|FAIL}
├── Marketplace: {compliant|issues}
└── Duration: {X}min
```

**HOP**: → `18_HOP_brand_validator.md`

---

## PHASE 5: Output Assembly & QA

**Objective**: Compile 2 copyable prompts (Grid + Individual)

**$arguments IN**:
- `$validated_prompts`: From Phase 4
- `$quality_score`: From Phase 4

**Actions**:
1. Generate PROMPT 1 (Grid 3x3):
   - Prefix: `{user_image} {seed:[RANDOM]} [GENERATE_ALL_9_SCENES_AS_GRID]`
   - All 9 scenes described in sequence
   - Camera system specs
   - Suffix: "Generate all 9 scenes as a single 3x3 grid PNG image in sequence now"
   - Target: 500-800 words

2. Generate PROMPT 2 (9 Individual):
   - Header: `[generate 1 png for each scene]`
   - 9 prompts with `{user_image} {seed:[RANDOM]} [SCENE_X_OF_9]`
   - Separated by blank lines
   - Suffix on Scene 9: "Generate all 9 scenes as separate PNGs in sequence now"
   - Target: 180-300 words each

3. Final QA:
   - All seeds present
   - All [OPEN_VARIABLES] present
   - Word counts correct
   - Copy-paste ready

**$arguments OUT**:
- `$final_output`: Single markdown with 2 code blocks

**Output Format**:
```markdown
# [Product Name] | Photo Prompts

## PROMPT 1: Grid 3x3 (9 Scenes in 1 Image)
```
{user_image} {seed:[RANDOM]} [GENERATE_ALL_9_SCENES_AS_GRID] ...
```

## PROMPT 2: Individual Scenes (9 Separate Images)
```
[generate 1 png for each scene]

{user_image} {seed:[RANDOM]} [SCENE_1_OF_9] ...
...
{user_image} {seed:[RANDOM]} [SCENE_9_OF_9] ... Generate all 9 scenes as separate PNGs now.
```
```

**Task Boundary**:
```
[BOUNDARY] OUTPUT_READY
├── Format: 2 copyable prompts
├── PROMPT 1: Grid 3x3 ({X} words)
├── PROMPT 2: 9 Individual ({Y} words avg)
├── QA: PASSED
├── Copy-paste: READY
└── Total Duration: {X}min
```

**HOP**: → `19_HOP_batch_assembler.md`

---

## EXECUTION MODES

### Full Mode (9 scenes)
```
Input: subject + style
Duration: 10-20min
Output: All 9 scenes
Use: Complete product photography set
```

### Quick Mode (3 scenes)
```
Input: subject + style
Duration: 3-5min
Output: Scene 1 (Hero) + Scene 2 (Lifestyle) + Scene 9 (Marketplace)
Use: Fast iteration, MVP testing
```

### Single Mode (1 scene)
```
Input: subject + style + scene_number
Duration: 1-2min
Output: Single scene only
Use: Specific scene regeneration
```

---

## SUCCESS CRITERIA

### Workflow Level
- ✅ All 5 phases completed
- ✅ All task boundaries reported
- ✅ Duration within target
- ✅ No critical errors

### Output Level
- ✅ 2 copyable prompts generated
- ✅ Quality score ≥0.85 (11/13)
- ✅ Scene 1+9 white background
- ✅ Copy-paste ready

### Quality Level
- ✅ 13-point validation passed
- ✅ [OPEN_VARIABLES] in all prompts
- ✅ `{seed:[RANDOM]}` in all prompts
- ✅ Marketplace compliance met

---

## METADATA

**Version**: 2.5.0
**Updated**: 2025-11-25
**Architecture**: Dual-Layer (ADW + HOP) | 12 Leverage Points
**Agent**: photo_agent v2.5.0
**Domain**: AI Product Photography (E-commerce)
**Phases**: 5 (with task boundaries)
**HOPs**: 5 modular prompts (15-19)
**Output**: 2 copyable prompts (no Trinity files)

**Changelog v2.5.0**:
- ✅ Added task boundaries (Leverage Point #5)
- ✅ Updated output format (2 prompts, no Trinity)
- ✅ Added execution modes (full/quick/single)
- ✅ Added $arguments chaining
- ✅ Updated HOP references to iso_vectorstore paths
- ✅ Applied 12 Leverage Points framework
