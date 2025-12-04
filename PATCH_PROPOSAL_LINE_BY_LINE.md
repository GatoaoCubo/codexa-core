# Detailed Line-by-Line PATCH Instructions for 204_ADW

**File**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\codexa_agent\workflows\204_ADW_INTEGRATED_PRODUCT_REFORM.md`

---

## CHANGE 1: Update MODULE_METADATA (Lines 19-35)

### BEFORE (Current)
```yaml
dependencies:
  - pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md
  - anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md
  - anuncio_agent/scripts/sync_all_shopify.py
  - anuncio_agent/plans/full_anuncio.json
```

### AFTER (New)
```yaml
dependencies:
  - pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md
  - anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md
  - photo_agent/workflows/100_ADW_RUN_PHOTO.md
  - photo_agent/prompts/10_scene_planner_HOP.md
  - photo_agent/prompts/20_camera_designer_HOP.md
  - photo_agent/prompts/30_prompt_generator_HOP.md
  - photo_agent/prompts/40_brand_validator_HOP.md
  - photo_agent/prompts/50_batch_assembler_HOP.md
  - anuncio_agent/scripts/unified_sync.py
  - anuncio_agent/plans/full_anuncio.json
mcp_requirements:
  - mcp__browser__search_marketplace
  - mcp__browser__extract_text
  - mcp__scout__discover
  - mcp__photo_agent__execute_workflow
