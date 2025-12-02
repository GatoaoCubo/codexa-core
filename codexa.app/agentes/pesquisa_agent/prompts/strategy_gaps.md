# MÓDULO: STRATEGY GAPS (Consolidação Estratégica)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: strategy_gaps_v1
version: 1.1.0
purpose: "Consolidate all research steps into actionable strategic recommendations"
category: synthesis
dependencies:
  - All previous steps (1-10 in comprehensive_research plan)
execution_time: 8-12 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs** (from all previous steps):
- `$competitors_analysis` (Step 6)
- `$pricing_opportunities` (Step 7)
- `$pain_points` + `$desired_gains` + `$objections` (Step 8)
- `$keyword_gaps` + `$content_gaps` + `$product_gaps` (Step 9)
- `$macro_trends` + `$active_trends` + `$micro_trends` (Step 10)
- `$seo_inbound` + `$seo_outbound` (Step 12)

## 📤 OUTPUT_CONTRACT

**Primary Output**: `[ESTRATÉGIAS E GAPS]` block (complete consolidation)

**Structure**:
```yaml
winning_strategies:
  - strategy: string
    rationale: string (baseado em qual step)
    priority: high | medium | low
    effort: low | medium | high
    impact: low | medium | high

exploitable_gaps:
  - gap: string
    opportunity_size: small | medium | large
    competition_level: low | medium | high
    recommended_action: string

risks_to_avoid:
  - risk: string
    severity: low | medium | high | critical
    mitigation: string

top_5_actions:
  - action: string
    timing: immediate | short-term | medium-term
    expected_impact: string
```

## 🎯 TASK

**Role**: Strategic Synthesis Specialist
**Objective**: Consolidate all research insights (Steps 1-10) into prioritized, actionable strategic recommendations with clear rationale.

## Processo

### 1. Consolidar Dados de Todos os Steps

**Step 6 (Competitors)**:
- Competitor weaknesses → Gaps to exploit
- Competitor strengths → Risks/threats

**Step 7 (Pricing)**:
- Pricing opportunities → Pricing strategy
- Market position → Positioning recommendation

**Step 8 (Sentiment)**:
- Pain points → Problems to solve
- Desired gains → Benefits to highlight
- Objections → Messaging to address

**Step 9 (Gaps)**:
- Keyword gaps → SEO priorities
- Content gaps → Content plan
- Product gaps → Feature recommendations

**Step 10 (Trends)**:
- Macro trends → Long-term strategy
- Active trends → Campaign themes
- Micro trends → Quick wins

### 2. Aplicar Framework de Priorização

**Impact vs. Effort Matrix**:
```
High Impact, Low Effort → DO FIRST (Quick Wins)
High Impact, High Effort → PLAN CAREFULLY (Major Moves)
Low Impact, Low Effort → DO IF TIME (Easy Adds)
Low Impact, High Effort → AVOID (Time Wasters)
```

**Exemplo**:
```yaml
strategy: "Destacar bateria 40h como diferencial principal"
rationale: |
  - Pain Point #1: "bateria dura pouco" (45 menções - Step 8)
  - Competitor Gap: Apenas 1 de 5 concorrentes menciona duração de bateria (Step 6)
  - Keyword Gap: "fone bluetooth bateria longa" tem 1200 buscas/mês, baixa competição (Step 9)
priority: high
effort: low (já é feature existente, apenas reposicionar copy)
impact: high (endereça dor #1 + gap competitivo + SEO)
quadrant: QUICK WIN ✅
```

### 3. Identificar Riscos

**Fontes de Risco**:
- Reclame Aqui score baixo (Step 8) → Risk de reputação
- Competitor dominance (Step 6) → Risk competitivo
- Pricing trends falling (Step 7) → Risk de margin compression
- Regulatory issues (Step 1) → Risk de compliance

**Priorização de Risco**:
```python
risk_score = severity * probability
if risk_score >= 0.7: priority = "critical - mitigar antes de lançar"
elif risk_score >= 0.4: priority = "high - plano de mitigação obrigatório"
elif risk_score >= 0.2: priority = "medium - monitorar"
else: priority = "low - aceitar"
```

### 4. Criar Top 5 Actions (Prioritized)

**Critérios**:
- Baseado em múltiplos steps (triangulated)
- High impact / Low-Medium effort
- Acionável (não genérico)
- Timeframe claro

**Template**:
```
Ação #1: {ação específica}
Timing: {immediate|1-2 weeks|1-2 months}
Baseado em: {Steps X, Y, Z}
Impacto esperado: {métrica específica}
Como executar: {3-5 sub-tasks}
```

