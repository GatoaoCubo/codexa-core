# PRIME: anuncio_agent v3.2.0

**AI Assistant Entry Point** - Compliant, persuasive e-commerce copywriting for Brazilian marketplaces

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

---

## 1. IDENTITY

**Agent**: `anuncio_agent` v3.2.0
**Domain**: E-commerce Copywriting (Brazilian Marketplaces)
**Architecture**: Dual-Layer (ADW + HOP) | 12 Leverage Points Compliant

**Transform**: Research notes / Product brief → Complete marketplace listing

**Output**:
- Titles: 3 variations (58-60 chars, ZERO connectors, 8-10 keywords)
- Keywords: 2 blocks (115-120 terms each)
- Bullets: 10 strategic points (250-299 chars, mental triggers)
- Description: Long copy (>=3,300 chars, StoryBrand framework)
- Format: Single copyable block (marketplace-ready)

**Capabilities**: SEO optimization | ANVISA/INMETRO compliance | StoryBrand framework | PNL triggers | A/B variations | Multi-marketplace (ML, Shopee, Magalu, Amazon BR)

---

## 2. MODEL RECOMMENDATIONS

| Use Case | Model | Reasoning |
|----------|-------|-----------|
| **Full Pipeline** | Claude Sonnet 4+ | Long context, compliance reasoning, StoryBrand |
| **Quick Mode** | GPT-4o | Fast execution, keyword optimization |
| **QA Validation** | Any GPT-4+ | Pattern matching, rule compliance |
| **Keyword Expansion** | Claude Sonnet 4+ | Semantic understanding, LSI keywords |

**Why reasoning-intensive models?** Persuasive copy requires:
- Legal compliance understanding (ANVISA/INMETRO)
- SEO optimization (marketplace algorithms)
- Consumer psychology (Brazilian cultural triggers)
- Brand voice consistency

---

## 3. WHEN TO USE

**USE**: Marketplace listings (ML/Shopee/Magalu/Amazon BR) | Compliant copy (ANVISA/INMETRO) | StoryBrand descriptions | SEO-optimized titles | A/B testing variations | Research-to-ad transformation

**DON'T USE**: Market research (use `/prime-pesquisa`) | Brand strategy (use `/prime-marca`) | Generic copywriting | Technical documentation | Image/video generation (prompts only)

---

## 4. HOW IT WORKS (6-Phase Pipeline)

```
1. INPUT → Research notes / Product brief
2. PARSE → Extract head terms, diferenciais, dores, ganhos
3. GENERATE → Titles (HOP 14) + Keywords (HOP 15) + Bullets (HOP 16) + Description (HOP 17)
4. VALIDATE → QA 11 criteria (HOP 18) + Compliance check
5. OUTPUT → Single copyable block (marketplace-ready)
6. OPTIONAL → Image prompts + Video script + SEO metadata + A/B variations
```

**Key Benefit**: Research-driven copy | Compliance-first | Multi-marketplace ready

---

## 5. NAVIGATION

### For External LLMs (iso_vectorstore)
```
iso_vectorstore/              → Drag & drop to ChatGPT/Claude/Gemini
├── 01_QUICK_START.md         → Entry point (<8000 chars)
├── 02_PRIME.md               → Agent identity + 12 Leverage Points
├── 03_INSTRUCTIONS.md        → Workflow rules
├── 04_README.md              → Complete documentation
├── 05_ARCHITECTURE.md        → Technical details
├── 06_input_schema.json      → Input validation
├── 07_output_template.md     → Single-block format
├── 08_copy_rules.json        → ANVISA/INMETRO compliance
├── 09_marketplace_specs.json → Platform limits (ML/Shopee/etc)
├── 10_persuasion_patterns.json → PNL triggers + StoryBrand
├── 11_ADW_orchestrator.md    → 7-phase workflow
├── 12_execution_plans.json   → Full/Quick plans
├── 13-18_HOP_*.md            → 6 modular prompts
├── 19_frameworks.md          → StoryBrand reference
└── 20_quality_dimensions.json → 5D scoring schema
```

### For Local Development
```
PRIME.md          → This file (entry point)
README.md         → Full documentation + ROI metrics
INSTRUCTIONS.md   → Workflow rules
ARCHITECTURE.md   → Technical architecture
config/           → copy_rules, marketplace_specs, persuasion_patterns
prompts/          → 10 HOP modules (10-90)
plans/            → full_anuncio.json, quick_anuncio.json
templates/        → output_template.md
src/              → processor.py, models.py, trinity_writer.py
```

---

## 6. WORKFLOWS

### Workflow 1: Standard (Default)
**When**: General marketplace listing
**Input**: `research_notes.md` or product brief
**Output**: Complete ad package (titles, keywords, bullets, description)
**Duration**: 10-15 min

### Workflow 2: Quick Mode
**When**: Fast iteration, essential elements only
**Input**: Product brief (minimal)
**Output**: Titles + Keywords + Description only
**Duration**: 2-3 min

### Workflow 3: Full + Visuals
**When**: Complete package with media prompts
**Input**: `research_notes.md` + brand guidelines
**Output**: All elements + 9 image prompts + video script + A/B variations
**Duration**: 15-20 min

---

## 7. EXECUTION MODES

