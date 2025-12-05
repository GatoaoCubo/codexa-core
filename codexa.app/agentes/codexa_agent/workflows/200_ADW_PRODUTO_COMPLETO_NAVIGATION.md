# 200_ADW_PRODUTO_COMPLETO | LLM Navigation & Performance Guide

**Purpose**: Optimize LLM context loading for product creation pipeline
**Type**: Navigation Guide | **Version**: 1.0.0
**For**: `/spawn`, `/prime-anuncio`, `/codexa-orchestrate`

---

## DIAGNOSTICO DE PERFORMANCE

### Metricas do Index (Scout)

```
Total Files Indexed: 1,955
Index Build Time: 4,687ms (~5s)
Search Time: 17ms (avg)

By Category:
├── ADW (workflows): 65 files
├── HOP (prompts): 70 files
├── ISO Vectorstore: 222 files
├── Config: 39 files
├── Docs: 28 files
└── Other: 1,531 files

By Agent:
├── codexa_agent: 253 files (13 critical)
├── anuncio_agent: 109 files (6 critical)
├── photo_agent: 80 files
├── pesquisa_agent: 108 files
└── Others: 1,405 files
```

---

## PATHS CRITICOS PARA PIPELINE

### Tier 1: CRITICAL (sempre carregar)

```
CODEXA_AGENT (Orchestrator):
├── codexa.app/agentes/codexa_agent/PRIME.md                    [100]
├── codexa.app/agentes/codexa_agent/INSTRUCTIONS.md             [95]
└── codexa.app/agentes/codexa_agent/workflows/200_ADW_PRODUTO_COMPLETO.md [85]

ANUNCIO_AGENT (Content):
├── codexa.app/agentes/anuncio_agent/PRIME.md                   [100]
├── codexa.app/agentes/anuncio_agent/INSTRUCTIONS.md            [95]
└── codexa.app/agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md [85]

PHOTO_AGENT (Images):
├── codexa.app/agentes/photo_agent/PRIME.md                     [100]
└── codexa.app/agentes/photo_agent/INSTRUCTIONS.md              [95]

PESQUISA_AGENT (Research):
├── codexa.app/agentes/pesquisa_agent/PRIME.md                  [100]
└── codexa.app/agentes/pesquisa_agent/INSTRUCTIONS.md           [95]
```

### Tier 2: HIGH (carregar sob demanda)

```
ADWs:
├── codexa_agent/workflows/200_ADW_PRODUTO_COMPLETO_QUICKREF.md [85]
├── codexa_agent/workflows/300_ADW_MASTER_ANUNCIO_PIPELINE.md   [85]
├── anuncio_agent/workflows/101_ADW_PESQUISA_BRIDGE.md          [85]
└── pesquisa_agent/workflows/ADW_TEMPLATE.md                    [80]

HOPs:
├── anuncio_agent/prompts/10_main_agent_HOP.md                  [85]
└── anuncio_agent/iso_vectorstore/13_HOP_main_agent_HOP.md      [85]

Schemas:
├── anuncio_agent/iso_vectorstore/06_input_schema.json          [80]
└── photo_agent/iso_vectorstore/06_input_schema.json            [80]
```

### Tier 3: MEDIUM (referencia)

```
├── */README.md files
├── */iso_vectorstore/*.md
├── */config/*.json
└── */templates/*.md
```

---

## FLUXO DE CONTEXTO OTIMIZADO

### Cenario: Zero Context → Produto Completo

```
FASE 1: BOOTSTRAP (2-3 tool calls)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tool Call 1: mcp__scout__discover("criar produto anuncio")
  → Returns: Entry points + recommended reading order
  → Context: ~500 tokens

Tool Call 2: Read CLAUDE.md (auto-loaded)
  → Context: ~2,000 tokens

Tool Call 3: Read 200_ADW_PRODUTO_COMPLETO_QUICKREF.md
  → Context: ~3,000 tokens

TOTAL BOOTSTRAP: ~5,500 tokens | 3 calls | ~5s


FASE 2: AGENT PRIMING (parallel reads)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Read in parallel:
├── anuncio_agent/PRIME.md (~1,500 tokens)
├── photo_agent/PRIME.md (~1,200 tokens)
└── pesquisa_agent/PRIME.md (~1,000 tokens)

TOTAL PRIMING: ~3,700 tokens | 3 calls | ~2s


FASE 3: SPAWN EXECUTION
━━━━━━━━━━━━━━━━━━━━━━━━
/spawn (3 agents parallel)
├── pesquisa_agent → produto.json
├── anuncio_agent → anuncio.json
└── photo_agent → photo_prompts.json

SPAWN OVERHEAD: ~500 tokens (task definitions)
SPAWN DURATION: 5-8 min (parallel)


FASE 4: SEQUENTIAL EXECUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scripts execution (no LLM context needed):
├── generate_images.py (Imagen API)
├── upload_to_supabase.py (Storage API)
└── create_product.py (DB + Shopify)

DURATION: 5-10 min


TOTAL CONTEXT BUDGET:
━━━━━━━━━━━━━━━━━━━━━
Bootstrap:     5,500 tokens
Agent Priming: 3,700 tokens
Spawn Tasks:     500 tokens
Margin:        2,300 tokens
─────────────────────────────
TOTAL:        12,000 tokens (optimal)
```

---

## COMANDOS SCOUT PARA NAVEGACAO

### Descoberta Inicial
```
mcp__scout__discover("criar produto completo")
→ Returns entry points + reading order
```

