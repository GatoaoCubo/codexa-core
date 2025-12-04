# 300_ADW_MASTER_ANUNCIO_PIPELINE | Complete Product Marketing Package Orchestration

**Version**: 1.0.0 | **Created**: 2025-12-04
**Type**: Multi-Agent ADW Orchestration (6-Phase Master Pipeline)
**Duration**: 65-108 minutes (depends on complexity)
**Pattern**: Sequential Multi-Agent Execution with Bridge Phases
**Output**: Complete marketing package (research + copy + photos) in Trinity format

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "master_anuncio_pipeline",
  "workflow_name": "Complete Product Marketing Package Orchestration",
  "version": "1.0.0",
  "type": "master_orchestration_multi_agent",
  "context_strategy": "full_history_with_bridges",
  "failure_handling": "stop_and_report_with_rollback",
  "min_llm_model": "gpt-4+ or claude-sonnet-4+",

  "composition": [
    "100_ADW_RUN_PESQUISA (pesquisa_agent)",
    "101_ADW_PESQUISA_BRIDGE (bridge)",
    "100_ADW_RUN_ANUNCIO (anuncio_agent)",
    "101_ADW_ANUNCIO_BRIDGE (bridge)",
    "100_ADW_RUN_PHOTO (photo_agent)"
  ],

  "phases": [
    {
      "phase_id": "phase_0_knowledge",
      "phase_name": "Knowledge Loading",
      "duration": "2-3min",
      "module": "PHASE_0_KNOWLEDGE_LOADING",
      "task_hint": "marketing_orchestration"
    },
    {
      "phase_id": "phase_1_research",
      "phase_name": "Market Research (pesquisa_agent)",
      "duration": "20-30min",
      "workflow": "100_ADW_RUN_PESQUISA",
      "agent": "pesquisa_agent"
    },
    {
      "phase_id": "phase_1_bridge",
      "phase_name": "Research to Copy Bridge",
      "duration": "2-3min",
      "workflow": "101_ADW_PESQUISA_BRIDGE",
      "agent": "bridge"
    },
    {
      "phase_id": "phase_2_copy",
      "phase_name": "Ad Copy Generation (anuncio_agent)",
      "duration": "24-40min",
      "workflow": "100_ADW_RUN_ANUNCIO",
      "agent": "anuncio_agent"
    },
    {
      "phase_id": "phase_2_bridge",
      "phase_name": "Copy to Photo Bridge",
      "duration": "2-3min",
      "workflow": "101_ADW_ANUNCIO_BRIDGE",
      "agent": "bridge"
    },
    {
      "phase_id": "phase_3_photo",
      "phase_name": "Photo Prompt Generation (photo_agent)",
      "duration": "15-30min",
      "workflow": "100_ADW_RUN_PHOTO",
      "agent": "photo_agent"
    }
  ],

  "quality_gates": [
    {
      "phase": "phase_1_research",
      "threshold": 0.70,
      "metric": "research_quality_score",
      "action": "halt_if_below"
    },
    {
      "phase": "phase_2_copy",
      "threshold": 0.85,
      "metric": "ad_copy_quality_score",
      "action": "halt_if_below"
    },
    {
      "phase": "phase_3_photo",
      "threshold": 0.80,
      "metric": "photo_prompt_quality_score",
      "action": "halt_if_below"
    }
  ]
}
```

---

## PURPOSE

Orchestrates a complete marketing pipeline for Brazilian e-commerce products:

1. **Market Research** (pesquisa_agent) → Discovers market landscape, competitors, keywords
2. **Research Bridge** → Transforms research into anuncio context
3. **Ad Copy Generation** (anuncio_agent) → Creates marketplace-specific product copy
4. **Copy Bridge** → Transforms copy into visual concepts
5. **Photo Generation** (photo_agent) → Generates AI image prompts aligned with copy

**Output**: Complete marketing package ready for marketplace launch
- Research insights + competitor analysis
- SEO-optimized titles (3 variations)
- Persuasive descriptions + keywords
- A/B test variants
- 9-scene photo prompt grid

---

## INPUT_CONTRACT

**User Input (Product Brief)**:
```yaml
product_name: string (required)
  # Example: "Arranhador Gato Modular Torre Vertical"

category: string (required)
  # Example: "Pet > Gatos > Brinquedos"

target_audience: string (required)
  # Example: "Donos de gatos responsáveis, classe média"

price_range: string in BRL (required)
  # Example: "R$ 150-200"

marketplace_target: enum (optional, default: "MERCADO_LIVRE")
  # Options: "MERCADO_LIVRE", "SHOPEE", "TIKTOK_SHOP", "AMAZON_BR"

competitors: array[string] (optional)
  # Example: ["Competidor A", "Competidor B"]

special_requirements: object (optional)
  # Example: {
  #   "compliance": ["ANVISA", "INMETRO"],
  #   "style": "minimalist",
  #   "tone": "luxury"
  # }
