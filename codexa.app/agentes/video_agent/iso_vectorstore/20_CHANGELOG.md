# CHANGELOG | video_agent

All notable changes to this agent are documented in this file.

---

## [2.5.0] - 2025-11-25

### Added
- 12 Leverage Points framework implementation
- `07_output_template.md` - Trinity output specification
- `08_video_rules.json` - Video production methodology
- `09_platform_specs.json` - Consolidated platform specs (6 platforms + 5 social)
- `10_production_patterns.json` - Scripts, transitions, hooks, narrative arcs
- `12_execution_plans.json` - Full/Quick/Batch/Campaign plans
- `20_CHANGELOG.md` - Version history
- Task boundaries pattern for progress visibility
- Mental checklist in QUICK_START

### Changed
- iso_vectorstore restructured to 20 numbered files
- PRIME.md updated to v2.5.0 with 12 Leverage Points
- INSTRUCTIONS.md updated to v2.5.0 with task boundaries
- README.md updated to v2.5.0 with new architecture
- Platform documentation consolidated (6 files -> 1 JSON)
- ADW_orchestrator moved to position 11
- Voice library moved to position 13
- Video modes moved to position 14

### Fixed
- Version sync across all documentation files
- Duplicate files between root and iso_vectorstore
- Missing execution_plans.json

### Deprecated
- Individual platform markdown files (use 09_platform_specs.json)
- Files 21-22 renumbered to 13-14

---

## [2.0.0] - 2025-11-25

### Added
- Pre-flight phase with auto-selection logic
- Post-validation phase with 11-point checklist
- Video modes: "overlay" vs "clean" (--NO TEXT)
- PT-BR voice library (8 ElevenLabs voices)
- Complete test suite with fixtures
- Production templates (brand_story, product_demo, social_ad)
- Trinity output example with full documentation
- PROCESSADOS/ knowledge cards (6 documents)
- iso_vectorstore enriched (22 files)
- Voice auto-selection by tom/gender
- config/voice_config.json
- config/video_modes.json

### Changed
- Pipeline expanded: 5 phases -> 7 phases
- Script phase: mode-aware text overlay logic
- Visual phase: composition by video_mode
- Editing phase: conditional text rendering

---

## [1.0.0] - 2025-11-24

### Added
- Initial release
- 5-stage pipeline: Concept -> Script -> Visual -> Production -> Editing
- Runway Gen-3 integration (primary)
- Pika 1.5 integration (fallback)
- ElevenLabs TTS integration
- FFmpeg editing pipeline
- Trinity output format (.mp4, .llm.json, .meta.json)
- 5 builders (01-05)
- 5 HOPs (10-50)
- 3 validators
- Input/output JSON schemas
- Video styles configuration
- API configuration
- Platform knowledge base (6 platforms)
- Prompt engineering knowledge (anatomy, camera, lighting, magic words)
- Brand alignment system

### Technical
- Claude Sonnet 4 for concept/script (reasoning)
- Claude Haiku for visual/validation (fast)
- Async parallel video generation
- 11-point quality validation
- Cost tracking per video

---

## Version Numbering

- **Major (X.0.0)**: Breaking changes, architecture shifts
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, documentation

---

## Upgrade Path

### 1.0.0 -> 2.0.0
1. Add voice_config.json and video_modes.json to config/
2. Update script builder for mode-awareness
3. Update visual builder for composition modes
4. Add pre-flight and post-validation phases
5. Sync iso_vectorstore with new files

### 2.0.0 -> 2.5.0
1. Restructure iso_vectorstore (22 -> 20 files)
2. Add new JSON spec files (07, 08, 09, 10, 12)
3. Update PRIME.md with 12 Leverage Points
4. Add task boundaries to workflows
5. Add execution plans (full/quick/batch/campaign)

---

## Quality Metrics by Version

| Version | Quality Score | Files | iso_vectorstore |
|---------|---------------|-------|-----------------|
| 1.0.0 | TBD | ~40 | 20 |
| 2.0.0 | 9.2/10 | ~55 | 22 |
| 2.5.0 | 9.5/10 | ~55 | 20 |

---

**Agent**: video_agent
**Type**: Specialist Agent
**Domain**: AI Video Production
**Created**: 2025-11-24
**Last Updated**: 2025-11-25
