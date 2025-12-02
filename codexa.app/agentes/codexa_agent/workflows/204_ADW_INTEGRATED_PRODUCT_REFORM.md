# 204_ADW_INTEGRATED_PRODUCT_REFORM | Pesquisa + Anuncio + Sync Pipeline

**Purpose**: End-to-end automated product reform (research → ad copy → Shopify sync)
**Type**: 5-Phase Integrated ADW | **Duration**: ~45-60min per product (batch: ~15min/product with parallelization)
**Output**: research_notes.md + anuncio.md + anuncio.json + Shopify sync + consolidated report
**Architecture**: Orchestration Layer (coordinates pesquisa_agent + anuncio_agent + sync_script)
**Status**: Production-Ready | **Version**: 1.0.0

---

## MODULE_METADATA

```yaml
id: 204_ADW_INTEGRATED_PRODUCT_REFORM
version: 1.0.0
category: orchestration-workflows
type: ADW (Agentic Developer Workflow)
execution_mode: batch_orchestration
dependencies:
  - pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md
  - anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md
  - anuncio_agent/scripts/sync_all_shopify.py
  - anuncio_agent/plans/full_anuncio.json
status: production_ready
created: 2025-11-29
platform_patterns:
  - Devin: batch processing, checkpoint resume
  - Claude Code: MCP integration, task boundaries
  - Cursor: research-first approach
  - Poke: parallel product processing
  - Windsurf: quality gates, defensive sync
mcp_requirements:
  - mcp__browser__search_marketplace
  - mcp__browser__extract_text
  - mcp__scout__discover
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_integrated_product_reform",
  "workflow_name": "Integrated Product Reform Pipeline",
  "version": "1.0.0",
  "orchestrates": ["pesquisa_agent", "anuncio_agent", "sync_shopify"],
  "context_strategy": "product_scoped",
  "failure_handling": "continue_batch_report_failures",
  "min_llm_model": "claude-sonnet-4+ or gpt-4o",

  "required_capabilities": {
    "web_search": true,
    "browser_mcp": true,
    "file_write": true,
    "supabase_api": true
  },

  "batch_config": {
    "max_parallel_products": 3,
    "rate_limit_ms": 1000,
    "checkpoint_interval": 5
  },

  "phases": [
    {
      "phase_id": "phase_0_knowledge",
      "phase_name": "Knowledge Loading",
      "duration": "1-2min",
      "module": "PHASE_0_KNOWLEDGE_LOADING",
      "task_hint": "product_reform"
    },
    {
      "phase_id": "phase_1_discovery",
      "phase_name": "Product Discovery & Queue Setup",
      "duration": "2-5min",
      "description": "Fetch product list from Supabase, prioritize, create processing queue"
    },
    {
      "phase_id": "phase_2_research",
      "phase_name": "Competitive Research (per product)",
      "duration": "8-15min/product",
      "description": "Browser MCP marketplace search + extract competitor data"
    },
    {
      "phase_id": "phase_3_generation",
      "phase_name": "Ad Copy Generation (per product)",
      "duration": "10-15min/product",
      "description": "Execute anuncio_agent full_anuncio plan with research context"
    },
    {
      "phase_id": "phase_4_validation",
      "phase_name": "Quality Validation (per product)",
      "duration": "2-3min/product",
      "description": "11-criteria QA check + compliance validation"
    },
    {
      "phase_id": "phase_5_sync",
      "phase_name": "Shopify Sync & Batch Report",
      "duration": "1-2min/product + 5min report",
      "description": "Push to Shopify via Edge Function + generate consolidated report"
    }
  ]
}
```

---

## PREREQUISITES

**Before starting, ensure:**

1. **Environment Variables**:
   ```bash
   SUPABASE_URL=https://fuuguegkqnpzrrhwymgw.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=<service_key>  # Required for sync
   ```

2. **MCP Servers Available**:
   - `mcp__browser__search_marketplace` (for competitive research)
   - `mcp__browser__extract_text` (for page analysis)
   - `mcp__scout__discover` (for file discovery)

3. **Agent Context Loaded**:
   - `pesquisa_agent/PRIME.md` (research methodology)
   - `anuncio_agent/PRIME.md` (ad generation rules)
   - `anuncio_agent/config/copy_rules.json` (compliance)
   - `anuncio_agent/config/marketplace_specs.json` (platform limits)

