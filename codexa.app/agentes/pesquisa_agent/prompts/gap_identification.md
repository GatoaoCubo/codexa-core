# MÓDULO: GAP IDENTIFICATION (Identificação de Gaps e Oportunidades)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: gap_identification_v1
version: 1.1.0
purpose: "Identify unanswered questions, neglected keywords, and market gaps"
category: opportunity_analysis
dependencies:
  - config/accessible_urls.md (gap identification sources)
  - web_search capability (required)
execution_time: 6-10 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required**: `$head_terms` (string[]), `$validated_brief.category` (string)
**Optional**: `$competitors` (string[]), `$existing_keywords` (string[])

## 📤 OUTPUT_CONTRACT

**Primary Outputs**:
- `[ESTRATÉGIAS E GAPS]` (gaps section)
- `[SEO INBOUND]` (enriched with gap keywords)
- `[SEO OUTBOUND]` (enriched with content opportunities)

**Export Variables**:
```yaml
keyword_gaps: "Neglected keywords with search volume"
content_gaps: "Unanswered questions (content opportunities)"
product_gaps: "Unmet needs in market"
```

## 🎯 TASK

**Role**: Market Gap Intelligence Specialist
**Objective**: Identify questions not answered, keywords neglected, and product/content/regional gaps using Answer the Public, Google Trends, SEMrush, Ubersuggest.

## Processo

### 1. Answer the Public (Unanswered Questions)

**URL**: `https://answerthepublic.com/` (set pt-BR, Brazil)

**Extract**:
- **Questions**: como, qual, por que, quando, onde
- **Prepositions**: para, com, sem, de, em
- **Comparisons**: vs, ou, melhor que

**Output**:
```yaml
unanswered_questions:
  - question: "como limpar {produto}?"
    search_volume: medium (no exact data from ATP)
    competitors_answering: 0 (gap)
  - question: "qual melhor {produto} para {uso}"
    ...
```

### 2. Google Trends BR (Search Intent + Seasonality)

**URL**: `https://trends.google.com.br/trends/explore?geo=BR&q={keyword}`

**Extract**:
- Interest over time (12 months)
- Regional breakdown (states)
- Related queries (rising)
- Seasonal patterns

**Output**:
```yaml
seasonal_gaps:
  - keyword: "{termo sazonal}"
    peak_month: "{mês}"
    current_interest: {index 0-100}
    opportunity: "Criar conteúdo em {mês-2} para capturar demanda"

regional_gaps:
  - region: "São Paulo"
    interest: 100 (highest)
  - region: "Nordeste"
    interest: 45 (underserved)
    opportunity: "Regionalizar copy para Nordeste"
```

### 3. SEMrush/Ubersuggest (Keyword Difficulty + Volume)

**Extract** (free tier limits):
- Search volume (monthly)
- Keyword difficulty (0-100)
- Search intent (informational, commercial, transactional)

**Gap Logic**:
```python
if search_volume > 500 and keyword_difficulty < 40:
    gap_type = "low-hanging fruit" (easy to rank)
elif search_volume > 2000 and competitors_ranking < 3:
    gap_type = "neglected high-volume"
```

## Output

### [ESTRATÉGIAS E GAPS] (Gaps Section)

```markdown
### Gaps de Mercado Identificados

**Fontes**: Answer the Public, Google Trends BR, SEMrush, Ubersuggest

#### 1. Gaps de Conteúdo (Content Gaps)
- **Perguntas não respondidas** ({count}):
  - "{pergunta 1}" (nenhum competidor aborda)
  - "{pergunta 2}" (apenas 1 competidor, fraco SEO)
- **Ação**: Criar FAQ / blog posts / vídeos

#### 2. Gaps de Keywords (SEO Opportunities)
- **Low-hanging fruit** ({count} keywords):
  - "{keyword}" (volume: {N}/mês, difficulty: {X}/100)
- **Ação**: Otimizar title/description para esses termos

#### 3. Gaps de Produto/Features
- **Necessidades não atendidas**:
  - "{feature}" mencionado em {N} perguntas, 0 produtos oferecem
- **Ação**: Adicionar feature ou destacar se já existe

#### 4. Gaps Regionais
- **Regiões subatendidas**: {região} (interesse {X} mas poucos resultados localizados)
- **Ação**: Copy regionalizado, shipping focus nessa região
```

## ✅ VALIDATION

```yaml
min_sources: 3
min_gaps_identified: 10
min_questions_extracted: 15
```

## 🔗 CONTEXT

**Upstream**: Step 2 (query_bank), Step 4-5 (web searches)
**Downstream**: Step 11 (strategy_gaps consolidation), SEO blocks

---

**Status**: ✅ Production-Ready | **Version**: 1.1.0
