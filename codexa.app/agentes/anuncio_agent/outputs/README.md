# Outputs | anuncio_agent

**Purpose**: Generated marketplace listings, titles, descriptions, and optimization artifacts

## Directory Structure

```
outputs/
├── README.md
├── listings/                # Complete listing packages (title + description + bullets)
├── titles/                  # Title variations and A/B test options
├── descriptions/            # Full descriptions with formatting
├── bullets/                 # Bullet points and key features
├── seo_keywords/            # Backend keywords and search terms
├── variations/              # Listing variations by platform
└── consolidated/            # Final consolidated listings ready for upload
```

## Trinity Output Format

All outputs generate 3 files:
- **.md** - Human-readable listing content
- **.llm.json** - Structured data for LLM consumption/iteration
- **.meta.json** - Metadata (version, timestamp, quality_score, platform)

## Naming Convention

```
{produto}_{plataforma}_{tipo}_{versao}.{ext}

Examples:
- caneca_gatinha_ml_listing_v1.md
- caneca_gatinha_amazon_titles_v2.md
- caneca_gatinha_shopee_bullets_v1.llm.json
```

## Platform Codes

| Platform | Code |
|----------|------|
| Mercado Livre | `ml` |
| Amazon BR | `amazon` |
| Shopee | `shopee` |
| Magazine Luiza | `magalu` |
| Americanas | `americanas` |
| Generic/All | `generic` |

## Example Output

```
outputs/listings/
├── caneca_gatinha_ml_listing_v1.md
├── caneca_gatinha_ml_listing_v1.llm.json
└── caneca_gatinha_ml_listing_v1.meta.json

outputs/titles/
├── caneca_gatinha_ml_titles_v1.md        # 10 title variations
├── caneca_gatinha_amazon_titles_v1.md
└── caneca_gatinha_shopee_titles_v1.md
```

## Meta.json Schema

```json
{
  "version": "1.0.0",
  "created_at": "2025-11-30T10:00:00Z",
  "product": "caneca_gatinha",
  "platform": "mercadolivre",
  "output_type": "listing",
  "quality_score": 0.92,
  "seo_score": 0.88,
  "character_counts": {
    "title": 58,
    "description": 1847,
    "bullets": 5
  },
  "open_variables_used": ["[PRODUTO]", "[MARCA]", "[BENEFICIO_PRINCIPAL]"],
  "source_research": "pesquisa_agent/outputs/market_analysis/caneca_gatinha_v1.llm.json"
}
```

## Integration

**Inputs from:**
- **pesquisa_agent** - Market research, keywords, competitor analysis
- **marca_agent** - Brand voice, tone, messaging

**Outputs to:**
- **photo_agent** - Product context for image prompts
- Marketplace upload tools

## Gitignore

```
outputs/**/*.md
outputs/**/*.json
!outputs/README.md
```
