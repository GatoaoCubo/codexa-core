# 100_ADW_RUN_PESQUISA | Complete Market Research Execution Workflow

**Purpose**: End-to-end Brazilian e-commerce market research (brief → research_notes.md)
**Type**: 9-Phase ADW (Agentic Developer Workflow) | **Duration**: 20-30 minutes
**Output**: research_notes.md (22 blocks) + metadata.json + queries.json
**Architecture**: Dual-Layer (ADW Orchestration ↔ HOP Execution)
**Status**: Production-Ready (Integrated with HOP prompts v2.0.0) | **Version**: 2.0.0

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "pesquisa_complete_research",
  "workflow_name": "Complete Market Research Execution",
  "agent": "pesquisa_agent",
  "version": "1.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4o / claude-sonnet-3.5+",

  "required_capabilities": {
    "web_search": true,
    "vision": false,
    "file_search": false,
    "code_interpreter": false
  },

  "phases": [
    {
      "phase_id": "phase_0_knowledge",
      "phase_name": "Knowledge Loading",
      "duration": "1-2min",
      "module": "PHASE_0_KNOWLEDGE_LOADING",
      "task_hint": "market_research"
    },
    {
      "phase_id": "phase_1_discovery",
      "phase_name": "Capability Discovery & Brief Validation",
      "duration": "2min",
      "prime_step": "Step 1",
      "description": "Auto-detect LLM capabilities + validate research brief"
    },
    {
      "phase_id": "phase_2_query_bank",
      "phase_name": "Query Bank Generation",
      "duration": "3min",
      "prime_step": "Step 2",
      "description": "Generate head terms, longtails, synonyms, variations"
    },
    {
      "phase_id": "phase_3_inbound_search",
      "phase_name": "Web Search INBOUND (Marketplaces)",
      "duration": "8min",
      "prime_step": "Step 3",
      "description": "Search 9 BR marketplaces + extract data"
    },
    {
      "phase_id": "phase_4_outbound_search",
      "phase_name": "Web Search OUTBOUND (SERP & Social)",
      "duration": "8min",
      "prime_step": "Step 4",
      "description": "Search Google, YouTube, TikTok, Instagram, Reclame Aqui"
    },
    {
      "phase_id": "phase_5_competitor_analysis",
      "phase_name": "Competitor Analysis & Benchmark",
      "duration": "6min",
      "prime_step": "Step 5",
      "description": "Analyze top 3-5 competitors + quantitative benchmark"
    },
    {
      "phase_id": "phase_6_seo_taxonomy",
      "phase_name": "SEO Taxonomy & Strategy",
      "duration": "4min",
      "prime_step": "Step 6",
      "description": "Consolidate SEO data (inbound/outbound) + categorize"
    },
    {
      "phase_id": "phase_7_compliance",
      "phase_name": "Compliance & Risk Analysis",
      "duration": "3min",
      "prime_step": "Step 7",
      "description": "Validate ANVISA, INMETRO, CONAR compliance"
    },
    {
      "phase_id": "phase_8_synthesis",
      "phase_name": "Synthesis & Insights",
      "duration": "3min",
      "prime_step": "Step 8",
      "description": "Generate actionable insights + prioritize opportunities"
    },
    {
      "phase_id": "phase_9_output",
      "phase_name": "Output Assembly & Validation",
      "duration": "2min",
      "prime_step": "Step 9",
      "description": "Assemble research_notes.md + metadata + queries + validate"
    }
  ]
}
```

---

## PREREQUISITES

**Before starting, ensure:**

1. **Context Loaded**:
   - Read `PRIME.md` (complete TAC-7 instructions)
   - Read `templates/research_notes.md` (22-block template)
   - Read `config/marketplaces.json` (9 BR marketplace data)

2. **Capabilities Available**:
   - `web_search`: REQUIRED (workflow will abort if not available)
   - `vision`: Optional (enables screenshot analysis)
   - `file_search`: Optional (enables compliance rules lookup)
   - `code_interpreter`: Optional (enables advanced metrics)

3. **User Input Ready**:
   - Research brief with minimum fields:
     - Product name (string)
     - Category (string)
     - Target audience (string)
     - Price range (string in BRL)
   - Optional: competitors, marketplace target, special requirements

---

## ARCHITECTURE: DUAL-LAYER INTEGRATION (ADW ↔ HOP)

This workflow implements a **Dual-Layer Architecture** where:

### **LAYER 1: ADW (Adaptive Dual-layer Workflow)**
- **Purpose**: High-level orchestration and coordination
- **This file**: Defines phases, sequencing, validation, error handling
- **Role**: "What to do" and "When to do it"

### **LAYER 2: HOP (Hyper-Optimized Prompts)**
- **Purpose**: Detailed execution and domain-specific implementation
- **Location**: `prompts/` directory (12 modular prompts, ~260KB total)
- **Role**: "How to do it" with comprehensive examples and templates

### **Integration Pattern:**

```
ADW Phase N
├── **Objective**: High-level goal
├── **HOP Implementation**: prompts/XX_name.md (size)
│   └── Detailed instructions, examples, templates
├── **Actions**: (implemented in HOP)
│   └── Summary of what HOP prompt does
├── **Input/Output**: Data contracts
├── **Validation**: Quality gates and thresholds
└── **Error Handling**: Specific failure strategies
```

### **Benefits of Dual-Layer:**
1. ✅ **Single Source of Truth**: Detailed logic lives in HOP prompts only
2. ✅ **Modularity**: HOP prompts can be updated independently
3. ✅ **Reusability**: HOP prompts can be used standalone or in other workflows
4. ✅ **Maintainability**: Changes in one place propagate naturally
5. ✅ **Testability**: HOP prompts can be tested individually

### **Execution Flow:**
```
User Input → ADW (Load Phase 1) → HOP XX (Execute) → Validate →
ADW (Load Phase 2) → HOP YY (Execute) → Validate → ... → Output
```

### **HOP Prompts Inventory:**
| Phase | HOP Prompt | Size | Purpose |
|-------|-----------|------|---------|
| 1 | `intake_validation.md` | 16KB | Brief validation & capability discovery |
| 2 | `main_agent_hop.md` | 31KB | Query bank generation (head terms, longtails, synonyms) |
| 3 | `web_search_inbound.md` | 13KB | Marketplace search execution (9 BR platforms) |
| 3 | `image_analysis.md` | 12KB | Screenshot analysis (optional, if vision available) |
| 4 | `web_search_outbound.md` | 15KB | SERP & social search (Google, YouTube, TikTok, Instagram) |
| 4 | `sentiment_analysis.md` | 14KB | Reclame Aqui & review sentiment analysis |
| 5 | `competitor_analysis.md` | 66KB | Deep competitor profiling & benchmarking |
| 5 | `price_comparison.md` | 12KB | Price range analysis across marketplaces |
| 6 | `seo_taxonomy.md` | 56KB | SEO keyword clustering & taxonomy creation |
| 7 | (no specific HOP) | - | Generic compliance validation |
| 8 | `gap_identification.md` | 4KB | Market opportunity gap analysis |
| 8 | `strategy_gaps.md` | 7.5KB | Strategic positioning gap analysis |
| 8 | `trend_analysis.md` | 3.7KB | Trend identification & forecasting |
| 9 | (no specific HOP) | - | ADW orchestration (Trinity output assembly) |

**Total HOP library**: 12 prompts, ~260KB of specialized market research knowledge

---

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `market_research`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

## PHASE 1: Capability Discovery & Brief Validation

**Objective**: Detect LLM capabilities + validate brief completeness

**HOP Implementation**: `prompts/intake_validation.md` (16KB)
- Comprehensive brief validation with field-by-field checks
- Capability auto-detection (web_search, vision, file_search, code_interpreter)
- Gap identification and assumption generation
- Confidence scoring (HIGH/MEDIUM/LOW based on data completeness)
- Execution: Load HOP prompt with `$brief` (user input) as context

**Actions** (implemented in HOP):
1. Auto-detect available capabilities:
   - Try `web_search` tool → REQUIRED (abort if not available)
   - Try `vision` tool → Optional (flag availability)
   - Try `file_search` tool → Optional (flag availability)
   - Try `code_interpreter` tool → Optional (flag availability)

2. Validate research brief:
   - Check required fields present (product, category, audience, price)
   - Identify missing fields (gaps)
   - Generate reasonable assumptions for missing data

3. Output `[LACUNAS DO BRIEF]` block:
   - List missing fields
   - List assumptions made
   - Flag confidence level (HIGH if all required present, MEDIUM if 1-2 missing, LOW if 3+ missing)

**Input**:
- `$brief` (user-provided research brief)

**Output**:
- `$capabilities` (detected: web_search, vision, file_search, code_interpreter)
- `$validated_brief` (brief with assumptions filled)
- `$brief_gaps` (list of missing fields)
- `$confidence_level` (HIGH/MEDIUM/LOW)

**Validation**:
- ✅ web_search available (REQUIRED - abort if false)
- ✅ Brief has product name
- ✅ Brief has category or can infer from product
- ✅ Brief has audience or can infer generic (25-45 anos)
- ✅ Brief has price range or can estimate from category

**Error Handling**:
- If web_search NOT available → ABORT with message: "web_search capability required. See SETUP.md for platform configuration."
- If <2 required fields → ABORT with message: "Insufficient brief data. Minimum: product + category OR product + price."

---

## PHASE 2: Query Bank Generation

**Objective**: Generate comprehensive keyword bank for searches

**HOP Implementation**: `prompts/main_agent_hop.md` (31KB)
- Head terms extraction (10-15 high commercial intent keywords)
- Longtail generation (30-50 phrases with attributes, benefits, context)
- Synonym mapping (regional variations, colloquial vs formal, brand vs generic)
- Query list creation (inbound: marketplace queries | outbound: SERP/social queries)
- Brazilian Portuguese optimization with regional variations
- Execution: Load HOP prompt with `$validated_brief` from Phase 1

**Actions** (implemented in HOP):
1. Extract **Head Terms** (10-15 terms):
   - 1-3 words, high commercial intent
   - Derived from product name + category
   - Brazilian Portuguese variations

2. Generate **Longtails** (30-50 phrases):
   - Head term + attribute (cor, tamanho, material)
   - Head term + benefit (economico, resistente, premium)
   - Head term + context (para academia, para trabalho, infantil)

3. Map **Synonyms and Variations**:
   - Regional variations (BR specific)
   - Colloquial vs formal terms
   - Brand vs generic terms

4. Create **Query Lists**:
   - Inbound queries: "{head term} + marketplace name"
   - Outbound queries: "{head term} + review/tutorial/comparacao"

**Input**:
- `$validated_brief` (from Phase 1)

**Output**:
- `$head_terms` (10-15 prioritized terms)
- `$longtails` (30-50 phrases)
- `$synonyms` (variations map)
- `$inbound_queries` (marketplace search list)
- `$outbound_queries` (SERP/social search list)

**Validation**:
- ✅ ≥10 head terms generated
- ✅ ≥30 longtails generated
- ✅ ≥5 synonyms/variations mapped
- ✅ Queries in Brazilian Portuguese

**Output to research_notes.md**:
- `[HEAD TERMS PRIORITÁRIOS]` - 10-15 terms
- `[LONGTAILS]` - 30-50 phrases
- `[SINÔNIMOS E VARIAÇÕES]` - Variations table

---

## PHASE 3: Web Search INBOUND (Marketplaces)

**Objective**: Search Brazilian marketplaces + extract competitive data

**HOP Implementation**:
- `prompts/web_search_inbound.md` (13KB) - Marketplace search execution (9 BR platforms)
- `prompts/image_analysis.md` (12KB) - Screenshot analysis (optional, if vision capability available)
- Combined execution: web_search_inbound runs marketplace queries → image_analysis processes screenshots if vision enabled
- Execution: Load HOP prompts sequentially with `$head_terms` and `$inbound_queries` from Phase 2

**Actions** (implemented in HOP):
1. **Execute marketplace searches** (9 BR marketplaces):
   - Mercado Livre (priority 1)
   - Shopee (priority 2)
   - Magazine Luiza (priority 3)
   - Amazon BR (priority 4)
   - Americanas, Casas Bahia, Submarino, TikTok Shop, Shein

2. **For each head term** (top 10):
   - Search ≥3 marketplaces
   - Extract: product titles, prices, ratings, review counts, badges, shipping
   - Screenshot top 3-5 listings (if vision available)

3. **Log all queries**:
   - Date, source (marketplace), search term, URL, key insight
   - Store in `$query_log` for output

4. **Extract patterns**:
   - Common title structures
   - Price ranges (min/avg/max)
   - Most used attributes (cores, tamanhos, materiais)
   - Persuasion patterns (frete gratis, desconto, garantia)

**Input**:
- `$head_terms` (from Phase 2)
- `$inbound_queries` (from Phase 2)
- `$capabilities.web_search` (REQUIRED)
- `$capabilities.vision` (optional)

**Output**:
- `$marketplace_data` (extracted listings data)
- `$price_ranges` (min/avg/max per marketplace)
- `$title_patterns` (common structures)
- `$query_log` (append marketplace queries)

**Validation**:
- ✅ ≥3 marketplaces searched per head term (top 10 terms)
- ✅ ≥30 total marketplace queries logged
- ✅ Price data extracted (BRL format)
- ✅ All queries logged with URL

**Output to research_notes.md**:
- `[SEO INBOUND]` - Marketplace keyword patterns
- `[PADRÕES DE LINGUAGEM EFICAZ]` - Title structures, messaging
- `[CONSULTAS WEB]` - First batch of logged queries

---

## PHASE 4: Web Search OUTBOUND (SERP & Social)

**Objective**: Search organic channels + extract audience insights

**HOP Implementation**:
- `prompts/web_search_outbound.md` (15KB) - SERP & social search (Google, YouTube, TikTok, Instagram)
- `prompts/sentiment_analysis.md` (14KB) - Reclame Aqui & review sentiment analysis
- Combined execution: web_search_outbound runs organic queries → sentiment_analysis processes complaint & review data
- Execution: Load HOP prompts with `$outbound_queries` from Phase 2

**Actions** (implemented in HOP):
1. **Google SERP** (5-10 queries):
   - "{product} review"
   - "{product} comparacao"
   - "{product} vale a pena"
   - Extract: blog posts, comparison articles, review sites

2. **YouTube** (3-5 queries):
   - "{product} review"
   - "{product} unboxing"
   - "{product} tutorial"
   - Extract: video titles, comments, pain points mentioned

3. **TikTok** (3-5 queries):
   - "{product} demo"
   - "#{product}"
   - Extract: trends, user content themes

4. **Instagram** (2-3 queries):
   - "#{product}"
   - Visual trends, influencer content

5. **Reclame Aqui** (REQUIRED):
   - Search top 3 competitor brands
   - Extract: complaints, risk patterns, sentiment

**Extract from all sources**:
- **Dores** (pain points) - problems customers mention
- **Ganhos** (desired gains) - benefits customers seek
- **Objeções** (objections) - doubts, FAQs, hesitations
- **Provas** (social proof) - testimonials, ratings, reviews

**Input**:
- `$head_terms` (from Phase 2)
- `$outbound_queries` (from Phase 2)
- `$capabilities.web_search` (REQUIRED)

**Output**:
- `$serp_data` (organic content insights)
- `$social_data` (social media trends)
- `$pain_points` (customer problems)
- `$desired_gains` (customer benefits)
- `$objections` (doubts/FAQs)
- `$social_proof` (testimonials/evidence)
- `$query_log` (append outbound queries)

**Validation**:
- ✅ ≥15 outbound queries logged (SERP + social)
- ✅ Reclame Aqui checked (REQUIRED)
- ✅ ≥5 pain points extracted
- ✅ ≥5 desired gains extracted
- ✅ All queries logged with URL

**Output to research_notes.md**:
- `[SEO OUTBOUND]` - Organic content keywords
- `[DORES DO PÚBLICO]` - Pain points
- `[GANHOS DESEJADOS]` - Desired gains
- `[OBJEÇÕES E RESPOSTAS]` - Objections + responses
- `[PROVAS E EVIDÊNCIAS]` - Social proof
- `[CONSULTAS WEB]` - Append outbound queries

---

## PHASE 5: Competitor Analysis & Benchmark

**Objective**: Deep dive on top competitors + quantitative benchmark

**HOP Implementation**:
- `prompts/competitor_analysis.md` (66KB) - Deep competitor profiling & quantitative benchmarking
- `prompts/price_comparison.md` (12KB) - Price range analysis across marketplaces
- Combined execution: competitor_analysis performs individual profiling → price_comparison aggregates pricing data
- Execution: Load HOP prompts with `$marketplace_data` and `$serp_data` from Phases 3-4

**Actions** (implemented in HOP):
1. **Identify top 3-5 competitors**:
   - From marketplace searches (Phase 3)
   - From user brief (if provided)
   - From organic searches (Phase 4)

2. **Individual competitor analysis**:
   - Product name + brand
   - Price (BRL)
   - Rating (X.X/5.0)
   - Review count (#)
   - Key differentiators (features, claims)
   - Positioning (premium, economic, mid-range)
   - Messaging patterns (tone, persuasion)
   - Shipping options (free, paid, speed)

3. **Aggregated benchmark**:
   - Avg price (BRL)
   - Avg rating (X.X/5.0)
   - Avg reviews (#)
   - Free shipping prevalence (%)
   - Top claimed features (frequency count)

4. **Gap identification**:
   - Underserved features (mentioned in reviews but not offered)
   - Weak messaging (opportunities for differentiation)
   - Price gaps (sweet spots)

**Input**:
- `$marketplace_data` (from Phase 3)
- `$serp_data` (from Phase 4)
- `$validated_brief` (from Phase 1)

**Output**:
- `$competitors` (3-5 individual profiles)
- `$benchmark` (aggregated quantitative table)
- `$competitive_gaps` (market opportunities)
- `$differentiators` (positioning suggestions)

**Validation**:
- ✅ ≥3 competitors analyzed
- ✅ All prices in BRL
- ✅ Quantitative metrics (not just qualitative)
- ✅ Benchmark table complete

**Output to research_notes.md**:
- `[ANÁLISE DE CONCORRENTES]` - Individual profiles
- `[BENCHMARK AGREGADO]` - Quantitative table
- `[GAPS COMPETITIVOS]` - Market opportunities
- `[DIFERENCIAIS COMPETITIVOS]` - Positioning suggestions

---

## PHASE 6: SEO Taxonomy & Strategy

**Objective**: Consolidate SEO data + categorize keywords

**HOP Implementation**: `prompts/seo_taxonomy.md` (56KB)
- Semantic keyword clustering (grouping related terms)
- Inbound vs outbound separation (marketplace-specific vs organic content keywords)
- Negative keyword mapping (competitors, wrong categories, negative associations)
- Taxonomy creation (primary/secondary categories, attributes, benefits)
- Brazilian Portuguese SEO optimization
- Execution: Load HOP prompt with `$head_terms`, `$longtails`, `$marketplace_data`, and `$serp_data` from Phases 2-4

**Actions** (implemented in HOP):
1. **Cluster keywords semantically**:
   - Group related terms (head terms + longtails)
   - Identify category positioning terms
   - Separate branded vs generic

2. **Separate inbound vs outbound**:
   - Inbound: marketplace-specific keywords
   - Outbound: organic content keywords (blogs, videos)

3. **Map negative keywords**:
   - Terms to avoid (competitors, wrong category, negative associations)

4. **Create taxonomy**:
   - Primary category
   - Secondary categories
   - Attributes (cor, tamanho, material)
   - Benefits (economico, premium, resistente)

**Input**:
- `$head_terms` (from Phase 2)
- `$longtails` (from Phase 2)
- `$marketplace_data` (from Phase 3)
- `$serp_data` (from Phase 4)

**Output**:
- `$seo_inbound` (marketplace keywords consolidated)
- `$seo_outbound` (organic keywords consolidated)
- `$taxonomy` (category structure)
- `$negative_keywords` (terms to avoid)

**Validation**:
- ✅ ≥20 inbound keywords categorized
- ✅ ≥20 outbound keywords categorized
- ✅ Taxonomy has primary + secondary categories
- ✅ ≥5 negative keywords identified

**Output to research_notes.md**:
- `[SEO INBOUND]` - Marketplace keywords (finalized)
- `[SEO OUTBOUND]` - Organic keywords (finalized)
- `[TERMO CONTEXTUAL E OCASIÃO]` - Context/usage keywords

---

## PHASE 7: Compliance & Risk Analysis

**Objective**: Validate regulatory compliance + identify risks

**HOP Implementation**: (no specific HOP - generic validation)
- This phase uses generic compliance validation logic (not extracted to separate HOP)
- Future optimization: Create `prompts/compliance_validator.md` for Brazilian regulatory checks (ANVISA, INMETRO, ANATEL, CONAR)
- Current execution: ADW-level validation using `config/marketplaces.json` and optional `file_search` or `web_search` capabilities

**Actions**:
1. **Compliance validation** (if `file_search` available):
   - ANVISA: health, cosmetics, supplements
   - INMETRO: toys, electronics, textiles
   - ANATEL: telecom, wireless devices
   - CONAR: advertising claims, ethical rules

2. **Fallback** (if `file_search` NOT available):
   - Use web_search for public compliance guidelines
   - Flag high-risk categories (saúde, infantil, eletrônicos)

3. **Extract risks**:
   - Prohibited claims (sem comprovação, termos regulados)
   - Required certifications (registro ANVISA, selo INMETRO)
   - Market risks (competitor dominance, price wars, negative reviews)

4. **Critical marketplace rules**:
   - Title restrictions (character limits, prohibited words)
   - Image requirements (backgrounds, watermarks)
   - Category-specific policies

**Input**:
- `$validated_brief` (from Phase 1)
- `$capabilities.file_search` (optional)
- `$capabilities.web_search` (fallback)
- `config/marketplaces.json` (marketplace policies)

**Output**:
- `$compliance_flags` (regulatory issues)
- `$required_certifications` (ANVISA, INMETRO, etc.)
- `$market_risks` (competition, reviews, pricing)
- `$marketplace_rules` (platform-specific restrictions)

**Validation**:
- ✅ High-risk categories flagged (saúde, infantil, eletrônicos)
- ✅ Required certifications identified (if applicable)
- ✅ Marketplace rules checked for top 3 platforms

**Output to research_notes.md**:
- `[RISCOS E ALERTAS]` - Compliance + market risks
- `[REGRAS CRÍTICAS DE MARKETPLACE]` - Platform restrictions

---

## PHASE 8: Synthesis & Insights

**Objective**: Consolidate findings + generate actionable insights

**HOP Implementation**:
- `prompts/gap_identification.md` (4KB) - Market opportunity gap analysis
- `prompts/strategy_gaps.md` (7.5KB) - Strategic positioning gap analysis
- `prompts/trend_analysis.md` (3.7KB) - Trend identification & forecasting
- Combined execution: Load all 3 HOP prompts with consolidated data from Phases 1-7 → synthesize into prioritized opportunities
- Execution: gap_identification finds underserved features → strategy_gaps finds positioning opportunities → trend_analysis forecasts market direction

**Actions** (implemented in HOP):
1. **Consolidate all phases**:
   - Review all extracted data
   - Identify patterns across marketplaces, SERP, social
   - Cross-reference competitor data with audience insights

2. **Prioritize opportunities**:
   - High impact, low complexity → Priority 1
   - High impact, high complexity → Priority 2
   - Low impact, low complexity → Priority 3
   - Low impact, high complexity → Deprioritize

3. **Create initial copy decisions**:
   - Recommended tone (formal, casual, technical)
   - Key messaging (benefits to emphasize)
   - Proof points (testimonials, data, certifications)
   - Mental triggers (scarcity, social proof, authority)

4. **Calculate confidence scores** per block:
   - 1.0 = Complete data, multiple sources
   - 0.75 = Good data, some gaps
   - 0.5 = Limited data, assumptions made
   - 0.25 = Insufficient data, high uncertainty

**Input**:
- All outputs from Phases 1-7

**Output**:
- `$opportunities` (prioritized action items)
- `$copy_decisions` (tone, messaging, proofs)
- `$mental_triggers` (persuasion strategies)
- `$confidence_scores` (per research block)
- `$executive_summary` (3-5 sentence overview)

**Validation**:
- ✅ ≥5 opportunities identified
- ✅ Opportunities prioritized (high/medium/low impact)
- ✅ Copy decisions include tone + messaging + proofs
- ✅ Confidence scores calculated for all 22 blocks

**Output to research_notes.md**:
- `[OPORTUNIDADES ACIONÁVEIS]` - Prioritized opportunities
- `[ARGUMENTOS DE VENDA]` - Proof points
- `[GATILHOS MENTAIS]` - Mental triggers
- `[DECISÕES DE COPY INICIAIS]` - Tone/messaging recommendations
- `[RESUMO EXECUTIVO]` - Executive summary

---

## PHASE 9: Output Assembly & Validation

**Objective**: Assemble all outputs + validate quality

**HOP Implementation**: (no specific HOP - ADW orchestration)
- This phase performs ADW-level orchestration (Trinity output assembly)
- Uses outputs from all previous HOP prompts (Phases 1-8)
- Future optimization: Create `prompts/trinity_assembler.md` for standardized .md + .llm.json + .meta.json generation
- Current execution: ADW orchestrates template filling using `templates/research_notes.md`

**Actions**:
1. **Assemble research_notes.md**:
   - Fill all 22 blocks using `templates/research_notes.md`
   - Ensure Markdown formatting
   - Include examples, quotes, data points

2. **Generate metadata.json**:
   ```json
   {
     "product": "{product_name}",
     "category": "{category}",
     "execution_date": "{ISO 8601 date}",
     "duration_minutes": {actual_duration},
     "quality_score": {overall_score},
     "completeness": {filled_blocks / 22 * 100},
     "confidence_score": {avg_confidence},
     "capabilities_used": {
       "web_search": true/false,
       "vision": true/false,
       "file_search": true/false,
       "code_interpreter": true/false
     },
     "stats": {
       "competitors_analyzed": {count},
       "queries_logged": {count},
       "marketplaces_searched": {count}
     }
   }
   ```

3. **Generate queries.json**:
   ```json
   {
     "total_queries": {count},
     "queries": [
       {
         "id": 1,
         "date": "{ISO 8601}",
         "source": "Mercado Livre / YouTube / Google / etc.",
         "query": "{search term}",
         "url": "{result URL}",
         "insight": "{key finding}"
       }
     ]
   }
   ```

4. **Quality validation**:
   ```python
   completeness = (filled_blocks / 22) * 100  # Target: ≥75%
   suggestions_ratio = suggestion_count / total_fields  # Target: ≤10%
   confidence_score = avg(block_confidence_scores)  # Target: ≥0.75
   quality_score = (completeness * 0.4 + (1 - suggestions_ratio) * 0.3 + confidence_score * 0.3)
   ```

5. **Save outputs**:
   - `user_research/{product_name}_research_notes.md`
   - `user_research/{product_name}_metadata.json`
   - `user_research/{product_name}_queries.json`

**Input**:
- All outputs from Phases 1-8
- `templates/research_notes.md` (22-block template)

**Output**:
- `research_notes.md` (22 blocks, human-readable)
- `metadata.json` (execution metadata)
- `queries.json` (all queries traced)

**Validation**:
- ✅ All 22 blocks present
- ✅ ≥3 competitors analyzed
- ✅ ≥15 queries logged with URLs
- ✅ Completeness ≥75%
- ✅ Suggestions ratio ≤10%
- ✅ Confidence score ≥0.75
- ✅ Files saved to user_research/

**Quality Gates**:
- If quality_score < 0.75 → Flag as LOW CONFIDENCE, suggest re-run with more detailed brief
- If competitors_analyzed < 3 → Flag WARNING, extend search
- If queries_logged < 15 → Flag WARNING, extend channel coverage
- If suggestions_ratio > 10% → Flag WARNING, niche product or limited data

---

## EXECUTION INSTRUCTIONS

### For AI Assistants (Conversational Mode)

**Step 1: Load Context**
```
Read the following files in order:
1. pesquisa_agent/PRIME.md (complete instructions)
2. pesquisa_agent/templates/research_notes.md (output template)
3. pesquisa_agent/config/marketplaces.json (marketplace data)
4. This file (100_ADW_RUN_PESQUISA.md) for workflow steps
```

**Step 2: Obtain User Brief**
```
Ask user for research brief with minimum fields:
- Product name
- Category
- Target audience
- Price range (BRL)

