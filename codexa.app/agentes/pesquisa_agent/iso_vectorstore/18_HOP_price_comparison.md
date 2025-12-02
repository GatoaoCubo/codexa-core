# HOP 18: PRICE COMPARISON | pesquisa_agent v3.0.0

**Purpose**: Collect and analyze pricing data across BR marketplaces
**Scope**: RESEARCH | **Output**: price_intelligence + opportunities

---

## INPUT

- `{$head_terms}` - Primary keywords from HOP 13
- `{$competitor_data}` - Competitor prices from HOP 15
- `{$marketplaces}` - Target marketplaces (default: all 9 BR)

---

## RULES

1. All prices in BRL format (R$ X,XX)
2. Include current price, "was" price, discount %
3. Track shipping costs (free shipping indicator)
4. Note promotional badges (Black Friday, etc.)
5. Calculate price positioning (premium/mid/budget)

### MARKETPLACES (9 BR)
- Mercado Livre, Shopee, Magazine Luiza, Amazon BR
- Americanas, Casas Bahia, Submarino, TikTok Shop, Shein

---

## STEPS

1. **Collect prices**: Search each marketplace for head terms
2. **Extract data**: Current, was, discount, shipping
3. **Calculate ranges**: Min, avg, max per marketplace
4. **Identify positioning**: Premium, mid-market, budget
5. **Find opportunities**: Price gaps, promotional windows

---

## OUTPUT FORMAT

```markdown
## COMPARACAO DE PRECOS

### Por Marketplace
| Marketplace | Min | Media | Max | Frete Gratis |
|-------------|-----|-------|-----|--------------|
| Mercado Livre | R$ {X} | R$ {Y} | R$ {Z} | {%} |
| Shopee | R$ {X} | R$ {Y} | R$ {Z} | {%} |
| Amazon BR | R$ {X} | R$ {Y} | R$ {Z} | {%} |

### Posicionamento Recomendado
- **Premium** (>R$ {X}): {justificativa}
- **Mid-market** (R$ {X}-{Y}): {justificativa}
- **Budget** (<R$ {X}): {justificativa}

### Oportunidades de Preco
- {oportunidade_1}
- {oportunidade_2}

## ARGUMENTOS DE VENDA
- {argumento_1}
- {argumento_2}

## GATILHOS MENTAIS
- Escassez: {exemplo}
- Prova social: {exemplo}
- Urgencia: {exemplo}
```

---

## VALIDATION

- [ ] 3+ marketplaces covered
- [ ] All prices in BRL
- [ ] Ranges calculated
- [ ] Positioning defined
- [ ] Opportunities identified

---

**HOP**: 18 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~700 (optimized)
