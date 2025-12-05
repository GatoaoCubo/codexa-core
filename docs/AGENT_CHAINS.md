# AGENT_CHAINS Reference

**Version**: 1.0.0
**Updated**: 2025-12-03
**Purpose**: Document agent connections, data flow, and bridge patterns

---

## Overview

CODEXA has 12 agents organized in interconnected chains. This document maps how outputs from one agent become inputs for another.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AGENT ECOSYSTEM                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   BRAND HUB                    CONTENT CHAIN                                │
│   ┌─────────┐                  ┌─────────┐                                  │
│   │  marca  │─────────────────▶│ anuncio │──────┐                          │
│   └────┬────┘                  └────┬────┘      │                          │
│        │                            │           ▼                          │
│        │   RESEARCH                 │      ┌─────────┐                     │
│        │   ┌──────────┐             │      │  photo  │                     │
│        │   │ pesquisa │─────────────┘      └─────────┘                     │
│        │   └──────────┘                                                     │
│        │                                                                    │
│        │   EDUCATION CHAIN                                                  │
│        │   ┌─────────┐      ┌─────────┐      ┌─────────┐                   │
│        └──▶│  curso  │─────▶│  video  │─────▶│  voice  │                   │
│            └─────────┘      └─────────┘      └─────────┘                   │
│                                                                             │
│   INFRASTRUCTURE                                                            │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐                                    │
│   │ codexa  │  │  scout  │  │ mentor  │                                    │
│   └─────────┘  └─────────┘  └─────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Directory

| # | Agent | Domain | Trigger | Primary Output |
|---|-------|--------|---------|----------------|
| 1 | marca_agent | Brand identity | `/marca` | metadata.json, brand guide |
| 2 | pesquisa_agent | Market research | `/pesquisa` | competitor analysis, trends |
| 3 | anuncio_agent | Product listings | `/anuncio` | optimized copy, bullets |
| 4 | photo_agent | Visual prompts | `/photo` | Midjourney/DALL-E prompts |
| 5 | video_agent | Video production | `/video` | scripts, storyboards |
| 6 | curso_agent | Course creation | `/curso` | outlines, modules, timelines |
| 7 | voice_agent | Audio/speech | `/voice` | voice scripts, audio |
| 8 | mentor_agent | Guidance | `/mentor` | recommendations |
| 9 | codexa_agent | Meta-construction | `/codexa-*` | agents, workflows, prompts |
| 10 | scout_agent | File discovery | `mcp__scout__*` | file paths, context |
| 11 | qa_agent | Quality assurance | `/qa` | validation reports |
| 12 | persona_agent | Brand chatbot | `/persona` | themed responses |

---

## Chain 1: Research → Content

```
pesquisa_agent ──────▶ anuncio_agent
     │                      │
     │ OUTPUT:              │ INPUT:
     │ - Competitor data    │ - Market positioning
     │ - Price analysis     │ - Keyword targets
     │ - Trend insights     │ - Competitive angles
     │                      │
     ▼                      ▼
USER_DOCS/Pesquisa/     user_anuncios/*.md
```

### Data Bridge Pattern

```markdown
## From pesquisa_agent output:
keywords_principais: ["arranhador gato", "brinquedo gato"]
faixa_preco_mercado: "R$ 89-199"
diferenciais_competitivos: ["design moderno", "sustentavel"]

## To anuncio_agent input:
Use keywords in title/bullets
Position price within market range
Highlight differentiators in description
```

### Bridge Trigger

```bash
# After pesquisa completes, anuncio can consume:
/anuncio --context=USER_DOCS/Pesquisa/[product]_analysis.md
```

---

## Chain 2: Content → Visual

```
anuncio_agent ──────▶ photo_agent
     │                      │
     │ OUTPUT:              │ INPUT:
     │ - Product benefits   │ - Scene descriptions
     │ - Key features       │ - Mood/style
     │ - Target emotions    │ - Color palette
     │                      │
     ▼                      ▼
user_anuncios/*.md      photo prompts
```

### Data Bridge Pattern

```markdown
## From anuncio_agent output:
TITULO: "Arranhador Gato Modular Premium"
BENEFICIO_1: "Montagem sem ferramentas"
BENEFICIO_2: "Material sustentavel"
EMOCAO_ALVO: "orgulho, praticidade"

## To photo_agent input:
SCENE: Cat scratching modern modular tower
MOOD: Premium, clean, sustainable
HERO_SHOT: Easy assembly demonstration
LIFESTYLE: Happy cat owner, organized space
```

### Bridge Trigger

```bash
# After anuncio completes, photo can consume:
/photo --product-copy=user_anuncios/[product].md
```

---

## Chain 3: Education → Production

