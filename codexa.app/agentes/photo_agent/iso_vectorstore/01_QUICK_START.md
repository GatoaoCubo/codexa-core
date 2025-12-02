# photo_agent | Quick Start Guide v2.5.0

**Version**: 2.5.0 | **Max Chars**: 8000 | **Architecture**: 12 Leverage Points

---

## IDENTITY

**Agent**: photo_agent v2.5.0
**Function**: Transform product descriptions → 2 copyable photography prompts
**Output**: Grid 3x3 (1 image) + 9 Individual prompts with `{user_image} {seed:[RANDOM]}`
**Use Case**: E-commerce product photography for AI generators (Midjourney, Flux, DALL-E, Imagen)

---

## QUICK START (3 Steps)

**1. READ FOUNDATION** (Files 01-04)
→ Start with **02_PRIME** + **03_INSTRUCTIONS** + **04_README**

**2. LOAD CONFIGS** (Files 05-11)
→ Read JSON schemas: **05** (input) + **09-11** (camera/styles/PNL) + **12** (output template)

**3. EXECUTE WORKFLOW** (Files 14-19)
→ Follow **14_ADW** → Call HOPs **15-19** → Output **2 copyable prompts**

---

## FILE ARCHITECTURE (20 Files)

### Core Documentation (01-04)
| File | Purpose |
|------|---------|
| **01_QUICK_START.md** | This file - compact navigation guide |
| **02_PRIME.md** | Agent identity + 12 Leverage Points status |
| **03_INSTRUCTIONS.md** | Core Workflow 1 & 2 (Standard + Brand-Aligned) |
| **04_README.md** | Complete documentation |

### Schemas & Validation (05-08)
| File | Purpose |
|------|---------|
| **05_input_schema.json** | Input validation (subject, style, brand_profile) |
| **06_output_standard_schema.json** | Standard output validation |
| **07_output_marketplace_schema.json** | Marketplace compliance validation |
| **08_output_brand_schema.json** | Brand alignment validation |

### Photography Data (09-11)
| File | Purpose |
|------|---------|
| **09_camera_profiles.json** | 12 camera profiles (lens, aperture, ISO, shutter) |
| **10_photography_styles.json** | 7 styles (minimalist, dramatic, lifestyle...) |
| **11_pnl_triggers.json** | 18 PNL triggers + scene mapping + brand archetypes |

### Templates & Setup (12-13)
| File | Purpose |
|------|---------|
| **12_output_template.md** | v3.2.0 format (seeds + [OPEN_VARIABLES]) |
| **13_SETUP.md** | Configuration + installation |

### Execution (14-19)
| File | Purpose |
|------|---------|
| **14_ADW_orchestrator.md** | 5-phase workflow with task boundaries |
| **15_HOP_scene_planner.md** | Phase 1: Scene grid planning |
| **16_HOP_camera_designer.md** | Phase 2: Camera + lighting specs |
| **17_HOP_prompt_generator.md** | Phase 3: AI prompt generation |
| **18_HOP_brand_validator.md** | Phase 4: Brand + compliance validation |
| **19_HOP_batch_assembler.md** | Phase 5: Assembly + QA |

### Meta (20)
| File | Purpose |
|------|---------|
| **20_CHANGELOG.md** | Version history |

---

## EXECUTION FLOW (5 Phases)

```
PHASE 0: PREP
├── READ: 02_PRIME + 03_INSTRUCTIONS + 04_README
├── LOAD: 05_input + 09_camera + 10_styles + 11_pnl + 12_template
└── READY: Begin execution

PHASE 1: SCENE PLANNING (HOP 15)
├── IN: $subject + $style
├── PROCESS: Load 10+11 → Design 3x3 grid
├── OUT: $scene_grid (9 scenes defined)
└── BOUNDARY: "Scene planning complete"

PHASE 2: CAMERA DESIGN (HOP 16)
├── IN: $scene_grid
├── PROCESS: Load 09 → Camera + lighting per scene
├── OUT: $camera_specs + $lighting
└── BOUNDARY: "Camera specs complete"

PHASE 3: PROMPT GENERATION (HOP 17)
├── IN: $scene_grid + $camera_specs
├── PROCESS: Apply 12_template → Add seeds + [OPEN_VARIABLES]
├── OUT: $prompts_array (9 prompts)
└── BOUNDARY: "Prompts generated"

PHASE 4: VALIDATION (HOP 18)
├── IN: $prompts_array
├── PROCESS: 13-point QC + brand check + PNL check
├── OUT: $validated_prompts + $quality_score
└── BOUNDARY: "Validation complete (score: X/13)"

PHASE 5: ASSEMBLY (HOP 19)
├── IN: $validated_prompts
├── PROCESS: Format PROMPT 1 (grid) + PROMPT 2 (individual)
├── OUT: Single markdown with 2 code blocks
└── BOUNDARY: "Output ready - copy-paste enabled"
```

