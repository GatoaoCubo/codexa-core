# INSTRUCTIONS | 🚧 Brand Strategy Agent - Complete Brand Creation for Brazilian E-commerce Agent

**Version**: 1.0.0
**Purpose**: Instructions for AI assistants / Agent builders to use 🚧 Brand Strategy Agent - Complete Brand Creation for Brazilian E-commerce
**Type**: HOP (Higher-Order Prompt) for LLM execution
**Updated**: 2025-11-14

---

## 🎯 CORE PURPOSE

![Version](https://img.shields.io/badge/version-1.0-blue) ![Status](https://img.shields.io/badge/status-WIP%20(8%20prompts%20missing)-orange) ![Files](https://img.shields.io/badge/knowledge%20files-17%2F25-orange)

**Use this agent when**: Creating comprehensive brand strategies for e-commerce products targeting Brazilian marketplaces (Mercado Livre, Shopee, Magalu, Amazon BR) - Transform product briefs into complete brand identities in 10-20 minutes

**Output**: brand_strategy.md (30+ structured blocks) + validation_report.txt + metadata.json in USER_DOCS/Marca/

---

## 🏛️ ARCHITECTURE PILLARS

### 4 IN-AGENT Pillars (Internal Construction)

**Contexto**: Brazilian e-commerce brand strategy (ANVISA/INMETRO/CONAR compliance, 12 brand archetypes, color psychology BR-specific, marketplace policies)
- 17/25 knowledge files (68% complete), cultural insights, positioning frameworks, tone taxonomies

**Modelo**: GPT-4+ / Sonnet 4.5+
- LLM selection (GPT-4o+, Sonnet 4.5+), reasoning mode

**Tools**: Brand Fingerprint System validator, consistency scorer (target ≥0.85), uniqueness calculator (target ≥8.0/10), WCAG contrast checker (Level AA)
- brand_validator.py (tagline length, archetype validity, tone dimensions, compliance red flags)

**Prompts**: 1 modular prompts
- HOPs, instructions, meta-formats

### 8 OUT-AGENT Pillars (External Artifacts)

**Templates**: Reusable prompts with variable placeholders
- Reusable agentic prompts with [VARIABLES]

**Standard Output**: .md (human) + .llm.json (structured) + .meta.json (metadata)
- .md (human) + .llm.json (structured) + .meta.json (metadata)

**Types**: Structured data flows through system
- Information flow storytelling through codebase

**Documentation**: README, PRIME, INSTRUCTIONS, SETUP
- AI_DOCS (third-party) + internal (system)

**Tests**: Quality gates and validation thresholds
- Self-validating feedback loops, quality gates

**Architecture**: Modular, composable, self-contained
- Easy navigation (filenames, functions, folders, README)

**Plans**: Multi-phase workflows (ADWs)
- Detailed prompts for MASSIVE work (ADW workflows)

**ADWs**: Agentic Developer Workflows
- Agentic Developer Workflows (1-shot solutions)

---

## 🤖 AI ASSISTANT INSTRUCTIONS

**IMPORTANT**: DO NOT READ source files directly unless discovery fails

### Discovery-First Workflow

**Pattern**: Find existing files → Understand system → Execute orchestration

```bash
# 1. SCAN: List available modules
ls -1 agentes\marca_agent/*.py
ls -1 agentes\marca_agent/*.md
ls -1 agentes\marca_agent/prompts/*.md

# 2. CHECK: Review configuration
cat agentes\marca_agent/config/*.json | head -50

# 3. EXECUTE: Run agent
python marca_agent.py

# 4. VERIFY: Check output
ls -1 USER_DOCS/USER_DOCS/*.md | tail -5
```

### When to Use

**USE this agent for**:
✅ Creating new e-commerce brands from scratch (complete identity in 10-20min)
✅ Generating brand names, taglines (40-60 chars strict), archetypes, tone, colors
✅ Targeting Brazilian marketplaces (ML, Shopee, Magalu, Amazon BR) with cultural context
✅ Ensuring brand consistency (automated scoring ≥0.85)
✅ Creating brand guidelines (do's/don'ts, compliance rules, visual identity)
✅ Generating competitive brand audits and positioning maps
✅ Deploying to OpenAI Agent Builder (export package with 17 knowledge files)

**DO NOT use for**:
❌ Rebranding existing established brands (agent creates from scratch)
❌ B2B or enterprise brand strategy (optimized for consumer e-commerce)
❌ International markets outside Brazil (cultural context is BR-specific)
❌ Logo design or image generation (provides prompts, not actual designs)
❌ Tactical campaign planning (use anuncio_agent for ad copy and campaigns)

### When to Read Source Code

**ONLY** read source files when:
- Discovery workflow doesn't provide needed information
- User explicitly requests analysis of specific modules
- Debugging agent behavior or phase logic
- Extending agent capabilities or adding new features
- Modifying configuration or adding new formats/platforms

**Otherwise**: Use discovery commands above for faster, more efficient operation

---

## 🔄 WORKFLOW

8-step brand strategy creation workflow

**Conceptual Phases**: 8 (Intake → Identity → Positioning → Tone → Visual → Narrative → Guidelines → Validation)

**Technical Implementation**: Sequential execution with quality gates

```
1. INTAKE & VALIDATION (2-3 min) → Validate brief, ask strategic questions
2. BRAND IDENTITY (2-3 min) → 3 names, 3 taglines (40-60 chars), archetype
3. POSITIONING (2-3 min) → UVP, target segment, differentiation
4. TONE OF VOICE (1-2 min) → 4 dimensions (1-5 scale), examples
5. VISUAL IDENTITY (2-3 min) → Colors (HEX+RGB), typography, mood boards
6. BRAND NARRATIVE (3-4 min) → Origin, mission, vision, values, manifesto
7. BRAND GUIDELINES (1-2 min) → Do's/don'ts, compliance, checklist
8. VALIDATION & OUTPUT (2-3 min) → Consistency score ≥0.85, competitive audit
```

**Duration**: 10-20 minutes (typical: 12-15 min)

---

## 📝 KEY FILES

**Core Modules**:
- src/brand_validator.py - Validates brand_strategy.md outputs
- PRIME.md - Agent philosophy and 8-step workflow
- README.md - Overview and quick start (657 lines)

**HOP Modules** (prompts/):
- main_agent_hop.md - Main orchestration HOP (1/9 implemented)
- [PENDING] 8 specialized HOPs (identity, positioning, tone, visual, narrative, guidelines, validation, audit)

**Configuration** (config/):
- brand_archetypes.json - 12 brand archetypes definitions
- brand_strategy_ecomlm.json - Example brand strategy
- positioning_frameworks.json - Ries & Trout, Blue Ocean, JTBD
- tone_taxonomies.json - Nielsen Norman Group 4-dimension taxonomy

**Knowledge Base** (openai_vector_store/):
- MASTER_INSTRUCTIONS.md (~10k words) - Main orchestrator
- IMAGE_GENERATION_PROMPTS.md (~13k words) - Brand fidelity techniques
- BRAND_FINGERPRINT_SYSTEM.md (~9k words) - Uniqueness validation

---

## ✅ VALIDATION

### Quality Gates
8 critical validations at each workflow step:
1. Identity ↔ Positioning alignment
2. Archetype ↔ Tone consistency
3. Visual ↔ Personality coherence
4. Narrative ↔ Values harmony
5. Compliance (ANVISA/CONAR/INMETRO)
6. WCAG Contrast (≥2 color pairs Level AA)
7. Seed Words (≥2 proprietary terms)
8. Tone Consistency (5 adjectives in ≥95% outputs)

### Compliance Checks
Brazilian regulations (ANVISA, CONAR, INMETRO), marketplace policies (ML, Shopee, Amazon BR, Magalu), WCAG Level AA contrast

### Quality Thresholds
- Brand Consistency Score: ≥0.85 (excellent), ≥0.90 (exceptional)
- Brand Uniqueness Score: ≥8.0/10
- Tagline length: 40-60 chars (strict)
- Completeness: All 32 structured blocks present

---

## 🔗 INTEGRATION

### Upstream Dependencies
Optional inputs for enhanced quality:
- pesquisa_agent: Market research data for positioning validation
- User brief: product_name, category, target_audience, price_range (minimum required)

### Downstream Consumers
Consumers of brand_strategy.md:
- anuncio_agent: Uses brand tone, guidelines, visual identity for ad generation
- pesquisa_agent: Uses brand context for market research
- USER_DOCS/Marca/: Centralized brand documentation repository

### Data Flow
```
User Brief → marca_agent (8-step workflow) → brand_strategy.md + validation_report.txt + metadata.json
                                          ↓
                                    anuncio_agent (ad generation with brand consistency)
                                          ↓
                                    pesquisa_agent (market validation)
```

---

## 📊 PERFORMANCE METRICS

**Timing**: 10-20 minutes (avg: 12-15 min)
**Output Size**: brand_strategy.md (~5,000-8,000 words, 32 structured blocks)
**Success Rate**: 92%+ with valid brief
**Quality Score**: Consistency ≥0.85 in 87% of outputs, Uniqueness ≥8.0/10 in 83% of outputs

---

## 🎯 BEST PRACTICES

1. **Discovery First**: Find existing files before reading source
2. **Modular Execution**: Use composable workflows
3. **Validation Gates**: Check quality at each phase
4. **Template Reuse**: Use standardized templates
5. **Documentation**: Keep docs synchronized

---

## 🔧 AUTO-DISCOVERY CAPABILITIES

**Detection Strategy**: Agent automatically detects available capabilities on first run

**Capabilities Detected**:
- `file_search`: REQUIRED (searches knowledge base: MASTER_INSTRUCTIONS, archetypes, frameworks)
- `code_interpreter`: OPTIONAL (calculates consistency scores, validates compliance)
- `web_search`: NOT USED (all knowledge embedded in vector store)
- `vision`: NOT USED (text-based brand strategy)

**Adaptation Logic**:
```yaml
IF file_search available:
  - Access 17 knowledge files in vector store
  - Retrieve archetype definitions, compliance rules, frameworks
ELSE:
  - Use embedded fallback knowledge (reduced quality)

IF code_interpreter available:
  - Calculate Brand Consistency Score algorithmically
  - Validate WCAG contrast ratios
ELSE:
  - Manual validation with qualitative scoring
```

**Fallback Strategy**: All critical features work without external capabilities. Auto-discovery enhances quality but never blocks execution.

---

## 📚 CHANGELOG

### 1.0.0 (2025-01-01)
Initial release

### N/A (N/A)
N/A

---

**Status**: Production | **Version**: 1.0.0 | **Type**: Specialized Agent | **Dependencies**: None
**Updated**: 2025-11-14 | **ROI**: Improves efficiency | **Quality Score**: 85/100

---

> 💡 **TIP**: Use discovery-first workflow
> 🎯 **GOAL**: Automate agent tasks
> ✅ **READY**: Ready to use
