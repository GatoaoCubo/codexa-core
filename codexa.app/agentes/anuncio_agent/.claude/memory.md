# anuncio_agent Memory Context

## Agent Identity
- **Agent**: anuncio_agent
- **Domain**: E-commerce ad generation (Mercado Livre, Shopee, Amazon BR)
- **Output**: Copy + keywords + image prompts (Trinity format)

## Quality Standards
- Titles: 58-60 chars, ZERO connectors (de, para, com, e)
- Keywords: 25 main + 25 secondary, no duplicates
- Bullets: 5 bullets, 250-299 chars each, PNL triggers
- Description: 3300+ chars, StoryBrand structure

## Compliance Rules
- ANVISA: No therapeutic claims without registration
- INMETRO: No safety claims without certification
- Marketplace: No "#1", "best", "only" without proof

## Workflow Pattern
1. Load product_brief.json
2. Run STEP_COPY_FULL (5 phases)
3. Validate with quality gates (score >= 0.85)
4. Output Trinity format (.md + .llm.json + .meta.json)

## Key Commands
- `/prime-anuncio` - Load full context
- `/anuncio-copy` - Generate copy
- `/anuncio-validate` - Run validators

## Human Review Checklist
Before publishing any generated copy:
- [ ] ANVISA/INMETRO compliance verified
- [ ] Character limits within spec
- [ ] No prohibited claims
- [ ] Brand voice consistent
