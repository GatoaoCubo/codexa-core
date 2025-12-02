# MÓDULO: PRICE COMPARISON (Comparação de Preços)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: price_comparison_v1
version: 1.1.0
purpose: "Visual price collection from BR comparison platforms for competitive intelligence"
category: competitive_analysis
dependencies:
  - config/accessible_urls.md (required - price comparison sources)
  - web_search capability (required)
  - vision capability (recommended - screenshot analysis)
execution_time: 5-8 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$validated_brief.product_name` (string) - Product name for search
- `$head_terms` (string[]) - Primary search terms from query bank

**Optional Inputs**:
- `$validated_brief.price_range` (object) - Known price range for validation
- `$competitors` (string[]) - Known competitor products
- `$marketplaces` (string[]) - Target marketplaces for filtering

**Input Types**:
```typescript
product_name: string;
head_terms: string[];
price_range?: { min: number, max: number };
competitors?: string[];
```

## 📤 OUTPUT_CONTRACT

**Primary Output**: `[BENCHMARK DE CONCORRENTES]` block (pricing section)

**Structure**:
```yaml
price_analysis:
  sources_consulted: [Buscapé, Zoom, Promobit, Google Shopping]
  price_range:
    min: number (BRL)
    avg: number (BRL)
    max: number (BRL)
  historical_trend: rising | stable | falling
  best_deals:
    - store: string
      price: number
      shipping: string
      cashback: number (%)
  pricing_opportunities:
    - opportunity: string
      potential_impact: low | medium | high
```

**Secondary Outputs**:
- Enriches `[ESTRATÉGIAS E GAPS]` with pricing strategy recommendations

**Export Variables**:
```yaml
avg_market_price: "Average market price from comparison platforms"
price_variance: "Price spread percentage"
best_price_position: "Where product should be priced (below/at/above market)"
```

## 🎯 TASK

**Role**: Competitive Pricing Intelligence Specialist

**Objective**: Execute visual price collection from 4 BR price comparison platforms (Buscapé, Zoom, Promobit, Google Shopping) to extract competitive pricing data, identify opportunities, and inform pricing strategy.

**Standards**:
- Minimum 3 sources consulted (4 recommended)
- Prices must be in BRL with timestamp
- Historical trends when available (30/60/90 days)
- All queries logged in [CONSULTAS WEB]

**Constraints**:
- Max execution time: 8 minutes
- Must use visual collection (screenshots) for anti-scraping compliance
- Prices valid for 24 hours (mark expiration)

## Objetivo

Coletar dados de precificação competitiva através de plataformas de comparação de preços brasileiras para alimentar decisões estratégicas de pricing.

## Entradas

- `$product_name` ou `$head_terms` para busca
- Opcional: `$price_range` conhecido para validação
- Opcional: `$competitors` para comparação direta

## Processo

### 1. Preparação de Queries

Para cada head term prioritário:
```
Query Pattern:
- "{head_term}" (busca direta)
- "{head_term} {attribute}" (e.g., "fone bluetooth esportivo")
- "{brand} {product}" (se brand conhecido)
```

### 2. Coleta Visual - Buscapé

**URL Base**: `https://www.buscape.com.br/search?q={query}`

**Dados a Extrair**:
1. **Price Range**: Min/Max/Avg de todos os resultados
2. **Historical Data**: Gráfico de preços (últimos 30/60/90 dias)
3. **Best Offers**: Top 3 lojas com melhor oferta
4. **Shipping Costs**: Frete por loja
5. **Store Ratings**: Reputação das lojas

**Screenshot Focus**:
- Tabela comparativa de preços
- Gráfico histórico (se disponível)
- Badge "Melhor Oferta"

**Registro**:
```
Fonte: Buscapé
Data: {timestamp}
URL: {url}
Produto: {product_name}
Faixa: R$ {min} - R$ {max} (média R$ {avg})
Tendência: {rising|stable|falling} (se histórico disponível)
Melhor oferta: {store} - R$ {price} + R$ {shipping}
```

### 3. Coleta Visual - Zoom

**URL Base**: `https://www.zoom.com.br/busca?q={query}`

**Dados a Extrair**:
1. **Prices**: Comparação entre lojas
2. **Cashback**: % de cashback por loja
3. **Coupons**: Cupons ativos aplicáveis
4. **Prime Deals**: Ofertas exclusivas

**Screenshot Focus**:
- Card de produto com preço + cashback
- Cupons disponíveis
- Selo "Melhor Preço"