```

---

## PREREQUISITES

**Before starting, ensure:**

1. **All Agent Context Loaded**:
   - `pesquisa_agent/PRIME.md`
   - `pesquisa_agent/README.md`
   - `anuncio_agent/PRIME.md`
   - `anuncio_agent/README.md`
   - `photo_agent/PRIME.md`
   - `photo_agent/README.md`
   - This workflow file

2. **Configuration Files Available**:
   - `config/marketplaces.json` (9 BR marketplace specs)
   - `config/marketplace_specs.json` (char limits, forbidden words)
   - `config/copy_rules.json` (product-type specific rules)
   - `config/persuasion_patterns.json` (AIDA, PAS, FAB frameworks)
   - `config/camera_profiles.json` (photo settings)
   - `config/photography_styles.json` (style templates)
   - `config/pnl_triggers.json` (psychological triggers)

3. **Capabilities Available**:
   - Web search (REQUIRED for pesquisa)
   - LLM: gpt-4+ or claude-sonnet-4+
   - Multi-format output (.md + .json)
   - File I/O and JSON parsing

4. **Output Directories Created**:
   - `USER_DOCS/Pesquisa/` (research output)
   - `USER_DOCS/anuncios/` (ad copy output)
   - `USER_DOCS/fotos/` (photo prompts output)

---

## ARCHITECTURE: SEQUENTIAL MULTI-AGENT WITH BRIDGES

```
USER INPUT (Product Brief)
        ↓
PHASE 0: Knowledge Loading
        ↓
┌─────────────────────────────────┐
│ PHASE 1: MARKET RESEARCH        │
│ (pesquisa_agent / 20-30min)     │
│ Output: research_notes.md       │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│ BRIDGE 1: Research→Copy         │
│ (2-3min)                        │
│ Transform: Insights→Context     │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│ PHASE 2: AD COPY GENERATION     │
│ (anuncio_agent / 24-40min)      │
│ Output: anuncio.md + variants   │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│ BRIDGE 2: Copy→Photo            │
│ (2-3min)                        │
│ Transform: Copy→Visual Concepts │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│ PHASE 3: PHOTO GENERATION       │
│ (photo_agent / 15-30min)        │
│ Output: photo_prompts_grid_3x3  │
└─────────────────────────────────┘
        ↓
FINAL OUTPUT: Marketing Package
├── research_notes.md
├── anuncio.md (+ .llm.json + .meta.json)
├── photo_prompts.md (+ .llm.json + .meta.json)
├── ab_variants.md
└── package_manifest.json
```

### Why This Architecture?

1. **Sequential Flow**: Each phase outputs feeds into next phase input
2. **Isolation with Bridges**: Agents remain specialized, bridges handle context transformation
3. **Quality Gates**: Validation at each phase prevents garbage-in/garbage-out
4. **Modularity**: Each phase can be rerun independently with saved context
5. **Traceability**: Full audit trail of data transformation through pipeline

---

## PHASE 0: Knowledge Loading (Cross-Agent)

**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `marketing_orchestration`
**Duration**: 2-3min

**Actions**:
1. Detect task type from user input (marketing_orchestration)
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for orchestration task:
   - pesquisa_agent/PRIME.md (research methodology)
   - anuncio_agent/PRIME.md (copy frameworks)
   - photo_agent/PRIME.md (visual generation)
4. Read recommended files:
   - config/marketplace_specs.json
   - config/persuasion_patterns.json
   - config/pnl_triggers.json
5. Store in $knowledge_context (available for all subsequent phases)

**Output**:
```yaml
$knowledge_context:
  pesquisa_framework: "TAC-7 research methodology"
  anuncio_framework: "AIDA/PAS/FAB persuasion patterns"
  photo_framework: "Scene planning + PNL triggers"
  marketplace_rules: "Marketplace-specific compliance"
  config_files: {loaded: true, paths: [...]}
  estimated_duration_minutes: 65-108
