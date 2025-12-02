# FONTES - External Documentation System

**Sistema de documentação externa sempre atualizada para Mentor Agent**

---

## 🎯 **O QUE É FONTES/**

FONTES/ é o sistema de **conhecimento externo vivo** do Mentor Agent que mantém documentação atualizada de:

- 🤖 **LLM Platforms** - Anthropic, OpenAI, Google, Cohere
- 🛒 **Marketplaces** - Mercado Livre, Shopee, Amazon BR, Magalu
- 🛠️ **Frameworks** - LangChain, Vercel AI SDK, LlamaIndex, CrewAI
- 📚 **E-commerce** - SEO, copywriting, CRO, analytics

## 🏗️ **ARQUITETURA**

```
FONTES/
├── catalogo_fontes.json          # Master index of all sources
├── README.md (this file)          # Complete usage guide
│
├── LLM_PLATFORMS/                 # LLM provider docs
│   ├── README.md
│   ├── anthropic/
│   │   ├── _index.json
│   │   ├── api_reference.md
│   │   ├── prompt_engineering.md
│   │   ├── vision.md
│   │   ├── tool_use.md
│   │   └── streaming.md
│   ├── openai/
│   ├── google/
│   └── cohere/
│
├── MARKETPLACES/                  # Brazilian marketplace APIs
│   ├── README.md
│   ├── mercadolivre/
│   │   ├── _index.json
│   │   ├── api_reference.md
│   │   ├── listings_guide.md
│   │   ├── seo_guide.md
│   │   └── best_practices.md
│   ├── shopee/
│   ├── amazon_br/
│   └── magalu/
│
├── FRAMEWORKS/                    # AI/LLM development frameworks
│   ├── README.md
│   ├── langchain/
│   ├── vercel_ai_sdk/
│   ├── llamaindex/
│   └── crewai/
│
└── ECOMMERCE/                     # E-commerce best practices
    ├── README.md
    ├── seo/
    ├── copywriting/
    ├── conversion/
    └── analytics/
```

---

## 🚀 **QUICK START** (Simplificado v2.1.0)

### Comando Único (Recomendado)

```bash
/fontes sync                      # Sync completo (check + refresh + validate)
/fontes sync --priority critical  # Apenas fontes críticas
/fontes status                    # Ver estado atual
/fontes validate                  # Validar saúde dos links
```

**99% dos casos**: Use apenas `/fontes sync`

### Alternativa: CLI Direto

```bash
python scripts/fontes.py sync
python scripts/fontes.py status --show-pending
python scripts/fontes.py validate
```

### ⚡ ULTRA-QUICK
```bash
# Tudo que você precisa
/fontes sync
```

---

## 📖 **USO PELO SCOUT**

O **Scout** agora busca automaticamente em FONTES/ quando detecta queries sobre:

### Queries que Ativam Busca em FONTES/

```python
# LLM platforms
"como usar anthropic claude api"
"openai gpt best practices"
"google gemini prompt engineering"

# Marketplaces
"mercado livre api integration"
"shopee product management"
"amazon seller api"

# Frameworks
"langchain agents tutorial"
"vercel ai sdk streaming"
"llamaindex rag implementation"

# E-commerce
"google seo best practices"
"copywriting conversion techniques"
"ab testing methodology"
```

### Exemplo de Uso

```python
from src.scout_fontes import ScoutFontes

scout = ScoutFontes(mentor_root)

# Smart search (decides automatically)
results = scout.smart_search("claude api tool use", top_k=5)

for result in results:
    print(f"[{result.source_type}] {result.categoria} - {result.assunto}")
    print(f"File: {result.file_path}")
    print(f"Relevance: {result.relevance_score}")
```

---

## 🔄 **REFRESH WORKFLOW**

### Automated Workflow

