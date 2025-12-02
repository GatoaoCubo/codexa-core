<!-- iso_vectorstore -->
<!--
  Source: INSTRUCTIONS.md
  Agent: curso_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# INSTRUCTIONS | CODEXA Curso Agent v2.0.0

**Version**: 2.0.0
**Purpose**: Instructions for AI assistants to use curso_agent meta-constructor
**Type**: HOP (Higher-Order Prompt) for LLM execution
**Updated**: 2025-11-21

---

## CORE PURPOSE

**Educational content meta-constructor** for creating comprehensive Hotmart courses about CODEXA E-COM LM system.

**Use this agent when**: Building courses, generating video scripts, creating workbooks, designing sales materials for Hotmart platform.

**Output**: Trinity format (.md + .llm.json + .meta.json)

---

## ARCHITECTURE (12 CODEXA Pillars)

### 4 IN-AGENT Pillars

| Pillar | Description |
|--------|-------------|
| **Contexto** | CODEXA system (6 agents), e-commerce, Brazilian market |
| **Modelo** | GPT-4o / Claude Sonnet 4.5+ with reasoning |
| **Tools** | 5 builders + 5 validators |
| **Prompts** | 5 HOPs in TAC-7 format |

### 8 OUT-AGENT Pillars

| Pillar | Description |
|--------|-------------|
| **Templates** | 4 templates with 197 [OPEN_VARIABLES] |
| **Output** | Trinity format (.md + .llm.json + .meta.json) |
| **Types** | Layer 1 → 2 → 3 progression |
| **Docs** | PRIME, INSTRUCTIONS, SETUP, README |
| **Tests** | 5 validators with quality thresholds |
| **Architecture** | Progressive pedagogy |
| **Plans** | Course outlines with timing |
| **ADWs** | 3 workflows (Quick/Full/Sales) |

---

## AI ASSISTANT WORKFLOW

### Discovery-First Pattern

```bash
# 1. SCAN: Check available infrastructure
ls builders/*.py
ls validators/*.py
ls commands/*.md

# 2. LOAD: Read context
cat context/00_INDICE_CURSO_CODEXA.md

# 3. EXECUTE: Run builder
python builders/02_video_script_builder.py --module 01 --verbose

# 4. VALIDATE: Check quality
python validators/01_content_quality_validator.py --file outputs/video_scripts/01_*.md

# 5. VERIFY: Check output
ls outputs/video_scripts/
```

### When to Use

**USE curso_agent for**:
- Building CODEXA courses for Hotmart
- Generating video scripts (15-30min)
- Creating student workbooks (8-15 pages)
- Designing sales materials (landing, emails, ads)
- Validating content quality (4 checklists)
- Packaging for Hotmart deployment

**DO NOT use for**:
- Actual CODEXA agent usage (use specialized agents)
- Market research (use /prime-pesquisa)
- Brand strategy (use /prime-marca)
- Product listings (use /prime-anuncio)

---

## KEY FILES

### Core Documentation
| File | Purpose |
|------|---------|
| PRIME.md | Agent philosophy and instructions |
| README.md | Overview and quick start |
| INSTRUCTIONS.md | This file - AI integration guide |
| SETUP.md | Platform deployment guide |

### Builders (builders/)
| File | Purpose |
|------|---------|
| 01_course_outline_builder.py | Course structure |
| 02_video_script_builder.py | Video scripts (CORE) |
| 03_workbook_builder.py | Student workbooks |
| 04_sales_collateral_builder.py | Sales materials |
| 05_hotmart_package_builder.py | Hotmart packaging |

### Validators (validators/)
| File | Threshold | Checks |
|------|-----------|--------|
| 01_content_quality_validator.py | >=7.0 | Hook, timing, objectives |
| 02_brand_voice_validator.py | >=7.0 | Seed words, tone |
| 03_pedagogical_validator.py | >=7.0 | Complexity, exercises |
| 04_technical_validator.py | >=7.0 | [OPEN_VARIABLES], examples |
| 05_hotmart_compliance_validator.py | >=8.0 | DRM, LGPD, specs |

### HOPs (prompts/)
| File | Format |
|------|--------|
| HOP_VIDEO_SCRIPT.md | TAC-7 |
| HOP_WORKBOOK.md | TAC-7 |
| HOP_SALES_COPY.md | TAC-7 |
| HOP_EMAIL_SEQUENCE.md | TAC-7 |
| HOP_LANDING_PAGE.md | TAC-7 |

### Templates (templates/)
| File | [OPEN_VARIABLES] |
|------|------------------|
| TEMPLATE_VIDEO_SCRIPT.md | 21 |
| TEMPLATE_WORKBOOK.md | 32 |
| TEMPLATE_SALES_PAGE.md | 67 |
| TEMPLATE_EMAIL_SEQUENCE.md | 77 |

---

## WORKFLOWS (ADW)

### Quick Course (5-10 min)
```
Plan → Build outline → Test → Review → Document
```

### Full Module (30-45 min)
```
Plan → Build script + workbook → Test (4 validators) → Review → Document
```

### Sales Package (20-30 min)
```
Plan → Build sales + package → Test (2 validators) → Review → Document
```

---

## QUALITY VALIDATION

### Thresholds
| Validator | Minimum Score |
|-----------|---------------|
| Content Quality | >= 7.0/10.0 |
| Brand Voice | >= 7.0/10.0 |
| Pedagogical | >= 7.0/10.0 |
| Technical | >= 7.0/10.0 |
| Hotmart Compliance | >= 8.0/10.0 |

### Running Validators
```bash
# Single file
python validators/01_content_quality_validator.py --file [PATH] --verbose

# All outputs
python validators/01_content_quality_validator.py --file outputs/video_scripts/*.md
```

---

## INTEGRATION

### Dependencies
| Agent | Provides |
|-------|----------|
| pesquisa_agent | Market research data |
| marca_agent | Brand voice guidelines |
| anuncio_agent | Copywriting patterns |

### Output Location
```
outputs/
├── video_scripts/   # .md + .llm.json + .meta.json
├── workbooks/       # .md + .llm.json + .meta.json
├── sales/           # .md + .llm.json + .meta.json
└── hotmart_package/ # MANIFEST.json + README_DEPLOY.md
```

---

## BEST PRACTICES

1. **Load context first**: Read context/ files before generating
2. **Use builders**: Run Python builders for consistent output
3. **Validate always**: Run validators after each generation
4. **Trinity output**: Always generate .md + .llm.json + .meta.json
5. **[OPEN_VARIABLES]**: Include >=2 per module for customization

---

**Status**: Production | **Version**: 2.0.0 | **Quality Score**: 9.5/10