```

**Validation**:
- ✅ All 3 agent frameworks loaded
- ✅ Config files accessible
- ✅ Output directories verified
- ✅ User input validated for required fields

**Error Handling**:
- If any agent framework missing → HALT: "Missing [agent] framework. Check PRIME.md paths"
- If config files missing → WARN: "Missing config. Using defaults: [list defaults]"
- If directories unavailable → CREATE: "Creating output directories: [paths]"

---

## PHASE 1: Market Research (pesquisa_agent)

**Objective**: Complete market research for product
**Workflow**: `100_ADW_RUN_PESQUISA` (pesquisa_agent)
**Duration**: 20-30min
**Sub-phases**: 9 phases (discovery, query generation, web search, competitor analysis, compliance, synthesis)

### Phase 1 High-Level Actions

**1.1 Execute pesquisa_agent**:
```bash
# In context of orchestration:
WORKFLOW: 100_ADW_RUN_PESQUISA
AGENT: pesquisa_agent
INPUT: {
  product_name: $input.product_name,
  category: $input.category,
  target_audience: $input.target_audience,
  price_range: $input.price_range,
  marketplace_target: $input.marketplace_target,
  competitors: $input.competitors
}
OUTPUT: research_notes.md (22 blocks)
```

**1.2 Key Research Deliverables**:
- `[HEAD TERMS]`: High-volume keywords (8+ terms)
- `[LONGTAILS]`: Specific phrases (10+ phrases)
- `[DORES]`: Customer pain points (3-5 points)
- `[GANHOS]`: Benefits/gains (3-5 gains)
- `[PROVAS]`: Social proof + evidence (2-3 proofs)
- `[OBJEÇÕES]`: Common objections (2-3 objections)
- `[CONCORRENTES]`: Competitor analysis (3-5 competitors)
- `[TENDENCIAS]`: Market trends (2-4 trends)
- `[COMPLIANCE]`: Regulatory requirements (if applicable)

**1.3 Validation**:
- ✅ All 22 research blocks completed
- ✅ Research quality score ≥0.70
- ✅ Head terms: ≥8 terms with search volume
- ✅ Competitors: ≥3 analyzed with pricing/differentiation
- ✅ research_notes.md saved to USER_DOCS/Pesquisa/

**Error Handling**:
- If research_quality < 0.70 → HALT: "Research quality insufficient ([X]%). Requires manual review or re-research."
- If competitors < 3 → WARN: "Only [X] competitors found. Continue with caution."
- If file save fails → RETRY: "Failed to save research. Check permissions: USER_DOCS/Pesquisa/"
- If web_search unavailable → HALT: "Web search capability required but not available"

**Output**:
```yaml
$research_output:
  file_path: "USER_DOCS/Pesquisa/[product_name]_research_notes.md"
  quality_score: 0.0-1.0
  block_count: 22
  head_terms_count: int
  competitors_count: int
  compliance_requirements: [list]
```

---

## PHASE 1 BRIDGE: Research to Copy Bridge

**Objective**: Transform research output into anuncio_agent input context
**Workflow**: `101_ADW_PESQUISA_BRIDGE`
**Duration**: 2-3min

### Bridge Actions

**Bridge 1.1: Locate Research File**:
```bash
# Already have from Phase 1:
$research_file = $research_output.file_path
```

**Bridge 1.2: Extract Anuncio-Relevant Data**:
```python
RESEARCH_TO_ANUNCIO = {
    "[HEAD TERMS]": {
        "destination": "title_keywords",
        "usage": "SEO optimization, title generation"
    },
    "[LONGTAILS]": {
        "destination": "keyword_blocks",
        "usage": "Semantic expansion, description weaving"
    },
    "[DORES]": {
        "destination": "pain_point_hooks",
        "usage": "Description opening, emotional positioning"
    },
    "[GANHOS]": {
        "destination": "benefit_bullets",
        "usage": "Bullet points, benefits section"
    },
    "[PROVAS]": {
        "destination": "social_proof",
        "usage": "Credibility sections, testimonials"
    },
    "[OBJEÇÕES]": {
        "destination": "objection_handling",
        "usage": "Preemptive copy addressing concerns"
    },
    "[CONCORRENTES]": {
        "destination": "differentiation_points",
        "usage": "Unique value proposition"
    },
    "[COMPLIANCE]": {
        "destination": "compliance_requirements",
        "usage": "Copy compliance sections (ANVISA, etc.)"
    }
}
```

**Bridge 1.3: Validate Completeness**:
- ✅ Head terms extracted (≥3 items)
- ✅ Price positioning identified
- ✅ Differentiators mapped (≥2 items)
- ✅ Quality score ≥7.0/10

**Bridge 1.4: Generate Handoff Block**:
```handoff
contexto: Market research complete for [product_name]
arquivos_gerados:
  - USER_DOCS/Pesquisa/[product]_research_notes.md
proximo: Run anuncio_agent with research context
dados:
  product_name: $input.product_name
  category: $input.category
  target_audience: $input.target_audience
  marketplace_target: $input.marketplace_target
  price_positioning: [extracted from research]
  keywords_principais: [top 10 from HEAD TERMS]
  diferenciais: [from DIFERENCIAS section]
  tendencias: [from TENDENCIAS section]
  compliance: $research_output.compliance_requirements
  provas_sociais: [from PROVAS section]
  objecoes_comuns: [from OBJEÇÕES section]
  competidores_analise: [from CONCORRENTES section]
qualidade: $research_output.quality_score
```

**Output**:
```yaml
$anuncio_context:
  product_name: string
  category: string
  marketplace_target: string
  price_positioning: string
  keywords_principais: [string array]
  diferenciais: [string array]
  compliance_requirements: [string array]
  emotional_triggers: [string array]
  competitor_gaps: [string array]
  research_quality: float
