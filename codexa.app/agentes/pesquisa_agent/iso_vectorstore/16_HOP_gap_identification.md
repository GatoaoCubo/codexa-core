# HOP 16: GAP IDENTIFICATION | pesquisa_agent v3.0.0

**Purpose**: Identify market gaps, unanswered questions, neglected keywords
**Scope**: RESEARCH | **Output**: gaps + opportunities + seo_taxonomy

---

## INPUT

- `{$head_terms}` - Primary keywords from HOP 13
- `{$competitor_data}` - Analysis from HOP 15
- `{$sentiment_data}` - Pain points from HOP 19

---

## RULES

1. Search Google "People Also Ask" for unanswered questions
2. Identify keywords competitors are NOT targeting
3. Find features mentioned in reviews but not in listings
4. Cluster keywords into semantic groups
5. Separate inbound (marketplace) vs outbound (SERP) keywords

---

## STEPS

1. **Search PAA**: "People Also Ask" for each head term
2. **Analyze competitor gaps**: Features missing from top listings
3. **Review gap analysis**: Pain points without solutions
4. **Keyword clustering**: Group by intent and topic
5. **SEO taxonomy**: Categorize inbound vs outbound

---

## OUTPUT FORMAT

```markdown
## GAPS COMPETITIVOS

### Perguntas Nao Respondidas
- {pergunta_1}?
- {pergunta_2}?

### Keywords Negligenciadas
- {keyword_1}: {oportunidade}
- {keyword_2}: {oportunidade}

### Features Desejadas (nao oferecidas)
- {feature_1}: mencionada em {N} reviews
- {feature_2}: mencionada em {N} reviews

## TAXONOMIA DE CATEGORIAS

### Categoria Principal
{categoria} > {subcategoria} > {tipo}

### Categorias Alternativas
- {alt_1}
- {alt_2}

## SEO INBOUND (Marketplaces)
- {keyword_marketplace_1}
- {keyword_marketplace_2}

## SEO OUTBOUND (SERP/Social)
- {keyword_serp_1}
- {keyword_serp_2}
```

---

## VALIDATION

- [ ] PAA questions extracted
- [ ] Competitor gaps identified
- [ ] Keywords clustered
- [ ] Taxonomy defined
- [ ] Inbound/outbound separated

---

**HOP**: 16 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~600 (optimized)
