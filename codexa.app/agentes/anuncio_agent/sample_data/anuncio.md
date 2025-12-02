# /prime-anuncio

## 🎯 Purpose
Provide focused context and instructions for working with the **Anuncio Agent** - the TAC-7 system responsible for generating high-conversion marketplace listings for Brazilian e-commerce platforms (Mercado Livre, Shopee, Magalu, Amazon BR).

This prime ensures AI assistants understand the agent's architecture, execution patterns, and integration points without reading the entire codebase.

## 🤖 INSTRUCTIONS FOR AI ASSISTANTS

**IMPORTANT:** DO NOT READ prompts or configs DIRECTLY. Use the discovery workflow below.

### Discovery-First Workflow

1. **Understand Agent Structure**:
   ```bash
   # List available prompt modules
   ls -1 anuncio-agent/prompts/*.md

   # Check configuration files
   ls -1 anuncio-agent/config/*.json

   # View output templates
   ls -1 anuncio-agent/templates/*.md
   ```

2. **Check Available Options**:
   ```bash
   # Compliance rules per marketplace
   cat anuncio-agent/config/copy_rules.json | head -50

   # Persuasion frameworks and mental triggers
   cat anuncio-agent/config/persuasion_patterns.json | head -50

   # Marketplace technical specifications
   cat anuncio-agent/config/marketplace_specs.json | head -50
   ```

3. **Execute Agent Workflow**:
   ```bash
   # Via HOP framework (recommended)
   /hop_anuncio

   # Verify outputs were generated
   ls -1 USER_DOCS/produtos/marketplace/*.md | tail -5
   ```

### When to Use
Use `/prime-anuncio` when:
- **Starting work on the Anuncio Agent** - need quick context without reading all prompts
- **Debugging agent execution** - understand workflow without deep code dive
- **Modifying agent behavior** - know what configs/prompts control what behavior
- **Creating agent documentation** - understand integration points and data flow
- **Onboarding new contributors** - provide focused context on agent capabilities
- **Troubleshooting output quality** - know where compliance rules and persuasion patterns are defined

**DO NOT use this prime for**:
- Other agents (use `/prime-pesquisa`, `/prime-marca`, `/prime-knowledge` instead)
- Generic e-commerce questions (this is agent-specific context)
- Deep prompt engineering (this provides architecture, not prompt details)

### Key Files for Context
- **Main Orchestrator**: `anuncio-agent/prompts/main_agent.md` - coordinates all sub-modules
- **Specialized Modules**:
  - `titulo_generator.md` - generates 3 title options (58-60 chars)
  - `keywords_expander.md` - expands to 115-120 keywords
  - `descricao_builder.md` - creates long description (≥3,300 chars)
  - `image_prompts_generator.md` - generates 9 image prompts (3x3 grid)
  - `video_script_veo3.md` - creates video script for VEO3
  - `seo_metadata.md` - generates SEO metadata
  - `qa_validation.md` - validates compliance and quality
  - `variacoes_s5.md` - creates 3 StoryBrand variations
- **Configuration**:
  - `config/copy_rules.json` - ANVISA/INMETRO/CONAR compliance per marketplace
  - `config/persuasion_patterns.json` - PNL, mental triggers, StoryBrand frameworks
  - `config/marketplace_specs.json` - technical specs (char limits, image sizes, etc.)
- **Templates**:
  - `templates/output_template.md` - final announcement structure
  - `templates/research_notes_schema.json` - input validation schema

### When to Read Source
ONLY when:
- Discovery commands don't provide needed information
- User requests specific prompt/config analysis for modifications
- Debugging agent behavior requires understanding prompt logic
- Extending agent capabilities (adding new modules, marketplaces, frameworks)

---

## Agent Framework

### Input Requirements
The Anuncio Agent expects `research_notes.md` files with 22 structured blocks from `pesquisa-agent`:
1. Briefing de Produto
2. Análise de Competidores
3. Gaps Competitivos
4. Taxonomia SEO
5. Keywords de Alto Volume
6. Análise de Imagens
7. Cluster de Informações
8. Preço Competitivo
9. Argumentos de Venda
10. Objeções e Respostas
11. Gatilhos Mentais
12. Call-to-Actions
13. Social Proof
14. Diferenciação de Marca
15. Benefícios vs Features
16. Tom de Voz
17. Compliance (ANVISA/INMETRO/CONAR)
18. Estrutura de Descrição
19. Storytelling e Narrativa
20. Proof Points
21. Resumo Executivo
22. Metadados