```

**Error Handling**:
- If quality_score < 7.0 → RETRY: "Bridge quality too low. Review research completeness"
- If keywords_principais empty → HALT: "No main keywords extracted from research"
- If file read fails → HALT: "Cannot access research file. Path: [path]"

---

## PHASE 2: Ad Copy Generation (anuncio_agent)

**Objective**: Generate marketplace-specific ad copy with variants
**Workflow**: `100_ADW_RUN_ANUNCIO` (anuncio_agent)
**Duration**: 24-40min
**Sub-phases**: 8 phases (input validation, title generation, keywords expansion, description building, visual assets, QA & variants, output assembly)

### Phase 2 High-Level Actions

**2.1 Execute anuncio_agent**:
```bash
# In context of orchestration:
WORKFLOW: 100_ADW_RUN_ANUNCIO
AGENT: anuncio_agent
INPUT: $anuncio_context (from Phase 1 Bridge)
OUTPUT: {
  file_md: "anuncio.md",
  file_json: "anuncio.llm.json",
  file_meta: "anuncio.meta.json"
}
```

**2.2 Key Copy Deliverables**:
- **Titles** (3 variations):
  - SEO-optimized
  - Marketplace-specific (ML char limits, Shopee emojis, etc.)
  - Quality scored
- **Keywords** (4 semantic blocks):
  - Technical/Attributes
  - Benefits/Comparisons
  - Use Cases
  - Features/Compliance
- **Description** (marketplace template):
  - Hook (1-2 sentences)
  - Benefits (3-5 paragraphs)
  - Specs (bulleted list)
  - Compliance (if applicable)
  - Warranty/CTA
- **A/B Variants** (2-3 versions):
  - Title variations
  - Benefit emphasis variations
  - Tone variations
- **Visual Assets** (supporting prompts):
  - Image prompts for AI generation
  - Video script (optional)

**2.3 Quality Gates**:
- ✅ Title word count within marketplace limits (STRICT for ML)
- ✅ Keyword density 0.02-0.05 (2-5%, natural)
- ✅ Description word count within range
- ✅ Zero forbidden words (compliance check)
- ✅ Aggregate quality score ≥0.85
- ✅ A/B variants generated if quality ≥0.85

**2.4 Validation**:
- ✅ 3 title variations generated
- ✅ 4 keyword blocks with ≥10 keywords each
- ✅ Description includes all required sections
- ✅ No ANVISA/INMETRO violations (if regulated)
- ✅ Readability score ≥60
- ✅ Output files (.md + .json + .meta.json) saved

**Error Handling**:
- If quality_score < 0.85 → WARN: "Ad copy quality suboptimal ([X]%). Improvement suggestions: [list]"
- If title char_count out of range → RETRY: "Title must be [X]-[Y] chars for [marketplace]. Current: [Z]"
- If forbidden_words detected → RETRY: "Remove superlatives without proof: [list words]"
- If ANVISA compliance required but missing → HALT: "Regulated product requires compliance section"
- If file save fails → RETRY: "Failed to save anuncio output. Check permissions"

**Output**:
```yaml
$anuncio_output:
  file_path: "USER_DOCS/anuncios/[product_name]/"
  files:
    - anuncio.md
    - anuncio.llm.json
    - anuncio.meta.json
  quality_score: 0.0-1.0
  titles_count: 3
  keywords_total: int (typically 60-80)
  description_word_count: int
  variants_count: 2-3
  compliance_issues: [list or empty]
```

---

## PHASE 2 BRIDGE: Copy to Photo Bridge

**Objective**: Transform copy output into photo_agent visual context
**Workflow**: `101_ADW_ANUNCIO_BRIDGE` (photo_agent/workflows/)
**Duration**: 2-3min

### Bridge Actions

**Bridge 2.1: Locate Anuncio File**:
```bash
# Already have from Phase 2:
$anuncio_file = $anuncio_output.file_path + "/anuncio.md"
```

**Bridge 2.2: Extract Photo-Relevant Data**:
```python
ANUNCIO_TO_PHOTO = {
    "TITULO": {
        "keywords": "subject_description",
        "product_name": "primary_subject"
    },
    "BULLETS": {
        "features": "hero_shot_elements",
        "benefits": "lifestyle_context",
        "mental_triggers": "pnl_triggers"
    },
    "DESCRICAO": {
        "emocao_alvo": "mood_primary",
        "dores": "scene_problems_solved",
        "ganhos": "scene_transformations",
        "transformacao": "emotional_arc"
    },
    "KEYWORDS": {
        "head_terms": "visual_elements",
        "long_tail": "scene_details"
    }
}
```

**Bridge 2.3: Transform Copy to Visual Concepts** (9-scene grid):

| Anuncio Element | Photo Scene | Visual Translation |
|-----------------|-------------|-------------------|
| Product name + keywords | Scene 1 & 9 | Hero pack shot (white bg for ML compliance) |
| Benefit bullets | Scenes 2-6 | 5 distinct scene types (lifestyle, detail, assembly, social, integration) |
| Material/texture focus | Scene 3 | Macro photography of key material/texture |
| Emotional transformation | Scene 7 | Before/after or comparative visual |
| Compliance/certification | Scene 8 | Detail shot showing quality/durability |

**Bridge 2.4: Map PNL Triggers**:
```json
{
  "copy_emotion": "emocao_alvo",
  "pnl_triggers": [
    "escassez → urgência → fast-paced scene",
    "prova_social → pertencimento → multiple users scene",
    "autoridade → confiança → quality/professional scene",
    "reciprocidade → conforto → ease-of-use scene"
  ]
}
```

**Bridge 2.5: Validate Visual Concepts**:
- ✅ Subject description extracted (from TITULO)
- ✅ 9 scene concepts defined
- ✅ PNL triggers mapped (≥1)
- ✅ Mood/emotional tone defined
- ✅ Marketplace compliance included (white bg if ML)
- ✅ Quality score ≥7.0/10

**Bridge 2.6: Generate Handoff Block**:
```handoff
contexto: Ad copy complete for [product_name]
arquivos_gerados:
  - USER_DOCS/anuncios/[product]/anuncio.md
