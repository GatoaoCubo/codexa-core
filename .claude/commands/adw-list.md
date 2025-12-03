# List Available ADW Workflows

Display all available ADW (Agentic Developer Workflow) workflows with their specifications.

## Output Format

```markdown
# 📋 Available ADW Workflows

## 1. PESQUISA_AGENT - Market Research
**File**: codexa.app/agentes/pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md
**Phases**: 9 phases (20-30min total)
**Output**: research_notes.md (22 blocks) + metadata.json + queries.json
**Architecture**: Dual-Layer (12 HOP prompts, ~260KB)

**Input Required**:
- Product name
- Category
- Target audience
- Price range (BRL)

**Quality Gates**:
- Quality score ≥0.75
- Completeness ≥75%
- Queries logged ≥15

**Usage**: `/prime pesquisa [product details]`

---

## 2. ANUNCIO_AGENT - Ad Generation
**File**: codexa.app/agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md
**Phases**: 7 phases (23-38min total)
**Output**: Trinity format (.md + .llm.json + .meta.json)
**Architecture**: Dual-Layer (10 HOP prompts, 466KB)

**Input Required**:
- Research notes path (from pesquisa_agent)

**Quality Gates**:
- Quality score ≥0.85
- Keyword density 0.70-0.80
- No compliance violations

**Usage**: `/prime anuncio [research_notes_path]`

---

## 3. MENTOR_AGENT - E-commerce Mentoring
**File**: codexa.app/agentes/mentor_agent/workflows/100_ADW_RUN_MENTOR.md
**Phases**: 6 phases (16-31min total)
**Output**: .md files (mentoring response)
**Architecture**: Dual-Layer (8 HOP prompts, ~100KB)

**Input Required**:
- Seller question/problem

**Quality Gates**:
- Quality score ≥0.87
- Skill gaps identified ≥2
- Resources provided ≥3

**Usage**: `/prime mentor [seller question]`

---

## 4. MARCA_AGENT - Brand Strategy
**File**: codexa.app/agentes/marca_agent/workflows/100_ADW_RUN_MARCA.md
**Phases**: 7 phases (21-36min total)
**Output**: brand_strategy.md (30+ blocks) + validation_report.txt
**Architecture**: Dual-Layer (2 HOP prompts, ~46KB)

**Input Required**:
- Business brief (mission, vision, values, product, audience)

**Quality Gates**:
- Brand consistency ≥0.85
- Values count: 3-5
- Positioning statement ≤2 sentences

**Usage**: `/prime marca [business brief]`

---

## 5. PHOTO_AGENT - AI Photography Prompts
**File**: codexa.app/agentes/photo_agent/workflows/100_ADW_RUN_PHOTO.md
**Phases**: 5 phases (15-30min total)
**Output**: Trinity format (grid 3x3: 9 individual + 1 batch)
**Architecture**: Dual-Layer (5 HOP prompts, ~110KB)

**Input Required**:
- Subject (product)
- Style (minimalist, lifestyle, etc.)

**Quality Gates**:
- Quality score ≥7.0/10
- All prompts ≥80 words
- 9 scenes validated

**Usage**: `/prime photo subject=[product], style=[style]`

---

## 6. CODEXA_AGENT - Integrated Product Reform (Orchestration)
**File**: codexa.app/agentes/codexa_agent/workflows/204_ADW_INTEGRATED_PRODUCT_REFORM.md
**Phases**: 5 phases (15min/product batch, 45-60min/product single)
**Output**: research_notes.md + Trinity format + Shopify sync + batch report
**Architecture**: Orchestration Layer (coordinates pesquisa + anuncio + sync)

**Input Required**:
- Supabase credentials (products list)
- Optional: --limit, --parallel, --product-ids

**Quality Gates**:
- QA score ≥0.85 per product
- 11 validation criteria
- Batch success ≥80%

**Usage**: `/reform-batch --limit 22 --parallel 3` or `/reform-product [name]`

**Orchestrates**:
- pesquisa_agent (Phase 2: research via Browser MCP)
- anuncio_agent (Phase 3: full_anuncio plan)
- sync_shopify (Phase 5: Edge Function)

---

## 📊 Summary Statistics

| Agent | Phases | Duration | HOP Prompts | Quality Threshold |
|-------|--------|----------|-------------|-------------------|
| pesquisa | 9 | 20-30min | 12 (~260KB) | ≥0.75 |
| anuncio | 7 | 23-38min | 10 (466KB) | ≥0.85 |
| mentor | 6 | 16-31min | 8 (~100KB) | ≥0.87 |
| marca | 7 | 21-36min | 2 (~46KB) | ≥0.85 |
| photo | 5 | 15-30min | 5 (~110KB) | ≥7.0/10 |
| **codexa (204)** | 5 | 15min/prod | Orchestration | ≥0.85 |

**Total**: 6 workflows, 39 phases, 37 HOP prompts + 1 orchestrator (~982KB knowledge base)

## Common Workflow Pattern

All workflows follow the same execution pattern:

1. **Load Context**: PRIME.md + ADW file + config files
2. **Execute Phases**: Sequential execution with validation gates
3. **Generate Output**: Agent-specific format (Trinity or custom)
4. **Report Results**: Duration, quality score, files saved, next steps

## Status

✅ All workflows are **PRODUCTION-READY** for conversational execution (Phase A)
📋 Python automation scripts (Phase B) are planned but not yet implemented

## Next Steps

Use `/prime {agent_name} [input]` to execute a specific workflow.
```
