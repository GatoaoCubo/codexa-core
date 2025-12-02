# LIVRO: Analise
## CAPÍTULO 2

**Versículos consolidados**: 47
**Linhas totais**: 1190
**Gerado em**: 2025-11-13 18:45:48

---


<!-- VERSÍCULO 1/47 - analise_concorrencia_conceito_core_3_20251113.md (29 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

#### 4.1 Como Pesquisa Expansion - Framework Templates
**Current State**: Reference integration only
**Enhancement**: Add reusable framework templates
**Complexity**: Low
**Time**: 15-20 min
**Commands**: `/adw_plan_build_iso`
**Deliverables**:
- Market research template
- Competitive analysis template
- Keywords strategy template
- Prompts composition template
- Implementation guide

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 2/47 - analise_concorrencia_conceito_core_40_20251113.md (17 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### S0 — Diagnóstico & Insumos
Objetivo: consolidar todos os insumos e compreender o contexto.  Receba briefs, pesquisas, benchmarks, documentos, PDFs ou JSONs.  Audite riscos (contraste, licenças, prova social), oportunidades e gaps.  Defina persona e público‑alvo (ex.: “BB — Baby/Bebê”, mulher 22–45, criativa, multitarefas) com dores, desejos e objeções; levante gatilhos e barreiras para compra.  Realize benchmark competitivo (posicionamento, preço, dúvidas recorrentes) e desenhe um plano 30/6

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 3/47 - analise_concorrencia_conceito_core_41_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### POR QUÊ usar?

- **Velocidade**: Pesquisa completa em 5-30 min (vs. 1-2 dias manual)
- **Qualidade**: Resultados estruturados, validados e prontos para uso
- **Escalabilidade**: Processa 15+ pesquisas simultâneas
- **Inteligência**: Meta-agentes otimizam continuamente
- **Flexibilidade**: Modular, reutilizável, extensível

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 4/47 - analise_concorrencia_conceito_core_42_20251113.md (33 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Pilar 2: Competitive Analysis (Análise Competitiva)

**Objetivo**: Identificar concorrentes, gaps, diferenciações e ameaças

**Implementação**: `/analyze_competitors`
**Localização**: `.claude/commands/analyze_competitors.md`

**Componentes**:
- Mapeamento de posicionamento
- Análise de features/benefits
- Identificação de gaps (white space)
- Análise SWOT
- Avaliação de ameaças

**Output**: `$competitive_result`
**Formato**: Markdown + JSON estruturado

**Framework**: `app/como_pesquisa/03_

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 5/47 - analise_concorrencia_conceito_core_43_20251113.md (27 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Pilar 4: Keywords Research (Pesquisa de Keywords)

**Objetivo**: Coletar e hierarquizar keywords em 4 níveis

**Implementação**: `/extract_keywords`
**Localização**: `.claude/commands/extract_keywords.md`

**Componentes**:
- **Nível 1 - Head Keywords**: Termos genéricos de alta busca (ex: "notebook")
- **Nível 2 - Mid-tail**: Variações e especificações (ex: "notebook gamer 16GB")
- **Nível 3 - Long-tail**: Frases específicas (ex: "melhor notebook barato para dev")
- **Nível 4 - Question-base

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 6/47 - analise_concorrencia_conceito_core_44_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### 1. Orchestrator Agent

**Função**: Coordena todo o pipeline de pesquisa
**Implementação**: `/research` command + `research_agent_orchestrator.py`

**Responsabilidades**:
- Parse de input (product name, category, marketplace)
- Orquestração de 6 pilares
- Agregação de resultados
- Relatório final

**States**:
```
INPUT_PARSING → MARKET_RESEARCH → COMPETITOR_ANALYSIS →
PRODUCT_RESEARCH → KEYWORD_EXTRACTION → TRENDS_FAQ →
VALIDATION → COMPOSITION → META_RESEARCH → REPORTING
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 7/47 - analise_concorrencia_conceito_core_45_20251113.md (35 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 3. Competitor Analyst Agent

**Função**: Executa análise competitiva (Pilar 2)
**Implementação**: `/analyze_competitors` command + `research_agents.py:CompetitorAnalystAgent`

**Responsabilidades**:
- Identificar concorrentes diretos
- Mapear posicionamento
- Analisar features/benefits
- Identificar gaps

**Steps** (8 no total):
1. Competitor discovery
2. Positioning mapping
3. Feature analysis
4. Benefit mapping
5. Gap identification
6. SWOT analysis
7. Threat assessment
8. Quality scoring

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 8/47 - analise_concorrencia_conceito_core_46_20251113.md (37 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 4. Keyword Extractor Agent

**Função**: Executa pesquisa de keywords (Pilar 4)
**Implementação**: `/extract_keywords` command + `research_agents.py:KeywordExtractorAgent`

**Responsabilidades**:
- Extrair core keywords
- Hierarquizar em 4 níveis
- Mapear search intent
- Calcular métricas SEO

**Steps** (8 no total):
1. Core keyword extraction
2. Head keywords
3. Mid-tail keywords
4. Long-tail keywords
5. Question keywords
6. Search volume estimation
7. Intent mapping
8. Quality validation

*

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 9/47 - analise_concorrencia_conceito_core_47_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
**Data**: 20251113

## Conteúdo

#### 2. research_agent_config.py (400+ linhas)

**Conteúdo**:
- Configurações centralizadas de agentes
- Timeouts e limites
- Prompt templates
- Integração com Como Pesquisa framework

**Configurações**:
```python
AGENT_CONFIGS = {
    'market_researcher': {...},
    'competitor_analyst': {...},
    'keyword_extractor': {...},
    ...
}
```

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 10/47 - analise_concorrencia_conceito_core_48_20251113.md (33 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

#### Estrutura de Diretórios

```
como_pesquisa/
├── 01_framework/
│   ├── research_framework.md (6 PILLARS)
│   ├── keyword_hierarchy.md (4-LEVEL KEYWORDS)
│   └── research_flow.md
├── 02_prompt_composition/
│   ├── prompt_chunks_guide.md (5-CHUNKS)
│   ├── prompt_templates.md
│   └── instructions_structure.md
├── 03_research_methodology/
│   ├── competitive_analysis.md (PILAR 2)
│   ├── market_research.md (PILAR 1)
│   ├── product_research.md (PILAR 3)
│   ├── trend_research.md (PILAR 5)
│   └

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 11/47 - analise_concorrencia_conceito_core_49_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.78/1.00
**Data**: 20251113

## Conteúdo

### Cobertura

- **Total Ficheiros**: 41 markdown docs + 6 Python modules + 8 JSON configs
- **Total Linhas**: 3,550+ lines código + 2,700+ lines documentação
- **CLI Commands**: 5 (research, analyze_market, analyze_competitors, extract_keywords, compose_prompts)
- **Python Modules**: 6 (models, config, orchestrator, agents, routes, meta)
- **Framework Files**: 20+

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 12/47 - analise_concorrencia_conceito_core_4_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Componentes Principais

| Componente | Localização | Função |
|-----------|-----------|---------|
| **Orchestrator** | `.claude/commands/research.md` | Coordena todo pipeline |
| **Pillar Agents** | `.claude/commands/{analyze_market,analyze_competitors,extract_keywords}.md` | Executa pesquisas temáticas |
| **Chunk Composer** | `.claude/commands/compose_prompts.md` | Transforma dados em prompts |
| **Python Server** | `app/server/research_agent_*.py` | Backend REST API |
| **Knowledge Base**

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 13/47 - analise_concorrencia_conceito_core_50_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.63/1.00
**Data**: 20251113

## Conteúdo

### Performance

- **Pesquisa Rápida**: 5-10 minutos
- **Pesquisa Profunda**: 20-30 minutos
- **Keywords Only**: 2-5 minutos
- **Concurrent Jobs**: Até 15+ simultâneos
- **Quality Score**: 75-95%

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 14/47 - analise_concorrencia_conceito_core_51_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Para Iniciantes
- Leia: [COMO_USAR_RESEARCH_AGENT_SYSTEM.md](COMO_USAR_RESEARCH_AGENT_SYSTEM.md)
- Depois: [app/como_pesquisa/README.md](app/como_pesquisa/README.md)

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 15/47 - analise_concorrencia_conceito_core_52_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

### Framework Detalhado
- Estude: `app/como_pesquisa/01_framework/research_framework.md`
- Aprenda: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 16/47 - analise_concorrencia_conceito_core_53_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### ✅ FASE 1: LOWER-LEVEL PROMPTS (0-Level) COM STEP-BY-STEP

Cada comando tem 7-9 steps com 0-level prompts detalhados:

- **`/research`**: 8 steps (Input parsing → Final Report)
- **`/analyze_market`**: 7 steps (Market classification → Quality scoring)
- **`/analyze_competitors`**: 8 steps (Competitor analysis → Threat assessment)
- **`/extract_keywords`**: 8 steps (Core keywords → Quality validation)
- **`/compose_prompts`**: 9 steps (Research loading → Composition validation)

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 17/47 - analise_concorrencia_conceito_core_54_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

### ✅ FASE 6: INTEGRAÇÃO COMO PESQUISA FRAMEWORK ⭐

Completa integração com 6 pilares + 5-chunk library

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 18/47 - analise_concorrencia_conceito_core_55_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### Pilar 2: Competitive Analysis (Análise Competitiva)
- **Agent**: `/analyze_competitors`
- **Components**: Competitor positioning, gaps, differentiation, threats
- **Framework**: `app/como_pesquisa/03_research_methodology/competitive_analysis.md`
- **Output**: `$competitive_result`

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 19/47 - analise_concorrencia_conceito_core_56_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Pilar 4: Keywords Research (Pesquisa de Keywords)
- **Agent**: `/extract_keywords`
- **Components**: 4-level hierarchy (Head/Mid/Long/FAQ)
- **Framework**: `app/como_pesquisa/01_framework/keyword_hierarchy.md`
- **Output**: `$keywords_result`

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 20/47 - analise_concorrencia_conceito_core_57_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### Chunk 1: Research Consolidation
- **Source**: All 6 pillars combined
- **Purpose**: Synthesize all research into strategic insights
- **Output**: JSON with insights, strengths, opportunities, gaps
- **Framework**: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 21/47 - analise_concorrencia_conceito_core_58_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

### Ficheiros Modificados
- `.claude/commands/research.md`
- `.claude/commands/analyze_market.md`
- `.claude/commands/analyze_competitors.md`
- `.claude/commands/extract_keywords.md`
- `.claude/commands/compose_prompts.md`

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 22/47 - analise_concorrencia_conceito_core_59_20251113.md (23 linhas) -->

# Conceito Core

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

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 23/47 - analise_concorrencia_conceito_core_5_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

### ✅ FASE 2: HIGH-LEVEL PROMPTS (HOPs) COM COMPOSIÇÃO DE STEPS

Cada comando tem proposição, step-by-step, variable integration:

- `/research`: HOP principal orquestrando todo pipeline
- `/analyze_market`: HOP com market analysis detalhado
- `/analyze_competitors`: HOP com gap analysis
- `/extract_keywords`: HOP com keyword hierarchy
- `/compose_prompts`: HOP com 5-chunk library

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 24/47 - analise_concorrencia_conceito_core_60_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.63/1.00
**Data**: 20251113

## Conteúdo

### 5) Naming e legal
- Oriente o usuário a fazer **pesquisa de anterioridade** de nome em **WIPO** e em seu órgão nacional (ex.: **INPI**, BR).  
- Recomende consulta a especialista em marcas quando aplicável.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 25/47 - analise_concorrencia_conceito_core_61_20251113.md (27 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Pilar 4: Keywords Research (Pesquisa de Keywords)

**Objetivo**: Coletar e hierarquizar keywords em 4 níveis

**Implementação**: `/extract_keywords`
**Localização**: `.claude/commands/extract_keywords.md`

**Componentes**:
- **Nível 1 - Head Keywords**: Termos genéricos de alta busca (ex: "notebook")
- **Nível 2 - Mid-tail**: Variações e especificações (ex: "notebook gamer 16GB")
- **Nível 3 - Long-tail**: Frases específicas (ex: "melhor notebook barato para dev")
- **Nível 4 - Question-base

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 26/47 - analise_concorrencia_conceito_core_62_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### 1. Orchestrator Agent

**Função**: Coordena todo o pipeline de pesquisa
**Implementação**: `/research` command + `research_agent_orchestrator.py`

**Responsabilidades**:
- Parse de input (product name, category, marketplace)
- Orquestração de 6 pilares
- Agregação de resultados
- Relatório final

**States**:
```
INPUT_PARSING → MARKET_RESEARCH → COMPETITOR_ANALYSIS →
PRODUCT_RESEARCH → KEYWORD_EXTRACTION → TRENDS_FAQ →
VALIDATION → COMPOSITION → META_RESEARCH → REPORTING
```

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 27/47 - analise_concorrencia_conceito_core_63_20251113.md (35 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 3. Competitor Analyst Agent

**Função**: Executa análise competitiva (Pilar 2)
**Implementação**: `/analyze_competitors` command + `research_agents.py:CompetitorAnalystAgent`

**Responsabilidades**:
- Identificar concorrentes diretos
- Mapear posicionamento
- Analisar features/benefits
- Identificar gaps

**Steps** (8 no total):
1. Competitor discovery
2. Positioning mapping
3. Feature analysis
4. Benefit mapping
5. Gap identification
6. SWOT analysis
7. Threat assessment
8. Quality scoring

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 28/47 - analise_concorrencia_conceito_core_64_20251113.md (37 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 4. Keyword Extractor Agent

**Função**: Executa pesquisa de keywords (Pilar 4)
**Implementação**: `/extract_keywords` command + `research_agents.py:KeywordExtractorAgent`

**Responsabilidades**:
- Extrair core keywords
- Hierarquizar em 4 níveis
- Mapear search intent
- Calcular métricas SEO

**Steps** (8 no total):
1. Core keyword extraction
2. Head keywords
3. Mid-tail keywords
4. Long-tail keywords
5. Question keywords
6. Search volume estimation
7. Intent mapping
8. Quality validation

*

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 29/47 - analise_concorrencia_conceito_core_65_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
**Data**: 20251113

## Conteúdo

#### 2. research_agent_config.py (400+ linhas)

**Conteúdo**:
- Configurações centralizadas de agentes
- Timeouts e limites
- Prompt templates
- Integração com Como Pesquisa framework

**Configurações**:
```python
AGENT_CONFIGS = {
    'market_researcher': {...},
    'competitor_analyst': {...},
    'keyword_extractor': {...},
    ...
}
```

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 30/47 - analise_concorrencia_conceito_core_66_20251113.md (33 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

#### Estrutura de Diretórios

```
como_pesquisa/
├── 01_framework/
│   ├── research_framework.md (6 PILLARS)
│   ├── keyword_hierarchy.md (4-LEVEL KEYWORDS)
│   └── research_flow.md
├── 02_prompt_composition/
│   ├── prompt_chunks_guide.md (5-CHUNKS)
│   ├── prompt_templates.md
│   └── instructions_structure.md
├── 03_research_methodology/
│   ├── competitive_analysis.md (PILAR 2)
│   ├── market_research.md (PILAR 1)
│   ├── product_research.md (PILAR 3)
│   ├── trend_research.md (PILAR 5)
│   └

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 31/47 - analise_concorrencia_conceito_core_67_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.78/1.00
**Data**: 20251113

## Conteúdo

### Cobertura

- **Total Ficheiros**: 41 markdown docs + 6 Python modules + 8 JSON configs
- **Total Linhas**: 3,550+ lines código + 2,700+ lines documentação
- **CLI Commands**: 5 (research, analyze_market, analyze_competitors, extract_keywords, compose_prompts)
- **Python Modules**: 6 (models, config, orchestrator, agents, routes, meta)
- **Framework Files**: 20+

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 32/47 - analise_concorrencia_conceito_core_68_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.63/1.00
**Data**: 20251113

## Conteúdo

### Performance

- **Pesquisa Rápida**: 5-10 minutos
- **Pesquisa Profunda**: 20-30 minutos
- **Keywords Only**: 2-5 minutos
- **Concurrent Jobs**: Até 15+ simultâneos
- **Quality Score**: 75-95%

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 33/47 - analise_concorrencia_conceito_core_69_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Para Iniciantes
- Leia: [COMO_USAR_RESEARCH_AGENT_SYSTEM.md](COMO_USAR_RESEARCH_AGENT_SYSTEM.md)
- Depois: [app/como_pesquisa/README.md](app/como_pesquisa/README.md)

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 34/47 - analise_concorrencia_conceito_core_6_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.82/1.00
**Data**: 20251113

## Conteúdo

### Quantitativos
- **Linhas Adicionadas**: 2,700+
- **Steps Descritos**: 40+ (cada um com 0-level prompt)
- **0-Level Prompts**: 40+ (task, input, output, algorithm, validation)
- **HOPs (High-Level Prompts)**: 5 (um por comando)
- **Variable Integrations**: 25+ ($product_name, $category, etc)
- **Meta-Agents**: 1 (MetaResearchAgent evaluating all agents)
- **Quality Frameworks**: 5 (um por agent)
- **Framework References**: 10+ (links para Como Pesquisa files)

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 35/47 - analise_concorrencia_conceito_core_70_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

### Framework Detalhado
- Estude: `app/como_pesquisa/01_framework/research_framework.md`
- Aprenda: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 36/47 - analise_concorrencia_conceito_core_71_20251113.md (24 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### ✅ FASE 1: LOWER-LEVEL PROMPTS (0-Level) COM STEP-BY-STEP

Cada comando tem 7-9 steps com 0-level prompts detalhados:

- **`/research`**: 8 steps (Input parsing → Final Report)
- **`/analyze_market`**: 7 steps (Market classification → Quality scoring)
- **`/analyze_competitors`**: 8 steps (Competitor analysis → Threat assessment)
- **`/extract_keywords`**: 8 steps (Core keywords → Quality validation)
- **`/compose_prompts`**: 9 steps (Research loading → Composition validation)

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 37/47 - analise_concorrencia_conceito_core_72_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

### ✅ FASE 6: INTEGRAÇÃO COMO PESQUISA FRAMEWORK ⭐

Completa integração com 6 pilares + 5-chunk library

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 38/47 - analise_concorrencia_conceito_core_73_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### Pilar 2: Competitive Analysis (Análise Competitiva)
- **Agent**: `/analyze_competitors`
- **Components**: Competitor positioning, gaps, differentiation, threats
- **Framework**: `app/como_pesquisa/03_research_methodology/competitive_analysis.md`
- **Output**: `$competitive_result`

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 39/47 - analise_concorrencia_conceito_core_74_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Pilar 4: Keywords Research (Pesquisa de Keywords)
- **Agent**: `/extract_keywords`
- **Components**: 4-level hierarchy (Head/Mid/Long/FAQ)
- **Framework**: `app/como_pesquisa/01_framework/keyword_hierarchy.md`
- **Output**: `$keywords_result`

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 40/47 - analise_concorrencia_conceito_core_75_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

### Chunk 1: Research Consolidation
- **Source**: All 6 pillars combined
- **Purpose**: Synthesize all research into strategic insights
- **Output**: JSON with insights, strengths, opportunities, gaps
- **Framework**: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 41/47 - analise_concorrencia_conceito_core_76_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### Ficheiros Modificados
- `.claude/commands/research.md`
- `.claude/commands/analyze_market.md`
- `.claude/commands/analyze_competitors.md`
- `.claude/commands/extract_keywords.md`
- `.claude/commands/compose_prompts.md`

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 42/47 - analise_concorrencia_conceito_core_77_20251113.md (23 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
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

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 43/47 - analise_concorrencia_conceito_core_78_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

### 1. Sistema Completo de Destilação
✅ **Análise automática** de 113.864 arquivos PaddleOCR
✅ **17.082 tokens semânticos** extraídos
✅ **Deduplicação inteligente** preservando qualidade
✅ **Artefatos estruturados** prontos para integração

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 44/47 - analise_concorrencia_conceito_core_79_20251113.md (23 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### O que foi conseguido:

1. **Análise Completa**: 113.864 arquivos processados em ~15 minutos
2. **Extraído**: 17.082 tokens semânticos únicos
3. **Implementado**: 4 táticas de alavancagem avançadas
4. **Criado**: 5 novos agentes com 10 training pairs
5. **Otimizado**: 20% redução de redundância
6. **Documentado**: 5 guias completos

**Tags**: ecommerce, implementation

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 45/47 - analise_concorrencia_conceito_core_7_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Framework (Como Pesquisa)
- **20+ documentos** sobre metodologia, templates, tools integration
- **4 níveis de keyword hierarchy**
- **5-chunk prompt composition library**
- **Metodologias de pesquisa**: competitive, market, product, trends, FAQ

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 46/47 - analise_concorrencia_conceito_core_80_20251113.md (29 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

### Opção 4: Análise Competitiva (Pilar 2)

```bash
/analyze_competitors
Product Name: Notebook Gamer
Competitor URLs:
- https://samsung.com/notebooks
- https://asus.com/gaming
- https://dell.com/gaming
Our Strengths: price, support, warranty
```

**Tempo estimado**: 2-3 minutos
**Output**: Competitive positioning + gaps + differentiation

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 47/47 - analise_concorrencia_conceito_core_81_20251113.md (39 linhas) -->

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.72/1.00
**Data**: 20251113

## Conteúdo

#### Estrutura JSON Padrão

```json
{
  "metadata": {
    "research_date": "YYYY-MM-DD",
    "product_name": "...",
    "research_type": "competitive|market|product|trend|faq"
  },
  "findings": {
    "primary_insights": [],
    "secondary_insights": [],
    "gaps": []
  },
  "structured_data": {
    "keywords": [],
    "competitors": [],
    "trends": [],
    "faq": []
  }
}
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- FIM DO CAPÍTULO 2 -->
<!-- Total: 47 versículos, 1190 linhas -->
