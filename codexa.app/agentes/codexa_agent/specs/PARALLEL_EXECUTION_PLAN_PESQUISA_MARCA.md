# Parallel Execution Plan | pesquisa_agent + marca_agent

**Created**: 2025-11-30
**Workflow**: ADW-104 v2.1.0 (ISO_VECTORSTORE_OPTIMIZATION)
**Baseline**: anuncio_agent v3.5.0 (-90% tokens, single code block)

---

## EXECUTIVE SUMMARY

| Agent | Files | Target | Issues | Priority |
|-------|-------|--------|--------|----------|
| pesquisa_agent | 30 | 21 | Duplicate numbering (9 pairs), missing MANIFEST | HIGH |
| marca_agent | 32 | 21 | Severe duplicates, numbers to 27, .py in vectorstore | HIGH |

**Estimated Duration**: 4-6h per agent (parallel execution possible)

---

## AGENT 1: pesquisa_agent

### Current State
```yaml
version: 2.7.0
scope: RESEARCH
generates: [research_notes.md, metadata.json, queries.json]
delegates: [ad_copy → anuncio_agent, brand → marca_agent]
file_count: 30
missing: 00_MANIFEST.md
```

### Issues Detected

#### 1. Duplicate Numbering (9 pairs)
| Number | File A | File B |
|--------|--------|--------|
| 06 | 06_agent_config.json | 06_input_schema.json |
| 10 | 10_agent.json | 10_HOP_main.md |
| 11 | 11_HOP_competitor.md | 11_ADW_orchestrator.md |
| 13 | 13_marketplace_analysis.md | 13_HOP_competitor_analysis.md |
| 14 | 14_competitor_tracking.md | 14_HOP_gap_identification.md |
| 15 | 15_trend_analysis.md | 15_HOP_image_analysis.md |
| 16 | 16_research_templates.md | 16_HOP_intake_validation.md |
| 17 | 17_output_formats.md | 17_HOP_main_agent.md |
| 18 | 18_quality_gates.md | 18_HOP_price_comparison.md |
| 19 | 19_research_framework.md | 19_HOP_sentiment_analysis.md |

#### 2. Scattered HOPs
HOPs found at: 10, 11, 13-19 (inconsistent placement)

#### 3. Missing Files
- 00_MANIFEST.md
- SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md

### Optimization Plan

#### Phase 1: DISCOVERY (30min)
1.1. List all 30 files with sizes
1.2. Estimate tokens per file
1.3. Categorize: Core (01-05), Config (06-10), HOPs (11+), Reference

#### Phase 2: SCOPE ANALYSIS (15min)
2.1. Read PRIME.md (done - v2.7.0, RESEARCH scope)
2.2. Identify out-of-scope files (visual, audio, etc.)
2.3. Map what pesquisa GENERATES vs DELEGATES

#### Phase 3: RESOLUTION (2h)

**Numbering Resolution**:
```
Keep (Standard) | Delete/Merge (Duplicate)
----------------|-------------------------
06_input_schema.json | DELETE 06_agent_config.json (merge into input_schema)
10_agent.json → MERGE into 06 | KEEP 10 slot for HOP
11_ADW_orchestrator.md | DELETE 11_HOP_competitor.md (move to 14)
```

**New File Structure** (target 21):
```
00_MANIFEST.md                    # CREATE
01_QUICK_START.md                 # KEEP
02_PRIME.md                       # KEEP
03_INSTRUCTIONS.md                # KEEP
04_README.md                      # KEEP
05_ARCHITECTURE.md                # KEEP
06_input_schema.json              # KEEP (merge agent_config)
07_brief_schema.json              # KEEP
08_execution_plan.json            # KEEP
09_marketplaces.json              # KEEP
10_research_config.json           # MERGE from 10_agent.json
11_ADW_orchestrator.md            # KEEP
12_execution_plans.json           # CREATE or rename
13_HOP_main_agent.md              # RENAME from 17_HOP_main_agent.md
14_HOP_competitor_analysis.md     # RENAME from 13_HOP_competitor_analysis.md
15_HOP_gap_identification.md      # RENAME from 14_HOP_gap_identification.md
16_HOP_intake_validation.md       # KEEP
17_HOP_price_comparison.md        # RENAME from 18_HOP_price_comparison.md
18_HOP_qa_validation.md           # CREATE or rename
19_frameworks.md                  # MERGE from 19_research_framework.md
20_quality_dimensions.json        # CREATE
```