### Output Structure
Generated announcements follow this structure:
```markdown
# [Produto] - [Título Principal]

## Metadados
- Categoria, Público-alvo, Preço, Marketplace

## Títulos (3 variações)
1. Título emocional (58-60 chars)
2. Título técnico (58-60 chars)
3. Título equilibrado (58-60 chars)

## Keywords (115-120 termos)
- Long-tail, short-tail, branded, transactional, informational

## Descrição Longa (≥3,300 chars)
- Opening hook
- StoryBrand framework
- Features + benefits
- Social proof
- CTA

## 9 Prompts de Imagem (Grid 3x3)
- Hero, context, detail, lifestyle, scale, packaging, texture, action, benefit

## Roteiro de Vídeo VEO3
- Hook, demo, proof, CTA (30-60s)

## 3 Variações StoryBrand (S5)
- Emocional, técnica, equilibrada

## Metadados SEO
- Meta title, description, OG tags, schema markup
```

### Execution Context

**Workflow:**
1. User provides `research_notes.md` in `USER_DOCS/produtos/research/`
2. User invokes `/hop_anuncio` command
3. HOP framework orchestrates agent execution:
   - Validates input via `research_notes_schema.json`
   - Loads marketplace-specific configs
   - Executes 8 prompt modules in sequence
   - Validates output via `qa_validation.md`
   - Generates final announcement using `output_template.md`
4. Output saved to `USER_DOCS/produtos/marketplace/[produto]_anuncio.md`

**Quality Gates:**
- Input validation (22 blocks present)
- Compliance validation (no forbidden claims)
- Quality validation (≥3,300 chars description, 115-120 keywords)
- Consistency validation (tone, brand voice, messaging)

**Performance:**
- Average execution time: 3-5 minutes
- Success rate: 97%+ (with valid research_notes input)
- Output quality: Consistently ≥4.5/5 on internal quality rubric

### Integration Points

**Upstream:**
- **pesquisa-agent** → provides `research_notes.md`
- User briefs → initial product requirements

**Downstream:**
- **USER_DOCS/produtos/marketplace/** → final announcements
- Marketplace publishing (manual or API)
- A/B testing (3 variations ready)

**Parallel:**
- **brand-agent** → provides brand guidelines for tone/voice
- Compliance databases → ANVISA/INMETRO/CONAR rules

**Configuration:**
- Marketplace rules updated quarterly (compliance changes)
- Persuasion patterns versioned (A/B test results)
- Technical specs synced with marketplace APIs

## Best Practices

### For AI Assistants Working with Anuncio Agent

1. **Always validate input first**:
   ```bash
   # Check research_notes exists and has required blocks
   cat USER_DOCS/produtos/research/[produto]_research_notes.md | grep "##"
   ```

2. **Check marketplace specs before modifications**:
   ```bash
   # Verify char limits, image specs, compliance rules
   cat anuncio-agent/config/marketplace_specs.json | grep -A 5 "mercado_livre"
   ```

3. **Test compliance rules with edge cases**:
   ```bash
   # Review forbidden claims for target marketplace
   cat anuncio-agent/config/copy_rules.json | grep -A 10 "forbidden_claims"
   ```

4. **Verify all 8 modules executed**:
   ```bash
   # Check generated announcement has all sections
   cat USER_DOCS/produtos/marketplace/[produto]_anuncio.md | grep "^##"
   ```

5. **Quality-check keyword count**:
   ```bash
   # Ensure 115-120 keywords generated
   cat USER_DOCS/produtos/marketplace/[produto]_anuncio.md | grep -A 50 "## Keywords" | wc -w
   ```

### Common Pitfalls

❌ **Reading all prompts at once** → Use discovery commands instead
❌ **Ignoring compliance rules** → Always check `copy_rules.json` first
❌ **Modifying prompt modules directly** → Test in `/custom` directory first
❌ **Skipping input validation** → Agent fails without proper `research_notes.md`
❌ **Ignoring marketplace specs** → Output may be rejected by marketplace

### Extension Points

**To add a new marketplace:**
1. Add specs to `marketplace_specs.json`
2. Add compliance rules to `copy_rules.json`
3. Update `main_agent.md` orchestrator
4. Test with sample `research_notes.md`

**To add a new prompt module:**
1. Create `anuncio-agent/prompts/[module_name].md`
2. Add to `main_agent.md` execution sequence
3. Update `output_template.md` if needed
4. Add quality validation in `qa_validation.md`

**To add a new persuasion framework:**
1. Document in `persuasion_patterns.json`
2. Reference in relevant prompt modules
3. Add examples to `variacoes_s5.md`
4. A/B test and measure conversion impact

## Related Primes

- `/prime-pesquisa` - Research agent that generates input for anuncio-agent
- `/prime-marca` - Brand agent that provides brand guidelines
- `/prime-hop` - HOP framework orchestration system

## Version History

- **v1.0** (2025-11-10): Initial prime creation with "When to Use" section
- Follows pattern documented in `TAXONOMY_VALIDATION.md`
