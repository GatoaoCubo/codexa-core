# ISO_VECTORSTORE Standard | v1.0.0

**Purpose**: Padrao para iso_vectorstore de todos os agents CODEXA
**Baseline**: anuncio_agent v3.2.0 (-90% token reduction)
**Date**: 2025-11-30

---

## O QUE E ISO_VECTORSTORE

Pacote isolado de arquivos que pode ser:
- Uploaded para qualquer LLM vector store
- Drag-and-drop para ChatGPT, Claude, Gemini, etc.
- Executado sem dependencias externas

**Principio**: Self-contained, portable, LLM-agnostic

---

## ESTRUTURA PADRAO (21 arquivos max)

```
iso_vectorstore/
├── 00_MANIFEST.md           # Package inventory (OBRIGATORIO)
├── 01_QUICK_START.md        # LLM entry point
├── 02_PRIME.md              # Agent identity
├── 03_INSTRUCTIONS.md       # Workflow rules
├── 04_README.md             # Documentation
├── 05_ARCHITECTURE.md       # Tech architecture
├── 06_input_schema.json     # Input validation
├── 07_output_template.md    # Output format
├── 08_{domain}_rules.json   # Domain compliance
├── 09_{domain}_specs.json   # Platform limits
├── 10_{domain}_patterns.json # Domain patterns
├── 11_ADW_orchestrator.md   # Workflow manager
├── 12_execution_plans.json  # Full/Quick plans
├── 13_HOP_main.md           # Parse + orchestrate
├── 14_HOP_{task_1}.md       # Task-specific HOP
├── 15_HOP_{task_2}.md       # Task-specific HOP
├── 16_HOP_{task_3}.md       # Task-specific HOP
├── 17_HOP_{task_4}.md       # Task-specific HOP
├── 18_HOP_qa_validation.md  # QA validation
├── 19_frameworks.md         # Framework reference
└── 20_quality_dimensions.json # Scoring schema
```

---

## LIMITES

### File Count
| Limite | Valor | Motivo |
|--------|-------|--------|
| Maximum | 21 | Vector store compatibility |
| Minimum | 15 | Core functionality |
| HOPs | 6-8 | Task coverage |

### Token Count
| Tipo | Target | Maximum |
|------|--------|---------|
| Total package | < 15,000 | 20,000 |
| Core files (00-05) | ~2,500 | 4,000 |
| Config files (06-10) | ~2,000 | 3,000 |
| Execution (11-12) | ~1,000 | 1,500 |
| Each HOP | 600-1,200 | 1,500 |
| Reference (19-20) | ~600 | 1,000 |

### Version
- Format: semver (MAJOR.MINOR.PATCH)
- Consistency: 100% across all files
- Updated date: ISO-8601

---

## CHUNK SETTINGS (Vector Store)

| Setting | Recommended | Default | Motivo |
|---------|-------------|---------|--------|
| Chunk size | 800 | 4096 | HOPs are ~600-1200 tokens |
| Chunk overlap | 200 | 2048 | Clear section boundaries |

**Rationale**:
- HOPs sao modulos independentes
- Com chunk 4096, multiplos HOPs viram um blob
- Com chunk 800, cada HOP fica isolado para retrieval preciso

---

## CATEGORIAS DE ARQUIVOS

### Core (00-05)
| File | Purpose | Token Target |
|------|---------|--------------|
| 00_MANIFEST.md | Inventory, deploy checklist | ~400 |
| 01_QUICK_START.md | LLM navigation guide | ~600 |
| 02_PRIME.md | Agent identity, 12 pillars | ~500 |
| 03_INSTRUCTIONS.md | Workflow rules | ~400 |
| 04_README.md | Full documentation | ~300 |
| 05_ARCHITECTURE.md | Technical architecture | ~500 |

### Config (06-10)
| File | Purpose | Format |
|------|---------|--------|
| 06_input_schema.json | Input validation | JSON Schema |
| 07_output_template.md | Output format | Markdown |
| 08_{domain}_rules.json | Compliance rules | JSON |
| 09_{domain}_specs.json | Platform limits | JSON |
| 10_{domain}_patterns.json | Domain patterns | JSON |

### Execution (11-12)
| File | Purpose |
|------|---------|
| 11_ADW_orchestrator.md | Workflow manager, phase control |
| 12_execution_plans.json | Full/Quick execution plans |

