# PRIME Command - ADW Workflow Executor

Execute um workflow ADW (Agentic Developer Workflow) completo de ponta a ponta.

## Usage

```bash
/prime {agent_name} [user_input]
```

## Available Agents

### Tier 1: Content Production (ADW Workflows)
| Agent | Domain | Phases | Duration | Command |
|-------|--------|--------|----------|---------|
| `pesquisa` | Market Research | 10 | 20-30min | `/prime-pesquisa` |
| `anuncio` | Ad Generation | 8 | 23-38min | `/prime-anuncio` |
| `mentor` | E-commerce Mentoring | 7 | 16-31min | `/prime-mentor` |
| `marca` | Brand Strategy | 8 | 21-36min | `/prime-marca` |
| `photo` | AI Photography | 5 | 15-30min | `/prime-photo` |
| `video` | Video Production | 10 | 25-45min | `/prime-video` |
| `curso` | Course Building | 3 | 30-60min | `/prime-curso` |

### Tier 2: System & Infrastructure
| Agent | Domain | Type | Command |
|-------|--------|------|---------|
| `codexa` | Meta-Construction | Builder | `/prime-codexa` |
| `scout` | File Navigation | MCP Server | `/prime-scout` |
| `voice` | Voice Interface | MCP Server | `/prime-voice` |

### Not Yet Available (No /prime-* command)
- `persona` - Persona generation (use via codexa_agent)
- `qa` - Quality assurance (use via codexa_agent)

## Execution Steps

### Step 1: Load Context

Read the following files in order:

1. **PRIME.md**: `codexa.app/agentes/{agent_name}_agent/PRIME.md`
2. **ADW Workflow**: `codexa.app/agentes/{agent_name}_agent/workflows/100_ADW_RUN_{AGENT}.md`
3. **Config Files**: `codexa.app/agentes/{agent_name}_agent/config/*.json` (all)

### Step 2: Parse User Input

**For pesquisa_agent**:
- Expect: Product name, category, target audience, price range (BRL)
- Example: "Garrafa térmica, categoria: casa e cozinha, público: 25-45 anos fitness, preço: R$ 50-150"

**For anuncio_agent**:
- Expect: Path to research notes or research data
- Example: "USER_DOCS/produtos/research/garrafa_termica_research_notes.md"

**For mentor_agent**:
- Expect: Seller question/problem
- Example: "Como melhorar minhas fotos de produto no Mercado Livre?"

**For marca_agent**:
- Expect: Business brief (mission, vision, values, product, audience)
- Example: "Marca de garrafas térmicas sustentáveis, missão: reduzir plástico descartável..."

**For photo_agent**:
- Expect: Subject + style
- Example: "subject=Garrafa térmica, style=minimalist"

**For video_agent**:
- Expect: Subject + format + duration
- Example: "subject=Garrafa térmica, format=reels, duration=30s"

**For curso_agent**:
- Expect: Course topic + target audience + format
- Example: "topic=E-commerce para iniciantes, audience=MEIs, format=hotmart"

**For codexa_agent**:
- Expect: Build type (agent/prompt/command/mcp/schema)
- Example: "build-agent: novo agente de email marketing"

**For scout_agent**:
- Expect: Discovery query or file pattern
- Example: "find all ADW workflows" or "**/*_HOP.md"

**For voice_agent**:
- Expect: Voice command or configuration
- Example: "start listening" or "configure elevenlabs"

### Step 3: Execute Workflow

Follow the phases defined in `100_ADW_RUN_{AGENT}.md`:

```
For each phase (1 → 2 → ... → N):
  1. Announce phase start: "🔄 Phase {N}: {Phase Name}"

  2. Load HOP Implementation:
     - Read the HOP prompt file specified in "HOP Implementation" section
     - Example: agentes/{agent}_agent/prompts/{hop_file}.md

  3. Execute HOP Instructions:
     - Follow step-by-step instructions in HOP prompt
     - Use examples and templates provided
     - Apply validation checklists

  4. Validate Outputs:
     - Check against "Validation" criteria in ADW phase
     - If validation fails → apply "Error Handling" strategy
     - If validation passes → proceed to next phase

  5. Report phase completion: "✅ Phase {N} completed"
```

### Step 4: Generate Final Output

Based on agent type:

**pesquisa_agent**:
- `user_research/{product_name}_research_notes.md` (22 blocks)
- `user_research/{product_name}_metadata.json`
- `user_research/{product_name}_queries.json`

**anuncio_agent**:
- `USER_DOCS/anuncios/{product_name}/{product_name}_ad_copy.md`
- `USER_DOCS/anuncios/{product_name}/{product_name}_ad_copy.llm.json`
- `USER_DOCS/anuncios/{product_name}/{product_name}_ad_copy.meta.json`

**mentor_agent**:
- Mentoring response (markdown format)
- Summary + Action Plan + Resources + Next Steps

**marca_agent**:
- `USER_DOCS/marcas/{brand_name}/brand_strategy.md` (30+ blocks)
- `USER_DOCS/marcas/{brand_name}/validation_report.txt`
- Brand consistency score

**photo_agent**:
- `USER_DOCS/photos/{product_name}/photo_prompts.md` (9 individual + 1 batch)
- `USER_DOCS/photos/{product_name}/photo_prompts.llm.json`
- `USER_DOCS/photos/{product_name}/photo_prompts.meta.json`

**video_agent**:
- `USER_DOCS/videos/{product_name}/video_script.md`
- `USER_DOCS/videos/{product_name}/storyboard.md`
- `USER_DOCS/videos/{product_name}/video.meta.json`

