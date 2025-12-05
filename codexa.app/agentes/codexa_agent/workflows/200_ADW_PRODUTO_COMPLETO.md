# 200_ADW_PRODUTO_COMPLETO | End-to-End Product Creation Pipeline

**Purpose**: Create complete product from reference (URL/image) to published listing
**Type**: 10-Phase ADW | **Duration**: ~15-30min
**Output**: Product live on Supabase + Shopify with 9 AI-generated images
**Architecture**: Multi-Agent Orchestration (Parallel Execution)
**Status**: Production-Ready | **Version**: 1.0.0

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_produto_completo",
  "workflow_name": "Complete Product Creation Pipeline",
  "agent": "codexa_agent (orchestrator)",
  "version": "1.0.0",
  "context_strategy": "rolling_window",
  "failure_handling": "retry_then_report",
  "min_llm_model": "claude-sonnet-4+ or gpt-4+",

  "required_capabilities": {
    "parallel_agent_execution": true,
    "image_generation_api": true,
    "supabase_storage": true,
    "shopify_sync": true
  },

  "agents_involved": [
    "pesquisa_agent",
    "anuncio_agent",
    "photo_agent",
    "codexa_agent"
  ],

  "external_apis": [
    "Google Imagen 4.0",
    "Supabase Storage",
    "Supabase Database",
    "Shopify Admin API"
  ],

  "phases": [
    {"phase_id": "phase_1_input", "name": "Input Capture", "duration": "1min", "agent": "user"},
    {"phase_id": "phase_2_identification", "name": "Product Identification", "duration": "2min", "agent": "pesquisa_agent"},
    {"phase_id": "phase_3_content", "name": "Content Generation", "duration": "5min", "agent": "anuncio_agent"},
    {"phase_id": "phase_4_prompts", "name": "Image Prompts", "duration": "3min", "agent": "photo_agent"},
    {"phase_id": "phase_5_images", "name": "Image Generation", "duration": "5min", "agent": "imagen_api"},
    {"phase_id": "phase_6_upload", "name": "Storage Upload", "duration": "2min", "agent": "codexa_agent"},
    {"phase_id": "phase_7_supabase", "name": "Database Insert", "duration": "1min", "agent": "codexa_agent"},
    {"phase_id": "phase_8_shopify", "name": "Shopify Sync", "duration": "1min", "agent": "edge_function"},
    {"phase_id": "phase_9_validation", "name": "Validation", "duration": "1min", "agent": "codexa_agent"},
    {"phase_id": "phase_10_commit", "name": "Git Commit & Push", "duration": "1min", "agent": "codexa_agent"}
  ]
}
```

---

## PREREQUISITES

**Before starting, ensure:**

1. **API Keys Configured** (in `codexa-core/.env`):
   - `GOOGLE_API_KEY` - Imagen 4.0 image generation
   - `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` - Database & Storage
   - Shopify token configured in Supabase Edge Functions

2. **Supabase Ready**:
   - Storage bucket exists (public)
   - `products` table schema matches expected fields
   - Edge Function `sync-shopify-product` deployed

3. **Dependencies Installed**:
   ```bash
   pip install google-genai  # For Imagen 4.0
   ```

---

## PHASE 1: INPUT CAPTURE

**Objective**: Collect product reference from user

**Input Types** (any one):
- URL do produto (Shopee, Mercado Livre, AliExpress)
- Imagem do produto (local path ou URL)
- Descricao textual do produto

**Actions**:
1. Receive input from user
2. Identify input type (URL, image, text)
3. If URL: Extract product image and basic info
4. If image: Analyze with vision model
5. Create `$product_reference` object

**Output**:
```json
{
  "reference_type": "url|image|text",
  "source_url": "https://...",
  "source_image": "path/to/image.webp",
  "initial_description": "...",
  "detected_category": "..."
}
```

**Validation**:
- ✅ At least one valid input received
- ✅ Image accessible (if URL)
- ✅ Product identifiable

---

## PHASE 2: PRODUCT IDENTIFICATION

**Objective**: Extract complete product information

**Agent**: `pesquisa_agent` (can run in parallel with Phase 3)

**Actions**:
1. Analyze reference image/URL
2. Identify product category
3. Extract features, dimensions, materials
4. Research competitor pricing
5. Identify target audience

**Output**: `$product_data`
```json
{
  "name": "Product Name",
  "category": "Category",
  "features": ["feature1", "feature2"],
  "materials": ["material1"],
  "dimensions": "...",
  "colors": ["color1", "color2"],
  "target_audience": "...",
  "price_range": {"min": 0, "max": 0}
}
```

---

## PHASE 3: CONTENT GENERATION

**Objective**: Generate all textual content for listing

**Agent**: `anuncio_agent` (ADW: 100_ADW_RUN_ANUNCIO)

**Can run in PARALLEL with Phase 2** (uses initial reference)

**Actions**:
1. Generate SEO-optimized titles (3 variants)
2. Expand keywords (60+ keywords)
3. Create bullet points (10 benefits)
4. Write long description
5. Generate FAQ (5 Q&As)
6. Create video script (30s)

**Output**: `$anuncio_data`
```json
{
  "titles": ["title1", "title2", "title3"],
  "keywords": ["kw1", "kw2", ...],
  "seo_title": "...",
  "seo_description": "...",
  "description": "...",
  "long_description": "...",
  "benefits_functional": [...],
  "benefits_emotional": [...],
  "faq": [{"q": "...", "a": "..."}],
  "video_script": "..."
}
```

---

## PHASE 4: IMAGE PROMPTS GENERATION

**Objective**: Create 9 professional image prompts

**Agent**: `photo_agent`

**Can run in PARALLEL with Phases 2-3**

**Actions**:
1. Load photo_agent PRIME.md
2. Generate 9 prompts following the standard set:
   - HERO_WHITE (priority: HIGH)
   - HERO_GRADIENT (priority: HIGH)
   - SCALE_HAND (priority: HIGH)
   - LIFESTYLE_VANITY
   - LIFESTYLE_BEDROOM
   - DETAIL_MIRROR
   - DETAIL_JEWELRY
   - SOCIAL_FLATLAY
   - SOCIAL_AESTHETIC

**Output**: `$photo_prompts`
```json
{
  "prompts": [
    {
      "id": "HERO_WHITE",
      "tipo": "hero",
      "prompt_midjourney": "...",
      "prompt_dalle": "...",
      "aspect_ratio": "4:3",
      "priority": "HIGH"
    },
    ...
  ]
}
```

---

## PHASE 5: IMAGE GENERATION

**Objective**: Generate 9 product images using AI

**API**: Google Imagen 4.0 (`imagen-4.0-generate-001`)

**Actions**:
1. Initialize Google GenAI client
2. For each prompt in priority order:
   - Call `client.models.generate_images()`
   - Save PNG to `imagens_geradas/`
3. Log generation results

**Code Reference**:
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GOOGLE_API_KEY)

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt=prompt_text,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="4:3",
    )
)

# Save image
with open(filepath, 'wb') as f:
    f.write(response.generated_images[0].image.image_bytes)
```

