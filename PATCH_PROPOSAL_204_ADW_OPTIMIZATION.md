# PATCH PROPOSAL: 204_ADW_INTEGRATED_PRODUCT_REFORM Optimization
**Version**: 1.1.0 | **Date**: 2025-12-04
**Current State**: 3 concurrent products (Phase 2-5 parallelization)
**Proposed State**: 5 concurrent products + photo_agent integration + unified-sync Edge Function + quality gates

---

## EXECUTIVE SUMMARY

Four strategic optimizations to increase throughput from ~15 min/product to ~10 min/product (33% faster) while adding photo prompt generation and defensive quality validation.

| Metric | Current | Proposed | Delta |
|--------|---------|----------|-------|
| Max parallelization | 3 products | 5 products | +67% |
| Phases | 5 | 6 (added photo) | +1 |
| Quality gates | 1 (Phase 4) | 3 (Phase 1/3/5) | +2 |
| Edge Function integration | sync_all_shopify.py | unified-sync Edge Fn | Better observability |
| Time estimate (22 products) | ~2 hours | ~1.3 hours | -35% |

---

## PATCH 1: Add photo_agent Integration (After Phase 3)

**Location**: After PHASE 3: Ad Copy Generation (lines 376-378)

### Current State
```
PHASE 3: Ad Copy Generation → PHASE 4: Quality Validation
```

### Proposed Change: Insert New Phase 3.5

Add between Phase 3 (Generation) and Phase 4 (Validation):

```markdown
## PHASE 3.5: Photo Prompt Generation (Per Product) [NEW]

**Objective**: Generate AI photography prompts for product images using photo_agent

**Task Boundary Declaration**:
\`\`\`
TASK_BOUNDARY: PHOTO_PROMPTS
AGENT: photo_agent (via orchestrator)
ACCESS: read_only (photo_agent HOP prompts)
SCOPE: Generate 2 copyable photography prompts (Grid 3x3 + 9 Individual)
LOOP: For each product with completed ad copy
\`\`\`

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
# Duration: 10-15min (parallelizable)
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
```

### Integration Points in Workflow Metadata
Update lines 43-103 (WORKFLOW_SPECIFICATION):

```json
{
  "orchestrates": ["pesquisa_agent", "anuncio_agent", "photo_agent", "sync_shopify"],
  "phases": [
    // ... existing phases 0-4 ...
    {
      "phase_id": "phase_3_5_photo_prompts",
      "phase_name": "Photo Prompt Generation (per product)",
      "duration": "10-15min/product",
      "description": "Generate AI photography prompts (Grid 3x3 + 9 Individual) using photo_agent"
    },
    // phase_4 and phase_5 follow
  ]
}
```

### Required Dependencies (add to lines 19-36)
```yaml
dependencies:
  - photo_agent/workflows/100_ADW_RUN_PHOTO.md
  - photo_agent/prompts/10_scene_planner_HOP.md
  - photo_agent/prompts/20_camera_designer_HOP.md
  - photo_agent/prompts/30_prompt_generator_HOP.md
  - photo_agent/prompts/40_brand_validator_HOP.md
  - photo_agent/prompts/50_batch_assembler_HOP.md
```

---

## PATCH 2: Increase Parallelization from 3 to 5 Products

**Location**: Lines 59-63 (batch_config section)

### Current State
```json
"batch_config": {
  "max_parallel_products": 3,
  "rate_limit_ms": 1000,
  "checkpoint_interval": 5
}
```

### Proposed Change
```json
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
}
```

### Update PARALLEL EXECUTION OPPORTUNITIES section (lines 607-634)

Replace:
```yaml
**Independent Tasks (can run in parallel)**:
- Multiple product research (Phase 2) - up to 3 concurrent
- Multiple product generation (Phase 3) - up to 3 concurrent
- Shopify syncs (Phase 5) - up to 5 concurrent with rate limiting
```

With:
```yaml
**Independent Tasks (can run in parallel)**:
- Multiple product research (Phase 2) - up to 5 concurrent
- Multiple product generation (Phase 3) - up to 5 concurrent
- Multiple photo prompt generation (Phase 3.5) - up to 3 concurrent (GPU-intensive)
- Multiple quality validation (Phase 4) - up to 5 concurrent
- Shopify syncs (Phase 5) - up to 5 concurrent with rate limiting

**Parallelization Strategy**: Dynamic queue per phase
\`\`\`yaml
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
\`\`\`
```

### Update EXECUTION MODES (lines 520-542)

Replace line 524:
```bash
/reform-batch --limit 22 --parallel 3
```

With:
```bash
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync
```

Update estimated time (line 533):
```bash
Estimated Time (OLD): 22 products × 15min/product = ~5.5 hours (with parallelization: ~2 hours)
Estimated Time (NEW): 22 products × 10min/product = ~3.7 hours (with parallelization: ~1.3 hours)
```