**curso_agent**:
- `USER_DOCS/cursos/{course_name}/outline.md`
- `USER_DOCS/cursos/{course_name}/scripts/*.md`
- `USER_DOCS/cursos/{course_name}/workbook.md`

**codexa_agent**:
- New agent/prompt/command files in appropriate directories
- Validation reports in `outputs/`

**scout_agent**:
- File discovery results (in-memory, not saved)
- Path validation reports

**voice_agent**:
- Voice transcriptions (in-memory or logged)
- Audio files (if TTS enabled)

### Step 5: Report Completion

```
========================================
{AGENT_NAME} WORKFLOW COMPLETED
========================================

Duration: {actual_minutes}min (target: {min}-{max}min)
Quality Score: {score}/1.0 ({EXCELLENT|GOOD|ACCEPTABLE})

Generated Assets:
- {asset_1}
- {asset_2}
- ...

Files Saved:
- {path_1}
- {path_2}
- ...

Next Steps:
- {recommendation_1}
- {recommendation_2}
========================================
```

## Examples

### Example 1: Market Research
```bash
/prime pesquisa Product: Fone Bluetooth ANC, Category: Eletrônicos, Audience: 20-35 anos tech-savvy, Price: R$ 150-400
```

### Example 2: Ad Generation
```bash
/prime anuncio USER_DOCS/produtos/research/fone_bluetooth_research_notes.md
```

### Example 3: Mentoring
```bash
/prime mentor Como usar palavras-chave no título do Mercado Livre sem violar regras?
```

### Example 4: Brand Strategy
```bash
/prime marca Business: Fones Bluetooth premium, Mission: Democratizar áudio de alta qualidade, Values: Qualidade, Acessibilidade, Inovação, Target: Millennials urbanos
```

### Example 5: AI Photography
```bash
/prime photo subject=Fone Bluetooth, style=lifestyle
```

### Example 6: Video Production
```bash
/prime video subject=Fone Bluetooth, format=reels, duration=30s
```

### Example 7: Course Building
```bash
/prime curso topic=Dropshipping 2025, audience=iniciantes, format=hotmart
```

### Example 8: Meta-Construction
```bash
/prime codexa build-agent: agente de email marketing para e-commerce
```

### Example 9: File Discovery
```bash
/prime scout find all HOP files for pesquisa_agent
```

### Example 10: Voice Mode
```bash
/prime voice start listening
```

## Quality Gates

All workflows enforce quality thresholds:

### Tier 1: Content Production
- **pesquisa**: Quality ≥0.75, Completeness ≥75%, Queries ≥15
- **anuncio**: Quality ≥0.85, Keyword density 0.70-0.80, No compliance violations
- **mentor**: Quality ≥0.87, Skill gaps ≥2, Resources ≥3
- **marca**: Brand consistency ≥0.85, Values 3-5, Positioning ≤2 sentences
- **photo**: Quality ≥7.0/10, All prompts ≥80 words, 9 scenes validated
- **video**: Quality ≥7.0/10, Script coherence ≥0.85, Platform compliance
- **curso**: Quality ≥7.0/10, Module completeness ≥90%, Hotmart compliance

### Tier 2: System & Infrastructure
- **codexa**: Output validation ≥7.0/10, LAW compliance, No broken paths
- **scout**: Path accuracy 100%, Index freshness <24h
- **voice**: Transcription accuracy ≥95%, Latency <2s

## Error Handling

If any phase fails validation:

1. **WARN** (score 0.70-0.84): Report issues, ask user if should proceed
2. **FAIL** (score <0.70): HALT workflow, report specific errors, suggest fixes
3. **RETRY**: For fixable issues, apply suggested solution and re-execute phase
4. **HALT**: For critical issues, stop workflow and wait for user intervention

## Notes

- All workflows use **Dual-Layer Architecture** (ADW + HOP)
- ADW defines **WHAT** and **WHEN** (orchestration)
- HOPs define **HOW** (detailed execution)
- Context strategy: **full_history** (all previous phases inform current phase)
- Minimum LLM: **gpt-4+ or claude-sonnet-4+**

## Architecture Reference

```
agentes/{agent_name}_agent/
├── PRIME.md                          # Entry point (TAC-7)
├── workflows/100_ADW_RUN_{AGENT}.md  # ADW orchestration
├── prompts/{module}_HOP.md           # HOP execution details
└── config/*.json                     # Domain knowledge
```

## Status

### Tier 1: Content Production (7 agents)
| Agent | Status | ADW | Notes |
|-------|--------|-----|-------|
| pesquisa | ✅ PRODUCTION | 100_ADW_RUN_PESQUISA | 10 phases |
| anuncio | ✅ PRODUCTION | 100_ADW_RUN_ANUNCIO | 8 phases |
| mentor | ✅ PRODUCTION | 100_ADW_RUN_MENTOR | 7 phases |
| marca | ✅ PRODUCTION | 100_ADW_RUN_MARCA | 8 phases |
| photo | ✅ PRODUCTION | 100_ADW_RUN_PHOTO | 5 phases |
| video | ✅ PRODUCTION | 100_ADW_RUN_VIDEO | 10 workflows |
| curso | ✅ PRODUCTION | 01-03_ADW_* | 3 workflows |

### Tier 2: System & Infrastructure (3 agents)
| Agent | Status | Type | Notes |
|-------|--------|------|-------|
| codexa | ✅ PRODUCTION | Meta-Builder | 17 ADWs |
| scout | ✅ PRODUCTION | MCP Server | 10+ tools |
| voice | ⚠️ BETA | MCP Server | Requires setup |

### Not Yet Available (2 agents)
- `persona_agent` - No /prime-persona command
- `qa_agent` - No /prime-qa command

**Last Updated**: 2025-12-05 | **Version**: 2.0.0
