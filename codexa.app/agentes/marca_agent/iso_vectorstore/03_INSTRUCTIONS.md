<!-- iso_vectorstore -->
<!--
  Source: INSTRUCTIONS.md
  Agent: marca_agent
  Synced: 2025-11-30
  Version: 3.0.0
  Package: iso_vectorstore (export package)
-->

# INSTRUCTIONS | marca_agent | Brand Strategy Agent

**Version**: 3.0.0 | **Updated**: 2025-11-30
**Purpose**: Instructions for AI assistants using marca_agent for brand creation
**Type**: HOP-based workflow for Brazilian e-commerce brand strategy

---

## CORE PURPOSE

**What this agent does**: Creates comprehensive brand strategies for e-commerce products targeting Brazilian marketplaces (Mercado Livre, Shopee, Magalu, Amazon BR) - Transform product briefs into complete brand identities in 10-20 minutes

**Use this agent when**:
- Creating new e-commerce brands from scratch
- Generating brand names, taglines (40-60 chars strict), archetypes, tone, colors
- Targeting Brazilian marketplaces with cultural context
- Ensuring brand consistency (automated scoring >= 0.85)
- Creating brand guidelines (do's/don'ts, compliance, visual identity)

**Output**: brand_strategy.md (30+ structured blocks) + validation_report.txt + metadata.json

---

## ARCHITECTURE PILLARS

### 4 IN-AGENT Pillars

| Pillar | Implementation |
|--------|----------------|
| **Contexto** | Brazilian e-commerce brand strategy (ANVISA/INMETRO/CONAR compliance, 12 brand archetypes, color psychology BR-specific) |
| **Modelo** | Claude Sonnet 4+ or GPT-4o+ for brand strategy with cultural reasoning |
| **Tools** | Brand Fingerprint System validator, consistency scorer (>= 0.85), uniqueness calculator (>= 8.0/10), WCAG contrast checker |
| **Prompts** | Modular HOPs for identity, positioning, tone, visual, narrative, validation |

### 8 OUT-AGENT Pillars

| Pillar | Implementation |
|--------|----------------|
| **Templates** | Reusable prompts with variable placeholders |
| **Standard Output** | .md (human) + .llm.json (structured) + .meta.json (metadata) |
| **Types** | input_schema.json (validation), output_schema.json (format) |
| **Documentation** | QUICK_START, PRIME, INSTRUCTIONS, README, ARCHITECTURE |
| **Tests** | Quality gates and validation thresholds |
| **Architecture** | Modular, composable, self-contained |
| **Plans** | Multi-phase ADW workflows |
| **ADWs** | Agentic Developer Workflows (1-shot solutions) |

---

## DISCOVERY-FIRST WORKFLOW

**Pattern**: Find existing files -> Understand system -> Execute orchestration

### Step 1: Scan Available Modules
```bash
# List available modules
ls -1 agentes/marca_agent/*.py
ls -1 agentes/marca_agent/*.md
ls -1 agentes/marca_agent/prompts/*.md
```

### Step 2: Review Configuration
```bash
# Check configuration files
cat agentes/marca_agent/config/*.json | head -50
```

### Step 3: Execute Agent
```bash
python marca_agent.py
```

---

## WHEN TO USE

**USE this agent for**:
- Creating new e-commerce brands from scratch (complete identity in 10-20min)
- Generating brand names, taglines (40-60 chars strict), archetypes, tone, colors
- Targeting Brazilian marketplaces (ML, Shopee, Magalu, Amazon BR) with cultural context
- Ensuring brand consistency (automated scoring >= 0.85)
- Creating brand guidelines (do's/don'ts, compliance rules, visual identity)
- Generating competitive brand audits and positioning maps

**DO NOT use for**:
- Rebranding existing established brands (agent creates from scratch)
- B2B or enterprise brand strategy (optimized for consumer e-commerce)
- International markets outside Brazil (cultural context is BR-specific)
- Logo design or image generation (provides prompts, not actual designs)
- Tactical campaign planning (use anuncio_agent for ad copy and campaigns)

---

## WHEN TO READ SOURCE CODE

**ONLY** read source files when:
- Discovery workflow doesn't provide needed information
- User explicitly requests analysis of specific modules
- Debugging agent behavior or phase logic
- Extending agent capabilities or adding new features
- Modifying configuration or adding new formats/platforms

**Otherwise**: Use discovery commands for faster, more efficient operation

---

## WORKFLOW PHASES

### 8-Step Brand Strategy Creation

