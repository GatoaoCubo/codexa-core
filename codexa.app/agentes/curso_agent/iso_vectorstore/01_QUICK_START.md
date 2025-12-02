# Quick Start | Curso Agent v2.5.0

## Mental Checklist (Before Starting)

```
[ ] Know what to build? (outline/script/workbook/sales)
[ ] Know which module? (M0-M6)
[ ] Know which layer? (1=Conceito, 2=Pratica, 3=Mestria)
[ ] Context files loaded? (context/0*_MODULO_*.md)
```

## Navigation Map

```
WHAT DO YOU NEED?
│
├─ Course Structure ──────► /curso_outline
│   └─ Input: topic, layer, duration
│   └─ Output: Module outline with objectives
│
├─ Video Script ──────────► /curso_script
│   └─ Input: module_id (01-06)
│   └─ Output: 15-30min script with timing
│   └─ HOP: 13_HOP_video_script.md
│
├─ Student Workbook ──────► /curso_workbook
│   └─ Input: module_id, video_script_path
│   └─ Output: 8-15 page workbook
│   └─ HOP: 14_HOP_workbook.md
│
├─ Sales Materials ───────► /curso_sales
│   └─ Input: course_outline, pricing
│   └─ Output: Landing page, emails, ads
│   └─ HOP: 15_HOP_sales_copy.md
│
├─ Validate Content ──────► /curso_validate
│   └─ Input: generated content path
│   └─ Output: Quality scores (threshold >=7.0)
│
└─ Package for Hotmart ───► /curso_package
    └─ Input: all validated content
    └─ Output: Hotmart-ready package
```

## Fastest Path: Generate Video Script

```bash
# 1. Load context (read module content)
Read: context/01_MODULO_INTRODUCAO.md

# 2. Execute builder
python builders/02_video_script_builder.py --module 01

# 3. Validate output
python validators/01_content_quality_validator.py --file outputs/video_scripts/01_*.md
```

## Key Files Reference

| Need | File | Location |
|------|------|----------|
| Identity & capabilities | 02_PRIME.md | iso_vectorstore/ |
| Workflow rules | 03_INSTRUCTIONS.md | iso_vectorstore/ |
| Input validation | 06_input_schema.json | iso_vectorstore/ |
| Educational rules | 08_curso_rules.json | iso_vectorstore/ |
| Hotmart specs | 09_hotmart_specs.json | iso_vectorstore/ |
| Learning design | 10_pedagogy_patterns.json | iso_vectorstore/ |
| 5-phase workflow | 11_ADW_orchestrator.md | iso_vectorstore/ |
| Execution plans | 12_execution_plans.json | iso_vectorstore/ |

## Quality Thresholds

| Validator | Minimum Score |
|-----------|---------------|
| Content Quality | 7.0 |
| Brand Voice | 7.0 |
| Pedagogical | 7.0 |
| Technical | 7.0 |
| Hotmart Compliance | 8.0 |

## Execution Plans

| Plan | Duration | Use For |
|------|----------|---------|
| quick | 5-10 min | Course outline only |
| full_module | 30-45 min | Complete module content |
| sales_package | 20-30 min | Sales funnel materials |
| complete_course | 4-6 hours | End-to-end course |

## Brand Voice Reminders

**Required Seed Words**: Meta-Construcao, Destilacao de Conhecimento, Cerebro Plugavel

**Forbidden Words**: revolucionario, magico, unico no mercado, garantido

**Tone**: Disruptivo-sofisticado (60% formal, 90% technical)

## Common Patterns

### Video Script Structure
```
HOOK (0:00-1:30) -> OBJECTIVES (1:30-2:00) -> CORE (2:00-25:00) -> RECAP (25:00-28:00) -> CTA (28:00-30:00)
```

### Workbook Structure
```
COVER -> THEORY (2-3p) -> EXERCISES (3-4p) -> PRACTICE (2-3p) -> REFLECTION (1p) -> RESOURCES (1p)
```

### 5-Phase ADW
```
PLAN -> BUILD -> TEST -> REVIEW -> DOCUMENT
```

## Output Format (Trinity)

Every builder produces:
- `.md` - Human-readable content
- `.llm.json` - Structured data for LLM
- `.meta.json` - Metadata and statistics

## Hotmart Video Specs

- **Duration**: 8-12 min (optimal), max 30 min
- **Format**: MP4, H.264, 1080p
- **Hook**: <=90 seconds
- **Timing marks**: Every 2-3 minutes
- **[OPEN_VARIABLES]**: >=2 per module

---

**Version**: 2.5.0 | **Status**: Production-Ready | **Quality**: 9.3/10
