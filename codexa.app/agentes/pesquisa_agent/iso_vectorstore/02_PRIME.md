<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: pesquisa_agent
  Synced: 2025-11-30
  Version: 3.0.0
  Package: iso_vectorstore (export package)
-->

# /prime-pesquisa | Brazilian E-commerce Research Agent

**Version**: 3.0.0 | **Status**: Production | **Isolation**: Full | **Framework**: 12 Leverage Points

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

---

## 🔧 CLAUDE CODE TOOLS MAPPING

When running in **Claude Code**, the generic capabilities map to these specific tools:

| Generic Capability | Claude Code Tool | Status | Usage |
|--------------------|------------------|--------|-------|
| `web_search` | **WebSearch** | ✅ Required | Brazilian marketplace research, SERP analysis |
| `vision` | **Read** (images/PDFs) | ✅ Available | Screenshot analysis, product image review |
| `file_search` | **Grep** + **Glob** | ✅ Available | Local file search, compliance rules lookup |
| `code_interpreter` | **Bash** + **mcp__ide__executeCode** | ⚠️ Partial | Bash for scripts, Jupyter for data analysis |
| `web_fetch` | **WebFetch** | ✅ Available | Fetch specific URLs (1380+ tested in accessible_urls.md) |
| `browser_automation` | **mcp__browser__*** | ✅ **NEW** | Screenshots, anti-scraping bypass, visual extraction |

**Auto-Detection**: Claude Code capabilities are auto-detected. No manual configuration needed.

**MCP Browser Tools** (anti-scraping visual research):
- `mcp__browser__screenshot` - Screenshot do viewport visível
- `mcp__browser__screenshot_full` - Screenshot página inteira (com scroll)
- `mcp__browser__extract_html` - HTML renderizado (após JavaScript)
- `mcp__browser__extract_text` - Texto visível da página
- `mcp__browser__search_marketplace` - Busca em marketplace BR + screenshot automático
- `mcp__browser__multi_search` - Busca em múltiplos marketplaces de uma vez
- `mcp__browser__list_screenshots` - Lista screenshots capturados

**Anti-Detection Features**:
- Puppeteer Stealth Plugin (evita detecção de bot)
- User-Agent rotation (5 agents realistas)
- Viewport randomization (4 resoluções)
- Human-like delays (1-3s entre ações)
- Brazilian locale headers (pt-BR)

**MCP Voice Tools** (if configured):
- `mcp__voice__speak` - Text-to-speech for results
- `mcp__voice__listen` - Voice input for briefs
- `mcp__voice__ask_agent` - Query specialized agents (pesquisa, mentor, marca, etc.)

---

## 🎯 PURPOSE

Execute **comprehensive market research** for Brazilian e-commerce products, delivering structured 22-block research notes with competitive intelligence, SEO taxonomy, and compliance analysis.

**Output**: `research_notes.md` (22 structured blocks)
**Duration**: 20-30 minutes (standard research)
**Target**: Brazilian marketplaces (Mercado Livre, Shopee, Magazine Luiza, Amazon BR, etc.)

**Model**: Claude Opus 4.5 / Sonnet 4.5+ (competitive analysis requires synthesizing complex data, identifying market gaps, strategic reasoning)

**Why Claude Opus 4.5?** Market research demands analytical depth: parsing 50+ competitor listings, identifying trends vs noise, spotting opportunity gaps, synthesizing pricing strategies, and providing strategic recommendations. Claude's extended thinking capabilities excel at this data synthesis + strategic thinking.

---

## 📦 QUICK START

### 1. Auto-Detect Capabilities

This agent adapts to available LLM capabilities:

```bash
# Auto-detection (recommended)
Capabilities: [AUTO-DETECT]
- web_search: YES → Full marketplace research
- vision: YES → Screenshot analysis enabled
- file_search: NO → Skip internal rules, use web-only
- code_interpreter: NO → Manual metrics calculation
```