### HOPs (13-18)
| File | Purpose | Token Target |
|------|---------|--------------|
| 13_HOP_main.md | Parse input, orchestrate | ~800 |
| 14-17_HOP_{task}.md | Task-specific generation | 600-1200 |
| 18_HOP_qa_validation.md | Quality validation | ~800 |

### Reference (19-20)
| File | Purpose |
|------|---------|
| 19_frameworks.md | Framework reference (StoryBrand, etc) |
| 20_quality_dimensions.json | Scoring schema |

---

## HOP STRUCTURE (Optimized)

```markdown
# HOP {NUMBER}: {NAME} | {agent_name} v{VERSION}

**Purpose**: {one-line description}
**Scope**: {scope} | **Output**: {output description}

---

## INPUT
- {input_1}
- {input_2}

---

## RULES
1. {critical_rule_1}
2. {critical_rule_2}

### FAZER
- {do_1}
- {do_2}

### EVITAR
- {avoid_1}
- {avoid_2}

---

## STEPS
1. {step_1}
2. {step_2}
3. {step_3}

---

## OUTPUT FORMAT

```
{example_output}
```

---

## VALIDATION
- [ ] {check_1}
- [ ] {check_2}

---

**HOP**: {number} | **Agent**: {agent_name} | **Version**: {VERSION}
**Tokens**: ~{count} (optimized)
```

---

## GARBAGE PATTERNS (TO REMOVE)

### YAML Injection
```regex
/^---\n[\s\S]*?^---/m
```

### Duplicate Metadata
```regex
/Version:.*\nVersion:/
/Updated:.*\nUpdated:/
```

### Cross-Agent Injection
```regex
/mentor_agent|pesquisa_agent|photo_agent/ (in wrong agent)
```

### Empty Sections
```regex
/<reasoning>\s*<\/reasoning>/
/## [A-Z]+\n\n##/
```

### Massive Examples
```regex
/```[\s\S]{3000,}```/
```

---

## SCOPE DEFINITIONS

### TEXT-ONLY
```yaml
generates:
  - titulos
  - descricao
  - bullets
  - keywords
delegates:
  - image_prompts → photo_agent
  - video_scripts → video_agent
out_of_scope:
  - HOP_image_*
  - HOP_video_*
  - visual_*
```

### VISUAL
```yaml
generates:
  - image_prompts
  - photo_specs
  - visual_guidelines
delegates:
  - text_copy → anuncio_agent
out_of_scope:
  - HOP_titulo_*
  - HOP_descricao_*
  - copy_rules
```

### RESEARCH
```yaml
generates:
  - research_notes
  - competitor_analysis
  - market_data
delegates:
  - ad_copy → anuncio_agent
  - visuals → photo_agent
out_of_scope:
  - HOP_titulo_*
  - HOP_bullet_*
```

---

## DEPLOY CHECKLIST

### Pre-Deploy
- [ ] File count <= 21
- [ ] Token estimate < 15,000
- [ ] Version consistency 100%
- [ ] MANIFEST present
- [ ] SYSTEM_INSTRUCTIONS present
- [ ] All HOPs < 1,500 tokens

### Vector Store Setup
- [ ] Create vector store
- [ ] Set chunk size: 800
- [ ] Set chunk overlap: 200
- [ ] Upload all files

### Agent Builder Setup
- [ ] Copy SYSTEM_INSTRUCTIONS
- [ ] Enable File Search
- [ ] Enable Code Interpreter (if applicable)
- [ ] Configure Web Search (optional)

### Verification
- [ ] Test with sample input
- [ ] Verify output format
- [ ] Check QA scoring
- [ ] Confirm copyable content works

---

## QUALITY METRICS

### File Quality
| Metric | Target |
|--------|--------|
| File count | <= 21 |
| Token estimate | < 15,000 |
| Version consistency | 100% |

### HOP Quality
| Metric | Target |
|--------|--------|
| Tokens per HOP | < 1,500 |
| Essential instructions | Preserved |
| Garbage content | 0% |

### Deploy Quality
| Metric | Target |
|--------|--------|
| MANIFEST present | Yes |
| SYSTEM_INSTRUCTIONS present | Yes |
| Chunk settings correct | Yes |

---

## RELATED RESOURCES

- **ADW-104**: ISO_VECTORSTORE_OPTIMIZATION workflow
- **Templates**: `codexa_agent/templates/iso_vectorstore/`
- **Baseline**: `anuncio_agent/iso_vectorstore/` (v3.2.0)

---

**Version**: 1.0.0 | **Status**: Production Standard
**Baseline**: anuncio_agent v3.2.0 (-90% token reduction)
**Author**: codexa_agent