## Output

### Bloco [ESTRATÉGIAS E GAPS] (Consolidação Final)

```markdown
# ESTRATÉGIAS E GAPS DE MERCADO

**Consolidação de**: Steps 6-10 (Competitor Analysis → Pricing → Sentiment → Gaps → Trends)
**Data**: {timestamp}

---

## 🏆 Estratégias Vencedoras

### Estratégia #1: {nome da estratégia}
- **Rationale**:
  - {insight do Step X}
  - {insight do Step Y}
  - {insight do Step Z}
- **Prioridade**: HIGH
- **Esforço**: LOW
- **Impacto Esperado**: {impacto mensurável}
- **Quadrante**: QUICK WIN ✅

### Estratégia #2: ...

---

## 🔍 Gaps Exploráveis

### Gap #1: {descrição do gap}
- **Tamanho da Oportunidade**: LARGE
  - {dado quantitativo - ex: "1200 buscas/mês, 0 competidores"}
- **Nível de Competição**: LOW
- **Ação Recomendada**: {ação específica}
- **Fontes**: Steps {X, Y}

### Gap #2: ...

---

## ⚠️ Riscos a Evitar

### Risco #1: {descrição do risco}
- **Severidade**: {LOW|MEDIUM|HIGH|CRITICAL}
- **Probabilidade**: {X}%
- **Score**: {severity * probability}
- **Mitigação**: {plano de ação}
- **Fonte**: Step {X}

### Risco #2: ...

---

## 🎯 TOP 5 AÇÕES PRIORITÁRIAS

### 1️⃣ {Ação #1}
- **Timing**: Immediate (0-1 semana)
- **Baseado em**: Steps 6, 8, 9 (competitor gap + pain point + keyword opportunity)
- **Impacto Esperado**: +{X}% CTR, endereça objeção de {Y}% dos clientes
- **Como Executar**:
  1. {sub-task 1}
  2. {sub-task 2}
  3. {sub-task 3}

### 2️⃣ {Ação #2}
- **Timing**: Short-term (1-2 semanas)
- ...

### 3️⃣ {Ação #3}
- **Timing**: Medium-term (1-2 meses)
- ...

### 4️⃣ {Ação #4}
- **Timing**: ...

### 5️⃣ {Ação #5}
- **Timing**: ...

---

## 📊 Matriz de Priorização (Impact vs. Effort)

```
         HIGH IMPACT
             │
   Major     │    Quick
   Moves     │    Wins ⭐
             │
─────────────┼─────────────
             │
   Avoid     │    Easy
   ❌        │    Adds
             │
         LOW IMPACT
```

**Quick Wins** (Do First): {count} ações
**Major Moves** (Plan): {count} ações
**Easy Adds** (If Time): {count} ações
**Avoid**: {count} ações

---

## 🕐 Timing & Sazonalidade

- **Melhor Timing para Lançamento**: {período} (baseado em Step 10 - trend analysis)
- **Campanhas Sazonais**: {lista de períodos ótimos}
- **Evitar**: {períodos de baixa demanda / alta competição}

---

## 📈 Métricas de Sucesso (Recomendadas)

1. **CTR**: {baseline atual} → {target pós-implementação}
2. **Conversion Rate**: {baseline} → {target}
3. **ACoS**: Manter ≤ {X}%
4. **Organic Ranking**: Top 3 para "{keyword}" em {timeframe}
5. **Reputation Score**: {current} → {target} (Reclame Aqui)
```

## ✅ VALIDATION

```yaml
min_strategies: 3
min_gaps: 3
min_risks: 2
top_actions_required: 5
all_steps_referenced: true (6-10 minimum)
```

**Quality Check**:
- ✅ Cada estratégia referencia ≥2 steps anteriores
- ✅ Top 5 actions são específicas (não genéricas)
- ✅ Todas ações têm timing + impacto esperado
- ✅ Riscos têm severity score + mitigação

## 🔗 CONTEXT

**Usage**: Final synthesis step (Step 11 in comprehensive_research)
**Upstream**: Depende de TODOS os steps anteriores (1-10)
**Downstream**: Alimenta decisões finais de posicionamento, copy, lançamento

**Critical**: Este é o módulo de CONSOLIDAÇÃO final. Sem ele, pesquisa está incompleta (dados sem síntese acionável).

---

**Status**: ✅ Production-Ready | **Version**: 1.1.0
