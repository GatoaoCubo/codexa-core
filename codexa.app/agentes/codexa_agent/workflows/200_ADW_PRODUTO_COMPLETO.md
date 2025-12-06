# 200_ADW_PRODUTO_COMPLETO | End-to-End Product Creation Pipeline

**Purpose**: Create complete product from reference (URL/image) to published listing with real-time dashboard
**Type**: 11-Phase ADW | **Duration**: ~15-30min
**Output**: Product live on Supabase + Shopify with 9 AI-generated images + Preview page
**Architecture**: Multi-Agent Orchestration (Parallel Execution) + Pipeline Live Dashboard
**Status**: Production-Ready | **Version**: 2.0.0
**Dashboard**: http://localhost:3456 (Pipeline Live tab)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_produto_completo",
  "workflow_name": "Complete Product Creation Pipeline with Dashboard",
  "agent": "codexa_agent (orchestrator)",
  "version": "2.0.0",
  "context_strategy": "rolling_window",
  "failure_handling": "retry_then_report",
  "min_llm_model": "claude-sonnet-4+ or gpt-4+",
  "dashboard_url": "http://localhost:3456",
  "pipeline_state_file": "outputs/pipeline_state.json",

  "required_capabilities": {
    "parallel_agent_execution": true,
    "image_generation_api": true,
    "supabase_storage": true,
    "shopify_sync": true,
    "pipeline_emitter": true
  },

  "agents_involved": [
    "pesquisa_agent",
    "anuncio_agent",
    "photo_agent",
    "codexa_agent"
  ],

  "external_apis": [
    "Gemini 2.5 Flash (imagen-3.0-generate-002)",
    "Supabase Storage",
    "Supabase Database",
    "Shopify Admin API"
  ],

  "phases": [
    {"phase_id": "phase_1_input", "name": "Input Capture", "duration": "1min", "agent": "user"},
    {"phase_id": "phase_2_identification", "name": "Product Identification", "duration": "2min", "agent": "pesquisa_agent"},
    {"phase_id": "phase_3_content", "name": "Content Generation", "duration": "5min", "agent": "anuncio_agent"},
    {"phase_id": "phase_4_prompts", "name": "Image Prompts", "duration": "3min", "agent": "photo_agent"},
    {"phase_id": "phase_5_images", "name": "Image Generation", "duration": "5min", "agent": "gemini_api"},
    {"phase_id": "phase_6_upload", "name": "Storage Upload", "duration": "2min", "agent": "codexa_agent"},
    {"phase_id": "phase_7_supabase", "name": "Database Insert", "duration": "1min", "agent": "codexa_agent"},
    {"phase_id": "phase_8_preview", "name": "Preview Generation", "duration": "1min", "agent": "codexa_agent"},
    {"phase_id": "phase_9_shopify", "name": "Shopify Sync", "duration": "1min", "agent": "edge_function"},
    {"phase_id": "phase_10_validation", "name": "Validation", "duration": "1min", "agent": "codexa_agent"},
    {"phase_id": "phase_11_commit", "name": "Git Commit & Push", "duration": "1min", "agent": "codexa_agent"}
  ]
}
```

---

## PIPELINE EMITTER INTEGRATION

### Initialization (Before Phase 1)

```python
from builders.pipeline_emitter import PipelineEmitter

# Initialize pipeline with product name
emitter = PipelineEmitter(product_name="Nome do Produto")

# Custom phases (if different from default)
custom_phases = [
    {"id": "pesquisa", "name": "Market Research", "status": "pending", "progress": 0},
    {"id": "anuncio", "name": "Ad Copy", "status": "pending", "progress": 0},
    {"id": "photo", "name": "Photo Prompts", "status": "pending", "progress": 0},
    {"id": "images", "name": "Image Gen", "status": "pending", "progress": 0},
    {"id": "preview", "name": "Preview Page", "status": "pending", "progress": 0},
    {"id": "shopify", "name": "Shopify Sync", "status": "pending", "progress": 0},
]
emitter = PipelineEmitter(product_name, phases=custom_phases)
```

### Per-Phase Integration Pattern

```python
# At phase start
emitter.start_phase("pesquisa", "Market Research")
emitter.emit_thought("pesquisa_agent", "Iniciando analise de mercado...")

# During execution
emitter.update_progress("pesquisa", 50, "Analyzing competitors")
emitter.emit_thought("pesquisa_agent", "47 listings analisados no Mercado Livre")

# At phase end
emitter.complete_phase("pesquisa", quality_score=0.85, outputs={"keywords_count": 47})

