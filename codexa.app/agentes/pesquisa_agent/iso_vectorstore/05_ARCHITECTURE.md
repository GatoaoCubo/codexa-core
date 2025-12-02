# ARCHITECTURE | pesquisa_agent v3.0.0

**Purpose**: Technical architecture and capability detection
**Version**: 3.0.0 | **Updated**: 2025-11-30 | **Framework**: 12 Leverage Points

---

## 🏗️ SYSTEM ARCHITECTURE

### Dual-Layer Design (ADW + HOP)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
│  12_ADW_workflow.md (9-phase pipeline)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Phase 1 → Phase 2 → ... → Phase 9 → Trinity Output      │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION LAYER                              │
│  HOPs (Higher-Order Prompts) - TAC-7 Format                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 10_HOP_main │  │11_HOP_comp  │  │ prompts/*   │             │
│  │ Orchestrator│  │ Competitor  │  │ Modules     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                   │
│  Schemas + Configs + Templates                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │06_agent   │  │07_brief   │  │08_exec    │  │09_market  │   │
│  │config.json│  │schema.json│  │plan.json  │  │places.json│   │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 CAPABILITY DETECTION

### Required Capabilities

| Capability | Status | Detection | Fallback |
|------------|--------|-----------|----------|
| **web_search** | REQUIRED | Auto-detect on first tool use | ABORT (cannot run) |
| **vision** | Optional | Auto-detect | text_only mode |
| **file_search** | Optional | Auto-detect | web_search fallback |
| **code_interpreter** | Optional | Auto-detect | manual_calculation |

### Auto-Detection Flow

```
[STARTUP]
    │
    ▼
┌─────────────────────────────┐
│ Try web_search tool         │
│ ├─ Success → web_search=true│
│ └─ Fail → ABORT (required)  │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ Try vision tool             │
│ ├─ Success → vision=true    │
│ └─ Fail → vision=false      │
│           (continue)        │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ Try file_search tool        │
│ ├─ Success → file_search=true│
│ └─ Fail → file_search=false │
│           (use web fallback)│
└─────────────────────────────┘
    │
    ▼
[RESEARCH EXECUTION]
```

---

## 📂 ISO_VECTORSTORE STRUCTURE (20 Files)

### Navigation Index

| # | File | Purpose | Layer |
|---|------|---------|-------|
| 01 | QUICK_START.md | LLM entry point (<8000 chars) | Navigation |
| 02 | PRIME.md | Complete TAC-7 framework | Core |
| 03 | INSTRUCTIONS.md | Platform setup guide | Core |
| 04 | README.md | Agent overview | Core |
| 05 | ARCHITECTURE.md | This file - technical structure | Core |
| 06 | agent_config.json | Agent configuration | Data |
| 07 | brief_schema.json | Input validation schema | Data |
| 08 | execution_plan.json | Standard research plan | Data |
| 09 | marketplaces.json | 9 BR marketplaces + URLs | Data |
| 10 | HOP_main.md | Main orchestration HOP | Execution |
| 11 | HOP_competitor.md | Competitor analysis HOP | Execution |
| 12 | ADW_workflow.md | 9-phase workflow | Orchestration |
| 13 | marketplace_analysis.md | Marketplace search strategies | Knowledge |
| 14 | competitor_tracking.md | Benchmarking methodology | Knowledge |
| 15 | trend_analysis.md | Market trend identification | Knowledge |
| 16 | research_templates.md | Output templates (22-block) | Templates |
| 17 | output_formats.md | Trinity output specs | Templates |
| 18 | quality_gates.md | Validation rules | Tests |
| 19 | research_framework.md | Research methodology | Knowledge |
| 20 | CHANGELOG.md | Version history | Meta |

---

## 🔄 DATA FLOW

### Research Pipeline

```
User Brief (JSON/text)
    │
    ▼
┌─────────────────────────────────────┐
│ PHASE 1: Capability Discovery       │
│ - Detect: web_search, vision, etc.  │
│ - Validate brief                    │
│ - Output: $capabilities, $brief     │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ PHASE 2: Query Bank Generation      │
│ - Extract head terms (10-15)        │
│ - Generate longtails (30-50)        │
│ - Output: $head_terms, $longtails   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ PHASE 3-4: Web Search (IN/OUT)      │
│ - INBOUND: 9 BR marketplaces        │
│ - OUTBOUND: SERP, social, reviews   │
│ - Output: $marketplace_data         │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ PHASE 5: Competitor Analysis        │
│ - Top 3-5 competitor profiles       │
│ - Quantitative benchmark            │
│ - Output: $competitors, $benchmark  │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ PHASE 6-8: SEO + Compliance + Synth │
│ - Keyword clustering                │
│ - ANVISA/INMETRO/CONAR validation   │
│ - Actionable insights               │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ PHASE 9: Output Assembly            │
│ - Trinity Output:                   │
│   - research_notes.md (human)       │
│   - research_notes.llm.json (LLM)   │
│   - metadata.json (execution data)  │
└─────────────────────────────────────┘
```

---

## 🎯 INTEGRATION POINTS

### Upstream (Inputs)

| Source | Data | Format |
|--------|------|--------|
| User | Product brief | JSON/text |
| marca_agent | Brand guidelines | Optional |
| Historical | Previous research | Optional |

### Downstream (Outputs)

| Consumer | Data | Format |
|----------|------|--------|
| anuncio_agent | research_notes.md | 22-block MD |
| marca_agent | Market insights | JSON |
| user_research/ | All outputs | Trinity |

---

## 🔧 TASK BOUNDARIES

### Progress Communication Protocol

```
[TASK_START] Phase {N}: {Phase Name}
[PROGRESS] {Action description}... {status}
[TASK_END] Phase {N} complete → {summary}

[ERROR] {Error description} → {recovery action}
[WARNING] {Warning description} → {impact}
```

### Example Output

```
[TASK_START] Phase 3: Web Search INBOUND
[PROGRESS] Searching Mercado Livre for "fone bluetooth"... ✅
[PROGRESS] Searching Shopee for "fone bluetooth"... ✅
[PROGRESS] Searching Magazine Luiza for "fone bluetooth"... ✅
[PROGRESS] Extracted 15 competitor listings
[TASK_END] Phase 3 complete → 45 queries logged, 15 competitors found
```

---

## 📊 QUALITY METRICS

### Thresholds

| Metric | Threshold | Critical |
|--------|-----------|----------|
| Completeness | ≥75% | Yes |
| Confidence | ≥0.75 | Yes |
| Competitors | ≥3 | Yes |
| Queries logged | ≥15 | Yes |
| Suggestions ratio | ≤10% | Yes |
| All 22 blocks | 100% | Yes |

### Quality Score Formula

```python
quality_score = (
    completeness * 0.4 +
    (1 - suggestions_ratio) * 0.3 +
    confidence_score * 0.3
)
# Target: quality_score ≥ 0.75
```

---

## 🔗 PLATFORM COMPATIBILITY

| Platform | web_search | vision | file_search | code_interpreter |
|----------|------------|--------|-------------|------------------|
| Claude Code | ✅ WebFetch | ✅ Read | ❌ | ❌ |
| OpenAI API | ✅ Browsing | ✅ Vision | ✅ Vector | ✅ |
| ChatGPT GPT | ✅ Browsing | ✅ Vision | ✅ Knowledge | ✅ |
| Gemini | ✅ Grounding | ✅ Vision | ⚠️ Limited | ❌ |
| Local LLMs | ❌ External | ⚠️ Model | ❌ | ❌ |

**Legend**: ✅ Full | ⚠️ Partial | ❌ Not available

---

**Version**: 3.0.0 | **Updated**: 2025-11-30 | **Framework**: 12 Leverage Points
**Maintainer**: CODEXA Meta-Construction System
