# LIVRO: Analise
## CAPÍTULO 1

**Versículos consolidados**: 47
**Linhas totais**: 1177
**Gerado em**: 2025-11-13 18:45:48

---


<!-- VERSÍCULO 1/47 - analise_concorrencia_5_princ_pios_orientadores_para_treinar_1_20251113.md (19 linhas) -->

# 5. Princípios Orientadores para Treinar LLMs

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
**Data**: 20251113

## Conteúdo

1. **Formato Primeiro**: os modelos devem ser instruídos a respeitar JSON STRICT; qualquer saída inválida precisa acionar reparo ou retry.
2. **Fluxo Multi-etapas**: reforçar a sequência benchmark → síntese → geração → validação → empacotamento para maximizar consistência.
3. **Resiliência de Fornecedor**: manter fallback cross-vendor e monitorar métricas de sucesso para calibrar preferências dinâmicas.
4. **Enriquecimento Determinístico**: SEO e n

**Tags**: ecommerce, intermediate

**Palavras-chave**: Princípios, Orientadores, Treinar, LLMs

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 2/47 - analise_concorrencia_5_princ_pios_orientadores_para_treinar_20251113.md (19 linhas) -->

# 5. Princípios Orientadores para Treinar LLMs

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
**Data**: 20251113

## Conteúdo

1. **Formato Primeiro**: os modelos devem ser instruídos a respeitar JSON STRICT; qualquer saída inválida precisa acionar reparo ou retry.
2. **Fluxo Multi-etapas**: reforçar a sequência benchmark → síntese → geração → validação → empacotamento para maximizar consistência.
3. **Resiliência de Fornecedor**: manter fallback cross-vendor e monitorar métricas de sucesso para calibrar preferências dinâmicas.
4. **Enriquecimento Determinístico**: SEO e n

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Treinar, Princípios, Orientadores, LLMs

**Origem**: desconhecida


---


<!-- VERSÍCULO 3/47 - analise_concorrencia_6_research_pillars_framework_foundat_20251113.md (36 linhas) -->

# 🏗️ 6 RESEARCH PILLARS (Framework Foundation)

**Categoria**: analise_concorrencia
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

### Pilar 1: Market Research (Pesquisa de Mercado)
- **Agent**: `/analyze_market`
- **Components**: Market size, growth, seasonality, pricing, channels
- **Framework**: `app/como_pesquisa/01_framework/research_framework.md`
- **Output**: `$market_research_result`

### Pilar 2: Competitive Analysis (Análise Competitiva)
- **Agent**: `/analyze_competitors`
- **Components**: Competitor positioning, gaps, differentiation, threats
- **Framework**: `app/como_pesquisa/03_research_methodology/competitive_analysis.md`
- **Output**: `$competitive_result`

### Pilar 3: Product Research (Pesquisa de Produto)
- **Processing**: Internal (Features → Benefits → Emotions)
- **Components**: Technical specs, functional benefits, emotional benefits, personas
- **Output**: `$product_research_result`

