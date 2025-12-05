# MANIFEST | shared_knowledge v1.1.0

**Package**: shared_knowledge (cross-agent knowledge base)
**Version**: 1.1.0 | **Date**: 2025-12-05
**Scope**: Reusable knowledge cards for multiple agents
**Files**: 10 | **Total Tokens**: ~20,000

---

## PURPOSE

Central repository of knowledge that applies across multiple agents. Avoids duplication by consolidating shared concepts, frameworks, and guidelines in one location.

**Philosophy**: Write once, reference everywhere.

---

## DEPLOY CHECKLIST

```
[ ] Review knowledge cards for completeness
[ ] Verify cross-references in consuming agents
[ ] Test retrieval via Scout MCP
[ ] Update agent PRIME.md files to reference shared knowledge
```

---

## FILE INVENTORY (10 Files)

### Root (00) ~400 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Package index |

### COPYWRITING_FRAMEWORKS/ ~7,600 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Category index |
| 01 | persuasion_patterns.md | ~2,000 | Mental triggers (escassez, urgencia, prova social) |
| 02 | storytelling_frameworks.md | ~2,200 | StoryBrand, Hero's Journey, AIDA, PAS |
| 03 | marketplace_copy_rules.md | ~1,800 | ML, Shopee, Amazon copy guidelines |
| 04 | brand_voice_template.md | ~1,200 | Template for consistent brand voice |

### AI_PLATFORMS/ ~12,000 tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~500 | Category index |
| 01 | platform_comparison.md | ~3,500 | Image/Video/Audio platform matrix |
| 02 | prompt_engineering.md | ~3,000 | Universal prompting patterns |
| 03 | api_integration.md | ~2,500 | Common API patterns (auth, rate limits) |
| 04 | quality_assessment.md | ~2,500 | How to evaluate AI outputs |

---

## CATEGORY INDEX

### COPYWRITING_FRAMEWORKS/

Knowledge cards for persuasive writing in Brazilian e-commerce context.

**Consuming Agents**:
- anuncio_agent: Marketplace copy generation
- marca_agent: Brand messaging consistency
- curso_agent: Sales copy and landing pages
- photo_agent: Image caption alignment
- video_agent: Script persuasion elements

**Usage Pattern**:
```
1. Load relevant card via Scout
2. Apply framework to specific context
3. Validate output against guidelines
```

### AI_PLATFORMS/

Knowledge cards for AI generation platforms (image, video, audio).

**Consuming Agents**:
- photo_agent: Image generation (Midjourney, DALL-E, Imagen)
- video_agent: Video generation (Runway, Pika, Veo, Sora, Kling, Hailuo)
- voice_agent: Audio/TTS (ElevenLabs, Edge TTS, Whisper)
- qa_agent: Quality assessment

**Usage Pattern**:
```
1. Select platform using comparison matrix
2. Apply prompt engineering patterns
3. Integrate via API patterns
4. Validate with quality assessment
```

---

## KNOWLEDGE CARD STRUCTURE

Each card follows this template:

```markdown
# [Topic] | shared_knowledge

**Purpose**: [Single sentence]
**Version**: X.X.X | **Updated**: YYYY-MM-DD
**Quality Score**: X.XX/1.00

---

## OVERVIEW
[What and why]

## FRAMEWORKS
[Core content with examples]

## BRAZILIAN CONTEXT
[Local adaptations]

## USAGE EXAMPLES
[Practical applications]

## INTEGRATION
[How agents use this]
```

---

## QUALITY STANDARDS

| Metric | Threshold |
|--------|-----------|
| Completeness | >= 0.75 |
| Brazilian relevance | >= 0.80 |
| Practical examples | >= 5 per card |
| Agent applicability | >= 3 agents |

---

## FUTURE CATEGORIES (Planned)

```
shared_knowledge/
├── COPYWRITING_FRAMEWORKS/     [ACTIVE]
├── AI_PLATFORMS/               [ACTIVE]
├── SEO_GUIDELINES/             [PLANNED]
├── COMPLIANCE_RULES/           [PLANNED]
├── MARKETPLACE_SPECS/          [PLANNED]
└── VISUAL_STANDARDS/           [PLANNED]
```

---

## CROSS-REFERENCES

| Document | Purpose |
|----------|---------|
| [COPYWRITING_FRAMEWORKS/00_MANIFEST.md](COPYWRITING_FRAMEWORKS/00_MANIFEST.md) | Copywriting category index |
| [AI_PLATFORMS/00_MANIFEST.md](AI_PLATFORMS/00_MANIFEST.md) | AI platforms category index |
| [docs/PLACEHOLDERS.md](../docs/PLACEHOLDERS.md) | Distillation placeholders |

---

**Package**: shared_knowledge v1.1.0
**Status**: ACTIVE
**Tokens**: ~20,000
**Date**: 2025-12-05
