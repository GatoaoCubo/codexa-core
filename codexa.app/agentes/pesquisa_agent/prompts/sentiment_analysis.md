# MÓDULO: SENTIMENT ANALYSIS (Análise de Sentimento de Mercado)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: sentiment_analysis_v1
version: 1.1.0
purpose: "Extract pain points, gains, objections from reviews/complaints for customer insight"
category: customer_intelligence
dependencies:
  - config/accessible_urls.md (required - sentiment sources)
  - web_search capability (required)
  - Reclame Aqui (MANDATORY source)
execution_time: 8-12 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$validated_brief.product_name` (string) - Product name
- `$head_terms` (string[]) - Search terms
- `$competitors` (string[]) - Competitor list from competitor_analysis

**Optional Inputs**:
- `$validated_brief.brand` (string) - Brand name for brand-specific sentiment
- `$marketplaces` (string[]) - Focus on specific marketplaces

**Input Types**:
```typescript
product_name: string;
head_terms: string[];
competitors: string[];
brand?: string;
```

## 📤 OUTPUT_CONTRACT

**Primary Outputs**:
- `[DORES DO PÚBLICO]` block - Pain points extracted from reviews/complaints
- `[GANHOS DESEJADOS]` block - Desired gains from positive reviews
- `[OBJEÇÕES E RESPOSTAS]` block - Common objections + suggested responses

**Structure**:
```yaml
pain_points:
  - pain: string
    frequency: number (mentions count)
    severity: low | medium | high | critical
    source: [Reclame Aqui | Trustpilot | etc]

desired_gains:
  - gain: string
    frequency: number
    importance: low | medium | high
    current_satisfaction: percentage

objections:
  - objection: string
    frequency: number
    suggested_response: string
    proof_needed: string[]
```

**Export Variables**:
```yaml
sentiment_score: "Overall sentiment (-1.0 to 1.0)"
top_pain_point: "Most mentioned pain point"
top_desired_gain: "Most desired benefit"
critical_objections_count: "Number of critical objections"
```

## 🎯 TASK

**Role**: Customer Sentiment Intelligence Specialist

**Objective**: Analyze reviews, complaints, and social mentions to extract authentic customer pain points, desired gains, and objections. Prioritize Reclame Aqui (mandatory) + 3 additional sources for triangulation.

**Standards**:
- Minimum 4 sources (Reclame Aqui + 3 others)
- Minimum 20 pain points extracted
- Minimum 15 desired gains extracted
- Minimum 10 objections identified
- All data points with source + frequency

**Constraints**:
- Max execution time: 12 minutes
- Reclame Aqui is MANDATORY (risk analysis)
- Sentiment must be scored (-1.0 to 1.0)
- No editorial bias (extract raw customer voice)

## Objetivo

Extrair insights autênticos de clientes através de análise de reviews, reclamações e menções sociais para alimentar decisões de copy, produto e atendimento.

## Entradas

- `$product_name` ou `$head_terms`
- `$competitors` (análise comparativa de sentiment)
- Opcional: `$brand` (sentiment específico da marca)

## Processo

### 1. Coleta MANDATÓRIA - Reclame Aqui ⭐

**URL Base**: `https://www.reclameaqui.com.br/busca/?q={query}`

**Por que MANDATÓRIO**:
- Maior base de reclamações BR (15M+ reclamações)
- Dados estruturados (categorias, status, reputação)
- Crítico para risk analysis

**Dados a Extrair**:

**1.1 Reputation Score**:
```
Brand/Product: {name}
Reputação: {score}/10
Categoria de Reputação: {ÓTIMO|BOM|REGULAR|RUIM|PÉSSIMO}
```

**1.2 Complaint Categories**:
```
Top 5 Categorias de Reclamação:
1. {categoria_1}: {percentage}% ({count} reclamações)
2. {categoria_2}: {percentage}%
3. {categoria_3}: {percentage}%
...

Exemplos:
- "Produto com defeito" (35%)
- "Entrega atrasada" (28%)
- "Propaganda enganosa" (15%)
```

**1.3 Resolution Metrics**:
```
Taxa de Resposta: {percentage}%
Taxa de Solução: {percentage}%
Tempo Médio de Resposta: {days} dias
```

