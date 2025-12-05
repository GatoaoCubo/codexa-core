# /prime-marca | Brand Strategy Agent v3.1.0

**Purpose**: TAC-7 system for comprehensive Brazilian e-commerce brand identities
**Time**: 15-20min | **Output**: brand_strategy.md (32 blocks) + validation_report.txt + metadata.json (Trinity)
**Architecture**: Dual-Layer ADW+HOP | 5-Phase SDLC | 12 Leverage Points

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

> **LAW 9**: Scout-First Consolidation | Toda tarefa começa com scouts → CRUD Priority: Delete > Update > Read > Create

---

## ARCHITECTURE PILLARS

### 12 LEVERAGE POINTS OF AGENTIC BRANDING

| # | Leverage Point | Implementation | Reference |
|---|---------------|----------------|-----------|
| 1 | **Context** | Brazilian compliance, 12 archetypes, cultural insights | iso_vectorstore/08_brand_rules.json |
| 2 | **Model** | Claude Opus 4.5 / Sonnet 4.5+ | This file |
| 3 | **Prompt** | TAC-7 HOPs with structured execution | iso_vectorstore/13-15_HOP_*.md |
| 4 | **Tools** | Validator, consistency scorer, WCAG checker | src/brand_validator.py |
| 5 | **Standard Out** | Task boundaries, phase transitions | iso_vectorstore/11_ADW_orchestrator.md |
| 6 | **Types** | Input/output JSON schemas | iso_vectorstore/06_input_schema.json |
| 7 | **Documentation** | README, INSTRUCTIONS, ARCHITECTURE | iso_vectorstore/01-05_*.md |
| 8 | **Tests** | 8 quality gates, validation checklist | iso_vectorstore/07_output_template.md |
| 9 | **Architecture** | Dual-Layer ADW+HOP, 5-phase SDLC | iso_vectorstore/11_ADW_orchestrator.md |
| 10 | **Plans** | Full/Quick execution plans | iso_vectorstore/12_execution_plans.json |
| 11 | **Templates** | Output format, brand strategy template | iso_vectorstore/07_output_template.md |
| 12 | **ADWs** | 5-phase: Plan->Build->Test->Review->Document | iso_vectorstore/11_ADW_orchestrator.md |

### 4 IN-AGENT Pillars
**Contexto** - Brazilian compliance (ANVISA/INMETRO/CONAR), 12 brand archetypes, cultural insights, color psychology (BR-specific) | **Modelo** - Claude Opus 4.5 / Sonnet 4.5+ (brand strategy requires deep creative reasoning + long context) | **Tools** - Brand Fingerprint System validator, consistency scorer, uniqueness calculator, WCAG contrast checker | **Prompts** - 5-phase ADW workflow + Metamorfose methodology + TAC-7 HOPs

### 8 OUT-AGENT Pillars
**Templates** - brand_strategy_template, input_schema.json, output_template.md | **Standard Output** - Trinity format: brand_strategy.md + .llm.json + .meta.json | **Types** - Brand briefs, archetype configs, positioning frameworks | **Documentation** - 01_QUICK_START, 02_PRIME, 03_INSTRUCTIONS | **Tests** - 8 quality gates, consistency >= 0.85, uniqueness >= 8.0/10 | **Architecture** - 5-phase SDLC, Dual-Layer ADW+HOP | **Plans** - full_brand_strategy, quick_positioning in execution_plans.json | **ADWs** - Plan -> Build -> Test -> Review -> Document

---

## 🤖 AI ASSISTANT INSTRUCTIONS

### Discovery-First Workflow
```bash
# 1. List knowledge files
ls -1 marca_agent/*.md
ls -1 marca_agent/openai_vector_store/*.{md,json}
ls -1 scripts/brand_*.py

# 2. Check configurations
cat marca_agent/config/brand_archetypes.json | head -50
cat marca_agent/config/positioning_frameworks.json | head -50
cat marca_agent/config/compliance_rules.json | head -50

# 3. Execute + validate
ls -1 export_package/
uv run scripts/brand_validator.py USER_DOCS/Marca/[brand]_strategy.md
```

