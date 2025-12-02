# 100_ADW_RUN_MARCA | Marca (Brand) Agent Execution Workflow

**Purpose**: End-to-end execution workflow for marca_agent
**Type**: 7-Phase ADW | **Duration**: ~21-36min
**Output**: # ✅ Brand Consistency Score: 0.87 (Excellent), brand_strategy.md (30+ blocks) + validation_report.txt (json+markdown)
**Architecture**: Dual-Layer (ADW Orchestration ↔ HOP Execution)
**Status**: Production-Ready (Integrated with HOP prompts v2.0.0)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_run_marca",
  "workflow_name": "Marca (Brand) Agent Execution",
  "agent": "marca_agent",
  "version": "1.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4+ or claude-sonnet-4+",
  "required_capabilities": {
    "compliance validation": true
  },
  "phases": [
    {
      "phase_id": "phase_0_knowledge",
      "phase_name": "Knowledge Loading",
      "duration": "1-2min",
      "module": "PHASE_0_KNOWLEDGE_LOADING",
      "task_hint": "brand_strategy"
    },
    {
      "phase_id": "phase_1_input_validation_&_discovery",
      "phase_name": "Input Validation & Discovery",
      "duration": "2-5min",
      "description": "Validate business brief and conduct brand discovery"
    },
    {
      "phase_id": "phase_2_brand_positioning_strategy",
      "phase_name": "Brand Positioning Strategy",
      "duration": "3-7min",
      "description": "Define unique brand positioning using StoryBrand framework"
    },
    {
      "phase_id": "phase_3_messaging_&_voice_development",
      "phase_name": "Messaging & Voice Development",
      "duration": "3-7min",
      "description": "Create brand messaging hierarchy and tone of voice"
    },
    {
      "phase_id": "phase_4_visual_identity_guidelines",
      "phase_name": "Visual Identity Guidelines",
      "duration": "3-7min",
      "description": "Design visual identity system and usage guidelines"
    },
    {
      "phase_id": "phase_5_brand_asset_generation",
      "phase_name": "Brand Asset Generation",
      "duration": "5-10min",
      "description": "Generate brand assets (logos, colors, typography specs)"
    },
    {
      "phase_id": "phase_6_qa_&_brand_consistency",
      "phase_name": "QA & Brand Consistency",
      "duration": "3-7min",
      "description": "Validate brand consistency and create variant applications"
    },
    {
      "phase_id": "phase_7_output_assembly",
      "phase_name": "Output Assembly",
      "duration": "2-5min",
      "description": "Compile final brand strategy documentation"
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
   - `config/brand_strategy_ecomlm.json`
   - `config/color_psychology.json`
   - `config/compliance_rules.json`
   - `config/marketplace_policies.json`
   - `config/storytelling_frameworks.json`

2. **Capabilities Available**:
   - LLM: gpt-4+ or claude-sonnet-4+
   - Tools: compliance validation

3. **User Input Ready**:
   - "Garrafa de água reutilizável, ecológica

---

## ARCHITECTURE: DUAL-LAYER INTEGRATION (ADW ↔ HOP)

This workflow implements a **Dual-Layer Architecture** where:

### **LAYER 1: ADW (Adaptive Dual-layer Workflow)**
- **Purpose**: High-level orchestration and coordination
- **This file**: Defines phases, sequencing, validation, error handling
- **Role**: "What to do" and "When to do it"

### **LAYER 2: HOP (Hyper-Optimized Prompts)**
- **Purpose**: Detailed execution and domain-specific implementation
- **Location**: `prompts/` directory (2 modular prompts, ~46KB total)
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
| 1-6 | `01_brand_identity_HOP.md` | 23KB | Complete brand construction (discovery, positioning, messaging, visual identity, assets, QA) |
| 7 | `main_agent_hop.md` | 23KB | Output assembly & orchestration (Trinity: .md + .llm.json + .meta.json) |

**Total HOP library**: 2 prompts, ~46KB of specialized brand strategy knowledge

---

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `brand_strategy`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

## PHASE 1: Input Validation & Discovery

**Objective**: Validate business brief and conduct brand discovery

**HOP Implementation**: `prompts/01_brand_identity_HOP.md` (23KB)
- Section 1: Input validation and discovery
- Business brief parsing (mission, vision, values extraction)
- Auto-detection of business type (B2B/B2C/Service)
- Competitive landscape analysis (≥3 competitors with positioning)
- Target audience definition (demographics + psychographics + pain points)
- Quality scoring (completeness threshold ≥0.70)
- Execution: Load HOP prompt with `$user_input` and config files

**Actions** (implemented in HOP):
1. **Read and parse business brief**: Load from user input or brief document
2. **Auto-detect business type**: B2B (keywords: 'enterprise', 'platform', 'SaaS') | B2C (keywords: 'consumidor', 'produto', 'varejo') | Service (keywords: 'consultoria', 'serviço')
3. **Conduct stakeholder discovery**: Extract business values, mission, vision from brief
4. **Analyze competitive landscape**: Identify ≥3 competitors and their positioning
5. **Define target audience**: Demographics + psychographics + pain points
6. **Validate discovery completeness**: Mission defined, values ≥3, competitors ≥3, audience defined, quality_score ≥0.70

**Input**:
- `$user_input`
- `$config_files`

**Output**:
- `$validated_data`
- `$quality_score`

**Validation**:
- ✅ Business brief validated (mission + vision + values present)
- ✅ Business type detected with confidence ≥0.6
- ✅ Competitors analyzed ≥3 (with positioning mapped)
- ✅ Target audience defined (demographics + psychographics)
- ✅ Quality score ≥0.70 (discovery completeness)

**Error Handling**:
- If brief missing mission/vision → HALT: 'Business brief incomplete. Need mission + vision. Provide via brief document or user input.'
- If competitors <3 → WARN: 'Only [X] competitors analyzed. Need ≥3 for quality positioning. Add more competitors.'
- If quality_score <0.70 → FAIL: 'Discovery quality below threshold. Score: [X]. Issues: [list missing elements]'

---
## PHASE 2: Brand Positioning Strategy

**Objective**: Define unique brand positioning using StoryBrand framework

**HOP Implementation**: `prompts/01_brand_identity_HOP.md` (23KB)
- Section 2: Brand positioning and strategy
- Positioning statement generation (template-based)
- Brand values establishment (3-5 core values with definitions)
- Brand archetype selection (12 archetypes: Hero, Sage, Rebel, Caregiver, Creator, etc.)
- Messaging pillars development (3-5 key messages)
- Positioning validation (statement ≤2 sentences, no archetype-values conflicts)
- Execution: Uses `$phase_1_output` (validated discovery data)

**Actions** (implemented in HOP):
1. **Extract brand essence** from discovery (values, differentiators, audience insights)
2. **Define positioning statement**: Template: 'For [target] who [need], [brand] is [category] that [unique benefit]. Unlike [competition], we [proof]'
3. **Establish brand values** (3-5 core values with definitions + manifestations)
4. **Select brand archetype**: Choose from 12 archetypes (Hero, Sage, Rebel, Caregiver, Creator, etc) aligned with positioning
5. **Develop messaging pillars** (3-5 key messages supporting positioning)
6. **Validate positioning**: Statement ≤2 sentences, values 3-5, archetype not conflicting, pillars ≥3

**Input**:
- `$phase_1_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Positioning statement ≤2 sentences
- ✅ Brand values count: 3-5 (ideal 4)
- ✅ Archetype selected from validated list (12 options)
- ✅ Messaging pillars: 3-5 (each with ≥3 supporting points)
- ✅ No archetype-values conflicts detected

**Error Handling**:
- If positioning_statement >2 sentences → RETRY: 'Condense to max 2 sentences. Current: [X] sentences. Remove: [suggestions]'
- If values count <3 or >5 → RETRY: 'Need 3-5 values. Current: [X]. [Add|Remove]: [suggestions]'
- If archetype conflicts with values → RETRY: 'Archetype [X] conflicts with value [Y]. Select alternative: [suggest 2-3 archetypes]'
- If messaging_pillars <3 → RETRY: 'Need ≥3 pillars. Current: [X]. Add pillars for: [suggest topics based on positioning]'

---
## PHASE 3: Messaging & Voice Development

**Objective**: Create brand messaging hierarchy and tone of voice

**HOP Implementation**: `prompts/01_brand_identity_HOP.md` (23KB)
- Section 3: Messaging hierarchy and voice development
- Messaging hierarchy creation (primary + secondary + proof points)
- Brand voice attributes definition (3-5 attributes: Professional, Friendly, Innovative, etc.)
- Tone of voice guidelines (Do's + Don'ts + Example phrases)
- StoryBrand framework application (7 elements: Character, Problem, Guide, Plan, CTA, Success, Failure)
- Communication templates generation (tagline, elevator pitch, brand story 200-300 words)
- Execution: Uses `$phase_2_output` (positioning and values)

**Actions** (implemented in HOP):
1. **Create messaging hierarchy**: Primary message + secondary messages + proof points
2. **Define brand voice attributes** (3-5 attributes: e.g., 'Professional', 'Friendly', 'Innovative')
3. **Establish tone of voice guidelines**: Do's + Don'ts + Example phrases for each voice attribute
4. **Apply StoryBrand framework**: Character (customer) + Problem + Guide (brand) + Plan + Call-to-Action + Success + Failure
5. **Generate key communication templates**: Tagline, elevator pitch, brand story (200-300 words)
6. **Validate messaging**: Hierarchy clear (3 levels), voice attributes 3-5, StoryBrand elements complete

**Input**:
- `$phase_2_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Messaging hierarchy has 3 levels (primary, secondary, proof points)
- ✅ Voice attributes count: 3-5
- ✅ Tone guidelines complete (Do's + Don'ts + Examples)
- ✅ StoryBrand 7 elements present (Character, Problem, Guide, Plan, CTA, Success, Failure)
- ✅ Communication templates generated: tagline, elevator pitch, brand story (200-300 words)

**Error Handling**:
- If voice_attributes <3 or >5 → RETRY: 'Need 3-5 voice attributes. Current: [X]. [Add|Remove]: [suggestions]'
- If StoryBrand elements incomplete → RETRY: 'Missing StoryBrand elements: [list]. Complete: [provide examples]'
- If brand_story word_count <200 or >300 → RETRY: 'Brand story length issue. Current: [X] words. Target: 200-300. [Expand|Condense]'

---
## PHASE 4: Visual Identity Guidelines

**Objective**: Design visual identity system and usage guidelines

**HOP Implementation**: `prompts/01_brand_identity_HOP.md` (23KB)
- Section 4: Visual identity system design
- Color palette design (primary 1-2 + secondary 2-3 + accent 1-2 with hex codes)
- Typography system selection (primary font headlines + secondary body + tertiary optional)
- Logo usage guidelines (variations, minimum sizes, clear space, incorrect usage)
- Visual style definition (photography, illustration, iconography, graphic elements)
- Brand patterns establishment (shapes, textures, motifs aligned with personality)
- Execution: Uses `$phase_3_output` (messaging and voice) to ensure visual alignment

**Actions** (implemented in HOP):
1. **Design color palette**: Primary (1-2 colors) + Secondary (2-3 colors) + Accent (1-2 colors) with hex codes
2. **Select typography system**: Primary font (headlines) + Secondary font (body) + Tertiary (optional) with usage rules
3. **Create logo usage guidelines**: Logo variations (primary, secondary, monochrome), minimum sizes, clear space, incorrect usage examples
4. **Define visual style**: Photography style, illustration style, iconography, graphic elements
5. **Establish brand patterns**: Shapes, textures, motifs aligned with brand personality
6. **Validate visual identity**: Color palette complete (≥3 colors), typography ≥2 fonts, logo guidelines comprehensive

**Input**:
- `$phase_3_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Color palette: ≥3 colors (primary + secondary + accent) with hex codes
- ✅ Typography: ≥2 fonts (headline + body) with usage rules
- ✅ Logo guidelines comprehensive (variations, sizes, clear space, incorrect usage)
- ✅ Visual style defined (photography, illustration, iconography)
- ✅ Brand patterns established (aligned with personality)

**Error Handling**:
- If color_palette <3 → RETRY: 'Need ≥3 colors (primary + secondary + accent). Current: [X]. Add: [suggest color types]'
- If typography <2 fonts → RETRY: 'Need ≥2 fonts (headline + body). Current: [X]. Add: [suggest font categories]'
- If logo_guidelines incomplete → RETRY: 'Logo guidelines missing: [list]. Add: variations, sizes, clear space, incorrect usage examples'

---
## PHASE 5: Brand Asset Generation

**Objective**: Generate brand assets (logos, colors, typography specs)

**HOP Implementation**: `prompts/01_brand_identity_HOP.md` (23KB)
- Section 5: Brand asset generation (AI-ready prompts)
- AI-ready logo prompts (3-5 variations: wordmark, symbol, combination - ≥80 words each)
- Brand mockups creation (business cards, letterhead, social media templates - ≥60 words each)
- Visual asset templates design (presentation slides, document headers, email signatures)
- Brand application examples (website hero, packaging, signage - context-specific)
- Asset validation (prompts detailed ≥60 words with style, color, mood)
- Execution: Uses `$phase_4_output` (visual identity specifications)

**Actions** (implemented in HOP):
1. **Generate AI-ready logo prompts** (3-5 variations: wordmark, symbol, combination - ≥80 words each with style, color, mood)
2. **Create brand mockups**: Business cards, letterhead, social media templates (AI prompts ≥60 words each)
3. **Design visual asset templates**: Presentation slides, document headers, email signatures (specifications + AI prompts)
4. **Produce brand application examples**: Website hero, packaging, signage (context-specific)
5. **Validate assets**: Logo prompts ≥3, mockups ≥5, templates comprehensive, AI prompts detailed (≥60 words)

**Input**:
- `$phase_4_output`
- `$accumulated_context`

**Output**:
- `$generated_content`
- `$metadata`

**Validation**:
- ✅ Logo prompts: 3-5 variations (≥80 words each)
- ✅ Mockups: ≥5 assets (business cards, letterhead, social media)
- ✅ Templates: presentation, document, email (with specifications)
- ✅ All AI prompts detailed (≥60 words with style, color, mood)
- ✅ Brand applications context-appropriate

**Error Handling**:
- If logo_prompts <3 → RETRY: 'Need 3-5 logo variations. Current: [X]. Generate: [suggest missing variations]'
- If AI_prompt_length <60 words → RETRY: 'AI prompt [X] too vague ([Y] words). Add: style details, color specs, mood, technical requirements'
- If mockups <5 → WARN: 'Only [X] mockups generated. Recommend ≥5. Add: [suggest missing asset types]'

---
## PHASE 6: QA & Brand Consistency

**Objective**: Validate brand consistency and create variant applications

**HOP Implementation**: `prompts/01_brand_identity_HOP.md` (23KB)
- Section 6: Brand consistency validation and QA
- Brand consistency checks (positioning ↔ visual, messaging ↔ voice, archetype ↔ values)
- Consistency score calculation (weighted formula: positioning*0.25 + messaging*0.25 + visual*0.25 + voice*0.15 + archetype*0.10)
- Quality thresholds (≥0.85 excellent | 0.70-0.84 good | <0.70 needs improvement)
- Brand applications generation (2-3 variant scenarios: formal/casual, B2B/B2C, print/digital)
- Improvement documentation (if score <0.90: specific issues + concrete fixes)
- Execution: Uses all previous phase outputs (comprehensive brand audit)

**Actions** (implemented in HOP):
1. **Run brand consistency checks**: Positioning aligned with visual identity, messaging consistent with voice, archetype coherent with values
2. **Calculate brand consistency score**: positioning*0.25 + messaging*0.25 + visual*0.25 + voice*0.15 + archetype*0.10
3. **Quality thresholds**: ≥0.85 excellent | 0.70-0.84 good | <0.70 needs improvement
4. **Generate brand applications** (2-3 variant scenarios: formal/casual, B2B/B2C, print/digital)
5. **Document improvement areas** if score <0.90 (specific issues + concrete fixes)

**Input**:
- `$phase_5_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Brand consistency score calculated
- ✅ Score ≥0.85 (excellent) | 0.70-0.84 (good) | <0.70 (needs work)
- ✅ Positioning-visual alignment validated
- ✅ Messaging-voice consistency validated
- ✅ Brand applications generated: 2-3 variant scenarios

**Error Handling**:
- If consistency_score <0.70 → HALT: 'Brand consistency too low ([X]). Critical issues: [list]. Fix before proceeding.'
- If consistency_score 0.70-0.84 → WARN: 'Brand consistency acceptable but suboptimal ([X]). Improvements: [list]. Proceed?'
- If positioning-visual misalignment → RETRY: 'Visual identity doesn't match positioning. Mismatch: [describe]. Adjust: [specific changes]'

---
## PHASE 7: Output Assembly

**Objective**: Compile final brand strategy documentation

**HOP Implementation**: `prompts/main_agent_hop.md` (23KB)
- Trinity output assembly (.md + .llm.json + .meta.json)
- .md file structuring (Brand Strategy Summary → Positioning → Messaging → Visual Identity → Assets → Applications → Guidelines)
- .llm.json generation (structured data: positioning_statement, values, archetype, messaging_pillars, color_palette, typography, logo_guidelines)
- .meta.json generation (workflow metadata: phase breakdown, consistency scores, execution time, brand type)
- Output validation (all 3 files generated, JSON parseable, ≥30 content blocks in .md)
- Execution: Uses `$phase_6_output` (complete brand system + QA results)

**Actions** (implemented in HOP):
1. **Assemble Trinity Output** (.md human-readable + .llm.json structured + .meta.json metadata)
2. **Structure .md file**: Brand Strategy Summary → Positioning → Messaging → Visual Identity → Assets → Applications → Guidelines
3. **Generate .llm.json**: Complete structured data (positioning_statement, values, archetype, messaging_pillars, color_palette, typography, logo_guidelines)
4. **Generate .meta.json**: Workflow metadata (phase breakdown, consistency scores, execution time, brand type)
5. **Validate outputs**: All 3 files generated, JSON parseable, all required sections present (30+ content blocks expected)

**Input**:
- `$phase_6_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ All 3 files generated (.md + .llm.json + .meta.json)
- ✅ .md file has ≥30 content blocks (comprehensive)
- ✅ .llm.json is valid JSON (parseable)
- ✅ .meta.json contains phase breakdown + scores
- ✅ Files saved successfully to output directory

**Error Handling**:
- If validation fails → Report specific issues and halt
- If partial failure → Continue with warnings logged
- If complete failure → Retry once with adjusted parameters, then escalate

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
- ✅ # ✅ Brand Consistency Score: 0.87 (Excellent), brand_strategy.md (30+ blocks) + validation_report.txt generated
- ✅ Quality score ≥0.7
- ✅ Format: json+markdown

### Quality Level
- ✅ 10 validation criteria passed
- ✅ Compliance requirements met (if applicable)

---

## METADATA

**Created**: 2025-11-17
**Updated**: 2025-11-17 (Integrated with HOP prompts)
**Generator**: CODEXA ADW Intelligent Constructor v1.0.0
**Agent**: marca_agent v2.0.0
**Domain**: Brand Strategy (E-commerce & General Business)
**Phases**: 7
**Architecture**: Dual-Layer (ADW ↔ HOP)
**HOP Prompts**: 2 modular prompts (~46KB total)
**Auto-generated**: True (reviewed, validated, and enhanced with HOP integration)

---

**Status**: Production-Ready (Dual-Layer Integrated)
**Maintainer**: CODEXA Meta-Constructor
**Version**: 2.0.0 (ADW + HOP Integration)