**1.4 Pain Points Extraction**:
Ler últimas 20-30 reclamações e extrair:
```yaml
- pain: "Produto chegou com {defeito específico}"
  frequency: 12 (de 30 reclamações lidas)
  severity: high
  category: "qualidade_produto"

- pain: "Bateria dura menos que o anunciado ({X}h vs {Y}h prometidas)"
  frequency: 8
  severity: medium
  category: "propaganda_enganosa"
```

**Registro**:
```
Fonte: Reclame Aqui
Data: {timestamp}
URL: {url}
Marca/Produto: {name}
Reputação: {score}/10 ({categoria})
Reclamações analisadas: 30
Pain Points extraídos: {count}
Severidade crítica: {count} pontos
```

### 2. Coleta - Trustpilot Brasil

**URL Base**: `https://br.trustpilot.com/search?query={brand_or_product}`

**Dados a Extrair**:

**2.1 Rating Distribution**:
```
Rating Geral: {X}/5.0 ({total} reviews)
Distribuição:
- 5⭐: {percentage}% ({count})
- 4⭐: {percentage}%
- 3⭐: {percentage}%
- 2⭐: {percentage}%
- 1⭐: {percentage}% ← FOCAR AQUI para pain points
```

**2.2 Positive Aspects (de 4-5⭐ reviews)**:
```yaml
desired_gains:
  - gain: "{aspecto positivo mencionado}"
    frequency: {count} menções
    quotes: ["{exemplo de review}", "{outro exemplo}"]
    importance: high (se >15% mencionam)
```

**2.3 Negative Aspects (de 1-2⭐ reviews)**:
```yaml
pain_points:
  - pain: "{problema mencionado}"
    frequency: {count}
    severity: high (se em reviews 1⭐)
```

**Registro**:
```
Fonte: Trustpilot BR
Rating: {X}/5.0
Reviews analisados: {count}
Aspectos positivos: {count} (de 4-5⭐)
Aspectos negativos: {count} (de 1-2⭐)
```

### 3. Coleta - Google Maps (Reviews Locais)

**URL Base**: `https://www.google.com/maps/search/{store_name}+{location}`

**Dados a Extrair**:

**3.1 Local Store Reviews**:
```
Loja: {store_name} - {location}
Rating: {X}/5.0 ({total} reviews)
```

**3.2 Q&A Section**:
- Perguntas frequentes = Objeções não respondidas
- Dúvidas = Gaps de informação

**Exemplo**:
```yaml
objections:
  - objection: "Tem garantia? Quanto tempo?"
    frequency: 5 perguntas similares
    suggested_response: "Garantia de {X} meses contra defeitos de fabricação (certificado {Y})"
    proof_needed: ["certificado de garantia", "política de trocas"]
```

**3.3 Customer Photos**:
- Photos de produtos em uso real
- Identificar contextos não mencionados em copy oficial

**Registro**:
```
Fonte: Google Maps
Lojas analisadas: {count}
Reviews lidos: {count}
Perguntas Q&A: {count}
Photos de clientes: {count}
```

### 4. Coleta - Reddit Brasil

**Subreddits Relevantes**:
```
r/brasil (geral)
r/ConselhosLegais (reclamações)
r/investimentos (produtos financeiros)
r/gamesEcultura (tech/gaming)
```

**URL Pattern**: `https://www.reddit.com/r/{subreddit}/search/?q={product_name}`

**Dados a Extrair**:

**4.1 Sentiment da Comunidade**:
```
Threads encontrados: {count}
Upvote ratio médio: {percentage}%
Sentiment: {positive|neutral|negative} (baseado em upvotes)
```

**4.2 Unanswered Questions**:
- Perguntas com muitos upvotes mas poucas respostas = Gaps de info
- "Vale a pena {produto}?" (142 upvotes, 3 respostas)

**4.3 Comparison Threads**:
- "{Produto A} vs {Produto B}" threads
- Extrair critérios de decisão mencionados

**Exemplo**:
```yaml
decision_criteria:
  - criterion: "Durabilidade a longo prazo"
    importance: high (mencionado em 80% dos comparison threads)
    current_market_perception: "Produtos importados duram menos"

objections:
  - objection: "Produtos chineses quebram rápido"
    frequency: 15 mentions
    suggested_response: "Certificação {X}, garantia estendida {Y}, materiais {Z}"
    proof_needed: ["certificação", "warranty policy", "material specs"]
```

