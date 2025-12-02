# 100_ADW_RUN_MENTOR | Mentor Agent Execution Workflow

**Purpose**: End-to-end execution workflow for mentor_agent
**Type**: 6-Phase ADW | **Duration**: ~16-31min
**Output**: .md files ONLY (NO subfolders) (json+markdown)
**Architecture**: Dual-Layer (ADW Orchestration ↔ HOP Execution)
**Status**: Production-Ready (Integrated with HOP prompts v2.0.0)

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_run_mentor",
  "workflow_name": "Mentor Agent Execution",
  "agent": "mentor_agent",
  "version": "2.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop_and_report",
  "min_llm_model": "gpt-4+ or claude-sonnet-4+",
  "required_capabilities": {
    "compliance validation": true
  },
  "phases": [
    {
      "phase_id": "phase_1_discovery_&_scout",
      "phase_name": "Discovery & Scout",
      "duration": "2-5min",
      "description": "Search knowledge catalog and identify relevant resources"
    },
    {
      "phase_id": "phase_2_knowledge_synthesis",
      "phase_name": "Knowledge Synthesis",
      "duration": "3-7min",
      "description": "Extract actionable insights and translate to seller language"
    },
    {
      "phase_id": "phase_3_assessment",
      "phase_name": "Assessment",
      "duration": "3-7min",
      "description": "Evaluate current state, gaps, and opportunities"
    },
    {
      "phase_id": "phase_4_action_planning",
      "phase_name": "Action Planning",
      "duration": "3-7min",
      "description": "Create customized step-by-step plan"
    },
    {
      "phase_id": "phase_5_guidance_&_resources",
      "phase_name": "Guidance & Resources",
      "duration": "3-7min",
      "description": "Provide strategic recommendations and tools"
    },
    {
      "phase_id": "phase_6_output_assembly",
      "phase_name": "Output Assembly",
      "duration": "2-5min",
      "description": "Compile mentoring response and next steps"
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
   - `config/categorias_conhecimento.json`
   - `config/seller_language_guide.json`

2. **Capabilities Available**:
   - LLM: gpt-4+ or claude-sonnet-4+
   - Tools: compliance validation

3. **User Input Ready**:
   - raw files (PDFs, videos

---

## ARCHITECTURE: DUAL-LAYER INTEGRATION (ADW ↔ HOP)

This workflow implements a **Dual-Layer Architecture** where:

### **LAYER 1: ADW (Adaptive Dual-layer Workflow)**
- **Purpose**: High-level orchestration and coordination
- **This file**: Defines phases, sequencing, validation, error handling
- **Role**: "What to do" and "When to do it"

### **LAYER 2: HOP (Hyper-Optimized Prompts)**
- **Purpose**: Detailed execution and domain-specific implementation
- **Location**: `prompts/` directory (8 modular prompts, ~100KB total)
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
| 1 | `scout_internal.md` | 11K | Internal knowledge catalog search (PROCESSADOS/catalogo.json) |
| 1 | `scout_global_navigator_HOP.md` | 12K | Global resource navigation & semantic search |
| 2 | `knowledge_processor_HOP.md` | 18K | Insight extraction & seller language translation (WHEN/HOW/WHAT) |
| 3 | `quality_validator_5d_HOP.md` | 21K | 5D quality assessment (current state, gaps, opportunities, risks, priorities) |
| 4 | `mentor_orchestrator.md` | 14K | Action planning (immediate/short/long-term with checkpoints) |
| 5 | `strategic_advisor.md` | 6.2K | Strategic recommendations & expert tips |
| 5 | `tactical_reports.md` | 6.5K | Tools, templates & practical resources |
| 6 | `aula_builder.md` | 11K | Mentoring response assembly (summary + plan + resources + next steps) |

**Total HOP library**: 8 prompts, ~100KB of specialized mentoring knowledge

---

## PHASE 1: Discovery & Scout

**Objective**: Search knowledge catalog and identify relevant resources

**HOP Implementation**:
- `prompts/scout_internal.md` (11K) - Internal knowledge catalog search
- `prompts/scout_global_navigator_HOP.md` (12K) - Global resource navigation
- Combined execution: scout_internal searches PROCESSADOS/catalogo.json → scout_global_navigator performs semantic ranking
- Execution: Load HOP prompts with `$user_input` (seller question/context)

**Actions** (implemented in HOP):
1. **Parse seller question/context**: Extract intent, topic, urgency level
2. **Search knowledge catalog** (`PROCESSADOS/catalogo.json`): Semantic search on categoria + assunto + tags + aplicacao
3. **Rank results**: Multi-dimensional matching (relevance score ≥0.60)
4. **Read top 3-5 knowledge files**: Load from `PROCESSADOS/[arquivo].md`
5. **Identify knowledge gaps**: Flag areas where catalog lacks coverage

**Input**:
- `$user_input`
- `$config_files`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Knowledge catalog searched successfully
- ✅ ≥3 relevant knowledge files found (relevance ≥0.60)
- ✅ Top results read and parsed
- ✅ Knowledge gaps identified (if any)

**Error Handling**:
- If catalog search fails → HALT: 'Knowledge catalog not accessible. Check PROCESSADOS/catalogo.json exists.'
- If <3 results found → WARN: 'Limited knowledge ([X] results). Consider: (1) Broaden search terms, (2) Add to knowledge base, (3) Provide general guidance.'
- If relevance_score <0.60 → WARN: 'Low relevance matches. Best: [X]. Proceeding with available knowledge but answer may be partial.'

---
## PHASE 2: Knowledge Synthesis

**Objective**: Extract actionable insights and translate to seller language

**HOP Implementation**: `prompts/knowledge_processor_HOP.md` (18K)
- Actionable insight extraction (WHEN/HOW/WHAT framework)
- Technical → Practical translation (Brazilian e-commerce context)
- Priority structuring (high-impact first, quick wins highlighted)
- Context examples (Mercado Livre, Shopee scenarios)
- Execution: Uses `$phase_1_output` (top 3-5 knowledge files)

**Actions** (implemented in HOP):
1. **Extract actionable insights**: WHEN to use (context detection) + HOW to apply (steps) + WHAT to do (concrete actions)
2. **Translate to seller language**: Technical → Practical (Brazilian e-commerce context)
3. **Structure by priority**: High-impact actions first, quick wins highlighted
4. **Add context examples**: Real marketplace scenarios (Mercado Livre, Shopee, etc.)
5. **Validate synthesis**: Insights ≥3, all actionable, no jargon

**Input**:
- `$phase_1_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ ≥3 actionable insights extracted
- ✅ All insights translated to seller language (no jargon)
- ✅ WHEN + HOW + WHAT structure complete
- ✅ Context examples added

**Error Handling**:
- If insights <3 → RETRY: 'Only [X] insights extracted. Analyze deeper: Look for implicit recommendations, compare approaches, identify patterns.'
- If jargon detected → RETRY: 'Technical terms found: [list]. Translate to seller language: [examples]'
- If WHEN/HOW/WHAT incomplete → RETRY: 'Missing: [component]. Add: context conditions (WHEN), step-by-step process (HOW), concrete deliverables (WHAT).'

---
## PHASE 3: Assessment

**Objective**: Evaluate current state, gaps, and opportunities

**HOP Implementation**: `prompts/quality_validator_5d_HOP.md` (21K)
- 5D assessment framework (current state, skill gaps, opportunities, risks, impact prioritization)
- ROI potential scoring (high/medium/low)
- Compliance & platform dependency risk analysis
- Gap identification (≥2 skill gaps required)
- Execution: Uses `$phase_2_output` (actionable insights)

**Actions** (implemented in HOP):
1. **Evaluate current state**: Seller's experience level, resources, constraints
2. **Identify skill gaps**: Compare current vs. required capabilities
3. **Map opportunities**: Quick wins, strategic initiatives, long-term investments
4. **Assess risks**: Common pitfalls, compliance issues, resource bottlenecks
5. **Prioritize by impact**: ROI potential (high/medium/low)

**Input**:
- `$phase_2_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Current state evaluated
- ✅ Skill gaps identified (≥2)
- ✅ Opportunities mapped by priority (high/medium/low)
- ✅ Risks assessed

**Error Handling**:
- If skill_gaps <2 → RETRY: 'Need ≥2 skill gaps. Current: [X]. Consider: technical skills, marketplace knowledge, operational capacity, marketing skills.'
- If risks not assessed → WARN: 'No risks identified. Common risks: compliance, cashflow, competition, platform dependency. Add risk assessment.'

---
## PHASE 4: Action Planning

**Objective**: Create customized step-by-step plan

**HOP Implementation**: `prompts/mentor_orchestrator.md` (14K)
- Step-by-step plan creation (≥5 actionable steps with time estimates)
- Timeframe structuring (immediate 0-7 days, short-term 1-4 weeks, long-term 1-3 months)
- Prerequisites mapping (tools, skills, resources, budget)
- Success checkpoints (metrics per milestone)
- Alternative paths (Plan A + Plan B for resource constraints)
- Execution: Uses `$phase_3_output` (assessment & gaps)

**Actions** (implemented in HOP):
1. **Create step-by-step plan**: Numbered actions with time estimates
2. **Structure plan**: Immediate (0-7 days) + Short-term (1-4 weeks) + Long-term (1-3 months)
3. **Add prerequisites**: What seller needs before starting each step
4. **Include checkpoints**: Success metrics for each milestone
5. **Provide alternatives**: Plan A + Plan B (if resource constraints)

**Input**:
- `$phase_3_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Step-by-step plan created (≥5 actionable steps)
- ✅ Plan structured by timeframe (immediate + short + long)
- ✅ Prerequisites listed for each step
- ✅ Success checkpoints defined

**Error Handling**:
- If steps <5 → RETRY: 'Plan too brief ([X] steps). Need ≥5 actionable steps. Break down: [suggest subdivisions]'
- If no timeframes → RETRY: 'Add timeframes: Immediate (0-7 days), Short-term (1-4 weeks), Long-term (1-3 months).'
- If prerequisites missing → WARN: 'No prerequisites listed. Add what seller needs: tools, skills, resources, budget.'

---
## PHASE 5: Guidance & Resources

**Objective**: Provide strategic recommendations and tools

**HOP Implementation**:
- `prompts/strategic_advisor.md` (6.2K) - Strategic recommendations & expert tips
- `prompts/tactical_reports.md` (6.5K) - Tools, templates & practical resources
- Combined execution: strategic_advisor provides high-level guidance → tactical_reports delivers actionable tools/templates
- Execution: Uses `$phase_4_output` (action plan)

**Actions** (implemented in HOP):
1. **Recommend tools**: Specific marketplace features, free/paid tools, automations
2. **Provide templates**: Copy-paste ready content (descriptions, responses, etc.)
3. **Link resources**: Relevant knowledge files, external guides, video tutorials
4. **Add expert tips**: Pro shortcuts, common mistakes to avoid
5. **Suggest next learning**: What to study next for continuous improvement

**Input**:
- `$phase_4_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ ≥3 tools/resources recommended
- ✅ Templates provided (if applicable)
- ✅ Expert tips included (≥2)
- ✅ Next learning steps suggested

**Error Handling**:
- If resources <3 → RETRY: 'Only [X] resources provided. Need ≥3. Add: tools, templates, guides, courses.'
- If no expert tips → WARN: 'No expert tips included. Add: shortcuts, common mistakes, pro insights.'

---
## PHASE 6: Output Assembly

**Objective**: Compile mentoring response and next steps

**HOP Implementation**: `prompts/aula_builder.md` (11K)
- Mentoring response assembly (summary + plan + resources + next steps)
- Readability formatting (bullet points, numbered lists, clear headers)
- Metadata generation (response_id, confidence_score, knowledge_sources_used)
- Completeness validation
- Conversation logging (feedback loop)
- Execution: Uses `$phase_5_output` (guidance & resources)

**Actions** (implemented in HOP):
1. **Structure response**: Summary (2-3 sentences) + Action Plan (steps) + Resources (tools/links) + Next Steps
2. **Format for readability**: Bullet points, numbered lists, clear headers
3. **Add metadata**: Response_id, confidence_score, knowledge_sources_used
4. **Validate completeness**: Answer addresses question, plan is actionable, resources are relevant
5. **Save conversation**: Log for feedback loop and continuous improvement

**Input**:
- `$phase_5_output`
- `$accumulated_context`

**Output**:
- `$phase_output`
- `$status`

**Validation**:
- ✅ Response structured (summary + plan + resources + next steps)
- ✅ Formatted for readability
- ✅ Metadata added (response_id, confidence, sources)
- ✅ Completeness validated

**Error Handling**:
- If structure incomplete → RETRY: 'Missing sections: [list]. Required: Summary + Action Plan + Resources + Next Steps.'
- If metadata missing → WARN: 'No metadata. Add: response_id, confidence_score, sources_used.'

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
- ✅ All 6 phases completed
- ✅ Duration within target
- ✅ No validation failures

### Output Level
- ✅ .md files ONLY (NO subfolders) generated
- ✅ Quality score ≥0.87
- ✅ Format: json+markdown

### Quality Level
- ✅ 5 validation criteria passed
- ✅ Compliance requirements met (if applicable)

---

## METADATA

**Created**: 2025-11-17
**Updated**: 2025-11-17 (Integrated with HOP prompts)
**Generator**: CODEXA ADW Intelligent Constructor v1.0.0
**Agent**: mentor_agent v2.0.0
**Domain**: E-commerce Mentoring (Brazilian Marketplace Sellers)
**Phases**: 6
**Architecture**: Dual-Layer (ADW ↔ HOP)
**HOP Prompts**: 8 modular prompts (~100KB total)
**Auto-generated**: True (reviewed, validated, and enhanced with HOP integration)

---

**Status**: Production-Ready (Dual-Layer Integrated)
**Maintainer**: CODEXA Meta-Constructor
**Version**: 2.5.0 (12 Leverage Points Upgrade)
**Plans**: See 12_execution_plans.json for full/quick modes