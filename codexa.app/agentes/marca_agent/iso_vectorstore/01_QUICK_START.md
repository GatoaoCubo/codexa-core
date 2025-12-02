# marca_agent | Quick Start Guide v3.0.0

**Version**: 3.0.0 | **Max Chars**: 8000 | **Purpose**: LLM Navigation for Brazilian E-commerce Brand Strategy

---

## IDENTITY

**Agent**: marca_agent
**Domain**: Brand Strategy (Brazilian E-commerce)
**Function**: Transform product briefs into complete brand identities
**Model**: GPT-5 thinking hard OR Claude Sonnet 4.5+ (deep creative reasoning)
**Output**: brand_strategy.md (32 blocks) + validation_report.txt + metadata.json

---

## MENTAL CHECKLIST (Auto-Navigation)

When starting, the LLM should:

```yaml
checklist:
  1_load_context:
    - Read: 02_PRIME.md (identity + capabilities)
    - Read: 03_INSTRUCTIONS.md (workflow rules)
    - Scan: 08_brand_rules.json (methodology)

  2_validate_input:
    - Schema: 06_input_schema.json
    - Required: product_name, category, target_audience, price_range
    - Optional: marketplace_target, competitors, USPs

  3_select_mode:
    - FULL: 5-phase workflow (~15-20min)
    - QUICK: 3-phase positioning (~8-12min)
    - Reference: 12_execution_plans.json

  4_execute_workflow:
    - ADW: 11_ADW_orchestrator.md
    - HOPs: 13_HOP_brand_identity.md, 14_HOP_brand_builder.md

  5_validate_output:
    - Template: 07_output_template.md
    - Quality: Consistency >= 0.85, Uniqueness >= 8.0/10
    - Compliance: ANVISA/INMETRO/CONAR
```

---

## FILE ARCHITECTURE (20 Files)

### Core Navigation (01-05) | Read First
| File | Purpose | Priority |
|------|---------|----------|
| **01_QUICK_START.md** | This file - LLM navigation | CRITICAL |
| **02_PRIME.md** | Identity, philosophy, capabilities | CRITICAL |
| **03_INSTRUCTIONS.md** | Workflow rules, AI instructions | CRITICAL |
| **04_README.md** | Complete documentation | Reference |
| **05_documentation.md** | Architecture details | Reference |

### Schemas & Templates (06-10) | Validation
| File | Purpose | Priority |
|------|---------|----------|
| **06_input_schema.json** | Input validation schema | REQUIRED |
| **07_output_template.md** | Output format template | REQUIRED |
| **08_brand_rules.json** | Branding methodology | REQUIRED |
| **09_archetype_specs.json** | 12 archetypes + voice | REQUIRED |
| **10_identity_patterns.json** | Visual, verbal, values | REQUIRED |

### ADW & HOPs (11-15) | Execution
| File | Purpose | Priority |
|------|---------|----------|
| **11_ADW_orchestrator.md** | 5-phase workflow orchestration | CRITICAL |
| **12_execution_plans.json** | Full/Quick execution plans | CRITICAL |
| **13_HOP_brand_identity.md** | Phase 2: Identity creation | CRITICAL |
| **14_HOP_brand_builder.md** | Phase 3-4: Build + Validate | CRITICAL |
| **15_HOP_main_agent.md** | Main orchestration HOP | Reference |

### Reference Guides (16-20) | Knowledge Base
| File | Purpose | Priority |
|------|---------|----------|
| **16_brand_archetypes.md** | 12 archetypes deep dive | Reference |
| **17_positioning_framework.md** | Ries & Trout, Blue Ocean | Reference |
| **18_visual_identity.md** | Colors, typography, WCAG | Reference |
| **19_messaging_guide.md** | Tone of voice, do's/don'ts | Reference |
| **20_CHANGELOG.md** | Version history | Reference |

---

## EXECUTION MODES

### MODE: FULL (5-Phase ADW)
```
Duration: 15-20 min
Phases: Plan -> Build -> Test -> Review -> Document
Output: 32 structured blocks
Use: New brand from scratch
```

### MODE: QUICK (3-Phase)
```
Duration: 8-12 min
Phases: Plan -> Build -> Validate
Output: Core positioning + identity
Use: Fast positioning, iteration
```

---

## QUICK REFERENCE

### Input Requirements
```json
{
  "required": ["product_name", "category", "target_audience", "price_range"],
  "recommended": ["marketplace_target", "competitors", "USPs"],
  "optional": ["brand_inspirations", "tone_preferences", "research_notes"]
}
```

### Quality Thresholds
```yaml
consistency_score: ">= 0.85"
uniqueness_score: ">= 8.0/10"
tagline_length: "40-60 chars (strict)"
wcag_compliance: "Level AA (>= 2 color pairs)"
seed_words: ">= 2 in critical pieces"
```

### 8 Quality Gates
1. Identity <-> Positioning alignment
2. Archetype <-> Tone consistency
3. Visual <-> Personality coherence
4. Narrative <-> Values harmony
5. Compliance (ANVISA/INMETRO/CONAR)
6. WCAG Contrast validation
7. Seed Words presence
8. Tone Consistency (95% outputs)

---

## INTEGRATION

**Upstream**: User brief -> marca_agent
**Downstream**: brand_strategy.md -> anuncio_agent, pesquisa_agent
**Output Path**: USER_DOCS/Marca/

---

## TASK BOUNDARIES

```yaml
phase_transitions:
  plan_start: "[TASK_BOUNDARY] PHASE 1: PLAN - Starting brief validation"
  build_start: "[TASK_BOUNDARY] PHASE 2: BUILD - Creating brand identity"
  test_start: "[TASK_BOUNDARY] PHASE 3: TEST - Validating consistency"
  review_start: "[TASK_BOUNDARY] PHASE 4: REVIEW - Quality assessment"
  document_start: "[TASK_BOUNDARY] PHASE 5: DOCUMENT - Assembling outputs"
  complete: "[TASK_BOUNDARY] COMPLETE - Brand strategy ready"
```

---

**Version**: 3.0.0 | **Updated**: 2025-11-30 | **Chars**: ~4500/8000

**Next**: Read 02_PRIME.md -> 03_INSTRUCTIONS.md -> Execute via 11_ADW_orchestrator.md