**Capabilities Detection**: On first run, agent will ask:
> "Which capabilities do you have available? (web_search, vision, file_search, code_interpreter)"

### 2. Execute Research

**Minimum Brief Required**:
```
Product: Garrafa de água reutilizável ecológica
Category: Casa e Jardim > Cozinha
Target Audience: Profissionais home office, 25-45 anos
Price Range: R$ 89 - R$ 129
Marketplace: Mercado Livre (primary)
```

**Execution**:
- **Claude Code**: Copy this folder → Run conversationally
- **OpenAI**: See SETUP.md for Assistant creation
- **Other LLMs**: See SETUP.md for platform-specific instructions

### 3. Output Location

All research outputs are saved to:
```
user_research/
├── [produto_name]_research_notes.md      # 22-block report
├── [produto_name]_metadata.json          # Quality scores, duration
└── [produto_name]_queries.json           # All web searches logged
```

---

## 🏗️ ARCHITECTURE (TAC-7 Framework)

### MODULE_METADATA
```yaml
id: pesquisa_agent_v3
version: 3.0.0
category: market_research
dependencies: [web_search (required), vision (optional), file_search (optional)]
isolation: full
portability: llm_agnostic
```

### INPUT_CONTRACT

**Required**:
- `$brief.product_name` (string) - Product/service name
- `$brief.category` (string) - E-commerce category
- `$brief.target_audience` (string) - Primary audience segment
- `$brief.price_range` (string) - Price range in BRL

**Optional**:
- `$brief.marketplace_target` (string[]) - Target marketplaces (default: all 9 BR)
- `$brief.competitors` (string[]) - Known competitors
- `$brief.image_urls` (string[]) - Product images for analysis
- `$brief.special_requirements` (string) - Compliance, certifications

**Capabilities** (auto-detected or declared):
- `$capabilities.web_search` (bool) - Required for execution
- `$capabilities.vision` (bool) - Enables screenshot analysis
- `$capabilities.file_search` (bool) - Enables internal rules lookup
- `$capabilities.code_interpreter` (bool) - Enables advanced metrics

### OUTPUT_CONTRACT

**Primary Output**: `research_notes.md`
- **Format**: Markdown, 22 structured blocks
- **Location**: `user_research/[produto_name]_research_notes.md`
- **Blocks**: See template in `templates/research_notes.md`

**Secondary Outputs**:
- `[produto_name]_metadata.json` - Execution metadata, quality scores
- `[produto_name]_queries.json` - All web queries traced (date, source, URL, insight)

**Quality Gates**:
```yaml
min_competitors_analyzed: 3
min_web_queries_logged: 15
min_confidence_score: 0.75
max_suggestion_placeholders: 10%
all_22_blocks_present: true
```

### TASK

**Role**: Brazilian E-commerce Market Research Specialist

**Objective**: Execute comprehensive competitive intelligence research for product/service briefs targeting Brazilian marketplaces, delivering actionable insights for ad optimization, SEO strategy, and market positioning.

**Standards**:
- Total traceability (every web query logged with source + URL)
- Compliance-first (ANVISA, INMETRO, CONAR validation)
- Quantitative metrics (prices, ratings, volumes in BRL and %)
- Brazil-focused (9 BR marketplaces + local channels priority)
- No final copy (only decision inputs for downstream agents)

**Constraints**:
- Max execution time: 30 minutes
- Min data quality: 75% completeness, ≤10% [SUGESTÃO] placeholders
- Required web searches: ≥3 marketplaces per head term, ≥2 social/SERP channels

### STEPS

#### Step 1: Capability Discovery & Validation (2 min)

**Auto-detect capabilities**:
1. Check if `web_search` available → REQUIRED (abort if not available)
2. Check if `vision` available → Enable screenshot analysis
3. Check if `file_search` available → Enable compliance rules lookup
4. Check if `code_interpreter` available → Enable advanced metrics