### When to Use
✅ Creating new e-commerce brands from scratch (complete identity in 10-20min) | ✅ Understanding brand validation (consistency scoring, uniqueness algorithms) | ✅ Debugging brand execution (8-step workflow) | ✅ Deploying to OpenAI (export package with 17 knowledge files) | ✅ Ensuring brand consistency (automated scoring, target ≥0.85) | ✅ Generating brand guidelines (do's/don'ts, compliance, visual identity) | ✅ Modifying brand behavior (archetypes, tone, colors knowledge files) | ✅ Onboarding contributors (focused context on capabilities)

❌ Other agents (use appropriate `/prime-*`) | ❌ Rebranding established brands (creates from scratch) | ❌ B2B/enterprise branding (optimized for consumer e-commerce) | ❌ International markets (BR-specific cultural context) | ❌ Logo design execution (provides prompts, not actual designs)

### When to Read Source
ONLY if: Discovery fails | User requests framework/methodology analysis | Debugging validation logic | Extending capabilities (new archetypes/frameworks/marketplaces)

---

## AGENT FRAMEWORK

### Variables
**Input**:
- `$brief` (string|JSON) - product_name, category, target_audience, price_range (required) | marketplace_target, competitors, USPs, brand inspirations, tone preferences (optional)
- `$marketplace_target` (string) - "mercadolivre"|"shopee"|"magalu"|"amazon_br"|"all" (default: "all BR")
- `$output_path` (string) - Default: USER_DOCS/Marca/

**Quality**:
- `$consistency_threshold` (float) - Min brand consistency score (default: 0.85)
- `$uniqueness_threshold` (float) - Min brand uniqueness score (default: 8.0/10)
- `$wcag_compliance` (string) - Color contrast validation (default: "Level AA")
- `$seed_words_min` (int) - Min proprietary vocabulary (default: 2)

**Validation**:
- `$archetype_compatibility_check` (bool) - Validate archetype ↔ tone alignment (default: true)
- `$compliance_validation` (bool) - Enable ANVISA/INMETRO/CONAR checks (default: true)
- `$tone_consistency_threshold` (float) - Min tone adjectives in outputs (default: 95%)

**Cultural**:
- `$brazilian_context_enabled` (bool) - Apply BR-specific cultural insights (default: true)
- `$pt_br_linguistics` (bool) - Brazilian Portuguese patterns (default: true)

### Instructions (8-Step Workflow)

**1. INTAKE & VALIDATION** (2-3min): Validate brief vs BRAND_BRIEF_SCHEMA.json | Ask 3-5 strategic questions if insufficient | Extract product requirements + brand objectives | Set quality gates + validation thresholds

**2. BRAND IDENTITY** (2-3min): Generate 3 brand names (descriptive, evocative, creative) | Create 3 taglines (40-60 chars strict, no emojis) | Select primary + secondary archetype (from 12 options) | Define 5 core personality traits | **Gate**: Names unique, taglines within char limits

**3. POSITIONING STRATEGY** (2-3min): Craft unique value proposition (UVP) | Define target segment (demographic + psychographic + behavioral) | Map competitive differentiation (tangible + intangible) | Formulate brand promise | Apply Ries & Trout positioning framework | **Gate**: UVP ≥70% differentiated from competitors

**4. TONE OF VOICE** (1-2min): Define 4 personality dimensions (1-5 scale): Formal↔Casual, Enthusiastic↔Matter-of-fact, Respectful↔Irreverent, Serious↔Funny | Create language style guide (sentence structure, vocabulary level) | List 5 do's + 5 don'ts for messaging | Generate 10 example phrases in brand voice | **Gate**: Tone aligns with archetype, 5 adjectives consistent in 95% outputs

**5. VISUAL IDENTITY** (2-3min): Select color palette (primary + secondary + accent colors: HEX + RGB values, psychology rationale per color, WCAG contrast validation Level AA min) | Choose typography (primary + secondary fonts with fallbacks) | Generate 9 mood board prompts (3x3 grid for image generation) | Define visual style guidelines | **Gate**: ≥2 color pairs meet WCAG Level AA, colors aligned with archetype

**6. BRAND NARRATIVE** (3-4min): Write origin story (≥500 chars, compelling narrative) | Craft mission statement (100-150 chars, action-oriented) | Articulate vision statement (100-150 chars, aspirational) | Define 5 core values (defensible, non-generic, measurable) | Create brand manifesto (≥300 chars, emotional rallying cry) | Apply StoryBrand 7-element framework | **Gate**: Narrative harmony with values, Hero's Journey structure

