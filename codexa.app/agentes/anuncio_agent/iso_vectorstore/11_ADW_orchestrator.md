<!-- iso_vectorstore -->
<!--
  Source: 100_ADW_RUN_ANUNCIO.md
  Agent: anuncio_agent
  Synced: 2025-11-30
  Version: 3.2.0
  Package: iso_vectorstore (export package)
-->

# 100_ADW_RUN_ANUNCIO | Anúncio Generation Agent Execution Workflow

**Purpose**: End-to-end execution workflow for anuncio_agent
**Type**: 7-Phase ADW | **Duration**: ~23-38min
**Output**: anuncio.json + anuncio.md, Trinity (.md + .llm.json + .meta.json) (trinity)
**Architecture**: Dual-Layer (ADW Orchestration ↔ HOP Execution)
**Status**: Production-Ready (Integrated with HOP prompts v3.2.0)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_run_anuncio",
  "workflow_name": "An\u00fancio Generation Agent Execution",
  "agent": "anuncio_agent",
  "version": "3.2.0",
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4+ or claude-sonnet-4+",
  "required_capabilities": {
    "multi-format output (.md + .json)": true,
    "compliance validation": true
  },
  "phases": [
    {
      "phase_id": "phase_1_input_validation",
      "phase_name": "Input Validation",
      "duration": "2-5min",
      "description": "Validate research notes and create strategic brief"
    },
    {
      "phase_id": "phase_2_title_generation",
      "phase_name": "Title Generation",
      "duration": "5-10min",
      "description": "Generate SEO-optimized titles with max keyword density"
    },
    {
      "phase_id": "phase_3_keywords_expansion",
      "phase_name": "Keywords Expansion",
      "duration": "3-7min",
      "description": "Expand keywords into semantic blocks"
    },
    {
      "phase_id": "phase_4_description_building",
      "phase_name": "Description Building",
      "duration": "5-10min",
      "description": "Create persuasive long-form descriptions"
    },
    {
      "phase_id": "phase_5_visual_assets",
      "phase_name": "Visual Assets",
      "duration": "3-7min",
      "description": "Generate image prompts and video scripts"
    },
    {
      "phase_id": "phase_6_qa_&_variants",
      "phase_name": "QA & Variants",
      "duration": "3-7min",
      "description": "Quality validation and A/B variant creation"
    },
    {
      "phase_id": "phase_7_output_assembly",
      "phase_name": "Output Assembly",
      "duration": "2-5min",
      "description": "Compile final output in required format"
    }
  ]
}
```

---

## PREREQUISITES

**Before starting, ensure:**

1. **Context Loaded**:
   - Read `PRIME.md` (agent instructions)
   - Read `README.md` (agent structure)
   - `config/copy_rules.json`
   - `config/marketplace_specs.json`
   - `config/persuasion_patterns.json`

2. **Capabilities Available**:
   - LLM: gpt-4+ or claude-sonnet-4+
   - Tools: multi-format output (.md + .json), compliance validation

3. **User Input Ready**:
   - Research notes from `USER_DOCS/produtos/research/`

---

## ARCHITECTURE: DUAL-LAYER INTEGRATION (ADW ↔ HOP)

This workflow implements a **Dual-Layer Architecture** where:

### **LAYER 1: ADW (Adaptive Dual-layer Workflow)**
- **Purpose**: High-level orchestration and coordination
- **This file**: Defines phases, sequencing, validation, error handling
- **Role**: "What to do" and "When to do it"

### **LAYER 2: HOP (Hyper-Optimized Prompts)**
- **Purpose**: Detailed execution and domain-specific implementation
- **Location**: `prompts/` directory (10 modular prompts, 466KB total)
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
User Input → ADW (Load Phase 1) → HOP 10 (Execute) → Validate →
ADW (Load Phase 2) → HOP 20 (Execute) → Validate → ... → Trinity Output
```

### **HOP Prompts Inventory:**
| Phase | HOP Prompt | Size | Purpose |
|-------|-----------|------|---------|
| 1 | `10_main_agent_hop.md` | 26KB | Context detection & validation |
| 2 | `20_titulo_generator.md` | 75KB | Title generation (marketplace-specific) |
| 3 | `30_keywords_expander.md` | 13KB | Semantic keyword expansion |
| 4 | `40_bullet_points.md` | 83KB | Benefit-focused bullet points |
| 4 | `50_descricao_builder.md` | 108KB | Full description templates |
| 5 | `60_image_prompts.md` | 46KB | AI image generation prompts |
| 5 | `70_video_script.md` | 40KB | Video storyboards |
| 6 | `85_variacoes_s5.md` | 15KB | A/B variant generation |
| 6 | `90_qa_validation.md` | 42KB | Quality validation |
| 7 | `80_seo_metadata.md` | 18KB | SEO metadata (optional) |

**Total HOP library**: 10 prompts, 466KB of specialized knowledge

---

## PHASE 1: Input Validation

**Objective**: Validate research notes, detect context (product type + marketplace), create strategic brief

**HOP Implementation**: `prompts/10_main_agent_hop.md` (26KB)
- This phase is fully implemented in the main agent HOP prompt
- The HOP prompt contains detailed instructions for context detection, validation, and strategic brief creation
- Execution: Load and execute the HOP prompt with user research notes as input

**Actions** (implemented in HOP):
1. **Read and parse input data**:
   - Load research notes from `USER_DOCS/produtos/research/[product_name]_research_notes.md`
   - Count blocks: [HEAD TERMS], [LONGTAILS], [DORES], [GANHOS], [OBJEÇÕES], [PROVAS], [CONCORRENTES]
   - Validate: Minimum 15 blocks required (quality threshold)

2. **Auto-detect product type** (determines keyword strategy):
   - B2B SaaS: Look for keywords "API", "platform", "framework", "developer", "integration", "LLM", "AI tool"
   - Physical Product: Look for "material", "dimensões", "peso", "cor", "tamanho", attributes
   - Service: Look for "consultoria", "atendimento", "processo", "garantia", service-related terms
   - Default: Physical Product (if ambiguous)

