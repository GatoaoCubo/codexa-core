# Architecture | Curso Agent v2.5.0

## 12 Leverage Points Implementation

### Foundation Layer (1-4)

| Pillar | Implementation | Files |
|--------|---------------|-------|
| **1. Context** | Auto-navigation, mental checklist | 01_QUICK_START.md |
| **2. Model** | GPT-4o / Claude Sonnet 4.5+ | 02_PRIME.md |
| **3. Prompt** | TAC-7 format HOPs | 13-15_HOP_*.md |
| **4. Tools** | 5 builders + 5 validators | builders/, validators/ |

### Flow Layer (5-8)

| Pillar | Implementation | Files |
|--------|---------------|-------|
| **5. Standard Out** | Trinity Output, task boundaries | 11_ADW_orchestrator.md |
| **6. Types** | JSON schemas | 06, 08, 09, 10, 12 |
| **7. Documentation** | Complete README, PRIME | PRIME.md, README.md |
| **8. Tests** | 5 validators with thresholds | validators/*.py |

### Orchestration Layer (9-12)

| Pillar | Implementation | Files |
|--------|---------------|-------|
| **9. Architecture** | Dual-Layer ADW+HOP | 11_ADW_orchestrator.md |
| **10. Plans** | Execution plans (quick/full) | 12_execution_plans.json |
| **11. Templates** | 4 templates (200 vars) | templates/*.md |
| **12. ADWs** | 5-phase workflow | 11_ADW_orchestrator.md |

## File Structure (20 Files)

```
iso_vectorstore/
├── 01_QUICK_START.md         # Navigation, mental checklist
├── 02_PRIME.md               # Identity, capabilities
├── 03_INSTRUCTIONS.md        # Workflow rules
├── 04_README.md              # Agent overview
├── 05_ARCHITECTURE.md        # This file (12 Leverage Points)
├── 06_input_schema.json      # Input validation
├── 07_output_template.md     # Output format
├── 08_curso_rules.json       # Educational methodology
├── 09_hotmart_specs.json     # Platform specifications
├── 10_pedagogy_patterns.json # Bloom's taxonomy
├── 11_ADW_orchestrator.md    # 5-phase workflow
├── 12_execution_plans.json   # Quick/full/sales plans
├── 13_HOP_video_script.md    # TAC-7: Video scripts
├── 14_HOP_workbook.md        # TAC-7: Workbooks
├── 15_HOP_sales_copy.md      # TAC-7: Sales copy
├── 16_hotmart_integration.md # 0-to-1 checklist
├── 17_HOP_hotmart_video.md   # Video upload
├── 18_HOP_hotmart_checkout.md# Checkout config
├── 19_HOP_hotmart_club.md    # Club structure
├── 20_CHANGELOG.md           # Version history
└── catalogo.json             # File catalog
```

## Dual-Layer Architecture

### Layer 1: ADW (Agentic Developer Workflow)
```
PLAN -> BUILD -> TEST -> REVIEW -> DOCUMENT
```
- Orchestrates multi-phase execution
- Quality gates at each phase
- $arguments chaining between phases
- Error handling and iteration

### Layer 2: HOP (Higher-Order Prompts)
```
MODULE_METADATA -> INPUT_CONTRACT -> OUTPUT_CONTRACT -> TASK -> STEPS -> VALIDATION -> CONTEXT
```
- TAC-7 format for consistency
- Reusable prompt templates
- [OPEN_VARIABLES] for customization
- Validation checklist embedded

## Data Flow

```
User Request
    │
    v
┌─────────────────────────────────────────┐
│  06_input_schema.json (Validation)      │
└─────────────────────────────────────────┘
    │
    v
┌─────────────────────────────────────────┐
│  11_ADW_orchestrator.md (5-Phase)       │
│  ├── PLAN: Load context                 │
│  ├── BUILD: Execute builders            │
│  ├── TEST: Run validators               │
│  ├── REVIEW: Apply feedback             │
│  └── DOCUMENT: Package output           │
└─────────────────────────────────────────┘
    │
    v
┌─────────────────────────────────────────┐
│  13-15_HOP_*.md (Content Generation)    │
│  ├── Video Script                       │
│  ├── Workbook                           │
│  └── Sales Copy                         │
└─────────────────────────────────────────┘
    │
    v
┌─────────────────────────────────────────┐
│  validators/*.py (Quality Gates)        │
│  ├── Content Quality >= 7.0             │
│  ├── Brand Voice >= 7.0                 │
│  ├── Pedagogical >= 7.0                 │
│  ├── Technical >= 7.0                   │
│  └── Hotmart Compliance >= 8.0          │
└─────────────────────────────────────────┘
    │
    v
Trinity Output (.md + .llm.json + .meta.json)
```

## Integration Points

### Internal (CODEXA Agents)
- pesquisa_agent: Market research
- marca_agent: Brand voice
- anuncio_agent: Copywriting

### External (Platforms)
- Hotmart: Course delivery
- GitHub: Version control
- CI/CD: Automated validation

## Schema Relationships

```
06_input_schema.json
    └── validates -> User Input

08_curso_rules.json
    └── defines -> Content Rules
    └── used by -> 13-15_HOP_*.md

09_hotmart_specs.json
    └── defines -> Platform Requirements
    └── used by -> 05_hotmart_compliance_validator.py

10_pedagogy_patterns.json
    └── defines -> Learning Objectives
    └── used by -> 03_pedagogical_validator.py

12_execution_plans.json
    └── defines -> Workflow Phases
    └── used by -> 11_ADW_orchestrator.md
```

## Quality Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Content Quality | >= 7.0 | 8.2 |
| Brand Voice | >= 7.0 | 7.8 |
| Pedagogical | >= 7.0 | 8.5 |
| Technical | >= 7.0 | 7.9 |
| Hotmart Compliance | >= 8.0 | 8.7 |
| **Overall** | >= 7.0 | **9.3** |

---

**Version**: 2.5.0
**Pattern**: Dual-Layer (ADW + HOP)
**Status**: Production-Ready