### Pilar 4: Keywords Research (Pesquisa de Keywords)
- **Agent**: `/extract_keywords`
- **Components**: 4-level hierarchy (Head/Mid/Long/FAQ)
- **Framework**: `app/como_pesquisa/01_framework/keyword_hierarchy

**Tags**: ecommerce, abstract

**Palavras-chave**: RESEARCH, PILLARS, Framework, Foundation

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 4/47 - analise_concorrencia_app_docs_master_backup_ecommerce_canon_20251113.md (22 linhas) -->

# [app_docs\_MASTER_BACKUP\ecommerce-canon\GENESIS\RAW\RAW_005_RESEARCH_AGENT.md]

**Categoria**: analise_concorrencia
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

Lines: 665

# Research Agent System - Complete Documentation

**KEYWORDS**: research|agent|system|documentation|meta-pesquisa

Complete research agent system for automated market research, competitive analysis, and AI-powered prompt composition.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: RAW_005_RESEARCH_AGENT, app_docs, canon, Core, ecommerce, server, RESEARCH_AGENT_SYSTEM, Conceito, GENESIS, _MASTER_BACKUP

**Origem**: desconhecida


---


<!-- VERSÍCULO 5/47 - analise_concorrencia_architecture_1_prompt_1_agent_1_rea_20251113.md (28 linhas) -->

# Architecture: 1 Prompt = 1 Agent = 1 Reason

**Categoria**: analise_concorrencia
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

Each agent is designed with a single, clear responsibility and communicates via dense keywords.

### Agent Specifications

| Agent | Role | Input | Output | Keywords |
|-------|------|-------|--------|----------|
| **ORCHESTRATOR** | Coordinates workflow | ResearchRequest | ResearchReport | orchestration\|coordination\|workflow |
| **MarketResearchAgent** | Market analysis | ProductInfo | MarketResearchResult | market\|size\|trends\|growth |
| **CompetitorAnalystAgent** | Competitive intelligence | Competitor URLs | CompetitiveAnalysisResult | competitor\|analysis\|positioning |
| **KeywordExtractionAgent** | SEO keyword extraction | Product info | KeywordExtractionResult | keyword\|seo\|hierarchy\|search |
| **FAQCollectionAgent** | Objection handling | Market data | FAQCollectionResult | faq\|objection\|question\|answer |
| **DataValidatorAgent** | Quality assurance | All data | DataValidationResult | validation\|quality\|scoring |
| **PromptComposerAgent** | AI prompt generation | R

**Tags**: concrete, ecommerce, general

**Palavras-chave**: Architecture, Prompt, Agent, Reason

**Origem**: desconhecida


---


<!-- VERSÍCULO 6/47 - analise_concorrencia_arquitetura_do_sistema_20251113.md (38 linhas) -->

# 🏗️ Arquitetura do Sistema

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Fluxo de Dados Completo

```
INPUT (Product Name + Category + Marketplace)
  ↓
ORCHESTRATOR (/research - Main Agent)
  ↓
┌─────────────────────────────────────────────────────────────┐
│ PIPELINE DE 6 PILARES (em paralelo ou sequencial)          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Pilar 1: /analyze_market → $market_research_result        │
│ Pilar 2: /analyze_competitors → $competitive_result       │
│ Pilar 3: [Internal] Product Research → $product_result    │
│ Pilar 4: /extract_keywords → $keywords_result             │
│ Pilar 5: [Internal] Trends & Insights → $trends_result    │
│ Pilar 6: [Internal] FAQ Collection → $faq_result          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  ↓
VALIDATION LAYER (Quality Scoring + Meta-Analysis)
  ↓
┌────────────────────────────────────────────────────────────

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Sistema, Arquitetura

**Origem**: desconhecida


---


<!-- VERSÍCULO 7/47 - analise_concorrencia_artefatos_consolidados_20251113.md (30 linhas) -->

# 🎯 Artefatos Consolidados

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Research System (Origem)
- **6 Pilares**: Market, Competitors, Product, Keywords, Trends, FAQ
- **5-Chunk Library**: Consolidation, Keywords, Gaps, Ad Structure, Validation
- **7 Agentes**: Orchestrator, Market, Competitor, Keyword, FAQ, Validator, Meta
- **5 CLI Commands**: /research, /analyze_market, /analyze_competitors, /extract_keywords, /compose_prompts
- **6 Python Modules**: models, config, orchestrator, agents, routes, meta
- **Knowledge Base**: 8 JSON files com semantic maps, inventories, catalogs

### Framework (Como Pesquisa)
- **20+ documentos** sobre metodologia, templates, tools integration
- **4 níveis de keyword hierarchy**
- **5-chunk prompt composition library**
- **Metodologias de pesquisa**: competitive, market, product, trends, FAQ

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Consolidados, Artefatos

**Origem**: desconhecida


