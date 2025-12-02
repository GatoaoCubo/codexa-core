# Outputs | pesquisa_agent

**Purpose**: Market research results, competitor analysis, and strategic insights

## Directory Structure

```
outputs/
├── README.md
├── market_analysis/         # Market size, trends, opportunities
├── competitor_intel/        # Competitor analysis and positioning
├── keyword_research/        # SEO keywords, search volume data
├── pricing_strategy/        # Price analysis and recommendations
├── audience_insights/       # Target audience profiles
├── platform_reports/        # Marketplace-specific insights (ML, Amazon, Shopee)
└── consolidated/            # Final consolidated reports
```

## Trinity Output Format

All outputs generate 3 files:
- **.md** - Human-readable report
- **.llm.json** - Structured data for LLM consumption
- **.meta.json** - Metadata (version, timestamp, sources, confidence_score)

## Naming Convention

```
{produto}_{tipo}_{versao}.{ext}

Examples:
- caneca_gatinha_market_analysis_v1.md
- caneca_gatinha_market_analysis_v1.llm.json
- caneca_gatinha_market_analysis_v1.meta.json
```

## Example Output

```
outputs/market_analysis/
├── caneca_gatinha_market_analysis_v1.md
├── caneca_gatinha_market_analysis_v1.llm.json
└── caneca_gatinha_market_analysis_v1.meta.json

outputs/competitor_intel/
├── caneca_gatinha_competitors_v1.md
├── caneca_gatinha_competitors_v1.llm.json
└── caneca_gatinha_competitors_v1.meta.json
```

## Meta.json Schema

```json
{
  "version": "1.0.0",
  "created_at": "2025-11-30T10:00:00Z",
  "product": "caneca_gatinha",
  "output_type": "market_analysis",
  "sources": ["mercadolivre", "amazon", "shopee"],
  "confidence_score": 0.85,
  "data_freshness_days": 7,
  "open_variables_used": ["[PRODUTO]", "[NICHO]"]
}
```

## Integration

These outputs feed into:
- **marca_agent** - Brand strategy development
- **anuncio_agent** - Listing optimization
- **photo_agent** - Visual strategy

## Gitignore

```
outputs/**/*.md
outputs/**/*.json
!outputs/README.md
```
