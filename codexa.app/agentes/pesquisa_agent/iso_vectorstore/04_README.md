<!-- iso_vectorstore -->
<!--
  Source: README.md
  Agent: pesquisa_agent
  Synced: 2025-11-30
  Version: 3.0.0
  Package: iso_vectorstore (export package)
-->

# Pesquisa Agent v3.0.0 | Brazilian E-commerce Research

**Isolated, portable, LLM-agnostic market research agent** for Brazilian marketplaces.

**Framework**: 12 Leverage Points | **Architecture**: Dual-Layer ADW+HOP | **Files**: ~90

---

## 🚀 QUICK START

1. **Read** `PRIME.md` - Complete agent instructions (includes Claude Code tools mapping)
2. **Setup** your LLM platform - See `SETUP.md`
3. **Provide brief** - Minimum 4 fields (product, category, audience, price)
4. **Get output** - 22-block `research_notes.md` in `user_research/`

---

## 🔧 CLAUDE CODE TOOLS

When running in Claude Code, capabilities auto-map:

| Capability | Tool | Status |
|------------|------|--------|
| web_search | **WebSearch** | ✅ Required |
| vision | **Read** (images) | ✅ Available |
| file_search | **Grep** + **Glob** | ✅ Available |
| web_fetch | **WebFetch** | ✅ 1380+ URLs |

---

## 📂 STRUCTURE (~90 Files)

```
pesquisa_agent/
│
├── 📄 PRIME.md ⭐                  # Entry point (TAC-7 + tools mapping)
├── 📄 SETUP.md                     # Platform setup (Claude/OpenAI/Gemini/Local)
├── 📄 README.md                    # This file
├── 📄 INSTRUCTIONS.md              # Detailed execution guide
├── 📄 .env.example                 # Capabilities config template
│
├── 📁 config/ (6 files)
│   ├── agent.json                  # Agent configuration
│   ├── marketplaces.json           # 9 BR marketplaces + policies
│   ├── accessible_urls.md          # 1380+ tested URLs for research
│   ├── brief_schema.json           # Input validation schema
│   ├── execution_plan_schema.json  # Plan schema
│   └── plans/
│       ├── standard_research.json  # Default 9-step plan (20-30 min)
│       └── comprehensive_research.json # Deep dive (60+ min)
│
├── 📁 prompts/ (12 modular HOPs)
│   ├── main_agent_hop.md           # HOP orchestrator
│   ├── intake_validation.md        # Brief validation
│   ├── web_search_inbound.md       # Marketplace search (9 BR)
│   ├── web_search_outbound.md      # SERP + social search
│   ├── competitor_analysis.md      # Competitor deep dive
│   ├── seo_taxonomy.md             # SEO keyword extraction
│   ├── image_analysis.md           # Visual analysis
│   ├── price_comparison.md         # Pricing intelligence
│   ├── sentiment_analysis.md       # Review sentiment
│   ├── gap_identification.md       # Market gaps
│   ├── trend_analysis.md           # Trend identification
│   └── strategy_gaps.md            # Strategic opportunities
│
├── 📁 iso_vectorstore/ (20 files) 🆕
│   ├── 01_QUICK_START.md           # Compact guide for external LLMs
│   ├── 02_PRIME.md                 # Full framework
│   ├── 03-04                       # Instructions + README
│   ├── 05-09                       # Architecture + JSON configs
│   ├── 10-12                       # HOP orchestration + ADW workflow
│   ├── 13-19                       # Research modules
│   └── 20_CHANGELOG.md             # Version history
│   └── (Upload to OpenAI/Custom GPT knowledge base)
│
├── 📁 competitor_intelligence/ (40+ sources) 🆕
│   ├── INDEX.md                    # Navigation hub
│   ├── QUICKSTART.md               # 5-minute setup
│   ├── README.md                   # Full documentation
│   ├── config.json                 # System config
│   ├── sources/                    # 4 JSON source databases
│   │   ├── ai_courses_platforms.json    (10 courses)
│   │   ├── marketplaces_docs.json       (9 marketplaces)
│   │   ├── ecommerce_trends.json        (12 news/research)
│   │   └── compliance_sources.json      (8 regulations)
│   ├── docs/                       # Fetched documentation
│   ├── snapshots/                  # Historical data
│   └── scripts/                    # Automation tools
│
├── 📁 templates/ (2 files)
│   ├── research_notes.md           # 22-block output template
│   └── research_notes.llm.json.template # LLM-structured schema
│
├── 📁 workflows/ (6 files)
│   ├── 100_ADW_RUN_PESQUISA.md     # Main execution workflow
│   ├── ADW_TEMPLATE.md             # Workflow template
│   └── README_WORKFLOWS.md         # Documentation
│
├── 📁 commands/ (2 files)
│   ├── pesquisa.md                 # /pesquisa slash command
│   └── update-competitor-docs.md   # /update-competitor-docs
│
└── 📁 user_research/ (output)
    ├── [produto]_research_notes.md     # 22-block report
    ├── [produto]_research_notes.llm.json # LLM-structured
    ├── [produto]_metadata.json          # Quality scores
    └── [produto]_queries.json           # Web searches logged
```