---


<!-- VERSÍCULO 8/47 - analise_concorrencia_checklist_de_entrega_1_20251113.md (27 linhas) -->

# ✅ Checklist de Entrega

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

- ✅ Análise completa de 113.864 arquivos
- ✅ 17.082 tokens semânticos extraídos
- ✅ 4 scripts de alavancagem implementados
- ✅ 1 orquestrador maestro funcional
- ✅ Documentação completa (5 guias)
- ✅ Exemplos práticos incluídos
- ✅ Tratamento de erros robusto
- ✅ Logs detalhados para auditoria
- ✅ Qualidade score 100/100 mantido
- ✅ Zero duplicação de conhecimento

---

**Tags**: ecommerce, concrete

**Palavras-chave**: Checklist, Entrega

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 9/47 - analise_concorrencia_checklist_de_entrega_20251113.md (27 linhas) -->

# ✅ Checklist de Entrega

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

- ✅ Análise completa de 113.864 arquivos
- ✅ 17.082 tokens semânticos extraídos
- ✅ 4 scripts de alavancagem implementados
- ✅ 1 orquestrador maestro funcional
- ✅ Documentação completa (5 guias)
- ✅ Exemplos práticos incluídos
- ✅ Tratamento de erros robusto
- ✅ Logs detalhados para auditoria
- ✅ Qualidade score 100/100 mantido
- ✅ Zero duplicação de conhecimento

---

**Tags**: ecommerce, concrete

**Palavras-chave**: Checklist, Entrega

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 10/47 - analise_concorrencia_checklist_de_entrega_2_20251113.md (27 linhas) -->

# ✅ Checklist de Entrega

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

- ✅ Análise completa de 113.864 arquivos
- ✅ 17.082 tokens semânticos extraídos
- ✅ 4 scripts de alavancagem implementados
- ✅ 1 orquestrador maestro funcional
- ✅ Documentação completa (5 guias)
- ✅ Exemplos práticos incluídos
- ✅ Tratamento de erros robusto
- ✅ Logs detalhados para auditoria
- ✅ Qualidade score 100/100 mantido
- ✅ Zero duplicação de conhecimento

---

**Tags**: ecommerce, concrete

**Palavras-chave**: Checklist, Entrega

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 11/47 - analise_concorrencia_checklist_pr_uso_1_20251113.md (25 linhas) -->

# ✅ CHECKLIST PRÉ-USO

**Categoria**: analise_concorrencia
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

Antes de executar a pesquisa, verifique:

- [ ] **Product Name**: Claro e específico
- [ ] **Category**: Classificado corretamente
- [ ] **Marketplace**: Selecionado (amazon, mercado_livre, ebay, generic)
- [ ] **Competitor URLs**: 3-5 URLs válidas (se análise competitiva)
- [ ] **Research Type**: Definido (quick, deep, keywords_only, competitors, ai_assisted)
- [ ] **AI Composition**: Marcado como true se precisa dos chunks

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: CHECKLIST

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 12/47 - analise_concorrencia_checklist_pr_uso_20251113.md (25 linhas) -->

# ✅ CHECKLIST PRÉ-USO

**Categoria**: analise_concorrencia
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

Antes de executar a pesquisa, verifique:

- [ ] **Product Name**: Claro e específico
- [ ] **Category**: Classificado corretamente
- [ ] **Marketplace**: Selecionado (amazon, mercado_livre, ebay, generic)
- [ ] **Competitor URLs**: 3-5 URLs válidas (se análise competitiva)
- [ ] **Research Type**: Definido (quick, deep, keywords_only, competitors, ai_assisted)
- [ ] **AI Composition**: Marcado como true se precisa dos chunks

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: CHECKLIST

**Origem**: desconhecida


---


<!-- VERSÍCULO 13/47 - analise_concorrencia_como_pesquisa_integration_20251113.md (37 linhas) -->

# 🔗 COMO PESQUISA INTEGRATION

