# 300_ADW_KNOWLEDGE_HYDRATION | Sistema Unificado de Hidratacao de Conhecimento

**Version**: 1.0.0 | **Created**: 2025-12-05
**Type**: ADW Workflow (Multi-Agent Hydration System)
**Estimated Time**: 2-4 hours (full pipeline) | 15-30min (single agent)
**Complexity**: High (orchestrates 10 agents)

---

## MODULE_METADATA

```yaml
id: 300_ADW_KNOWLEDGE_HYDRATION
version: 1.0.0
purpose: Sistema unificado para hidratar todos os agentes CODEXA com conhecimento de dominio
category: meta-construction
type: ADW (Agentic Developer Workflow)
execution_mode: parallel_multi_agent
reference_implementation: mentor_agent/FONTES/PROMPT_ENGINEERING/
status: production_ready
created: 2025-12-05

target_agents:
  - anuncio_agent      # Marketplace copy
  - codexa_agent       # Meta-construction
  - curso_agent        # Education/courses
  - marca_agent        # Brand strategy
  - mentor_agent       # E-commerce mentoring (reference)
  - pesquisa_agent     # Market research
  - photo_agent        # Visual prompting
  - video_agent        # Video production
  - voice_agent        # Audio/speech (CRITICAL GAP)
  - scout_agent        # File discovery (CRITICAL GAP)

excluded_agents:
  - ronronalda_agent   # Being reworked
  - qa_gato3_agent     # Being reworked
```

---

## ARCHITECTURE

### Three-Layer Knowledge System

```
LAYER 1: OPERATIONAL (iso_vectorstore/)
  Purpose: "How the agent executes"
  Contents: HOPs, ADWs, configs, schemas
  Optimization: ADW-104 (iso_vectorstore optimization)

LAYER 2: DOMAIN (FONTES/)                    <-- THIS ADW
  Purpose: "What the agent KNOWS about its domain"
  Contents: Knowledge cards, external docs, guidelines
  Pattern: mentor_agent/FONTES/ as reference

LAYER 3: SHARED (shared_knowledge/)
  Purpose: "Cross-agent reusable knowledge"
  Contents: Marketplaces, copywriting, AI platforms
  Location: codexa.app/shared_knowledge/
```

### Reference Implementation

The `mentor_agent/FONTES/PROMPT_ENGINEERING/` system is the proven model:

```
4-STAGE PIPELINE:
Sources → EXTRACT → Structured JSON
                         ↓
                    INDEX → catalogo.json
                         ↓
                  SYNTHESIZE → Knowledge Cards
                         ↓
                CONSOLIDATE → Playbook
```

---

## INPUT_CONTRACT

### Required Inputs

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `$target_agents` | array | Agents to hydrate | All 10 (excl. ronronalda, qa) |
| `$hydration_mode` | enum | full \| incremental \| single | full |
| `$knowledge_sources` | array | Source categories | All available |

### Optional Inputs

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `$parallel_limit` | int | Max concurrent agents | 5 |
| `$dry_run` | bool | Simulate without writing | false |
| `$priority_agents` | array | Process first | [voice_agent, scout_agent] |

---

## OUTPUT_CONTRACT

### Primary Outputs

```yaml
$hydrated_agents:
  type: directory_structure
  per_agent:
    - FONTES/catalogo_fontes.json     # Domain knowledge index
    - FONTES/{categoria}/*.md         # Knowledge cards
    - config/domain_taxonomy.json     # Domain categories
    - iso_vectorstore/ (updated)      # Cross-references

$shared_knowledge:
  type: directory
  location: codexa.app/shared_knowledge/
  contents:
    - COPYWRITING_FRAMEWORKS/
    - MARKETPLACES/
    - AI_PLATFORMS/
    - BRAND_IDENTITY/
    - BRASIL_ECOMMERCE/

$hydration_report:
  type: MD + JSON
  location: outputs/hydration_reports/
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "300_ADW_KNOWLEDGE_HYDRATION",
  "phases": [
    {"phase_id": "phase_0", "phase_name": "Knowledge Discovery", "duration": "5-10min", "mode": "parallel_scouts"},
    {"phase_id": "phase_1", "phase_name": "Gap Analysis", "duration": "10-15min", "mode": "analysis"},
    {"phase_id": "phase_2", "phase_name": "Source Collection", "duration": "20-40min", "mode": "parallel_fetch"},
    {"phase_id": "phase_3", "phase_name": "Knowledge Extraction", "duration": "30-60min", "mode": "parallel_process"},
    {"phase_id": "phase_4", "phase_name": "Synthesis & Indexing", "duration": "20-30min", "mode": "sequential"},
    {"phase_id": "phase_5", "phase_name": "Cross-Agent Consolidation", "duration": "15-20min", "mode": "consolidate"},
    {"phase_id": "phase_6", "phase_name": "Validation & Report", "duration": "10-15min", "mode": "validate"}
  ]
}
```