proximo: Run photo_agent with visual context
dados:
  subject: "[extracted from TITULO]"
  style: "[inferred from product type + copy tone]"
  scenes: 9
  pnl_triggers: [extracted mental triggers]
  brand_profile:
    mood: "[extracted from DESCRICAO emotional arc]"
    target_audience: [from copy positioning]
  compliance_mode: "[marketplace requirement]"
scene_concepts:
  - hero_pack_shot: "[from TITULO + subject]"
  - lifestyle_use: "[from benefits bullets]"
  - material_detail: "[from material/texture mention]"
  - assembly_ease: "[from 'fácil de usar' type benefits]"
  - social_validation: "[from social proof elements]"
  - home_integration: "[from lifestyle/environment context]"
  - transformation: "[from DESCRICAO emotional transformation]"
  - durability_quality: "[from quality/warranty guarantees]"
  - scale_reference: "[from product dimensions if mentioned]"
qualidade: $anuncio_output.quality_score
```

**Output**:
```yaml
$photo_context:
  subject: string
  style: string
  scenes: 9
  pnl_triggers: [string array]
  mood: string
  compliance_mode: "marketplace" | "lifestyle" | "editorial"
  scene_concepts: [9 descriptions]
  marketplace_hints: [specific requirements]
  copy_quality: float
```

**Error Handling**:
- If quality_score < 7.0 → RETRY: "Bridge quality too low. Review copy completeness"
- If subject_unclear → HALT: "Cannot extract clear product subject from copy"
- If TITULO missing → HALT: "No title found in anuncio file"

---

## PHASE 3: Photo Prompt Generation (photo_agent)

**Objective**: Generate AI image prompts aligned with copy and research
**Workflow**: `100_ADW_RUN_PHOTO` (photo_agent)
**Duration**: 15-30min
**Sub-phases**: 5 phases (input processing, camera design, prompt generation, brand validation, batch assembly)

### Phase 3 High-Level Actions

**3.1 Execute photo_agent**:
```bash
# In context of orchestration:
WORKFLOW: 100_ADW_RUN_PHOTO
AGENT: photo_agent
INPUT: $photo_context (from Phase 2 Bridge)
OUTPUT: {
  file_md: "photo_prompts_grid_3x3.md",
  file_json: "photo_prompts_grid_3x3.llm.json",
  file_meta: "photo_prompts_grid_3x3.meta.json"
}
```

**3.2 Key Photo Deliverables**:
- **9 Individual Prompts** (Scene 1-9):
  - Each ≥80 words (detailed for Midjourney/DALL-E)
  - Includes: subject, style, composition, lighting, color, mood, technical specs
  - Marketplace compliance (white background for scenes 1 & 9 if ML)
- **1 Batch Concatenated Block**:
  - All 9 prompts in single block (for bulk generation)
- **Scene Planning Document**:
  - Grid layout showing scene relationships
  - Camera profiles and lighting setups
  - PNL trigger mapping per scene
- **Midjourney/DALL-E Optimization**:
  - Prompt syntax specific to AI model
  - Aspect ratios optimized per marketplace
  - Quality/detail parameters

**3.3 Quality Gates**:
- ✅ 9 prompts generated (Scenes 1-9)
- ✅ Each prompt ≥80 words (detailed enough for quality generation)
- ✅ Scene 1 & 9 have white background #FFFFFF (if ML compliance required)
- ✅ Scenes 2-8 provide visual diversity (hero, lifestyle, detail, etc.)
- ✅ PNL triggers present in scene descriptions
- ✅ Brand consistency maintained across all 9 scenes
- ✅ Aggregate quality score ≥0.80

**3.4 Validation**:
- ✅ 9 scene prompts + 1 batch block generated
- ✅ File format Trinity (.md + .json + .meta.json)
- ✅ Compliance requirements met (marketplace-specific)
- ✅ Scene diversity confirmed (at least 5 distinct scene types)
- ✅ PNL trigger density ≥1 per scene
- ✅ Output files saved to USER_DOCS/fotos/

**Error Handling**:
- If prompt_count < 9 → RETRY: "Need 9 scene prompts. Generated: [X]"
- If any prompt < 80 words → RETRY: "Prompt [X] too vague ([Y] words). Expand with: style, lighting, mood"
- If compliance missing (white bg) → HALT: "Marketplace [ML] requires white background for scenes 1 & 9"
- If file save fails → RETRY: "Failed to save photo prompts. Check permissions"

**Output**:
```yaml
$photo_output:
  file_path: "USER_DOCS/fotos/[product_name]/"
  files:
    - photo_prompts_grid_3x3.md
    - photo_prompts_grid_3x3.llm.json
    - photo_prompts_grid_3x3.meta.json
  quality_score: 0.0-1.0
  scene_count: 9
  batch_block_present: true
  pnl_trigger_density: float (avg per scene)
  compliance_status: "passed" | "needs_review"
  marketplace_compliance:
    mercado_livre: bool (white bg scenes 1+9)
    shopee: bool (lifestyle included)
    tiktok_shop: bool (vertical format)