3. **Auto-detect marketplace type** (determines constraints):
   - GitHub: Keywords "repository", "open-source", "stars", "README", "developer tool"
   - Mercado Livre: Keywords "vendedor ML", "anúncio mercado livre", "categoria ML"
   - Shopee: Keywords "shopee", "vendedor shopee"
   - TikTok Shop: Keywords "tiktok", "short video"
   - Default: Mercado Livre (Brazilian e-commerce primary)

4. **Create strategic brief** with detected context:
   ```json
   {
     "product_name": "[extracted from research]",
     "product_type": "B2B_SAAS | PHYSICAL_PRODUCT | SERVICE",
     "marketplace_type": "GITHUB | MERCADO_LIVRE | SHOPEE | TIKTOK_SHOP",
     "target_audience": "[extracted from [PÚBLICO]]",
     "head_terms": "[top 10 from [HEAD TERMS]]",
     "main_differentiator": "[from [DIFERENCIAIS]]",
     "compliance_requirements": "[ANVISA, INMETRO, or NONE]",
     "quality_score": 0.0-1.0
   }
   ```

5. **Load context-specific config files**:
   - `config/marketplace_specs.json` → filter by detected marketplace
   - `config/copy_rules.json` → filter by product type
   - `config/persuasion_patterns.json` → filter by audience type

**Input**:
- `$user_research_notes` (research/[product]_research_notes.md)
- `$config_files` (marketplace_specs.json, copy_rules.json, persuasion_patterns.json)

**Output**:
- `$strategic_brief` (JSON with detected context + extracted data)
- `$quality_score` (0.0-1.0, based on research completeness)

**Validation**:
- ✅ Research blocks ≥15 (PASS) / 10-14 (WARN) / <10 (FAIL)
- ✅ Product type detected with confidence ≥0.6
- ✅ Marketplace type detected with confidence ≥0.6
- ✅ Quality score ≥0.70 (minimum threshold)
- ✅ Head terms count ≥8
- ✅ Competitors analyzed ≥3

**Error Handling**:
- If blocks <10 → HALT: "Research insufficient. Need minimum 10 blocks, found [X]. Missing: [list missing block types]"
- If product type confidence <0.6 → WARN: "Ambiguous product type detected. Defaulting to PHYSICAL_PRODUCT. Override with explicit flag if needed."
- If marketplace type confidence <0.6 → WARN: "Ambiguous marketplace detected. Defaulting to MERCADO_LIVRE."
- If quality_score <0.70 → FAIL: "Research quality below threshold. Score: [X]. Issues: [list incomplete sections]"

---
## PHASE 2: Title Generation

**Objective**: Generate SEO-optimized titles with max keyword density (context-aware per marketplace)

**HOP Implementation**: `prompts/20_titulo_generator.md` (75KB)
- Comprehensive title generation prompt with marketplace-specific templates
- Contains examples for GitHub, Mercado Livre, Shopee, TikTok Shop
- Includes validation rules, forbidden words, and compliance checks
- Execution: Load HOP prompt with `$strategic_brief` from Phase 1

**Actions** (implemented in HOP):

1. **Extract head terms** from `$strategic_brief.head_terms`:
   - Prioritize: Search volume (high→low) + Intent (transactional→informational)
   - Front-load strategy: Most valuable term FIRST (not buried mid-title)
   - Example: ✅ "AI Agent Framework E-commerce" ❌ "Framework for E-commerce AI Agents"

2. **Generate 3 title variations** based on `$strategic_brief.marketplace_type`:

   **IF marketplace_type == "GITHUB"**:
   - **Constraints**: 60-80 chars | 9-10 keywords min | ZERO connectors | Developer-focused
   - **Structure**: [HEAD_TERM] + [DIFFERENTIATOR] + [USE_CASE] + [TECH_STACK]
   - **Example (EcomLM)**:
     - ✅ "Meta-Construction AI Framework E-commerce LLM Specialization Brazilian Marketplaces Open-Source"
     - ✅ "E-commerce Brain LLM Agents Self-Building Meta-System Mercado Livre Shopee Automation"
     - ✅ "Agentic Framework E-commerce Vertical Specialization Isolated Agents Brazil-First Developer Tools"
   - **Forbidden**: Connectors ("de", "para", "com", "e", "the", "for", "with", "and")

   **IF marketplace_type == "MERCADO_LIVRE"**:
   - **Constraints**: 58-60 chars STRICT | Max density | Compliance (no superlatives without proof)
   - **Structure**: [PRODUCT] + [ATTRIBUTES] + [BENEFITS] + [DIFFERENTIATORS]
   - **Example (Physical Product - Headphone)**:
     - ✅ "Fone Bluetooth 5.3 ANC Cancelamento Ruído 40h Bateria IPX7"
     - ✅ "Headphone Gamer RGB LED Surround 7.1 Microfone Removível"
     - ❌ "Melhor fone Bluetooth do mercado" (superlative without proof = ML violation)
   - **Forbidden**: "melhor", "único", "revolucionário" (unless backed by [PROVAS])

   **IF marketplace_type == "SHOPEE"**:
   - **Constraints**: 60-80 chars | Emoji allowed (1-2 max) | Promo-friendly
   - **Structure**: [PRODUCT] + [PROMO_HOOK] + [ATTRIBUTES] + [BENEFITS]
   - **Example**:
     - ✅ "Fone Bluetooth ANC 🎧 Cancelamento Ruído Ativo 40h Bateria Entrega Rápida"
     - ✅ "Teclado Mecânico Gamer ⚡ RGB Switch Blue 60% Wireless Bluetooth"
   - **Forbidden**: Excessive emojis (≥3 = spammy), ALL CAPS words

   **IF marketplace_type == "TIKTOK_SHOP"**:
   - **Constraints**: 30-50 chars (short attention span) | Viral hooks | Emoji encouraged
   - **Structure**: [HOOK] + [PRODUCT] + [WOW_FACTOR]
   - **Example**:
     - ✅ "🔥 Fone ANC Silêncio Total 40h Bateria"
     - ✅ "😱 Teclado Gamer RGB Wireless Premium"
   - **Forbidden**: Long technical specs (TikTok = emotion > specs)