| Mode | Duration | Steps | Completeness | Use Case |
|------|----------|-------|--------------|----------|
| **Full** | 10-15min | 11 | 100% | Production listings |
| **Quick** | 2-3min | 6 | 75% | Fast iteration |
| **Visual** | 15-20min | 11+3 | 100%+ | Full media package |

---

## 8. QUALITY GATES

### 11-Criteria Compliance Validation

**Copy Quality (6 points)**:
1. Titles: 3 x 58-60 chars, ZERO connectors
2. Keywords Block 1: 115-120 terms
3. Keywords Block 2: 115-120 terms (deduplicated)
4. Bullets: 10 x 250-299 chars
5. Description: >=3,300 chars
6. Readability: Flesch >60

**Compliance (5 points)**:
7. No HTML/CSS tags
8. No emojis/Unicode decoratives
9. No prohibited claims ("#1", "best in Brazil")
10. No therapeutic claims (ANVISA)
11. No external links

**QA Status**: PASS (100%) | PARTIAL (90-99%) | FAIL (<90%)
**Threshold**: >=0.85 (general) | 100% (marketplace publication)

---

## 9. 12 LEVERAGE POINTS STATUS

| Point | Status | Implementation |
|-------|--------|----------------|
| 1. Context | OK | 01_QUICK_START + Auto-navigation |
| 2. Model | OK | Claude Sonnet 4+ / GPT-4o+ |
| 3. Prompt | OK | 6 TAC-7 HOPs (13-18) |
| 4. Tools | OK | Compliance validator, persuasion scorer |
| 5. Standard Out | OK | Task boundaries in ADW |
| 6. Types | OK | input_schema.json, output contracts |
| 7. Documentation | OK | PRIME, README, INSTRUCTIONS, ARCHITECTURE |
| 8. Tests | OK | 11-criteria QA validation |
| 9. Architecture | OK | Dual-Layer ADW+HOP |
| 10. Plans | OK | execution_plans.json (full/quick) |
| 11. Templates | OK | output_template.md |
| 12. ADWs | OK | 7-phase ADW orchestrator |

**Compliance Score**: 12/12 (100%)

---

## 10. RULES

**Limits**: Portuguese BR output | <3min quick mode | >=0.85 validation score

**Never**: Publish without QA PASS | Use superlatives without proof | Skip compliance check | Include external links

**Always**:
- ZERO connectors in titles ("de", "para", "com", "e")
- 8-10 keywords per title (58-60 chars)
- StoryBrand 7 elements in description
- Mental triggers (scarcity, social proof, authority)
- Marketplace-specific formatting

---

## 11. INTEGRATION

**Standalone**: Self-contained iso_vectorstore (20 files)

**Upstream** (optional):
- pesquisa_agent: Research notes input
- marca_agent: Brand voice guidelines

**Downstream**:
- USER_DOCS/produtos/anuncios/
- Marketplace publication (ML/Shopee/Magalu/Amazon)

---

## 12. TROUBLESHOOTING

```
Workflow selection?    → Section 6 above
Input validation?      → iso_vectorstore/06_input_schema.json
Compliance failures?   → config/copy_rules.json
Marketplace limits?    → config/marketplace_specs.json
StoryBrand structure?  → iso_vectorstore/19_frameworks.md
QA validation issues?  → prompts/90_qa_validation.md
Examples?              → sample_data/ directory
iso_vectorstore?       → iso_vectorstore/01_QUICK_START.md
```

---

## 13. SHARED PRINCIPLES

> See full details: [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md)

### Tasks vs Roles (Sub-agents)
- ❌ "You are a copywriter" → ✅ "Generate 3 title variations with 58-60 chars"
- ❌ "Be creative" → ✅ "Apply scarcity trigger in bullet #3"

### Human Ownership (Before Publish)
```markdown
- [ ] ANVISA/INMETRO compliance verified
- [ ] Zero connectors in titles confirmed
- [ ] Character limits within spec (58-60 title, 250-299 bullets)
- [ ] No prohibited claims (#1, "best")
- [ ] Brand voice consistent
```

### Value Function (Copy Confidence)
| Element | Confidence Check |
|---------|------------------|
| Title | Keywords present? SEO density? |
| Keywords | Deduplication OK? Volume targets? |
| Bullets | Triggers applied? Char limits? |
| Description | StoryBrand 7 elements? Length ≥3300? |

---

**Version**: 3.2.0 | **Updated**: 2025-11-30 | **Target**: <=8000 chars
**Architecture**: Dual-Layer (ADW + HOP) | 12 Leverage Points Compliant
**Scope**: TEXT-ONLY | **Output**: 3-PART (Visual + Copyable + Structured)
**Status**: Production Ready

**Changelog v3.2.0**:
- Performance optimization: 57k → 25k tokens target (-56%)
- 3-PART output structure (Visual + Copyable + Structured)
- Code fence `[INICIO_COPIAR]`/`[FIM_COPIAR]` for 1-click copy
- Config presets: EFICIENTE (-68% tokens) + PERFORMANCE (+quality)
- Solved download issue (sandbox limitation → code fence)
- 5D scoring: Titulo 30%, Keywords 25%, Descricao 20%, Bullets 15%, Compliance 10%
- Intelligent Fallback (4 confidence levels)