**Registro**:
```
Fonte: Reddit Brasil
Subreddits: {list}
Threads analisados: {count}
Perguntas não respondidas: {count}
Comparison criteria: {count}
```

### 5. Coleta - Fóruns Especializados

**Fontes**:
- Adrenaline (tech): `https://forum.adrenaline.com.br/search/1/?q={product}`
- Hardware BR: `https://www.hardware.com.br/forum/`
- Mães de Plantão (baby/kids): `https://www.maesdeplantao.com.br/forum/`

**Dados a Extrair**:

**5.1 Long-term Usage Experiences**:
- Reviews após 6 meses, 1 ano de uso
- Problemas que aparecem com tempo

**Exemplo**:
```yaml
pain_points:
  - pain: "Bateria perde capacidade após 6 meses de uso diário"
    frequency: 4 mentions (em tópicos long-term review)
    severity: high
    source: "Adrenaline Forum"
    timeframe: "após 6 meses"
```

**5.2 Technical Doubts**:
- Dúvidas técnicas = Objeções complexas
- Mitos/misconceptions = Educational opportunities

**Registro**:
```
Fonte: Fóruns Especializados
Fóruns consultados: {count}
Tópicos analisados: {count}
Long-term reviews: {count}
Dúvidas técnicas: {count}
```

### 6. Consolidação e Análise

**6.1 Frequency Analysis**:
Agrupar pain points/gains similares e contar frequência total:

```python
pain_points_consolidated = group_similar(pain_points_all_sources)
sort_by_frequency_desc(pain_points_consolidated)

# Top 3 dores:
# 1. "Bateria dura menos que anunciado" (45 menções, 5 fontes)
# 2. "Produto chegou com defeito" (32 menções, 4 fontes)
# 3. "Difícil de conectar com alguns dispositivos" (28 menções, 3 fontes)
```

**6.2 Severity Scoring**:
```python
severity_score = (
    frequency * 0.4 +  # 40% peso
    (1 if in_reclameaqui else 0) * 0.3 +  # 30% peso (Reclame Aqui = crítico)
    source_count / 5 * 0.3  # 30% peso (múltiplas fontes = confiável)
)

if severity_score >= 0.8: severity = "critical"
elif severity_score >= 0.6: severity = "high"
elif severity_score >= 0.4: severity = "medium"
else: severity = "low"
```

**6.3 Sentiment Scoring**:
```python
sentiment_score = (
    positive_mentions - negative_mentions
) / total_mentions

# Range: -1.0 (100% negativo) a +1.0 (100% positivo)
# Exemplo: 120 positivos, 80 negativos, 200 total
# Sentiment = (120-80)/200 = 0.20 (levemente positivo)
```

## Output

### Bloco [DORES DO PÚBLICO]

```markdown
## Dores Identificadas (por Frequência)

**Fontes**: Reclame Aqui ⭐, Trustpilot BR, Google Maps, Reddit Brasil, Fóruns (Adrenaline)
**Total de Menções Analisadas**: {count}
**Data**: {timestamp}

### Dores Críticas (Severity: CRITICAL)
1. **{pain_1}**
   - Frequência: {count} menções ({sources_count} fontes)
   - Severidade: CRITICAL
   - Fontes: {source_list}
   - Contexto: {contexto adicional}
   - Impacto: {alto|médio|baixo} na decisão de compra

2. **{pain_2}**
   - Frequência: {count} menções
   - Severidade: CRITICAL
   ...

### Dores Altas (Severity: HIGH)
3. **{pain_3}** ({count} menções, {sources_count} fontes)
4. **{pain_4}** ...

### Dores Médias (Severity: MEDIUM)
...

### Padrões Identificados
- **Categoria dominante**: {categoria} ({percentage}% das dores)
- **Timing**: {quando a dor aparece - ex: "após 6 meses de uso"}
- **Segmento afetado**: {qual público reclama mais}
```

### Bloco [GANHOS DESEJADOS]