| Phase | Duration | Description |
|-------|----------|-------------|
| 1. INTAKE & VALIDATION | 2-3 min | Validate brief, ask strategic questions |
| 2. BRAND IDENTITY | 2-3 min | 3 names, 3 taglines (40-60 chars), archetype |
| 3. POSITIONING | 2-3 min | UVP, target segment, differentiation |
| 4. TONE OF VOICE | 1-2 min | 4 dimensions (1-5 scale), examples |
| 5. VISUAL IDENTITY | 2-3 min | Colors (HEX+RGB), typography, mood boards |
| 6. BRAND NARRATIVE | 3-4 min | Origin, mission, vision, values, manifesto |
| 7. BRAND GUIDELINES | 1-2 min | Do's/don'ts, compliance, checklist |
| 8. VALIDATION & OUTPUT | 2-3 min | Consistency score >= 0.85, competitive audit |

**Total Duration**: 10-20 minutes (typical: 12-15 min)

---

## KEY FILES REFERENCE

| File | Purpose | When to Use |
|------|---------|-------------|
| PRIME.md | Agent philosophy and workflow | Context loading |
| README.md | Overview and quick start | First read |
| INSTRUCTIONS.md | This file | Workflow rules |
| src/brand_validator.py | Validation tools | Quality checks |
| config/brand_archetypes.json | 12 archetype definitions | Identity phase |
| config/positioning_frameworks.json | Strategy frameworks | Positioning phase |
| config/tone_taxonomies.json | 4-dimension taxonomy | Tone phase |
| iso_vectorstore/ | Knowledge base | Reference materials |

---

## VALIDATION CHECKLIST

### Quality Gates (8 Critical Validations)

1. Identity <-> Positioning alignment
2. Archetype <-> Tone consistency
3. Visual <-> Personality coherence
4. Narrative <-> Values harmony
5. Compliance (ANVISA/CONAR/INMETRO)
6. WCAG Contrast (>= 2 color pairs Level AA)
7. Seed Words (>= 2 proprietary terms)
8. Tone Consistency (5 adjectives in >= 95% outputs)

### Quality Thresholds

| Metric | Threshold |
|--------|-----------|
| Brand Consistency Score | >= 0.85 (excellent), >= 0.90 (exceptional) |
| Brand Uniqueness Score | >= 8.0/10 |
| Tagline length | 40-60 chars (strict) |
| Completeness | All 32 structured blocks present |

---

## INTEGRATION

### Upstream Dependencies (Optional)
| Agent | Provides |
|-------|----------|
| pesquisa_agent | Market research data for positioning validation |
| User brief | product_name, category, target_audience, price_range |

### Downstream Consumers
| Consumer | Uses |
|----------|------|
| anuncio_agent | Brand tone, guidelines, visual identity for ad generation |
| pesquisa_agent | Brand context for market research |
| USER_DOCS/Marca/ | Centralized brand documentation |

### Data Flow
```
User Brief -> marca_agent (8-step workflow) -> brand_strategy.md
                                            -> validation_report.txt
                                            -> metadata.json
                                                    |
                                                    v
                                            anuncio_agent (ad generation)
                                                    |
                                                    v
                                            pesquisa_agent (market validation)
```

---

## PERFORMANCE METRICS

| Metric | Target | Typical |
|--------|--------|---------|
| Execution time | 10-20 min | 12-15 min |
| Output size | 5,000-8,000 words | 32 blocks |
| Success rate | >= 90% | 92% with valid brief |
| Consistency score | >= 0.85 | 87% of outputs |
| Uniqueness score | >= 8.0/10 | 83% of outputs |

---

## BEST PRACTICES

1. **Discovery First**: Find existing files before reading source
2. **Modular Execution**: Use composable workflows
3. **Validation Gates**: Check quality at each phase
4. **Template Reuse**: Use standardized templates
5. **Documentation**: Keep docs synchronized

---

## AUTO-DISCOVERY CAPABILITIES

| Capability | If Available | If Not Available |
|------------|--------------|------------------|
| file_search | Access 17 knowledge files in vector store | Use embedded fallback knowledge |
| code_interpreter | Calculate Brand Consistency Score algorithmically | Manual qualitative scoring |
| web_search | NOT USED (all knowledge embedded) | N/A |
| vision | NOT USED (text-based brand strategy) | N/A |

**Fallback Strategy**: All critical features work without external capabilities. Auto-discovery enhances quality but never blocks execution.

---

## FRAMEWORKS USED

- **12 Brand Archetypes** - Jungian archetype mapping
- **Metamorfose Methodology** - Brazilian brand transformation
- **Brand Fingerprint System** - Consistency validation
- **WCAG 2.1** - Accessibility compliance
- **Nielsen Norman Group** - 4-dimension tone taxonomy

---

**Status**: Production Ready | **Version**: 3.0.0 | **Quality Score**: 89/100
**Updated**: 2025-11-30 | **Framework**: 12 Leverage Points