```

---

## FINAL OUTPUT ASSEMBLY

**Objective**: Compile complete marketing package and generate manifest
**Duration**: 3-5min

### Output Assembly Actions

**Output A1: Organize Deliverables**:
```
USER_DOCS/
├── Pesquisa/
│   ├── [product_name]_research_notes.md (22 blocks)
│   └── [product_name]_research_notes.meta.json
├── anuncios/
│   ├── [product_name]/
│   │   ├── anuncio.md
│   │   ├── anuncio.llm.json
│   │   └── anuncio.meta.json
└── fotos/
    └── [product_name]/
        ├── photo_prompts_grid_3x3.md
        ├── photo_prompts_grid_3x3.llm.json
        └── photo_prompts_grid_3x3.meta.json
```

**Output A2: Generate Package Manifest**:
```json
{
  "workflow_id": "master_anuncio_pipeline_[timestamp]",
  "product_name": "...",
  "marketplace_target": "...",
  "generated_at": "ISO 8601 timestamp",
  "total_duration_minutes": int,

  "phase_breakdown": {
    "phase_0_knowledge": {"status": "completed", "duration_min": X},
    "phase_1_research": {"status": "completed", "duration_min": X, "quality_score": 0.XX},
    "phase_1_bridge": {"status": "completed", "duration_min": X},
    "phase_2_copy": {"status": "completed", "duration_min": X, "quality_score": 0.XX},
    "phase_2_bridge": {"status": "completed", "duration_min": X},
    "phase_3_photo": {"status": "completed", "duration_min": X, "quality_score": 0.XX}
  },

  "deliverables": {
    "research": {
      "file": "USER_DOCS/Pesquisa/[product]_research_notes.md",
      "blocks_completed": 22,
      "head_terms": int,
      "competitors_analyzed": int,
      "compliance_requirements": [list]
    },
    "ad_copy": {
      "file": "USER_DOCS/anuncios/[product]/anuncio.md",
      "titles": 3,
      "keywords_total": int,
      "description_words": int,
      "variants": int,
      "quality_score": 0.XX
    },
    "photo_prompts": {
      "file": "USER_DOCS/fotos/[product]/photo_prompts_grid_3x3.md",
      "scenes": 9,
      "batch_block": true,
      "compliance_ready": bool,
      "quality_score": 0.XX
    }
  },

  "quality_metrics": {
    "research_quality": 0.XX,
    "copy_quality": 0.XX,
    "photo_quality": 0.XX,
    "overall_package_score": 0.XX,
    "all_phases_passed_gates": bool
  },

  "next_steps": [
    "Review research insights in: [path]",
    "Test A/B variants from: [path]",
    "Generate images using photo prompts from: [path]",
    "Optimize based on quality feedback",
    "Launch on [marketplace_target]"
  ],

  "rollback_instructions": "If issues found: [describe how to rerun individual phases]"
}
```

**Output A3: Generate Execution Report**:
```markdown
========================================
MARKETING PACKAGE GENERATION COMPLETED
========================================

Product: [name]
Marketplace: [target]
Package Quality Score: [X.XX]/1.00 ([EXCELLENT|GOOD|ACCEPTABLE])

Generated Assets:
──────────────────────────────────────
RESEARCH (20-30min)
├─ 22-block research document
├─ Head terms: [X] (quality: [X.XX]/10)
├─ Competitors: [X] (depth: thorough)
├─ Compliance: [ANVISA|INMETRO|None]
└─ File: USER_DOCS/Pesquisa/[product]_research_notes.md

AD COPY (24-40min)
├─ 3 title variations (best: [title], score: [X.XX])
├─ [XX] keywords across 4 semantic blocks
├─ [XXX]-word description (readability: [XX]/100)
├─ 2-3 A/B test variants (strategy: [variants])
├─ Quality score: [X.XX]/1.00
└─ Files: USER_DOCS/anuncios/[product]/

PHOTO PROMPTS (15-30min)
├─ 9-scene grid plan (3x3 layout)
├─ Individual prompts: ≥80 words each
├─ Batch concatenated block: 1 (for bulk generation)
├─ Compliance: ✅ Marketplace requirements met
├─ Quality score: [X.XX]/1.00
└─ Files: USER_DOCS/fotos/[product]/

──────────────────────────────────────
Total Execution Time: [XX]min (target: 65-108min)
Quality Gates Passed: [X]/3 (research, copy, photo)

Recommended Actions:
──────────────────────────────────────
1. Review research insights for market positioning
2. Test A/B variants before launch (title/benefit emphasis)
3. Generate images using photo prompts
4. Verify compliance (ANVISA/INMETRO if applicable)
5. A/B test on marketplace before full rollout

Files Ready For:
──────────────────────────────────────
✓ Marketplace listings (title + description + keywords)
✓ Image generation (Midjourney/DALL-E batch)
✓ A/B testing (multiple variants)
✓ Performance tracking (baseline metrics)