**Total**: ~90 files (organized in 8 directories)

---

## ⚡ CAPABILITIES

### Required
- ✅ **web_search** - REQUIRED (cannot run without it)

### Optional (Auto-detected)
- 📄 **vision** - Screenshot analysis of marketplaces
- 📄 **file_search** - Compliance rules lookup (ANVISA, INMETRO)
- 📄 **code_interpreter** - Advanced metrics calculation

---

## 🎯 OUTPUT (22 Blocks)

**research_notes.md** structure:
1. Lacunas do Brief
2. Head Terms Prioritários
3. Longtails
4. Sinônimos e Variações
5. Termo Contextual e Ocasião
6. Dores do Público
7. Ganhos Desejados
8. Objeções e Respostas
9. Provas e Evidências
10. Diferenciais Competitivos
11. Riscos ou Alertas
12. Análise de Concorrentes (≥3)
13. Benchmark de Concorrentes
14. Estratégias e Gaps
15. Padrões de Linguagem
16. SEO Outbound
17. SEO Inbound
18. Regras Críticas de Marketplace
19. Decisões de Copy Iniciais
20. Consultas Web (≥15 logged)
21. Imagens Analisadas (if applicable)
22. Resumo Executivo

---

## 🤖 PLATFORM SUPPORT

| Platform | Status | Setup Guide |
|----------|--------|-------------|
| **Claude Code** | ✅ Tested | `SETUP.md` → Section 1 |
| **OpenAI Assistants** | ✅ Tested | `SETUP.md` → Section 2 |
| **Gemini AI Studio** | ✅ Tested | `SETUP.md` → Section 3 |
| **Local LLMs** | ⚠️ Experimental | `SETUP.md` → Section 4 |

---

## 📖 EXAMPLE BRIEF

**Minimum**:
```
Product: Fone de ouvido Bluetooth esportivo
Category: Eletrônicos > Áudio
Target Audience: Atletas, 18-35 anos
Price Range: R$ 150 - R$ 280
```

**Recommended** (add):
```
Marketplace: Mercado Livre (primary)
Competitors: JBL Endurance Run, Xiaomi Mi Sports
Special Requirements: Resistente à água (IPX5+)
```

---

## ✅ QUALITY GATES

Outputs validated against:
- ✅ ≥3 competitors analyzed
- ✅ ≥15 web queries logged with URLs
- ✅ All 22 blocks present
- ✅ ≤10% [SUGESTÃO] placeholders
- ✅ Confidence score ≥0.75/1.0

---

## 🔧 CONFIGURATION

### Option 1: Auto-detect (Default)
Agent detects capabilities on first run. No setup needed.