```
┌─────────────────────────────────────────────────┐
│  FONTES/ Refresh Workflow                       │
└─────────────────────────────────────────────────┘

1. CHECK FOR UPDATES
   ├─ Fetch URL headers (Last-Modified, ETag)
   ├─ Compare with cached hashes
   └─ Log updates detected

2. FETCH CONTENT (if updated)
   ├─ Download HTML from official docs
   ├─ Extract main content (remove nav/footer)
   └─ Convert HTML to Markdown

3. SAVE LOCALLY
   ├─ Save to FONTES/[categoria]/[plataforma]/
   ├─ Add metadata header (source URL, fetch date)
   └─ Create/update _index.json

4. UPDATE CATALOG
   ├─ Update last_refresh timestamp
   ├─ Update next_refresh date
   └─ Save catalogo_fontes.json

5. GENERATE REPORT
   ├─ Summary (total, updated, errors)
   ├─ Details per fonte
   └─ Save to outputs/fontes_reports/
```

### Manual Workflow

```bash
# Step 1: Check what needs updating
python scripts/fontes/check_updates.py --all

# Step 2: Review updates_available.json
cat FONTES/updates_available.json

# Step 3: Sync specific fonte
python scripts/fontes/refresh_fonte.py --fonte anthropic_docs

# Step 4: Validate links
python scripts/fontes/validate_links.py --all

# Step 5: Review reports
ls outputs/fontes_reports/
```

---

## 📊 **CATALOGO_FONTES.JSON**

### Structure

```json
{
  "fontes": [
    {
      "id": "anthropic_docs",
      "categoria": "LLM_PLATFORMS",
      "plataforma": "anthropic",
      "nome": "Anthropic Claude Documentation",
      "url_oficial": "https://docs.anthropic.com",
      "urls_especificas": {
        "api_reference": "https://docs.anthropic.com/en/api/...",
        "prompt_engineering": "https://docs.anthropic.com/en/docs/..."
      },
      "arquivos_locais": [
        "FONTES/LLM_PLATFORMS/anthropic/api_reference.md",
        "FONTES/LLM_PLATFORMS/anthropic/prompt_engineering.md"
      ],
      "topics": ["claude_api", "prompt_engineering", "tool_use"],
      "refresh_frequency": "weekly",
      "last_refresh": "2025-11-24T10:00:00",
      "status": "active",
      "priority": "critical",
      "aplicacao": [
        "quando_desenvolver_agentes_llm",
        "quando_otimizar_prompts"
      ]
    }
  ],
  "categorias": [...],
  "refresh_schedule": {...},
  "automation": {...}
}
```

### Key Fields

- **fonte_id**: Unique identifier
- **categoria**: LLM_PLATFORMS | MARKETPLACES | FRAMEWORKS | ECOMMERCE
- **priority**: critical | high | medium | low
- **refresh_frequency**: weekly | bi-weekly | monthly | quarterly
- **status**: active | inactive | deprecated
- **aplicacao**: When to use this fonte (context triggers)

---

## 🔧 **SCRIPTS REFERENCE**

### check_updates.py

**Purpose**: Detect if external docs have been updated

```bash
python scripts/fontes/check_updates.py --all
python scripts/fontes/check_updates.py --fonte anthropic_docs
python scripts/fontes/check_updates.py --priority critical
python scripts/fontes/check_updates.py --force
```

**Output**: `FONTES/updates_available.json`

### refresh_fonte.py

**Purpose**: Fetch and save updated documentation

```bash
python scripts/fontes/refresh_fonte.py --fonte anthropic_docs
python scripts/fontes/refresh_fonte.py --priority critical
python scripts/fontes/refresh_fonte.py --all
```

**Output**: Updated .md files in FONTES/[categoria]/[plataforma]/

### sync_all.py

**Purpose**: Master sync script (check + refresh + validate)

```bash
python scripts/fontes/sync_all.py --dry-run
python scripts/fontes/sync_all.py --priority critical
python scripts/fontes/sync_all.py --force
```

**Output**:
- Updated documentation
- `outputs/fontes_reports/sync_report_*.json`
- `outputs/fontes_reports/sync_report_*.md`

### validate_links.py

**Purpose**: Validate all URLs are accessible

```bash
python scripts/fontes/validate_links.py --all
python scripts/fontes/validate_links.py --fonte anthropic_docs
python scripts/fontes/validate_links.py --priority critical
```

**Output**: `outputs/fontes_reports/validation_report_*.json`

---

## 📅 **REFRESH SCHEDULE**

