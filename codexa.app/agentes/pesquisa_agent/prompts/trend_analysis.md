# MÓDULO: TREND ANALYSIS (Análise de Tendências)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: trend_analysis_v1
version: 1.1.0
purpose: "Identify emerging trends (micro/macro), consumer behavior, market forecasts"
category: market_intelligence
dependencies:
  - config/accessible_urls.md (trend sources)
  - web_search capability (required)
execution_time: 10-15 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required**: `$validated_brief.category` (string), `$head_terms` (string[])
**Optional**: `$validated_brief.launch_timeline` (object)

## 📤 OUTPUT_CONTRACT

**Primary Output**: `[ESTRATÉGIAS E GAPS]` (trends section)

**Export Variables**:
```yaml
macro_trends: "Long-term market movements (1-3 years)"
active_trends: "Current trending topics (3-6 months)"
micro_trends: "Emerging micro-trends (<3 months)"
timing_recommendation: "Best timing for launch/campaign"
```

## 🎯 TASK

**Role**: Trend Intelligence Specialist
**Objective**: Analyze 10 sources (Think with Google BR, TikTok Creative Center, Pinterest, ML Trends, Statista, IBGE, Euromonitor, ABComm, Meta Insights) to identify trends and timing opportunities.

## Processo

### 1. Think with Google Brasil (Consumer Behavior)

**URL**: `https://www.thinkwithgoogle.com/intl/pt-br/tendencias-de-consumo/`

**Extract**:
- Micro-moments studies
- Search behavior trends
- Category-specific insights

### 2. TikTok Creative Center (Viral Content)

**URL**: `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/pt?region=BR`

**Extract**:
- Trending hashtags (last 7/30 days)
- Viral products by category
- Creator insights

### 3. Pinterest Trends (Visual Trends)

**URL**: `https://trends.pinterest.com/country/brazil/`

**Extract**:
- Rising search terms
- Visual aesthetics
- Seasonal predictions

### 4. Mercado Livre Trends (E-commerce Data)

**URL**: `https://www.mercadolivre.com.br/tendencias/`

**Extract**:
- Best-selling products (daily/weekly/monthly)
- Category growth %
- Seasonal hot products

### 5. Statista Brazil (Market Size + Projections)

**Extract** (free tier):
- Market size (BRL)
- Growth projections (CAGR)
- E-commerce penetration %

### 6. IBGE (Economic Data)

**Extract**:
- Retail sales volume (monthly)
- Income by region
- Consumer spending patterns

### 7. Euromonitor / ABComm / Meta (Industry Reports)

**Extract** (limited free data):
- Market forecasts
- Payment trends (Pix, installments)
- Social commerce insights

## Output

### [ESTRATÉGIAS E GAPS] (Trends Section)

```markdown
### Análise de Tendências

**Fontes**: Think with Google BR, TikTok, Pinterest, ML Trends, Statista, IBGE, ABComm, Meta

#### Macro-Tendências (1-3 anos)
1. **{macro_trend_1}** (fonte: {Statista/IBGE})
   - Projeção: Crescimento de {X}% CAGR até {ano}
   - Impacto na categoria: {alto|médio|baixo}

#### Tendências Ativas (3-6 meses)
1. **{trend_1}** (fonte: {TikTok/ML Trends})
   - Status: Em alta (+{X}% interesse último mês)
   - Janela de oportunidade: {timing}

#### Micro-Tendências Emergentes (<3 meses)
1. **{micro_trend_1}** (fonte: {Pinterest/TikTok})
   - Estágio: Emerging (ainda não saturado)
   - Recomendação: {ação imediata}

### Timing Estratégico
- **Momento Atual**: {favorável|neutro|desfavorável} para entrada
- **Melhor Timing**: {quando lançar / quando fazer campanha}
- **Sazonalidade**: Picos em {meses}, queda em {meses}
```

## ✅ VALIDATION

```yaml
min_sources: 5
min_trends_identified: 8
timing_recommendation_required: true
```

## 🔗 CONTEXT

**Upstream**: Steps 1-9 (todos inputs anteriores)
**Downstream**: Step 11 (strategy_gaps), final recommendations

---

**Status**: ✅ Production-Ready | **Version**: 1.1.0
