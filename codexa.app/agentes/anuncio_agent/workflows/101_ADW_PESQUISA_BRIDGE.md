# 101_ADW_PESQUISA_BRIDGE

**ID**: 101_ADW_PESQUISA_BRIDGE
**Version**: 1.0.0
**Type**: ADW (Bridge Workflow)
**Chain**: pesquisa_agent → anuncio_agent

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_pesquisa_bridge",
  "workflow_name": "Research to Anuncio Bridge",
  "agent": "anuncio_agent",
  "version": "1.0.0",
  "type": "bridge",
  "chain": "pesquisa_agent → anuncio_agent",
  "context_strategy": "isolated",
  "failure_handling": "stop_and_report",
  "min_llm_model": "claude-sonnet-4-20250514",
  "required_capabilities": {
    "scout_mcp": true,
    "file_parsing": true,
    "yaml_extraction": true
  },
  "quality_threshold": 7.0,
  "estimated_duration": "2-3 minutes",
  "phases": ["LOCATE", "EXTRACT", "VALIDATE", "HANDOFF"]
}
```

---

## PURPOSE

Bridges research output from `pesquisa_agent` to `anuncio_agent` input, ensuring data flows correctly between agents.

---

## INPUT_CONTRACT

From `pesquisa_agent`:
- `$research_file`: Path to research output (USER_DOCS/Pesquisa/*.md)

Expected research data:
```yaml
keywords_principais: [string array]
faixa_preco_mercado: string (e.g., "R$ 89-199")
diferenciais_competitivos: [string array]
tendencias: [string array]
competidores: [object array]
```

---

## PHASES

### Phase 1: LOCATE (30s)
Discover pesquisa outputs for target product.

```bash
# Using Scout
mcp__scout__discover("pesquisa output for [product_name]")

# OR direct glob
Glob: USER_DOCS/Pesquisa/*[product_name]*.md
```

**Output**: `$research_paths` (list of matching files)

---

### Phase 2: EXTRACT (1min)
Parse research file and extract anuncio-relevant data.

```python
# Extraction mapping
RESEARCH_TO_ANUNCIO = {
    "keywords_principais": "title_keywords",
    "faixa_preco_mercado": "price_positioning",
    "diferenciais_competitivos": "bullet_highlights",
    "tendencias": "emotional_hooks",
    "competidores.gaps": "differentiation_points"
}
```

**Output**: `$anuncio_context` (structured JSON)

---

### Phase 3: VALIDATE (30s)
Check data completeness before handoff.

```markdown
## Validation Checklist
- [ ] keywords_principais has ≥3 items
- [ ] faixa_preco_mercado is defined
- [ ] diferenciais_competitivos has ≥2 items
- [ ] Quality score ≥7.0/10
```

**Output**: `$validation_result` (pass/fail + score)

---

### Phase 4: HANDOFF (30s)
Prepare context for anuncio_agent.

```handoff
contexto: Research complete for [product_name]
arquivos_gerados:
  - USER_DOCS/Pesquisa/[product]_analysis.md
proximo: Run anuncio_agent with research context
dados:
  keywords: $anuncio_context.title_keywords
  price: $anuncio_context.price_positioning
  highlights: $anuncio_context.bullet_highlights
  hooks: $anuncio_context.emotional_hooks
qualidade: $validation_result.score
```

---

## OUTPUT_CONTRACT

- `$handoff_block`: Formatted handoff for anuncio_agent
- `$anuncio_context`: Extracted context JSON

---

## TRIGGERS

### Manual
```bash
/flow do "bridge pesquisa to anuncio for [product]"
```

### Automatic (after pesquisa)
```bash
# In pesquisa workflow completion:
NEXT_WORKFLOW: 101_ADW_PESQUISA_BRIDGE
```

### Via Spawn
```bash
/spawn
1. explore: find pesquisa output for [product]
2. review: validate research quality
3. build: execute 101_ADW_PESQUISA_BRIDGE
```

---

## EXAMPLE

### Input (pesquisa output)
```markdown
# Análise: Arranhador Gato Modular

## Keywords Principais
- arranhador gato
- brinquedo gato modular
- arranhador vertical

## Faixa de Preço Mercado
R$ 89 - R$ 249 (média: R$ 159)

## Diferenciais Competitivos
- Design modular (único no mercado)
- Material sustentável
- Fácil montagem sem ferramentas
```

### Output (anuncio context)
```json
{
  "title_keywords": ["arranhador gato", "modular", "premium"],
  "price_positioning": "mid-high (R$ 159-199)",
  "bullet_highlights": [
    "Design modular único",
    "Material sustentável",
    "Montagem sem ferramentas"
  ],
  "emotional_hooks": ["orgulho", "praticidade", "sustentabilidade"]
}
```

### Generated Handoff
```handoff
contexto: Research complete for Arranhador Gato Modular
arquivos_gerados:
  - USER_DOCS/Pesquisa/arranhador_analysis.md
proximo: Run /anuncio with research context
dados:
  keywords: ["arranhador gato", "modular", "premium"]
  price: "mid-high (R$ 159-199)"
  highlights: ["Design modular único", "Material sustentável", "Montagem sem ferramentas"]
qualidade: 8.5/10
```

---

## INTEGRATION

### With /flow
```bash
/flow plan "criar anuncio com pesquisa para [product]"
# Automatically includes bridge phase
```

### With /spawn
```bash
/spawn
1. build: pesquisa for [product]
2. build: bridge pesquisa→anuncio
3. build: anuncio with context
```

---

## VALIDATION

Quality gate (≥7.0/10):
- [ ] Keywords extracted (3+ items)
- [ ] Price positioning defined
- [ ] Differentiators mapped (2+ items)
- [ ] Handoff format correct

---

**Version**: 1.1.0
**Created**: 2025-12-03
**Type**: Bridge Workflow (pesquisa → anuncio)
