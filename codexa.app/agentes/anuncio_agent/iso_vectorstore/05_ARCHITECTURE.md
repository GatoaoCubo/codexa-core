# ARCHITECTURE | anuncio_agent v3.2.0

**Purpose**: Technical architecture for TEXT-ONLY e-commerce ad generation
**Version**: 3.2.0 | **Updated**: 2025-11-30 | **Scope**: TEXT-ONLY

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│         (URL / Brief / research_notes from pesquisa_agent)  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              ANUNCIO_AGENT v3.2.0 (TEXT-ONLY)               │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ CONFIG PRESETS                                       │    │
│  │ - EFICIENTE: ~18k tokens, minimal output            │    │
│  │ - PERFORMANCE: ~35k tokens, full quality            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 7-STEP PIPELINE                                      │    │
│  │                                                      │    │
│  │ [1] INPUT → Parse, calculate confidence              │    │
│  │      ↓                                               │    │
│  │ [2] TITULOS → 3 x 58-60 chars, ZERO connectors      │    │
│  │      ↓                                               │    │
│  │ [3] KEYWORDS → 2 blocks x 115-120 terms             │    │
│  │      ↓                                               │    │
│  │ [4] BULLETS → 10 x 250-299 chars                    │    │
│  │      ↓                                               │    │
│  │ [5] DESCRICAO → >= 3,300 chars StoryBrand           │    │
│  │      ↓                                               │    │
│  │ [6] QA → 5D scoring + compliance                    │    │
│  │      ↓                                               │    │
│  │ [7] OUTPUT → 3-PART (Visual + Copyable + JSON)      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT (3-PART)                           │
│                                                              │
│  PART 1: VISUAL REVIEW (display only, QA, scores)           │
│  PART 2: COPYABLE CONTENT (code fence, 1-click copy)        │
│  PART 3: STRUCTURED DATA (JSON, optional)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Scope Definition (v3.1.0+)

### THIS AGENT GENERATES (Text-Only)

| Element | Spec | Source HOP |
|---------|------|------------|
| Titulos | 3 x 58-60 chars, ZERO connectors | HOP 14 |
| Keywords | 2 blocks x 115-120 terms | HOP 15 |
| Bullets | 10 x 250-299 chars | HOP 16 |
| Descricao | >= 3,300 chars, StoryBrand | HOP 17 |

### DELEGATED TO OTHER AGENTS

| Element | Delegate | Reason |
|---------|----------|--------|
| Image prompts | photo_agent | Specialized visual generation |
| Video scripts | video_agent | Specialized video content |
| A/B variations | testing_agent | Statistical optimization |

---

## 5-Dimension Scoring (v3.1.0+)

```
OVERALL SCORE = weighted average of 5 dimensions

| Dimension  | Weight | Threshold | Rationale              |
|------------|--------|-----------|------------------------|
| Titulo     | 30%    | >= 0.75   | Drives CTR, most visible |
| Keywords   | 25%    | >= 0.75   | SEO discoverability    |
| Descricao  | 20%    | >= 0.75   | Converts after click   |
| Bullets    | 15%    | >= 0.75   | Scannable decisions    |
| Compliance | 10%    | >= 0.75   | Binary quality gate    |

PASS: overall >= 0.85
PASS_WITH_WARNINGS: 0.75 <= overall < 0.85
FAIL: overall < 0.75
```

---

## Intelligent Fallback (v3.1.0+)

```
INPUT CONFIDENCE → ACTION

| Confidence | Action                          | Behavior                    |
|------------|--------------------------------|----------------------------|
| >= 0.8     | generate_full                  | Full output, no markers    |
| 0.6-0.79   | generate_with_suggestions      | Output + [VERIFICAR]       |
| 0.4-0.59   | generate_partial               | Output + [COMPLETAR]       |
| < 0.4      | request_enrichment             | Ask for minimum data       |

MINIMUM VIABLE INPUT:
- Required: product_name, category
- Recommended: head_terms, diferenciais, dores
- Optional: provas, ganhos, competitor_analysis
```

---

## HOP Pipeline (6 Core Modules)

| # | HOP | Input | Output | Duration |
|---|-----|-------|--------|----------|
| 13 | main_agent | input, research | $head_terms, $diferenciais, $confidence | 1-2 min |
| 14 | titulo_generator | $head_terms, $diferenciais | $titulos_list (3) | 1-2 min |
| 15 | keywords_expander | $head_terms, $titulos | $keywords_blocks (2) | 1-2 min |
| 16 | bullet_points | $diferenciais, $dores, $ganhos | $bullets_list (10) | 1-2 min |
| 17 | descricao_builder | $bullets, $keywords | $descricao_text | 2-3 min |
| 18 | qa_validation | all outputs | $qa_report, $score | 1-2 min |