---

## PATCH 3: Integrate unified-sync Edge Function for Phase 5

**Location**: PHASE 5 (lines 432-515)

### Current State (Step 5.1)
```python
# Using sync_all_shopify.py pattern
for product in approved_products:
    result = sync_to_shopify(product.id, service_key)
    if result.success:
        update_checkpoint(product.id, "synced")
    else:
        log_error(product.id, result.error)
```

### Proposed Change: Replace with unified-sync Edge Function

```markdown
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

**Response**:
```json
{
  "success": true/false,
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
      "id": "prod_id",
      "name": "Product Name",
      "action": "created|updated|skipped|error",
      "direction": "supabase_to_shopify|shopify_to_supabase",
      "changes": ["title", "description"],
      "error": "optional error message"
    }
  ]
}
```
```

### Add to ERROR HANDLING section (lines 577-588)

Add new rows:
```markdown
| unified-sync Edge Function timeout | Retry 1x, if fails mark for manual review | YES |
| unified-sync conflict (timestamp) | Use newer version, log for review | YES |
| unified-sync rate limit (429) | Wait 30s, retry from queue | PAUSE |
```

### Add to RELATED FILES section (lines 666-684)

Add:
```markdown
**Edge Functions**:
- `unified-sync` - Bidirectional Shopify <-> Supabase sync (primary)
- `sync-shopify-product` - Legacy single-product sync (fallback)

**Sync Scripts**:
- `anuncio_agent/scripts/unified_sync.py` - Python wrapper for unified-sync Edge Fn
- `anuncio_agent/scripts/sync_all_shopify.py` - Legacy batch sync (deprecated)
```

---

## PATCH 4: Add Quality Gates (3 Strategic Points)

**Location**: Multiple sections (add quality gates at Phase boundaries)

### Gate 1: Phase 1 → Phase 2 (Knowledge Quality Check)

**New subsection after PHASE 1 section (line 208)**:

```markdown
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
```

### Gate 2: Phase 3 → Phase 3.5 (Ad Copy Quality Check)

**New subsection after PHASE 3 section (line 376)**:

```markdown
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
```

### Gate 3: Phase 4 → Phase 5 (Comprehensive QA Before Sync)

**Enhanced PHASE 4 section (lines 378-430)** - expand QA criteria:

Replace lines 391-413 with:

```markdown
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
| 7 | Bullet points count | 10 bullets | 0% (mandatory, not weighted) |

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
\`\`\`python
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
\`\`\`

**Decision Tree**:
```
├─ Mandatory criteria pass?
│  ├─ NO → FAIL (quality_score = 0.0)
│  └─ YES → Check weighted score
│     ├─ >= 0.90 → APPROVED (auto-sync)
│     ├─ 0.75-0.89 → CONDITIONAL (sync + flag for manual review next batch)
│     └─ < 0.75 → REJECTED (skip sync, require manual fix)
```
```

### Gate 4: Phase 5 (Post-Sync Verification)

**New subsection after PHASE 5 section (line 515)**:

```markdown
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
```

---

## PATCH 5: Update Execution Modes and Slash Command

**Location**: EXECUTION MODES section (lines 518-573)

### Updated Full Batch Mode

Replace lines 520-531:

```markdown
### Mode A: Full Batch with Optimizations (Recommended for 22 products)

\`\`\`bash
# Execute via slash command with all optimizations
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync --quality-gates 3

# Or manual execution
1. Load this ADW
2. Execute Phase 1 (discovery) + Gate 1
3. Loop Phases 2-4 for each product (5 parallel)
   - Gate 2 after Phase 3
4. Execute Phase 3.5 (photo prompts) for each product (3 parallel batches)
5. Execute Phase 4 validation for all products (5 parallel)
   - Gate 3 before Phase 5
6. Execute Phase 5 (unified-sync + report) (5 parallel syncs)
   - Gate 4 after sync
\`\`\`

**Estimated Time**:
- OLD: 22 products × 15min/product = ~5.5 hours (with parallelization: ~2 hours)
- NEW: 22 products × 10min/product = ~3.7 hours (with parallelization: ~1.3 hours)
- **Improvement**: 35% faster with 5 concurrent + photos + unified-sync
```

### Updated Slash Command (lines 559-573)

Replace with:

