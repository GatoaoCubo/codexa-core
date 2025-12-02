# MANIFEST | marca_agent iso_vectorstore v3.1.0

**Package**: iso_vectorstore (drag-and-drop for any LLM)
**Agent**: marca_agent | **Version**: 3.1.0 | **Date**: 2025-11-30
**Scope**: BRAND_STRATEGY (Brazilian e-commerce brand identities)
**Output**: brand_strategy.md (32 blocks) + validation_report.txt + metadata.json
**Files**: 20 | **Total Tokens**: ~51,500 (optimized from ~124,000)

---

## DEPLOY CHECKLIST

```
[ ] Upload 20 arquivos ao vector store / file search
[ ] Upload brand_validator.py ao Code Interpreter (separado - em src/)
[ ] Aplicar config preset (STANDARD ou QUICK)
[ ] Testar com brief de produto
[ ] Verificar brand_strategy.md output (32 blocks)
```

---

## FILE INVENTORY (20 Files)

### Core (00-05) ~18,000 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Package inventory |
| 01 | QUICK_START.md | ~1,300 | LLM entry point |
| 02 | PRIME.md | ~4,900 | Agent identity + framework |
| 03 | INSTRUCTIONS.md | ~2,300 | Workflow rules |
| 04 | README.md | ~6,800 | Full documentation |
| 05 | ARCHITECTURE.md | ~3,300 | Tech architecture |

### Config (06-10) ~9,500 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 06 | input_schema.json | ~1,600 | Input validation |
| 07 | quick_tips.md | ~1,800 | Brand tips reference |
| 08 | brand_strategy.json | ~1,800 | Strategy schema |
| 09 | output_template.md | ~2,300 | Output format |
| 10 | brand_rules.json | ~2,300 | ANVISA/INMETRO/CONAR rules |

### Execution (11-12) ~8,500 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 11 | ADW_orchestrator.md | ~5,600 | 5-phase workflow manager |
| 12 | execution_plans.json | ~3,000 | Full/Quick plans |

### HOPs (13-14) ~1,500 tokens (OPTIMIZED from ~12,000)

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 13 | HOP_brand_identity.md | ~700 | Brand identity generation |
| 14 | HOP_main_agent.md | ~800 | Main orchestrator |

### Reference (15-18) ~12,000 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 15 | brand_archetypes.md | ~3,600 | 12 archetype definitions |
| 16 | positioning_framework.md | ~3,000 | Ries & Trout framework |
| 17 | visual_identity.md | ~2,500 | Visual guidelines |
| 18 | messaging_guide.md | ~2,700 | Tone of voice guide |

### Separado (Code Interpreter / Validation)

| File | Location | Purpose |
|------|----------|---------|
| brand_validator.py | src/ | Brand consistency validation (32 blocks) |
| validate_iso.py | root | ISO vectorstore compliance validator |

---

## SCOPE (BRAND_STRATEGY)

### GENERATES
- Brand Names: 3 options (descriptive, evocative, creative)
- Taglines: 3 x 40-60 chars
- Archetype: Primary + Secondary from 12 options
- Positioning: UVP, target segment, differentiation
- Tone of Voice: 4 dimensions, do's/don'ts
- Visual Identity: Colors (HEX/RGB), typography, mood boards
- Narrative: Origin story, mission, vision, values
- Guidelines: Compliance, consistency checklist

### DELEGATES
- Mood board images → photo_agent
- Ad copy → anuncio_agent

---

## QUALITY GATES (8 Validations)

| Gate | Threshold | Description |
|------|-----------|-------------|
| Consistency Score | >= 0.85 | Brand coherence |
| Uniqueness Score | >= 8.0/10 | Differentiation |
| WCAG Contrast | Level AA | Color accessibility |
| Tagline Chars | 40-60 | Length compliance |
| Seed Words | >= 2 | Proprietary vocabulary |
| Tone Alignment | 95% | Archetype match |
| Compliance | PASS | ANVISA/INMETRO/CONAR |
| Values | Non-generic | Defensible values |

---

## OUTPUT STRUCTURE (32 Blocks)

```
SECTION 1: BRAND IDENTITY (5 blocks)
- Brand Names, Taglines, Archetype, Traits, Essence

SECTION 2: POSITIONING (5 blocks)
- UVP, Target, Differentiation, Promise, Statement

SECTION 3: TONE OF VOICE (5 blocks)
- Dimensions, Style, Do's, Don'ts, Examples

SECTION 4: VISUAL IDENTITY (4 blocks)
- Colors, Typography, Mood Boards, Guidelines

SECTION 5: BRAND NARRATIVE (5 blocks)
- Origin, Mission, Vision, Values, Manifesto

SECTION 6: BRAND GUIDELINES (4 blocks)
- Messaging Do's, Don'ts, Compliance, Checklist

SECTION 7: VALIDATION & AUDIT (4 blocks)
- Consistency Score, Uniqueness Score, Audit, Integration
```

---

## COMPATIBILITY

| Platform | Status |
|----------|--------|
| ChatGPT Responses API | OK |
| Claude Projects | OK |
| OpenAI Assistants | OK |
| Gemini | OK |

---

## CONFIG PRESETS

### STANDARD
```yaml
duration: 15-20min
reasoning_effort: high
validation: full (8 gates)
output: brand_strategy.md (32 blocks)
```

### QUICK
```yaml
duration: 8-12min
reasoning_effort: medium
validation: core (4 gates)
output: brand_strategy.md (essential blocks)
```

---

**Package**: marca_agent iso_vectorstore v3.1.0
**Status**: DEPLOY READY
**Tokens**: ~51,500 (optimized -58% from ~124,000)
**Date**: 2025-11-30 (Platform-Agnostic)
