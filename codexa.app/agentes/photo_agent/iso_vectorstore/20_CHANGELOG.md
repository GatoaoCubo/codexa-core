# photo_agent | CHANGELOG

All notable changes to photo_agent documented here.

---

## [2.5.0] - 2025-11-25 - 12 LEVERAGE POINTS UPGRADE

### Added - 12 Leverage Points Framework
- ✅ **Context** (1): Auto-navigation in 01_QUICK_START.md with file architecture
- ✅ **Model** (2): Recommendations in 02_PRIME.md (GPT-5/Sonnet 4.5+)
- ✅ **Prompt** (3): TAC-7 compliant HOPs (15-19)
- ✅ **Tools** (4): Validators + JSON schemas (05-08)
- ✅ **Standard Out** (5): Task boundaries in 14_ADW_orchestrator.md
- ✅ **Types** (6): 4 JSON schemas (input + 3 output)
- ✅ **Documentation** (7): README + SETUP + CHANGELOG
- ✅ **Tests** (8): 13-point validation checklist
- ✅ **Architecture** (9): Dual-Layer ADW+HOP
- ✅ **Plans** (10): Execution modes (full/quick/single)
- ✅ **Templates** (11): 12_output_template.md v3.2.0
- ✅ **ADWs** (12): 5-phase workflow with task boundaries

### Added - Task Boundaries
- ✅ `SCENE_PLANNING_COMPLETE` - Phase 1 progress
- ✅ `CAMERA_DESIGN_COMPLETE` - Phase 2 progress
- ✅ `PROMPTS_GENERATED` - Phase 3 progress
- ✅ `VALIDATION_COMPLETE` - Phase 4 progress (with score)
- ✅ `OUTPUT_READY` - Phase 5 completion

### Added - Execution Modes
- ✅ **Full** (9 scenes, 10-20min): Complete product photography set
- ✅ **Quick** (3 scenes, 3-5min): Hero + Lifestyle + Marketplace
- ✅ **Single** (1 scene, 1-2min): Specific scene regeneration

### Changed - Version Synchronization
- ✅ 01_QUICK_START.md → v2.5.0
- ✅ 02_PRIME.md → v2.5.0
- ✅ 14_ADW_orchestrator.md → v2.5.0
- ✅ Root PRIME.md → v2.5.0

### Changed - ADW Updates
- ✅ Added $arguments chaining (Phase N → Phase N+1)
- ✅ Updated HOP references to iso_vectorstore paths
- ✅ Removed Trinity output references (deprecated)
- ✅ Added task boundary messages per phase

### Compliance
- ✅ **12 Leverage Points**: 12/12 implemented
- ✅ **iso_vectorstore**: 20 files (01-20)
- ✅ **OPOP Score**: 10/10

---

## [3.2.2] - 2025-11-18

### iso_vectorstore Structure
- ✅ **FIXED**: Consolidated to exactly 20 files (was 23 + workflows/)
- ✅ **REMOVED**: workflows/ subfolder (violates flat structure)
- ✅ **REMOVED**: 20_CODEXA_framework.md (generic, not photo-specific)
- ✅ **REMOVED**: 21_HOP_framework.md (generic framework)
- ✅ **REMOVED**: 22_agent_registry.json (not needed in isolated agent)
- ✅ **CONSOLIDATED**: Brand-aligned workflow into 03_INSTRUCTIONS.md
- ✅ **CREATED**: This CHANGELOG as file 20

### Structure
- 01-04: Core docs (QUICK_START, PRIME, INSTRUCTIONS, README)
- 05-12: Schemas and templates
- 13-19: HOPs and ADW
- 20: This CHANGELOG

**Status**: Production ready, drag & drop compliant

---

## [3.2.1] - 2025-11-18

### Fixed
- ✅ Updated PNG generation commands with tested working solution
- ✅ Added double PNG command to PROMPT 2 for reliability

---

## [3.2.0] - 2025-11-18 - BREAKING CHANGE

