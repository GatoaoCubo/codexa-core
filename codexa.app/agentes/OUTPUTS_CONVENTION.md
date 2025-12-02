# CODEXA Outputs Convention

**Version**: 1.0.0
**Last Updated**: 2025-11-30

## Overview

This document defines the standard output structure for all CODEXA agents. Following this convention ensures:
- Consistency across agents
- Easy navigation for humans and LLMs
- Scalable structure for future products
- Clean data flow between agents

---

## Trinity Output Format

All CODEXA outputs use the **Trinity Format** - 3 files per output:

| Extension | Purpose | Consumer |
|-----------|---------|----------|
| `.md` | Human-readable content | Humans, documentation |
| `.llm.json` | Structured data | LLMs, agent pipelines |
| `.meta.json` | Metadata & provenance | Tracking, validation |

### Example

```
caneca_gatinha_market_analysis_v1.md       # Human reads this
caneca_gatinha_market_analysis_v1.llm.json # LLM consumes this
caneca_gatinha_market_analysis_v1.meta.json # System tracks this
```

---

## Naming Convention

```
{produto}_{tipo}_{versao}.{ext}
```

| Component | Description | Examples |
|-----------|-------------|----------|
| `produto` | Product/brand slug | `caneca_gatinha`, `codexa`, `nanobanana` |
| `tipo` | Output type | `market_analysis`, `listing`, `prompts` |
| `versao` | Version number | `v1`, `v2`, `v3` |
| `ext` | File extension | `md`, `llm.json`, `meta.json` |

### Platform-Specific Outputs

For marketplace-specific content:
```
{produto}_{plataforma}_{tipo}_{versao}.{ext}
```

Platform codes: `ml`, `amazon`, `shopee`, `magalu`, `americanas`, `generic`

---

## Agent Output Directories

### pesquisa_agent
```
outputs/
├── market_analysis/      # Market size, trends
├── competitor_intel/     # Competitor analysis
├── keyword_research/     # SEO keywords
├── pricing_strategy/     # Price recommendations
├── audience_insights/    # Target audience
├── platform_reports/     # Marketplace insights
└── consolidated/         # Final reports
```

### marca_agent
```
outputs/
├── brand_strategy/       # Full strategy docs
├── brand_voice/          # Voice & tone
├── visual_identity/      # Colors, typography
├── naming/               # Names, taglines
├── positioning/          # Market positioning
├── validation_reports/   # Consistency reports
└── consolidated/         # Brand books
```

### anuncio_agent
```
outputs/
├── listings/             # Complete listings
├── titles/               # Title variations
├── descriptions/         # Full descriptions
├── bullets/              # Key features
├── seo_keywords/         # Backend keywords
├── variations/           # Platform variations
└── consolidated/         # Upload-ready
```

### photo_agent
```
outputs/
├── prompts/              # AI image prompts
├── shot_lists/           # Photography briefs
├── mood_boards/          # Visual references
├── composition_guides/   # Framing specs
├── lighting_specs/       # Lighting setups
├── style_guides/         # Visual guidelines
├── generated_images/     # AI images
└── consolidated/         # Final packages
```

### curso_agent
```
outputs/
├── video_scripts/        # Video content
├── workbooks/            # Exercises
├── hands_on/             # Practical exercises
├── cheat_sheets/         # Quick references
├── sales/                # Landing pages
├── visuals/              # Diagrams
├── extras/               # FAQs, guides
└── hotmart_package/      # Platform packages
```

### codexa_agent
```
outputs/
├── reviews/              # Code reviews
├── reports/              # Analysis reports
├── integrations/         # Integration specs
└── consolidated/         # Final artifacts
```

---

## Meta.json Standard Schema

```json
{
  "version": "1.0.0",
  "created_at": "2025-11-30T10:00:00Z",
  "updated_at": "2025-11-30T10:00:00Z",
  "agent": "pesquisa_agent",
  "product": "caneca_gatinha",
  "output_type": "market_analysis",
  "quality_score": 0.85,
  "confidence_score": 0.90,
  "sources": [],
  "open_variables_used": [],
  "dependencies": {
    "inputs": [],
    "outputs_to": []
  }
}
```

---

## Data Flow Between Agents

```
┌─────────────────┐
│ pesquisa_agent  │
│    (Research)   │
└────────┬────────┘
         │ market_analysis.llm.json
         │ competitor_intel.llm.json
         ▼
┌─────────────────┐
│  marca_agent    │
│   (Branding)    │
└────────┬────────┘
         │ brand_strategy.llm.json
         │ brand_voice.llm.json
         ▼
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│anuncio│ │ photo │
│ agent │ │ agent │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
   [Marketplace Ready]
```

---

## Git Strategy

Add to `.gitignore`:
```gitignore
# Outputs (regeneratable)
**/outputs/**/*.md
**/outputs/**/*.json
**/outputs/**/*.png
**/outputs/**/*.jpg

# Keep READMEs
!**/outputs/README.md
```

### When to Commit Outputs

- **Never commit**: Generated content (listings, prompts, images)
- **Commit**: README.md files, example outputs for documentation
- **Optional**: Consolidated "golden" outputs as reference

---

## Scalability

### Per-Product Organization (Future)

For multiple products, consider:
```
outputs/
├── README.md
└── {produto}/
    ├── v1/
    │   ├── market_analysis.md
    │   └── market_analysis.meta.json
    └── latest/ → symlink to current version
```

### Batch Processing

For bulk operations:
```
outputs/
└── batches/
    └── 2025-11-30_batch_001/
        ├── manifest.json
        └── products/
            ├── produto_1/
            └── produto_2/
```

---

## Quick Reference

| Agent | Primary Output | Key Consumers |
|-------|---------------|---------------|
| pesquisa | `market_analysis.llm.json` | marca, anuncio |
| marca | `brand_strategy.llm.json` | anuncio, photo |
| anuncio | `listing.llm.json` | marketplaces |
| photo | `prompts.llm.json` | image APIs |
| curso | `video_scripts.md` | video production |

---

**Author**: CODEXA System
**For questions**: See individual agent `outputs/README.md` files