========================================
Status: ✅ READY FOR LAUNCH
========================================
```

**Output A4: Save Manifest + Report**:
- `USER_DOCS/anuncios/[product]/package_manifest.json`
- `USER_DOCS/anuncios/[product]/execution_report.md`

---

## QUALITY GATES & VALIDATION

### Gate 1: Research Quality (After Phase 1)

**Threshold**: ≥0.70/1.00
**Metrics**:
- Research blocks completed: 22/22
- Head terms: ≥8 with search volume data
- Competitors: ≥3 analyzed with pricing
- Research quality score: ≥0.70

**Actions**:
- ✅ If PASS → Proceed to Phase 1 Bridge
- ⚠️ If WARN (0.65-0.69) → Extend research, manual review
- ❌ If FAIL (<0.65) → HALT, re-research required

### Gate 2: Ad Copy Quality (After Phase 2)

**Threshold**: ≥0.85/1.00
**Metrics**:
- Title validation: 3 variations within spec
- Keyword density: 0.02-0.05 (natural)
- Description: All sections present + readability ≥60
- Compliance: Zero violations
- A/B variants: 2-3 generated

**Actions**:
- ✅ If PASS → Proceed to Phase 2 Bridge
- ⚠️ If WARN (0.70-0.84) → Continue with improvements flagged
- ❌ If FAIL (<0.70) → HALT, regenerate

### Gate 3: Photo Quality (After Phase 3)

**Threshold**: ≥0.80/1.00
**Metrics**:
- Scene prompts: 9/9 ≥80 words each
- Compliance: Marketplace requirements met
- PNL triggers: Present in all scenes
- Batch block: Generated and concatenated

**Actions**:
- ✅ If PASS → Package assembly
- ⚠️ If WARN (0.70-0.79) → Continue with quality notes
- ❌ If FAIL (<0.70) → Regenerate photo prompts

### Overall Quality Score

```
Overall = (
  research_score * 0.30 +
  copy_score * 0.40 +
  photo_score * 0.30
)
```

**Interpretation**:
- ≥0.85 → EXCELLENT (ready for launch)
- 0.70-0.84 → GOOD (ready with minor improvements)
- <0.70 → NEEDS WORK (flag for review)

---

## ERROR HANDLING & RECOVERY (LAW 7)

### Recoverable Errors (Retry Strategy)

| Error | Category | Strategy | Max Retries |
|-------|----------|----------|------------|
| Web search timeout | Transient | Backoff 2-3min, retry | 2 |
| Rate limit (429) | Transient | Wait 5min, retry | 1 |
| File lock | Transient | Wait 10s, retry | 3 |
| Network hiccup | Transient | Backoff exponential | 2 |
| Output truncation | Transient | Split into smaller chunks | 1 |

### Fatal Errors (Fail Fast)

| Error | Action | Message |
|-------|--------|---------|
| Web search unavailable | HALT Phase 1 | "Web search required but not available" |
| Invalid product brief | HALT Phase 0 | "Required fields missing: [list]" |
| Quality gate failure (2+ retries) | HALT + FLAG | "Quality threshold not reached after 2 retries" |
| File permissions error | HALT + CREATE | "Cannot write to [path]. Creating directory..." |
| Config file missing | HALT + USE_DEFAULT | "Config missing. Using defaults: [list]" |

### Degrade Gracefully

| Issue | Degradation | Continue? |
|-------|-------------|-----------|
| Competitor data incomplete | Proceed with 3 competitors (not 5) | ✅ YES |
| Photo compliance edge case | Flag for manual review | ✅ YES (with flag) |
| Title perfect match (2 of 3) | Use 2 variants instead of 3 | ✅ YES (with note) |
| Research quality 0.68 (below 0.70) | Continue with warning + improvements needed | ⚠️ MAYBE (manual decision) |

---

## EXECUTION INSTRUCTIONS

### For AI Assistants (This Workflow)

**Step 1: Load Context** (2-3min)
```
1. Read CLAUDE.md (project laws)
2. Read pesquisa_agent/PRIME.md
3. Read anuncio_agent/PRIME.md
4. Read photo_agent/PRIME.md
5. This workflow file (300_ADW_MASTER_ANUNCIO_PIPELINE.md)
```

**Step 2: Validate Prerequisites** (2min)
```
1. Confirm user input (product brief with all required fields)
2. Check output directories exist
3. Verify config files accessible
4. Confirm LLM model ≥gpt-4 or sonnet-4+
```

**Step 3: Execute Phases Sequentially** (65-108min)
```
Phase 0: Knowledge Loading (2-3min)
  └─ Load cross-agent frameworks, config files

Phase 1: Market Research (20-30min)
  └─ Execute 100_ADW_RUN_PESQUISA via pesquisa_agent
  └─ Validate research_quality ≥0.70

Phase 1 Bridge: Research→Copy (2-3min)
  └─ Transform research into anuncio context
  └─ Generate handoff block