```
curso_agent ──────▶ video_agent ──────▶ voice_agent
     │                   │                   │
     │ OUTPUT:           │ OUTPUT:           │ OUTPUT:
     │ - Module outline  │ - Video script    │ - Audio script
     │ - TIMELINE_MASTER │ - Storyboard      │ - Voice files
     │ - Learning goals  │ - B-roll list     │ - Timing marks
     │                   │                   │
     ▼                   ▼                   ▼
outputs/TIMELINE_*   outputs/VIDEO_*   outputs/VOICE_*
```

### Data Bridge Pattern

```markdown
## From curso_agent TIMELINE_MASTER:
SEC_0_30: Hook - "O que voce vai aprender"
SEC_30_120: Problema - "Por que isso importa"
SEC_120_300: Solucao - "Como funciona"

## To video_agent:
SCENE_1: Hook (0:00-0:30) - Dramatic opening
SCENE_2: Problem (0:30-2:00) - Pain points
SCENE_3: Solution (2:00-5:00) - Demo

## To voice_agent:
VOICE_SEGMENT_1: "Voce ja sentiu..." (Hook)
VOICE_SEGMENT_2: "O maior problema..." (Problem)
```

### Bridge Trigger

```bash
# Sequential chain:
/curso-outline --product=X
/video --timeline=outputs/TIMELINE_MASTER.md
/voice --script=outputs/VIDEO_SCRIPT.md
```

---

## Chain 4: Brand Hub → All

```
                    marca_agent
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    anuncio_agent  photo_agent    curso_agent
          │              │              │
          └──────────────┼──────────────┘
                         │
              {{BRAND_*}} placeholders
```

### Data Bridge Pattern

```json
// USER_DOCS/Marca/metadata.json
{
  "BRAND_NAME": "CODEXA",
  "BRAND_URL": "codexa.app",
  "PRIMARY_COLOR": "#0D9488",
  "TAGLINE": "Build the builder",
  "TARGET_AUDIENCE": "e-commerce sellers"
}
```

### Hydration Flow

```
1. marca_agent creates metadata.json
2. Other agents read {{PLACEHOLDERS}}
3. /flow distill creates templates
4. Hydration fills brand-specific values
```

---

## Orchestration Mechanisms

### Existing ADWs

| ADW | Purpose | Location |
|-----|---------|----------|
| 203_ADW_PARALLEL | Multi-agent parallel | codexa_agent/workflows/ |
| 204_ADW_INTEGRATED | Product reform batch | codexa_agent/workflows/ |
| 100_ADW_CODEXA_ORCHESTRATION | Global orchestration | codexa.app/workflows/ |

### Using /spawn for Chains

```bash
# Research + Content in parallel
/spawn
1. explore: find pesquisa outputs for [product]
2. review: validate pesquisa data quality
3. build: generate anuncio from pesquisa data

# Full content chain
/spawn
1. build: run pesquisa_agent for [product]
2. build: run anuncio_agent with pesquisa output
3. build: run photo_agent with anuncio output
```

---

## Chain Validation Gates

Between each chain step, validate quality:

| Gate | Threshold | Check |
|------|-----------|-------|
| pesquisa→anuncio | ≥7.0/10 | Data completeness |
| anuncio→photo | ≥7.0/10 | Copy quality |
| curso→video | ≥7.0/10 | Timeline coverage |

### Validation Pattern

```markdown
## Quality Gate Check

### Input Validation
- [ ] Required fields present
- [ ] Data format correct
- [ ] No placeholder artifacts

### Output Validation
- [ ] Quality score ≥7.0/10
- [ ] All sections complete
- [ ] Ready for next chain
```

---

## Handoff Protocol

Use `/handoff` between chain steps:

```handoff
contexto: Completed pesquisa for [product]
arquivos_gerados:
  - USER_DOCS/Pesquisa/[product]_analysis.md
proximo: Run anuncio_agent with research data
dados:
  - keywords: [list]
  - price_range: [range]
  - differentiators: [list]
qualidade: 8.5/10
```

---

## Quick Reference

### Start a Chain

```bash
# Research chain
/pesquisa "produto X"
/handoff
# → anuncio receives context

# Education chain
/curso-outline scope=1-3
/handoff
# → video receives timeline
```

### Parallel Chains

```bash
/spawn
1. build: pesquisa for product A
2. build: pesquisa for product B
3. build: pesquisa for product C
# → All research in parallel
```

### Full Pipeline

```bash
/flow auto "criar conteudo completo para produto X"
# → plan → pesquisa → anuncio → photo → distill
```

---

## See Also

- [WORKFLOWS.md](./WORKFLOWS.md) - ADW catalog
- [PLACEHOLDERS.md](./PLACEHOLDERS.md) - Template variables
- [CLAUDE.md](../CLAUDE.md) - Project laws

---

**Version**: 1.0.0
**Created**: 2025-12-03
**Type**: Agent Chain Reference