**Output**: 9 PNG files in `imagens_geradas/`

**Validation**:
- ✅ 9 images generated
- ✅ File sizes > 100KB each
- ✅ No generation errors

---

## PHASE 6: STORAGE UPLOAD

**Objective**: Upload images to Supabase Storage

**Storage**: Supabase Storage (public bucket)

**Actions**:
1. Connect to Supabase Storage API
2. For each image:
   - Upload to `produtos/{slug}/{filename}.png`
   - Get public URL (with proper URL encoding)
3. Collect all URLs

**Code Reference**:
```python
# Upload to Supabase Storage
api_url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{object_path}"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "image/png",
    "x-upsert": "true",
}

# POST file data
# Get public URL (URL-encoded for special chars)
public_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_encoded}/{object_path}"
```

**Output**: `$image_urls` (list of 9 public URLs)

**Important**: URL-encode bucket names with special characters!

---

## PHASE 7: DATABASE INSERT

**Objective**: Create product record in Supabase

**Table**: `products`

**Actions**:
1. Merge all data: `$product_data` + `$anuncio_data` + `$image_urls`
2. Set price and quantity (from user input or defaults)
3. Insert into Supabase `products` table
4. Store returned `product_id`

**Required Fields**:
```json
{
  "name": "...",
  "slug": "...",
  "description": "...",
  "long_description": "...",
  "price": 0.00,
  "quantity": 0,
  "status": "published",
  "images": ["url1", "url2", ...],
  "seo_title": "...",
  "seo_description": "...",
  "seo_keywords": [...],
  "features": [...],
  "benefits_functional": [...],
  "benefits_emotional": [...],
  "faq": [...],
  "shopify_sync_enabled": true,
  "inventory_sync_enabled": true
}
```

**Output**: `$product_id` (UUID)

---

## PHASE 8: SHOPIFY SYNC

**Objective**: Sync product to Shopify via Edge Function

**Edge Function**: `sync-shopify-product`

**Actions**:
1. Call Edge Function with `$product_id`
2. Function creates/updates product in Shopify
3. Function uploads images from URLs
4. Function updates inventory
5. Returns Shopify IDs

**Code Reference**:
```python
api_url = f"{SUPABASE_URL}/functions/v1/sync-shopify-product"
headers = {
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}
body = {"productId": product_id}

# Returns: shopifyProductId, shopifyVariantId
```

**Output**:
```json
{
  "shopify_product_id": "...",
  "shopify_variant_id": "...",
  "success": true
}
```

---

## PHASE 9: VALIDATION

**Objective**: Verify product is live and correct

**Actions**:
1. Query Supabase for product (verify all fields)
2. Check Shopify product exists
3. Verify images are accessible
4. Calculate quality score

**Validation Checklist**:
- ✅ Product in Supabase with all fields
- ✅ Images array has 9 URLs
- ✅ Shopify IDs populated
- ✅ Product accessible on store URL
- ✅ Price and inventory correct

**Quality Score Calculation**:
```
score = (
  0.2 * (images_count / 9) +
  0.2 * (keywords_count >= 50) +
  0.2 * (has_long_description) +
  0.2 * (has_faq) +
  0.2 * (shopify_synced)
)
```