4. **Output Directories**:
   - `USER_DOCS/produtos/research/` (research notes)
   - `USER_DOCS/produtos/anuncios/` (generated ads)
   - `USER_DOCS/produtos/reports/` (batch reports)

---

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `product_reform`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

## PHASE 1: Product Discovery & Queue Setup

**Objective**: Fetch products, prioritize, create processing queue

**Task Boundary Declaration**:
```
TASK_BOUNDARY: DISCOVERY
AGENT: orchestrator
ACCESS: read_only (Supabase API)
SCOPE: Fetch product list and create processing queue
```

**Actions**:

1. **Fetch product list from Supabase**:
   ```python
   # Using sync_all_shopify.py pattern
   api_url = f"{SUPABASE_URL}/rest/v1/products?select=id,name,category,shopify_product_id,updated_at&order=updated_at.asc"
   ```

2. **Filter products needing reform**:
   - No research_notes.md exists
   - No anuncio.json exists
   - Last sync > 30 days ago
   - Quality score < 0.85 (if available)

3. **Prioritize queue**:
   - Priority 1: Products with sales but low conversion
   - Priority 2: Products with no ad copy
   - Priority 3: Products with outdated research (> 60 days)

4. **Create processing checkpoint**:
   ```json
   {
     "batch_id": "reform_2025-11-29_001",
     "total_products": 22,
     "processed": 0,
     "queue": ["product_id_1", "product_id_2", ...],
     "status": "initialized"
   }
   ```

**Input**:
- Supabase API credentials
- Optional: `--product-ids` filter (specific products)
- Optional: `--limit` (max products to process)

**Output**:
- `$product_queue` (array of product objects)
- `$batch_checkpoint` (checkpoint file for resume)

**Validation**:
- [ ] Supabase connection successful
- [ ] At least 1 product found
- [ ] Checkpoint file created

---

## PHASE 2: Competitive Research (Per Product)

**Objective**: Gather marketplace intelligence using Browser MCP

**Task Boundary Declaration**:
```
TASK_BOUNDARY: RESEARCH
AGENT: pesquisa_agent (via orchestrator)
ACCESS: read_only (Browser MCP + web search)
SCOPE: Search marketplaces and extract competitor data
LOOP: For each product in queue
```

**For each product in queue, execute:**

### Step 2.1: Marketplace Search (Browser MCP)

```javascript
// Using mcp__browser__search_marketplace
const marketplaces = ["mercadolivre", "shopee", "amazon", "magazineluiza"];
const results = [];

for (const marketplace of marketplaces) {
  const search = await mcp__browser__search_marketplace({
    marketplace: marketplace,
    query: product.name + " " + product.category
  });
  results.push(search);
}
```

### Step 2.2: Extract Competitive Data

From each marketplace result, extract:

| Data Point | Source | Priority |
|------------|--------|----------|
| Competitor titles | Search results | HIGH |
| Price range (min/avg/max) | Listings | HIGH |
| Top keywords in titles | NLP extraction | HIGH |
| Rating averages | Stars/reviews | MEDIUM |
| Shipping patterns | Free/paid, speed | MEDIUM |
| Image styles | Visual analysis | LOW |

### Step 2.3: Generate Research Notes

Create lightweight `research_notes.md` with essential blocks:

```markdown
# Research Notes: [Product Name]
**Generated**: [timestamp]
**Marketplaces Searched**: 4
**Competitors Found**: [count]

## [HEAD TERMS PRIORITARIOS]
1. [term 1] - volume alto
2. [term 2] - volume medio
...

## [BENCHMARK DE CONCORRENTES]
| Concorrente | Preco | Rating | Reviews | Frete |
|-------------|-------|--------|---------|-------|
| [name 1]    | R$XX  | 4.5    | 1234    | Gratis|
...

## [DORES DO PUBLICO]
- [pain point 1 from reviews]
- [pain point 2]
...

## [DIFERENCIAIS COMPETITIVOS]
- [opportunity 1]
- [opportunity 2]
...
```

**Input**:
- `$product` (current product from queue)
- Browser MCP capabilities