### Added - Seed System
- ✅ `{user_image} {seed:[RANDOM]}` prefix in ALL prompts
- ✅ Controlled variation between generations
- ✅ Reproducibility with fixed seeds

### Added - [OPEN_VARIABLES]
- ✅ Randomization ranges: `[f/5.6-f/11]`, `[ISO 100-400]`
- ✅ Multiple options: `[high-key|3-point-soft|natural]`
- ✅ Creative entropy while maintaining structure

### Changed - Scene 9
- **BREAKING**: Scene 9 now ALWAYS white background #FFFFFF
- Marketplace compliance requirement
- Scenes 1+9 both white for ML/Shopee/Amazon

### Added - Auto-PNG Generation
- ✅ Inline commands: "Generate all 9 scenes as..."
- ✅ PROMPT 1: "...single 3x3 grid PNG image in sequence now"
- ✅ PROMPT 2: "...separate PNG images in sequence now"

### Changed - Output Format
- PROMPT 1: 500-800 words (increased from 400-600 due to [OPEN_VARIABLES])
- PROMPT 2: 180-300 words each (increased from 150-250)
- Removed Trinity files (.md + .llm.json + .meta.json)
- Pure copyable prompts only

---

## [3.1.0] - 2025-11-17

### Changed
- ✅ Output format: 2 copyable prompts (Grid 3x3 + 9 Individual)
- ❌ Removed Trinity output files
- ✅ Added `12_output_template.md` with exact format

---

## [3.0.0] - 2025-11-15

### Added
- ✅ Modular workflows system
- ✅ OPOP 10/10 compliance
- ✅ Brand-aligned generation workflow
- ✅ PNL trigger integration

### Changed
- Reduced INSTRUCTIONS.md from 891 → 220 lines
- Separated workflows into dedicated files

---

## [2.3.0] - 2025-11-14

### Added
- ✅ HOP modules (scene_planner, camera_designer, prompt_generator, brand_validator, batch_assembler)
- ✅ ADW orchestrator
- ✅ Photography styles and camera profiles

---

## [2.0.0] - 2025-11-13

### Added
- ✅ iso_vectorstore/ structure (first version)
- ✅ 13 files for external LLM platforms

---

## [1.0.0] - 2025-11-12

### Initial Release
- ✅ Basic photo prompt generation
- ✅ 9-scene workflow
- ✅ Camera and lighting specifications

---

## VERSION SUMMARY

| Version | Date | Highlight |
|---------|------|-----------|
| **2.5.0** | 2025-11-25 | 12 Leverage Points + Task Boundaries |
| 3.2.2 | 2025-11-18 | iso_vectorstore 20-file structure |
| 3.2.0 | 2025-11-18 | Seed system + [OPEN_VARIABLES] |
| 3.1.0 | 2025-11-17 | 2-prompt copyable format |
| 3.0.0 | 2025-11-15 | Modular workflows |
| 2.0.0 | 2025-11-13 | iso_vectorstore structure |
| 1.0.0 | 2025-11-12 | Initial release |

---

## 12 LEVERAGE POINTS COMPLIANCE

| # | Point | Status | File |
|---|-------|--------|------|
| 1 | Context | ✅ | 01_QUICK_START.md |
| 2 | Model | ✅ | 02_PRIME.md |
| 3 | Prompt | ✅ | 15-19_HOPs |
| 4 | Tools | ✅ | validators/ |
| 5 | Standard Out | ✅ | 14_ADW (boundaries) |
| 6 | Types | ✅ | 05-08_schemas |
| 7 | Documentation | ✅ | 04_README, 13_SETUP |
| 8 | Tests | ✅ | 13-point checklist |
| 9 | Architecture | ✅ | Dual-Layer ADW+HOP |
| 10 | Plans | ✅ | Execution modes |
| 11 | Templates | ✅ | 12_output_template |
| 12 | ADWs | ✅ | 14_ADW_orchestrator |

**Compliance Score**: 12/12 (100%)

---

**Current Version**: 2.5.0
**iso_vectorstore Status**: 20 files, flat structure, production ready
**Last Updated**: 2025-11-25