---

## PHASE 10: GIT COMMIT & PUSH

**Objective**: Save all assets to repository

**Actions**:
1. Add all files in product folder
2. Create commit with standard message
3. Push to remote

**Commit Message Template**:
```
feat(produto): add {product_name}

- {N} images generated with Imagen 4.0
- Product created in Supabase (R${price}, {qty} units)
- Synchronized with Shopify (ID: {shopify_id})
- Quality score: {score}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Output Structure**:
```
USER_DOCS/produtos/{slug}/
├── README.md
├── produto.json
├── anuncio.json
├── photo_prompts.json
├── video_script.md
├── imagem_original.webp
├── supabase_result.json
├── generate_images.py
├── upload_to_supabase.py
└── imagens_geradas/
    ├── HERO_WHITE_*.png
    ├── HERO_GRADIENT_*.png
    ├── SCALE_HAND_*.png
    ├── LIFESTYLE_VANITY_*.png
    ├── LIFESTYLE_BEDROOM_*.png
    ├── DETAIL_MIRROR_*.png
    ├── DETAIL_JEWELRY_*.png
    ├── SOCIAL_FLATLAY_*.png
    ├── SOCIAL_AESTHETIC_*.png
    └── generation_log.json
```

---

## PARALLEL EXECUTION STRATEGY

```
Timeline (optimized):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: INPUT ────────┐
                       │
                       ├──→ Phase 2: PESQUISA ──────┐
                       │                            │
                       ├──→ Phase 3: ANUNCIO ───────┼──→ MERGE
                       │                            │
                       └──→ Phase 4: PHOTO_PROMPTS ─┘
                                                    │
Phase 5: IMAGE_GEN ←────────────────────────────────┘
         │
Phase 6: UPLOAD ←───────┘
         │
Phase 7: SUPABASE ←─────┘
         │
Phase 8: SHOPIFY ←──────┘
         │
Phase 9: VALIDATION ←───┘
         │
Phase 10: COMMIT ←──────┘

Parallel Groups:
- Group A: Phases 2, 3, 4 (can run simultaneously)
- Group B: Phases 5-10 (sequential, depends on A)
```

---

## SPAWN COMMAND FOR PARALLEL EXECUTION

```
/spawn
1. pesquisa_agent: Identify product from reference image, extract features, materials, dimensions, target audience
2. anuncio_agent: Generate SEO titles, 60 keywords, 10 bullets, long description, FAQ, video script
3. photo_agent: Create 9 professional image prompts (HERO_WHITE, HERO_GRADIENT, SCALE_HAND, etc.)
```

**Merge Strategy**:
After spawn completes, merge outputs into single product structure before Phase 5.

---

## ERROR HANDLING

| Phase | Error | Recovery |
|-------|-------|----------|
| 5 | Image generation failed | Retry with simplified prompt |
| 6 | Upload failed | Retry with exponential backoff |
| 7 | DB insert failed | Check schema, fix field types |
| 8 | Shopify sync failed | Check URL encoding, retry |
| 9 | Validation failed | Log issues, manual review |

**Retry Policy**:
- Max retries: 3
- Backoff: 1s, 3s, 10s
- On final failure: Log and continue (graceful degradation)

---

## SUCCESS CRITERIA

### Pipeline Level
- ✅ All 10 phases completed
- ✅ Duration < 30 minutes
- ✅ Quality score >= 0.8

### Output Level
- ✅ 9 images generated and uploaded
- ✅ Product live in Supabase
- ✅ Product synced to Shopify
- ✅ All files committed to repo

### Business Level
- ✅ Product visible on storefront
- ✅ Price and inventory correct
- ✅ SEO metadata complete

---

## QUICK REFERENCE PATHS

**Scripts**:
```
generate_images.py    → Phase 5 (Image Generation)
upload_to_supabase.py → Phase 6 (Storage Upload)
create_product.py     → Phase 7 (DB Insert) + Phase 8 (Shopify)
```

**APIs**:
```
Imagen 4.0:     client.models.generate_images()
Supabase REST:  {SUPABASE_URL}/rest/v1/products
Supabase Storage: {SUPABASE_URL}/storage/v1/object/{bucket}/{path}
Shopify Sync:   {SUPABASE_URL}/functions/v1/sync-shopify-product
```

**Keys** (from `codexa-core/.env`):
```
GOOGLE_API_KEY
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
```

---

## TRIGGER COMMAND

```
/flow do "criar produto completo para [REFERENCIA]"
```

Or manual:
```
/prime-pesquisa → identify product
/prime-anuncio → generate content
/prime-photo → create prompts
→ execute Phase 5-10 scripts
```

---

## VERSION HISTORY

**v1.0.0** (2025-12-05):
- Initial workflow creation
- 10-phase pipeline
- Parallel execution support
- Google Imagen 4.0 integration
- Supabase Storage + Shopify sync
- Based on successful "Espelho Gatinho" execution

---

**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor
**Reference Implementation**: `gato3-landing-pages/USER_DOCS/produtos/espelho-gatinho-organizador-joias/`