**Output**:
- `$research_notes` (markdown file)
- `$competitive_data` (structured JSON)

**Validation**:
- [ ] At least 3 marketplaces searched
- [ ] At least 3 competitors found
- [ ] Price data extracted (BRL)
- [ ] research_notes.md saved

**Error Handling**:
- If marketplace search fails → retry with alternative query
- If < 3 competitors → flag LOW_DATA, continue with available
- If all searches fail → skip product, log error, continue batch

---

## PHASE 3: Ad Copy Generation (Per Product)

**Objective**: Generate optimized ad copy using anuncio_agent

**Task Boundary Declaration**:
```
TASK_BOUNDARY: GENERATION
AGENT: anuncio_agent (via orchestrator)
ACCESS: write (file system for outputs)
SCOPE: Execute full_anuncio plan and generate Trinity output
LOOP: For each product with completed research
```

**Execute full_anuncio plan with research context:**

### Step 3.1: Load Research Context

```python
# Inject research into anuncio_agent
context = {
  "research_notes_path": f"USER_DOCS/produtos/research/{product_name}_research_notes.md",
  "marketplace": "mercado_livre",  # Primary target
  "product_type": detect_product_type(product),
  "competitive_data": research_phase_output
}
```

### Step 3.2: Execute Generation Steps

Follow `full_anuncio.json` plan (11 steps):

| Step | Module | Duration | Output |
|------|--------|----------|--------|
| 1 | 10_main_agent_hop.md | 2min | Strategic brief |
| 2 | 20_titulo_generator.md | 2min | 3 title variations |
| 3 | 30_keywords_expander.md | 2min | 2 keyword blocks |
| 4 | 40_bullet_points.md | 3min | 10 bullet points |
| 5 | 50_descricao_builder.md | 3min | Long description |
| 6 | 60_image_prompts.md | 2min | 9 image prompts |
| 7 | 70_video_script.md | 2min | Video storyboard |
| 8 | 80_seo_metadata.md | 2min | SEO data |
| 9 | 85_variacoes_s5.md | 2min | 3 A/B variants |
| 10 | 90_qa_validation.md | 2min | QA report |
| 11 | output_assembly | 1min | Final package |

### Step 3.3: Generate Trinity Output

Save to `USER_DOCS/produtos/anuncios/{product_name}/`:
- `{product_name}_anuncio.md` (human-readable)
- `{product_name}_anuncio.json` (structured for API)
- `{product_name}_anuncio.meta.json` (workflow metadata)

**Input**:
- `$research_notes` (from Phase 2)
- `$product` (product data)
- anuncio_agent HOP prompts

**Output**:
- `$anuncio_package` (Trinity output)
- `$quality_score` (0.0-1.0)

**Validation**:
- [ ] All 11 steps completed
- [ ] Title within char limits (58-60 for ML)
- [ ] Description >= 3300 chars
- [ ] Keywords >= 60 total
- [ ] No forbidden words detected

---

## PHASE 4: Quality Validation (Per Product)

**Objective**: Validate against 11 QA criteria before sync

**Task Boundary Declaration**:
```
TASK_BOUNDARY: VALIDATION
AGENT: verification_agent
ACCESS: read_only (validate outputs)
SCOPE: Run 11-criteria QA check and determine sync approval
LOOP: For each product with generated ad copy
```

**QA Checklist (from 90_qa_validation.md):**

| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 1 | Title char count | 58-60 chars (ML) | 10% |
| 2 | Title keyword density | >= 0.70 | 10% |
| 3 | Title no forbidden words | 0 violations | 10% |
| 4 | Keywords total count | >= 60 | 10% |
| 5 | Keywords coverage | >= 80% head terms | 5% |
| 6 | Description length | >= 3300 chars | 10% |
| 7 | Description keyword density | 2-5% | 5% |
| 8 | Bullet points count | 10 bullets | 10% |
| 9 | Bullet points char length | 250-299 each | 5% |
| 10 | Compliance check | PASS | 15% |
| 11 | Research backing | >= 3 competitors | 10% |

**Quality Score Calculation**:
```python
quality_score = sum(criterion.passed * criterion.weight for criterion in qa_checks)
# Threshold: >= 0.85 to proceed to sync
# 0.70-0.84: WARN, manual review suggested
# < 0.70: FAIL, do not sync
```