**7. BRAND GUIDELINES** (1-2min): List 8-10 messaging do's (voice, claims, storytelling) | List 8-10 messaging don'ts (forbidden claims, clichés, tone violations) | Document compliance rules (ANVISA/INMETRO/CONAR specific to category) | Create consistency checklist (10 validation points) | **Gate**: Compliance rules match marketplace category

**8. VALIDATION & OUTPUT** (2-3min): Run Brand Fingerprint System validation (Purpose Specificity 10pts, Values Uniqueness 10pts, Seed Words Usage 10pts, Tone Consistency 10pts, Benchmark Differentiation 10pts) | Calculate Brand Consistency Score: (Checks Passed / Total Checks) × Quality Factor | Generate competitive audit (position vs 3 competitors) | Create integration notes for downstream agents | Format using brand_strategy_template.md | **Gate**: Consistency ≥0.85, Uniqueness ≥8.0/10

**Total Duration**: 10-20min (typical: 12-15min)

### Workflow (Execution Pattern)
```bash
# 1. Prepare brief
brief="Garrafa água reutilizável, ecológica, pessoas conscientes praticam esportes, 25-40 anos, R$ 89-129"

# 2. Execute brand creation (via OpenAI Agent Builder interface)
# Agent follows 8-step workflow automatically

# 3. Agent outputs brand_strategy.md to USER_DOCS/Marca/

# 4. Validate
uv run scripts/brand_validator.py USER_DOCS/Marca/garrafa_agua_brand_strategy.md

# Output:
# ✅ Brand Consistency Score: 0.87 (Excellent)
# ✅ Brand Uniqueness Score: 8.3/10 (Excellent)
# ✅ WCAG Compliance: 3 pairs pass Level AA
# ✅ Seed Words: 3 found in critical pieces
# ⚠️ Warning: Tagline 2 is 62 chars (max 60)
```

### Report (Output Structure)

**32 Structured Blocks in brand_strategy.md**:

**SECTION 1: BRAND IDENTITY**
1. Brand Names (3 options: descriptive, evocative, creative)
2. Taglines (3 options: 40-60 chars strict)
3. Brand Archetype (primary + secondary from 12)
4. Personality Traits (5 defining characteristics)
5. Brand Essence (one-sentence core identity)

**SECTION 2: POSITIONING**
6. Unique Value Proposition (differentiated promise)
7. Target Segment (demo + psycho + behavioral profile)
8. Competitive Differentiation (tangible + intangible factors)
9. Brand Promise (what customer can always expect)
10. Positioning Statement (Ries & Trout framework)

**SECTION 3: TONE OF VOICE**
11. Personality Dimensions (4 scales 1-5 each)
12. Language Style (vocabulary, sentence structure, patterns)
13. Messaging Do's (5-8 guidelines)
14. Messaging Don'ts (5-8 anti-patterns)
15. Example Phrases (10 in brand voice)

**SECTION 4: VISUAL IDENTITY**
16. Color Palette (primary + secondary + accent: HEX + RGB + psychology)
17. Typography (primary + secondary fonts with fallbacks)
18. Mood Board Prompts (9 prompts 3x3 grid)
19. Visual Style Guidelines (layout, imagery, design patterns)

**SECTION 5: BRAND NARRATIVE**
20. Origin Story (≥500 chars, compelling narrative)
21. Mission Statement (100-150 chars, action-oriented)
22. Vision Statement (100-150 chars, aspirational)
23. Core Values (5 values: defensible, non-generic)
24. Brand Manifesto (≥300 chars, emotional rallying cry)

**SECTION 6: BRAND GUIDELINES**
25. Messaging Do's (8-10 guidelines with examples)
26. Messaging Don'ts (8-10 forbidden patterns)
27. Compliance Rules (ANVISA/INMETRO/CONAR category-specific)
28. Consistency Checklist (10 validation points)

**SECTION 7: VALIDATION & AUDIT**
29. Brand Consistency Score (0-1 scale with breakdown)
30. Brand Uniqueness Score (0-10 scale with 5 dimensions)
31. Competitive Audit (position vs 3 competitors)
32. Integration Notes (use with anuncio/pesquisa agents)