3. **Validate each title**:
   - **Char count**: Within marketplace range (STRICT for ML, flexible for GitHub/Shopee)
   - **Keyword count**: GitHub ≥9 | ML ≥7 | Shopee ≥6 | TikTok ≥4
   - **Keyword density**: (keywords / total_words) ≥ 0.70 (GitHub/ML), ≥0.60 (Shopee/TikTok)
   - **Forbidden words**: Check `config/marketplace_specs.json` blacklist
   - **Compliance**: ML superlatives must have `[PROVAS]` backing

4. **Rank variations** by:
   - Keyword density (primary)
   - Head term position (front-loaded = higher score)
   - Readability (avoid keyword stuffing that breaks grammar)
   - Marketplace compliance (ML strictest, TikTok most flexible)

**Input**:
- `$strategic_brief` (from Phase 1, contains head_terms + marketplace_type + product_type)
- `config/marketplace_specs.json` (char limits, forbidden words, compliance rules)

**Output**:
- `$title_variations` (array of 3 titles with scores)
  ```json
  [
    {
      "title": "...",
      "char_count": 72,
      "keyword_count": 9,
      "keyword_density": 0.75,
      "score": 0.92,
      "compliance_issues": []
    },
    ...
  ]
  ```

**Validation**:
- ✅ 3 variations generated
- ✅ ALL variations within char range (±2 chars tolerance for GitHub, STRICT for ML)
- ✅ Keyword density ≥0.70 (GitHub/ML) or ≥0.60 (Shopee/TikTok)
- ✅ ZERO forbidden words found
- ✅ Compliance check PASSED (ML superlatives backed by proof)
- ✅ At least 1 variation scores ≥0.85

**Error Handling**:
- If char_count out of range → RETRY: Regenerate with strict constraint reminder
- If keyword_count <minimum → RETRY: "Add more head terms, current: [X], need: [Y]"
- If forbidden_words detected → RETRY: "Remove: [list words]. Alternatives: [suggest replacements]"
- If compliance FAIL → HALT: "ML compliance violation: Superlative '[word]' needs proof from [PROVAS] section"
- If all variations score <0.80 → WARN: "Low quality titles. Consider: [specific improvement suggestions]"

**Examples (Bad vs Good)**:

**BAD (Generic, low density)**:
- ❌ "O melhor framework de IA para e-commerce do Brasil" (48 chars, 5 keywords, density=0.50, forbidden "melhor")
- ❌ "Framework que ajuda a construir agentes de IA" (47 chars, 4 keywords, density=0.40, too generic)

**GOOD (Specific, high density)**:
- ✅ "Meta-Construction AI Framework E-commerce LLM Specialization Brazilian Marketplaces" (80 chars, 9 keywords, density=0.75)
- ✅ "Agentic Framework E-commerce Vertical Isolated Agents Brazil-First Self-Building" (78 chars, 10 keywords, density=0.83)

---
## PHASE 3: Keywords Expansion

**Objective**: Expand keywords into semantic blocks (context-aware per product type + marketplace)

**HOP Implementation**: `prompts/30_keywords_expander.md` (13KB)
- Semantic keyword expansion with product-type specific strategies
- Generates 4 keyword blocks (A, B, C, D) with 10+ keywords each
- Includes coverage scoring and marketplace-specific modifiers
- Execution: Load HOP prompt with `$strategic_brief` + `$title_variations` from Phase 2

**Actions** (implemented in HOP):

1. **Load base keywords** from `$strategic_brief`:
   - Head terms (from research [HEAD TERMS])
   - Longtails (from research [LONGTAILS])
   - Synonyms (from research [SINÔNIMOS])

2. **Generate keyword blocks** based on `$strategic_brief.product_type`:

   **IF product_type == "B2B_SAAS"**:
   - **Block A: Technical Terms** (20-30 keywords):
     - Framework names, programming languages, integrations, APIs
     - Example (EcomLM): "meta-construction", "agentic framework", "LLM specialization", "multi-agent orchestration", "isolated agents", "Python framework", "Claude API", "OpenAI integration", "RAG system", "vector store", "HOP prompts", "TAC-7 format"

   - **Block B: Comparisons** (15-25 keywords):
     - "[Product] vs [Competitor]", "alternative to [X]", "better than [Y]"
     - Example: "LangChain alternative", "CrewAI vs EcomLM", "AutoGen comparison", "Shopify for AI", "meta-agents 2025", "self-building systems", "LLMOps tools"

   - **Block C: Use Cases** (20-30 keywords):
     - Industry-specific applications, user personas, problems solved
     - Example: "e-commerce automation", "Mercado Livre AI", "Shopee automation", "marketplace research", "ad copywriting AI", "brand strategy agent", "AI for online stores", "developer productivity"

   - **Block D: Features & Benefits** (15-20 keywords):
     - Specific capabilities, technical advantages, differentiators
     - Example: "zero dependencies", "portable agents", "one upload setup", "Brazilian marketplaces", "self-improving system", "meta-constructor", "quality gates", "compliance built-in"

   **IF product_type == "PHYSICAL_PRODUCT"**:
   - **Block A: Attributes** (20-30 keywords):
     - Material, color, size, weight, dimensions, technical specs
     - Example (Headphone): "Bluetooth 5.3", "ANC active noise canceling", "40h battery life", "IPX7 waterproof", "USB-C charging", "foldable design", "memory foam cushions", "50mm drivers", "20Hz-20kHz frequency"

   - **Block B: Benefits** (15-25 keywords):
     - User outcomes, pain points solved, value propositions
     - Example: "silêncio total", "conforto prolongado", "som imersivo", "graves potentes", "chamadas nítidas", "longa autonomia", "resistente água suor", "transporte fácil"

   - **Block C: Use Cases & Occasions** (15-20 keywords):
     - When/where/why to use, user scenarios
     - Example: "home office", "academia workout", "viagem avião", "gaming", "calls reuniões", "treino corrida", "podcast edição", "música alta qualidade"

   - **Block D: Compliance & Certifications** (10-15 keywords if applicable):
     - ANVISA, INMETRO, Anatel, FCC, CE, warranty terms
     - Example: "certificado Anatel", "1 ano garantia", "selo INMETRO", "homologado Brasil", "suporte técnico BR"

   **IF product_type == "SERVICE"**:
   - **Block A: Process & Methodology** (15-25 keywords):
     - How service is delivered, steps, framework used
     - Example (Consulting): "diagnóstico inicial", "análise competitiva", "estratégia customizada", "implementação guiada", "acompanhamento mensal", "relatórios detalhados"

   - **Block B: Benefits & Outcomes** (20-30 keywords):
     - Results, transformations, before/after states
     - Example: "aumento conversão", "redução custos", "automação processos", "escalabilidade negócio", "ROI positivo", "tempo economizado", "produtividade aumentada"

   - **Block C: Guarantees & Social Proof** (10-15 keywords):
     - Warranties, testimonials, certifications, case studies
     - Example: "garantia satisfação", "50+ clientes atendidos", "certificado Google Partners", "cases comprovados", "reembolso integral", "suporte ilimitado"