**Total**: 8-12 min (full mode) | 2-3 min (quick mode)

---

## File Structure (iso_vectorstore)

```
iso_vectorstore/           (20 files, drag-and-drop ready)
├── 01_QUICK_START.md      Entry point for LLMs
├── 02_PRIME.md            Agent identity
├── 03_INSTRUCTIONS.md     Workflow rules
├── 04_README.md           Documentation
├── 05_ARCHITECTURE.md     This file
├── 06_input_schema.json   Input validation
├── 07_output_template.md  3-PART output format (v3.2)
├── 08_copy_rules.json     ANVISA/INMETRO compliance
├── 09_marketplace_specs.json  Platform limits
├── 10_persuasion_patterns.json  PNL triggers
├── 11_ADW_orchestrator.md Workflow manager
├── 12_execution_plans.json  Full/Quick plans
├── 13_HOP_main_agent.md   Parse + confidence
├── 14_HOP_titulo_generator.md  Title generation
├── 15_HOP_keywords_expander.md  Keyword expansion
├── 16_HOP_bullet_points.md  Bullet generation
├── 17_HOP_descricao_builder.md  Description building
├── 18_HOP_qa_validation.md  5D validation
├── 19_frameworks.md       CODEXA/HOP reference
└── 20_quality_dimensions.json  5D scoring schema
```

---

## Configuration Presets (v3.2.0)

### EFICIENTE (Token-Optimized)

```yaml
target_tokens: ~18,000 (-68%)
reasoning_effort: medium
verbosity: low
web_search: OFF
output: PART 2 only (copyable block)
use_case: Batch processing, automation
```

### PERFORMANCE (Quality-Optimized)

```yaml
target_tokens: ~35,000 (-39%)
reasoning_effort: high
verbosity: high
web_search: ON
output: PART 1 + 2 + 3 (full)
use_case: Production, final quality
```

**Reference**: `config/MANUAL_CONFIGS.md`

---

## Output Structure (v3.2.0)

### PART 1: VISUAL REVIEW (Display Only)

- Formatted tables, headers
- QA report, 5D scores
- Source attribution summary
- NOT for copy/paste

### PART 2: COPYABLE CONTENT (Production Ready)

```txt
[INICIO_COPIAR]
================================================================================
TITULOS / DESCRICAO / BULLETS / KEYWORDS
================================================================================
[FIM_COPIAR]
```

- Code fence for 1-click copy
- Clean text, no markdown
- Ready for marketplace paste

### PART 3: STRUCTURED DATA (Optional)

```json
{
  "titulos": [...],
  "descricao": "...",
  "bullets": [...],
  "keywords": {...},
  "qa": {...}
}
```

- JSON format
- For API/automation
- Enable with config

---

## Compliance Validation

### Global Prohibitions

```yaml
prohibited:
  - HTML tags (<...>)
  - Emojis (any Unicode emoji)
  - Superlativos absolutos ("#1", "melhor do mundo")
  - Claims terapeuticas (sem ANVISA)
  - Links externos
  - Comparacoes diretas com marcas
```

### Marketplace-Specific

```yaml
mercado_livre:
  - "frete grátis" (only if true)
  - "entrega imediata" (prohibited)

shopee:
  - Precos no titulo (prohibited)

amazon_br:
  - Palavras repetidas > 2x
```

---

## Performance Metrics (v3.2.0)

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Total Tokens | 57,005 | TBD | <25,000 |
| Code Interpreter Calls | ~30 | TBD | <10 |
| Execution Time | 10-15 min | 8-12 min | <10 min |
| Output Copyability | 60% | 95% | 95% |
| 5D Score | N/A | >= 0.85 | >= 0.85 |

---

## Integration

### Upstream (Optional)

| Agent | Provides |
|-------|----------|
| pesquisa_agent | Research notes, competitive intel |
| marca_agent | Brand voice guidelines |
| mentor_agent | Pre-enrichment context |

### Downstream

| Destination | Format |
|-------------|--------|
| Marketplace | Copy PART 2 → paste |
| Automation | PART 3 JSON → API |
| Review | PART 1 → human audit |

---

**Version**: 3.2.0 | **Updated**: 2025-11-30
**Framework**: 12 Leverage Points + CODEXA
**Status**: Production Ready (TEXT-ONLY)