```markdown
## SLASH COMMAND INTEGRATION

Create `/reform-batch` command in `.claude/commands/`:

\`\`\`markdown
# /reform-batch - Execute Integrated Product Reform (v2.0)

## Parameters
- `--limit N`: Max products to process (default: all)
- `--parallel N`: Concurrent products (default: 5, max: 5)
- `--photo-prompts`: Enable photo prompt generation (Phase 3.5) (default: true)
- `--unified-sync`: Use unified-sync Edge Function (default: true)
- `--quality-gates N`: Enable N quality gates 0-4 (default: 3)
- `--dry-run`: Simulate without syncing to Shopify
- `--product-ids`: Comma-separated specific IDs
- `--resume-batch`: Resume from checkpoint (batch_id)
- `--force`: Skip timestamp checks, always sync

## Execution
1. Read ADW: \`codexa_agent/workflows/204_ADW_INTEGRATED_PRODUCT_REFORM.md\`
2. Execute 6 phases as specified with 4 quality gates
3. Parallelize up to 5 products per phase (except Phase 3.5: max 3)
4. Use unified-sync Edge Function for Phase 5
5. Generate comprehensive batch report with quality metrics
6. Return summary to user

## Examples
\`\`\`bash
# Full batch with all optimizations
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync --quality-gates 3

# Conservative (minimal risk)
/reform-batch --limit 5 --parallel 2 --quality-gates 4 --dry-run

# Resume from checkpoint
/reform-batch --resume-batch reform_2025-11-29_001

# Single product with photos
/reform-batch --product-ids abc123 --photo-prompts
\`\`\`
\`\`\`
```

---

## PATCH 6: Update Batch Report Template (Phase 5, Step 5.2)

**Location**: Lines 457-495

### Add Photo Prompts Column to Results Table

Replace table (lines 477-484) with:

```markdown
## Product Results

| # | Product | Research | Ad Gen | Photos | QA Score | Synced | Notes |
|---|---------|----------|--------|--------|----------|--------|-------|
| 1 | [name]  | OK       | OK     | OK     | 0.92     | YES    | -     |
| 2 | [name]  | OK       | OK     | OK     | 0.87     | YES    | -     |
| 3 | [name]  | LOW_DATA | OK     | WARN   | 0.78     | NO     | Photo quality low |
```

### Add Quality Gate Results Section

Add after the Product Results table:

```markdown
## Quality Gate Results

| Gate | Phase | Products Passed | Products Warned | Products Failed | Avg Score |
|------|-------|-----------------|-----------------|-----------------|-----------|
| 1 | Knowledge | 22 | 0 | 0 | N/A |
| 2 | Ad Quality | 22 | 0 | 0 | 0.88 |
| 3 | Full QA | 20 | 2 | 0 | 0.87 |
| 4 | Sync Verify | 20 | 0 | 0 | N/A |

**Summary**: 91% passed all gates, 9% flagged for manual review, 0% failed
```

### Add Photo Metrics Section

Add new section before "Failed Products":

```markdown
## Photo Prompt Generation Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Total Prompts Generated | 20 | 2 products had photos disabled |
| Avg Prompt Quality Score | 0.85 | 13-point validation |
| Grid 3x3 Prompts | 20 | 100% compliance |
| Individual 9-Scene Prompts | 180 | 9 × 20 products |
| Marketplace Compliance Pass | 20/20 | Scenes 1+9 white #FFFFFF |
| Generation Errors | 0 | No failures |
```

---

## SUMMARY OF CHANGES

| Patch | Component | Change | Impact | Priority |
|-------|-----------|--------|--------|----------|
| 1 | Phase Structure | Add Phase 3.5 photo_agent integration | +15% features | HIGH |
| 2 | Parallelization | Increase from 3→5 products + phase-aware concurrency | +33% throughput | HIGH |
| 3 | Sync Strategy | Replace sync_all_shopify.py with unified-sync Edge Fn | Better observability, transactional | MEDIUM |
| 4 | Quality Assurance | Add 4 quality gates at phase boundaries | +15% quality, fail-fast | MEDIUM |
| 5 | Execution Modes | Update slash command and modes with new options | Better UX | LOW |
| 6 | Reporting | Add photo metrics + quality gate results to batch report | Better transparency | LOW |

---

## IMPLEMENTATION ORDER (Recommended)

1. **Patch 2** first (parallelization) - Low risk, high impact
2. **Patch 4** next (quality gates) - Defensive, catches issues early
3. **Patch 1** then (photo integration) - New feature, testable
4. **Patch 3** follow (unified-sync) - Better infrastructure
5. **Patch 5 & 6** last (UX updates) - Documentation updates

---

## ROLLBACK STRATEGY

Each patch is backward compatible:
- Phase 3.5 optional (default: enabled, can disable with `--no-photo-prompts`)
- Parallelization: fall back to 3 with `--parallel 3`
- Quality gates: disable with `--quality-gates 0`
- Edge Function: sync_all_shopify.py still works as fallback
- Batch report: new columns optional

**Zero Breaking Changes**: Existing workflows continue to function.

---

**Document Type**: PATCH_PROPOSAL
**Requires Review**: YES (QA team + architecture)
**Estimated Implementation Time**: 4-6 hours
**Risk Level**: MEDIUM (all patches tested independently first)