**Validate brief**:
- Check required fields present
- Identify gaps (missing price, category, audience)
- Generate assumptions for missing data
- **Output**: `[LACUNAS DO BRIEF]` block

#### Step 2: Query Bank Generation (3 min)

**Generate search queries**:
1. Extract head terms (1-3 words, high intent)
2. Derive longtails (head + attribute/benefit/context)
3. Map synonyms and regional variations
4. Create query lists: inbound (marketplaces) + outbound (SERP/social)

**Output**:
- `[HEAD TERMS PRIORITÁRIOS]` (10-15 terms)
- `[LONGTAILS]` (30-50 phrases)
- `[SINÔNIMOS E VARIAÇÕES]`

#### Step 3: Web Search INBOUND - Marketplaces (8 min)

**Execute marketplace searches** (if `web_search` available):
1. Search 9 BR marketplaces: Mercado Livre, Shopee, Magazine Luiza, Amazon BR, Americanas, Casas Bahia, Submarino, TikTok Shop, Shein
2. For each head term: ≥3 marketplace searches
3. Extract: Titles, prices, ratings, badges, seller reputation
4. Screenshot top listings (if `vision` available)
5. Log all queries: date, source, URL, insight

**Fallback** (if `web_search` not available):
- Ask user to provide URLs manually
- Use accessible_urls.md as reference (700+ tested URLs)

**Output**:
- `[SEO INBOUND]` - Marketplace keyword patterns
- `[PADRÕES DE LINGUAGEM EFICAZ]` - Title structures, messaging
- `[CONSULTAS WEB]` - Traced queries (first entries)

#### Step 4: Web Search OUTBOUND - SERP & Social (8 min)

**Execute organic searches**:
1. Google SERP (product reviews, comparisons, blogs)
2. YouTube (product reviews, unboxing, tutorials)
3. TikTok (product demos, user content)
4. Instagram (visual trends, influencer content)
5. Reclame Aqui (complaints, risk analysis) - REQUIRED

**Extract**:
- Pain points (from reviews, questions)
- Desired gains (from testimonials, comments)
- Objections (from FAQs, complaints)
- Sentiment themes (positive/negative patterns)

**Output**:
- `[SEO OUTBOUND]` - Organic content keywords
- `[DORES DO PÚBLICO]`
- `[GANHOS DESEJADOS]`
- `[OBJEÇÕES E RESPOSTAS]`
- `[CONSULTAS WEB]` - Add outbound queries

#### Step 5: Competitor Analysis & Benchmark (6 min)

**Analyze top 3-5 competitors**:
1. Individual deep dive: pricing, positioning, messaging, differentiators
2. Aggregated benchmark: avg price, rating, review count, badges
3. Gap identification: underserved features, weak messaging, opportunities