---

## PHASE 0: KNOWLEDGE DISCOVERY (Parallel Scouts)

**Duration**: 5-10 min | **Mode**: /spawn scouts

**Objective**: Map existing knowledge and identify gaps across all target agents.

### Actions

```bash
/spawn preset:discovery
1. scout: Find all FONTES/ directories (existing knowledge)
2. scout: Find all iso_vectorstore files by agent
3. scout: Find shared knowledge candidates (duplicates)
4. scout: Find external source references
5. scout: Map knowledge_graph.json dependencies
```

### Scout Tasks

| Scout # | Mission | Output |
|---------|---------|--------|
| 1 | Inventory existing FONTES/ | `$existing_fontes` |
| 2 | Count iso_vectorstore by agent | `$iso_inventory` |
| 3 | Find duplicate/shared content | `$consolidation_candidates` |
| 4 | Extract URL references | `$external_sources` |
| 5 | Map knowledge graph | `$knowledge_dependencies` |

### Output

```json
{
  "existing_infrastructure": {
    "fontes_directories": ["mentor_agent/FONTES/", "FONTES/"],
    "iso_vectorstore_counts": {
      "anuncio_agent": 14,
      "voice_agent": 7,
      "scout_agent": 5
    }
  },
  "gaps_identified": {
    "critical": ["voice_agent", "scout_agent"],
    "moderate": ["photo_agent", "video_agent"],
    "healthy": ["mentor_agent", "anuncio_agent"]
  },
  "consolidation_opportunities": [
    {"category": "AI_PLATFORMS", "files": 3, "agents": ["photo", "video", "curso"]},
    {"category": "MARKETPLACES", "files": 62, "agents": ["anuncio", "pesquisa", "marca"]},
    {"category": "COPYWRITING", "files": 5, "agents": ["anuncio", "curso", "marca"]}
  ]
}
```

---

## PHASE 1: GAP ANALYSIS

**Duration**: 10-15 min | **Mode**: Analysis

**Objective**: Quantify knowledge gaps and prioritize hydration targets.

### Gap Scoring Matrix

| Agent | Current Files | Target Files | Gap Score | Priority |
|-------|---------------|--------------|-----------|----------|
| voice_agent | 7 | 20+ | 0.35 | CRITICAL |
| scout_agent | 5 | 15+ | 0.33 | CRITICAL |
| photo_agent | 24 | 30+ | 0.80 | MODERATE |
| video_agent | 27 | 35+ | 0.77 | MODERATE |
| anuncio_agent | 14 | 20+ | 0.70 | MODERATE |
| pesquisa_agent | 16 | 20+ | 0.80 | LOW |
| marca_agent | 18 | 25+ | 0.72 | MODERATE |
| curso_agent | 20 | 25+ | 0.80 | LOW |
| codexa_agent | 23 | 25+ | 0.92 | LOW |
| mentor_agent | 175+ | 175+ | 1.00 | REFERENCE |

### Domain Knowledge Requirements