| Priority | Frequency | Day | Fontes |
|----------|-----------|-----|--------|
| **Critical** | Weekly | Monday | Anthropic, Mercado Livre |
| **High** | Weekly | Monday | OpenAI, Google AI, LangChain, Vercel AI |
| **Medium** | Bi-weekly | Monday | Cohere, Shopee, Amazon, LlamaIndex, CrewAI |
| **Low** | Monthly | 1st Monday | SEO guides, copywriting, analytics |

### Automation Setup

Add to cron (Linux/Mac) or Task Scheduler (Windows):

```bash
# Every Monday at 8 AM - Check critical sources
0 8 * * 1 cd /path/to/mentor_agent && python scripts/fontes/sync_all.py --priority critical

# Every day at 9 AM - Quick validation check
0 9 * * * cd /path/to/mentor_agent && python scripts/fontes/check_updates.py --all
```

---

## 🎯 **WHEN TO USE FONTES/**

### Use FONTES/ when:

1. **Developing with LLM APIs**
   - ✅ Learning Anthropic Claude API
   - ✅ Implementing OpenAI GPT features
   - ✅ Comparing different LLM providers
   - ✅ Studying prompt engineering best practices

2. **Integrating Marketplace APIs**
   - ✅ Building Mercado Livre integrations
   - ✅ Automating Shopee listings
   - ✅ Understanding Amazon Seller API
   - ✅ Optimizing marketplace SEO

3. **Building with AI Frameworks**
   - ✅ Creating LangChain agents
   - ✅ Implementing RAG with LlamaIndex
   - ✅ Building UI with Vercel AI SDK
   - ✅ Orchestrating multi-agent systems

4. **Applying E-commerce Best Practices**
   - ✅ Learning Google SEO guidelines
   - ✅ Writing conversion-focused copy
   - ✅ Setting up A/B tests
   - ✅ Tracking with Google Analytics

### Use PROCESSADOS/ when:

- ❓ Seller-specific knowledge (internal business logic)
- ❓ Processed seller materials (USER/ → PROCESSADOS/)
- ❓ Synthesized knowledge from multiple sources
- ❓ Brazil-specific seller tactics and strategies

---

## 🔍 **SEARCH INTEGRATION**

### Scout Auto-Detection

Scout automatically determines when to search FONTES/ based on keywords:

```python
# Keywords that trigger FONTES/ search
FONTES_KEYWORDS = [
    # LLM platforms
    'anthropic', 'claude', 'openai', 'gpt', 'gemini', 'cohere',
    'api', 'llm', 'prompt engineering', 'function calling',

    # Marketplaces
    'mercado livre', 'shopee', 'amazon', 'magalu', 'marketplace api',

    # Frameworks
    'langchain', 'vercel', 'llamaindex', 'crewai', 'rag', 'agents',

    # E-commerce
    'seo', 'google search', 'copywriting', 'conversion', 'analytics'
]
```

### Search Priority

When both PROCESSADOS/ and FONTES/ have relevant results:

1. **Combine** results from both sources
2. **Sort** by relevance score
3. **Prefer** PROCESSADOS/ for seller-specific content
4. **Prefer** FONTES/ for technical/platform documentation
5. **Return** top K results (default: 5)

---

## 📝 **ADDING NEW FONTES**

### Step 1: Add to catalogo_fontes.json

```json
{
  "id": "new_platform_docs",
  "categoria": "LLM_PLATFORMS",
  "plataforma": "new_platform",
  "nome": "New Platform Documentation",
  "url_oficial": "https://docs.newplatform.com",
  "urls_especificas": {
    "api": "https://docs.newplatform.com/api",
    "guide": "https://docs.newplatform.com/guide"
  },
  "arquivos_locais": [
    "FONTES/LLM_PLATFORMS/new_platform/api.md",
    "FONTES/LLM_PLATFORMS/new_platform/guide.md"
  ],
  "topics": ["api", "guide", "examples"],
  "refresh_frequency": "weekly",
  "last_refresh": null,
  "status": "active",
  "priority": "high",
  "aplicacao": ["quando_usar_new_platform"]
}
```

### Step 2: Create Directory

```bash
mkdir -p FONTES/LLM_PLATFORMS/new_platform
```

### Step 3: Fetch Initial Documentation