**Input**:
- `$anuncio_package` (from Phase 3)
- `$research_notes` (from Phase 2)
- QA configuration

**Output**:
- `$qa_report` (detailed validation results)
- `$sync_approved` (boolean)
- `$improvement_suggestions` (if score < 0.95)

**Validation**:
- [ ] All 11 criteria evaluated
- [ ] Score calculated
- [ ] Sync decision made

---

## PHASE 5: Shopify Sync & Batch Report

**Objective**: Push approved products to Shopify + generate consolidated report

**Task Boundary Declaration**:
```
TASK_BOUNDARY: SYNC_AND_REPORT
AGENT: execution_agent
ACCESS: write (Shopify API + file system)
SCOPE: Push approved products and generate batch report
FINAL_PHASE: true
```

### Step 5.1: Sync to Shopify (for approved products)

```python
# Using sync_all_shopify.py pattern
for product in approved_products:
    result = sync_to_shopify(product.id, service_key)
    if result.success:
        update_checkpoint(product.id, "synced")
    else:
        log_error(product.id, result.error)
```

### Step 5.2: Generate Batch Report

```markdown
# Product Reform Batch Report

**Batch ID**: reform_2025-11-29_001
**Executed**: [timestamp]
**Duration**: [total_minutes] min

## Summary
| Metric | Value |
|--------|-------|
| Total Products | 22 |
| Successfully Reformed | 20 |
| Synced to Shopify | 18 |
| Failed | 2 |
| Avg Quality Score | 0.89 |
| Avg Research Time | 12min |
| Avg Generation Time | 14min |

## Product Results

| # | Product | Research | Ad Gen | QA Score | Synced | Notes |
|---|---------|----------|--------|----------|--------|-------|
| 1 | [name]  | OK       | OK     | 0.92     | YES    | -     |
| 2 | [name]  | OK       | OK     | 0.87     | YES    | -     |
| 3 | [name]  | LOW_DATA | OK     | 0.78     | NO     | Manual review |
...

## Failed Products (require manual intervention)
1. [product_name] - Error: [description]
2. [product_name] - Error: [description]

## Recommendations
- Products with score < 0.85: manual review before re-sync
- Products with LOW_DATA: deeper research needed
- Next batch: [suggested products]
```

### Step 5.3: Save Artifacts

- `USER_DOCS/produtos/reports/batch_[id]_report.md`
- `USER_DOCS/produtos/reports/batch_[id]_results.json`
- Update Supabase `products.last_reformed_at` timestamp

**Input**:
- All phase outputs
- Sync credentials

**Output**:
- `$batch_report` (markdown)
- `$batch_results` (JSON)
- Shopify product updates

**Validation**:
- [ ] All approved products synced
- [ ] Batch report generated
- [ ] Checkpoint updated

---

## EXECUTION MODES

### Mode A: Full Batch (Recommended for 22 products)

```bash
# Execute via slash command
/reform-batch --limit 22 --parallel 3

# Or manual execution
1. Load this ADW
2. Execute Phase 1 (discovery)
3. Loop Phases 2-4 for each product
4. Execute Phase 5 (sync + report)
```

**Estimated Time**: 22 products × 15min/product = ~5.5 hours (with parallelization: ~2 hours)

### Mode B: Single Product

```bash
/reform-product --id [product_id]

# Executes all 5 phases for 1 product
# Duration: ~45-60min
```

### Mode C: Resume from Checkpoint

```bash
/reform-resume --batch-id reform_2025-11-29_001

# Reads checkpoint, skips completed products
# Resumes from last successful product
```

---

## SLASH COMMAND INTEGRATION

Create `/reform-batch` command in `.claude/commands/`:

```markdown
# /reform-batch - Execute Integrated Product Reform

## Parameters
- `--limit N`: Max products to process (default: all)
- `--parallel N`: Concurrent products (default: 1, max: 3)
- `--dry-run`: Simulate without syncing
- `--product-ids`: Comma-separated specific IDs

## Execution
1. Read ADW: `codexa_agent/workflows/204_ADW_INTEGRATED_PRODUCT_REFORM.md`
2. Execute 5 phases as specified
3. Generate batch report
4. Return summary to user
```