```yaml
voice_agent:
  required_knowledge:
    - TTS_PLATFORMS: [elevenlabs, openai_tts, google_cloud_tts]
    - STT_PLATFORMS: [whisper, deepgram, assembly_ai]
    - VOICE_UI: [interaction_patterns, accessibility]
  sources:
    - ElevenLabs API docs
    - OpenAI TTS/Whisper docs
    - Voice UI best practices

scout_agent:
  required_knowledge:
    - SEARCH_PATTERNS: [semantic_search, indexing, relevance]
    - CODEBASE_NAVIGATION: [llm_context, file_discovery]
  sources:
    - FONTES/PROMPT_ENGINEERING patterns
    - Internal CODEXA patterns

photo_agent:
  required_knowledge:
    - AI_PLATFORMS: [midjourney_v6, dalle3, imagen, flux]
    - PHOTOGRAPHY: [product_photography, lighting, composition]
    - MARKETPLACE_VISUALS: [requirements_per_platform]
  sources:
    - Platform official docs
    - video_agent/knowledge/platforms/ (CONSOLIDATE)

video_agent:
  required_knowledge:
    - AI_VIDEO: [runway_gen3, pika, kling, heygen]
    - PRODUCTION: [storytelling, editing, social_formats]
    - YOUTUBE: [seo, algorithm_2024]
  sources:
    - Existing knowledge/platforms/ (OPTIMIZE)
    - YouTube Creator docs

anuncio_agent:
  required_knowledge:
    - MARKETPLACES: [ml, shopee, amazon_br, magalu]
    - COPYWRITING: [persuasion, gatilhos, estrutura]
    - COMPLIANCE: [termos_proibidos, anvisa, inmetro]
  sources:
    - mentor_agent/PROCESSADOS/LIVRO_marketplace (LINK)
    - Existing configs (CONSOLIDATE)

pesquisa_agent:
  required_knowledge:
    - RESEARCH_METHODS: [competitor_analysis, trends, pricing]
    - TOOLS: [google_trends, semrush, marketplace_apis]
    - BRAZIL_MARKET: [ecommerce_2024, regulations]
  sources:
    - External research tools docs
    - mentor_agent/PROCESSADOS/ (LINK)

marca_agent:
  required_knowledge:
    - BRANDING: [archetypes, positioning, naming]
    - VISUAL_IDENTITY: [color_psychology, typography, logos]
    - MESSAGING: [tone_of_voice, storytelling]
  sources:
    - Existing config/12_archetype_specs.json (OPTIMIZE)
    - Brand frameworks (ADD)

curso_agent:
  required_knowledge:
    - PLATFORMS: [hotmart, udemy, coursera]
    - PEDAGOGY: [adult_learning, microlearning, engagement]
    - CONTENT: [video_course_structure, workbooks]
  sources:
    - Hotmart Creator docs
    - Educational design patterns

codexa_agent:
  required_knowledge:
    - META_CONSTRUCTION: [agent_patterns, hop_patterns, adw_patterns]
    - PROMPT_ENGINEERING: [tool_calling, task_management]
    - CLAUDE_CODE: [subagents, mcp, workflows]
  sources:
    - FONTES/PROMPT_ENGINEERING (COMPLETE)
    - Claude Code docs
```

### Output

```json
{
  "hydration_plan": {
    "critical_priority": ["voice_agent", "scout_agent"],
    "high_priority": ["photo_agent", "video_agent", "anuncio_agent"],
    "medium_priority": ["marca_agent", "curso_agent"],
    "low_priority": ["pesquisa_agent", "codexa_agent"],
    "reference": ["mentor_agent"]
  },
  "estimated_effort": {
    "total_sources_to_fetch": 45,
    "total_cards_to_generate": 120,
    "shared_consolidations": 5
  }
}
```

---

## PHASE 2: SOURCE COLLECTION

**Duration**: 20-40 min | **Mode**: Parallel fetch

**Objective**: Gather external documentation and internal references.

### Source Categories

```yaml
EXTERNAL_DOCS (WebFetch):
  - AI platform docs (ElevenLabs, OpenAI, Runway, etc.)
  - Marketplace APIs (when accessible)
  - Framework docs (LangChain, etc.)

INTERNAL_REFERENCES (Scout):
  - mentor_agent/PROCESSADOS/ chapters
  - Existing knowledge/ directories
  - Config files with domain data

PROMPT_ENGINEERING:
  - FONTES/PROMPT_ENGINEERING/patterns/
  - FONTES/ai_tools_prompts/
```

### Parallel Fetch Strategy

```bash
/spawn model:haiku
1. fetch: ElevenLabs API docs → voice_agent/FONTES/TTS_PLATFORMS/
2. fetch: OpenAI TTS docs → voice_agent/FONTES/TTS_PLATFORMS/
3. fetch: Whisper docs → voice_agent/FONTES/STT_PLATFORMS/
4. fetch: Runway Gen3 docs → video_agent/FONTES/AI_VIDEO/
5. fetch: Midjourney v6 docs → photo_agent/FONTES/AI_PLATFORMS/
```

### Inaccessible Sources Handling

```yaml
strategy: graceful_degradation
actions:
  - Log inaccessible URL
  - Create placeholder with manual_fetch_required flag
  - Continue with available sources
  - Report in final output
```

---

## PHASE 3: KNOWLEDGE EXTRACTION

**Duration**: 30-60 min | **Mode**: Parallel process

**Objective**: Transform raw sources into structured knowledge cards.

### Extraction Pipeline (Per Source)

Using `mentor_agent/FONTES/PROMPT_ENGINEERING/extraction_schema.json` as template:

```python
def extract_knowledge(source_file, domain):
    """
    4-Stage Extraction Pipeline
    Reference: FONTES/PROMPT_ENGINEERING/pipeline_extract.py
    """

    # Stage 1: Parse source
    raw_content = read_source(source_file)

    # Stage 2: Extract structure
    extraction = {
        "metadata": {
            "domain": domain,
            "source": source_file.name,
            "date_extracted": today(),
            "tokens_estimate": len(raw_content) // 4
        },
        "sections": detect_sections(raw_content),
        "patterns": extract_patterns(raw_content, domain),
        "techniques": extract_techniques(raw_content),
        "insights_codexa": generate_insights(raw_content, domain),
        "metrics": {
            "clarity": score_clarity(raw_content),
            "completeness": score_completeness(raw_content),
            "reusability": score_reusability(raw_content),
            "innovation": score_innovation(raw_content)
        }
    }

    # Stage 3: Generate knowledge card
    card = synthesize_card(extraction, domain)

    # Stage 4: Validate quality (5D)
    if validate_5d(card) >= 0.75:
        return card
    else:
        return improve_card(card)
```

### Knowledge Card Template

```markdown
# {TITULO DO CONHECIMENTO}

**Domain**: {domain}
**Category**: {categoria}
**Source**: {fonte_original}
**Quality Score**: {score}/1.0

## RESUMO EXECUTIVO
{1-2 paragrafos com essencia absoluta}

## CONCEITOS-CHAVE
- **{Conceito 1}**: {Explicacao pratica}
- **{Conceito 2}**: {Explicacao pratica}
- **{Conceito 3}**: {Explicacao pratica}

## COMO APLICAR
1. {Passo 1 - acao concreta}
2. {Passo 2 - acao concreta}
3. {Passo 3 - acao concreta}

## EXEMPLOS PRATICOS
### Exemplo 1: {Contexto}
**Antes**: {situacao problematica}
**Depois**: {situacao resolvida}
**Resultado**: {metrica tangivel}

## QUANDO USAR
- Situacao 1 (especifica)
- Situacao 2 (especifica)
- Situacao 3 (especifica)

## RELACIONADO
- Ver tambem: {outro_arquivo.md}

---
**Processado**: {data}
**Tokens**: ~{count}
```

### Parallel Processing

```bash
/spawn model:sonnet
1. process: voice_agent sources (TTS/STT)
2. process: scout_agent sources (search patterns)
3. process: photo_agent sources (AI platforms)
4. process: video_agent sources (AI video)
5. process: remaining agents sources
```

---

## PHASE 4: SYNTHESIS & INDEXING

**Duration**: 20-30 min | **Mode**: Sequential

**Objective**: Create catalogo.json indexes and cross-references.

### Per-Agent Index Structure

```json
{
  "version": "1.0.0",
  "agent": "voice_agent",
  "last_updated": "2025-12-05",
  "categories": [
    {
      "id": "TTS_PLATFORMS",
      "files": ["elevenlabs.md", "openai_tts.md", "google_cloud_tts.md"],
      "total_tokens": 4500
    },
    {
      "id": "STT_PLATFORMS",
      "files": ["whisper.md", "deepgram.md"],
      "total_tokens": 3000
    },
    {
      "id": "VOICE_UI",
      "files": ["interaction_patterns.md", "accessibility.md"],
      "total_tokens": 2500
    }
  ],
  "search_triggers": [
    "elevenlabs", "tts", "text-to-speech", "voice", "audio",
    "whisper", "stt", "speech-to-text", "transcription"
  ],
  "cross_agent_refs": {
    "video_agent": ["voice_scripts", "narrator"],
    "curso_agent": ["audio_lessons"]
  }
}
```

### Update Knowledge Graph

Add new task types and knowledge categories to `mentor_agent/FONTES/knowledge_graph.json`:

```json
{
  "task_types": {
    "voice_generation": {
      "primary_agent": "voice_agent",
      "required_knowledge": ["voice_agent/FONTES/TTS_PLATFORMS/"],
      "recommended_knowledge": ["voice_agent/FONTES/VOICE_UI/"],
      "triggers": ["voice", "audio", "tts", "narration"],
      "estimated_tokens": 8000
    }
  }
}
```

---

## PHASE 5: CROSS-AGENT CONSOLIDATION

**Duration**: 15-20 min | **Mode**: Consolidate

**Objective**: Create shared_knowledge/ with deduplicated content.

### Shared Knowledge Structure

```
codexa.app/shared_knowledge/
├── 00_MANIFEST.md                    # Index of all shared knowledge
│
├── COPYWRITING_FRAMEWORKS/           # anuncio, curso, marca
│   ├── 00_MANIFEST.md
│   ├── 01_persuasion_patterns.md     # From LIVRO_copywriting
│   ├── 02_semantic_vocabulary.md     # Generalized from LP guides
│   ├── 03_marketplace_copy_rules.md  # From LIVRO_marketplace
│   └── 04_brand_voice_template.json
│
├── MARKETPLACES/                     # anuncio, pesquisa, marca
│   ├── 00_MANIFEST.md
│   ├── 01_marketplace_matrix.md      # ML vs Shopee vs Amazon rules
│   ├── 02_regulatory_framework.md    # ANVISA, INMETRO, CONAR
│   └── links_to_mentor_PROCESSADOS.md
│
├── AI_PLATFORMS/                     # photo, video, curso
│   ├── 00_MANIFEST.md
│   ├── 01_platform_comparison.md
│   ├── runway_prompting_guide.md     # From video_agent
│   ├── pika_prompting_guide.md
│   ├── midjourney_v6_guide.md
│   └── platform_selection_guide.md
│
├── BRAND_IDENTITY/                   # marca, anuncio, curso, video
│   ├── 00_MANIFEST.md
│   ├── 01_identity_template.md       # Parameterized
│   ├── 02_personality_framework.md   # 4D model
│   ├── 03_voice_guidelines.json
│   └── 04_red_flags_safety.md
│
└── BRASIL_ECOMMERCE/                 # ALL agents
    ├── 00_MANIFEST.md
    ├── 01_regulatory_framework.md
    ├── 02_marketplace_ecosystem.md
    ├── 03_cultural_linguistic_guide.md
    └── 04_payment_shipping.md
```

### Consolidation Rules

```yaml
consolidation_triggers:
  - duplicate_content: ">80% similarity across agents"
  - shared_domain: "3+ agents need same knowledge"
  - maintenance_burden: "update once, benefit all"

consolidation_actions:
  - Move to shared_knowledge/
  - Create symlinks or references in agent FONTES/
  - Update catalogo.json with cross-references
  - Remove duplicates from agent-specific locations
```

---

## PHASE 6: VALIDATION & REPORT

**Duration**: 10-15 min | **Mode**: Validate

**Objective**: Ensure quality and generate comprehensive report.

### Validation Checklist

```yaml
per_agent:
  - [ ] FONTES/ directory created
  - [ ] catalogo_fontes.json present
  - [ ] All knowledge cards pass 5D validation (>=0.75)
  - [ ] Cross-references valid
  - [ ] No broken links

shared_knowledge:
  - [ ] All 5 categories populated
  - [ ] MANIFESTs accurate
  - [ ] No orphan files

knowledge_graph:
  - [ ] All new task types registered
  - [ ] All new categories indexed
  - [ ] Cross-agent dependencies mapped
```

### Quality Gates

| Gate | Threshold | Action if Fail |
|------|-----------|----------------|
| Card quality score | >= 0.75 | Improve card |
| Index completeness | 100% | Flag missing |
| Cross-reference validity | 100% | Fix broken refs |
| Duplicate detection | <20% | Consolidate more |

### Hydration Report

