# Workflows Guide | ECOMLM.CODEXA

> **Status**: Production Documentation
> **Last Updated**: 2025-11-14
> **Version**: 1.0.0

---

## 🎯 Overview

This guide provides detailed workflow documentation for ECOMLM.CODEXA, covering common use cases from e-commerce automation to agent development. Each workflow includes step-by-step instructions, timing estimates, prerequisites, and troubleshooting guidance.

---

## 📋 Table of Contents

1. [E-Commerce Complete Pipeline](#1-e-commerce-complete-pipeline)
2. [Agent Creation Workflow](#2-agent-creation-workflow)
3. [HOP Module Creation](#3-hop-module-creation)
4. [Data Upload & Query Workflow](#4-data-upload--query-workflow)
5. [Navigation & Discovery](#5-navigation--discovery)
6. [Troubleshooting Common Issues](#6-troubleshooting-common-issues)

---

## 1. E-Commerce Complete Pipeline

**Purpose**: Complete workflow from product research to multi-marketplace listings

**Time Estimate**: 30-45 minutes (fully automated)

**Prerequisites**:
- Agents loaded: pesquisa, marca (optional), anuncio
- API keys configured (ANTHROPIC_API_KEY or OPENAI_API_KEY)
- Product or niche description

---

### Workflow Diagram (ASCII)

```
┌─────────────────┐
│ Product Idea    │
│ or Niche        │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│ STEP 1: Market Research         │
│ Command: /prime-pesquisa         │
│ Agent: pesquisa_agent            │
│ Duration: ~10-15 min             │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Output: research_notes.md        │
│ - 22-block structured research   │
│ - 9+ marketplace analysis        │
│ - Competitor insights            │
│ - Keywords & pricing             │
└────────┬────────────────────────┘
         │
         v (optional)
┌─────────────────────────────────┐
│ STEP 2: Brand Strategy (Beta)   │
│ Command: /prime-marca            │
│ Agent: marca_agent               │
│ Duration: ~8-12 min              │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Output: brand_strategy.md        │
│ - Brand identity                 │
│ - Tone guidelines                │
│ - Visual direction               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ STEP 3: Listing Generation      │
│ Command: /prime-anuncio          │
│ Agent: anuncio_agent             │
│ Duration: ~12-18 min             │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Output: anuncio.json +           │
│ marketplace_listings/            │
│ - 9+ marketplace listings        │
│ - 100% compliance validation     │
│ - SEO-optimized content          │
└─────────────────────────────────┘
```

---

### Step-by-Step Instructions

#### STEP 1: Market Research

**1.1 Load Research Agent**
```bash
/prime-pesquisa
```

**1.2 Execute Research**
```bash
/pesquisa "fone bluetooth para home office"
```

**Alternative**: Provide more detailed product description
```bash
/pesquisa "Fone de ouvido Bluetooth com cancelamento de ruído para home office, faixa de preço R$150-300, público-alvo profissionais 25-45 anos"
```

**1.3 Review Output**
- Check `research_notes.md` (22 blocks)
- Verify marketplace coverage (≥9)
- Validate competitor analysis (≥5 competitors)
- Review keyword extraction (≥15 keywords)

**Timing**: 10-15 minutes (automated analysis of 9+ marketplaces)

---

#### STEP 2: Brand Strategy (Optional)

**2.1 Load Brand Agent**
```bash
/prime-marca
```

**2.2 Execute Brand Development**
```bash
/marca
```

**2.3 Interactive Process**
- Answer prompts about business context
- Define brand personality
- Set tone and voice guidelines

**2.4 Review Output**
- Check `brand_strategy.md`
- Verify brand identity completeness
- Review guidelines applicability

**Timing**: 8-12 minutes (interactive session + generation)

**Note**: Beta feature - currently in development. Can skip for MVP listings.

---

#### STEP 3: Listing Generation

**3.1 Load Listing Agent**
```bash
/prime-anuncio
```

**3.2 Execute with Research Only**
```bash
/anuncio research_notes.md
```

**3.3 Execute with Research + Brand**
```bash
/anuncio research_notes.md brand_strategy.md
```

**3.4 Review Outputs**

**Primary Output** (`anuncio.json`):
```json
{
  "titulo": "...",
  "descricao": "...",
  "palavras_chave": [...],
  "preco_sugerido": {...},
  "categoria": "..."
}
```

**Marketplace Listings** (`marketplace_listings/`):
- `mercadolivre.md`
- `shopee.md`
- `magazineluiza.md`
- `americanas.md`
- `casasbahia.md`
- `amazon.md`
- `olx.md`
- `enjoei.md`
- `facebook_marketplace.md`

**3.5 Validation Checks**
- ✅ Title length: 58-60 chars
- ✅ Description: ≥3000 chars
- ✅ Keywords: 9-10 (optimal density)
- ✅ Compliance: 100% (all marketplaces)
- ✅ SEO score: ≥85/100

**Timing**: 12-18 minutes (9+ marketplace listings + validation)

---

### Prerequisites Checklist

- [ ] Python 3.12+ installed
- [ ] UV package manager installed (`pip install uv`)
- [ ] API key configured (`.env` file in `codexa.app/agentes/`)
  ```
  ANTHROPIC_API_KEY=sk-ant-...
  ```
- [ ] Agents available (check with `/prime`)
- [ ] Product/niche description prepared (clear 1-3 sentences)

---

### Troubleshooting

**Issue**: Research returns insufficient competitors
- **Fix**: Provide more specific product category
- **Example**: Instead of "fone bluetooth", use "fone bluetooth over-ear com ANC"

**Issue**: Listings fail compliance validation
- **Fix**: Check research_notes.md completeness (all 22 blocks)
- **Fix**: Ensure product category is specific

**Issue**: Brand strategy seems generic
- **Fix**: Provide more context in interactive prompts
- **Fix**: Specify target audience demographics

**Issue**: API rate limiting
- **Fix**: Add delays between requests (built-in retry with exponential backoff)
- **Fix**: Check API quota status

---

## 2. Agent Creation Workflow

**Purpose**: Create new AI agent using CODEXA meta-constructor (5-phase ADW)

**Time Estimate**: 30-45 minutes (fully automated)

**Prerequisites**:
- CODEXA agent loaded (`/prime-codexa`)
- ANTHROPIC_API_KEY configured
- Clear agent description (1-3 sentences)

---

### Workflow Diagram

```
┌─────────────────┐
│ Agent Concept   │
│ (description)   │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│ Load Meta-Constructor           │
│ Command: /prime-codexa           │
│ Duration: ~5 sec                 │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ PHASE 1: Strategic Planning     │
│ - Generate [OPEN_VARIABLES]     │
│ - Define capabilities (3-5)     │
│ - Select model (GPT-4o/Sonnet)  │
│ Duration: ~5-8 min               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ PHASE 2: Artifact Construction  │
│ - MASTER_INSTRUCTIONS.md         │
│ - AGENT_CONFIGURATION.json       │
│ - OUTPUT_SCHEMA.md               │
│ - VECTOR_STORE_MANIFEST.md       │
│ Duration: ~8-12 min              │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ PHASE 3: Testing & Validation   │
│ - Validate artifacts             │
│ - Create test scenarios (3-5)   │
│ - Schema validation              │
│ Duration: ~5-8 min               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ PHASE 4: Critical Review        │
│ - Quality scoring (1-10)         │
│ - Improvement suggestions        │
│ - Consistency checks             │
│ Duration: ~3-5 min               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ PHASE 5: Documentation          │
│ - README.md                      │
│ - DEPLOYMENT_GUIDE.md            │
│ - EXAMPLES.md                    │
│ - META_CONSTRUCTION_LOG.md       │
│ Duration: ~8-12 min              │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Output: Complete Agent          │
│ (8 artifacts, deployment-ready) │
│ Location: agents/{adw_id}/       │
└─────────────────────────────────┘
```

---

### Step-by-Step Instructions

#### STEP 1: Load Meta-Construction Context

```bash
/prime-codexa
```

**Expected Output**:
- Meta-construction context loaded
- Available builders listed (8 scripts)
- Available validators listed (4 scripts)
- Ready for meta-construction tasks

---

#### STEP 2: Execute Agent Builder

**Method 1: Using Command**
```bash
/codexa-build_agent
```
- Interactive prompts will guide you
- Asks for agent description
- Optional: model selection, target directory

**Method 2: Using Builder Directly**
```bash
uv run builders/02_agent_meta_constructor.py "Sentiment analysis agent for product reviews, generates positive/neutral/negative scores with justifications"
```

**Method 3: With Options**
```bash
uv run builders/02_agent_meta_constructor.py "Agent description" --model opus --target-dir agents/my-agent-v1/ --verbose
```

---

#### STEP 3: Monitor Progress

The builder will execute 5 phases automatically:

**Phase 1**: Strategic Planning
- Generates agent specification
- Creates [OPEN_VARIABLES] for creative freedom
- Selects optimal model and capabilities
- **Watch for**: Plan generation, agent name extraction

**Phase 2**: Artifact Construction
- Builds MASTER_INSTRUCTIONS.md (2000-5000 words)
- Creates AGENT_CONFIGURATION.json
- Generates schemas and manifests
- **Watch for**: Artifact count (should reach 4 core files)

**Phase 3**: Testing & Validation
- Validates file completeness
- Checks JSON schema validity
- Creates test scenarios (3-5)
- **Watch for**: Validation passed messages

**Phase 4**: Critical Review
- Quality scoring (1-10)
- Identifies improvements
- Suggests refinements
- **Watch for**: Quality score ≥ 7.0

**Phase 5**: Documentation
- README.md (overview + quick start)
- DEPLOYMENT_GUIDE.md (step-by-step)
- EXAMPLES.md (use cases)
- META_CONSTRUCTION_LOG.md (traceability)
- **Watch for**: All 8 files completed

---

#### STEP 4: Review Output

**Directory Structure**:
```
agents/{adw_id}/agent-artifacts/
├── MASTER_INSTRUCTIONS.md          # Core agent instructions
├── AGENT_CONFIGURATION.json        # OpenAI config
├── VECTOR_STORE_MANIFEST.md        # Knowledge base docs
├── OUTPUT_SCHEMA.md                # Output format schema
├── README.md                       # Overview
├── DEPLOYMENT_GUIDE.md             # Deployment steps
├── EXAMPLES.md                     # Usage examples
└── META_CONSTRUCTION_LOG.md        # Full workflow log
```

**Quality Checks**:
- [ ] All 8 files present
- [ ] MASTER_INSTRUCTIONS: 2000-5000 words
- [ ] AGENT_CONFIGURATION: Valid JSON
- [ ] README: Complete with quick start
- [ ] DEPLOYMENT_GUIDE: Step-by-step instructions
- [ ] No [PLACEHOLDER] or [VARIABLE] remaining
- [ ] Quality score ≥ 7.0

---

#### STEP 5: Deploy Agent (Optional)

**To OpenAI Agent Builder**:
1. Open https://platform.openai.com/playground/assistants
2. Click "Create Assistant"
3. Copy content from MASTER_INSTRUCTIONS.md
4. Upload files from VECTOR_STORE_MANIFEST.md
5. Configure as per AGENT_CONFIGURATION.json
6. Test with scenarios from EXAMPLES.md

**To CODEXA Registry**:
```bash
# Register agent in 51_AGENT_REGISTRY.json
python scripts/register_agent.py agents/{adw_id}/
```

---

### Prerequisites Checklist

- [ ] `/prime-codexa` loaded successfully
- [ ] ANTHROPIC_API_KEY or OPENAI_API_KEY in environment
- [ ] Python 3.10+ with `uv` installed
- [ ] Clear agent description (1-3 sentences)
- [ ] Agent purpose and domain clearly defined
- [ ] Target output directory writable

---

### Troubleshooting

**Issue**: Phase 1 fails with "insufficient description"
- **Fix**: Provide more detailed description (mention purpose, domain, capabilities)
- **Example**: "Sentiment analysis agent analyzing product reviews, generating scores (positive/neutral/negative) + justifications"

**Issue**: Phase 2 generates incomplete MASTER_INSTRUCTIONS (<2000 words)
- **Fix**: Re-run Phase 2 with `--verbose` flag
- **Fix**: Provide more specific capabilities in description

**Issue**: Phase 3 validation fails
- **Fix**: Check JSON syntax in AGENT_CONFIGURATION.json
- **Fix**: Ensure all required fields present in schemas

**Issue**: Quality score <7.0
- **Fix**: Review Phase 4 improvement suggestions
- **Fix**: Re-run weakest phase (usually Phase 2 or 5)

**Issue**: API rate limiting during construction
- **Fix**: Built-in exponential backoff (1s→2s→4s) will handle this
- **Fix**: If persists, increase delays in builder script

---

## 3. HOP Module Creation

**Purpose**: Create reusable Higher-Order Prompt following TAC-7 framework

**Time Estimate**: 15-25 minutes (automated generation + validation)

**Prerequisites**:
- CODEXA agent loaded (`/prime-codexa`)
- HOP specification (module purpose, inputs, outputs, steps)
- Understanding of TAC-7 framework (see [HOP_FRAMEWORK.md](./HOP_FRAMEWORK.md))

---

### Workflow Diagram

```
┌─────────────────┐
│ HOP Concept     │
│ (specification) │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│ Define Specification            │
│ - Module ID & purpose            │
│ - Input variables ($vars)        │
│ - Output structures              │
│ - Categories & dependencies      │
│ Duration: ~3-5 min               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Generate HOP Module             │
│ Command: /codexa-build_prompt    │
│ or: uv run builders/08_*.py      │
│ Duration: ~5-10 min              │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ TAC-7 Structure Generated       │
│ 1. MODULE_METADATA               │
│ 2. INPUT_CONTRACT                │
│ 3. OUTPUT_CONTRACT               │
│ 4. TASK                          │
│ 5. STEPS (3-7)                   │
│ 6. VALIDATION                    │
│ 7. CONTEXT                       │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Validate HOP Module             │
│ Tool: 07_hop_sync_validator.py   │
│ Duration: ~2-3 min               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Fix Issues (if any)             │
│ - Orphaned $variables            │
│ - Missing sections               │
│ - Weak validation rules          │
│ Duration: ~5-7 min               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Output: Production HOP          │
│ Location: prompts/{module}_HOP.md│
│ Status: TAC-7 compliant          │
└─────────────────────────────────┘
```

---

### Step-by-Step Instructions

#### STEP 1: Define HOP Specification

**Create Spec Object**:
```python
hop_spec = {
    "module_id": "data_validation",
    "purpose": "Validate uploaded data files against quality standards",
    "category": "validator",  # builder|validator|analyzer|transformer
    "domain": "data-quality",
    "inputs": [
        {
            "name": "$data_file",
            "type": "string",
            "required": True,
            "validation": "Valid file path, readable",
            "example": "data/products.csv"
        },
        {
            "name": "$quality_threshold",
            "type": "number",
            "required": False,
            "default": 0.8,
            "validation": "0.0 - 1.0 range",
            "example": 0.85
        }
    ],
    "outputs": [
        {
            "name": "$validation_report",
            "type": "object",
            "structure": "{passed: boolean, score: number, issues: array, suggestions: array}",
            "validation": "All fields required"
        }
    ]
}
```

---

#### STEP 2: Generate HOP

**Method 1: Using Command**
```bash
/codexa-build_prompt
```
- Interactive mode with prompts

**Method 2: Using Builder with Spec**
```bash
uv run builders/08_prompt_generator.py --spec hop_spec.json
```

**Method 3: Programmatic**
```python
from builders.adw_modules.prompt_generator import generate_hop

hop_module = generate_hop(hop_spec, template_reference="standard_tac7")
```

---

#### STEP 3: Review Generated HOP

**Check TAC-7 Sections**:
1. ✅ MODULE_METADATA: ID, version, purpose, dependencies, category
2. ✅ INPUT_CONTRACT: All $inputs with types, validation, examples
3. ✅ OUTPUT_CONTRACT: All $outputs with structures
4. ✅ TASK: Role, objective, standards, constraints
5. ✅ STEPS: 3-7 numbered actionable steps
6. ✅ VALIDATION: Quality gates (5-10) + scoring
7. ✅ CONTEXT: Usage, chaining, assumptions

---

#### STEP 4: Validate HOP

```bash
uv run validators/07_hop_sync_validator.py prompts/data_validation_HOP.md
```

**Expected Output**:
```
[OK] MODULE_METADATA complete
[OK] INPUT_CONTRACT has 2 inputs (all typed)
[OK] OUTPUT_CONTRACT has 1 output (structured)
[OK] TASK section complete
[OK] STEPS section has 5 steps
[OK] VALIDATION section has 7 quality gates
[OK] CONTEXT section complete
[OK] No orphaned $variables
[OK] Quality score: 8.5/10.0
```

---

#### STEP 5: Fix Issues (if any)

**Common Issues**:

**Orphaned $variables**:
```markdown
# Before (ERROR)
### STEP 2: Process Data
Use $data_rows to calculate statistics

# After (FIXED)
## INPUT_CONTRACT
- **$data_rows** (array) - Data rows from file | Validation: Non-empty array

### STEP 2: Process Data
Use $data_rows to calculate statistics
```

**Missing validation rules**:
```markdown
# Before (WEAK)
- ✅ Check outputs

# After (STRONG)
- ✅ **Output Completeness**: All required fields present | Verify: Check object keys | Fix: Re-run generation with full schema
```

**Weak steps**:
```markdown
# Before (TOO VAGUE)
### STEP 3: Validate
Validate the data

# After (ACTIONABLE)
### STEP 3: Validate Data Quality
**Actions**:
1. Check for null values in required columns
2. Validate data types match schema
3. Verify value ranges within acceptable bounds
4. Calculate quality score: (valid_rows / total_rows) * 100
**Outputs**: $quality_score, $invalid_rows[]
```

---

### Prerequisites Checklist

- [ ] HOP specification defined (purpose, inputs, outputs, steps)
- [ ] Category selected (builder/validator/analyzer/transformer)
- [ ] All $variables follow naming conventions ($prefix, snake_case)
- [ ] Input/output structures clearly defined
- [ ] Validation rules are automatable (not subjective)

---

### Troubleshooting

**Issue**: Validator reports orphaned $variables
- **Fix**: Add all $vars used in STEPS to INPUT_CONTRACT or OUTPUT_CONTRACT
- **Fix**: Remove unused $vars from contracts

**Issue**: Steps are too abstract
- **Fix**: Break complex steps into numbered sub-actions
- **Fix**: Add "Actions:" sub-list with concrete operations

**Issue**: Validation rules are subjective
- **Fix**: Replace "good quality" with "quality_score ≥ 0.8"
- **Fix**: Add measurable criteria (thresholds, counts, regex patterns)

**Issue**: Quality score <7.0
- **Fix**: Review scoring breakdown from validator
- **Fix**: Focus on weakest area (usually Steps or Validation sections)

---

## 4. Data Upload & Query Workflow

**Purpose**: Upload data files and execute natural language queries using FastAPI backend

**Time Estimate**: 5-15 minutes (depending on file size)

**Prerequisites**:
- FastAPI server running (`uv run python server.py`)
- Data file (CSV/JSON/JSONL format)
- Natural language query prepared

---

### Workflow Diagram

```
┌─────────────────┐
│ Data File       │
│ (CSV/JSON/JSONL)│
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│ Start FastAPI Server            │
│ Command: uv run python server.py│
│ Port: 8000 (default)             │
│ Duration: ~2-3 sec               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Upload File                     │
│ Endpoint: POST /api/upload       │
│ Converts to SQLite table         │
│ Duration: ~5-30 sec (size-dep.)  │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Table Created                   │
│ - Table name: {filename}         │
│ - Schema extracted               │
│ - Row count returned             │
│ - Sample data (first 5 rows)    │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Execute Natural Language Query  │
│ Endpoint: POST /api/query        │
│ LLM generates SQL                │
│ Duration: ~2-5 sec               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Query Results                   │
│ - Generated SQL                  │
│ - Results (data rows)            │
│ - Columns                        │
│ - Row count                      │
│ - Execution time                 │
└────────┬────────────────────────┘
         │
         v (optional)
┌─────────────────────────────────┐
│ Export Results                  │
│ Endpoint: POST /api/export/query │
│ Format: CSV                      │
│ Duration: ~1-2 sec               │
└─────────────────────────────────┘
```

---

### Step-by-Step Instructions

#### STEP 1: Start FastAPI Server

```bash
cd app/server
uv run python server.py
```

**Expected Output**:
```
[*] Initializing TAC-7 system...
[+] Database connection pool initialized
[+] LLM cache initialized (TTL: 1 hour)
[+] Schema cache initialized (TTL: 5 minutes)
[+] Products table initialized
[+] Database indexes created/verified
[+] TAC-7 system ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify Server**:
```bash
curl http://localhost:8000/api/health
```

---

#### STEP 2: Upload Data File

**Using cURL**:
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@data/products.csv" \
  -H "Accept: application/json"
```

**Using Python**:
```python
import httpx

with open("products.csv", "rb") as f:
    files = {"file": ("products.csv", f)}
    response = httpx.post("http://localhost:8000/api/upload", files=files)

result = response.json()
print(f"Table: {result['table_name']}")
print(f"Rows: {result['row_count']}")
print(f"Schema: {result['table_schema']}")
```

**Expected Response**:
```json
{
  "table_name": "products",
  "table_schema": {
    "id": "INTEGER",
    "name": "TEXT",
    "price": "REAL",
    "category": "TEXT"
  },
  "row_count": 1250,
  "sample_data": [
    {"id": 1, "name": "Wireless Mouse", "price": 29.99, "category": "Electronics"},
    {"id": 2, "name": "USB Cable", "price": 9.99, "category": "Accessories"}
  ]
}
```

---

#### STEP 3: Execute Natural Language Query

**Using cURL**:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me the top 10 products by price in the Electronics category"
  }'
```

**Using Python**:
```python
query = "Find all products cheaper than $50"

response = httpx.post(
    "http://localhost:8000/api/query",
    json={"query": query}
)

data = response.json()
print(f"Generated SQL: {data['sql']}")
print(f"Rows: {data['row_count']}")
print(f"Time: {data['execution_time_ms']}ms")

for row in data['results'][:5]:
    print(row)
```

**Expected Response**:
```json
{
  "sql": "SELECT * FROM products WHERE category = 'Electronics' ORDER BY price DESC LIMIT 10",
  "results": [
    {"id": 45, "name": "Gaming Laptop", "price": 1299.99, "category": "Electronics"},
    {"id": 78, "name": "4K Monitor", "price": 599.99, "category": "Electronics"}
  ],
  "columns": ["id", "name", "price", "category"],
  "row_count": 10,
  "execution_time_ms": 45.23
}
```

---

#### STEP 4: Export Results (Optional)

**Export Entire Table**:
```bash
curl -X POST http://localhost:8000/api/export/table \
  -H "Content-Type: application/json" \
  -d '{"table_name": "products"}' \
  --output products_export.csv
```

**Export Query Results**:
```python
query_result = httpx.post("http://localhost:8000/api/query", json={
    "query": "SELECT * FROM products WHERE price < 50"
}).json()

export_response = httpx.post(
    "http://localhost:8000/api/export/query",
    json={
        "data": query_result['results'],
        "columns": query_result['columns']
    }
)

with open("filtered_products.csv", "wb") as f:
    f.write(export_response.content)
```

---

### Prerequisites Checklist

- [ ] Python 3.12+ installed
- [ ] FastAPI server dependencies installed (`uv sync`)
- [ ] `.env` file configured with API keys
- [ ] Data file in supported format (CSV/JSON/JSONL)
- [ ] Server running on port 8000 (or custom port)

---

### Troubleshooting

**Issue**: File upload fails with "unsupported format"
- **Fix**: Ensure file extension is .csv, .json, or .jsonl
- **Fix**: Check file is not corrupted (open in text editor)

**Issue**: Query returns empty results
- **Fix**: Check table exists (`GET /api/schema`)
- **Fix**: Verify query syntax makes sense for your data
- **Fix**: Try simpler query first ("Show all data from table")

**Issue**: Server crashes during upload
- **Fix**: Check file size (very large files may need streaming)
- **Fix**: Verify CSV format is valid (no malformed rows)

**Issue**: Natural language query generates incorrect SQL
- **Fix**: Be more specific in natural language description
- **Fix**: Mention exact column names from schema
- **Example**: "Show products where price column is less than 50"

---

## 5. Navigation & Discovery

**Purpose**: Navigate ECOMLM.CODEXA hierarchy and discover available agents/commands

**Time Estimate**: 2-5 minutes

**Prerequisites**: None (entry-level workflow)

---

### Fractal Navigation Hierarchy

```
Level 1: ROOT (codexa/)
    │
    ├── /prime → General status + routing
    │
    └── Level 2: SYSTEM (codexa.app/)
            │
            ├── /prime-codexa → Meta-construction specialist
            │
            └── Level 3: AGENTS (agentes/)
                    │
                    ├── /prime-anuncio → E-commerce ads
                    ├── /prime-pesquisa → Market research
                    ├── /prime-marca → Brand strategy
                    ├── /prime-mentor → Strategic planning
                    ├── /prime-scout → Code navigation
                    ├── /prime-knowledge → ML & knowledge extraction
                    │
                    └── Level 4: INDIVIDUAL AGENT ({agent}/)
                            │
                            └── Agent-specific PRIME.md & documentation
```

---

### Step-by-Step Instructions

#### STEP 1: Start at ROOT

```bash
/prime
```

**What You'll See**:
- System overview
- 4-level navigation hierarchy
- Quick commands reference
- Routing decision tree

**Use This When**:
- Starting a new session
- Unsure which agent to use
- Need system-wide status

---

#### STEP 2: Navigate to System Level (Meta-Construction)

```bash
/prime-codexa
```

**What You'll See**:
- Meta-construction context loaded
- 9 builders available
- 4 validators available
- 3 HOPs (Higher-Order Prompts)
- Ready for agent creation, HOP generation, orchestration

**Use This When**:
- Building new agents
- Creating HOPs or commands
- Orchestrating workflows
- Self-improvement tasks

---

#### STEP 3: Navigate to Agent Level

**E-Commerce Agents**:
```bash
/prime-anuncio    # Product listing generation
/prime-pesquisa   # Market research
/prime-marca      # Brand strategy (beta)
```

**System Agents**:
```bash
/prime-mentor      # Strategic planning
/prime-scout       # Code navigation
/prime-knowledge   # ML & knowledge extraction
```

**What You'll See**:
- Agent-specific capabilities
- Available commands
- Input/output formats
- Usage examples

**Use This When**:
- Ready to execute domain-specific task
- Need agent-specific documentation
- Want to understand agent capabilities

---

#### STEP 4: Discovery Commands

**List All Available Commands**:
```bash
# Check .claude/commands/ directory
ls .claude/commands/

# Or use help
/help
```

**Agent-Specific Commands**:
Each agent may have its own commands following pattern:
- `/prime-{agent}` - Load agent context
- `/{agent} [args]` - Execute agent primary function
- `/codexa-build_{type}` - Meta-construction commands

---

### Decision Tree: Which Agent to Use?

```
What do you want to do?

1. Build/Create Something New
   ├── New Agent → /prime-codexa → /codexa-build_agent
   ├── New HOP → /prime-codexa → /codexa-build_prompt
   └── New Command → /prime-codexa → /codexa-build_command

2. E-Commerce Task
   ├── Research Product → /prime-pesquisa → /pesquisa "product"
   ├── Create Listing → /prime-anuncio → /anuncio research_notes.md
   └── Brand Strategy → /prime-marca → /marca

3. System Task
   ├── Strategic Planning → /prime-mentor
   ├── Navigate Code → /prime-scout
   └── Extract Knowledge → /prime-knowledge

4. Data Analysis
   ├── Upload Data → Start FastAPI server → POST /api/upload
   └── Query Data → POST /api/query

5. Unsure / General Help
   └── /prime → Read overview → Follow routing guide
```

---

### Troubleshooting

**Issue**: Command not found
- **Fix**: Check command spelling (exact match required)
- **Fix**: Verify command exists in `.claude/commands/`
- **Fix**: Check if agent is loaded first (some commands require `/prime-{agent}` first)

**Issue**: Wrong agent loaded
- **Fix**: Load correct agent with `/prime-{agent}`
- **Note**: Loading a new agent replaces current context

**Issue**: Don't know which agent to use
- **Fix**: Start with `/prime` and read routing guide
- **Fix**: Use decision tree above
- **Fix**: Ask for clarification (describe your goal)

---

## 6. Troubleshooting Common Issues

### General Issues

#### API Key Errors

**Symptom**: "ANTHROPIC_API_KEY not found" or "Authentication failed"

**Solutions**:
1. Check `.env` file exists in correct directory:
   - For agents: `codexa.app/agentes/.env`
   - For server: `app/server/.env`

2. Verify `.env` format:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   # or
   OPENAI_API_KEY=sk-...
   ```

3. Reload environment:
   ```bash
   source .env  # Linux/Mac
   # or restart terminal/IDE
   ```

---

#### Rate Limiting

**Symptom**: "Rate limit exceeded" or "Too many requests"

**Solutions**:
1. Built-in retry with exponential backoff (1s→2s→4s) should handle this automatically
2. If persists, wait 1 minute and retry
3. Check API quota/billing status
4. Consider using lower-tier model (sonnet instead of opus)

---

#### File Not Found Errors

**Symptom**: "File not found" or "Path does not exist"

**Solutions**:
1. Verify file path is absolute or relative to current directory
2. Check file permissions (readable)
3. Ensure file was created by previous step (check workflow log)
4. Use absolute paths when unsure:
   ```python
   from pathlib import Path
   file_path = Path("data/products.csv").absolute()
   ```

---

### Agent-Specific Issues

#### Pesquisa Agent

**Issue**: Insufficient competitor data
- **Fix**: Provide more specific product category
- **Fix**: Include price range in description
- **Fix**: Mention target marketplace if specific

**Issue**: Keywords seem irrelevant
- **Fix**: Review research_notes.md for accuracy
- **Fix**: Provide clearer product description
- **Fix**: Re-run with refined input

---

#### Anuncio Agent

**Issue**: Compliance validation fails
- **Fix**: Ensure research_notes.md has all 22 blocks
- **Fix**: Verify product category is allowed in target marketplace
- **Fix**: Check for restricted keywords (weapons, pharmaceuticals, etc.)

**Issue**: Listings too generic
- **Fix**: Include brand_strategy.md for personalization
- **Fix**: Provide more detailed research_notes.md
- **Fix**: Specify unique selling points in initial description

---

#### CODEXA Agent

**Issue**: Agent construction fails at Phase 2
- **Fix**: Provide more detailed agent description
- **Fix**: Specify capabilities explicitly (3-5 bullet points)
- **Fix**: Re-run with `--verbose` flag for diagnostics

**Issue**: Quality score <7.0
- **Fix**: Review META_CONSTRUCTION_LOG.md for weak areas
- **Fix**: Re-run specific phase (not full workflow)
- **Fix**: Check MASTER_INSTRUCTIONS word count (should be 2000-5000)

---

### FastAPI Server Issues

**Issue**: Server won't start
- **Fix**: Check port 8000 not already in use:
  ```bash
  # Linux/Mac
  lsof -i :8000
  # Windows
  netstat -ano | findstr :8000
  ```
- **Fix**: Use different port: `BACKEND_PORT=8001 uv run python server.py`
- **Fix**: Check dependencies installed: `uv sync`

**Issue**: Database locked
- **Fix**: Close other connections to `db/database.db`
- **Fix**: Restart server
- **Fix**: Delete `db/database.db` (will recreate empty)

---

## 📚 Related Documentation

- [API Reference](./API_REFERENCE.md) - Complete API documentation with examples
- [HOP Framework](./HOP_FRAMEWORK.md) - TAC-7 framework guide
- [Agent Registry](../codexa.app/51_AGENT_REGISTRY.json) - All agent specifications
- [PRIME.md](../PRIME.md) - System navigator
- [CODEXA Agent](../codexa.app/agentes/codexa_agent/README.md) - Meta-constructor documentation

---

**Last Updated**: 2025-11-14
**Maintained By**: CODEXA Team
**Status**: Production Documentation
**Version**: 1.0.0