**Categoria**: analise_concorrencia
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Framework Foundation Files
- `app/como_pesquisa/README.md`
- `app/como_pesquisa/01_framework/research_framework.md` (6 PILLARS)
- `app/como_pesquisa/01_framework/keyword_hierarchy.md` (4-LEVEL KEYWORDS)
- `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md` (5-CHUNKS)
- `app/como_pesquisa/02_prompt_composition/prompt_templates.md` (TEMPLATES)
- `app/como_pesquisa/03_research_methodology/competitive_analysis.md`
- `app/como_pesquisa/07_templates/research_report_template.md`

### Research Agents Mapping
- Pilar 1 → `/analyze_market` → Market Research
- Pilar 2 → `/analyze_competitors` → Competitive Analysis
- Pilar 3 → [Internal] → Product Research
- Pilar 4 → `/extract_keywords` → Keywords (4-level)
- Pilar 5 → [Internal] → Trends & Insights
- Pilar 6 → [Internal] → FAQ Collection

### Chunk Library Mapping
- Chunk 1: Research Consolidation ← ALL PILLARS
- Chunk 2: Keyword Analysis ← PILAR 4 + 3
- Chunk 3: Competitive Gaps ← PILAR 2 + 1
- Chunk 4: Ad Structure ← ALL PILL

**Tags**: ecommerce, abstract

**Palavras-chave**: COMO, PESQUISA, INTEGRATION

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 14/47 - analise_concorrencia_complete_workflow_20251113.md (48 linhas) -->

# 🎯 COMPLETE WORKFLOW

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

```
INPUT (Product Name, Category, Marketplace)
  ↓
/research COMMAND (Main Orchestrator - HIGH-LEVEL PROMPT)
  ↓
STEP 1: INPUT PARSING & VALIDATION
  └─ Output: $product_name, $category, $marketplace, $research_type
  ↓
STEP 2: PILAR 1 - /analyze_market
  └─ Output: $market_research_result (size, growth, trends, channels)
  ↓
STEP 3: PILAR 2 - /analyze_competitors
  └─ Output: $competitive_result (gaps, positioning, threats)
  ↓
STEP 4: PILAR 3 - PRODUCT RESEARCH (Internal)
  └─ Output: $product_research_result
  ↓
STEP 5: PILAR 4 - /extract_keywords
  └─ Output: $keywords_result (4-level hierarchy)
  ↓
STEP 6: PILAR 5+6 - TRENDS & FAQ (Internal)
  └─ Output: $trends_result + $faq_result
  ↓
STEP 7: DATA VALIDATION & QUALITY SCORING
  └─ Output: $validation_result + $quality_score
  ↓
STEP 8: /compose_prompts (5-CHUNK LIBRARY)
  ├─ Chunk 1: Research Consolidation
  ├─ Chunk 2: Keyword Analysis
  ├─ Chunk 3: Competitive Insights
  ├─ Chunk 4: Ad Brief
  └─ Chunk 5: Copy Optimization
  

**Tags**: ecommerce, intermediate

**Palavras-chave**: COMPLETE, WORKFLOW

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 15/47 - analise_concorrencia_conceito_core_10_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

### 2️⃣ Revisar Saída Estruturada

O relatório incluirá:
- **Pilar 1 Results**: Market size, growth, trends, channels
- **Pilar 2 Results**: Competitors, gaps, positioning
- **Pilar 3 Results**: Features, benefits, emotions
- **Pilar 4 Results**: Keywords em 4 níveis
- **Pilar 5 Results**: Market trends
- **Pilar 6 Results**: FAQ e objections

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 16/47 - analise_concorrencia_conceito_core_11_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.72/1.00
**Data**: 20251113

## Conteúdo

### Communication Topology

```
ORCHESTRATOR (hub):
├── ↔ MARKET_RESEARCHER
├── ↔ COMPETITOR_ANALYST
├── ↔ KEYWORD_EXTRACTOR
├── ↔ DATA_VALIDATOR
├── ↔ PROMPT_COMPOSER
└── ↔ META_RESEARCHER

