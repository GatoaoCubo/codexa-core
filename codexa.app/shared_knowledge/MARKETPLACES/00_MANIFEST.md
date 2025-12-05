# MARKETPLACES - Knowledge Category Manifest

**Version**: 1.0.0
**Updated**: 2025-12-05
**Domain**: Brazilian E-commerce Marketplaces
**Type**: Shared Knowledge (Cross-Agent)

---

## CATEGORY OVERVIEW

This knowledge category consolidates Brazilian marketplace intelligence for use across multiple agents. Contains platform specifications, regulatory requirements, SEO patterns, and comparative data.

### Purpose

Enable agents to generate marketplace-compliant content by providing:
- Platform-specific technical constraints
- Brazilian regulatory framework (ANVISA, INMETRO, CONAR, CDC)
- SEO optimization patterns per marketplace
- Comparative data for multi-platform strategies

---

## FILE INDEX

| File | Purpose | Priority |
|------|---------|----------|
| `01_marketplace_matrix.md` | Platform comparison (ML vs Shopee vs Amazon vs Magalu) | HIGH |
| `02_regulatory_framework.md` | Brazilian compliance (ANVISA, INMETRO, CONAR, CDC) | CRITICAL |
| `03_platform_specs.md` | Character limits, image specs, technical requirements | HIGH |
| `04_seo_optimization.md` | Marketplace-specific SEO patterns | MEDIUM |

---

## AGENT CROSS-REFERENCES

### Primary Consumers

| Agent | Usage Pattern |
|-------|--------------|
| `anuncio_agent` | Title generation, description building, compliance validation |
| `pesquisa_agent` | Competitive analysis, market positioning, keyword research |
| `marca_agent` | Brand consistency, platform adaptation, compliance strategy |

### Integration Points

```
pesquisa_agent (research)
    |
    v
[MARKETPLACES knowledge]
    |
    v
anuncio_agent (content creation)
    |
    v
marca_agent (brand validation)
```

---

## USAGE GUIDELINES

### When to Load

1. **Title Generation**: Load `03_platform_specs.md` for character limits
2. **Compliance Check**: Load `02_regulatory_framework.md` for category requirements
3. **Multi-Platform Strategy**: Load `01_marketplace_matrix.md` for comparison
4. **SEO Optimization**: Load `04_seo_optimization.md` for ranking factors

### Loading Priority

```
CRITICAL: 02_regulatory_framework.md (always check compliance first)
HIGH:     01_marketplace_matrix.md + 03_platform_specs.md
MEDIUM:   04_seo_optimization.md
```

---

## MAINTENANCE

### Update Frequency

- `01_marketplace_matrix.md`: Quarterly (platform policies change)
- `02_regulatory_framework.md`: As regulations change (monitor ANVISA, INMETRO)
- `03_platform_specs.md`: Monthly (technical specs evolve)
- `04_seo_optimization.md`: Bi-monthly (algorithm updates)

### Data Sources

- Official marketplace documentation
- Seller Central / Partner Center portals
- Brazilian regulatory agencies (ANVISA, INMETRO, CONAR)
- Industry reports and seller communities

---

## METADATA

```json
{
  "category": "MARKETPLACES",
  "version": "1.0.0",
  "files": 4,
  "primary_language": "pt-BR",
  "geographic_focus": "Brazil",
  "agents_served": ["anuncio_agent", "pesquisa_agent", "marca_agent"],
  "last_validated": "2025-12-05"
}
```

---

**Status**: Active
**Maintainer**: codexa_agent
