# ANUNCIO PIPELINE - Unified E-commerce Ad Generation System

**Version**: 2.5.0 | **Updated**: 2025-12-04 | **Status**: Production-Ready

Complete documentation for the unified anuncio pipeline: research → ad generation → photography

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Agent Chain: Research to Photos](#agent-chain-research-to-photos)
3. [Slash Commands](#slash-commands)
4. [Python Scripts & CLI](#python-scripts--cli)
5. [Edge Functions](#edge-functions)
6. [Quality Gates & Thresholds](#quality-gates--thresholds)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Configuration Reference](#configuration-reference)

---

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ANUNCIO UNIFIED PIPELINE                              │
└─────────────────────────────────────────────────────────────────────────────┘

INPUT SOURCES (Pesquisa Agent)
│
├─ Market Research     Research Notes    Product Brief
│  (Web Research)      (Markdown)        (JSON)
│
└──────────────────────┬──────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  PESQUISA AGENT (Research)   │
        │                              │
        │ • Competitor Analysis        │
        │ • Market Gaps                │
        │ • Price Intelligence         │
        │ • SEO Taxonomy               │
        │ • Customer Sentiment         │
        │                              │
        │ OUTPUT: research_notes.md    │
        └───────────────┬──────────────┘
                        │
                        ▼
        ┌──────────────────────────────┐
        │  ANUNCIO AGENT (Ad Copy)     │
        │                              │
        │ 7-Phase Pipeline:            │
        │  1. Parse Research           │
        │  2. Generate Titles (3x)     │
        │  3. Expand Keywords (2x)     │
        │  4. Write Bullet Points      │
        │  5. Compose Description      │
        │  6. Validate Compliance      │
        │  7. Calculate Persuasion     │
        │                              │
        │ OUTPUT:                      │
        │ ├─ anuncio.md               │
        │ ├─ anuncio.llm.json         │
        │ └─ anuncio.meta.json        │
        └───────────────┬──────────────┘
                        │
                        ▼
        ┌──────────────────────────────┐
        │  PHOTO AGENT (Visuals)       │
        │                              │
        │ • Grid 3x3 Master Prompt     │
        │ • 9 Individual Scene Prompts │
        │ • Lighting & Composition     │
        │ • Brand Integration          │
        │                              │
        │ OUTPUT:                      │
        │ ├─ grid_prompts.md          │
        │ └─ individual_prompts.md    │
        └───────────────┬──────────────┘
                        │
                        ▼
        ┌──────────────────────────────┐
        │  EDGE FUNCTIONS (Sync)       │
        │                              │
        │ • unified-sync               │
        │ • crud-sandbox               │
        │ • webhook-manager            │
        │                              │
        │ SYNCS:                       │
        │ Supabase ←→ Shopify ←→ LP   │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  MARKETPLACE PUBLISHING      │
        │                              │
        │ Outputs to:                  │
        │ • Mercado Livre              │
        │ • Shopee                     │
        │ • Magalu                     │
        │ • Amazon BR                  │
        └──────────────────────────────┘

STORAGE LAYERS
├─ user_anuncios/     (Generated ads in Markdown)
├─ Supabase Database  (Products + Metadata)
├─ Shopify Admin      (Published listings)
└─ Landing Page       (Public product pages)
```

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Pesquisa Agent** | Market research & competitive analysis | `codexa.app/agentes/pesquisa_agent/` |
| **Anuncio Agent** | Ad copy generation (titles, keywords, bullets, description) | `codexa.app/agentes/anuncio_agent/` |
| **Photo Agent** | Photography prompt generation for AI image tools | `codexa.app/agentes/photo_agent/` |
| **Edge Functions** | Serverless sync operations (Supabase) | Remote (Supabase) |
| **Config** | Marketplace rules, compliance, persuasion patterns | `codexa.app/agentes/anuncio_agent/config/` |

---

## Agent Chain: Research to Photos

### 1. Pesquisa Agent → Research Notes

**Entry Point**: `/prime-pesquisa`

**Input**: Product name, category, marketplace(s)

**Output**: `research_notes.md` containing:
- Competitor analysis (pricing, positioning)
- Market gaps & opportunities
- SEO keywords & taxonomy
- Customer pain points & desires
- Price intelligence
- Market sentiment

**Key Files**:
- `codexa.app/agentes/pesquisa_agent/PRIME.md` - Agent identity
- `codexa.app/agentes/pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md` - Execution workflow
- `codexa.app/agentes/pesquisa_agent/templates/research_notes.md` - Template

**Execution Time**: 15-30 minutes

---

### 2. Anuncio Agent → Complete Listing Copy

**Entry Point**: `/prime-anuncio` or `python codex_anuncio.py generate`

**Input**:
- Research notes (from pesquisa_agent) OR
- Direct product brief (JSON/Markdown)

**Processing**: 7-Phase Pipeline

```
PHASE 1: PARSE RESEARCH
├─ Extract head terms
├─ Identify diferenças (unique selling props)
├─ Map pain points & desires
└─ Categorize benefits

PHASE 2: GENERATE TITLES (3 Variations)
├─ Title A: Emotional + benefit-driven
├─ Title B: Technical + feature-focused
├─ Title C: Balanced + versatile
├─ Constraints: 58-60 chars, ZERO connectors, 8-10 keywords

PHASE 3: EXPAND KEYWORDS (2 Blocks)
├─ Block 1: 115-120 primary keywords
├─ Block 2: 115-120 secondary + LSI keywords
└─ Strategy: Semantic relevance + search volume

PHASE 4: WRITE BULLET POINTS (10 Points)
├─ Mental triggers (PNL framework)
├─ Feature-benefit mapping
├─ Objection handling
└─ Format: 250-299 chars per bullet

PHASE 5: COMPOSE DESCRIPTION
├─ StoryBrand framework (5-act structure)
├─ Problem-Agitate-Solution narrative
├─ Technical specs integration
├─ Authority & social proof
└─ Minimum: 3,300 characters

PHASE 6: VALIDATE COMPLIANCE
├─ ANVISA rules (health/supplement claims)
├─ INMETRO rules (technical specs)
├─ CONAR rules (advertising ethics)
├─ Marketplace-specific restrictions
└─ Output: Compliance score + issues list

PHASE 7: CALCULATE PERSUASION SCORE
├─ PNL trigger effectiveness
├─ StoryBrand element presence
├─ Emotional resonance
└─ Output: Persuasion level (1-10) + recommendations
```

**Output Formats**:

Trinity Format (Default - 3 files):
```
user_anuncios/
├─ produto_nome_ad_copy.md           # Human-readable markdown
├─ produto_nome_ad_copy.llm.json     # LLM-parseable JSON
└─ produto_nome_ad_copy.meta.json    # Metadata & validation scores
```

Single Block Format:
```
Copyable marketplace-ready block:
═══════════════════════════════════════════════════════════════

TÍTULO
[Title A / B / C - up to 60 chars]

DESCRIÇÃO
[Full description with line breaks for readability]

FICHA TÉCNICA (Bullet Points)
• Benefit 1: Feature detail (250-299 chars)
• Benefit 2: Feature detail (250-299 chars)
[... 10 total ...]

PALAVRAS-CHAVE
[Block 1]: keyword1 keyword2 keyword3 ... (115-120 terms)
[Block 2]: keyword_secondary1 keyword_secondary2 ... (115-120 terms)

VALIDAÇÃO
✓ Compliance Score: 95%
✓ Persuasion: HIGH (8.5/10)
✓ QA Status: PASSED
```

**Key Files**:
- `codexa.app/agentes/anuncio_agent/PRIME.md` - Agent identity
- `codexa.app/agentes/anuncio_agent/codex_anuncio.py` - CLI
- `codexa.app/agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md` - Workflow
- `codexa.app/agentes/anuncio_agent/config/copy_rules.json` - Compliance rules
- `codexa.app/agentes/anuncio_agent/config/marketplace_specs.json` - Platform limits

**Execution Time**: 3-8 minutes

**Quality Gate**: Must pass ≥0.75 quality score (see [Quality Gates](#quality-gates--thresholds))

---

### 3. Photo Agent → AI Photography Prompts

**Entry Point**: `/prime-photo`

**Input**:
- Product description (from anuncio_agent) OR
- Direct product brief

**Output**: Two prompt sets

**Set 1: Grid 3x3 Master Prompt**
- Single prompt generates 9-scene composition in one image
- Format: Markdown code block with Midjourney syntax
- Includes: `{user_image}`, `seed:[RANDOM]`, `[OPEN_VARIABLES]`
- Use case: Quick 9-in-1 visualization

**Set 2: 9 Individual Scene Prompts**
- Separate prompt for each scene/angle
- Photographic direction for each angle:
  - Angle 1: Hero shot (straight-on, product dominant)
  - Angle 2: Lifestyle context (in-use scenario)
  - Angle 3: Detail close-up (texture/quality)
  - Angle 4: Lifestyle model (person with product)
  - Angle 5: Comparison shot (vs. alternative)
  - Angle 6: Packaging beauty shot
  - Angle 7: Multiple variations (color/size options)
  - Angle 8: Use scenario (product in action)
  - Angle 9: Lifestyle environment (aspirational context)
- Use case: Individual AI image generation per angle

**Photography Directions Include**:
- Camera specs (ISO, aperture, shutter speed)
- Lighting setup (5 professional setups: key, fill, back, side, ambient)
- Composition theory (rule of thirds, leading lines, depth of field)
- PNL emotional triggers (colors, patterns, context)
- Marketplace compliance (image dimensions, background, text overlay rules)

**Key Files**:
- `codexa.app/agentes/photo_agent/PRIME.md` - Agent identity
- `codexa.app/agentes/photo_agent/photo_agent.py` - Core logic
- `codexa.app/agentes/photo_agent/config/photography_styles.json` - Style templates

**Execution Time**: 2-4 minutes

**Compatible AI Tools**: Midjourney, DALL-E 3, Stable Diffusion XL, Imagen 3

---

## Slash Commands

### Agent Entry Points

#### 1. `/prime-pesquisa` - Load Research Agent

```bash
/prime-pesquisa
```

**What it does**:
- Loads complete pesquisa_agent context
- Configures for market research & competitive analysis
- Validates web search sources
- Prepares competitor intelligence system

**Response includes**:
- Identity (research specialist)
- 8-phase workflow
- Compliance rules (web scraping, data collection)
- Quality gates

---

#### 2. `/prime-anuncio` - Load Ad Generation Agent

```bash
/prime-anuncio
```

**What it does**:
- Loads complete anuncio_agent context
- Configures for marketplace ad copy
- Validates compliance rules (ANVISA/INMETRO/CONAR)
- Prepares Trinity output writer

**Response includes**:
- Identity (copywriter specialist)
- 7-phase pipeline
- Marketplace compliance rules
- Quality gates & thresholds

---

#### 3. `/prime-photo` - Load Photography Agent

```bash
/prime-photo
```

**What it does**:
- Loads complete photo_agent context
- Configures for AI photography prompts
- Prepares 2-output format (grid + individual)
- Validates prompt syntax (Midjourney, DALL-E)

**Response includes**:
- Identity (photography specialist)
- Dual-input workflow
- 5 lighting setups
- 18 PNL emotional triggers

---

### Execution Commands

#### Direct Anuncio Execution

**In Claude interface** (after `/prime-anuncio`):

```
Generate ad copy for [research_notes.md]:
- Marketplace: mercado_livre
- Output format: trinity
- Auto-correct: enabled
```

**The agent will execute**:
1. Read research notes
2. Parse input (validate)
3. Execute 7-phase pipeline
4. QA validate output
5. Save trinity files (or single block)

---

## Python Scripts & CLI

### Main CLI: `codex_anuncio.py`

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\codex_anuncio.py`

**Version**: 1.2.0 | **Status**: Production-Ready

#### Usage

```bash
# Generate ad from research notes
python codex_anuncio.py generate research_notes.md

# Generate for specific marketplace
python codex_anuncio.py generate research_notes.md -m shopee --auto-correct

# Generate with Trinity output (3 files)
python codex_anuncio.py generate research_notes.md -f trinity

# Generate with single JSON file
python codex_anuncio.py generate research_notes.md -f json

# Generate with single Markdown file
python codex_anuncio.py generate research_notes.md -f markdown

# Validate existing ad
python codex_anuncio.py validate anuncio.json
```

#### Commands

**1. Generate Command**

```bash
python codex_anuncio.py generate <input_file> [options]
```

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `-m, --marketplace` | mercadolivre, shopee, magalu, amazon, all | all | Target marketplace |
| `-o, --output` | path | `outputs/` | Output directory |
| `-f, --format` | trinity, json, markdown | trinity | Output format |
| `--auto-correct` | flag | disabled | Enable correction loop |
| `--max-attempts` | 1-10 | 3 | Correction attempts |
| `-v, --verbose` | flag | disabled | Detailed output |

**Example**:

```bash
python codex_anuncio.py generate "research/gatinha_notebook_desk.md" \
  -m shopee \
  -f trinity \
  --auto-correct \
  --max-attempts 5 \
  -v
```

**Output**:

```
✅ Anúncio gerado com sucesso!
   QA Status: PASSED
   Persuasion: HIGH (8.7/10)
   Compliance: 98%

📁 Outputs:
   ├─ gatinha_notebook_desk_ad_copy.md
   ├─ gatinha_notebook_desk_ad_copy.llm.json
   └─ gatinha_notebook_desk_ad_copy.meta.json
```

**2. Validate Command**

```bash
python codex_anuncio.py validate <anuncio_file> [options]
```

**Example**:

```bash
python codex_anuncio.py validate "user_anuncios/produto_ad_copy.json" -v
```

**Output**:

```
🔍 Validando: produto_ad_copy.json
   QA Status: PASSED
   Persuasion: HIGH (8.5/10)
   Compliance: 95%

✅ Validação PASSOU
```

---

### Sync & Publishing Scripts

#### 1. `unified_sync.py` - Bidirectional Supabase ↔ Shopify Sync

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\unified_sync.py`

**Purpose**: Synchronize product data between Supabase database and Shopify store

**Usage**:

```bash
# Pull all data from Shopify → Supabase
python unified_sync.py pull

# Push all data from Supabase → Shopify
python unified_sync.py push

# Smart bidirectional sync (newer wins)
python unified_sync.py bidirectional

# Sync single product
python unified_sync.py single <product-id>

# Dry-run preview without applying changes
python unified_sync.py pull --dry-run

# Sync only inventory
python unified_sync.py push --scope=inventory

# Force sync (ignore timestamps)
python unified_sync.py bidirectional --force
```

**Scope Options**: `all|inventory|content|price`

**Output**:

```
======================================================================
UNIFIED SYNC
Mode: pull | Scope: all
Dry Run: false | Force: false
======================================================================

Executing... (this may take a few minutes)

======================================================================
MODE: PULL
SCOPE: all
DURATION: 12534ms
----------------------------------------------------------------------
TOTAL:    145
SYNCED:   142 (23 created, 119 updated)
SKIPPED:  3
ERRORS:   0
======================================================================

PRODUCTS:
  [+] Caneca Gatinha Notebook...       created (shopify)
  [~] Cama de Gato com Ventosa...       updated (bidirectional)
  [-] Produto Descontinuado...          skipped (already synced)
```

**Config**: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` in `.env`

---

#### 2. `auto_publish_anuncios.py` - Publish Generated Ads

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\auto_publish_anuncios.py`

**Purpose**: Publish generated ads from `user_anuncios/` to Supabase → Shopify → Landing Page

**Usage**:

```bash
# Publish all pending anuncios
python auto_publish_anuncios.py

# Dry-run (preview without publishing)
python auto_publish_anuncios.py --dry-run

# Publish specific file
python auto_publish_anuncios.py --file arranhador
```

**Flow**:

```
user_anuncios/*.md → Parse metadata → Supabase (create/update) → Shopify API → LP
```

**Parsing**:
- Extracts: titles, description, bullets, keywords
- Validates: compliance, character limits, formatting
- Maps: marketplace-specific requirements
- Stores: metadata (persuasion score, compliance score)

**Output**:

```
PUBLICANDO ANÚNCIOS
===================

[01/15] Caneca Gatinha Notebook Desk...
        Produto ID: ed1f6428
        Status: CRIADO em Supabase
        Shopify ID: gid://shopify/Product/123456789
        URL LP: https://codexa.app/produtos/caneca-gatinha

[02/15] Cama de Gato com Ventosa...
        Status: ATUALIZADO em Supabase
        Alterações: titulo, descricao, keywords
        ✓ Publicado em Shopify

===================
RESUMO: 13 publicados, 2 falhados
```

---

#### 3. `sync_all_shopify.py` - Batch Shopify Sync

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\sync_all_shopify.py`

**Purpose**: Batch synchronize all Supabase products with Shopify store

**Usage**:

```bash
# Sync all products with Shopify
python sync_all_shopify.py
```

**Output**:

```
======================================================================
SINCRONIZANDO TODOS OS PRODUTOS COM SHOPIFY
======================================================================

Total: 145 produtos

[01/145] Caneca Gatinha Notebook Desk...
         Shopify ID: gid://shopify/Product/123456789
         OK - Sincronizado!

[02/145] Cama de Gato com Ventosa...
         Shopify ID: gid://shopify/Product/987654321
         OK - Sincronizado!

[03/145] Coleira com Sino...
         ERROR - Campo obrigatório 'preco' vazio

======================================================================
RESUMO
TOTAL:    145
OK:       143
ERROS:    2
TEMPO:    45s
======================================================================
```

---

#### 4. `reform_product.py` - Batch Fix & Reformat

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\reform_product.py`

**Purpose**: Reformat and fix existing product listings

**Usage**:

```bash
# Reformat all products
python reform_product.py

# Reformat specific product
python reform_product.py <product-id>

# Dry-run preview
python reform_product.py --dry-run
```

---

#### 5. `update_stock.py` - Inventory Management

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\update_stock.py`

**Purpose**: Batch update inventory across all marketplaces

**Usage**:

```bash
# Update inventory from Shopify
python update_stock.py

# Update specific product
python update_stock.py <product-id> <quantity>
```

---

#### 6. `list_products.py` - Inventory Listing

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\list_products.py`

**Purpose**: List all products with status and metadata

**Usage**:

```bash
# List all products
python list_products.py

# Filter by status
python list_products.py --status published

# Filter by marketplace
python list_products.py --marketplace shopee

# Export CSV
python list_products.py --export products.csv
```

---

#### 7. `fetch_product.py` - Product Detail Fetcher

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\codexa.app\agentes\anuncio_agent\scripts\fetch_product.py`

**Purpose**: Fetch detailed product information from Supabase or Shopify

**Usage**:

```bash
# Fetch from Supabase
python fetch_product.py <product-id>

# Fetch from Shopify
python fetch_product.py <product-id> --source shopify

# Export as JSON
python fetch_product.py <product-id> --json > product.json
```

---

## Edge Functions

### Overview

Supabase Edge Functions handle serverless backend operations: syncing, validation, webhook handling

**Deployment**: Supabase Functions v1 API
**Authentication**: Service Role Key (admin) required
**Timeout**: 300 seconds (5 minutes)

---

### 1. `unified-sync` - Bidirectional Sync

**Endpoint**: `POST /functions/v1/unified-sync`

**Purpose**: Smart synchronization between Shopify (source of truth) and Supabase (metadata store)

**Request Body**:

```json
{
  "mode": "pull|push|bidirectional|single",
  "scope": "all|inventory|content|price",
  "dryRun": false,
  "force": false,
  "productId": "optional-for-single-mode"
}
```

**Modes**:

| Mode | Direction | Logic | Use Case |
|------|-----------|-------|----------|
| **pull** | Shopify → Supabase | Fetch all from Shopify, create/update in Supabase | Initial setup, catch missing products |
| **push** | Supabase → Shopify | Send all Supabase data to Shopify API | Batch publish, content updates |
| **bidirectional** | Both ↔ Both | Compare timestamps, newer wins | Regular sync, both systems active |
| **single** | Single product | Sync one product by ID | Quick fix, single product update |

**Scopes**:

| Scope | Syncs | Use Case |
|-------|-------|----------|
| **all** | Titles, descriptions, keywords, inventory, price, images | Full resync |
| **inventory** | Stock quantity only | Inventory updates |
| **content** | Titles, descriptions, keywords, images | Content refresh |
| **price** | Price, currency, discount | Price updates |

**Response**:

```json
{
  "success": true,
  "mode": "pull",
  "scope": "all",
  "duration_ms": 12534,
  "stats": {
    "total": 145,
    "synced": 142,
    "created": 23,
    "updated": 119,
    "skipped": 3,
    "errors": 0
  },
  "products": [
    {
      "id": "ed1f6428",
      "name": "Caneca Gatinha Notebook Desk",
      "action": "created",
      "direction": "shopify",
      "changes": {
        "titulo_a": true,
        "descricao": true,
        "keywords": true
      }
    }
  ]
}
```

**Error Handling**:

```json
{
  "success": false,
  "error": "HTTP 401: Unauthorized - SUPABASE_SERVICE_ROLE_KEY invalid",
  "code": 401
}
```

**Headers Required**:

```
Authorization: Bearer {SUPABASE_SERVICE_ROLE_KEY}
Content-Type: application/json
```

---

### 2. `crud-sandbox` - CRUD Operations Wrapper

**Endpoint**: `POST /functions/v1/crud-sandbox`

**Purpose**: Safe CRUD operations with validation and rollback

**Request Body**:

```json
{
  "operation": "create|read|update|delete",
  "table": "products|anuncios|metadata",
  "data": { /* operation-specific data */ },
  "filters": { /* for read/update/delete */ },
  "validate": true,
  "dryRun": false
}
```

**Operations**:

```
CREATE
POST /functions/v1/crud-sandbox
{
  "operation": "create",
  "table": "products",
  "data": {
    "name": "Produto Novo",
    "sku": "SKU-001",
    "categoria": "Pet",
    "titulo_a": "...",
    "descricao": "...",
    "preco": 99.90
  }
}

READ
POST /functions/v1/crud-sandbox
{
  "operation": "read",
  "table": "products",
  "filters": {
    "id": "ed1f6428"
  }
}

UPDATE
POST /functions/v1/crud-sandbox
{
  "operation": "update",
  "table": "products",
  "data": {
    "titulo_a": "Novo título otimizado",
    "descricao": "Nova descrição completa..."
  },
  "filters": {
    "id": "ed1f6428"
  }
}

DELETE
POST /functions/v1/crud-sandbox
{
  "operation": "delete",
  "table": "products",
  "filters": {
    "id": "ed1f6428"
  }
}
```

**Response**:

```json
{
  "success": true,
  "operation": "update",
  "affected_rows": 1,
  "data": {
    "id": "ed1f6428",
    "titulo_a": "Novo título otimizado",
    "updated_at": "2025-12-04T15:30:00Z"
  },
  "validation": {
    "passed": true,
    "warnings": []
  }
}
```

---

### 3. `webhook-manager` - Webhook Event Handler

**Endpoint**: `POST /functions/v1/webhook-manager`

**Purpose**: Handle Shopify webhooks, marketplace events, trigger sync operations

**Event Types**:

```
Shopify Events:
├─ products/create → Create in Supabase
├─ products/update → Update in Supabase
├─ products/delete → Archive in Supabase (soft delete)
└─ inventory/update → Update stock in Supabase

Landing Page Events:
├─ product/published → Update status in Supabase
├─ product/unpublished → Mark as draft
└─ product/featured → Update metadata

Manual Triggers:
├─ sync/full → Execute unified-sync pull
├─ sync/marketplace → Sync to Shopify
└─ publish/batch → Batch publish pending anúncios
```

**Request Body**:

```json
{
  "event": "products/update",
  "webhook_id": "gid://shopify/WebhookSubscription/123456789",
  "shop_id": "shop-id.myshopify.com",
  "data": {
    "id": "gid://shopify/Product/123456789",
    "title": "Updated Title",
    "description": "Updated Description",
    "vendor": "codexa.app",
    "tags": ["anuncio-v2.5.0", "marketplace:shopee"]
  }
}
```

**Webhook Verification**:

```json
{
  "valid": true,
  "shop": "codexa.myshopify.com",
  "timestamp": "2025-12-04T15:30:00Z"
}
```

**Processing Flow**:

```
Webhook Received
  ├─ Verify HMAC signature
  ├─ Check event type
  ├─ Extract product data
  ├─ Validate against compliance rules
  ├─ Update Supabase record
  ├─ Trigger cascade operations (sync, publish)
  └─ Return 200 OK (acknowledge receipt)
```

---

## Quality Gates & Thresholds

### QA Validation Criteria

**11-Point QA Matrix** (Must pass ≥7 criteria for approval):

| # | Criterion | Metric | Pass | Fail |
|---|-----------|--------|------|------|
| 1 | Compliance Score | No ANVISA/INMETRO/CONAR violations | ≥95% | <95% |
| 2 | Title Format | 58-60 chars, zero connectors, 8-10 keywords | PASS | FAIL |
| 3 | Keywords Density | LSI optimized, 115-120 per block, no spam | PASS | FAIL |
| 4 | Bullets Count | Exactly 10 strategic benefits | PASS | FAIL |
| 5 | Bullet Length | 250-299 chars each | ≥8/10 | <8/10 |
| 6 | Description Length | ≥3,300 characters | ≥3,300 | <3,300 |
| 7 | Description Quality | StoryBrand framework present | PASS | FAIL |
| 8 | Mental Triggers | PNL patterns identified | ≥5 triggers | <5 triggers |
| 9 | Marketplace Compliance | Limits respected (char, images, fields) | PASS | FAIL |
| 10 | SEO Optimization | Keyword placement, density, relevance | ≥0.75 | <0.75 |
| 11 | Persuasion Score | StoryBrand + PNL effectiveness | ≥7.0/10 | <7.0/10 |

---

### Quality Score Interpretation

**Overall Score Calculation**:

```
Quality Score = (Passed Criteria / 11) × 100
```

| Score Range | Level | Status | Action |
|-------------|-------|--------|--------|
| **90-100%** | EXCELLENT | ✅ PASSED | Approve, publish immediately |
| **75-89%** | GOOD | ✅ PASSED (with warnings) | Approve, review warnings |
| **60-74%** | FAIR | ⚠️ CAUTION | Review, consider revisions |
| **<60%** | POOR | ❌ FAILED | Reject, reprocess with auto-correct |

---

### Compliance Score Breakdown

**Compliance Categories**:

```
CRITICAL (weight: 2.0x) - If any fail, entire ad fails
├─ No HTML/CSS/JS tags
├─ No therapeutic claims (ANVISA)
├─ No absolute superlatives without proof
└─ No prohibited marketplace terms

HIGH (weight: 1.5x) - 1-2 failures acceptable
├─ No external links/URLs
├─ No emoji overuse
├─ No false discount claims
└─ No discriminatory language

MEDIUM (weight: 1.0x) - Multiple failures reduce score
├─ Price format consistency
├─ Specification accuracy
├─ Formatting consistency
└─ Tone appropriateness
```

**Compliance Score Formula**:

```
Base Score = 100
Critical Penalties = -30 per violation
High Penalties = -15 per violation
Medium Penalties = -5 per violation

Final = max(0, Base - Penalties)
```

---

### Persuasion Score Metrics

**Persuasion Elements** (18 total, goal: 8+ present):

**PNL Triggers** (Neurolinguistic Programming):
1. Loss aversion (pain of missing out)
2. Social proof (testimonials, numbers)
3. Scarcity (limited time, quantity)
4. Authority (expert endorsement)
5. Reciprocity (free value first)
6. Liking (emotional connection)
7. Consistency (brand alignment)
8. Urgency (time pressure)
9. Trust signals (certifications, guarantees)

**StoryBrand Elements** (5 acts):
1. Character (customer is hero)
2. Problem (specific pain point)
3. Guide (brand as mentor)
4. Plan (clear process/steps)
5. Call to Action (what customer does next)

**Persuasion Score Calculation**:

```
Base = 50 (neutral)
PNL Triggers Present: +1 point each (max +9)
StoryBrand Elements: +2 points each (max +10)
Emotional Language: +1 point

Final = Base + Triggers + Story + Emotion
Range: 0-70 → Normalized to 0-10 scale
```

---

### Execution Plans

**Default Plans**: `codexa.app/agentes/anuncio_agent/plans/`

#### Full Plan (11 steps, ~23-38 minutes)

```json
{
  "name": "full_anuncio",
  "duration_minutes": 38,
  "steps": [
    {
      "phase": "INPUT",
      "step": 1,
      "name": "Load Research Notes",
      "duration_minutes": 2,
      "input": "research_notes.md"
    },
    {
      "phase": "PARSE",
      "step": 2,
      "name": "Extract Research Elements",
      "duration_minutes": 3
    },
    {
      "phase": "GENERATE",
      "step": 3,
      "name": "Generate 3 Title Variations",
      "duration_minutes": 4
    },
    {
      "phase": "GENERATE",
      "step": 4,
      "name": "Expand Keywords (2 blocks)",
      "duration_minutes": 3
    },
    {
      "phase": "GENERATE",
      "step": 5,
      "name": "Write 10 Bullet Points",
      "duration_minutes": 5
    },
    {
      "phase": "GENERATE",
      "step": 6,
      "name": "Compose Description (3300+ chars)",
      "duration_minutes": 8
    },
    {
      "phase": "VALIDATE",
      "step": 7,
      "name": "QA Validation (11 criteria)",
      "duration_minutes": 4
    },
    {
      "phase": "VALIDATE",
      "step": 8,
      "name": "Compliance Check (ANVISA/INMETRO/CONAR)",
      "duration_minutes": 2
    },
    {
      "phase": "CALCULATE",
      "step": 9,
      "name": "Persuasion Score & Recommendations",
      "duration_minutes": 2
    },
    {
      "phase": "OUTPUT",
      "step": 10,
      "name": "Generate Trinity Files",
      "duration_minutes": 1
    },
    {
      "phase": "PUBLISH",
      "step": 11,
      "name": "Optional: Publish to Supabase/Shopify",
      "duration_minutes": 4
    }
  ]
}
```

#### Quick Plan (6 steps, ~8-12 minutes)

```json
{
  "name": "quick_anuncio",
  "duration_minutes": 12,
  "steps": [
    {
      "phase": "PARSE",
      "step": 1,
      "name": "Quick Parse Research",
      "duration_minutes": 2
    },
    {
      "phase": "GENERATE",
      "step": 2,
      "name": "Generate Best Title (1 variation)",
      "duration_minutes": 2
    },
    {
      "phase": "GENERATE",
      "step": 3,
      "name": "Generate Keywords (1 block, essential only)",
      "duration_minutes": 2
    },
    {
      "phase": "GENERATE",
      "step": 4,
      "name": "Write 8 Key Bullets",
      "duration_minutes": 2
    },
    {
      "phase": "VALIDATE",
      "step": 5,
      "name": "Quick QA Check (critical items only)",
      "duration_minutes": 2
    },
    {
      "phase": "OUTPUT",
      "step": 6,
      "name": "Output Single Copyable Block",
      "duration_minutes": 2
    }
  ]
}
```

---

## Troubleshooting Guide

### Common Issues

#### 1. CLI Not Found

**Error**: `python: command not found`

**Solution**:
```bash
# Check Python installation
python --version
# or
python3 --version

# Install Python 3.8+ from python.org
# Or use WSL if on Windows
wsl python --version
```

---

#### 2. Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'config'`

**Cause**: Working directory not set correctly

**Solution**:
```bash
# Navigate to anuncio_agent directory
cd /path/to/codexa.app/agentes/anuncio_agent

# Run from correct location
python codex_anuncio.py generate research_notes.md
```

---

#### 3. Configuration Missing

**Error**: `SUPABASE_URL not configured`, `SUPABASE_SERVICE_ROLE_KEY not found`

**Solution**:
```bash
# Check .env file in codexa-core root
cat ../../.env

# Ensure variables are set
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="eyJ..."
export SUPABASE_ANON_KEY="eyJ..."

# Test connection
python -c "from config.env_loader import supabase; print(supabase.url)"
```

---

#### 4. Compliance Violations Detected

**Error**: `❌ Validação FALHOU` with compliance issues

**Cause**: Generated copy violates ANVISA/INMETRO/CONAR/marketplace rules

**Solution**:
```bash
# Use auto-correct flag
python codex_anuncio.py generate research_notes.md --auto-correct --max-attempts 5

# Or check specific violations
python codex_anuncio.py validate output.json -v

# Review compliance rules
cat config/copy_rules.json | grep -A 20 "proibicoes_gerais"

# Manual fix: Edit research notes to remove problematic claims
# Example: Remove "cura ansiedade" → replace with "auxilia no bem-estar"
```

---

#### 5. Low Persuasion Score

**Error**: `Persuasion: LOW (4.2/10)` - Below acceptable threshold

**Cause**: Missing StoryBrand elements or PNL triggers

**Solution**:
```bash
# Check recommendations in output
# Example recommendations:
# - Adicionar social proof (testimonials, numbers)
# - Enfatizar problema-solução (StoryBrand)
# - Incluir urgência (limited time, quantity)

# Enhance research notes with:
# 1. Customer testimonials
# 2. Problem statement
# 3. Specific benefits (not generic)
# 4. Trust signals (certifications, guarantees)
# 5. Emotional language

# Regenerate with enhanced input
python codex_anuncio.py generate research_notes_v2.md --auto-correct
```

---

#### 6. Sync Failures

**Error**: `unified_sync.py: HTTP 401 - Unauthorized`

**Cause**: Invalid or missing service role key

**Solution**:
```bash
# Verify credentials
echo $SUPABASE_SERVICE_ROLE_KEY

# Check service role key format (should start with eyJ)
# If missing, update .env file

# Test API connectivity
curl -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  $SUPABASE_URL/rest/v1/products?select=id&limit=1

# Check Supabase dashboard for API keys
# https://app.supabase.com/project/[project-id]/settings/api
```

**Error**: `unified_sync.py: Timeout - request took >300 seconds`

**Cause**: Too many products (>500), network issues

**Solution**:
```bash
# Sync by scope instead of all
python unified_sync.py pull --scope=content --dry-run

# Sync in batches (single mode)
python unified_sync.py single product-id-1
python unified_sync.py single product-id-2

# Check network
ping -c 3 xxxxx.supabase.co

# Increase timeout in code if needed
```

---

#### 7. Marketplace Compliance Failure

**Error**: `❌ Mercado Livre: Título com 71 caracteres (máximo: 60)`

**Cause**: Output exceeds marketplace limits

**Solution**:
```bash
# Check marketplace specs
cat config/marketplace_specs.json | grep -A 10 "mercadolivre"

# Current title too long? Auto-correct will shorten
python codex_anuncio.py generate research_notes.md --auto-correct

# Manual reduction strategy:
# Original: "Caneca Gatinha Fofa Notebook Desk Ceramic 350ml Cores Sortidas"
# Shortened: "Caneca Gatinha Fofa Notebook Desk 350ml"
# (Keep core keywords: product + unique aspect + size)
```

---

#### 8. Output File Format Issues

**Error**: `trinity` format files not created as expected

**Cause**: Output directory doesn't exist or permission denied

**Solution**:
```bash
# Ensure output directory exists
mkdir -p user_anuncios
chmod 755 user_anuncios

# Check file creation
ls -la user_anuncios/

# If using custom output path
mkdir -p /path/to/custom/output
python codex_anuncio.py generate research_notes.md -o /path/to/custom/output
```

---

#### 9. Research Notes Parsing Issues

**Error**: `research_notes.md: Invalid format`

**Cause**: Missing required sections or incorrect structure

**Solution**:

Check research notes structure:

```markdown
# Pesquisa de Mercado

## Produto
- Nome: [product name]
- Categoria: [category]
- Subcategoria: [subcategory]

## Mercado
- Tamanho mercado: [market size]
- Crescimento: [growth rate]
- Tendências: [trends]

## Competidores
- Competitor A: [analysis]
- Competitor B: [analysis]

## Diferenças (USP)
- Unique aspect 1
- Unique aspect 2

## Dores do Cliente (Pain Points)
- Problem 1
- Problem 2

## Ganhos Esperados (Benefits)
- Benefit 1
- Benefit 2

## Pricing
- Market range: R$ X - R$ Y
- Our price: R$ Z

## Keywords
- Primary: [list]
- Secondary: [list]
```

Use template: `codexa.app/agentes/pesquisa_agent/templates/research_notes.md`

---

#### 10. Photo Agent Integration

**Error**: `photo_agent: Prompt syntax invalid for Midjourney`

**Cause**: Template variables not properly formatted

**Solution**:

Check prompt structure:

```markdown
# Prompts Midjourney

## Grid 3x3 Master Prompt

[Complete prompt with {user_image}, seed:[RANDOM], [OPEN_VARIABLES]]

## Individual Scene Prompts

### Scene 1 - Hero Shot
[Detailed photographic direction]
[Camera specs: ISO, aperture, shutter]
[Lighting setup]
[Composition theory]
[PNL triggers]
```

Test with Midjourney directly before batch processing

---

### Debug Mode

**Enable verbose output**:

```bash
# Python scripts
python codex_anuncio.py generate research_notes.md -v

# Show full traceback on error
python codex_anuncio.py generate research_notes.md --verbose 2>&1 | tail -50

# Check validation details
python codex_anuncio.py validate output.json -v --debug
```

**Log files**:

```bash
# Recent executions
ls -lt scripts/*.log | head -5

# View specific log
cat scripts/execution_log_20251204.log

# Filter for errors
grep -i error scripts/execution_log_20251204.log
```

---

## Configuration Reference

### Environment Variables

**Required** (must be set):

```bash
SUPABASE_URL                # https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY   # eyJ0eXAiOiJKV1QiLC... (admin key)
SUPABASE_ANON_KEY          # eyJ0eXAiOiJKV1QiLC... (public key)
```

**Optional** (sensible defaults if missing):

```bash
MARKETPLACE_DEFAULT        # "all" (mercadolivre, shopee, magalu, amazon, all)
OUTPUT_FORMAT             # "trinity" (trinity, json, markdown)
AUTO_CORRECT_ENABLED      # "false" (true, false)
MAX_CORRECTION_ATTEMPTS   # "3" (1-10)
```

**Location**: `C:\Users\PC\Documents\GitHub\codexa-core\.env`

---

### Compliance Rules File

**Location**: `codexa.app/agentes/anuncio_agent/config/copy_rules.json`

**Key Sections**:

```json
{
  "proibicoes_gerais": {
    "html_css_js": { /* CRITICAL */ },
    "emojis": { /* HIGH */ },
    "claims_ranking": { /* HIGH */ },
    "claims_terapeuticos": { /* CRITICAL */ },
    "superlativos_absolutos": { /* MEDIUM */ },
    "links_externos": { /* HIGH */ },
    "precos_desatualizados": { /* MEDIUM */ }
  },
  "proibicoes_por_marketplace": {
    "mercadolivre": { /* 60-char limit, no links */ },
    "shopee": { /* 120-char limit, no spam keywords */ },
    "magalu": { /* 256-char limit, no text in images */ },
    "amazon": { /* 200-char limit, no promo info */ }
  },
  "orgaos_reguladores": {
    "ANVISA": { /* Health claims */ },
    "INMETRO": { /* Technical specs */ },
    "CONAR": { /* Advertising ethics */ }
  }
}
```

---

### Marketplace Specifications

**Location**: `codexa.app/agentes/anuncio_agent/config/marketplace_specs.json`

**Key Limits**:

| Marketplace | Title | Description | Images | Video | Bullets |
|-------------|-------|-------------|--------|-------|---------|
| **Mercado Livre** | 60 chars | 50k chars | 12 | 1 | N/A |
| **Shopee** | 120 chars | 3k chars | 9 | 1 (60s) | N/A |
| **Magalu** | 256 chars | 4k chars | 20 | 1 (2min) | N/A |
| **Amazon** | 200 chars | 2k chars | 9 | 1 (2min) | 5 (500 chars) |

---

### Persuasion Patterns

**Location**: `codexa.app/agentes/anuncio_agent/config/persuasion_patterns.json`

**PNL Triggers** (9 patterns):

```json
{
  "loss_aversion": {
    "description": "Pain of missing out",
    "patterns": ["Não perca", "Tempo limitado", "Último em estoque"],
    "weight": 1.5
  },
  "social_proof": {
    "description": "Numbers, testimonials",
    "patterns": ["1000+ vendidos", "5 estrelas", "Recomendado por"],
    "weight": 2.0
  },
  "scarcity": {
    "description": "Limited availability",
    "patterns": ["Apenas 5 restantes", "Edição limitada"],
    "weight": 1.8
  }
  // ... 6 more triggers
}
```

**StoryBrand Elements** (5-act framework):

```json
{
  "character": {
    "description": "Customer is the hero",
    "examples": ["Você merece", "Para quem quer", "Ideal para"]
  },
  "problem": {
    "description": "Specific pain point",
    "examples": ["Cansado de", "Problema com", "Difícil de"]
  },
  // ... 3 more acts
}
```

---

## Summary

The unified anuncio pipeline is a production-ready system for generating Brazilian marketplace listings:

**Key Metrics**:
- **Speed**: 3min for quick generation, 8-40min for full pipeline
- **Quality**: 95%+ compliance, 7.5+/10 persuasion average
- **Scale**: 10-50 ads/day per team member
- **ROI**: 2-4 hours → 3 minutes per ad (95%+ time savings)

**Three Agent Chain**:
1. **Pesquisa** → Research insights
2. **Anuncio** → Complete copy (titles, keywords, bullets, description)
3. **Photo** → Photography prompts for AI image generation

**Execution Methods**:
- **CLI**: `python codex_anuncio.py generate research_notes.md`
- **Claude**: `/prime-anuncio` + conversational prompts
- **Automation**: `auto_publish_anuncios.py` + `unified_sync.py`
- **Webhooks**: Shopify events trigger sync operations automatically

**Safety & Compliance**:
- 11-point QA validation
- ANVISA/INMETRO/CONAR compliance checking
- Marketplace-specific limit enforcement
- Auto-correct correction loop (up to 5 attempts)

For detailed implementation, see:
- `codexa.app/agentes/anuncio_agent/PRIME.md` - Agent identity
- `codexa.app/agentes/anuncio_agent/README.md` - Full documentation
- `codexa.app/agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md` - Execution workflow