**Files to DELETE** (9):
- 06_agent_config.json (merge)
- 10_agent.json (merge)
- 10_HOP_main.md (duplicate)
- 11_HOP_competitor.md (move content)
- 13_marketplace_analysis.md (merge into frameworks)
- 14_competitor_tracking.md (merge)
- 15_trend_analysis.md (merge into frameworks)
- 16_research_templates.md (merge)
- 17_output_formats.md (merge)
- 18_quality_gates.md (merge)
- 20_CHANGELOG.md (keep in parent, not iso)

#### Phase 4: HOP OPTIMIZATION (2h)
- Audit each HOP for token count
- Target: < 1500 tokens per HOP
- Remove YAML injection, duplicates
- Apply pattern from anuncio_agent HOPs

#### Phase 5: GENERATION (1h)
5.1. Generate 00_MANIFEST.md using template
5.2. Generate SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md
5.3. Apply lessons learned (8.5-8.8):
    - Verify file references
    - Add OUTPUT FORMAT section
    - Add single code block rules
    - Add CRITICAL self-validation

#### Phase 6: VALIDATION (30min)
- File count <= 21
- Token estimate < 15,000
- Version consistency 100%
- All HOPs < 1500 tokens

---

## AGENT 2: marca_agent

### Current State
```yaml
version: 2.5.1
scope: BRAND_STRATEGY
generates: [brand_strategy.md, validation_report.txt, metadata.json]
delegates: [ad_copy → anuncio_agent]
file_count: 32
missing: 00_MANIFEST.md
```

### Issues Detected

#### 1. Severe Duplicate Numbering
| Number | File A | File B |
|--------|--------|--------|
| 09 | 09_output_template.md | 09_brand_strategy_ecomlm.json |
| 11 | 11_color_psychology.json | 11_ADW_orchestrator.md |
| 13 | 13_storytelling_frameworks.json | 13_HOP_brand_identity.md |
| 14 | 14_HOP_brand_builder.md | 14_HOP_main_agent.md |
| 20 | 20_ADW_brand_workflow.md | 20_CHANGELOG.md |

#### 2. Multiple ADW Files
- 11_ADW_orchestrator.md
- 16_ADW_orchestrator.md (duplicate!)
- 20_ADW_brand_workflow.md

#### 3. Multiple CHANGELOGs
- 20_CHANGELOG.md
- 27_CHANGELOG.md

#### 4. Python File in iso_vectorstore
- 18_brand_validator.py (should be in src/)

#### 5. Numbers Go to 27
Files numbered up to 27 (target max: 21)

### Optimization Plan

#### Phase 1: DISCOVERY (30min)
1.1. List all 32 files with sizes
1.2. Estimate tokens per file
1.3. Identify large JSON files (color_psychology, archetypes, etc.)

#### Phase 2: CLEANUP (1h)

**Files to DELETE/MOVE**:
- 16_ADW_orchestrator.md (duplicate of 11)
- 18_brand_validator.py → MOVE to src/
- 20_ADW_brand_workflow.md (merge into 11)
- 20_CHANGELOG.md (keep in parent)
- 27_CHANGELOG.md (duplicate)
- 09_brand_strategy_ecomlm.json (merge or delete)

**Files to MERGE**:
- 11_color_psychology.json + 12_archetype_specs.json → config.json
- 13_storytelling_frameworks.json + 15_identity_patterns.json → patterns.json

#### Phase 3: RENUMBERING (1h)

**New File Structure** (target 21):
```
00_MANIFEST.md                    # CREATE
01_QUICK_START.md                 # KEEP
02_PRIME.md                       # KEEP
03_INSTRUCTIONS.md                # KEEP
04_README.md                      # KEEP
05_ARCHITECTURE.md                # KEEP
06_input_schema.json              # KEEP
07_output_template.md             # RENAME from 09
08_brand_rules.json               # RENAME from 10
09_brand_strategy_config.json     # MERGE (archetypes + psychology)
10_brand_patterns.json            # MERGE (storytelling + identity)
11_ADW_orchestrator.md            # KEEP (merge 16, 20)
12_execution_plans.json           # RENAME from 19
13_HOP_main_agent.md              # RENAME from 22 or 14
14_HOP_brand_identity.md          # RENAME from 21 or 13
15_HOP_brand_builder.md           # RENAME from 14
16_HOP_visual_identity.md         # CREATE from 25 content
17_HOP_brand_narrative.md         # CREATE from 26 content
18_HOP_qa_validation.md           # CREATE
19_frameworks.md                  # MERGE from positioning + storytelling
20_quality_dimensions.json        # CREATE
```

#### Phase 4: HOP OPTIMIZATION (2h)
- Create concise HOPs (currently missing structured HOPs)
- Target: < 1500 tokens per HOP
- Apply anuncio_agent HOP structure