```bash
python scripts/fontes/refresh_fonte.py --fonte new_platform_docs
```

### Step 4: Verify

```bash
ls FONTES/LLM_PLATFORMS/new_platform/
cat FONTES/LLM_PLATFORMS/new_platform/_index.json
```

---

## 🚨 **TROUBLESHOOTING**

### Issue: "No updates detected" but docs have changed

**Solution**:
```bash
# Clear cache and force refresh
rm -rf FONTES/.cache/
python scripts/fontes/refresh_fonte.py --fonte [FONTE_ID]
```

### Issue: "Connection timeout" during refresh

**Solution**:
1. Check internet connection
2. Verify URL is accessible: `curl -I [URL]`
3. Increase timeout in refresh_fonte.py
4. Try again later (rate limiting)

### Issue: "Invalid markdown generated"

**Solution**:
1. Check if URL structure changed
2. Update HTML selector in extract_main_content()
3. Manually fetch and inspect HTML
4. Adjust conversion settings in refresh_fonte.py

### Issue: "Links broken" in validation

**Solution**:
```bash
# Identify broken links
python scripts/fontes/validate_links.py --all

# Check reports
cat outputs/fontes_reports/validation_report_*.md

# Update URLs in catalogo_fontes.json
# Re-fetch affected fontes
```

---

## 📊 **METRICS & MONITORING**

### Key Metrics

- **Total Fontes**: 16 sources
- **Total Documentation Files**: ~80+ files
- **Coverage**: 4 categories
- **Update Frequency**: Daily checks, weekly/monthly syncs
- **Success Rate**: Target >95% accessibility

### Reports Generated

All reports saved to: `outputs/fontes_reports/`

- `sync_report_*.json` - Full sync details
- `sync_report_*.md` - Human-readable summary
- `validation_report_*.json` - Link validation results
- `validation_report_*.md` - Broken links summary

### Monitoring Commands

```bash
# Check last refresh dates
jq '.fontes[] | {id: .id, last_refresh: .last_refresh}' FONTES/catalogo_fontes.json

# Count total files
find FONTES -name "*.md" -not -name "README.md" | wc -l

# Check for pending updates
cat FONTES/updates_available.json

# Review latest sync report
ls -t outputs/fontes_reports/sync_report_*.md | head -1 | xargs cat
```

---

## 🎯 **BEST PRACTICES**

### DO:
- ✅ Run weekly checks for critical sources
- ✅ Review reports after each sync
- ✅ Keep catalogo_fontes.json organized
- ✅ Use smart_search() for queries
- ✅ Add new sources as needed
- ✅ Validate links regularly

### DON'T:
- ❌ Manual edits to fetched .md files (will be overwritten)
- ❌ Skip validation after major updates
- ❌ Ignore broken link warnings
- ❌ Store sensitive data in FONTES/
- ❌ Commit large binary files
- ❌ Disable automation without reason

---

## 🔗 **RELATED SYSTEMS**

### Integration with:

- **Scout** - `src/scout_fontes.py` - Unified search
- **PROCESSADOS/** - Internal knowledge base
- **RASCUNHO/** - Raw input processing
- **Mentor Agent** - Main agent orchestration

### Extends:

- Knowledge coverage (internal + external)
- Always up-to-date documentation
- Self-updating intelligence
- Platform-specific best practices

---

## 📚 **RESOURCES**

### Documentation
- [Anthropic Docs](https://docs.anthropic.com)
- [OpenAI Docs](https://platform.openai.com/docs)
- [Google AI Docs](https://ai.google.dev/docs)
- [Mercado Livre Developers](https://developers.mercadolivre.com.br)
- [LangChain Docs](https://python.langchain.com/docs)
- [Vercel AI SDK](https://sdk.vercel.ai/docs)

### Tools Used
- `requests` - HTTP fetching
- `BeautifulSoup` - HTML parsing
- `html2text` - HTML to Markdown conversion
- `json` - Catalog management

---

**Version**: 1.0.0
**Created**: 2025-11-24
**Agent**: mentor_agent
**Purpose**: External documentation management
**Status**: ✅ Production Ready

---

> 💡 **Pro Tip**: Use `/refresh_fontes check` weekly to stay updated with the latest platform changes!
