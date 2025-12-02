# ARCHITECTURE | mentor_agent v2.5.0

**Purpose**: Technical architecture and system design for mentor_agent
**Version**: 2.5.0 | **Updated**: 2025-11-25
**Framework**: 12 Leverage Points + Dual-Layer ADW+HOP

---

## SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                      MENTOR AGENT v2.5.0                        │
│            Knowledge + Discovery + Mentoring System             │
├─────────────────────────────────────────────────────────────────┤
│  INPUT                    │  PROCESSING           │  OUTPUT     │
│  ─────                    │  ──────────           │  ──────     │
│  RASCUNHO/  ────────────► │  Extract → Classify   │  PROCESSADOS/
│  (raw files)              │  Synthesize → Validate│  (flat .md) │
│                           │                       │             │
│  USER/      ────────────► │  Scout → Search       │  Responses  │
│  (seller files)           │  Synthesize → Respond │  (answers)  │
│                           │                       │             │
│  Questions  ────────────► │  Discovery-First      │  Lessons    │
│  (seller asks)            │  Catalog → Knowledge  │  (aulas)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## DUAL-LAYER ARCHITECTURE (ADW ↔ HOP)

### Layer 1: ADW (Orchestration)
- **Purpose**: High-level workflow coordination
- **File**: `13_ADW_mentor_workflow.md`
- **Role**: WHAT to do, WHEN to do it
- **Phases**: 6-phase execution flow

### Layer 2: HOP (Execution)
- **Purpose**: Detailed domain-specific implementation
- **Files**: `09_HOP_orchestrator.md`, `10_HOP_processor.md`, `11_HOP_scout_navigator.md`
- **Role**: HOW to do it with examples and templates

### Integration Pattern
```
ADW Phase N
├── Objective (what)
├── HOP Implementation (how)
│   └── prompts/XX_HOP.md
├── Actions (detailed steps)
├── Input/Output contracts
├── Validation gates
└── Error handling
```

---

## 12 LEVERAGE POINTS IMPLEMENTATION

| # | Leverage Point | Implementation | Status |
|---|----------------|----------------|--------|
| 1 | Context | 01_QUICK_START.md + mental checklist | ✅ |
| 2 | Model | GPT-5/Claude Sonnet 4.5+ recommendations | ✅ |
| 3 | Prompt | TAC-7 format HOPs | ✅ |
| 4 | Tools | Per-mode tool definitions | ✅ |
| 5 | Standard Out | Task boundaries in execution_plans | ✅ |
| 6 | Types | JSON schemas (input/output) | ✅ |
| 7 | Documentation | PRIME + INSTRUCTIONS + README | ✅ |
| 8 | Tests | 5D validation + qa_patterns | ✅ |
| 9 | Architecture | This file + Dual-Layer | ✅ |
| 10 | Plans | 12_execution_plans.json | ✅ |
| 11 | Templates | Output templates in HOPs | ✅ |
| 12 | ADWs | 13_ADW_mentor_workflow.md | ✅ |

---

## FOLDER STRUCTURE

```
mentor_agent/
├── iso_vectorstore/          # Core agent knowledge (20 files)
│   ├── 01_QUICK_START.md     # LLM navigation (<8000 chars)
│   ├── 02_PRIME.md           # Identity, capabilities
│   ├── 03_INSTRUCTIONS.md    # Workflow rules
│   ├── 04_README.md          # User documentation
│   ├── 05_ARCHITECTURE.md    # This file
│   ├── 06_knowledge_map.json # Knowledge taxonomy
│   ├── 07_categorias.json    # 10 categories
│   ├── 08_language_guide.json# Seller language patterns
│   ├── 09_HOP_orchestrator.md# Main orchestration HOP
│   ├── 10_HOP_processor.md   # Knowledge processing HOP
│   ├── 11_HOP_scout_navigator.md # Discovery HOP
│   ├── 12_execution_plans.json   # Full/quick plans
│   ├── 13_ADW_mentor_workflow.md # 6-phase ADW
│   ├── 14-19_module.md       # Processing modules
│   └── 20_CHANGELOG.md       # Version history
│
├── RASCUNHO/                 # Input: raw files (seller drops here)
├── USER/                     # Input: seller's personal library
├── PROCESSADOS/              # Output: processed .md (FLAT, no subfolders)
│   └── catalogo.json         # Master index
├── FONTES/                   # External documentation
│   ├── LLM_PLATFORMS/
│   ├── MARKETPLACES/
│   ├── FRAMEWORKS/
│   └── ECOMMERCE/
│
├── prompts/                  # HOP prompt files
├── config/                   # Configuration files
├── src/                      # Python source code
├── scripts/                  # Automation scripts
└── workflows/                # ADW workflow files
```

---

## DATA FLOW