#### Phase 5: GENERATION (1h)
5.1. Generate 00_MANIFEST.md
5.2. Generate SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md
5.3. Apply lessons learned (8.5-8.8)

#### Phase 6: VALIDATION (30min)
- File count <= 21
- Token estimate < 15,000
- Version consistency 100%

---

## PARALLEL EXECUTION STRATEGY

### Execution Order
```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: DISCOVERY                        │
│  [pesquisa_agent]              [marca_agent]                │
│  - List 30 files               - List 32 files              │
│  - Token audit                 - Token audit                │
│  Duration: 30min each (parallel)                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 2: CLEANUP                          │
│  [pesquisa_agent]              [marca_agent]                │
│  - Resolve 9 duplicates        - Remove .py, duplicates     │
│  - Merge configs               - Merge large JSONs          │
│  Duration: 1-2h each (parallel)                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 3: RENUMBER                         │
│  [pesquisa_agent]              [marca_agent]                │
│  - 30 → 21 files               - 32 → 21 files              │
│  - Clean HOP sequence          - Create missing HOPs        │
│  Duration: 1h each (parallel)                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 4: HOP OPTIMIZATION                 │
│  [pesquisa_agent]              [marca_agent]                │
│  - 7 HOPs to optimize          - Create 6 HOPs from scratch │
│  - Target: <1500 tokens each   - Apply standard structure   │
│  Duration: 2h each (parallel)                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 5: GENERATION                       │
│  [pesquisa_agent]              [marca_agent]                │
│  - 00_MANIFEST.md              - 00_MANIFEST.md             │
│  - SYSTEM_INSTRUCTIONS         - SYSTEM_INSTRUCTIONS        │
│  - Apply lessons 8.5-8.8       - Apply lessons 8.5-8.8      │
│  Duration: 1h each (parallel)                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 6: VALIDATION                       │
│  [Both agents simultaneously]                                │
│  - File count <= 21                                          │
│  - Tokens < 15,000                                          │
│  - Version 100% consistent                                  │
│  - Report generated                                          │
│  Duration: 30min total                                      │
└─────────────────────────────────────────────────────────────┘
```

### Git Strategy
```bash
# Create feature branches
git checkout -b feat/optimize-pesquisa-iso
git checkout -b feat/optimize-marca-iso

# Commit pattern per phase
git commit -m "feat(pesquisa_agent): phase 1 - discovery audit"
git commit -m "feat(pesquisa_agent): phase 2 - cleanup duplicates"
git commit -m "feat(pesquisa_agent): phase 3 - renumber to 21 files"
git commit -m "feat(pesquisa_agent): phase 4 - optimize HOPs"
git commit -m "feat(pesquisa_agent): phase 5 - generate MANIFEST + SYSTEM_INSTRUCTIONS"
git commit -m "feat(pesquisa_agent): phase 6 - validation PASS"

# Same for marca_agent
```

---

## SUCCESS CRITERIA

### pesquisa_agent
- [ ] 30 → 21 files
- [ ] 0 duplicate numbers
- [ ] 00_MANIFEST.md present
- [ ] SYSTEM_INSTRUCTIONS present
- [ ] All HOPs < 1500 tokens
- [ ] Version consistency 100%
- [ ] Token estimate < 15,000

### marca_agent
- [ ] 32 → 21 files
- [ ] 0 duplicate numbers
- [ ] No .py files in iso_vectorstore
- [ ] 00_MANIFEST.md present
- [ ] SYSTEM_INSTRUCTIONS present
- [ ] All HOPs < 1500 tokens
- [ ] Version consistency 100%
- [ ] Token estimate < 15,000

---

## LESSONS APPLIED (from anuncio_agent)

### Pattern 1: File Name Verification (8.5)
- Cross-reference ALL file names in SYSTEM_INSTRUCTIONS
- Use hybrid format: `{number}_{name}.md`
- Complete DOCUMENT REFERENCE table

### Pattern 2: Output Format (8.6)
- Add "REGRA ABSOLUTA: UM ÚNICO CODE BLOCK"
- Template with triple backticks
- PROIBIDO list

### Pattern 3: Constraints Update (8.7)
- ALWAYS output inside ONE code block
- NEVER duplicate content
- NEVER output text outside

### Pattern 4: Self-Validation (8.8)
- CRITICAL checks for code block
- No text outside check
- No duplication check

### Pattern 5: Token Optimization
- Batch code interpreter calls (<=5)
- Disable web search when URL provided
- Never emit empty reasoning blocks

---

**Version**: 1.0.0
**Workflow**: ADW-104 v2.1.0
**Author**: codexa_agent
**Date**: 2025-11-30
