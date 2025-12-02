# HOP 20: QA VALIDATION | pesquisa_agent v3.0.0

**Purpose**: Validate research_notes.md completeness and quality
**Scope**: RESEARCH | **Output**: validation_status + confidence_score

---

## INPUT

- `{research_notes}` - Draft research_notes.md content
- `{queries_log}` - Web queries executed
- `{competitors_data}` - Competitor analysis results

---

## RULES

1. All 22 blocks must be present
2. Minimum 3 competitors analyzed with quantitative data
3. Minimum 15 web queries logged with URLs
4. Maximum 10% [SUGESTAO] placeholders
5. All prices in BRL format
6. All ratings in X.X/5.0 format

### REQUIRED BLOCKS
- HEAD TERMS PRIORITARIOS
- LONGTAILS
- SEO INBOUND
- SEO OUTBOUND
- ANALISE DE CONCORRENTES
- BENCHMARK AGREGADO
- DORES DO PUBLICO
- GANHOS DESEJADOS
- OBJECOES E RESPOSTAS
- RISCOS E ALERTAS
- OPORTUNIDADES ACIONAVEIS
- RESUMO EXECUTIVO

---

## STEPS

1. **Count blocks**: Verify all 22 blocks present
2. **Validate competitors**: Check >= 3 with prices, ratings, reviews
3. **Audit queries**: Verify >= 15 logged with source + URL
4. **Check placeholders**: Calculate [SUGESTAO] ratio
5. **Validate formats**: BRL prices, ratings, dates
6. **Calculate confidence**: (checks_passed / total_checks) * quality_factor

---

## OUTPUT FORMAT

```markdown
## VALIDACAO DA PESQUISA

**Status**: PASS / PASS_WITH_WARNINGS / FAIL

### Metricas
| Metrica | Target | Atual | Status |
|---------|--------|-------|--------|
| Blocos presentes | 22 | {n} | OK/FAIL |
| Concorrentes | >= 3 | {n} | OK/FAIL |
| Queries logadas | >= 15 | {n} | OK/FAIL |
| Placeholders | <= 10% | {n}% | OK/FAIL |

### Confidence Score
**Score**: {0.XX} / 1.0

### Recomendacoes
- {item_1}
- {item_2}
```

---

## VALIDATION

- [ ] All 22 blocks checked
- [ ] Competitor count verified
- [ ] Query log audited
- [ ] Placeholder ratio calculated
- [ ] Confidence score generated

---

**HOP**: 20 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~600 (optimized)