Optional:
- Marketplace target (default: all 9 BR)
- Known competitors
- Special requirements
```

**Step 3: Execute Workflow**
```
Follow phases 1-9 sequentially:
- Announce phase start: "Starting Phase X: {phase_name}"
- Execute phase actions as detailed above
- Validate phase outputs
- If validation fails → report error + suggest fix
- Announce phase completion: "Phase X complete. Moving to Phase Y."
```

**Step 4: Report Completion**
```
Upon completion, report:
- Duration: {actual_minutes} minutes
- Quality score: {score}/1.0
- Completeness: {percentage}%
- Files saved: user_research/{product}_*
- Next step: Review research_notes.md or pass to anuncio_agent
```

### For Python Automation (Future - Phase B)

**Script location**: `pesquisa_agent/workflows/run_pesquisa_agent.py`

**Usage**:
```bash
python run_pesquisa_agent.py \
  --brief "Product: X, Category: Y, Audience: Z, Price: R$ A-B" \
  --output user_research/ \
  --model gpt-4o

# Or with JSON brief:
python run_pesquisa_agent.py \
  --brief-file my_brief.json \
  --output user_research/
```

**Note**: Python automation script to be implemented in Phase B (after ADW pattern validated).

---

## SUCCESS CRITERIA

### Workflow Level
- ✅ All 9 phases completed without errors
- ✅ Duration ≤35 minutes (target: 20-30 min)
- ✅ No phase validation failures

### Output Level
- ✅ research_notes.md has all 22 blocks filled
- ✅ metadata.json generated with valid structure
- ✅ queries.json has ≥15 logged queries
- ✅ Quality score ≥0.75/1.0
- ✅ Completeness ≥75%
- ✅ Confidence score ≥0.75
- ✅ ≥3 competitors analyzed
- ✅ Suggestions ratio ≤10%

### Quality Level
- ✅ All prices in BRL format (R$ X,XX)
- ✅ All URLs logged with queries
- ✅ Reclame Aqui checked (risk analysis)
- ✅ Marketplace rules validated for top 3 platforms
- ✅ SEO keywords categorized (inbound/outbound)

---

## TROUBLESHOOTING

### Phase 1 Issues
**Error**: "web_search not available"
→ **Solution**: Check LLM platform configuration. See SETUP.md for web_search enablement.

**Warning**: "Brief missing 3+ required fields"
→ **Solution**: Ask user for more information or make reasonable assumptions (flag as LOW CONFIDENCE).

### Phase 3-4 Issues
**Warning**: "Queries logged < 15"
→ **Solution**: Extend search to more channels or marketplaces.

**Error**: "No marketplace results found"
→ **Solution**: Verify head terms are Brazilian Portuguese, try broader search terms.

### Phase 5 Issues
**Warning**: "Competitors analyzed < 3"
→ **Solution**: Broaden competitor definition, include adjacent product categories.

### Phase 9 Issues
**Error**: "Quality score < 0.75"
→ **Solution**: Review lowest confidence blocks, re-execute weak phases with more detailed searches.

**Warning**: "Suggestions ratio > 10%"
→ **Solution**: Niche product or limited data - flag in executive summary, suggest manual supplementation.

---

## RELATED FILES

**Core Documentation**:
- `PRIME.md` - Complete TAC-7 instructions (entry point)
- `README.md` - Agent structure and navigation
- `SETUP.md` - Platform-specific setup guides
- `INSTRUCTIONS.md` - Operational instructions

**Templates**:
- `templates/research_notes.md` - 22-block output template

**Configuration**:
- `config/agent.json` - Agent configuration
- `config/marketplaces.json` - 9 BR marketplaces database
- `config/plans/standard_research.json` - Default execution plan

**Output Directory**:
- `user_research/` - All research outputs saved here

---

## VERSION HISTORY

**v2.0.0** (2025-11-17):
- **Integrated with HOP prompts** (Dual-Layer Architecture)
- Added "ARCHITECTURE: DUAL-LAYER INTEGRATION" section
- Added "HOP Implementation" subsection to all 9 phases
- Each phase now explicitly references its HOP prompt(s)
- Added HOP Prompts Inventory table (12 prompts, ~260KB total)
- Updated status: "Production-Ready" → "Dual-Layer Integrated"
- Pattern based on anuncio_agent POC (commit 5c5ceeb01)

**v1.0.0** (2025-11-17):
- Initial ADW creation
- 9-phase workflow (mapped from PRIME.md Steps 1-9)
- Complete validation gates
- Quality scoring system
- Conversational execution mode
- Python automation stub (Phase B prep)

---

## NEXT STEPS

**Immediate** (Phase A):
1. Test this ADW with sample brief
2. Validate outputs against quality gates
3. Document any issues or improvements

**Phase B** (Python Automation):
1. Create `run_pesquisa_agent.py` script
2. Implement LLM API integration (Anthropic/OpenAI)
3. Add CLI arguments for brief input
4. Add batch processing mode
5. Add CI/CD integration hooks

**Replication** (Other Agents):
1. Use this ADW as template for other agents:
   - anuncio_agent → Ad copy generation workflow
   - marca_agent → Brand strategy workflow
   - mentor_agent → Mentoring workflow
   - photo_agent → Photo generation workflow
2. Follow same structure: phases, validation, quality gates
3. Document agent-specific adaptations

---

## METADATA

**Created**: 2025-11-17
**Updated**: 2025-11-17 (Integrated with HOP prompts)
**Generator**: CODEXA ADW Intelligent Constructor v1.0.0
**Agent**: pesquisa_agent v2.0.0
**Domain**: Market Research (Brazilian e-commerce)
**Phases**: 9
**Architecture**: Dual-Layer (ADW ↔ HOP)
**HOP Prompts**: 12 modular prompts (~260KB total)
**Auto-generated**: True (reviewed, validated, and enhanced with HOP integration)

---

**Status**: Production-Ready (Dual-Layer Integrated)
**Maintainer**: CODEXA Meta-Constructor
**Version**: 2.0.0 (ADW + HOP Integration)
**Contact**: See agentes/README.md for system navigation
**License**: Internal use only (EcomLM Codexa system)
