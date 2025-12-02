# HOP 19: SENTIMENT ANALYSIS | pesquisa_agent v3.0.0

**Purpose**: Extract pain points, gains, objections from reviews/complaints
**Scope**: RESEARCH | **Output**: customer_insights + sentiment_data

---

## INPUT

- `{$head_terms}` - Primary keywords from HOP 13
- `{$competitor_data}` - Competitor URLs from HOP 15
- `{$category}` - Product category

---

## RULES

1. Reclame Aqui search is MANDATORY
2. Analyze YouTube reviews and comments
3. Check TikTok and Instagram for sentiment
4. Extract specific pain points with frequency
5. Identify objections and counter-arguments

### REQUIRED SOURCES
- **Reclame Aqui**: Complaints, resolution rate, company score
- **YouTube**: Product reviews, unboxing, tutorials
- **Social**: TikTok, Instagram trends and comments

---

## STEPS

1. **Search Reclame Aqui**: Brand/category complaints
2. **Analyze YouTube**: Reviews, comments sentiment
3. **Check social**: TikTok, Instagram product mentions
4. **Extract pain points**: Recurring complaints
5. **Identify gains**: Desired benefits from reviews
6. **Map objections**: Purchase barriers + responses

---

## OUTPUT FORMAT

```markdown
## DORES DO PUBLICO
1. {dor_1} - mencionada {N}x
2. {dor_2} - mencionada {N}x
3. {dor_3} - mencionada {N}x

## GANHOS DESEJADOS
1. {ganho_1} - mencionado {N}x
2. {ganho_2} - mencionado {N}x
3. {ganho_3} - mencionado {N}x

## OBJECOES E RESPOSTAS
| Objecao | Frequencia | Resposta |
|---------|------------|----------|
| {objecao_1} | {N}x | {resposta_1} |
| {objecao_2} | {N}x | {resposta_2} |

## RECLAME AQUI
- Empresa: {nome}
- Score: {X.X}/10
- Taxa resolucao: {X}%
- Principais queixas: {lista}

## OPORTUNIDADES ACIONAVEIS
- {oportunidade_1}
- {oportunidade_2}

## RESUMO EXECUTIVO
{3-5 frases resumindo insights principais}
```

---

## VALIDATION

- [ ] Reclame Aqui searched
- [ ] 5+ pain points identified
- [ ] 5+ desired gains listed
- [ ] Objections mapped with responses
- [ ] Executive summary written

---

**HOP**: 19 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~700 (optimized)