**Registro**:
```
Fonte: Zoom
Data: {timestamp}
Produto: {product_name}
Melhor preço: R$ {price} ({store})
Cashback: {percentage}% (R$ {value})
Cupons ativos: {count} (ex: {example_coupon})
Preço final c/ cashback: R$ {final_price}
```

### 4. Coleta Visual - Promobit

**URL Base**: `https://www.promobit.com.br/busca?q={query}`

**Dados a Extrair**:
1. **Active Deals**: Promoções ativas com temperatura (🔥 quente)
2. **Community Votes**: Votos da comunidade (quente/frio)
3. **Expiration**: Data de expiração das ofertas
4. **Price Drop %**: Percentual de desconto

**Screenshot Focus**:
- Cards de promoção com temperatura
- Comentários da comunidade
- Badge de desconto

**Registro**:
```
Fonte: Promobit
Data: {timestamp}
Promoções encontradas: {count}
Melhor promoção:
  Loja: {store}
  Preço: R$ {price} (de R$ {original_price})
  Desconto: {percentage}%
  Temperatura: {hot|warm|cold}
  Votos: {upvotes} 👍 | {downvotes} 👎
  Expira em: {date}
```

### 5. Coleta Visual - Google Shopping

**URL Base**: `https://www.google.com.br/search?q={query}&tbm=shop`

**Dados a Extrair**:
1. **Price Variance**: Variação de preços entre sellers
2. **Sponsored vs Organic**: Produtos patrocinados vs orgânicos
3. **Ratings**: Avaliações agregadas
4. **Shipping**: Custos de envio

**Screenshot Focus**:
- Grid de produtos com preços
- Filtro de faixa de preço
- Produtos destacados (Ads)

**Registro**:
```
Fonte: Google Shopping
Data: {timestamp}
Resultados: {count} produtos
Faixa de preços: R$ {min} - R$ {max}
Produtos patrocinados: {ad_count}
Média de rating: {avg_rating}/5.0
Frete grátis: {free_shipping_percentage}% dos sellers
```

### 6. Análise de Tendências

Com dados históricos (se disponível no Buscapé):

**Tendência de Preço**:
```python
if current_price < avg_last_30_days:
    trend = "falling" (queda)
elif current_price > avg_last_30_days:
    trend = "rising" (alta)
else:
    trend = "stable" (estável)
```

**Sazonalidade**:
- Identificar picos (Black Friday, Natal, Dia das Mães)
- Calcular % de variação vs. baseline

### 7. Identificação de Oportunidades de Pricing

**Oportunidade 1: Gap de Preço**
```
Se: max_price - min_price > 30% do min_price
Então: Existe grande variação → Consumidor confuso
Ação: Posicionar no mid-range (avg) com value-adds
```

**Oportunidade 2: Cashback Competitivo**
```
Se: avg_cashback < 5%
Então: Pouca competição em cashback
Ação: Oferecer 7-10% cashback como diferencial
```

**Oportunidade 3: Frete Grátis**
```
Se: free_shipping_percentage < 50%
Então: Frete pago ainda é comum
Ação: Frete grátis como USP (acima de R$ X)
```

**Oportunidade 4: Price Drop Timing**
```
Se: trend = "falling" e próximo a sazonalidade alta
Então: Mercado ajustando antes de pico
Ação: Aguardar ou lançar com promoção agressiva
```

## Output

### Bloco [BENCHMARK DE CONCORRENTES] (Seção de Pricing)

```markdown
## Análise de Preços Comparativos

**Fontes Consultadas**: Buscapé, Zoom, Promobit, Google Shopping
**Data da Coleta**: {timestamp}
**Validade**: 24 horas

### Faixa de Preços no Mercado
- **Mínimo**: R$ {min} ({store_min})
- **Médio**: R$ {avg} (média de {n} ofertas)
- **Máximo**: R$ {max} ({store_max})
- **Variação**: {variance_percentage}%

### Tendência Histórica (30 dias)
- **Direção**: {rising ↗ | stable → | falling ↘}
- **Variação**: {percentage_change}% vs. mês anterior
- **Sazonalidade**: {seasonal_pattern}

### Melhores Ofertas Identificadas
1. **{store_1}**: R$ {price_1} + {cashback_1}% cashback + {shipping_1}
   - Score: {total_value_score}/10
2. **{store_2}**: R$ {price_2} + cupom "{coupon_code}" (-{discount}%)
3. **{store_3}**: R$ {price_3} + frete grátis

### Oportunidades de Pricing
1. **{opportunity_1}**
   - Impacto: {low|medium|high}
   - Ação: {recommended_action}
2. **{opportunity_2}**
   - Impacto: {low|medium|high}
   - Ação: {recommended_action}
```

