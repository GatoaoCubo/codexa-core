# MAESTRO - Meta-Orquestrador Autônomo CODEXA

> **"Eu não executo. Eu orquestro quem executa."**

**Version**: 1.0.0
**Type**: Meta-Orchestrator Agent
**Status**: DRAFT

---

## IDENTIDADE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MAESTRO                                         │
│                                                                              │
│  O cérebro central do CODEXA que sabe:                                      │
│  • ONDE está tudo (via NAVIGATION_MAP.json)                                 │
│  • O QUE cada agente faz (via agent capabilities)                           │
│  • COMO executar (via spawn-agent paralelo)                                 │
│  • QUANDO validar (via quality gates)                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ARQUITETURA

```
                    ┌─────────────────────┐
                    │     USUÁRIO         │
                    │  "Quero lançar 10   │
                    │  produtos novos"    │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              MAESTRO                                          │
│                                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │  LISTENER   │───▶│   PLANNER   │───▶│  SPAWNER    │───▶│  COLLECTOR  │   │
│  │             │    │             │    │             │    │             │   │
│  │ Parse NL    │    │ Decompose   │    │ Task()      │    │ Aggregate   │   │
│  │ Intent      │    │ Select ADWs │    │ Parallel    │    │ Validate    │   │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘   │
│         │                  │                  │                  │           │
│         │                  ▼                  │                  │           │
│         │     ┌─────────────────────┐        │                  │           │
│         │     │  NAVIGATION_MAP.json │        │                  │           │
│         │     │  (Memória Central)   │        │                  │           │
│         │     └─────────────────────┘        │                  │           │
└─────────┼────────────────────────────────────┼──────────────────┼───────────┘
          │                                    │                  │
          │                                    ▼                  │
          │         ┌──────────────────────────────────────┐      │
          │         │         SPAWN LAYER                   │      │
          │         │                                       │      │
          │         │  ┌─────────┐  ┌─────────┐  ┌────────┐│      │
          │         │  │Task #1  │  │Task #2  │  │Task #N ││      │
          │         │  │pesquisa │  │anuncio  │  │photo   ││      │
          │         │  │_agent   │  │_agent   │  │_agent  ││      │
          │         │  └────┬────┘  └────┬────┘  └───┬────┘│      │
          │         └───────┼────────────┼──────────┼──────┘      │
          │                 │            │          │              │
          │                 ▼            ▼          ▼              │
          │         ┌─────────────────────────────────────┐       │
          │         │          RESULTS                     │       │
          │         │  research_notes.json                 │───────┘
          │         │  anuncio_output.md                   │
          │         │  photo_prompts.json                  │
          │         └─────────────────────────────────────┘
```

---

## FLUXO DE OPERAÇÃO

### 1. LISTENER (Parse Intent)

```yaml
Input: "Quero lançar 10 produtos de pet shop com pesquisa completa"

Parsed Intent:
  action: "product_launch"
  quantity: 10
  category: "pet shop"
  scope: "full" (pesquisa + anuncio + photo)

Confidence: 0.95
```

### 2. PLANNER (Decompose & Select)

```yaml
Consulta: NAVIGATION_MAP.json

Selected Agents:
  - pesquisa_agent: "market research per product"
  - anuncio_agent: "ad copy generation"
  - photo_agent: "AI photo prompts"

Selected ADWs:
  - 204_ADW_INTEGRATED_PRODUCT_REFORM (orchestration)
  - 100_ADW_RUN_PESQUISA (per product)
  - 100_ADW_RUN_ANUNCIO (per product)

Execution Plan:
  Phase 1: Parallel research (10 products × pesquisa_agent)
  Phase 2: Parallel ad copy (10 products × anuncio_agent)
  Phase 3: Parallel photos (10 products × photo_agent)
  Phase 4: Quality validation & aggregation
```

### 3. SPAWNER (Execute via Task)

```javascript
// Maestro spawns parallel tasks
const tasks = products.map(product => ({
  agent: "pesquisa_agent",
  prompt: `Execute 100_ADW_RUN_PESQUISA for: ${product.name}`,
  context: loadAgentContext("pesquisa_agent")
}));

// Execute in parallel batches (max 5 concurrent)
await Promise.all(tasks.map(t => Task(t)));
```

### 4. COLLECTOR (Aggregate & Validate)

```yaml
Results:
  - 10/10 research complete (avg score: 8.2/10)
  - 10/10 anuncios generated (avg score: 8.5/10)
  - 10/10 photo prompts ready (avg score: 8.1/10)

Quality Gate: PASSED (all ≥ 7.0)

Final Output:
  - outputs/batch_2024-12-02/research/
  - outputs/batch_2024-12-02/anuncios/
  - outputs/batch_2024-12-02/photos/
```

---

## CAPABILITIES MATRIX

O Maestro sabe invocar qualquer combinação de agentes:

| Task Type | Agents Invoked | ADW Used |
|-----------|----------------|----------|
| `product_launch` | pesquisa → anuncio → photo | 204_ADW_INTEGRATED |
| `market_research` | pesquisa | 100_ADW_RUN_PESQUISA |
| `ad_generation` | anuncio | 100_ADW_RUN_ANUNCIO |
| `brand_creation` | marca | 100_ADW_RUN_MARCA |
| `course_creation` | curso | 01_ADW_QUICK_COURSE |
| `video_production` | video | video_agent pipeline |
| `full_ecommerce` | pesquisa → marca → anuncio → photo → video | CUSTOM_PIPELINE |

---

## NAVIGATION_MAP INTEGRATION

O Maestro carrega o `NAVIGATION_MAP.json` como sua memória:

```javascript
// maestro_context_loader.js
const MEMORY = {
  agents: navigationMap.navigation.agents.items,      // 12 agents
  workflows: navigationMap.navigation.workflows,      // 18 ADWs
  commands: navigationMap.navigation.commands,        // 23 commands
  quickPaths: navigationMap.quick_paths,              // shortcuts
  denseIndex: navigationMap.llm_dense_index          // keyword mapping
};

// Intent → Agent mapping via dense index
function selectAgents(intent) {
  const keywords = extractKeywords(intent);
  return MEMORY.denseIndex
    .filter(entry => matchesKeywords(entry, keywords))
    .map(entry => entry.agents);
}
```

---

## SPAWN PATTERNS

### Pattern 1: Sequential Pipeline

```
User: "Crie uma marca completa para pet shop"

Maestro Plan:
  1. spawn(pesquisa_agent) → market_research.json
  2. spawn(marca_agent, { input: market_research }) → brand_strategy.md
  3. spawn(photo_agent, { brand: brand_strategy }) → visual_prompts.json
```

### Pattern 2: Parallel Batch

```
User: "Gere anúncios para todos os 22 produtos"

Maestro Plan:
  1. load(products_cache.json) → 22 products
  2. spawn_parallel([
       anuncio_agent(product_1),
       anuncio_agent(product_2),
       ...
       anuncio_agent(product_22)
     ], { max_concurrent: 5 })
  3. collect_results() → batch_anuncios/
```

### Pattern 3: Hybrid (Research → Parallel Execute)

```
User: "Descubra os 5 produtos mais promissores e crie anúncios"

Maestro Plan:
  1. spawn(pesquisa_agent) → top_5_products.json
  2. spawn_parallel([
       anuncio_agent(top_1),
       anuncio_agent(top_2),
       anuncio_agent(top_3),
       anuncio_agent(top_4),
       anuncio_agent(top_5)
     ])
  3. spawn(qa_gato3_agent) → validation_report.json
```

---

## HYBRID AUTONOMY

O Maestro opera em modo híbrido:

### AUTO (Known Patterns)
- Tarefas que já tem ADW definido
- Quantidade ≤ 10 items
- Custo estimado < $5.00

### CONFIRM (New/Risky)
- Tarefas sem ADW mapeado
- Quantidade > 10 items
- Custo estimado > $5.00
- Operações destrutivas

```yaml
# Exemplo de confirmação
Maestro: "Vou executar o seguinte plano:"

  TASK: Lançar 50 produtos novos

  PHASES:
    1. Research: 50 × pesquisa_agent (~2h, ~$10)
    2. Ad Copy: 50 × anuncio_agent (~1h, ~$5)
    3. Photos: 50 × photo_agent (~30min, ~$2)

  TOTAL ESTIMADO: ~3.5h, ~$17

  Confirmar? [Y/n]
```

---

## INTEGRAÇÃO COM SCOUT

O Maestro usa o Scout MCP para descoberta dinâmica:

```javascript
// Antes de spawnar, verifica contexto atualizado
const agentContext = await mcp_scout_smart_context({
  agent: "anuncio_agent",
  task: "ad_generation"
});

// Injeta contexto no spawn
spawn(anuncio_agent, {
  context: agentContext.must_read,
  input: productData
});
```

---

## SLASH COMMAND

```markdown
# /maestro

Execute o Meta-Orquestrador CODEXA.

## Usage
/maestro <natural_language_task>

## Examples
/maestro "Lance os 10 produtos do catálogo com pesquisa e fotos"
/maestro "Crie uma marca completa para loja de eletrônicos"
/maestro "Gere vídeos de 30s para os 5 produtos mais vendidos"

## Flags
--dry-run    Mostra o plano sem executar
--auto       Executa sem confirmação (cuidado!)
--verbose    Mostra progresso detalhado
```

---

## PRÓXIMOS PASSOS

1. [ ] Criar `maestro_agent/` structure
2. [ ] Implementar LISTENER (NL parsing)
3. [ ] Implementar PLANNER (NAVIGATION_MAP query)
4. [ ] Implementar SPAWNER (Task parallel)
5. [ ] Implementar COLLECTOR (aggregation)
6. [ ] Criar `/maestro` slash command
7. [ ] Testar com batch de produtos

---

## FILOSOFIA

> **"O Maestro não suja as mãos. Ele conhece quem suja."**

- Não executa ADWs diretamente
- Conhece todas as capabilities via NAVIGATION_MAP
- Spawna o agente certo para cada tarefa
- Coordena resultados e valida qualidade
- Escala horizontalmente via paralelismo

---

**Created**: 2025-12-02
**Author**: CODEXA Meta-Constructor
**Dependencies**: NAVIGATION_MAP.json, scout-mcp, all domain agents
