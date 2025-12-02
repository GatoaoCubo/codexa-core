# HOP 17: IMAGE ANALYSIS | pesquisa_agent v3.0.0

**Purpose**: Analyze product images and visual trends + compliance check
**Scope**: RESEARCH | **Output**: visual_insights + compliance_risks

---

## INPUT

- `{$image_urls}` - Product images from brief (optional)
- `{$competitor_images}` - Screenshots from HOP 15
- `{$category}` - Product category for compliance

---

## RULES

1. Requires vision capability (skip if unavailable)
2. Analyze product presentation, context, quality
3. Check ANVISA, INMETRO, CONAR compliance for category
4. Identify visual trends from competitors
5. Flag prohibited claims or imagery

### COMPLIANCE CHECKS
- **ANVISA**: Health claims, before/after, medical imagery
- **INMETRO**: Safety certifications, age restrictions
- **CONAR**: Misleading claims, comparative advertising

---

## STEPS

1. **Analyze product images**: Quality, context, presentation
2. **Extract visual trends**: From competitor screenshots
3. **Check compliance**: Category-specific rules
4. **Flag risks**: Prohibited claims, missing certifications
5. **Generate recommendations**: Visual improvements

---

## OUTPUT FORMAT

```markdown
## ANALISE DE IMAGENS

### Qualidade Visual
- Resolucao: {adequada/inadequada}
- Fundo: {branco/lifestyle/contextual}
- Iluminacao: {profissional/amadora}

### Tendencias Visuais (Concorrentes)
- {tendencia_1}
- {tendencia_2}

## RISCOS E ALERTAS

### Compliance
- ANVISA: {status} - {detalhes}
- INMETRO: {status} - {detalhes}
- CONAR: {status} - {detalhes}

### Alertas
- {alerta_1}
- {alerta_2}

## REGRAS CRITICAS DE MARKETPLACE
- {regra_1}
- {regra_2}
```

---

## VALIDATION

- [ ] Images analyzed (if vision available)
- [ ] Compliance checked
- [ ] Risks flagged
- [ ] Marketplace rules documented

---

**HOP**: 17 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~600 (optimized)