# Update preview results (optional)
emitter.update_results({
    "title_preview": "Garrafa Termica Inox Gato - 500ml",
    "keywords_preview": ["garrafa termica", "inox", "gato"],
    "images_generated": 9
})
```

### Dashboard Communication

- **State File**: `outputs/pipeline_state.json` (auto-updated by emitter)
- **Dashboard URL**: http://localhost:3456 (Pipeline Live tab)
- **Polling**: 1s interval (WebSocket fallback for Windows)

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

**Objective**: Generate 9 product images using AI with original image reference

**API**: Gemini 2.5 Flash (`gemini-2.5-flash-preview-05-20`) + Imagen 3.0 (`imagen-3.0-generate-002`)

> **HARD RULE**: Every image generation call MUST include the original product image as reference.
> See: `photo_agent/prompts/30_prompt_generator_HOP.md` for detailed requirements.

**Actions**:
1. Initialize Google GenAI client
2. Load original product image (REQUIRED)
3. For each prompt in priority order:
   - Call `client.models.generate_images()` WITH `reference_images`
   - Emit progress to dashboard
   - Save PNG to `imagens_geradas/`
4. Log generation results

**Code Reference**:
```python
from google import genai
from google.genai import types
from PIL import Image
from builders.pipeline_emitter import emit_thought, update_progress, start_phase, complete_phase

client = genai.Client(api_key=GOOGLE_API_KEY)

# OBRIGATORIO: Carregar imagem original
imagem_original = Image.open("imagem_original.webp")

# Emitir inicio da fase
start_phase("images", "Image Generation")

for i, prompt in enumerate(prompts, 1):
    emit_thought("gemini_api", f"Gerando imagem {i}/9: {prompt['id']}...")
    update_progress("images", int((i / 9) * 100), f"Image {i}/9")

    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt["text"],
        reference_images=[imagem_original],  # OBRIGATORIO - NUNCA OMITIR
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=prompt.get("aspect_ratio", "4:3"),
        )
    )

    # Save image
    filepath = f"imagens_geradas/{prompt['id']}_{i}.png"
    with open(filepath, 'wb') as f:
        f.write(response.generated_images[0].image.image_bytes)

    emit_thought("gemini_api", f"Imagem {i}/9 salva: {filepath}")

complete_phase("images", quality_score=0.95, outputs={"images_count": 9})
```

**Output**: 9 PNG files in `imagens_geradas/`

**Validation**:
- ✅ 9 images generated
- ✅ File sizes > 100KB each
- ✅ No generation errors
- ✅ **All images used original as reference** (consistency check)

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

## PHASE 8: PREVIEW GENERATION

**Objective**: Generate product preview page for validation before Shopify sync

**Output**: `preview.html` accessible at http://localhost:3456/preview.html

**Actions**:
1. Collect all generated data ($product_data + $anuncio_data + $image_urls)
2. Generate preview HTML from template
3. Save to `USER_DOCS/produtos/{slug}/preview.html`
4. Emit completion to dashboard
5. Open preview URL for user validation

**Code Reference**:
```python
from builders.pipeline_emitter import start_phase, complete_phase, emit_thought
from jinja2 import Template

start_phase("preview", "Preview Generation")
emit_thought("codexa_agent", "Gerando pagina de preview...")

# Load preview template
template = Template(open("templates/preview_template.html").read())

# Render with product data
preview_html = template.render(
    product_name=product_data["name"],
    title=anuncio_data["seo_title"],
    description=anuncio_data["description"],
    long_description=anuncio_data["long_description"],
    benefits=anuncio_data["benefits_functional"],
    faq=anuncio_data["faq"],
    keywords=anuncio_data["keywords"][:10],
    images=image_urls,
    price=product_data.get("price", 0),
)

# Save preview
preview_path = f"USER_DOCS/produtos/{slug}/preview.html"
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(preview_html)

emit_thought("codexa_agent", f"Preview salvo: {preview_path}")
complete_phase("preview", quality_score=0.90, outputs={"preview_url": f"http://localhost:3456/preview.html?product={slug}"})