SPECIALIZED AGENTS:
├── MARKET_RESEARCHER → DATA_VALIDATOR
├── COMPETITOR_ANALYST → DATA_VALIDATOR
├── KEYWORD_EXTRACTOR → DATA_VALIDATOR
└── All agents report back to ORCHESTRATOR
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 17/47 - analise_concorrencia_conceito_core_12_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Typical Execution Times
- Quick research: 5-10 minutes
- Deep research: 20-30 minutes
- Keywords only: 2-5 minutes
- Competitors: 10-15 minutes
- AI-assisted: 5-15 minutes

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 18/47 - analise_concorrencia_conceito_core_13_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.63/1.00
**Data**: 20251113

## Conteúdo

### Expected Data Collection
- Market research: 5-10 insights
- Competitor analysis: 3-5 competitors analyzed
- Keywords: 50-200 keywords extracted
- FAQs: 10-20 common questions
- Quality score: 75-95%

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 19/47 - analise_concorrencia_conceito_core_14_20251113.md (23 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

### Agent Performance
- Market Researcher: 85% success rate, 120s avg
- Competitor Analyst: 90% success rate, 150s avg
- Keyword Extractor: 95% success rate, 90s avg
- Data Validator: 98% success rate, 30s avg
- Prompt Composer: 92% success rate, 45s avg

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 20/47 - analise_concorrencia_conceito_core_15_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Issue: Low quality scores
**Solution**:
- Add more competitor URLs (minimum 5)
- Increase research depth (use deep instead of quick)
- Check competitor URLs are accessible

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 21/47 - analise_concorrencia_conceito_core_16_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Issue: Slow execution
**Solution**:
- Use quick research type for faster results
- Skip FAQ collection for non-conversion focused research
- Cache competitor data between runs

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 22/47 - analise_concorrencia_conceito_core_17_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

#### Check Competitors
→ **Command**: `/analyze_competitors`
→ **Python**: `CompetitorAnalystAgent().execute()`
→ **File**: `research_agents.py:CompetitorAnalystAgent`

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 23/47 - analise_concorrencia_conceito_core_18_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Command Files (.claude/commands/)

| File | Invocation | Use Case |
|------|-----------|----------|
| `research.md` | `/research` | Full research workflow |
| `analyze_market.md` | `/analyze_market` | Market analysis only |
| `analyze_competitors.md` | `/analyze_competitors` | Competitor analysis only |
| `extract_keywords.md` | `/extract_keywords` | Keyword extraction only |
| `compose_prompts.md` | `/compose_prompts` | Prompt composition only |

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 24/47 - analise_concorrencia_conceito_core_19_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### v1.1.0 (Próximas horas)
- [ ] Integração com MCP Server (usar com Claude)
- [ ] Recomendações automáticas por IA
- [ ] Análise de histórico do cliente

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 25/47 - analise_concorrencia_conceito_core_1_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

# Start research
curl -X POST http://localhost:8000/api/research/start \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wireless Speaker",
    "category": "Electronics",
    "research_type": "deep",
    "competitor_urls": ["url1", "url2"]
  }'

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 26/47 - analise_concorrencia_conceito_core_20251113.md (35 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### 7. Meta Researcher Agent

**Função**: Auto-análise e otimização
**Implementação**: `research_agent_meta.py:MetaResearchAgent`

**Responsabilidades**:
- Analisar performance de outros agentes
- Identificar gargalos
- Propor melhorias
- Tracking de métricas

**Análises**:
- Execution time analysis
- Quality trend analysis
- Bottleneck identification
- Optimization recommendations

**Output**: `$meta_research_result` com insights de melhoria

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 27/47 - analise_concorrencia_conceito_core_20_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Expected Execution Times
- Quick research: 5-10 minutes
- Deep research: 20-30 minutes
- Keywords only: 2-5 minutes
- Competitors: 10-15 minutes

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 28/47 - analise_concorrencia_conceito_core_21_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.68/1.00
**Data**: 20251113

## Conteúdo

# Escopo: Repositório de fontes (dos ficheiros carregados) com links e notas de uso

> Todas as fontes abaixo foram extraídas dos documentos que você subiu (“Base de Conhecimento StoryBrand…”, “Pesquisa StoryBrand – Donald Miller”). Organizei por tema e acrescentei “Como usar” para acelerar pesquisa e citação.

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 29/47 - analise_concorrencia_conceito_core_22_20251113.md (30 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

#### 3.2 Performance - Parallel Research Execution
**Current State**: Sequential pilar execution (3-5 min)
**Enhancement**: Parallel execution of independent pillars
**Complexity**: High
**Time**: 20-30 min
**Commands**: `/adw_plan_build_test_iso`
**Deliverables**:
- Parallel execution framework
- Dependency mapping
- Result aggregation system
- Concurrency limits
- Performance benchmarks
**Expected Speed**: 50% reduction (2-2.5 min instead of 3-5 min)

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 30/47 - analise_concorrencia_conceito_core_23_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

# Research Agent System - Complete Documentation

**KEYWORDS**: research|agent|system|documentation|meta-pesquisa

Complete research agent system for automated market research, competitive analysis, and AI-powered prompt composition.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 31/47 - analise_concorrencia_conceito_core_24_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### 4. Competitors (90 minutes)
- Competitive analysis
- Market positioning
- Differentiation strategy
- **Best for**: Competitive moves

**Tags**: ecommerce, architectural

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 32/47 - analise_concorrencia_conceito_core_25_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Chunk 3: Competitor Insights
**Purpose**: Extract competitive intelligence

**Input**: Competitor data
**Output**: Advantages, positioning, messaging angles

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 33/47 - analise_concorrencia_conceito_core_26_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

### Communication Topology

```
ORCHESTRATOR (hub):
├── ↔ MARKET_RESEARCHER
├── ↔ COMPETITOR_ANALYST
├── ↔ KEYWORD_EXTRACTOR
├── ↔ DATA_VALIDATOR
├── ↔ PROMPT_COMPOSER
└── ↔ META_RESEARCHER

SPECIALIZED AGENTS:
├── MARKET_RESEARCHER → DATA_VALIDATOR
├── COMPETITOR_ANALYST → DATA_VALIDATOR
├── KEYWORD_EXTRACTOR → DATA_VALIDATOR
└── All agents report back to ORCHESTRATOR
```

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 34/47 - analise_concorrencia_conceito_core_27_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Typical Execution Times
- Quick research: 5-10 minutes
- Deep research: 20-30 minutes
- Keywords only: 2-5 minutes
- Competitors: 10-15 minutes
- AI-assisted: 5-15 minutes

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 35/47 - analise_concorrencia_conceito_core_28_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.63/1.00
**Data**: 20251113

## Conteúdo

### Expected Data Collection
- Market research: 5-10 insights
- Competitor analysis: 3-5 competitors analyzed
- Keywords: 50-200 keywords extracted
- FAQs: 10-20 common questions
- Quality score: 75-95%

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 36/47 - analise_concorrencia_conceito_core_29_20251113.md (23 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

### Agent Performance
- Market Researcher: 85% success rate, 120s avg
- Competitor Analyst: 90% success rate, 150s avg
- Keyword Extractor: 95% success rate, 90s avg
- Data Validator: 98% success rate, 30s avg
- Prompt Composer: 92% success rate, 45s avg

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 37/47 - analise_concorrencia_conceito_core_2_20251113.md (31 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

#### 2.2 E2E Tests - Complete Research Flow Validation
**Current State**: Manual testing only
**Enhancement**: Automated end-to-end test suite
**Complexity**: Medium
**Time**: 15-20 min
**Commands**: `/adw_plan_build_test_iso`
**Deliverables**:
- Unit tests per pilar
- Integration tests between pillars
- 5-chunk composition tests
- Quality threshold validation
- Performance benchmarks
- `.claude/commands/e2e/test_research_flow.md`
**Coverage Target**: 85%+ of research workflows

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 38/47 - analise_concorrencia_conceito_core_30_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Issue: Low quality scores
**Solution**:
- Add more competitor URLs (minimum 5)
- Increase research depth (use deep instead of quick)
- Check competitor URLs are accessible

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 39/47 - analise_concorrencia_conceito_core_31_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Issue: Slow execution
**Solution**:
- Use quick research type for faster results
- Skip FAQ collection for non-conversion focused research
- Cache competitor data between runs

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 40/47 - analise_concorrencia_conceito_core_32_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### v1.1.0 (Próximas horas)
- [ ] Integração com MCP Server (usar com Claude)
- [ ] Recomendações automáticas por IA
- [ ] Análise de histórico do cliente

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 41/47 - analise_concorrencia_conceito_core_33_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

#### Check Competitors
→ **Command**: `/analyze_competitors`
→ **Python**: `CompetitorAnalystAgent().execute()`
→ **File**: `research_agents.py:CompetitorAnalystAgent`

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 42/47 - analise_concorrencia_conceito_core_34_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Command Files (.claude/commands/)

| File | Invocation | Use Case |
|------|-----------|----------|
| `research.md` | `/research` | Full research workflow |
| `analyze_market.md` | `/analyze_market` | Market analysis only |
| `analyze_competitors.md` | `/analyze_competitors` | Competitor analysis only |
| `extract_keywords.md` | `/extract_keywords` | Keyword extraction only |
| `compose_prompts.md` | `/compose_prompts` | Prompt composition only |

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 43/47 - analise_concorrencia_conceito_core_35_20251113.md (32 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Output 3: 5 AI-Ready Prompts

Cada chunk é um prompt completo com:
- **System Prompt**: Define o papel do AI
- **User Prompt**: Define a tarefa específica
- **Context Data**: Dados contextuais da pesquisa
- **Expected Output**: Estrutura esperada do resultado

```
CHUNK 1: Research Consolidation
=================================

SYSTEM PROMPT:
"You are a strategic research analyst. Your role is to consolidate
market research and competitive intelligence into actionable insights..."

USER PR

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 44/47 - analise_concorrencia_conceito_core_36_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

### Caso 2: Análise de Concorrência

**Fluxo**:
1. Execute `/analyze_competitors` com URLs
2. Revise gaps e diferenciadores
3. Use Chunk 3 para estratégia de posicionamento

**Tempo total**: 3-5 minutos
**Resultado**: Estratégia competitiva clara

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 45/47 - analise_concorrencia_conceito_core_37_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Problema: Pesquisa lenta (>10 minutos)

**Solução**:
- Use `Research Type: quick` (5-10 min)
- Forneça apenas 1-2 competitor URLs
- Omita trends collection se não necessário

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 46/47 - analise_concorrencia_conceito_core_38_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.63/1.00
**Data**: 20251113

## Conteúdo

### Problema: Qualidade score baixa (<60%)

**Solução**:
- Verifique se marketplace está correto
- Adicione competitor URLs (melhora análise)
- Ajuste research type para "deep" (mais dados)

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 47/47 - analise_concorrencia_conceito_core_39_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

### Após a Pesquisa Inicial

1. **Revisar Relatório**: Dedique 10-15 minutos revisando os pilares
2. **Validar Keywords**: Confirme se as keywords fazem sentido
3. **Analisar Gaps**: Identifique as melhores oportunidades competitivas
4. **Usar Chunks**: Copie os prompts para Claude/ChatGPT

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- FIM DO CAPÍTULO 1 -->
<!-- Total: 47 versículos, 1177 linhas -->
