# MANIFEST | anuncio_agent iso_vectorstore v3.2.0

**Package**: iso_vectorstore (drag-and-drop for any LLM)
**Agent**: anuncio_agent | **Version**: 3.2.0 | **Date**: 2025-11-30
**Scope**: TEXT-ONLY e-commerce copywriting
**Output**: 3-PART (Visual + Copyable + Structured)
**Files**: 21 | **Total Tokens**: ~8,000 (otimizado de ~80,000)

---

## DEPLOY CHECKLIST

```
[ ] Upload 21 arquivos ao vector store / file search
[ ] Upload validator.py ao Code Interpreter (separado)
[ ] Aplicar config preset (EFICIENTE ou PERFORMANCE)
[ ] Testar com URL de produto
[ ] Verificar 3-PART output
```

---

## FILE INVENTORY (21 Files)

### Core (00-05) ~2,000 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Package inventory |
| 01 | QUICK_START.md | ~600 | LLM entry point |
| 02 | PRIME.md | ~500 | Agent identity |
| 03 | INSTRUCTIONS.md | ~400 | Workflow rules |
| 04 | README.md | ~300 | Documentation |
| 05 | ARCHITECTURE.md | ~500 | Tech architecture |

### Config (06-10) ~1,500 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 06 | input_schema.json | ~300 | Input validation |
| 07 | output_template.md | ~400 | 3-PART output format |
| 08 | copy_rules.json | ~300 | ANVISA/INMETRO compliance |
| 09 | marketplace_specs.json | ~300 | Platform limits |
| 10 | persuasion_patterns.json | ~200 | PNL triggers |

### Execution (11-12) ~800 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 11 | ADW_orchestrator.md | ~400 | Workflow manager |
| 12 | execution_plans.json | ~400 | Full/Quick plans |

### HOPs (13-18) ~4,500 tokens (OTIMIZADO de ~60,000)

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 13 | HOP_main_agent.md | ~800 | Parse + confidence |
| 14 | HOP_titulo_generator.md | ~800 | 3 titles (58-60 chars) |
| 15 | HOP_keywords_expander.md | ~600 | 2 blocks x 115-120 terms |
| 16 | HOP_bullet_points.md | ~700 | 10 bullets (250-299 chars) |
| 17 | HOP_descricao_builder.md | ~1,200 | Description >= 3,300 chars |
| 18 | HOP_qa_validation.md | ~800 | 5D validation |

### Reference (19-20) ~600 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 19 | frameworks.md | ~300 | CODEXA/HOP reference |
| 20 | quality_dimensions.json | ~300 | 5D scoring schema |

### Separado (Code Interpreter)

| File | Tokens | Purpose |
|------|--------|---------|
| validator.py | ~2,500 | Python 5D validation |

---

## TOKEN OPTIMIZATION

| Componente | Antes | Depois | Reducao |
|------------|-------|--------|---------|
| HOP 14 (titulo) | ~26,000 | ~800 | -97% |
| HOP 17 (descricao) | ~34,000 | ~1,200 | -96% |
| HOPs total | ~60,000 | ~4,500 | -92% |
| **PACOTE TOTAL** | ~80,000 | ~8,000 | **-90%** |

---

## CONFIG PRESETS

### EFICIENTE
```yaml
tokens_target: ~18,000
reasoning_effort: medium
verbosity: low
web_search: OFF
output: PART 2 only
```

### PERFORMANCE
```yaml
tokens_target: ~35,000
reasoning_effort: high
verbosity: high
web_search: ON
output: PART 1 + 2 + 3
```

---

## OUTPUT STRUCTURE

```
PART 1: VISUAL REVIEW     → Display, QA scores (nao copiar)
PART 2: COPYABLE CONTENT  → Code fence [INICIO_COPIAR] (1-click copy)
PART 3: STRUCTURED DATA   → JSON (opcional, API)
```

---

## SCOPE (TEXT-ONLY)

### GERA
- Titulos: 3 x 58-60 chars
- Keywords: 2 x 115-120 terms
- Bullets: 10 x 250-299 chars
- Descricao: >= 3,300 chars

### DELEGADO
- Image prompts → photo_agent
- Video scripts → video_agent

---

## 5D SCORING

| Dim | Weight | Threshold |
|-----|--------|-----------|
| Titulo | 30% | >= 0.75 |
| Keywords | 25% | >= 0.75 |
| Descricao | 20% | >= 0.75 |
| Bullets | 15% | >= 0.75 |
| Compliance | 10% | >= 0.75 |

**PASS**: >= 0.85 | **FAIL**: < 0.75

---

## COMPATIBILITY

| Platform | Status |
|----------|--------|
| ChatGPT Responses API | OK |
| Claude Projects | OK |
| OpenAI Assistants | OK |
| Gemini | OK |

---

**Package**: anuncio_agent iso_vectorstore v3.2.0
**Status**: DEPLOY READY
**Tokens**: ~8,000 (otimizado -90%)
**Date**: 2025-11-30
