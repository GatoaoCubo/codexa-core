# FONTES - Marketplace Copywriting Knowledge Base

**Version**: 1.0.0 | **Agent**: anuncio_agent | **Purpose**: Curated copywriting knowledge for Brazilian marketplaces

---

## Overview

Este diretorio contem conhecimento especializado para copywriting de e-commerce no Brasil. Complementa os arquivos de configuracao (`config/`) com profundidade e exemplos praticos.

---

## Structure

```
FONTES/
├── 00_MANIFEST.md              # Este arquivo (indice)
├── MARKETPLACES/
│   ├── mercadolivre.md         # ML copy best practices
│   ├── shopee.md               # Shopee copy patterns
│   ├── amazon_br.md            # Amazon BR requirements
│   └── magalu.md               # Magazine Luiza specs
├── COPYWRITING/
│   ├── titulos.md              # Title optimization
│   ├── descricoes.md           # Description frameworks
│   └── bullets.md              # Bullet point patterns
└── COMPLIANCE/
    └── termos_proibidos.md     # Prohibited terms (ANVISA, INMETRO)
```

---

## Usage

### For LLM Execution
```
1. Load FONTES/00_MANIFEST.md (this file)
2. Load marketplace-specific file based on target
3. Apply COPYWRITING/ patterns
4. Validate against COMPLIANCE/termos_proibidos.md
```

### Integration with config/
| FONTES/ (Knowledge) | config/ (Rules) |
|---------------------|-----------------|
| Best practices, examples | Technical limits |
| Patterns, frameworks | Regex validation |
| Writing guidelines | Score thresholds |
| Mental triggers | Compliance rules |

---

## File Index

### MARKETPLACES/

| File | Content | Use When |
|------|---------|----------|
| `mercadolivre.md` | ML SEO, ranqueamento, copy patterns | Target: ML listings |
| `shopee.md` | Mobile-first, flash sales, engagement | Target: Shopee |
| `amazon_br.md` | A+ Content, Style Guide, backend keywords | Target: Amazon |
| `magalu.md` | EAN requirements, ficha tecnica | Target: Magalu |

### COPYWRITING/

| File | Content | Use When |
|------|---------|----------|
| `titulos.md` | Title formulas, keyword density, zero-connector | Generating titles |
| `descricoes.md` | StoryBrand, long-form, emotional triggers | Building descriptions |
| `bullets.md` | Benefit-focused, mental triggers, 250-299 chars | Creating bullet points |

### COMPLIANCE/

| File | Content | Use When |
|------|---------|----------|
| `termos_proibidos.md` | ANVISA, INMETRO, CONAR restrictions | Validation phase |

---

## Quick Reference

### Character Limits (by Marketplace)

| Element | ML | Shopee | Amazon | Magalu |
|---------|-----|--------|--------|--------|
| Title | 60 | 120 | 200 | 256 |
| Description | 50,000 | 3,000 | 2,000 | 4,000 |
| Bullets | N/A | N/A | 500/each | N/A |
| Images | 12 | 9 | 9 | 20 |

### Priority Reading Order

1. **New to agent**: `00_MANIFEST.md` > `mercadolivre.md` > `titulos.md`
2. **Compliance focus**: `termos_proibidos.md` first
3. **Specific marketplace**: Load that marketplace file + `titulos.md` + `descricoes.md`

---

## Maintenance

- **Update frequency**: Monthly or when marketplace policies change
- **Owner**: anuncio_agent maintainer
- **Last updated**: 2025-12-05
- **Sync with**: `config/marketplace_specs.json`, `config/copy_rules.json`

---

**Status**: Production Ready | **Language**: Portuguese BR