# Also update results for dashboard preview
update_results({
    "preview_url": f"http://localhost:3456/preview.html?product={slug}",
    "preview_ready": True
})
```

**Preview Page Features**:
- 9-image gallery with lightbox
- Product specs section
- Keywords display
- Bullet points (benefits)
- Long description
- FAQ accordion
- Price display

**Validation**:
- ✅ Preview HTML generated
- ✅ All 9 images displayed correctly
- ✅ All text content populated
- ✅ Accessible at dashboard URL

---

## PHASE 9: SHOPIFY SYNC

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

## PHASE 10: VALIDATION

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

## PHASE 11: GIT COMMIT & PUSH

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
Timeline (optimized with Dashboard):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: INPUT ────────┐                              [Dashboard: pipeline_state.json]
                       │                                        ↓
                       ├──→ Phase 2: PESQUISA ──────┐          emit_thought()
                       │                            │          update_progress()
                       ├──→ Phase 3: ANUNCIO ───────┼──→ MERGE
                       │                            │
                       └──→ Phase 4: PHOTO_PROMPTS ─┘
                                                    │
Phase 5: IMAGE_GEN ←────────────────────────────────┘  [HARD RULE: imagem_original]
         │
Phase 6: UPLOAD ←───────┘
         │
Phase 7: SUPABASE ←─────┘
         │
Phase 8: PREVIEW ←──────┘  [NEW: http://localhost:3456/preview.html]
         │
Phase 9: SHOPIFY ←──────┘
         │
Phase 10: VALIDATION ←──┘
         │
Phase 11: COMMIT ←──────┘

Parallel Groups:
- Group A: Phases 2, 3, 4 (can run simultaneously)
- Group B: Phases 5-11 (sequential, depends on A)

Dashboard Integration:
- All phases emit to pipeline_state.json
- Dashboard polls every 1s (WebSocket fallback)
- Live thoughts stream visible in Pipeline Live tab
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
- ✅ All 11 phases completed
- ✅ Duration < 30 minutes
- ✅ Quality score >= 0.8
- ✅ Dashboard shows all phases green

### Output Level
- ✅ 9 images generated with original reference (consistency)
- ✅ Product live in Supabase
- ✅ Preview page accessible
- ✅ Product synced to Shopify
- ✅ All files committed to repo

### Business Level
- ✅ Product visible on storefront
- ✅ Price and inventory correct
- ✅ SEO metadata complete
- ✅ Preview validated before publish

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

**v2.0.0** (2025-12-05):
- **Pipeline Live Dashboard Integration**
  - Added pipeline_emitter.py integration for real-time updates
  - Dashboard URL: http://localhost:3456 (Pipeline Live tab)
  - State file: outputs/pipeline_state.json
  - Polling 1s (WebSocket fallback for Windows)
- **New Phase 8: Preview Generation**
  - Preview page before Shopify sync
  - URL: http://localhost:3456/preview.html
  - 9-image gallery + specs + keywords + FAQ
- **Image Model Update**
  - Changed from Imagen 4.0 to Gemini 2.5 Flash
  - Model: gemini-2.5-flash-preview-05-20 + imagen-3.0-generate-002
  - HARD RULE: reference_images obrigatorio
- **11-phase pipeline** (was 10)
- Updated parallel execution diagram

**v1.0.0** (2025-12-05):
- Initial workflow creation
- 10-phase pipeline
- Parallel execution support
- Google Imagen 4.0 integration
- Supabase Storage + Shopify sync
- Based on successful "Espelho Gatinho" execution

---

## CONSOLIDATED TEMPLATES (v2.1.0)

Reusable templates for scaling product creation:

```
codexa.app/templates/produto_completo/
├── README.md                      → Quick start guide
├── TEMPLATE_PRODUTO.md            → Product documentation (80+ placeholders)
├── TEMPLATE_PHOTO_PROMPTS.json    → 9 photo prompts (50+ placeholders)
├── generate_images_universal.py   → Auto-detect image generation script
└── preview_template.html          → Preview HTML (30+ placeholders)
```

### Key Placeholders
- `{{PRODUCT_NAME}}` → Full product name
- `{{PRODUCT_SLUG}}` → URL-friendly slug
- `{{PRODUCT_DISTINCTIVE_FEATURE}}` → Unique selling point
- `{{LIFESTYLE_*_NAME}}` → Lifestyle scene names
- `{{EMOTIONAL_THEME}}` → Brand connection theme

### Scale Workflow (15 min/product)
1. Copy templates to `user_research/{{PRODUCT_SLUG}}/`
2. Run `/prime-pesquisa` → `product_data.json`
3. Run `/prime-anuncio` → `anuncio_completo.md`
4. Run `/prime-photo` → `photo_prompts.json`
5. Run `python generate_images.py` → 9 images
6. Serve `preview.html` → validate

**Full documentation**: `codexa.app/templates/produto_completo/README.md`

---

**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor
**Dashboard**: http://localhost:3456 (Pipeline Live tab)
**Reference Implementation**: `user_research/garrafa_termica_gato/`
**Templates**: `codexa.app/templates/produto_completo/`