---

## ERROR HANDLING

| Error Type | Action | Continue Batch? |
|------------|--------|-----------------|
| Marketplace search failed | Retry 2x, then skip product | YES |
| Research incomplete (< 3 competitors) | Flag LOW_DATA, continue | YES |
| Ad generation failed | Retry 1x, then skip | YES |
| QA score < 0.70 | Skip sync, log for review | YES |
| Shopify sync failed | Log error, retry next batch | YES |
| Supabase connection lost | Pause, wait 30s, retry | PAUSE |
| Rate limit hit | Wait 60s, continue | PAUSE |

---

## SUCCESS CRITERIA

### Per Product
- [ ] Research notes generated (>= 5 blocks filled)
- [ ] Ad copy generated (Trinity output)
- [ ] QA score >= 0.85
- [ ] Synced to Shopify (if approved)

### Batch Level
- [ ] >= 80% products successfully reformed
- [ ] Batch report generated
- [ ] No critical errors (Supabase/Shopify connection)
- [ ] Checkpoint saved for resume

---

## PARALLEL EXECUTION OPPORTUNITIES

**Independent Tasks (can run in parallel)**:
- Multiple product research (Phase 2) - up to 3 concurrent
- Multiple product generation (Phase 3) - up to 3 concurrent
- Shopify syncs (Phase 5) - up to 5 concurrent with rate limiting

**Sequential Tasks (must run in order)**:
- Phase 1 → Phase 2 (queue needed before research)
- Phase 2 → Phase 3 per product (research needed before generation)
- Phase 3 → Phase 4 per product (generation needed before validation)
- Phase 4 → Phase 5 per product (validation needed before sync)

**Parallelization Pattern**:
```yaml
# Batch parallelization
parallel_batch:
  max_concurrent: 3
  products:
    - product_1: "Phase 2 Research"
    - product_2: "Phase 2 Research"
    - product_3: "Phase 2 Research"
# Wait for batch to complete, then next phase
sequential_per_product:
  - phase_3: "Generation (needs research)"
  - phase_4: "Validation (needs generation)"
  - phase_5: "Sync (needs validation)"
```

---

## TROUBLESHOOTING

**Phase 1 issues**:
- Supabase connection fails → Check SUPABASE_URL and credentials
- No products found → Verify filter criteria or remove filters

**Phase 2 issues**:
- Marketplace search fails → Retry with simplified query, check MCP server
- < 3 competitors found → Flag LOW_DATA, continue with available data
- Rate limit hit → Wait 60s, reduce parallel count

**Phase 3 issues**:
- HOP prompt fails → Check anuncio_agent/prompts/ availability
- Output incomplete → Retry step, check context token limits
- Title too long/short → Regenerate with strict char constraint

**Phase 4 issues**:
- QA score < 0.70 → Review specific failing criteria, regenerate
- Compliance violation → Check forbidden words list, fix description
- Missing research backing → Return to Phase 2 for deeper research

**Phase 5 issues**:
- Shopify sync fails → Check service key, verify product exists
- Rate limit → Reduce concurrent syncs, wait 30s
- Report generation fails → Check output directory permissions

---

## RELATED FILES

**ADWs Orchestrated**:
- `pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md` (research methodology)
- `anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md` (ad generation)

**Plans Used**:
- `pesquisa_agent/config/plans/standard_research.json`
- `anuncio_agent/plans/full_anuncio.json`

**Scripts**:
- `anuncio_agent/scripts/sync_all_shopify.py` (sync pattern)
- `anuncio_agent/scripts/reform_product.py` (single product)

**MCP Tools**:
- `mcp__browser__search_marketplace`
- `mcp__browser__extract_text`
- `mcp__scout__discover`

---

## METADATA

**Created**: 2025-11-29
**Author**: CODEXA Meta-Constructor
**Version**: 1.0.0
**Type**: Orchestration ADW (coordinates multiple agents)
**Agents**: pesquisa_agent + anuncio_agent + sync_shopify
**Phases**: 5
**Estimated Duration**: 15min/product (batch), 45-60min/product (single)

---

**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor
**Contact**: See agentes/README.md for system navigation