Phase 2: Ad Copy (24-40min)
  └─ Execute 100_ADW_RUN_ANUNCIO via anuncio_agent
  └─ Validate quality_score ≥0.85

Phase 2 Bridge: Copy→Photo (2-3min)
  └─ Transform copy into visual concepts
  └─ Generate scene plan + PNL mapping

Phase 3: Photo Prompts (15-30min)
  └─ Execute 100_ADW_RUN_PHOTO via photo_agent
  └─ Validate quality_score ≥0.80

Output Assembly (3-5min)
  └─ Organize deliverables
  └─ Generate manifest + report
```

**Step 4: Report Completion** (2min)
```
Report:
- Total duration ([X]min, target 65-108min)
- Overall quality score ([X.XX]/1.00)
- All phases status (✅ passed or ❌ flagged)
- Output files location
- Recommended next steps
```

### For Manual Execution (Sequential)

1. **Start Phase 1**: Run pesquisa_agent independently with product brief
2. **Wait for Phase 1**: Confirm research_notes.md saved
3. **Manual Bridge**: Copy research insights to clipboard
4. **Start Phase 2**: Run anuncio_agent with pasted research context
5. **Wait for Phase 2**: Confirm anuncio.md + variants saved
6. **Manual Bridge**: Copy copy structure and PNL triggers
7. **Start Phase 3**: Run photo_agent with pasted copy context
8. **Generate Package**: Move files to organized USER_DOCS/ structure
9. **Validate**: Check quality metrics and compliance

---

## SUCCESS CRITERIA

### Workflow Level
- ✅ All 6 phases completed (Phase 0-3 + 2 bridges)
- ✅ Duration within target (65-108 minutes)
- ✅ No validation failures (all quality gates passed)
- ✅ All output files generated

### Output Level
- ✅ Research document: 22 blocks with ≥0.70 quality
- ✅ Ad copy: 3 titles + keywords + description + 2-3 variants with ≥0.85 quality
- ✅ Photo prompts: 9 scenes + batch block with ≥0.80 quality
- ✅ Format: Trinity (.md + .json + .meta.json) for copy and photo
- ✅ Compliance: All marketplace requirements met

### Quality Level
- ✅ 3/3 quality gates passed (research ≥0.70, copy ≥0.85, photo ≥0.80)
- ✅ Overall package score ≥0.75
- ✅ No critical compliance violations
- ✅ All deliverables usable for marketplace launch

---

## TROUBLESHOOTING

### Phase 1 Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Research quality <0.70 | Incomplete research blocks | Re-run with explicit block focus, add more competitor analysis |
| Web search unavailable | Network issue or API down | Check internet, verify API keys, wait 5min + retry |
| Competitors insufficient | Only 2 competitors found | Extend search, add indirect competitors, manual research |

### Phase 2 Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Copy quality <0.85 | Weak research input | Review Phase 1 quality, re-bridge with more detail |
| Title char count wrong | Marketplace specification not met | Regenerate with explicit char limit reminder |
| Keyword stuffing detected | Too many keywords in description | Reduce keyword repetition, space out distribution |
| Compliance violation (ML) | Superlatives without proof | Remove unsupported claims or add proof from research |

### Phase 3 Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Photo quality <0.80 | Vague scene descriptions | Add more detail to scene concepts in Phase 2 Bridge |
| Compliance missing (white bg) | Overlooked marketplace requirement | Regenerate with explicit marketplace compliance check |
| Prompt <80 words | Insufficient detail for AI | Expand prompt with: subject, style, composition, lighting, mood |

### Bridge Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Bridge quality <7.0 | Incomplete extraction | Review source phase output completeness |
| Subject unclear | Ambiguous product name | Clarify product definition in original brief |
| PNL triggers missing | Not extracted from copy | Manually add emotional positioning from copy |

---

## RELATED WORKFLOWS

- **100_ADW_RUN_PESQUISA** - Market research workflow (used in Phase 1)
- **100_ADW_RUN_ANUNCIO** - Ad copy generation workflow (used in Phase 2)
- **100_ADW_RUN_PHOTO** - Photo prompt generation workflow (used in Phase 3)
- **101_ADW_PESQUISA_BRIDGE** - Research→Copy bridge (used between Phases 1-2)
- **101_ADW_ANUNCIO_BRIDGE** - Copy→Photo bridge (used between Phases 2-3)
- **201_ADW_FEATURE_DEVELOPMENT** - Pattern reference for phase structure
- **203_ADW_PARALLEL_ORCHESTRATION** - For parallel variant generation opportunities

---

## METADATA

**Created**: 2025-12-04
**Version**: 1.0.0
**Type**: Master Orchestration (Multi-Agent ADW)
**Agents Involved**: pesquisa_agent, anuncio_agent, photo_agent
**Duration**: 65-108 minutes
**Composition**: 5 workflows + 2 bridges
**Architecture**: Sequential Multi-Agent with Bridge Phases
**Quality Gates**: 3 (research, copy, photo)
**Output Format**: Trinity (.md + .json + .meta.json)
**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor

---

**Version**: 1.0.0 (Initial Release)
**Last Updated**: 2025-12-04
**Generator**: CODEXA ADW Orchestration Framework