**Quality Indicators**: ✅ Consistency ≥0.85 (excellent), ≥0.90 (exceptional) | ✅ Uniqueness ≥8.0/10 | ✅ All taglines 40-60 chars (strict) | ✅ WCAG Level AA: ≥2 color pairs pass | ✅ Seed words: ≥2 in critical pieces | ✅ Tone consistency: 5 adjectives in ≥95% outputs | ✅ Compliance complete for category | ✅ Values defensible + non-generic | ✅ Archetype ↔ tone alignment validated

---

## EXECUTION CONTEXT

### Input Requirements
**Minimum**: product name, category, target audience, price range
**Recommended**: marketplace target, competitors, brand inspirations, USPs
**Optional**: research_notes.md (from pesquisa_agent), cultural preferences

**Brief Quality Impact**:
- Minimal brief (4 fields): Agent asks 3-5 strategic questions, duration +2-3min
- Standard brief (6-8 fields): Normal execution, 10-15min
- Rich brief (10+ fields): Higher quality, nuanced brand, 12-20min

### Output Structure
```
USER_DOCS/Marca/
├── [produto]_brand_strategy.md      # Main strategy (30+ blocks)
├── [produto]_validation_report.txt  # Validation scores + recommendations
└── [produto]_metadata.json          # Execution metadata + quality scores
```

### Quality Gates (8 Critical Validations)
1. ✅ Identity ↔ Positioning alignment (archetype reinforces UVP)
2. ✅ Archetype ↔ Tone consistency (personality dimensions match archetype)
3. ✅ Visual ↔ Personality coherence (colors/fonts reflect archetype)
4. ✅ Narrative ↔ Values harmony (story embodies core values)
5. ✅ Compliance (ANVISA/INMETRO/CONAR rules for category)
6. ✅ WCAG Contrast (≥2 color pairs meet Level AA)
7. ✅ Seed Words (≥2 proprietary terms in critical pieces)
8. ✅ Tone Consistency (5 adjectives in ≥95% of outputs)

### Performance
**Time**: 10-20min (avg: 12-15min) | **Success Rate**: 92%+ with valid brief | **Quality Score**: ≥4.5/5 consistently | **Consistency Score**: 87% outputs achieve ≥0.85 | **Uniqueness Score**: 83% outputs achieve ≥8.0/10

### Integration
**Upstream**: User briefs, pesquisa_agent (market data for positioning validation - optional)
**Downstream**: anuncio_agent (uses brand_strategy.md for tone/guidelines/visual identity), pesquisa_agent (uses brand context for research - optional), USER_DOCS/Marca/ (centralized brand documentation)
**Parallel**: Compliance DBs (ANVISA/INMETRO/CONAR), design tools (mood boards, color palettes)
**Config**: Brand archetypes (updated with new variations), color psychology (synced with BR cultural research), compliance rules (updated quarterly for regulation changes)

---

## BEST PRACTICES

### For AI Assistants
1. **Validate brief quality**: Check minimum fields | If insufficient, prepare 3-5 strategic questions
2. **Choose marketplace context**: ML/Shopee (mass market, price-sensitive) | Amazon BR (quality focus, trust) | Magalu (family-oriented, established trust)
3. **Verify archetype compatibility**: `cat marca_agent/config/brand_archetypes.json | grep -A 10 "hero"`
4. **Validate color contrast**: Ensure WCAG Level AA (WebAIM Contrast Checker or automated validator)
5. **Check uniqueness**: Run validation after generation (`uv run scripts/brand_validator.py outputs/brand_strategy.md`)

### Pitfalls
❌ Reading all knowledge files at once → Use discovery commands
❌ Ignoring brief validation → Poor briefs = generic brands
❌ Skipping archetype compatibility → Inconsistent brand personality
❌ Not validating color contrast → Accessibility issues
❌ Ignoring consistency scores → Low scores = incoherent brand
❌ Generic values → "Inovação, Qualidade, Excelência" are too common

### Extensions
**New archetype**: Define in brand_archetypes.json (core desire, fears, strategy) → Add tone mapping to tone_taxonomies.json → Add color associations to color_psychology.json → Update MASTER_INSTRUCTIONS.md → Test with 3 sample briefs

**New positioning framework**: Document in positioning_frameworks.json → Add application examples to MASTER_INSTRUCTIONS.md → Create templates in COPYWRITING_TEMPLATES.md → Update validation logic in brand_validator.py

**Enrich BR cultural context**: Update color_psychology.json (BR-specific meanings) → Add regional preferences to tone_taxonomies.json → Document in BRAND_FINGERPRINT_SYSTEM.md → A/B test with Brazilian audience

