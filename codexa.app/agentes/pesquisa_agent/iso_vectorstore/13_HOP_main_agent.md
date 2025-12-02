# HOP 13: MAIN AGENT | pesquisa_agent v3.0.0

**Purpose**: Parse brief, generate query bank, orchestrate research flow
**Scope**: RESEARCH | **Output**: query_bank + orchestration decisions

---

## INPUT

- `{$brief}` - Product brief (text or JSON)
- `{$capabilities}` - LLM capabilities detected
- `{$plan}` - Execution plan (default: standard_research)

---

## RULES

1. Web search capability is REQUIRED - abort if not available
2. Generate 10-15 head terms (1-3 words, high intent)
3. Derive 30-50 longtails (head + attribute/benefit)
4. Map synonyms and regional BR variations
5. Log ALL web queries with: date, source, URL, insight

### FAZER
- Prioritize BR Portuguese terms
- Include marketplace-specific syntax (ML, Shopee, Amazon)
- Add price modifiers (barato, promocao, oferta)
- Include benefit terms (melhor, top, profissional)

### EVITAR
- English-only terms without PT-BR translation
- Generic terms without intent signal
- Duplicate variations

---

## STEPS

1. **Parse brief**: Extract product, category, audience, price
2. **Validate required fields**: Abort if missing product or category
3. **Generate head terms**: Core product keywords (10-15)
4. **Expand longtails**: Head + modifiers (30-50)
5. **Map synonyms**: Regional variations, colloquialisms
6. **Create query lists**: Inbound (marketplaces) + Outbound (SERP)
7. **Set execution plan**: Based on brief completeness

---

## OUTPUT FORMAT

```markdown
## HEAD TERMS PRIORITARIOS
1. {term_1}
2. {term_2}
...

## LONGTAILS
- {head_term} + {modifier_1}
- {head_term} + {modifier_2}
...

## SINONIMOS E VARIACOES
| Term | Variations |
|------|------------|
| {term} | {var_1}, {var_2} |

## QUERY BANK
- Inbound: [{queries for marketplaces}]
- Outbound: [{queries for SERP/social}]
```

---

## VALIDATION

- [ ] 10-15 head terms generated
- [ ] 30-50 longtails derived
- [ ] Synonyms mapped
- [ ] Query bank created
- [ ] Execution plan selected

---

**HOP**: 13 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~800 (optimized from 8,000)
