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
  - photo_agent/workflows/100_ADW_RUN_PHOTO.md
  - photo_agent/prompts/10_scene_planner_HOP.md
  - photo_agent/prompts/20_camera_designer_HOP.md
  - photo_agent/prompts/30_prompt_generator_HOP.md
  - photo_agent/prompts/40_brand_validator_HOP.md
  - photo_agent/prompts/50_batch_assembler_HOP.md
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
  "orchestrates": ["pesquisa_agent", "anuncio_agent", "photo_agent", "sync_shopify"],
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
    "max_parallel_products": 5,
    "rate_limit_ms": 500,
    "checkpoint_interval": 10,
    "parallelization_strategy": "dynamic_queue_per_phase",
    "phase_concurrency": {
      "phase_2_research": 5,
      "phase_3_generation": 5,
      "phase_3_5_photo_prompts": 3,
      "phase_4_validation": 5,
      "phase_5_sync": 5
    }
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
      "phase_id": "phase_3_5_photo_prompts",
      "phase_name": "Photo Prompt Generation (per product)",
      "duration": "10-15min/product",
      "description": "Generate AI photography prompts (Grid 3x3 + 9 Individual) using photo_agent"
    },
    {
      "phase_id": "phase_4_validation",
      "phase_name": "Quality Validation (per product)",
      "duration": "2-3min/product",
      "description": "13-criteria QA check + compliance validation + photo integration"
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

### Quality Gate 1: Knowledge Load Validation

**Objective**: Verify knowledge context is sufficient before research starts

**Checklist**:
- [ ] pesquisa_agent/PRIME.md loaded
- [ ] anuncio_agent/PRIME.md loaded
- [ ] marketplace_specs.json accessible
- [ ] copy_rules.json accessible
- [ ] At least 1 product in queue
- [ ] Checkpoint file created

**Failure Action**: STOP and ask user to verify prerequisites

**Score Threshold**: ALL items must pass (no partial)

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

### Quality Gate 2: Ad Copy Quality Validation (Before Photo Generation)

**Objective**: Fast pre-photo validation to avoid wasting compute on bad copy

**Quick Checklist (5 criteria)**:
1. Title present and 55-65 chars? → YES/NO
2. Description > 500 chars? → YES/NO
3. Keywords >= 5 high-value terms? → YES/NO
4. No forbidden words detected? → YES/NO
5. At least 5 bullet points? → YES/NO

**Score**: 5 criteria × 20% each = 0-100%

**Thresholds**:
- ≥ 4/5 criteria (80%): PASS → Continue to Phase 3.5 (photo)
- 3/5 criteria (60%): WARN → Flag for manual review, continue
- < 3/5 criteria (60%): FAIL → Skip to Phase 4 validation (skip photos), continue

**Why This Gate?**: Photo generation is LLM-intensive; fail fast on broken copy.

---

## PHASE 3.5: Photo Prompt Generation (Per Product)

**Objective**: Generate AI photography prompts for product images using photo_agent

**Task Boundary Declaration**:
```
TASK_BOUNDARY: PHOTO_PROMPTS
AGENT: photo_agent (via orchestrator)
ACCESS: read_only (photo_agent HOP prompts)
SCOPE: Generate 2 copyable photography prompts (Grid 3x3 + 9 Individual)
LOOP: For each product with completed ad copy (Gate 2 passed)
```

**Execution Steps**:

### Step 3.5.1: Extract Product Visuals Context
From Phase 3 output, extract:
- Product type and category
- Key features from bullet points
- Color/material from description
- Target marketplace style (ML/Shopee/Amazon)

### Step 3.5.2: Call photo_agent (Workflow: Standard 9-Scene)

```python
# Invoke photo_agent with extracted context
photo_context = {
  "subject": f"{product.name} - {product.category}",
  "key_features": extracted_bullets[0:3],
  "colors": extract_dominant_colors(product.anuncio.description),
  "marketplace_compliance": "mercado_livre"
}

# Execute photo_agent/workflows/100_ADW_RUN_PHOTO.md
# Duration: 10-15min (parallelizable, max 3 concurrent due to LLM tokens)
```

### Step 3.5.3: Generate Trinity Output

Save to `USER_DOCS/produtos/fotos/{product_name}/`:
- `{product_name}_prompts.md` (human-readable grid + individual)
- `{product_name}_prompts.json` (structured for image generation API)
- `{product_name}_prompts.meta.json` (workflow metadata with seed values)

**Input**:
- `$anuncio_package` (from Phase 3)
- `$product` (product data)
- photo_agent HOP prompts

**Output**:
- `$photo_prompts_package` (Trinity output)
- `$photos_generated` (count)

**Validation**:
- [ ] Grid prompt present (3x3 concatenated)
- [ ] 9 individual prompts generated (≥80 words each)
- [ ] `{user_image} {seed:[RANDOM]}` prefix present
- [ ] Scenes 1 & 9 have white #FFFFFF background
- [ ] `[OPEN_VARIABLES]` placeholders included

**Error Handling**:
- If photo_agent fails → log warning, continue (photos optional)
- If < 6 prompts generated → flag LOW_PHOTOS, continue
- Retry count: 1 (time budget: 15min max)

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

### Quality Gate 3: Comprehensive QA Validation (Before Sync)

**QA Checklist (13 criteria across 4 categories)**:

#### Technical Criteria (50% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 1 | Title char count | 58-60 chars (ML) | 8% |
| 2 | Title keyword density | >= 0.70 | 8% |
| 3 | Keywords total count | >= 60 | 8% |
| 4 | Keywords coverage | >= 80% head terms | 8% |
| 5 | Description length | >= 3300 chars | 10% |
| 6 | Description keyword density | 2-5% | 8% |
| 7 | Bullet points count | 10 bullets | 0% (mandatory) |

#### Compliance Criteria (30% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 8 | No forbidden words | 0 violations | 10% |
| 9 | Price formatting valid | R$ format | 10% |
| 10 | No HTML tags in description | 0 tags | 10% |

#### Research-Backed Criteria (15% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 11 | Competitors analyzed | >= 3 | 8% |
| 12 | Keywords from research | >= 70% research terms | 7% |

#### Photo Integration Criteria (5% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 13 | Photo prompts generated | Present or N/A | 5% |

**Quality Score Calculation**:
```python
quality_score = sum(criterion.passed * criterion.weight for criterion in qa_checks)
# NEW: Mandatory checks (must pass all):
mandatory_pass = bullet_points == 10 and forbidden_words == 0

if not mandatory_pass:
    quality_score = 0.0  # Auto-fail
elif quality_score >= 0.90:
    sync_approved = True
elif quality_score >= 0.75:
    sync_approved = True
    flag_manual_review = True
else:
    sync_approved = False  # Require manual intervention
```

**Decision Tree**:
```
├─ Mandatory criteria pass?
│  ├─ NO → FAIL (quality_score = 0.0)
│  └─ YES → Check weighted score
│     ├─ >= 0.90 → APPROVED (auto-sync)
│     ├─ 0.75-0.89 → CONDITIONAL (sync + flag for manual review next batch)
│     └─ < 0.75 → REJECTED (skip sync, require manual fix)
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

### Step 5.1: Sync to Shopify via unified-sync Edge Function

**Option A: Batch Sync (Recommended)**
```python
# Using unified_sync.py wrapper (calls unified-sync Edge Function)
from anuncio_agent.scripts.unified_sync import call_unified_sync

result = call_unified_sync(
    mode="push",
    scope="content",  # Only ad copy + images
    dry_run=False,
    force=False  # Respect timestamps
)

# Result structure:
{
  "success": true,
  "mode": "push",
  "scope": "content",
  "duration_ms": 8500,
  "stats": {
    "total": 22,
    "synced": 20,
    "created": 2,
    "updated": 18,
    "skipped": 0,
    "errors": 2
  },
  "products": [
    {
      "id": "prod_123",
      "name": "Product Name",
      "action": "updated",
      "direction": "supabase_to_shopify",
      "changes": ["title", "description", "images"]
    }
  ]
}
```

**Option B: Per-Product Sync (for individual failures)**
```python
# Fallback for failed products
result = call_unified_sync(
    mode="push",
    scope="content",
    product_id=product.id,
    force=True
)
```

**Edge Function Benefits**:
1. **Transactional**: All-or-nothing for each product
2. **Observability**: Detailed change logs returned to Supabase
3. **Rate Limiting**: Built-in exponential backoff
4. **Conflict Resolution**: Timestamp-based smart merge
5. **Rollback**: On error, Edge Function reverts Shopify changes

**API Endpoint**: `https://fuuguegkqnpzrrhwymgw.supabase.co/functions/v1/unified-sync`

**Request Headers**:
```json
{
  "Authorization": "Bearer <SUPABASE_SERVICE_ROLE_KEY>",
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "mode": "push|pull|bidirectional",
  "scope": "all|content|inventory|price",
  "productId": "optional",
  "dryRun": false,
  "force": false
}
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

| # | Product | Research | Ad Gen | Photos | QA Score | Synced | Notes |
|---|---------|----------|--------|--------|----------|--------|-------|
| 1 | [name]  | OK       | OK     | OK     | 0.92     | YES    | -     |
| 2 | [name]  | OK       | OK     | OK     | 0.87     | YES    | -     |
| 3 | [name]  | LOW_DATA | OK     | WARN   | 0.78     | NO     | Photo quality low |
...

## Quality Gate Results

| Gate | Phase | Products Passed | Products Warned | Products Failed | Avg Score |
|------|-------|-----------------|-----------------|-----------------|-----------|
| 1 | Knowledge | 22 | 0 | 0 | N/A |
| 2 | Ad Quality | 22 | 0 | 0 | 0.88 |
| 3 | Full QA | 20 | 2 | 0 | 0.87 |
| 4 | Sync Verify | 20 | 0 | 0 | N/A |

**Summary**: 91% passed all gates, 9% flagged for manual review, 0% failed

## Photo Prompt Generation Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Total Prompts Generated | 20 | 2 products had photos disabled |
| Avg Prompt Quality Score | 0.85 | 13-point validation |
| Grid 3x3 Prompts | 20 | 100% compliance |
| Individual 9-Scene Prompts | 180 | 9 × 20 products |
| Marketplace Compliance Pass | 20/20 | Scenes 1+9 white #FFFFFF |
| Generation Errors | 0 | No failures |

## Failed Products (require manual intervention)
1. [product_name] - Error: [description]
2. [product_name] - Error: [description]

## Recommendations
- Products with score < 0.85: manual review before re-sync
- Products with LOW_DATA: deeper research needed
- Products with LOW_PHOTOS: regenerate with explicit scene instructions
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

### Quality Gate 4: Post-Sync Verification

**Objective**: Verify sync completed successfully before marking batch complete

**Checklist**:
- [ ] unified-sync returned success=true
- [ ] All approved products in sync stats
- [ ] Errors count <= 2 (< 10% failure rate)
- [ ] Batch report generated
- [ ] Checkpoint updated with synced timestamp

**If Errors > 2**:
1. Log error details to `batch_[id]_errors.json`
2. Retry failed products with `--force` flag
3. If still failing, move to manual review queue
4. Continue batch processing (don't pause)

**If Batch Integrity Compromised** (> 50% failures):
- PAUSE execution
- Return detailed error report to user
- Require `--force-continue` to proceed

---

## EXECUTION MODES

### Mode A: Full Batch with Optimizations (Recommended for 22 products)

```bash
# Execute via slash command with all optimizations
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync --quality-gates 4

# Or manual execution
1. Load this ADW
2. Execute Phase 1 (discovery) + Gate 1
3. Loop Phases 2-3 for each product (5 parallel)
   - Gate 2 after Phase 3
4. Execute Phase 3.5 (photo prompts) for each product (3 parallel batches)
5. Execute Phase 4 validation for all products (5 parallel)
   - Gate 3 before Phase 5
6. Execute Phase 5 (unified-sync + report) (5 parallel syncs)
   - Gate 4 after sync
```

**Estimated Time**:
- OLD: 22 products × 15min/product = ~5.5 hours (with parallelization: ~2 hours)
- NEW: 22 products × 10min/product = ~3.7 hours (with parallelization: ~1.3 hours)
- **Improvement**: 35% faster with 5 concurrent + photos + unified-sync

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
# /reform-batch - Execute Integrated Product Reform (v2.0)

## Parameters
- `--limit N`: Max products to process (default: all)
- `--parallel N`: Concurrent products (default: 5, max: 5)
- `--photo-prompts`: Enable photo prompt generation (Phase 3.5) (default: true)
- `--unified-sync`: Use unified-sync Edge Function (default: true)
- `--quality-gates N`: Enable N quality gates 0-4 (default: 4)
- `--dry-run`: Simulate without syncing to Shopify
- `--product-ids`: Comma-separated specific IDs
- `--resume-batch`: Resume from checkpoint (batch_id)
- `--force`: Skip timestamp checks, always sync

## Execution
1. Read ADW: `codexa_agent/workflows/204_ADW_INTEGRATED_PRODUCT_REFORM.md`
2. Execute 6 phases as specified with 4 quality gates
3. Parallelize up to 5 products per phase (except Phase 3.5: max 3)
4. Use unified-sync Edge Function for Phase 5
5. Generate comprehensive batch report with quality metrics
6. Return summary to user

## Examples
\`\`\`bash
# Full batch with all optimizations
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync --quality-gates 4

# Conservative (minimal risk)
/reform-batch --limit 5 --parallel 2 --quality-gates 4 --dry-run

# Resume from checkpoint
/reform-batch --resume-batch reform_2025-11-29_001

# Single product with photos
/reform-batch --product-ids abc123 --photo-prompts
\`\`\`
```

---

## ERROR HANDLING

| Error Type | Action | Continue Batch? |
|------------|--------|-----------------|
| Marketplace search failed | Retry 2x, then skip product | YES |
| Research incomplete (< 3 competitors) | Flag LOW_DATA, continue | YES |
| Ad generation failed | Retry 1x, then skip | YES |
| Photo prompt generation failed | Log warning, continue (photos optional) | YES |
| QA score < 0.70 | Skip sync, log for review | YES |
| Shopify sync failed | Log error, retry next batch | YES |
| unified-sync Edge Function timeout | Retry 1x, if fails mark for manual review | YES |
| unified-sync conflict (timestamp) | Use newer version, log for review | YES |
| unified-sync rate limit (429) | Wait 30s, retry from queue | PAUSE |
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
- Multiple product research (Phase 2) - up to 5 concurrent
- Multiple product generation (Phase 3) - up to 5 concurrent
- Multiple photo prompt generation (Phase 3.5) - up to 3 concurrent (LLM-intensive)
- Multiple quality validation (Phase 4) - up to 5 concurrent
- Shopify syncs (Phase 5) - up to 5 concurrent with rate limiting

**Sequential Tasks (must run in order)**:
- Phase 1 → Phase 2 (queue needed before research)
- Phase 2 → Phase 3 per product (research needed before generation)
- Phase 3 → Phase 4 per product (generation needed before validation)
- Phase 4 → Phase 5 per product (validation needed before sync)

**Parallelization Strategy**: Dynamic queue per phase
```yaml
batch_pipeline:
  phase_2_research:
    max_concurrent: 5
    queue: product_1, product_2, product_3, product_4, product_5

  phase_3_generation:
    max_concurrent: 5
    queue: product_1, product_2, product_3, product_4, product_5

  phase_3_5_photo_prompts:
    max_concurrent: 3  # LLM token limits
    queue: product_1, product_2, product_3 (batched)
    parallel_batch_2: product_4, product_5

  phase_4_validation:
    max_concurrent: 5
    queue: all_completed_products

  phase_5_sync:
    max_concurrent: 5
    rate_limiter: 500ms between API calls
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
- `anuncio_agent/scripts/unified_sync.py` - Python wrapper for unified-sync Edge Fn (primary)
- `anuncio_agent/scripts/sync_all_shopify.py` - Legacy batch sync (fallback)
- `anuncio_agent/scripts/reform_product.py` (single product)

**Edge Functions**:
- `unified-sync` - Bidirectional Shopify <-> Supabase sync (primary)
- `sync-shopify-product` - Legacy single-product sync (fallback)

**MCP Tools**:
- `mcp__browser__search_marketplace`
- `mcp__browser__extract_text`
- `mcp__scout__discover`

---

## METADATA

**Created**: 2025-11-29
**Updated**: 2025-12-04
**Author**: CODEXA Meta-Constructor
**Version**: 1.1.0
**Type**: Orchestration ADW (coordinates multiple agents)
**Agents**: pesquisa_agent + anuncio_agent + photo_agent + sync_shopify
**Phases**: 6 (including Phase 3.5 photo prompts)
**Quality Gates**: 4 (Phase 1→2, Phase 3→3.5, Phase 4→5, Post-sync)
**Estimated Duration**: 10min/product (batch with 5 concurrent), 35-45min/product (single)

---

**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor
**Contact**: See agentes/README.md for system navigation
