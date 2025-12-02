# pesquisa_agent | Quick Start Guide

**Version**: 3.0.0 | **Max Chars**: 8000 | **Output**: research_notes.md (22 blocks)

---

## IDENTITY

**Agent**: pesquisa_agent | Brazilian e-commerce market research
**Pipeline**: 9-Step (Capability detect → Web search → Analysis → 22-block report)
**Output**: research_notes.md + metadata.json + queries.json

---

## QUICK START (3 Steps)

**1. AUTO-DETECT** → Agent detects: **web_search** (REQUIRED) + vision/file_search (optional)
**2. READ CORE** → 02_PRIME (pipeline) + 03_INSTRUCTIONS (setup)
**3. EXECUTE** → Provide brief (product, category, audience, price) → Get 22-block report

---

## FILE ARCHITECTURE (21 Files)

### Core (00-05)
- **00_MANIFEST** → Package inventory
- **01_QUICK_START** → This file
- **02_PRIME** → TAC-7 framework + 9-step pipeline
- **03_INSTRUCTIONS** → Platform setup
- **04_README** → Overview
- **05_ARCHITECTURE** → Technical structure

### Config (06-10)
- **06-10** → JSON schemas (input, brief, plan, marketplaces, config)

### Execution (11-12)
- **11_ADW_orchestrator** → Workflow manager
- **12_execution_plans** → Full/Quick plans

### HOPs (13-20)
- **13-20** → Research modules (main, intake, competitor, gap, image, price, sentiment, QA)

---

## EXECUTION FLOW (9 Steps | 20-30 min)

1. **Capability Discovery** → Detect web_search (required)
2. **Query Bank** → 10-15 head terms + 30-50 longtails
3. **INBOUND Search** → 9 BR marketplaces
4. **OUTBOUND Search** → Google, YouTube, TikTok, Reclame Aqui
5. **Competitor Analysis** → Top 3-5 competitors
6. **SEO Taxonomy** → Cluster keywords
7. **Compliance Check** → ANVISA/INMETRO/CONAR
8. **Synthesis** → Actionable insights
9. **Output** → 22-block report + validation

---

## OUTPUT FORMAT (22 Blocks)

```markdown
# [PRODUTO] | Research Notes

## [LACUNAS DO BRIEF] → Missing data
## [HEAD TERMS] → 10-15 keywords
## [LONGTAILS] → 30-50 phrases
## [SINONIMOS] → Variations
## [TERMO CONTEXTUAL] → Context/occasion
## [DORES DO PUBLICO] → Pain points
## [GANHOS DESEJADOS] → Benefits
## [OBJECOES E RESPOSTAS] → Objections
## [PROVAS E EVIDENCIAS] → Proofs
## [DIFERENCIAIS] → Differentials
## [RISCOS] → Compliance risks
## [ANALISE CONCORRENTES] → Competitor profiles
## [BENCHMARK] → Quantitative table
## [ESTRATEGIAS E GAPS] → Opportunities
## [PADROES LINGUAGEM] → Effective patterns
## [SEO OUTBOUND] → Organic keywords
## [SEO INBOUND] → Marketplace SEO
## [REGRAS MARKETPLACE] → Platform rules
## [DECISOES COPY] → Initial decisions
## [CONSULTAS WEB] → Web queries logged
## [IMAGENS ANALISADAS] → Image analysis
## [NOTAS FALLBACK] → Suggestions
## [RESUMO EXECUTIVO] → Summary
```

---

## QUALITY GATES

| Gate | Target |
|------|--------|
| Blocks present | 22/22 |
| Competitors analyzed | >= 3 |
| Web queries logged | >= 15 |
| Confidence score | >= 0.75 |
| [SUGESTAO] placeholders | <= 10% |
| Prices in BRL | 100% |
| Ratings format | X.X/5.0 |

---

## CAPABILITIES

**REQUIRED**: web_search (cannot run without)
**OPTIONAL**: vision (screenshots), file_search (compliance), code_interpreter (metrics)

---

## MARKETPLACES (9 BR)

Mercado Livre, Shopee, Magazine Luiza, Amazon BR, Americanas, Casas Bahia, Submarino, TikTok Shop, Shein
**Plus**: Google SERP, YouTube, TikTok, Instagram, Reclame Aqui (REQUIRED)

---

## MINIMUM BRIEF

**Required**: product_name, category, target_audience, price_range
**Optional**: marketplace_target, competitors, image_urls, special_requirements

---

## INTEGRATION

**Input**: User brief (4 fields)
**Output**: research_notes.md → anuncio_agent / marca_agent / user_research/

---

## 6D SCORING

| Dimension | Weight |
|-----------|--------|
| Completeness | 25% |
| Competitors | 25% |
| Queries | 20% |
| Insights | 15% |
| Compliance | 10% |
| Coherence | 5% |

**PASS**: >= 0.75 | **FAIL**: < 0.75

---

**Version**: 3.0.0 | **Chars**: ~3500/8000 | **Date**: 2025-11-30
**Next**: 02_PRIME → 03_INSTRUCTIONS → Brief → Execute → 22-block report
**CRITICAL**: web_search REQUIRED. Output: `user_research/[produto]_research_notes.md`