3. **Expand with marketplace-specific modifiers**:

   **IF marketplace_type == "GITHUB"**:
   - Add: "open-source", "MIT license", "Python", "CLI", "API", "documentation", "examples", "contributors", "stars", "fork"
   - Expand longtails: "[feature] tutorial", "how to [use case]", "[product] vs [competitor] comparison", "best practices [topic]"

   **IF marketplace_type == "MERCADO_LIVRE" | "SHOPEE" | "TIKTOK_SHOP"**:
   - Add: "entrega rápida", "frete grátis", "parcela sem juros", "garantia [X] dias", "envio imediato", "estoque Brasil"
   - Expand with regional terms: "BR", "brasileiro", "nacional", regional slang if applicable

4. **Validate semantic coherence**:
   - Each block should have ≥10 keywords
   - No duplicate keywords across blocks (unless intentional for emphasis)
   - Keywords align with product type (don't use "API integration" for physical products)
   - Total unique keywords: B2B SaaS ≥70 | Physical Product ≥60 | Service ≥50

5. **Calculate keyword coverage score**:
   - Head terms coverage: (head_terms_used / head_terms_available) ≥0.80
   - Longtail coverage: (longtails_used / longtails_available) ≥0.60
   - Synonym diversity: (unique_synonyms / total_keywords) ≥0.20

**Input**:
- `$strategic_brief` (head_terms, product_type, marketplace_type)
- `$title_variations` (from Phase 2, for keyword consistency)
- Research blocks: [HEAD TERMS], [LONGTAILS], [SINÔNIMOS], [TERMO CONTEXTUAL]

**Output**:
- `$keyword_blocks` (JSON with 4 blocks per product type)
  ```json
  {
    "block_a": {
      "name": "Technical Terms | Attributes | Process",
      "keywords": [...],
      "count": 25
    },
    "block_b": {...},
    "block_c": {...},
    "block_d": {...},
    "coverage_score": {
      "head_terms": 0.85,
      "longtails": 0.70,
      "synonym_diversity": 0.25,
      "total_unique_keywords": 82
    }
  }
  ```

**Validation**:
- ✅ 4 keyword blocks generated (A, B, C, D)
- ✅ Each block ≥10 keywords
- ✅ Total unique keywords meets minimum (B2B ≥70 | Physical ≥60 | Service ≥50)
- ✅ Head terms coverage ≥0.80
- ✅ Longtail coverage ≥0.60
- ✅ Synonym diversity ≥0.20
- ✅ No product-type mismatches (e.g., "API" in physical product keywords)
- ✅ Marketplace-specific modifiers present (if GitHub → "open-source" found, if ML/Shopee → "entrega rápida" found)

**Error Handling**:
- If block count <4 → RETRY: "Generate all 4 blocks. Missing: [list missing blocks]"
- If any block <10 keywords → RETRY: "Block [X] has only [Y] keywords. Need minimum 10. Expand with: [suggestions based on research]"
- If total_unique_keywords <minimum → RETRY: "Only [X] keywords generated. Need [Y] for [product_type]. Check research [LONGTAILS] and [SINÔNIMOS] for more."
- If head_terms_coverage <0.80 → WARN: "Low head terms usage ([X]%). Prioritize high-volume terms from research."
- If product_type mismatch detected → FAIL: "Keyword '[keyword]' incompatible with product_type '[type]'. Example: 'API integration' not valid for PHYSICAL_PRODUCT."

**Examples (Product Type Adaptations)**:

**B2B SaaS (EcomLM)**:
- Block A (Technical): "meta-construction", "LLM framework", "agentic system", "Python", "Claude API", "vector store", "RAG", "isolated agents"
- Block B (Comparisons): "LangChain alternative", "CrewAI vs EcomLM", "better than AutoGen", "Shopify for AI"
- Block C (Use Cases): "e-commerce automation", "Mercado Livre AI", "marketplace research", "ad copywriting"
- Block D (Features): "zero dependencies", "one upload", "self-improving", "Brazil-first"

**Physical Product (Headphone)**:
- Block A (Attributes): "Bluetooth 5.3", "ANC noise canceling", "40h battery", "IPX7 waterproof", "USB-C", "memory foam"
- Block B (Benefits): "silêncio total", "conforto prolongado", "som imersivo", "longa autonomia", "resistente água"
- Block C (Use Cases): "home office", "academia", "viagem", "gaming", "podcast", "corrida"
- Block D (Compliance): "certificado Anatel", "1 ano garantia", "selo INMETRO", "suporte BR"

**Service (E-commerce Consulting)**:
- Block A (Process): "diagnóstico inicial", "análise competitiva", "estratégia customizada", "implementação guiada"
- Block B (Benefits): "aumento conversão", "redução custos", "automação processos", "ROI positivo"
- Block C (Guarantees): "garantia satisfação", "50+ clientes", "cases comprovados", "reembolso integral"

---
## PHASE 4: Description Building

**Objective**: Create persuasive long-form descriptions (marketplace-specific templates + compliance)

**HOP Implementation**:
- `prompts/40_bullet_points.md` (83KB) - Benefit-focused bullet points generation
- `prompts/50_descricao_builder.md` (108KB) - Full description with marketplace templates
- Combined execution: Generate bullet points first, then weave into full description
- Execution: Load both HOP prompts sequentially with accumulated context

**Actions** (implemented in HOP):

1. **Select description template** based on `$strategic_brief.marketplace_type`:

   **IF marketplace_type == "GITHUB" (README.md format)**:
   - Structure: Hero → Features → Installation → Quick Start → Use Cases → Comparisons → Contributing → License
   - Word count: 800-1500 words
   - Tone: Technical, developer-focused, code examples included
   - Key sections:
     - **Hero** (2-3 sentences): Problem + Solution + Differentiator
     - **Features** (bullet list, 5-8 items): Technical capabilities with emojis optional
     - **Quick Start** (code block): pip install / usage example
     - **Comparisons** (table): vs LangChain, CrewAI, AutoGen (if applicable)
     - **Use Cases** (3-5 scenarios): Real-world applications
   - Example keywords to weave: "open-source", "self-hosted", "MIT license", "production-ready", "extensible"

   **IF marketplace_type == "MERCADO_LIVRE"**:
   - Structure: Hook → Benefits → Specs → Compliance → Garantia → CTA
   - Word count: 400-800 words (ML limits long descriptions)
   - Tone: Persuasive but factual (no exaggeration without proof)
   - Key sections:
     - **Hook** (1-2 sentences): Main benefit + social proof if available
     - **Benefits** (3-5 paragraphs): Each benefit with explanation
     - **Specs** (bullet list or table): Technical specifications
     - **Compliance** (if applicable): ANVISA, INMETRO, Anatel certifications
     - **Garantia** (1 paragraph): Warranty terms, return policy
     - **CTA** (1 sentence): "Aproveite" / "Garanta já" / etc.
   - Forbidden: Superlatives ("melhor", "único") without backing from [PROVAS]
   - Required: Include keywords from Phase 3 naturally (not stuffed)

   **IF marketplace_type == "SHOPEE"**:
   - Structure: Visual Hook → Promo → Benefits → Specs → Social Proof
   - Word count: 300-600 words (shorter attention span)
   - Tone: Casual, promo-friendly, emoji usage encouraged
   - Key sections:
     - **Visual Hook** (1 sentence + emoji): "🔥 Oferta Imperdível!"
     - **Promo** (1 paragraph): Discount, free shipping, installment terms
     - **Benefits** (3-4 short paragraphs): Quick, scannable
     - **Specs** (bullet list, emojis): "✅ Bluetooth 5.3 ✅ 40h Bateria"
     - **Social Proof** (1 sentence): "X clientes satisfeitos" / ratings
   - Example: Include "entrega rápida", "parcela sem juros", "garantia X dias"

   **IF marketplace_type == "TIKTOK_SHOP"**:
   - Structure: Viral Hook → Wow Factor → Simple Benefits → Easy CTA
   - Word count: 100-250 words (very short, video-first platform)
   - Tone: Exciting, FOMO-driven, simple language
   - Key sections:
     - **Viral Hook** (1 sentence): "😱 Você PRECISA ver isso!"
     - **Wow Factor** (1-2 sentences): Most impressive feature
     - **Simple Benefits** (3 bullets max): Easy to understand
     - **CTA** (1 sentence): "Compre agora antes de acabar!"
   - Emojis: Encouraged (2-4 per paragraph)

2. **Weave keywords from Phase 3** naturally:
   - Distribution: 1 keyword per 50-80 words (natural density)
   - Placement: First paragraph (highest weight), headers, closing paragraph
   - Avoid: Keyword stuffing (repetition >3x = penalty risk)

3. **Add compliance sections** (if applicable to product_type):
   - **IF product requires ANVISA** (health, beauty, supplements): Include registration number, usage warnings
   - **IF product requires INMETRO** (electronics, toys): Include certification seal, safety info
   - **IF product requires Anatel** (wireless devices): Include homologation number

4. **Apply persuasion patterns** from `config/persuasion_patterns.json`:
   - Use [DORES] → [GANHOS] flow (pain points → solutions)
   - Include [PROVAS] (social proof, testimonials, benchmarks)
   - Address [OBJEÇÕES] preemptively (if applicable)

**Input**:
- `$title_variations` (Phase 2 - use top-scored title for hero section)
- `$keyword_blocks` (Phase 3 - weave into description)
- `$strategic_brief` (marketplace_type, product_type, compliance_requirements)
- Research blocks: [DORES], [GANHOS], [PROVAS], [OBJEÇÕES]
- `config/marketplace_specs.json` (word count limits, compliance rules)
- `config/persuasion_patterns.json` (AIDA, PAS, FAB frameworks)

**Output**:
- `$description_text` (formatted markdown or plain text per marketplace)
- `$word_count` (actual count)
- `$keyword_density` (keywords / total_words)
- `$compliance_checklist` (ANVISA/INMETRO/Anatel if applicable)

**Validation**:
- ✅ Word count within range (per marketplace type)
- ✅ Keyword density: 0.02-0.05 (2-5% = natural, not stuffing)
- ✅ Structure matches template (all required sections present)
- ✅ Compliance sections included (if product requires)
- ✅ No forbidden superlatives without [PROVAS] backing (for ML)
- ✅ Readability score ≥60 (Flesch Reading Ease or similar)

**Error Handling**:
- If word_count out of range → RETRY: "Description too [long|short]. Current: [X] words. Target: [Y]-[Z] words for [marketplace]. [Expand|Condense] sections: [suggestions]"
- If keyword_density <0.02 → WARN: "Low keyword usage ([X]%). Add keywords from Phase 3 blocks naturally."
- If keyword_density >0.05 → FAIL: "Keyword stuffing detected ([X]%). Reduce repetition. Keywords appearing >3x: [list]"
- If required section missing → RETRY: "Missing required section: [section_name]. Template for [marketplace] requires: [list all sections]"
- If compliance missing for regulated product → HALT: "Product requires [ANVISA|INMETRO|Anatel] but compliance section missing. Add: [specific requirements]"
- If superlative without proof (ML only) → RETRY: "Superlative '[word]' needs backing. Add reference to [PROVAS] section or remove."

---
## PHASE 5: Visual Assets

**Objective**: Generate image prompts and video scripts (product-type specific)

**HOP Implementation**:
- `prompts/60_image_prompts.md` (46KB) - AI image generation prompts (DALL-E, Midjourney, etc.)
- `prompts/70_video_script.md` (40KB) - Video storyboards with scenes, timing, voiceover
- Product-type specific templates (B2B SaaS, Physical Product, Service)
- Execution: Load both HOP prompts with `$description_text` and `$keyword_blocks`

**Actions** (implemented in HOP):

1. **Determine visual asset needs** based on `$strategic_brief.product_type`:

   **IF product_type == "B2B_SAAS"**:
   - **Image Assets** (3-5 prompts):
     - Hero image: UI screenshot or architecture diagram
     - Feature screenshots: Key capabilities in action
     - Comparison chart: vs competitors (visual table)
     - Architecture diagram: System components and flow
     - Use case illustrations: Real-world scenarios
   - **Video Script** (30-60 sec demo):
     - Hook (5s): Problem statement
     - Demo (40s): Quick walkthrough of key features
     - CTA (10s): GitHub star / docs link

   **IF product_type == "PHYSICAL_PRODUCT"**:
   - **Image Assets** (5-8 prompts):
     - Hero shot: Product on clean background (white/gradient)
     - 360° views: Front, back, sides, top angles
     - Detail shots: Key features close-up (buttons, ports, materials)
     - Lifestyle shots: Product in use context (person wearing/using)
     - Size comparison: Product next to common object (hand, coin, ruler)
     - Packaging shot: Box/unboxing appeal (if applicable)
   - **Video Script** (15-30 sec product showcase):
     - Hook (3s): Visual wow factor (product reveal)
     - Features (20s): Quick demo of 3-4 key benefits
     - CTA (5s): "Compre agora" / link

   **IF product_type == "SERVICE"**:
   - **Image Assets** (4-6 prompts):
     - Process diagram: Service delivery steps (flowchart)
     - Before/After comparison: Transformation results
     - Team photo: Credibility and trust (if available)
     - Case study screenshots: Client results (charts, metrics)
     - Testimonial cards: Social proof quotes with client names
   - **Video Script** (45-90 sec explainer):
     - Hook (10s): Client pain point
     - Process (50s): How service works (3-5 steps)
     - Results (20s): Outcomes and guarantees
     - CTA (10s): Book consultation / contact

2. **Generate image prompts** (AI-ready format for DALL-E, Midjourney, etc.):
   - Format: "[Subject], [Style], [Composition], [Lighting], [Color palette], [Mood], [Technical specs]"
   - Example (B2B SaaS - Architecture Diagram):
     - "System architecture diagram showing meta-construction agent framework, isometric style, clean minimalist design, soft shadows, blue and purple gradient palette, professional technical mood, 1920x1080, high detail"
   - Example (Physical Product - Hero Shot):
     - "Bluetooth headphones floating on white background, studio photography, centered composition, soft diffused lighting, matte black finish, premium modern mood, 2000x2000, sharp focus, product photography style"

3. **Generate video script** (storyboard format):
   ```markdown
   ## [Product Name] - [Duration] Video Script

   **SCENE 1** [0:00-0:05] - Hook
   - Visual: [describe what viewer sees]
   - Voiceover/Text: "[script text]"
   - Music: [upbeat / dramatic / calm]

   **SCENE 2** [0:05-0:25] - Demo/Process
   - Visual: [...]
   - Voiceover/Text: "[...]"

   **SCENE 3** [0:25-0:30] - CTA
   - Visual: [...]
   - Voiceover/Text: "[...]"
   ```

4. **Optimize for marketplace**:
   - **GitHub**: Focus on architecture diagrams, code screenshots, comparison charts
   - **Mercado Livre/Shopee**: Focus on product photos (multiple angles), infographics, size charts
   - **TikTok Shop**: Focus on short vertical video (9:16 ratio), fast-paced cuts, trending music

**Input**:
- `$strategic_brief` (product_type, marketplace_type)
- `$description_text` (Phase 4 - extract key features to visualize)
- `$keyword_blocks` (Phase 3 - use in image prompts for SEO)

**Output**:
- `$image_prompts` (array of 3-8 AI image generation prompts)
- `$video_script` (storyboard with scenes, timing, voiceover, visuals)
- `$asset_count` (total assets generated)

**Validation**:
- ✅ Image prompt count within range (B2B: 3-5 | Physical: 5-8 | Service: 4-6)
- ✅ Each image prompt ≥50 words (detailed enough for quality generation)
- ✅ Video script has 3+ scenes with timing breakdown
- ✅ Assets align with product_type (no lifestyle shots for SaaS, no architecture diagrams for physical products)
- ✅ Marketplace optimization applied (GitHub: diagrams, ML/Shopee: photos, TikTok: vertical video)

**Error Handling**:
- If asset_count out of range → RETRY: "Need [X]-[Y] image prompts for [product_type]. Generated: [Z]. [Add more|Remove excess]: [suggestions]"
- If image_prompt too short (<50 words) → RETRY: "Image prompt [X] too vague ([Y] words). Add: style, composition, lighting, mood, technical specs."
- If asset type mismatch → FAIL: "Asset '[asset_name]' incompatible with product_type '[type]'. Example: Architecture diagram not needed for PHYSICAL_PRODUCT."
- If video script missing scenes → RETRY: "Video script needs Hook + Demo/Process + CTA. Missing: [list missing scenes]"

---
## PHASE 6: QA & Variants

**Objective**: Quality validation and A/B variant creation (comprehensive quality gates)

**HOP Implementation**:
- `prompts/90_qa_validation.md` (42KB) - Comprehensive quality checks and validation
- `prompts/85_variacoes_s5.md` (15KB) - A/B variant generation (Strategy 5 method)
- Validates all previous phases' outputs with specific thresholds
- Execution: Load QA validation first, then generate variants if quality ≥0.85

**Actions** (implemented in HOP):

1. **Run quality checks** on all previous phase outputs:

   **Title Validation** (from Phase 2):
   - ✅ Char count compliance: GitHub (60-80) | ML (58-60 STRICT) | Shopee (60-80) | TikTok (30-50)
   - ✅ Keyword density ≥0.70 (GitHub/ML) or ≥0.60 (Shopee/TikTok)
   - ✅ Zero forbidden words (check blacklist from config/marketplace_specs.json)
   - ✅ No superlatives without [PROVAS] backing (ML only)

   **Keywords Validation** (from Phase 3):
   - ✅ Total unique keywords ≥ minimum (B2B: 70 | Physical: 60 | Service: 50)
   - ✅ Head terms coverage ≥0.80
   - ✅ Each block ≥10 keywords
   - ✅ No product-type mismatches (e.g., "API" in physical product)

   **Description Validation** (from Phase 4):
   - ✅ Word count within range (per marketplace)
   - ✅ Keyword density 0.02-0.05 (natural, not stuffing)
   - ✅ All required sections present (per marketplace template)
   - ✅ Compliance sections included (ANVISA/INMETRO/Anatel if required)
   - ✅ Readability score ≥60

   **Visual Assets Validation** (from Phase 5):
   - ✅ Asset count within range (per product type)
   - ✅ Each image prompt ≥50 words
   - ✅ Video script has 3+ scenes
   - ✅ Assets align with product_type

2. **Calculate aggregate quality score**:
   ```
   quality_score = (
     title_score * 0.25 +
     keywords_score * 0.20 +
     description_score * 0.30 +
     visual_assets_score * 0.15 +
     compliance_score * 0.10
   )
   ```
   - **Threshold**: ≥0.85 to proceed (HIGH quality gate)
   - If 0.70-0.84 → WARN and allow manual override
   - If <0.70 → HALT and require fixes

3. **Generate A/B variants** (2-3 variations for testing):

   **Variant Strategy** based on marketplace:
   - **GitHub**: Vary hero messaging (technical vs business value)
   - **Mercado Livre**: Vary benefit emphasis (price vs quality vs speed)
   - **Shopee**: Vary promo hooks (discount % vs free shipping vs installments)
   - **TikTok Shop**: Vary viral hooks (FOMO vs WOW factor vs social proof)

   **For Each Variant**:
   - Title variation (from Phase 2 alternatives)
   - Description variation (reorder benefits, adjust tone)
   - Image prompt variation (different angle/style)
   - Keep structure consistent, vary emphasis only

4. **Document improvements needed** (if quality_score <0.95):
   - List specific issues found
   - Suggest concrete fixes (not vague "improve quality")
   - Prioritize: Critical (blocks launch) > Important (reduces effectiveness) > Nice-to-have (polish)

**Input**:
- All previous phase outputs (Phases 1-5)
- `config/marketplace_specs.json` (validation rules)
- Quality thresholds (from workflow specification)

**Output**:
- `$qa_report` (pass/fail per check + aggregate score)
- `$variant_a`, `$variant_b`, `$variant_c` (A/B test variations)
- `$improvement_suggestions` (if score <0.95)

**Validation**:
- ✅ All quality checks executed (title + keywords + description + visual + compliance)
- ✅ Aggregate quality_score calculated
- ✅ If score ≥0.85 → 2-3 A/B variants generated
- ✅ If score <0.85 → Improvement suggestions provided (≥3 concrete items)

**Error Handling**:
- If quality_score <0.70 → HALT: "Quality below threshold ([X]). Critical issues: [list]. Fix before proceeding."
- If quality_score 0.70-0.84 → WARN: "Quality acceptable but suboptimal ([X]). Consider improvements: [list]. Proceed? [Y/N]"
- If quality_score ≥0.85 → PASS: "Quality excellent ([X]). Generating A/B variants."
- If variant generation fails → RETRY: "Failed to generate variants. Ensure Phase 2 has 3 title variations. Current count: [X]"

---
## PHASE 7: Output Assembly

**Objective**: Compile final output in Trinity format (.md + .llm.json + .meta.json)

**HOP Implementation**:
- `prompts/80_seo_metadata.md` (18KB) - SEO metadata generation (optional enhancement)
- Output assembly is primarily handled by ADW orchestration logic
- Trinity format generation: .md (human-readable) + .llm.json (structured) + .meta.json (workflow metadata)
- Execution: Aggregate all phase outputs and format according to Trinity specification

**Actions**:

1. **Assemble primary output** (.md file - human-readable):

   **File Structure**:
   ```markdown
   # [Product Name] - Ad Copy Package

   **Generated**: [timestamp]
   **Marketplace**: [marketplace_type]
   **Product Type**: [product_type]
   **Quality Score**: [X.XX]/1.00

   ---

   ## TITLES (3 variations)

   ### Variation A (Score: [X.XX])
   [title_text] ([XX] chars, [X] keywords, density: [X.XX])

   ### Variation B (Score: [X.XX])
   [...]

   ### Variation C (Score: [X.XX])
   [...]

   ---

   ## KEYWORDS ([XX] total)

   ### Block A: [Block Name]
   [keyword list]

   ### Block B: [Block Name]
   [...]

   ---

   ## DESCRIPTION ([XXX] words)

   [full description text]

   **Metrics**:
   - Word count: [XXX]
   - Keyword density: [X.XX]%
   - Readability: [XX]/100

   ---

   ## VISUAL ASSETS

   ### Image Prompts ([X] total)
   1. [prompt 1]
   2. [prompt 2]
   ...

   ### Video Script
   [full script]

   ---

   ## A/B VARIANTS ([X] total)

   ### Variant A: [Strategy]
   - Title: [...]
   - Description Hook: [...]
   - Primary Benefit: [...]

   ### Variant B: [Strategy]
   [...]

   ---

   ## QUALITY REPORT

   **Aggregate Score**: [X.XX]/1.00
   - Title: [X.XX]/1.00
   - Keywords: [X.XX]/1.00
   - Description: [X.XX]/1.00
   - Visual Assets: [X.XX]/1.00
   - Compliance: [X.XX]/1.00

   **Issues Found**: [X]
   - [list if any]

   **Improvement Suggestions**: [X]
   - [list if score <0.95]

   ---

   ## METADATA

   - Product: [name]
   - Marketplace: [type]
   - Product Type: [type]
   - Compliance: [ANVISA|INMETRO|Anatel|NONE]
   - Research Quality: [X.XX]/1.00
   - Total Execution Time: [XX]min
   ```

2. **Generate structured output** (.llm.json - machine-readable):

   ```json
   {
     "workflow_id": "adw_run_anuncio_[timestamp]",
     "product_name": "...",
     "marketplace_type": "GITHUB|MERCADO_LIVRE|SHOPEE|TIKTOK_SHOP",
     "product_type": "B2B_SAAS|PHYSICAL_PRODUCT|SERVICE",
     "quality_score": 0.XX,
     "execution_time_minutes": XX,

     "titles": [
       {"text": "...", "char_count": XX, "keyword_count": X, "density": 0.XX, "score": 0.XX},
       ...
     ],

     "keywords": {
       "block_a": {"name": "...", "keywords": [...], "count": XX},
       "block_b": {...},
       "block_c": {...},
       "block_d": {...},
       "coverage_score": {"head_terms": 0.XX, "longtails": 0.XX, "synonym_diversity": 0.XX}
     },

     "description": {
       "text": "...",
       "word_count": XXX,
       "keyword_density": 0.XX,
       "readability_score": XX,
       "sections": ["Hook", "Benefits", "Specs", ...]
     },

     "visual_assets": {
       "image_prompts": [...],
       "video_script": {...},
       "asset_count": X
     },

     "ab_variants": [
       {"strategy": "...", "title": "...", "description_hook": "...", "primary_benefit": "..."},
       ...
     ],

     "qa_report": {
       "title_validation": {"passed": true|false, "issues": [...]},
       "keywords_validation": {...},
       "description_validation": {...},
       "visual_assets_validation": {...},
       "compliance_validation": {...},
       "aggregate_score": 0.XX,
       "improvement_suggestions": [...]
     }
   }
   ```

3. **Generate metadata** (.meta.json - workflow metadata):

   ```json
   {
     "workflow_version": "1.0.0",
     "generator": "CODEXA ADW Intelligent Constructor v1.0.0",
     "generated_at": "2025-11-17T...",
     "phases_executed": 7,
     "total_duration_minutes": XX,

     "phase_breakdown": {
       "phase_1_input_validation": {"duration_min": X, "status": "completed"},
       "phase_2_title_generation": {...},
       "phase_3_keywords_expansion": {...},
       "phase_4_description_building": {...},
       "phase_5_visual_assets": {...},
       "phase_6_qa_variants": {...},
       "phase_7_output_assembly": {...}
     },

     "quality_metrics": {
       "research_quality": 0.XX,
       "final_output_quality": 0.XX,
       "validation_checks_passed": XX,
       "validation_checks_total": XX
     },

     "context": {
       "product_name": "...",
       "marketplace_type": "...",
       "product_type": "...",
       "compliance_requirements": [...]
     }
   }
   ```

4. **Save files** to output directory:
   - `USER_DOCS/anuncios/[product_name]/[product_name]_ad_copy.md`
   - `USER_DOCS/anuncios/[product_name]/[product_name]_ad_copy.llm.json`
   - `USER_DOCS/anuncios/[product_name]/[product_name]_ad_copy.meta.json`

5. **Generate execution report** (summary for user):
   ```
   ========================================
   AD COPY GENERATION COMPLETED
   ========================================

   Product: [name]
   Marketplace: [type]
   Quality Score: [X.XX]/1.00 ([EXCELLENT|GOOD|ACCEPTABLE])

   Generated Assets:
   - 3 title variations (best: [title], score: [X.XX])
   - [XX] keywords across 4 semantic blocks
   - [XXX]-word description
   - [X] image prompts + 1 video script
   - [X] A/B test variants

   Files Saved:
   - [path]_ad_copy.md
   - [path]_ad_copy.llm.json
   - [path]_ad_copy.meta.json

   Execution Time: [XX]min (target: 23-38min)

   Next Steps:
   - Review outputs in [path]
   - Test A/B variants if quality ≥0.85
   - Address improvement suggestions if score <0.95
   - Launch when ready!
   ========================================
   ```

**Input**:
- All previous phase outputs (Phases 1-6)
- Execution timestamps (start/end per phase)

**Output**:
- `[product_name]_ad_copy.md` (human-readable)
- `[product_name]_ad_copy.llm.json` (structured data)
- `[product_name]_ad_copy.meta.json` (workflow metadata)
- Execution report (printed to console/log)

**Validation**:
- ✅ All 3 files generated (.md + .llm.json + .meta.json)
- ✅ .md file has all required sections (titles, keywords, description, visuals, variants, QA report, metadata)
- ✅ .llm.json is valid JSON (parseable)
- ✅ .meta.json is valid JSON (parseable)
- ✅ Files saved successfully to output directory
- ✅ Execution report printed

**Error Handling**:
- If file write fails → RETRY: "Failed to save [filename]. Check permissions for directory: [path]"
- If JSON invalid → RETRY: "Invalid JSON structure in [.llm.json|.meta.json]. Error: [parse error details]"
- If required section missing → FAIL: "Output incomplete. Missing section: [section_name] in .md file"
- If directory doesn't exist → CREATE: "Creating output directory: [path]"

---

## EXECUTION INSTRUCTIONS

### For AI Assistants (Conversational Mode)

**Step 1: Load Context**
```
Read the following files:
1. {agent}/PRIME.md
2. {agent}/README.md
3. This workflow (ADW file)
```

**Step 2: Obtain User Input**
```
Ask user for required inputs
```

**Step 3: Execute Workflow**
```
Follow phases sequentially:
- Announce phase start
- Execute phase actions
- Validate outputs
- Report completion
```

**Step 4: Report Completion**
```
Report:
- Duration
- Quality metrics
- Outputs saved
- Next steps
```

---

## SUCCESS CRITERIA

### Workflow Level
- ✅ All 7 phases completed
- ✅ Duration within target
- ✅ No validation failures

### Output Level
- ✅ anuncio.json + anuncio.md, Trinity (.md + .llm.json + .meta.json) generated
- ✅ Quality score ≥0.7
- ✅ Format: trinity

### Quality Level
- ✅ 11 validation criteria passed
- ✅ Compliance requirements met (if applicable)

---

## METADATA

**Created**: 2025-11-17
**Updated**: 2025-11-17 (Integrated with HOP prompts)
**Generator**: CODEXA ADW Intelligent Constructor v1.0.0
**Agent**: anuncio_agent v1.2.1
**Domain**: Ad Generation (marketplace-specific)
**Phases**: 7
**Architecture**: Dual-Layer (ADW ↔ HOP)
**HOP Prompts**: 10 modular prompts (466KB total)
**Auto-generated**: True (reviewed, validated, and enhanced with HOP integration)

---

**Status**: Production-Ready (Dual-Layer Integrated)
**Maintainer**: CODEXA Meta-Constructor
**Version**: 3.2.0 (ADW + HOP Integration)