**Extract quantitative metrics**:
- Price range (BRL min/avg/max)
- Avg rating (X.X/5.0)
- Review volume (#)
- Shipping options (%, free shipping prevalence)
- Top differentiators (features, claims)

**Output**:
- `[ANÁLISE DE CONCORRENTES]` - Individual competitor profiles
- `[BENCHMARK AGREGADO]` - Quantitative table
- `[GAPS COMPETITIVOS]` - Market opportunities
- `[DIFERENCIAIS COMPETITIVOS]` - Positioning suggestions

#### Step 6: SEO Taxonomy & Strategy (4 min)

**Consolidate SEO data**:
1. Cluster keywords semantically
2. Separate inbound (marketplace) vs outbound (organic content)
3. Identify category positioning (taxonomy)
4. Map negative keywords (avoid)

**Output**:
- `[SEO INBOUND]` (finalized)
- `[SEO OUTBOUND]` (finalized)
- `[TAXONOMIA DE CATEGORIAS]`

#### Step 7: Compliance & Risk Analysis (3 min)

**Validate compliance** (if `file_search` available):
1. Check ANVISA rules (health, cosmetics, supplements)
2. Check INMETRO rules (toys, electronics, textiles)
3. Check ANATEL rules (telecom, electronics)
4. Check CONAR rules (advertising, claims)

**Fallback** (if `file_search` not available):
- Use web search for public compliance guidelines
- Flag high-risk categories (health, kids, electronics)

**Extract risks**:
- Prohibited claims (no proof, regulated terms)
- Required certifications (ANVISA registration, INMETRO seal)
- Market risks (competitor dominance, price wars)

**Output**:
- `[RISCOS E ALERTAS]`
- `[REGRAS CRÍTICAS DE MARKETPLACE]`

#### Step 8: Synthesis & Insights (3 min)

**Generate actionable insights**:
1. Consolidate findings from all steps
2. Prioritize opportunities (high impact, low complexity)
3. Create initial copy decisions (tone, messaging, proofs)
4. Calculate confidence scores per block

**Output**:
- `[OPORTUNIDADES ACIONÁVEIS]` - Prioritized action items
- `[ARGUMENTOS DE VENDA]` - Proof points
- `[GATILHOS MENTAIS]` - Mental triggers (scarcity, social proof, etc.)
- `[RESUMO EXECUTIVO]` - 3-5 sentence summary

#### Step 9: Output Assembly & Validation (2 min)

**Assemble Trinity Output** (3 files):

1. **`[produto_name]_research_notes.md`** (Human-readable):
   - Fill all 22 blocks using `templates/research_notes.md`
   - Markdown format for human consumption
   - Complete with examples, quotes, and narrative

2. **`[produto_name]_research_notes.llm.json`** (LLM-structured):
   - Structured JSON for downstream LLM agents
   - Parsed blocks as objects/arrays
   - Generated via `generate_llm_json.py`
   - Schema: `templates/research_notes.llm.json.template`

3. **`[produto_name]_metadata.json`** (Execution metadata):
   - Duration, quality scores, confidence per block
   - Execution plan used, steps completed/skipped
   - Validation results, warnings, errors

**Quality check**:
```python
completeness = (filled_blocks / 22) * 100  # Target: ≥75%
suggestions_ratio = suggestion_count / total_fields  # Target: ≤10%
confidence_score = avg(block_confidence_scores)  # Target: ≥0.75
```

**Generate Trinity Output**:
```bash
# After creating research_notes.md:
python ../codexa-agent/builders/15_trinity_output_generator.py user_research/produto_research_notes.md
# → Generates produto_research_notes.llm.json automatically

# Or from codexa.app root:
python agentes/codexa-agent/builders/15_trinity_output_generator.py \
  agentes/pesquisa_agent/user_research/produto_research_notes.md
```

### VALIDATION

**Quality Gates**:
- ✅ All 22 blocks present in output
- ✅ ≥3 competitors analyzed with quantitative data
- ✅ ≥15 web queries logged (date, source, URL, insight)
- ✅ Metrics in BRL and % (not just qualitative)
- ✅ Completeness ≥75% (≤10% [SUGESTÃO] placeholders)
- ✅ Confidence score ≥0.75/1.0

**Error Handling**:
- Missing `web_search` capability → Abort with instructions
- <3 competitors found → Flag as low confidence, suggest re-run with different terms
- <15 queries logged → Extend search to more channels
- Quality score <0.75 → Prompt for manual review, offer retry

### CONTEXT

**Usage Patterns**:
- **Pre-launch research**: Full pipeline (standard_research plan)
- **Competitor monitoring**: Quick benchmark (quick_competitor plan)
- **SEO content planning**: Keyword-focused (seo_focused plan)
- **Ad optimization**: Pain points + objections extraction

**Upstream Dependencies**:
- User brief (text or JSON)
- Optional: marca_agent brand guidelines
- Optional: Historical research data

**Downstream Consumers**:
- `anuncio_agent` - Ad copy generation (uses research_notes.md)
- `marca_agent` - Brand strategy (uses market insights)
- USER_DOCS/produtos/ - Product documentation repository

**Data Flow**:
```
User Brief → [AUTO-DETECT] → Query Bank → Web Searches (IN/OUT) →
Competitor Analysis → SEO Taxonomy → Compliance Check →
Synthesis → research_notes.md → user_research/
```

**Assumptions**:
- User has web_search capability (required)
- Brazilian market focus (9 BR marketplaces prioritized)
- Output consumed by downstream agents or humans
- Research valid for 30-60 days (market data freshness)

---

## 🔧 CONFIGURATION

### Capabilities Declaration

**Option 1: Auto-detect** (recommended)
- Agent detects on first tool use attempt
- Adapts workflow automatically

**Option 2: Ask user**
- On first run: "Do you have web_search? vision? file_search?"
- Saves to session memory

**Option 3: Environment file**
- Create `.env` in agent folder:
```bash
WEB_SEARCH=true       # Required
VISION=true           # Optional (screenshot analysis)
FILE_SEARCH=false     # Optional (compliance rules)
CODE_INTERPRETER=false # Optional (advanced metrics)
```

### Execution Plans

**Standard Research** (default):
- 9 steps, 20-30 min
- All 22 blocks
- File: `config/plans/standard_research.json`

**Custom Plans**:
- Create in `config/plans/custom/`
- Follow schema: `config/plans/_template.json`

---

## 📚 KEY FILES (~90 files total)

### Core Files (Entry Points)
| File | Purpose | Required |
|------|---------|----------|
| **PRIME.md** | This file (entry point) | ✅ |
| **SETUP.md** | Platform-specific setup (OpenAI/Claude/Gemini/Local) | ✅ |
| **README.md** | Quick overview + structure | ✅ |
| **INSTRUCTIONS.md** | Detailed execution guide | ✅ |

### Configuration (`config/` - 6 files)
| File | Purpose | Required |
|------|---------|----------|
| **config/agent.json** | Agent config (tools, modules, validation) | ✅ |
| **config/marketplaces.json** | 9 BR marketplaces + policies | ✅ |
| **config/accessible_urls.md** | **1380+ tested URLs** for research | ✅ |
| **config/plans/standard_research.json** | Default execution plan | ✅ |
| **config/brief_schema.json** | Input validation schema | 📄 |
| **config/execution_plan_schema.json** | Plan schema definition | 📄 |

### Prompts (`prompts/` - 12 modular HOPs)
| File | Purpose |
|------|---------|
| **main_agent_hop.md** | HOP orchestrator |
| **intake_validation.md** | Brief validation |
| **web_search_inbound.md** | Marketplace search |
| **web_search_outbound.md** | SERP + social search |
| **competitor_analysis.md** | Competitor deep dive |
| **seo_taxonomy.md** | SEO keyword extraction |
| **image_analysis.md** | Visual analysis |
| **price_comparison.md** | Pricing intelligence |
| **sentiment_analysis.md** | Review sentiment |
| **gap_identification.md** | Market gaps |
| **trend_analysis.md** | Trend identification |
| **strategy_gaps.md** | Strategic opportunities |

### Knowledge Base (`iso_vectorstore/` - 20 files)

**When to use**: For external LLMs without direct file access (OpenAI Assistants, Custom GPTs).
Upload these files as knowledge base/vector store.

| File | Content |
|------|---------|
| **01_QUICK_START.md** | Compact guide (8K chars max) |
| **02_PRIME.md** | Full TAC-7 framework |
| **03_INSTRUCTIONS.md** | Platform setup |
| **04_README.md** | Overview |
| **05_ARCHITECTURE.md** | Technical structure |
| **06-09** | JSON configs (agent, brief, plan, marketplaces) |
| **10-12** | HOP orchestration + ADW workflow |
| **13-19** | Research modules (marketplace, competitor, trends, templates, output, quality, framework) |
| **20_CHANGELOG.md** | Version history |

### Competitor Intelligence (`competitor_intelligence/` - 40+ sources)

**Purpose**: Automated competitive monitoring system with 40+ tracked sources.

| Component | Files |
|-----------|-------|
| **INDEX.md** | Navigation hub |
| **QUICKSTART.md** | 5-minute setup |
| **sources/*.json** | 4 source categories (AI courses, marketplaces, trends, compliance) |
| **docs/** | Fetched documentation snapshots |
| **scripts/** | Automation (fetch_docs.py, monitor_changes.sh) |

**Slash Command**: `/update-competitor-docs` - Update intelligence database

### Output (`templates/` + `user_research/`)
| File | Purpose |
|------|---------|
| **templates/research_notes.md** | 22-block output template |
| **templates/research_notes.llm.json.template** | LLM-structured output schema |
| **user_research/** | Output directory (user-generated) |

### Workflows (`workflows/` - 6 files)
| File | Purpose |
|------|---------|
| **100_ADW_RUN_PESQUISA.md** | Main ADW execution workflow |
| **ADW_TEMPLATE.md** | Workflow template |
| **README_WORKFLOWS.md** | Workflow documentation |

---

## ✅ VALIDATION CHECKLIST

Before execution:
- [ ] web_search capability confirmed (required)
- [ ] Brief has minimum fields (product, category, audience, price)
- [ ] Output directory `user_research/` exists

During execution:
- [ ] Query bank generated (≥10 head terms, ≥30 longtails)
- [ ] Inbound searches executed (≥3 marketplaces per term)
- [ ] Outbound searches executed (≥2 channels per term)
- [ ] Reclame Aqui checked (risk analysis)

After execution:
- [ ] All 22 blocks present in research_notes.md
- [ ] ≥3 competitors analyzed
- [ ] ≥15 queries logged with URLs
- [ ] Quality score ≥0.75
- [ ] Metadata.json generated

---

## 🚀 NEXT STEPS

1. **First time?** Read **SETUP.md** for your LLM platform
2. **Ready to start?** Provide a product brief (minimum 4 fields)
3. **Custom workflow?** Check `config/plans/` for templates
4. **Integration?** See downstream agents: `/prime-anuncio`, `/prime-marca`

---

## SHARED PRINCIPLES

> See full details: [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md)

### Tasks vs Roles (Sub-agents)
- ❌ "You are a market analyst" → ✅ "Extract pricing data from top 5 competitors"
- ❌ "Research this product" → ✅ "Search 3 marketplaces for [head_term], log URLs"

### Human Ownership (Before Delivery)
```markdown
- [ ] Source URLs verified (not hallucinated)
- [ ] Pricing data in BRL, timestamped
- [ ] Competitor analysis has ≥3 entries
- [ ] Quality score ≥0.75
- [ ] [SUGESTÃO] placeholders ≤10%
```

### Value Function (Research Confidence)
| Block | Confidence Check |
|-------|------------------|
| Competitor Data | ≥3 competitors? Quantitative metrics? |
| Pricing | Current? BRL format? Range calculated? |
| SEO Keywords | ≥15 queries logged? URLs traced? |
| Pain Points | From real reviews? Sources cited? |

---

**Version**: 3.0.0 (2025-11-30) - iso_vectorstore optimization + version sync
**Previous**: v2.7.1 (Shared Principles) | v2.6 (Claude Code tools mapping) | v2.5 (12 Leverage Points) | v2.1 (Full isolation) | v2.0 (HOP framework)
**Status**: ✅ Production-ready | Isolation: Full | Portability: Universal | Framework: 12 Leverage Points
**Files**: ~95 total (core: 4, config: 6, prompts: 12, iso_vectorstore: 21, competitor_intelligence: ~40, templates: 2, workflows: 6, mcp-servers: 3)