### Contexto de Agente
```
mcp__scout__smart_context(agent="anuncio_agent", max_files=10)
→ Returns must_read files with importance tiers
```

### Busca por Workflow
```
mcp__scout__search(pattern="**/200_ADW*.md")
→ Returns matching ADW files
```

### Validar Paths
```
mcp__scout__validate_paths(paths=["path1", "path2"])
→ Returns valid/invalid + suggestions
```

---

## SPAWN AGENTS CONFIGURATION

### Para /spawn (3 agents parallel)

```yaml
spawn_config:
  agents:
    - name: pesquisa_agent
      task: "Identify product from {reference}, extract features, materials, dimensions, colors, target audience"
      context_files:
        - codexa.app/agentes/pesquisa_agent/PRIME.md
      output: produto.json

    - name: anuncio_agent
      task: "Generate SEO titles (3), keywords (60+), bullets (10), long description, FAQ (5), video script (30s)"
      context_files:
        - codexa.app/agentes/anuncio_agent/PRIME.md
        - codexa.app/agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md
      output: anuncio.json

    - name: photo_agent
      task: "Create 9 professional image prompts: HERO_WHITE, HERO_GRADIENT, SCALE_HAND, LIFESTYLE_VANITY, LIFESTYLE_BEDROOM, DETAIL_MIRROR, DETAIL_JEWELRY, SOCIAL_FLATLAY, SOCIAL_AESTHETIC"
      context_files:
        - codexa.app/agentes/photo_agent/PRIME.md
      output: photo_prompts.json

  merge_strategy: "sequential_after_all"
  output_dir: "USER_DOCS/produtos/{slug}/"
```

### Spawn Command Template
```
/spawn model:sonnet
1. pesquisa_agent: Analyze {URL}, identify product category, extract features (materials, dimensions, colors), research competitor pricing, define target audience. Output: produto.json

2. anuncio_agent: Using product data, generate 3 SEO titles, 60+ keywords, 10 benefit bullets, persuasive long description, 5 FAQs, 30s video script. Output: anuncio.json

3. photo_agent: Create 9 professional image prompts following standard set (HERO_WHITE priority). Include Midjourney and DALL-E versions. Output: photo_prompts.json
```

---

## PERFORMANCE BENCHMARKS

### Context Loading

| Operation | Tokens | Time | Tool Calls |
|-----------|--------|------|------------|
| Scout discover | 500 | 17ms | 1 |
| Read PRIME.md | 1,500 | 50ms | 1 |
| Read ADW | 3,000 | 80ms | 1 |
| Smart context | 800 | 25ms | 1 |

### Execution Times

| Phase | Duration | Parallelizable |
|-------|----------|----------------|
| Bootstrap | 5s | No |
| Agent priming | 2s | Yes (3x) |
| Spawn execution | 5-8 min | Yes (3x) |
| Image generation | 3-5 min | No (API limit) |
| Upload + DB + Shopify | 2-3 min | Partial |
| **TOTAL** | **12-18 min** | |

### Token Budget

| Model | Context Window | Recommended Use |
|-------|----------------|-----------------|
| Claude Haiku | 200K | Simple searches, quick tasks |
| Claude Sonnet | 200K | Agent execution, content gen |
| Claude Opus | 200K | Complex orchestration |

**Optimal for Pipeline**: Sonnet (balance of speed + quality)

---

## ANTI-PATTERNS (evitar)

### 1. Over-loading Context
```
❌ Read all 253 codexa_agent files
✅ Read only PRIME.md + ADW + schema (3 files)
```

### 2. Sequential Agent Calls
```
❌ pesquisa → wait → anuncio → wait → photo
✅ /spawn all 3 in parallel
```

### 3. Re-reading Files
```
❌ Read PRIME.md multiple times in conversation
✅ Read once, reference by context
```

### 4. Manual Path Guessing
```
❌ "I think the file is at..."
✅ mcp__scout__discover("query") or mcp__scout__search("pattern")
```

---

## CHECKLIST DE NAVEGACAO LLM

### Antes de Executar Pipeline
```
[ ] Scout index atualizado (mcp__scout__refresh)
[ ] CLAUDE.md carregado (auto)
[ ] 200_ADW_PRODUTO_COMPLETO_QUICKREF.md lido
[ ] Input do usuario coletado (URL/imagem/texto)
```

### Durante Execucao
```
[ ] Spawn 3 agents com context minimo
[ ] Aguardar merge dos outputs
[ ] Executar scripts sequenciais (sem LLM)
[ ] Validar resultado final
```

### Pos-Execucao
```
[ ] Verificar produto no site
[ ] Commit e push
[ ] Atualizar Scout index se novos arquivos
```

---

## INTEGRACAO COM COMANDOS

### /prime-anuncio
```
Loads: anuncio_agent/PRIME.md
Then: Executes ADW 100_ADW_RUN_ANUNCIO
Context: ~4,000 tokens
```

### /codexa-orchestrate
```
Loads: codexa_agent/PRIME.md + target ADW
Then: Coordinates multi-agent execution
Context: ~6,000 tokens
```

### /spawn
```
Loads: Minimal (task definitions only)
Then: Creates N parallel agent instances
Context: ~500 tokens per agent
```

### /flow do "criar produto"
```
Loads: 200_ADW_PRODUTO_COMPLETO.md
Then: Executes full pipeline
Context: ~12,000 tokens total
```

---

## VERSION HISTORY

**v1.0.0** (2025-12-05):
- Initial navigation guide
- Performance benchmarks
- Scout integration paths
- Spawn configuration

---

**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor
