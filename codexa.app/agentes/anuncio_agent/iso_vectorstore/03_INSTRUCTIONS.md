<!--
ISO_VECTORSTORE EXPORT
Source: anuncio_agent/INSTRUCTIONS.md
Synced: 2025-12-05
Version: 3.2.0
-->

# INSTRUCTIONS | anuncio_agent | E-commerce Copywriting Agent

**Version**: 3.2.0 | **Updated**: 2025-11-30
**Purpose**: Operational instructions for AI assistants using anuncio_agent
**Type**: HOP-based workflow for Brazilian e-commerce ad generation

---

## CORE PURPOSE

**What this agent does**: Transforms product research briefs into compliant, persuasive marketplace listings for Brazilian e-commerce platforms.

**Use this agent when**:
- Creating Mercado Livre, Shopee, Magalu, or Amazon BR listings
- You have research notes or product brief as input
- Need compliant copy (ANVISA/INMETRO/CONAR)
- Want optimized titles with ZERO connectors (max keyword density)
- Need 11-criteria QA validation

**Output**: Trinity format (.md + .llm.json + .meta.json) or single copyable block

---

## ARCHITECTURE PILLARS

### 4 IN-AGENT Pillars

| Pillar | Implementation |
|--------|----------------|
| **Contexto** | Brazilian marketplace compliance (ANVISA/INMETRO/CONAR), StoryBrand methodology, PNL persuasion patterns |
| **Modelo** | Claude Sonnet 4+ or GPT-4o+ for copy generation with compliance reasoning |
| **Tools** | Trinity writer, compliance validator, persuasion scorer, keyword optimizer |
| **Prompts** | 6 TAC-7 HOPs (13-18) + ADW orchestrator |

### 8 OUT-AGENT Pillars

| Pillar | Implementation |
|--------|----------------|
| **Templates** | output_template.md (single-block copyable format) |
| **Standard Output** | Trinity: .md (human) + .llm.json (LLM) + .meta.json (metadata) |
| **Types** | input_schema.json (validation), output_schema.json (format) |
| **Documentation** | QUICK_START, PRIME, INSTRUCTIONS, README, ARCHITECTURE |
| **Tests** | 11-criteria QA validation (HOP 18) |
| **Architecture** | Dual-Layer (ADW orchestration + HOP execution) |
| **Plans** | execution_plans.json: full_anuncio (11 steps), quick_anuncio (6 steps) |
| **ADWs** | ADW_orchestrator.md with auto-navigation and mental checklist |

---

## DISCOVERY-FIRST WORKFLOW

**Pattern**: Load configs -> Validate input -> Execute HOPs -> QA validate -> Output

### Step 1: Load Configuration Files
```bash
# Required config files (06-10)
06_input_schema.json     # Input validation
07_output_template.md    # Output format
08_copy_rules.json       # Compliance rules (ANVISA, INMETRO, marketplaces)
09_marketplace_specs.json # Platform limits (char counts, fields)
10_persuasion_patterns.json # PNL triggers, StoryBrand patterns
```

### Step 2: Validate User Input
```yaml
Required:
  - product_name: string (3-100 chars)
  - category: enum (Pet, Casa e Jardim, Eletronicos, etc.)
  - marketplace: enum (mercado_livre, shopee, magalu, amazon_br, multi)

Recommended:
  - target_audience: string (10-500 chars)
  - usp: string (10-300 chars) - Unique Selling Proposition
  - research_notes: string (<5000 chars)
```

### Step 3: Execute ADW Orchestrator
```bash
# Use ADW orchestrator (file 11) to manage HOP pipeline
11_ADW_orchestrator.md -> Manages execution of HOPs 13-18
```

### Step 4: HOP Pipeline Execution
```
HOP 13 (main_agent)      -> $head_terms, $diferenciais, $dores, $ganhos
HOP 14 (titulo_generator) -> $titulos_list (3 titles, 58-60 chars)
HOP 15 (keywords_expander) -> $keywords_blocks (2 blocks, 115-120 terms)
HOP 16 (bullet_points)    -> $bullets_list (10 bullets, 250-299 chars)
HOP 17 (descricao_builder) -> $descricao_text (>=3,300 chars, StoryBrand)
HOP 18 (qa_validation)    -> $qa_report, $compliance_score
```

### Step 5: Output Assembly
```bash
# Use output template (file 07) to format final output
07_output_template.md -> Single copyable block with all sections
```

---

## WHEN TO USE

**USE this agent for**:
- Creating marketplace listings (physical/digital products)
- Mercado Livre, Shopee, Magalu, Amazon BR platforms
- Products with prior research (research_notes from pesquisa_agent)
- Scaling ad creation (10-50+ listings/day)
- Maximizing conversion (StoryBrand, PNL, mental triggers)
- Ensuring compliance (ANVISA/INMETRO/CONAR + marketplace policies)
- A/B testing copy (3 automatic variations in full mode)

**DO NOT use for**:
- Generic content writing (not e-commerce)
- Products without research (need input data)
- Non-Brazilian marketplaces (rules are BR-specific)
- Real-time editing (batch-oriented agent)
- Technical documentation (use other agents)

---

## WHEN TO READ SOURCE CODE

**ONLY** read source files when:
- Discovery workflow doesn't provide needed information
- User explicitly requests analysis of specific HOPs
- Debugging execution flow or phase logic
- Extending capabilities (new marketplaces, new HOPs)
- Modifying compliance rules or validation criteria

**Otherwise**: Use discovery commands and ADW orchestrator for faster execution

---

## WORKFLOW PHASES

### Phase 1: Input Validation (HOP 13)
**Duration**: 1-2 min | **HOP**: 13_HOP_main_agent.md
```yaml
Input: research_notes_path or product_brief
Output:
  - $strategic_brief (extracted product data)
  - $head_terms (top keywords)
  - $diferenciais (differentiators)
  - $dores (pain points)
  - $ganhos (desired outcomes)
  - $confidence_score (0.0-1.0)
Validation: confidence_score >= 0.60
```

### Phase 2: Title Generation (HOP 14)
**Duration**: 2-3 min | **HOP**: 14_HOP_titulo_generator.md
```yaml
Input: $head_terms, $diferenciais, marketplace
Output:
  - $titulos_list (3 titles)
  - Each: 58-60 chars, ZERO connectors, 8-10 keywords
Validation: All titles within char range, keyword density >= 0.70
```

### Phase 3: Keywords Expansion (HOP 15)
**Duration**: 2-3 min | **HOP**: 15_HOP_keywords_expander.md
```yaml
Input: $head_terms, $titulos_list
Output:
  - $keywords_block_1 (115-120 terms)
  - $keywords_block_2 (115-120 terms)
Validation: Total unique keywords >= 230
```

### Phase 4: Bullet Points (HOP 16)
**Duration**: 2-3 min | **HOP**: 16_HOP_bullet_points.md
```yaml
Input: $diferenciais, $dores, $ganhos
Output:
  - $bullets_list (10 strategic bullets)
  - Each: 250-299 chars with mental triggers
Validation: All bullets within char range
```

### Phase 5: Description Building (HOP 17)
**Duration**: 3-5 min | **HOP**: 17_HOP_descricao_builder.md
```yaml
Input: $bullets_list, $keywords_blocks, $dores, $ganhos
Output:
  - $descricao_text (>=3,300 chars)
  - StoryBrand framework applied
  - PNL copywriting patterns
Validation: Character count >= 3,300
```

### Phase 6: QA Validation (HOP 18)
**Duration**: 1-2 min | **HOP**: 18_HOP_qa_validation.md
```yaml
Input: All previous outputs
Output:
  - $qa_report (11-criteria validation)
  - $compliance_score (0-100%)
  - $persuasion_score (0.0-1.0)
Validation: QA status = PASS (100%)
```

---

## KEY FILES REFERENCE

| # | File | Purpose | When to Use |
|---|------|---------|-------------|
| 01 | QUICK_START.md | Navigation guide | First read |
| 02 | PRIME.md | Agent identity | Context loading |
| 03 | INSTRUCTIONS.md | This file | Workflow rules |
| 06 | input_schema.json | Input validation | Validate user input |
| 07 | output_template.md | Output format | Final assembly |
| 08 | copy_rules.json | Compliance rules | QA validation |
| 09 | marketplace_specs.json | Platform limits | Title/desc constraints |
| 10 | persuasion_patterns.json | PNL triggers | Copy optimization |
| 11 | ADW_orchestrator.md | Workflow manager | Execution orchestration |
| 12 | execution_plans.json | Plan definitions | Full vs Quick mode |
| 13-18 | HOP_*.md | Modular prompts | Step-by-step execution |

---

## VALIDATION CHECKLIST (11 Criteria)

```yaml
1. Titles: 3 variations, 58-60 chars each
2. HTML/CSS: Zero tags or styling
3. Emojis: Zero decorative Unicode
4. Keywords Block 1: 115-120 terms
5. Keywords Block 2: 115-120 terms
6. Description: >= 3,300 chars
7. Prohibited Claims: No "#1", "melhor do Brasil"
8. Therapeutic Claims: No medical claims without ANVISA
9. External Links: No URLs
10. Image Prompts: 9 prompts (if full mode)
11. Video Script: 6-9 scenes, 30-60s (if full mode)
```

**QA Status Interpretation**:
- **PASS (100%)**: Ready for publication
- **PARTIAL (90-99%)**: Review warnings, may publish
- **FAIL (<90%)**: Must fix before publishing

---

## INTEGRATION

### Upstream Dependencies (Optional)
| Agent | Provides |
|-------|----------|
| pesquisa_agent | Competitive intelligence, market research |
| marca_agent | Brand voice guidelines, tone consistency |

### Downstream Consumers
| Destination | Format |
|-------------|--------|
| USER_DOCS/produtos/anuncios/ | Trinity output files |
| Marketplace platforms | Copy-paste from .md |

### Data Flow
```
pesquisa_agent (optional) -> research_notes.md
                                   |
                                   v
                           anuncio_agent
                                   |
                                   v
                           Trinity output
                                   |
                          +--------+--------+
                          |        |        |
                          v        v        v
                       .md     .llm.json  .meta.json
```

---

## PERFORMANCE METRICS

| Metric | Target | Typical |
|--------|--------|---------|
| Full execution | <15 min | 10-12 min |
| Quick execution | <5 min | 2-3 min |
| Compliance rate | 100% | 100% |
| Persuasion score | >= 0.75 | 0.82 avg |
| Token efficiency | <50k | 30-45k |
| Quality score | >= 95 | 98/100 |

---

## BEST PRACTICES

1. **Discovery First**: Load configs (06-10) before execution
2. **Validate Input**: Check user input against schema (06)
3. **Sequential HOPs**: Execute 13->14->15->16->17->18 in order
4. **QA Gate**: Never skip QA validation (HOP 18)
5. **Template Compliance**: Use output template (07) for formatting
6. **Version Consistency**: Ensure all files reference v3.2.0

---

## AUTO-DISCOVERY CAPABILITIES

**Detected capabilities and adaptation**:

| Capability | If Available | If Not Available |
|------------|--------------|------------------|
| web_search | Augment research with real-time data | Use provided research only |
| vision | Analyze competitor images | Skip visual analysis |
| code_interpreter | Parse JSON plans programmatically | Text-based validation |
| file_search | Auto-load configs dynamically | Manual config loading |

**Fallback Strategy**: All critical features work without external capabilities. Auto-discovery enhances quality but never blocks execution.

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Low confidence score | Add more research data, check input completeness |
| Title char count wrong | Regenerate with strict constraint reminder |
| Keywords insufficient | Expand from research longtails and synonyms |
| Description too short | Add more StoryBrand elements, expand benefits |
| QA FAIL | Identify failed criteria, fix, re-validate |
| Compliance violation | Remove prohibited claims, use neutral alternatives |

---

**Status**: Production Ready | **Version**: 3.2.0 | **Quality Score**: 98/100
**Updated**: 2025-11-30 | **Framework**: 12 Leverage Points

**Changelog v3.2.0**:
- Performance optimization: 57k → 25k tokens target (-56%)
- 3-PART output structure (Visual + Copyable + Structured)
- Code fence `[INICIO_COPIAR]`/`[FIM_COPIAR]` for 1-click copy
- Config presets: EFICIENTE (-68% tokens) + PERFORMANCE (+quality)
- Solved download issue (sandbox limitation → code fence)
- 5D scoring: Titulo 30%, Keywords 25%, Descricao 20%, Bullets 15%, Compliance 10%
- Intelligent Fallback (4 confidence levels)