### Option 2: Declare via .env
```bash
cp .env.example .env
# Edit .env:
WEB_SEARCH=true
VISION=true
FILE_SEARCH=false
CODE_INTERPRETER=false
```

---

## 🌐 BRAZILIAN MARKETPLACES

**9 Marketplaces Supported**:
1. Mercado Livre (priority 1)
2. Shopee (priority 2)
3. Magazine Luiza (priority 3)
4. Amazon BR (priority 4)
5. Americanas
6. Casas Bahia
7. TikTok Shop
8. Shein
9. Submarino

**+ Social/SERP**:
- YouTube (product reviews)
- TikTok (demos)
- Instagram (visual trends)
- Google SERP (organic keywords)
- Reclame Aqui (risk analysis) - REQUIRED

---

## 📊 PERFORMANCE

| Metric | Target |
|--------|--------|
| **Execution Time** | 20-30 min (standard research) |
| **Quality Score** | ≥0.75/1.0 |
| **Completeness** | ≥75% |
| **Competitors** | ≥3 analyzed |
| **Web Queries** | ≥15 logged |

---

## 🔗 INTEGRATION

**Upstream**:
- User brief (required)
- marca_agent brand guidelines (optional)

**Downstream**:
- `anuncio_agent` - Ad copy generation
- `marca_agent` - Brand strategy
- `USER_DOCS/produtos/` - Product docs

---

## 🐛 TROUBLESHOOTING

### "web_search not available"
→ See `SETUP.md` for platform-specific web search enablement

### "Low quality score (<0.75)"
→ Re-run with more detailed brief or additional competitors

### "Output not saved to user_research/"
→ Check folder exists and has write permissions

### "Too many [SUGESTÃO] placeholders"
→ Niche product or limited public data - supplement with manual research

---

## 📚 DOCUMENTATION

- **PRIME.md** - Complete TAC-7 agent instructions (MAIN FILE)
- **SETUP.md** - Platform-specific setup guides
- **config/agent.json** - Technical configuration
- **config/marketplaces.json** - Brazilian marketplace database
- **.env.example** - Capabilities declaration template

---

## 🎯 USE CASES

1. **Pre-launch Research** - Understand market before launch (20-30min)
2. **Competitor Monitoring** - Track competition strategies (15-20min)
3. **Ad Optimization** - Improve low-conversion ads (15-20min)
4. **SEO Planning** - Extract keywords for content (15-20min)
5. **New Marketplace Entry** - Adapt for new channel (20-25min)

---

## 🚦 VERSION

**Current**: v2.6.0 (2025-11-26)
- ✅ **Claude Code Tools Mapping** - Direct mapping to WebSearch, Read, Grep, Glob
- ✅ **iso_vectorstore Documentation** - 20-file knowledge base documented
- ✅ **competitor_intelligence Integration** - 40+ sources integrated
- ✅ **12 Leverage Points Framework** - Full implementation
- ✅ **~90 Files Structure** - Complete documentation of all components
- ✅ Full isolation (no external dependencies)
- ✅ LLM-agnostic (works on any platform)
- ✅ Auto-capability detection

**Previous**: v2.5 (12 Leverage Points), v2.1 (Isolation), v2.0 (HOP), v1.1 (Vision), v1.0 (Initial)

---

## 💡 NEXT STEPS

1. **First time?** → Read `SETUP.md` for your platform
2. **Ready to test?** → Load `PRIME.md` and provide a brief
3. **Need help?** → Check `SETUP.md` → Troubleshooting section
4. **Want custom workflow?** → See `config/plans/standard_research.json`

---

**Status**: ✅ Production-ready
**Version**: 3.0.0
**Isolation**: Full
**Portability**: Universal (Claude, OpenAI, Gemini, Local LLMs)
**Quality**: Enterprise-grade (≥0.75 confidence)
**Framework**: 12 Leverage Points
**Files**: ~90 (8 directories)