```markdown
# Knowledge Hydration Report

**Workflow**: 300_ADW_KNOWLEDGE_HYDRATION
**Executed**: {DATE}
**Duration**: {TIME}
**Mode**: {full|incremental|single}

## Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total FONTES files | {n} | {n} | +{n} |
| Knowledge cards | {n} | {n} | +{n} |
| Shared categories | {n} | 5 | +{n} |
| Coverage score | {%} | {%} | +{%} |

## Per-Agent Results
| Agent | Status | Cards Added | Gap Closed |
|-------|--------|-------------|------------|
| voice_agent | CRITICAL→OK | +15 | 35%→85% |
| scout_agent | CRITICAL→OK | +10 | 33%→80% |
| photo_agent | MODERATE→OK | +8 | 80%→95% |
| ... | ... | ... | ... |

## Shared Knowledge Created
- COPYWRITING_FRAMEWORKS/: 4 files
- MARKETPLACES/: 3 files
- AI_PLATFORMS/: 5 files
- BRAND_IDENTITY/: 4 files
- BRASIL_ECOMMERCE/: 4 files

## Consolidation Savings
- Duplicate files removed: {n}
- Token savings: ~{n}k tokens
- Maintenance surface: -{n}%

## Issues Encountered
{list of issues and resolutions}

## Recommendations
{future improvements}
```

---

## EXECUTION

### Quick Start (Single Agent)

```bash
# Hydrate critical agent
/prime-codexa
Execute ADW-300 for voice_agent --mode=single

# Or via slash command
/hydrate voice_agent
```

### Full Pipeline (All Agents)

```bash
# Load context
/prime-codexa

# Execute full hydration
Execute ADW-300 --mode=full --parallel_limit=5

# Priority order: critical first
# voice_agent → scout_agent → photo_agent → video_agent → ...
```

### Incremental Update

```bash
# Only update changed sources
Execute ADW-300 --mode=incremental --since=2025-12-01
```

---

## SLASH COMMAND INTEGRATION

### /hydrate {agent}

```bash
/hydrate voice_agent
# → Executes phases 0-6 for single agent
# → Creates FONTES/ structure
# → Generates knowledge cards
# → Updates catalogo.json
# → Reports results
```

### /hydrate --all

```bash
/hydrate --all
# → Full pipeline for all 10 agents
# → Creates shared_knowledge/
# → Consolidates duplicates
# → Updates knowledge_graph.json
```

### /hydrate --status

```bash
/hydrate --status
# → Shows current hydration state per agent
# → Identifies gaps
# → Recommends priorities
```

---

## DEPENDENCIES

### Required Infrastructure
- `mentor_agent/FONTES/PROMPT_ENGINEERING/` (reference implementation)
- `_shared/phase0_knowledge_loading.md` (knowledge loading module)
- `mentor_agent/FONTES/knowledge_graph.json` (routing)
- `scout` MCP server (file discovery)

### Related ADWs
- ADW-104: ISO_VECTORSTORE_OPTIMIZATION (Layer 1)
- ADW-205: KNOWLEDGE_ENRICHMENT (single-file enrichment)
- ADW-203: PARALLEL_ORCHESTRATION (spawn patterns)

---

## SUCCESS CRITERIA

### Workflow Succeeds When
- [ ] All 10 agents have FONTES/ directory
- [ ] All agents have catalogo_fontes.json
- [ ] Critical gaps closed (voice_agent, scout_agent >= 80% coverage)
- [ ] shared_knowledge/ has all 5 categories
- [ ] knowledge_graph.json updated
- [ ] No broken cross-references
- [ ] Report generated

### Workflow Fails When
- [ ] Cannot create FONTES/ structure
- [ ] External sources completely inaccessible
- [ ] Quality scores below threshold (<0.75)
- [ ] Critical agents still below 50% coverage

---

## ROLLBACK

```bash
# If hydration causes issues
git checkout -- codexa.app/agentes/*/FONTES/
git checkout -- codexa.app/shared_knowledge/
git checkout -- mentor_agent/FONTES/knowledge_graph.json
```

---

**Version**: 1.0.0 | **Status**: Production Ready
**Reference**: mentor_agent/FONTES/PROMPT_ENGINEERING/
**Author**: codexa_agent + mentor_agent collaboration
**Trigger**: /hydrate {agent} | /hydrate --all