```

---

## CHANGE 2: Update WORKFLOW_SPECIFICATION (Lines 43-103)

### BEFORE (Current)
```json
{
  "workflow_id": "adw_integrated_product_reform",
  "workflow_name": "Integrated Product Reform Pipeline",
  "version": "1.0.0",
  "orchestrates": ["pesquisa_agent", "anuncio_agent", "sync_shopify"],
  ...
  "batch_config": {
    "max_parallel_products": 3,
    "rate_limit_ms": 1000,
    "checkpoint_interval": 5
  },

  "phases": [
    ...
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

### AFTER (New)
```json
{
  "workflow_id": "adw_integrated_product_reform",
  "workflow_name": "Integrated Product Reform Pipeline",
  "version": "2.0.0",
  "orchestrates": ["pesquisa_agent", "anuncio_agent", "photo_agent", "sync_shopify"],
  ...
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
    ...
    {
      "phase_id": "phase_4_validation",
      "phase_name": "Quality Validation (per product)",
      "duration": "2-3min/product",
      "description": "13-criteria QA check + compliance validation + photo validation"
    },
    {
      "phase_id": "phase_3_5_photo_prompts",
      "phase_name": "Photo Prompt Generation (per product) [NEW]",
      "duration": "10-15min/product",
      "description": "Generate AI photography prompts (Grid 3x3 + 9 Individual) using photo_agent"
    },
    {
      "phase_id": "phase_5_sync",
      "phase_name": "Shopify Sync & Batch Report",
      "duration": "1-2min/product + 5min report",
      "description": "Push to Shopify via unified-sync Edge Function + generate consolidated report"
    }
  ]
}
```

**Note**: Move phase_3_5 AFTER phase_4 in the array (it should execute after validation decides to sync).

---

## CHANGE 3: Insert Phase 3.5 Documentation (After Line 376)

### INSERT NEW SECTION

```markdown
---

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

From Phase 3 output (anuncio_package), extract:
- Product type and category (from research_notes)
- Key features (first 3 bullet points from Trinity output)
- Material/color/finish (from description keywords)
- Target marketplace style (mercado_livre for default)

\`\`\`python
photo_context = {
  "subject": f"{product.name} - {product.category}",
  "key_features": anuncio.bullets[0:3],
  "colors": extract_color_palette(anuncio.description),
  "marketplace_compliance": "mercado_livre",
  "product_type": detect_type(product.category)
}
\`\`\`

### Step 3.5.2: Call photo_agent (100_ADW_RUN_PHOTO)

```python
# Execute photo_agent workflow
from photo_agent.workflows.adw_runner import execute_photo_adw

result = execute_photo_adw(
    subject=photo_context["subject"],
    style="marketplace",  # Compliance mode
    compliance_mode="mercado_livre",
    product_type=photo_context["product_type"],
    brand_colors=photo_context["colors"]
)

# Result structure:
{
  "status": "complete",
  "grid_3x3_prompt": "...",
  "individual_prompts": ["...", "...", ...],  # 9 prompts
  "seeds": [12345, 23456, ...],
  "quality_score": 0.91,
  "generation_time_ms": 8500
}
```

**Duration**: 10-15min per product (LLM-bound, parallelizable in batches of 3)

### Step 3.5.3: Generate Trinity Output

Save to `USER_DOCS/produtos/fotos/{product_name}/`:

1. **{product_name}_prompts.md** (human-readable)
   ```markdown
   # Photo Prompts: [Product Name]
   Generated: [timestamp]
   Quality Score: 0.91

   ## Grid 3x3 (Master Prompt)
   [full concatenated prompt for all 9 scenes]

   ## Individual Prompts (9 Scenes)
   ### Scene 1: [description]
   [prompt 1]

   ### Scene 2: [description]
   [prompt 2]
   ...
   ```

2. **{product_name}_prompts.json** (structured)
   ```json
   {
     "product_id": "prod_123",
     "grid_3x3": "...",
     "scenes": [
       {
         "scene_id": 1,
         "name": "White Background Hero",
         "prompt": "...",
         "seed": 12345,
         "compliance_flags": []
       },
       ...
     ],
     "quality_score": 0.91,
     "compliance_check": "passed"
   }
   ```

3. **{product_name}_prompts.meta.json** (workflow metadata)
   ```json
   {
     "phase": "3.5",
     "agent": "photo_agent",
     "version": "100_ADW_RUN_PHOTO_v2.0.0",
     "execution_time_ms": 8500,
     "quality_score": 0.91,
     "generated_at": "[ISO8601]"
   }
   ```

**Input**:
- `$anuncio_package` (from Phase 3)
- `$research_notes` (from Phase 2)
- `$product` (product data)
- photo_agent HOP prompts (5 modules)

**Output**:
- `$photo_prompts_package` (Trinity format)
- `$photo_generation_time` (milliseconds)
- `$photo_quality_score` (0.0-1.0)

**Validation**:
- [ ] Grid prompt present (3x3 concatenated, ≥500 words)
- [ ] 9 individual prompts generated (≥80 words each)
- [ ] `{user_image} {seed:[RANDOM]}` prefix present
- [ ] Scenes 1 & 9 = white #FFFFFF background
- [ ] `[OPEN_VARIABLES]` placeholders included
- [ ] No impossible camera setups
- [ ] All prompts use same product reference

**Error Handling**:
- If photo_agent fails → log WARNING, flag as PHOTO_OPTIONAL, continue (photos not mandatory)
- If < 6 prompts generated → flag LOW_PHOTOS, save partial output
- If quality_score < 0.70 → retry once with same context
- Max timeout: 15 min per product, then skip and continue

---
```

---

## CHANGE 4: Add Quality Gate 1 (After Line 208, after PHASE 1)

### INSERT NEW SUBSECTION

```markdown
### Quality Gate 1: Knowledge Load Validation

**Objective**: Verify knowledge context is sufficient before research starts

**Trigger**: After Phase 1 completion, before Phase 2 starts

**Checklist** (all must pass):
- [ ] pesquisa_agent/PRIME.md loaded in context
- [ ] anuncio_agent/PRIME.md loaded in context
- [ ] photo_agent/PRIME.md loaded in context (NEW)
- [ ] marketplace_specs.json accessible (ML/Shopee/Amazon)
- [ ] copy_rules.json accessible (forbidden words list)
- [ ] At least 1 product in queue
- [ ] Checkpoint file created with valid JSON

**Validation Result**:
\`\`\`python
if all(checklist_items):
    gate_status = "PASS"
    continue_to_phase_2 = True
else:
    gate_status = "FAIL"
    continue_to_phase_2 = False
    error_message = f"Failed items: {[x for x in checklist_items if not x]}"
\`\`\`

**Failure Action**: STOP and log missing prerequisites. Do not proceed to Phase 2.

---
```

---

## CHANGE 5: Add Quality Gate 2 (After PHASE 3 section, line ~376)

### INSERT NEW SUBSECTION

```markdown
### Quality Gate 2: Fast Ad Copy Pre-Check (Before Photos)

**Objective**: Validate ad copy quality before expensive Phase 3.5 photo generation

**Trigger**: After Phase 3 completion, before Phase 3.5 decision

**Quick Validation** (5 criteria, ~30 seconds):

| # | Criterion | Check | Pass? |
|---|-----------|-------|-------|
| 1 | Title present & length | 55-65 chars | YES/NO |
| 2 | Description exists | > 500 chars | YES/NO |
| 3 | High-value keywords | ≥ 5 keywords | YES/NO |
| 4 | Forbidden words | 0 violations | YES/NO |
| 5 | Bullet points | ≥ 5 bullets | YES/NO |

**Scoring**:
\`\`\`python
score = (passed_criteria / 5) * 100

if score >= 80:  # 4-5 criteria pass
    gate_status = "PASS"
    execute_phase_3_5 = True
elif score >= 60:  # 3 criteria pass
    gate_status = "WARN"
    execute_phase_3_5 = True
    flag_for_manual_review = True
else:  # < 3 criteria pass
    gate_status = "FAIL"
    execute_phase_3_5 = False  # Skip photos, go to full QA
\`\`\`

**Decision**:
- PASS (80%+): Continue to Phase 3.5 (photos)
- WARN (60-79%): Continue with caution, flag for next manual review
- FAIL (<60%): Skip Phase 3.5, go directly to Phase 4 (full QA)

**Why This Gate?**: Phase 3.5 (photo generation) is compute-intensive. Fail fast on broken copy.

---
```

---

## CHANGE 6: Enhance Quality Gate in PHASE 4 (Lines 378-413)

### BEFORE (Current)
```markdown
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
\`\`\`python
quality_score = sum(criterion.passed * criterion.weight for criterion in qa_checks)
# Threshold: >= 0.85 to proceed to sync
# 0.70-0.84: WARN, manual review suggested
# < 0.70: FAIL, do not sync
\`\`\`
```

### AFTER (Enhanced)
```markdown
### Quality Gate 3: Comprehensive QA Validation (Before Sync)

**QA Checklist** (13 criteria, 4 categories):

#### Technical Criteria (50% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 1 | Title char count | 58-60 chars (ML) | 8% |
| 2 | Title keyword density | >= 0.70 | 8% |
| 3 | Keywords total count | >= 60 | 8% |
| 4 | Keywords coverage | >= 80% head terms | 8% |
| 5 | Description length | >= 3300 chars | 10% |
| 6 | Description keyword density | 2-5% | 8% |
| 7 | Bullet points count | ≥ 10 bullets | 0% (mandatory) |

#### Compliance Criteria (30% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 8 | No forbidden words | 0 violations | 10% |
| 9 | Price formatting | R$ format valid | 10% |
| 10 | No HTML in description | 0 HTML tags | 10% |

#### Research-Backed Criteria (15% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 11 | Competitors analyzed | >= 3 | 8% |
| 12 | Keywords from research | >= 70% research terms | 7% |

#### Photo Integration (5% weight)
| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 13 | Photo prompts | Present OR N/A | 5% |

**Quality Score Calculation**:
\`\`\`python
# Step 1: Check mandatory criteria
mandatory_pass = (
    bullet_points >= 10 and
    forbidden_words == 0 and
    price_format_valid
)

if not mandatory_pass:
    quality_score = 0.0  # Auto-fail
    sync_approved = False
else:
    # Step 2: Calculate weighted score
    quality_score = sum(criterion.passed * criterion.weight for criterion in qa_checks)

    # Step 3: Apply thresholds
    if quality_score >= 0.90:
        sync_approved = True
    elif quality_score >= 0.75:
        sync_approved = True
        flag_manual_review = True
    else:
        sync_approved = False
\`\`\`

**Decision Tree**:
```
Quality Gate 3
├─ Mandatory criteria pass?
│  ├─ NO → FAIL (quality_score = 0.0, sync_approved = False)
│  └─ YES → Check weighted score
│     ├─ >= 0.90 → APPROVED (auto-sync to Phase 5)
│     ├─ 0.75-0.89 → CONDITIONAL (sync + flag for manual review)
│     └─ < 0.75 → REJECTED (skip sync, require manual intervention)
```
```

---

## CHANGE 7: Add Quality Gate 4 (After PHASE 5, line ~515)

### INSERT NEW SUBSECTION

```markdown
### Quality Gate 4: Post-Sync Verification

**Objective**: Verify sync completed successfully before marking batch complete

**Trigger**: After Phase 5 unified-sync execution

**Checklist**:
- [ ] unified-sync Edge Function returned success=true
- [ ] All approved products in sync stats.total
- [ ] Errors count <= 2 (< 10% failure rate for batch)
- [ ] Batch report generated in USER_DOCS/produtos/reports/
- [ ] Checkpoint file updated with synced timestamp

**Failure Scenarios**:

| Scenario | Action | Continue Batch? |
|----------|--------|-----------------|
| 1 sync error | Log details, flag for manual review | YES |
| 2-3 sync errors | Log details, retry with `--force` | YES |
| > 3 errors OR > 50% failed | Log errors to batch_[id]_errors.json | PAUSE |

**Failure Action**:
\`\`\`python
if errors > 3 or (errors / total) > 0.5:
    gate_status = "CRITICAL"
    batch_status = "PAUSED"
    requires_user_action = True
    error_report_written = True
    message = f"Critical sync failure: {errors}/{total} products failed. Batch paused."
else:
    gate_status = "PASS_WITH_WARNINGS"
    batch_status = "COMPLETE"
    requires_user_action = False
\`\`\`

**If Batch Integrity Compromised**:
1. Write detailed error report: `batch_[id]_ERRORS.json`
2. List failed product IDs for retry
3. PAUSE batch execution
4. Return error report + summary to user
5. Require explicit `--force-continue` flag to proceed

---
```

---

## CHANGE 8: Update batch_config (Lines 59-63)

### BEFORE
```json
"batch_config": {
  "max_parallel_products": 3,
  "rate_limit_ms": 1000,
  "checkpoint_interval": 5
}
```

### AFTER
```json
"batch_config": {
  "max_parallel_products": 5,
  "rate_limit_ms": 500,
  "checkpoint_interval": 10,
  "parallelization_strategy": "dynamic_queue_per_phase",
  "quality_gates": {
    "gate_1": { "enabled": true, "phase": "1→2", "type": "knowledge" },
    "gate_2": { "enabled": true, "phase": "3→3.5", "type": "fast_precheck" },
    "gate_3": { "enabled": true, "phase": "4→5", "type": "comprehensive_qa" },
    "gate_4": { "enabled": true, "phase": "5_end", "type": "sync_verify" }
  },
  "phase_concurrency": {
    "phase_2_research": 5,
    "phase_3_generation": 5,
    "phase_3_5_photo_prompts": 3,
    "phase_4_validation": 5,
    "phase_5_sync": 5
  }
}
```

---

## CHANGE 9: Update PARALLEL EXECUTION OPPORTUNITIES (Lines 607-634)

### BEFORE
```markdown
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
\`\`\`yaml
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
\`\`\`
```

### AFTER
```markdown
**Independent Tasks (can run in parallel)**:
- Multiple product research (Phase 2) - up to 5 concurrent
- Multiple product generation (Phase 3) - up to 5 concurrent
- Multiple photo prompt generation (Phase 3.5) - up to 3 concurrent (LLM-bound)
- Multiple quality validation (Phase 4) - up to 5 concurrent
- Shopify syncs (Phase 5) - up to 5 concurrent with 500ms rate limiting

**Sequential Constraints** (must run in order):
- Phase 0 → Phase 1 (bootstrap)
- Phase 1 → Gate 1 → Phase 2 (queue needed before research)
- Phase 2 → Phase 3 per product (research needed before generation)
- Phase 3 → Gate 2 → Phase 3.5 (decision point for photos)
- Phase 3.5 → Phase 4 per product (photos optional, QA is mandatory)
- Phase 4 → Gate 3 → Phase 5 (sync approval decision)
- Phase 5 → Gate 4 (sync verification)

**Parallelization Strategy**: Dynamic Queue Per Phase
\`\`\`yaml
# Phase 2: All 5 products in parallel
phase_2_research:
  max_concurrent: 5
  queue: [product_1, product_2, product_3, product_4, product_5]
  duration: ~12min (5 products × 12min, parallelized)

# Wait for all Phase 2 complete

# Phase 3: All 5 products in parallel
phase_3_generation:
  max_concurrent: 5
  queue: [product_1, product_2, product_3, product_4, product_5]
  duration: ~14min

# Gate 2: Fast pre-check on all 5 products
gate_2_fast_precheck:
  max_concurrent: 5
  criteria: 5 quick checks
  decision: Which products get Phase 3.5 (photos)?

# Phase 3.5: Photos in batches (LLM-limited)
phase_3_5_photo_prompts:
  max_concurrent: 3  # LLM token limits
  batch_1: [product_1, product_2, product_3]
  batch_2: [product_4, product_5]
  duration: ~15min per batch

# Phase 4: All 5 products validated in parallel
phase_4_validation:
  max_concurrent: 5
  queue: [product_1, product_2, product_3, product_4, product_5]
  duration: ~2min per product

# Gate 3: Comprehensive QA on all 5 products
gate_3_comprehensive_qa:
  max_concurrent: 5
  criteria: 13 comprehensive checks
  decision: Which products sync to Shopify?

# Phase 5: Approved products sync in parallel
phase_5_sync:
  max_concurrent: 5
  rate_limiter: 500ms between API calls
  queue: [approved_product_1, approved_product_2, ...]
  duration: ~1min per product

# Gate 4: Verify sync success
gate_4_post_sync:
  max_concurrent: 1  # Sequential check
  criteria: sync success + error count
\`\`\`

**Total Time Estimate** (22 products):
- Phase 2 (research): 12 min (5 concurrent)
- Phase 3 (generation): 14 min (5 concurrent)
- Gate 2: 1 min
- Phase 3.5 (photos): 15 min (2 batches of 3)
- Phase 4 (validation): 2 min (5 concurrent)
- Gate 3: 1 min
- Phase 5 (sync): 1 min (5 concurrent)
- Gate 4: 1 min
- **Total**: ~47 min (vs. ~120 min sequentially, or ~60 min with old 3-concurrent model)
```

---

## CHANGE 10: Update PHASE 5 Step 5.1 (Lines 445-455)

### BEFORE
```python
# Using sync_all_shopify.py pattern
for product in approved_products:
    result = sync_to_shopify(product.id, service_key)
    if result.success:
        update_checkpoint(product.id, "synced")
    else:
        log_error(product.id, result.error)
```

### AFTER
```python
# Using unified-sync Edge Function (recommended)
from anuncio_agent.scripts.unified_sync import call_unified_sync

# Batch sync all approved products
result = call_unified_sync(
    mode="push",           # Supabase → Shopify
    scope="content",       # Only ad copy + images (no price/inventory)
    dry_run=False,
    force=False            # Respect timestamps
)

# Process results
if result["success"]:
    stats = result["stats"]
    print(f"Synced: {stats['synced']}/{stats['total']} products")
    print(f"  Created: {stats['created']}")
    print(f"  Updated: {stats['updated']}")
    print(f"  Errors: {stats['errors']}")

    # Update checkpoint with successful syncs
    for product in result["products"]:
        if product["action"] in ["created", "updated"]:
            update_checkpoint(product["id"], "synced", timestamp=now())
        elif product["action"] == "error":
            log_error(product["id"], product["error"])
else:
    print(f"Sync failed: {result['error']}")
    gate_4_status = "CRITICAL"
```

---

## CHANGE 11: Update ERROR HANDLING Table (Lines 577-588)

### ADD NEW ROWS

```markdown
| Error Type | Action | Continue Batch? |
|------------|--------|-----------------|
| Marketplace search failed | Retry 2x, then skip product | YES |
| Research incomplete (< 3 competitors) | Flag LOW_DATA, continue | YES |
| Ad generation failed | Retry 1x, then skip | YES |
| Photo generation failed | Log WARNING, flag PHOTO_OPTIONAL, continue | YES |
| QA score < 0.70 | Skip sync, log for review (Gate 3) | YES |
| Gate 2 fast-check FAIL | Skip photos, proceed to full QA (Gate 3) | YES |
| Gate 3 comprehensive QA FAIL | Do not sync, flag for manual intervention | YES |
| Unified-sync timeout (> 300s) | Retry 1x, if fails move to manual review | YES |
| Unified-sync conflict (timestamp) | Use newer version, log for review | YES |
| Unified-sync rate limit (429) | Wait 30s, retry from checkpoint | PAUSE |
| Gate 4 post-sync FAIL (>3 errors) | PAUSE batch, require --force-continue | PAUSE |
| Supabase connection lost | Pause, wait 30s, retry | PAUSE |
| Rate limit hit | Wait 60s, continue | PAUSE |
```

---

## CHANGE 12: Update RELATED FILES section (Lines 666-684)

### BEFORE
```markdown
**ADWs Orchestrated**:
- `pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md` (research methodology)
- `anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md` (ad generation)

**Plans Used**:
- `pesquisa_agent/config/plans/standard_research.json`
- `anuncio_agent/plans/full_anuncio.json`

**Scripts**:
- `anuncio_agent/scripts/sync_all_shopify.py` (sync pattern)
- `anuncio_agent/scripts/reform_product.py` (single product)
```

### AFTER
```markdown
**ADWs Orchestrated**:
- `pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md` (research methodology)
- `anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md` (ad generation)
- `photo_agent/workflows/100_ADW_RUN_PHOTO.md` (photo prompt generation)

**Plans & Configs Used**:
- `pesquisa_agent/config/plans/standard_research.json`
- `anuncio_agent/plans/full_anuncio.json`
- `photo_agent/config/scenes/9_scene_grid.json`
- `photo_agent/config/pnl_triggers.json`

**Sync Scripts & Edge Functions**:
- `anuncio_agent/scripts/unified_sync.py` (Python wrapper for unified-sync Edge Fn)
- `anuncio_agent/scripts/sync_all_shopify.py` (legacy, fallback)
- `anuncio_agent/scripts/reform_product.py` (single product)
- Edge Function: `unified-sync` (Supabase) - Bidirectional sync with conflict resolution
- Edge Function: `sync-shopify-product` (Supabase) - Legacy per-product sync (fallback)
```

---

## CHANGE 13: Update EXECUTION MODES (Lines 520-542)

### BEFORE
```bash
### Mode A: Full Batch (Recommended for 22 products)

# Execute via slash command
/reform-batch --limit 22 --parallel 3

# Or manual execution
1. Load this ADW
2. Execute Phase 1 (discovery)
3. Loop Phases 2-4 for each product
4. Execute Phase 5 (sync + report)

Estimated Time: 22 products × 15min/product = ~5.5 hours (with parallelization: ~2 hours)
```

### AFTER
```bash
### Mode A: Full Batch with Optimizations (Recommended for 22 products)

# Execute via slash command with all optimizations
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync --quality-gates 3

# Or manual execution
1. Load this ADW
2. Execute Phase 1 (discovery) + Gate 1 (knowledge check)
3. Execute Phase 2 (research) for all 5 products in parallel
4. Execute Phase 3 (generation) for all 5 products in parallel
   - Gate 2 (fast pre-check) on all 5
5. Execute Phase 3.5 (photos) for 3 products in parallel, then next batch
6. Execute Phase 4 (validation) for all products in parallel
   - Gate 3 (comprehensive QA) on all 5
7. Execute Phase 5 (sync) for approved products in parallel
   - Gate 4 (post-sync verify)
8. Generate batch report with all quality metrics

Estimated Time: 22 products × 10min/product = ~3.7 hours (with parallelization: ~1.3 hours)
Improvement: 35% faster than previous 2-hour estimate
```

---

## CHANGE 14: Update SLASH COMMAND INTEGRATION (Lines 559-573)

### BEFORE
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

### AFTER
```markdown
# /reform-batch - Execute Integrated Product Reform (v2.0)

## Parameters
- `--limit N`: Max products to process (default: all)
- `--parallel N`: Concurrent products (default: 5, max: 5)
- `--photo-prompts`: Enable Phase 3.5 photo generation (default: true)
- `--unified-sync`: Use unified-sync Edge Function (default: true)
- `--quality-gates N`: Enable quality gates 0-4 (default: 3)
- `--dry-run`: Simulate without syncing to Shopify
- `--product-ids`: Comma-separated specific IDs
- `--resume-batch ID`: Resume from checkpoint (batch_id)
- `--force`: Skip timestamp checks, always push to Shopify
- `--no-photo-prompts`: Disable photo generation (speed mode)

## Execution
1. Read ADW: `codexa_agent/workflows/204_ADW_INTEGRATED_PRODUCT_REFORM.md`
2. Execute 6 phases with 4 quality gates:
   - Phase 1 + Gate 1 (knowledge)
   - Phase 2 (research) - 5 concurrent
   - Phase 3 (generation) - 5 concurrent
   - Gate 2 (fast pre-check)
   - Phase 3.5 (photos) - 3 concurrent batches
   - Phase 4 (validation) - 5 concurrent
   - Gate 3 (comprehensive QA)
   - Phase 5 (sync) - unified-sync Edge Function
   - Gate 4 (post-sync verify)
3. Generate comprehensive batch report with quality metrics
4. Return summary and detailed results to user

## Examples

# Full batch with all optimizations
/reform-batch --limit 22 --parallel 5 --photo-prompts --unified-sync --quality-gates 3

# Conservative (manual review mode)
/reform-batch --limit 5 --parallel 2 --quality-gates 4 --dry-run

# Resume from checkpoint
/reform-batch --resume-batch reform_2025-11-29_001

# Single product with photos
/reform-batch --product-ids abc123 --photo-prompts

# Speed mode (skip photos)
/reform-batch --no-photo-prompts --parallel 5
```

---

## CHANGE 15: Update Batch Report Template (Lines 477-484)

### ADD TO PRODUCT RESULTS TABLE

```markdown
## Product Results

| # | Product | Research | Ad Gen | Photos | QA Score | Synced | Notes |
|---|---------|----------|--------|--------|----------|--------|-------|
| 1 | [name]  | OK       | OK     | OK     | 0.92     | YES    | -     |
| 2 | [name]  | OK       | OK     | OK     | 0.87     | YES    | -     |
| 3 | [name]  | LOW_DATA | OK     | WARN   | 0.78     | NO     | Photo quality < 0.80 |
| 4 | [name]  | OK       | OK     | N/A    | 0.85     | YES    | Skipped photos (Gate 2 WARN) |

*Legend*: OK = Passed | WARN = Warning, check notes | LOW_DATA = Incomplete but continued | N/A = Not applicable (skipped)
```

### INSERT NEW SECTIONS BEFORE "Failed Products"

```markdown
## Quality Gate Results

| Gate | Phase | Name | Products Passed | Warned | Failed | Status |
|------|-------|------|-----------------|--------|--------|--------|
| 1 | 1→2 | Knowledge Load | 22 | 0 | 0 | PASS |
| 2 | 3→3.5 | Fast Pre-Check | 22 | 0 | 0 | PASS |
| 3 | 4→5 | Comprehensive QA | 20 | 2 | 0 | PASS_WITH_WARNINGS |
| 4 | 5_end | Post-Sync Verify | 20 | 0 | 0 | PASS |

**Summary**: 91% passed all gates, 9% flagged for manual review next batch, 0% critical failures

---

## Photo Prompt Generation Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Total Prompts Generated | 20 | 2 products skipped (Gate 2 WARN) |
| Avg Generation Time | 12.5 min | LLM-bound, 3 concurrent |
| Avg Prompt Quality Score | 0.87 | 13-point validation |
| Grid 3x3 Prompts | 20 | 100% compliance |
| Individual 9-Scene Prompts | 180 | 9 × 20 products |
| Marketplace Compliance Pass | 20/20 | Scenes 1+9 = white #FFFFFF |
| Seed Values Generated | 180 | For image reproducibility |
| Generation Errors | 0 | No failures, 100% success rate |

---
```

---

## CHANGE 16: Update METADATA Section (Lines 687-702)

### BEFORE
```markdown
## METADATA

**Created**: 2025-11-29
**Author**: CODEXA Meta-Constructor
**Version**: 1.0.0
**Type**: Orchestration ADW (coordinates multiple agents)
**Agents**: pesquisa_agent + anuncio_agent + sync_shopify
**Phases**: 5
**Estimated Duration**: 15min/product (batch), 45-60min/product (single)
```

### AFTER
```markdown
## METADATA

**Created**: 2025-11-29
**Last Updated**: 2025-12-04
**Author**: CODEXA Meta-Constructor
**Version**: 2.0.0 (Optimized)
**Type**: Orchestration ADW (coordinates multiple agents + quality gates)
**Agents Orchestrated**: pesquisa_agent + anuncio_agent + photo_agent + sync_shopify
**Phases**: 6 (added Phase 3.5: Photo Prompts)
**Quality Gates**: 4 (Knowledge + Fast PreCheck + Comprehensive QA + Post-Sync)
**Parallelization**: 5 concurrent products (3 for Phase 3.5)
**Estimated Duration**:
  - Single product: 45-60min
  - Batch (22 products): ~1.3 hours (with 5 concurrent + photos)
  - Previous estimate: ~2 hours (35% improvement)
**Key Improvements**:
  - +1 photo generation phase (Phase 3.5)
  - +3 quality gates for fail-fast validation
  - +67% parallelization (3→5 products)
  - 35% faster batch processing
  - Replaced sync_all_shopify.py with unified-sync Edge Function
```

---

**Total Changes**: 16 sections across the entire file
**Estimated Edit Time**: 2-3 hours
**Recommended Approach**: Apply changes in order (1-16), test after each phase addition