---

## EXECUTION MODES

| Mode | Duration | Scenes | Description |
|------|----------|--------|-------------|
| **full** | 10-20min | 9 | Complete product photography set |
| **quick** | 3-5min | 3 | Hero (1) + Lifestyle (2) + Marketplace (9) |
| **single** | 1-2min | 1 | Single scene only |

---

## OUTPUT FORMAT (v3.2.0)

```markdown
# [Product Name] | Photo Prompts

## PROMPT 1: Grid 3x3 (9 Scenes in 1 Image)
```
{user_image} {seed:[RANDOM]} [GENERATE_ALL_9_SCENES_AS_GRID] Professional product photography grid 3x3...
```

## PROMPT 2: Individual Scenes (9 Separate Images)
```
{user_image} {seed:[RANDOM]} [SCENE_1_OF_9] Professional product photography...
{user_image} {seed:[RANDOM]} [SCENE_2_OF_9] ...
...
{user_image} {seed:[RANDOM]} [SCENE_9_OF_9] ... Generate all 9 scenes as separate PNGs now.
```
```

**Key Features v3.2.0**:
- `{user_image} {seed:[RANDOM]}` in ALL prompts
- `[OPEN_VARIABLES]` for randomization: `[f/5.6-f/11]`, `[high-key|3-point]`
- Scene 1 AND 9 white background #FFFFFF
- Auto-PNG generation commands inline

---

## QUALITY CHECKLIST (13 Points)

**Technical (7)**:
1. `{user_image} {seed:[RANDOM]}` prefix
2. `[OPEN_VARIABLES]` present
3. Camera specs realistic
4. Lighting physics correct
5. Word count: P1 500-800, P2 180-300 each
6. No impossible setups
7. Generation commands present

**Content (6)**:
8. Scene 1 white #FFFFFF
9. Scene 9 white #FFFFFF (CRITICAL)
10. PNL triggers with [OPTIONS]
11. Brand colors (if provided)
12. No text/logos
13. Copy-paste ready

**Threshold**: ≥0.85 | Marketplace: ≥0.90

---

## FILE READ PRIORITY

**Minimum** (6 files):
→ 01_QUICK + 02_PRIME + 03_INSTRUCTIONS + 05_input + 11_pnl + 12_template

**Recommended** (12 files):
→ Minimum + 04_README + 09_camera + 10_styles + 14_ADW + 15-17_HOPs

**Complete** (20 files):
→ All files for full context

---

## MODEL RECOMMENDATIONS

| Task | Model |
|------|-------|
| Prompt Generation | GPT-5 thinking / Claude Sonnet 4.5+ |
| Image Generation | Midjourney V6 / DALL-E 3 / Imagen 3 |
| Quick Tasks | GPT-4o / Claude Haiku |

---

## 12 LEVERAGE POINTS STATUS

| Point | Status |
|-------|--------|
| 1. Context | ✅ Auto-navigation in QUICK_START |
| 2. Model | ✅ Recommendations in PRIME |
| 3. Prompt | ✅ TAC-7 HOPs (15-19) |
| 4. Tools | ✅ Validators + schemas |
| 5. Standard Out | ✅ Task boundaries in ADW |
| 6. Types | ✅ 4 JSON schemas |
| 7. Documentation | ✅ README + SETUP |
| 8. Tests | ✅ 13-point checklist |
| 9. Architecture | ✅ Dual-Layer ADW+HOP |
| 10. Plans | ✅ Execution modes |
| 11. Templates | ✅ output_template v3.2.0 |
| 12. ADWs | ✅ 5-phase workflow |

---

**Version**: 2.5.0 | **OPOP**: 10/10 | **Chars**: ~6800/8000 | **Updated**: 2025-11-25

**Next Steps**: Read 02_PRIME → 03_INSTRUCTIONS → 12_output_template → Generate 2 copyable prompts

**CRITICAL**: Scene 9 ALWAYS white background #FFFFFF (marketplace compliance)
