# MANIFEST | pesquisa_agent iso_vectorstore v3.0.0

**Package**: iso_vectorstore (drag-and-drop for any LLM)
**Agent**: pesquisa_agent | **Version**: 3.0.0 | **Date**: 2025-11-30
**Scope**: RESEARCH (market research for Brazilian e-commerce)
**Output**: research_notes.md (22 structured blocks)
**Files**: 21 | **Total Tokens**: ~12,000 (optimized)

---

## DEPLOY CHECKLIST

```
[ ] Upload 21 arquivos ao vector store / file search
[ ] Upload validator.py ao Code Interpreter (separado)
[ ] Copiar SYSTEM_INSTRUCTIONS para System Prompt
[ ] Habilitar: File Search, Web Search (REQUIRED)
[ ] Testar com brief exemplo
[ ] Verificar 22 blocos no output
```

---

## FILE INVENTORY (21 Files)

### Core (00-05) ~4,200 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Package inventory |
| 01 | QUICK_START.md | ~600 | LLM entry point |
| 02 | PRIME.md | ~1,500 | Agent identity, 12 pillars |
| 03 | INSTRUCTIONS.md | ~800 | Workflow rules |
| 04 | README.md | ~600 | Documentation |
| 05 | ARCHITECTURE.md | ~700 | Tech architecture |

### Config (06-10) ~2,400 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 06 | input_schema.json | ~100 | Input validation |
| 07 | brief_schema.json | ~600 | Brief structure |
| 08 | execution_plan.json | ~700 | 9-phase plan |
| 09 | marketplaces.json | ~600 | 9 BR marketplaces |
| 10 | research_config.json | ~400 | Agent configuration |

### Execution (11-12) ~1,300 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 11 | ADW_orchestrator.md | ~800 | Workflow manager |
| 12 | execution_plans.json | ~500 | Full/Quick plans |

### HOPs (13-20) ~5,600 tokens (OPTIMIZED)

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 13 | HOP_main_agent.md | ~800 | Parse input, orchestrate |
| 14 | HOP_intake_validation.md | ~700 | Brief validation |
| 15 | HOP_competitor_analysis.md | ~900 | Competitor deep dive |
| 16 | HOP_gap_identification.md | ~600 | Market gaps |
| 17 | HOP_image_analysis.md | ~600 | Visual + compliance |
| 18 | HOP_price_comparison.md | ~700 | Pricing intelligence |
| 19 | HOP_sentiment_analysis.md | ~700 | Review sentiment |
| 20 | HOP_qa_validation.md | ~600 | QA validation |

### Separado (Code Interpreter)

| File | Tokens | Purpose |
|------|--------|---------|
| validator.py | ~2,500 | Python 6D validation |

---

## TOKEN OPTIMIZATION

| Component | Before | After | Reduction |
|-----------|--------|-------|-----------|
| Core docs | ~8,000 | ~4,200 | -47% |
| HOPs total | ~20,000 | ~5,600 | -72% |
| **PACKAGE TOTAL** | ~30,000 | ~12,000 | **-60%** |

---

## CONFIG PRESETS

### EFICIENTE
```yaml
tokens_target: ~25,000
reasoning_effort: medium
verbosity: low
web_search: ON (REQUIRED)
output: research_notes.md only
```

### PERFORMANCE
```yaml
tokens_target: ~45,000
reasoning_effort: high
verbosity: high
web_search: ON (REQUIRED)
mcp_browser: ON
output: research_notes.md + metadata.json
```

---

## OUTPUT STRUCTURE

```
research_notes.md
├── HEADER (product, date, marketplace)
├── 22 STRUCTURED BLOCKS
│   ├── Brief Analysis (1-5)
│   ├── Audience Insights (6-10)
│   ├── Competitor Intelligence (11-14)
│   ├── SEO Strategy (15-18)
│   └── Action Items (19-22)
└── RESUMO EXECUTIVO
```

---

## SCOPE (RESEARCH)

### GENERATES
- research_notes.md (22 blocks)
- metadata.json (quality scores)
- queries.json (traced web searches)

### DELEGATES
- Ad copy → anuncio_agent
- Brand strategy → marca_agent
- Visual assets → photo_agent

### OUT OF SCOPE
- HOP_titulo_*, HOP_descricao_* (→ anuncio_agent)
- HOP_brand_* (→ marca_agent)
- HOP_image_generation_* (→ photo_agent)

---

## 6D SCORING

| Dim | Weight | Threshold |
|-----|--------|-----------|
| Completeness | 25% | >= 0.75 |
| Competitors | 25% | >= 0.75 |
| Queries | 20% | >= 0.75 |
| Insights | 15% | >= 0.75 |
| Compliance | 10% | >= 0.75 |
| Coherence | 5% | >= 0.75 |

**PASS**: >= 0.75 | **FAIL**: < 0.75

---

## COMPATIBILITY

| Platform | Status |
|----------|--------|
| ChatGPT Responses API | OK |
| Claude Projects | OK |
| OpenAI Assistants | OK |
| Gemini | OK |

---

## QUICK START

```bash
# 1. Upload all 21 files to vector store (chunk: 800, overlap: 200)
# 2. Copy SYSTEM_INSTRUCTIONS to System Prompt
# 3. Enable: File Search, Web Search
# 4. Test with brief:
#    Product: Garrafa de agua reutilizavel
#    Category: Casa e Jardim > Cozinha
#    Target: Profissionais home office, 25-45 anos
#    Price: R$ 89 - R$ 129
```

---

**Package**: pesquisa_agent iso_vectorstore v3.0.0
**Status**: DEPLOY READY
**Tokens**: ~12,000 (optimized -60%)
**Date**: 2025-11-30