### Flow 1: Question Answering
```
Seller Question
    │
    ▼
[Scout Internal]
    │ Search catalogo.json
    │ Match: categoria + assunto + tags + aplicacao
    ▼
[Read Knowledge]
    │ Top 3-5 .md files from PROCESSADOS/
    ▼
[Synthesize]
    │ Extract WHEN/HOW/WHAT
    │ Translate to seller language
    ▼
[Respond]
    │ Practical answer + example + next step
    ▼
Seller Response
```

### Flow 2: File Processing
```
New File in RASCUNHO/
    │
    ▼
[Extract] ─────────── 14_module.md
    │ PDF/video/image → text
    ▼
[Classify] ────────── 15_module.md
    │ Detect categoria + assunto + nivel + tags
    ▼
[Synthesize] ──────── 17_module.md
    │ Create structured .md (800-1200 tokens)
    ▼
[Validate] ────────── 16_module.md
    │ 5D quality check (>0.75)
    ▼
[Catalog] ─────────── 19_module.md
    │ Save to PROCESSADOS/
    │ Update catalogo.json
    ▼
Processed Knowledge
```

### Flow 3: Lesson Building
```
"Me ensina sobre X"
    │
    ▼
[Search All]
    │ Find ALL related files (up to 5)
    ▼
[Read Multiple]
    │ Load all matches
    ▼
[Synthesize Lesson]
    │ Extract concepts
    │ Identify examples
    │ Build structure
    ▼
[Format]
    │ Apply lesson template
    │ Add emojis
    │ Include exercise
    ▼
Aula ao Vivo
```

---

## CATALOG STRUCTURE (catalogo.json)

```json
{
  "arquivos": [
    {
      "arquivo": "marketplace_titulos_seo_20251125.md",
      "categoria": "marketplace_optimization",
      "assunto": "titulos_seo",
      "tags": ["mercadolivre", "seo", "conversao"],
      "nivel": "intermediario",
      "aplicacao": "quando_criar_anuncios",
      "criado": "2025-11-25",
      "fonte_original": "RASCUNHO/guia_ml.pdf",
      "quality_score": 0.87
    }
  ],
  "categorias": [
    "marketplace_optimization",
    "copywriting",
    "estrategia_produto",
    "analise_concorrencia",
    "compliance_legal",
    "branding",
    "visual_design",
    "customer_experience",
    "operacoes_logistica",
    "financeiro_precificacao"
  ]
}
```

---

## QUALITY SYSTEM

### 5-Dimension Validation
| Dimension | Description | Weight | Threshold |
|-----------|-------------|--------|-----------|
| Completeness | All sections present | 20% | ≥0.60 |
| Clarity | No jargon, seller-friendly | 20% | ≥0.60 |
| Accuracy | Factual, Brazil-specific | 20% | ≥0.60 |
| Relevance | Useful for daily work | 20% | ≥0.60 |
| Actionability | Concrete steps | 20% | ≥0.60 |

**Overall Threshold**: ≥0.75 (75%)

### Quality Improvement Loop
```
Content → Validate → If <0.75 → Improve weak dimensions → Re-validate → Save
```

---

## INTEGRATION POINTS

### Internal (Other Agents)
- **Anuncio**: Delegate "cria anúncio" requests
- **Pesquisa**: Delegate market research
- **Marca**: Delegate brand strategy
- **CODEXA**: Meta-construction (builds this agent)

### External (FONTES/)
- **LLM_PLATFORMS**: Anthropic, OpenAI, Google, Cohere docs
- **MARKETPLACES**: ML, Shopee, Amazon, Magalu APIs
- **FRAMEWORKS**: LangChain, Vercel AI SDK, LlamaIndex
- **ECOMMERCE**: SEO, copywriting, CRO guides

---

## PERFORMANCE TARGETS

| Metric | Target | Current |
|--------|--------|---------|
| Processing Speed | <30s/file | ✅ |
| Quality Rate | >85% files ≥0.75 | 97.5% |
| Answer Latency | <3s | ✅ |
| Catalog Size | 100+ processed | 66,105 |
| Consolidation Ratio | High | 661:1 |

---

## ERROR HANDLING

### Catalog Not Found
- HALT: Check PROCESSADOS/catalogo.json exists
- Fallback: Create empty catalog, notify user

### Low Relevance Results
- WARN: Best match score < 0.60
- Action: Proceed with available, note partial answer

### Processing Failure
- RETRY: Try alternative extraction method
- FALLBACK: Ask user for copy-paste
- LOG: Record failure for improvement

---

## SECURITY RULES

1. **NO subfolders** in PROCESSADOS/ (flat structure only)
2. **NO generic names** (file1.md, temp.md prohibited)
3. **NO external URLs** without validation
4. **NO secrets** in processed files
5. **ALWAYS validate** before saving

---

**Version**: 2.5.0
**Framework**: 12 Leverage Points
**Architecture**: Dual-Layer (ADW + HOP)
**Status**: Production-Ready