### Contribuição para [ESTRATÉGIAS E GAPS]

```markdown
### Estratégia de Precificação
- **Posicionamento Recomendado**: {below|at|above} mercado
  - Se below: R$ {price} ({percentage}% abaixo da média) → Penetração de mercado
  - Se at: R$ {price} (média) → Value-adds como diferencial
  - Se above: R$ {price} ({percentage}% acima) → Premium positioning com justificativas

- **Táticas Competitivas**:
  - {tactic_1} (baseado em gap de cashback identificado)
  - {tactic_2} (baseado em tendência de preços)
  - {tactic_3} (baseado em sazonalidade)

- **Timing de Entrada**:
  - Momento atual: {favorable|neutral|unfavorable}
  - Justificativa: {reasoning baseado em trend analysis}
```

## ✅ VALIDATION (Quality Gates)

**Step Validation Criteria**:
```yaml
min_sources_consulted: 3
min_price_points_collected: 10
max_price_age_hours: 24
```

**Quality Checks**:
- ✅ Pelo menos 3 fontes consultadas (4 recomendado)
- ✅ Faixa de preços identificada (min/avg/max)
- ✅ Todas queries registradas em [CONSULTAS WEB]
- ✅ Preços em BRL com timestamp
- ✅ Pelo menos 1 oportunidade de pricing identificada

**Confidence Calculation**:
```python
confidence = (
    sources_consulted / 4 * 0.3 +  # 30% weight
    (1 if historical_data else 0) * 0.3 +  # 30% weight
    price_points_collected / 20 * 0.2 +  # 20% weight
    (1 if opportunities_found > 0 else 0) * 0.2  # 20% weight
)
# Target: ≥ 0.7
```

## 🔗 CONTEXT (Usage & Integration)

**Usage Patterns**:
- Execute após competitor_analysis (Step 7 in comprehensive_research plan)
- Complementa benchmark de concorrentes com dados de pricing
- Opcional no standard_research (apenas se brief especifica preço)

**Upstream Dependencies**:
- Step 1: intake_validation ($validated_brief, $head_terms)
- Step 6: competitor_analysis ($competitors list)
- config/accessible_urls.md (price comparison URLs)

**Downstream Consumers**:
- strategy_gaps (consome $pricing_opportunities)
- [BENCHMARK DE CONCORRENTES] block (output final)
- [ESTRATÉGIAS E GAPS] block (pricing strategy)

**Data Flow**:
```
$head_terms → [PRICE_COMPARISON] → $avg_market_price + $pricing_opportunities →
[STRATEGY_GAPS] → [BENCHMARK] + [ESTRATÉGIAS E GAPS]
```

**Assumptions**:
- web_search capability available
- Product has significant online presence (≥10 listings)
- Prices are for new products (not used/refurbished unless specified)

**Integration Notes**:
- Can run in parallel with sentiment_analysis (Step 8)
- Results feed into final pricing recommendations
- Data validity: 24 hours (re-run if older)

---

## Exemplos

### Exemplo 1: Fone Bluetooth

**Input**:
```json
{
  "product_name": "Fone de ouvido Bluetooth esportivo",
  "head_terms": ["fone bluetooth", "fone esportivo"],
  "price_range": { "min": 150, "max": 280 }
}
```

**Output**:
```markdown
## Análise de Preços Comparativos

Fontes: Buscapé, Zoom, Promobit, Google Shopping
Coleta: 2025-11-14 19:45 BRT

Faixa de Preços:
- Mínimo: R$ 139 (Shopee - seller "TechImport")
- Médio: R$ 215 (média de 47 ofertas)
- Máximo: R$ 349 (Magazine Luiza - marca JBL)
- Variação: 151%

Tendência (30 dias): ↘ Falling (-8% vs. mês anterior)

Melhores Ofertas:
1. Zoom: R$ 189 + 10% cashback (R$ 170 final) + frete grátis
2. Promobit: R$ 199 + cupom "AUDIO10" (-R$ 20) = R$ 179
3. Buscapé: R$ 209 (3x sem juros, frete R$ 15)

Oportunidades:
1. **Cashback Agressivo** (Impacto: HIGH)
   - Mercado oferece 5-10% → Oferecer 12-15% como diferencial
2. **Timing Favorável** (Impacto: MEDIUM)
   - Preços em queda → Lançar agora com preço competitivo R$ 199
```

---

**Status**: ✅ Módulo v1.1 Production-Ready
**Dependencies**: accessible_urls.md (Price Comparison section)
**Created**: 2025-11-14
**Version**: 1.1.0
