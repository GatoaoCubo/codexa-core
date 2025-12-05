# MANIFEST | COPYWRITING_FRAMEWORKS v1.0.0

**Package**: COPYWRITING_FRAMEWORKS (shared_knowledge subcategory)
**Version**: 1.0.0 | **Date**: 2025-12-05
**Scope**: Persuasive writing frameworks for Brazilian e-commerce
**Files**: 5 | **Total Tokens**: ~7,600

---

## PURPOSE

Consolidated copywriting knowledge for all agents that produce text content. Focuses on Brazilian e-commerce context with marketplace-specific guidelines.

**Target Marketplaces**: Mercado Livre, Shopee, Amazon BR, Magalu

---

## FILE INVENTORY (5 Files)

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Category index |
| 01 | persuasion_patterns.md | ~2,000 | Mental triggers for conversion |
| 02 | storytelling_frameworks.md | ~2,200 | Narrative structures (AIDA, PAS, StoryBrand) |
| 03 | marketplace_copy_rules.md | ~1,800 | Platform-specific guidelines |
| 04 | brand_voice_template.md | ~1,200 | Voice consistency template |

---

## KNOWLEDGE CARDS

### 01_persuasion_patterns.md

**Content**: Mental triggers that drive purchase decisions
- Escassez (scarcity)
- Urgencia (urgency)
- Prova social (social proof)
- Autoridade (authority)
- Reciprocidade (reciprocity)
- Compromisso (commitment)

**Primary Users**: anuncio_agent, curso_agent

### 02_storytelling_frameworks.md

**Content**: Narrative structures for compelling copy
- AIDA (Attention, Interest, Desire, Action)
- PAS (Problem, Agitation, Solution)
- StoryBrand (7-step framework)
- Hero's Journey (adapted for commerce)
- BAB (Before, After, Bridge)

**Primary Users**: marca_agent, curso_agent, video_agent

### 03_marketplace_copy_rules.md

**Content**: Platform-specific requirements
- Mercado Livre: Character limits, forbidden words
- Shopee: Title structure, keyword density
- Amazon BR: A+ content guidelines
- Magalu: Integration requirements

**Primary Users**: anuncio_agent

### 04_brand_voice_template.md

**Content**: Template for defining brand voice
- Tone attributes
- Vocabulary guidelines
- Do/Don't examples
- Archetype alignment

**Primary Users**: marca_agent, anuncio_agent

---

## CONSUMING AGENTS

| Agent | Primary Cards | Usage |
|-------|---------------|-------|
| anuncio_agent | 01, 03 | Marketplace listings |
| marca_agent | 02, 04 | Brand strategy |
| curso_agent | 01, 02 | Sales copy, landing pages |
| photo_agent | 01, 04 | Caption alignment |
| video_agent | 01, 02 | Script persuasion |

---

## INTEGRATION PATTERN

```markdown
## In Agent PRIME.md

### Shared Knowledge References

- [persuasion_patterns](../../shared_knowledge/COPYWRITING_FRAMEWORKS/01_persuasion_patterns.md)
- [storytelling_frameworks](../../shared_knowledge/COPYWRITING_FRAMEWORKS/02_storytelling_frameworks.md)
```

---

## QUALITY METRICS

| Card | Quality Score | Brazilian Relevance |
|------|---------------|---------------------|
| 01_persuasion_patterns | 0.85 | 0.90 |
| 02_storytelling_frameworks | 0.82 | 0.85 |
| 03_marketplace_copy_rules | 0.88 | 0.95 |
| 04_brand_voice_template | 0.80 | 0.85 |

**Category Average**: 0.84/1.00

---

## USAGE VIA SCOUT

```python
# Discover relevant cards
mcp__scout__discover(query="copywriting persuasion triggers")

# Get category context
mcp__scout__smart_context(agent="shared_knowledge")
```

---

**Package**: COPYWRITING_FRAMEWORKS v1.0.0
**Status**: ACTIVE
**Quality**: 0.84/1.00
**Date**: 2025-12-05