**New marketplace**: Add policies to marketplace_policies.json → Update compliance rules in compliance_rules.json → Adjust archetype recommendations per marketplace culture → Test with category-specific briefs

---

## KEY FILES

**Core Instructions** (Enriched v1.1 - 12,500+ words):
- MASTER_INSTRUCTIONS.md (~10k words) - Main orchestrator with knowledge patterns, validation algorithms, Metamorfose methodology
- IMAGE_GENERATION_PROMPTS.md (~13k words) - Brand fidelity techniques, advanced prompt engineering, LUTs, governança
- BRAND_FINGERPRINT_SYSTEM.md (~9k words) - Uniqueness validation, experiments, Brazilian cultural context

**Configuration**:
- brand_archetypes.json - 12 archetypes (Hero, Sage, Innocent, Explorer, etc.)
- positioning_frameworks.json - Ries & Trout, Blue Ocean, Jobs-to-be-Done
- tone_taxonomies.json - Nielsen Norman Group 4-dimension taxonomy
- color_psychology.json - Color meanings + BR cultural context
- compliance_rules.json - ANVISA/INMETRO/CONAR regulations
- marketplace_policies.json - ML, Shopee, Magalu, Amazon BR rules
- storytelling_frameworks.json - StoryBrand, Hero's Journey, PAS, AIDA

**Templates**:
- OUTPUT_SCHEMA.md - JSON schema for brand_strategy.md outputs (includes BSB Complete JSON)
- BRAND_BRIEF_SCHEMA.json - Structured brief collection schema
- COPYWRITING_TEMPLATES.md - Ready-to-use copy templates + formulas
- brand_strategy_template.md - Markdown template for final output

**Documentation**:
- QUICK_START.md - 5-minute setup guide
- KNOWLEDGE_INTEGRATION_REPORT.md - +12,500 words enrichment documentation
- IMPROVEMENT_ANALYSIS.md - Gap analysis + roadmap to 9.0/10 maturity
- AGENT_CONFIGURATION.md - OpenAI Agent Builder setup instructions

---

## RELATED PRIMES
`/prime-anuncio` - Ad generation (uses brand_strategy.md for tone/guidelines) | `/prime-pesquisa` - Research (can provide market context for positioning) | `/prime-knowledge` - Knowledge management (brand insights + learnings)

---

## SHARED PRINCIPLES

> See full details: [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md)

### Tasks vs Roles (Sub-agents)
- ❌ "You are a branding expert" → ✅ "Extract brand archetype from these 5 adjectives"
- ❌ "Create a brand" → ✅ "Generate color palette for [archetype] + [industry]"

### Human Ownership (Before Delivery)
```markdown
- [ ] Brand values align with business goals
- [ ] Archetype selection justified
- [ ] Visual identity consistent across touchpoints
- [ ] Tone of voice examples are practical
- [ ] Competitor differentiation clear
```

### Value Function (Brand Confidence)
| Element | Confidence Check |
|---------|------------------|
| Archetype | Matches business personality? |
| Values | Authentic to founder? |
| Visual | Consistent palette + typography? |
| Voice | Clear examples for each tone? |

---

**Version**: 3.0.0
**Updated**: 2025-11-30
**Status**: Production Ready
**Architecture**: Dual-Layer ADW+HOP | 5-Phase SDLC
**12 Leverage Points**: Fully Implemented
**Integration**: anuncio_agent, pesquisa_agent, USER_DOCS/Marca/

**Changelog v3.0.0** (2025-11-30):
- iso_vectorstore optimization (ADW-104 v2.1.0): 33 → 20 files, -58% tokens
- HOPs optimized: 13 (~6k → ~700 tokens), 14 (~6k → ~800 tokens)
- Created 00_MANIFEST.md and SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md
- Applied lessons learned (8.5-8.8 patterns)
- Version consistency enforced across all files

**Changelog v2.5.0** (2025-11-25):
- Full 12 Leverage Points implementation
- 5-phase SDLC: Plan -> Build -> Test -> Review -> Document
- Task boundaries for phase visibility
- New files: 06_input_schema.json, 07_output_template.md, 08_brand_rules.json, 09_archetype_specs.json, 10_identity_patterns.json, 11_ADW_orchestrator.md, 12_execution_plans.json
- Trinity output format: .md + .llm.json + .meta.json
