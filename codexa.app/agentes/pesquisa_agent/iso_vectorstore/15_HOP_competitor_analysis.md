# HOP 15: COMPETITOR ANALYSIS | pesquisa_agent v3.0.0

**Purpose**: Deep dive into top 3-5 competitors with quantitative benchmark
**Scope**: RESEARCH | **Output**: competitor_profiles + benchmark_table

---

## INPUT

- `{$query_bank}` - Head terms and longtails from HOP 13
- `{$marketplace_data}` - Raw data from marketplace searches
- `{$brief}` - Product brief with declared competitors

---

## RULES

1. Analyze minimum 3 competitors (target 5)
2. All prices in BRL format (R$ X,XX)
3. All ratings as X.X/5.0
4. Log source URL for each competitor
5. Include quantitative AND qualitative analysis

### INCLUDE COMPETITOR IF
- Top 10 in marketplace for head term
- Mentioned in 3+ reviews/comparisons
- Declared in brief
- 50+ reviews on major marketplace
- Similar positioning (category, price, audience)

### EXCLUDE COMPETITOR IF
- Product discontinued/unavailable
- No verifiable digital presence
- Very different category
- Price outlier (>5x or <20% of average)

---

## STEPS

1. **Identify competitors**: From marketplace searches + brief
2. **Collect per competitor**:
   - Name, brand, model
   - Price (current, was, discount %)
   - Rating (X.X/5.0) + review count
   - Top 3 strengths (with proof)
   - Top 3 weaknesses (with proof)
   - Differentiators
3. **Build benchmark table**: Aggregate metrics
4. **Identify gaps**: Underserved features, weak messaging

---

## OUTPUT FORMAT

```markdown
## ANALISE DE CONCORRENTES

### Concorrente 1: {nome}
- **Preco**: R$ {X} (era R$ {Y}, -{Z}%)
- **Avaliacao**: {X.X}/5.0 ({N} reviews)
- **Forcas**: {força_1}, {força_2}, {força_3}
- **Fraquezas**: {fraqueza_1}, {fraqueza_2}
- **Diferencial**: {diferencial}
- **Fonte**: {URL}

[Repeat for 3-5 competitors]

## BENCHMARK AGREGADO
| Metrica | Min | Media | Max |
|---------|-----|-------|-----|
| Preco | R$ {X} | R$ {Y} | R$ {Z} |
| Avaliacao | {X.X} | {Y.Y} | {Z.Z} |
| Reviews | {N} | {M} | {P} |

## GAPS COMPETITIVOS
- {gap_1}: {oportunidade}
- {gap_2}: {oportunidade}

## DIFERENCIAIS COMPETITIVOS
- {diferencial_1}
- {diferencial_2}
```

---

## VALIDATION

- [ ] 3-5 competitors analyzed
- [ ] All prices in BRL
- [ ] All ratings with review count
- [ ] Source URLs logged
- [ ] Benchmark table complete
- [ ] Gaps identified

---

**HOP**: 15 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~900 (optimized from 17,000)