```markdown
## Benefícios Desejados (por Importância)

**Fontes**: Trustpilot (5⭐ reviews), Google Maps, Reddit, Fóruns
**Reviews Positivos Analisados**: {count}

### Ganhos Críticos (High Importance)
1. **{desired_gain_1}**
   - Importância: HIGH (mencionado por {percentage}%)
   - Satisfação Atual no Mercado: {percentage}% satisfeitos
   - Gap de Mercado: {high|medium|low}
   - Quotes:
     - "{exemplo de review positivo}"
     - "{outro exemplo}"

2. **{desired_gain_2}**
   ...

### Ganhos Secundários (Medium Importance)
3. **{desired_gain_3}** ({percentage}% mencionam)
...

### Oportunidades Não Atendidas
- **{gap_1}**: Mencionado como desejado mas <30% satisfeitos
  - Ação: {como explorar esse gap}
```

### Bloco [OBJEÇÕES E RESPOSTAS]

```markdown
## Objeções Comuns + Respostas Sugeridas

**Fontes**: Q&A (Google Maps), Reddit, Fóruns, Reclame Aqui
**Objeções Identificadas**: {count}

### Objeções Críticas (>10 menções)
1. **"{objection_1}"**
   - Frequência: {count} menções ({sources_count} fontes)
   - Categoria: {preço|qualidade|entrega|suporte|etc}
   - Resposta Sugerida:
     > "{resposta persuasiva baseada em dados}"
   - Provas Necessárias:
     - {proof_1} (ex: certificação)
     - {proof_2} (ex: política de garantia)
     - {proof_3} (ex: depoimentos)

2. **"{objection_2}"**
   ...

### Objeções Médias (5-10 menções)
3. **"{objection_3}"**
   - Resposta Sugerida: ...
...

### Mitos/Misconceptions Identificados
- **Mito**: "{crença incorreta comum}"
  - Realidade: "{correção factual}"
  - Educar via: {copy|FAQ|vídeo|etc}
```

## ✅ VALIDATION (Quality Gates)

**Step Validation Criteria**:
```yaml
min_sources_consulted: 4
min_reclameaqui_included: true (MANDATORY)
min_pain_points: 20
min_desired_gains: 15
min_objections: 10
min_total_mentions_analyzed: 100
```

**Quality Checks**:
- ✅ Reclame Aqui incluído (mandatory)
- ✅ Pelo menos 4 fontes consultadas
- ✅ Pain points categorizados por severity
- ✅ Desired gains ranqueados por importance
- ✅ Objeções com respostas sugeridas + provas
- ✅ Sentiment score calculado (-1.0 a +1.0)

**Confidence Calculation**:
```python
confidence = (
    (sources_consulted / 5) * 0.25 +  # 25% weight
    (pain_points_count / 20) * 0.25 +  # 25% weight
    (1 if reclameaqui_included else 0) * 0.3 +  # 30% weight (crítico)
    (mentions_analyzed / 100) * 0.2  # 20% weight
)
# Target: ≥ 0.75
```

## 🔗 CONTEXT (Usage & Integration)

**Usage Patterns**:
- Execute após web_search_outbound (Step 8 in comprehensive_research)
- Pode rodar em paralelo com price_comparison (Step 7)
- Alimenta decisões de copy em anuncio_agent

**Upstream Dependencies**:
- Step 1: intake_validation ($validated_brief, $head_terms)
- Step 6: competitor_analysis ($competitors)
- config/accessible_urls.md (sentiment sources)

**Downstream Consumers**:
- anuncio_agent (usa pain points para ad copy)
- [OBJEÇÕES E RESPOSTAS] → FAQ creation
- [DORES] + [GANHOS] → Value proposition design

**Data Flow**:
```
$competitors + $head_terms → [SENTIMENT_ANALYSIS] →
$pain_points + $desired_gains + $objections →
[DORES] + [GANHOS] + [OBJEÇÕES] blocks
```

**Assumptions**:
- Product has public reviews/complaints (≥50 mentions)
- Reclame Aqui has data for category or competitors
- Sentiment represents authentic customer voice (not fake reviews)

---

**Status**: ✅ Módulo v1.1 Production-Ready
**Dependencies**: accessible_urls.md (Sentiment Sources section)
**Created**: 2025-11-14
**Version**: 1.1.0
