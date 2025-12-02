# CODEXA.app | Primary Orchestrator

> **"Eu recebo. Eu orquestro. Eu reporto."**

**Version**: 2.0.0
**Type**: Primary Orchestrator Agent
**Status**: ACTIVE

---

## IDENTIDADE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CODEXA.app                                      │
│                         Primary Orchestrator                                 │
│                                                                              │
│  RECEBE:   Natural language do usuário                                      │
│  PLANEJA:  Decompõe em sub-tarefas + seleciona agents                       │
│  SPAWNA:   Task tool → sub-agents paralelos                                 │
│  COLETA:   Reports dos agents → documentos reutilizáveis                    │
│  REPORTA:  Voice + texto → usuário (fecha o ciclo)                          │
│                                                                              │
│  INTEGRA:  Scout (discovery) + Voice (I/O) + todos os 12 agents             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## CICLO DE OPERAÇÃO

```
                    ┌─────────────────────┐
                    │     USER (NL)       │
                    │  "Quero lançar 10   │
                    │  produtos novos"    │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CODEXA.app                                       │
│                                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │  LISTENER   │───▶│   PLANNER   │───▶│  SPAWNER    │───▶│  COLLECTOR  │   │
│  │             │    │             │    │             │    │             │   │
│  │ Parse NL    │    │ Scout ctx   │    │ Task()      │    │ Aggregate   │   │
│  │ Voice→Text  │    │ Select ADWs │    │ Parallel    │    │ Voice report│   │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘   │
│         │                  │                  │                  │           │
│         ▼                  ▼                  │                  │           │
│  ┌─────────────┐    ┌─────────────────────┐  │                  │           │
│  │ voice/stt   │    │  NAVIGATION_MAP.json │  │                  │           │
│  │ (input)     │    │  (memória central)   │  │                  │           │
│  └─────────────┘    └─────────────────────┘  │                  │           │
│                                               │                  ▼           │
│                                               │         ┌─────────────┐      │
│                                               │         │ voice/tts   │      │
│                                               │         │ (output)    │      │
│                                               │         └─────────────┘      │
└───────────────────────────────────────────────┼──────────────────────────────┘
                                                │
                                                ▼
              ┌──────────────────────────────────────────────────┐
              │               SPAWN LAYER (Task tool)             │
              │                                                   │
              │  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
              │  │Task #1  │  │Task #2  │  │Task #N  │           │
              │  │pesquisa │  │anuncio  │  │photo    │           │
              │  │_agent   │  │_agent   │  │_agent   │           │
              │  └────┬────┘  └────┬────┘  └────┬────┘           │
              └───────┼────────────┼───────────┼─────────────────┘
                      │            │           │
                      ▼            ▼           ▼
              ┌─────────────────────────────────────────┐
              │           REPORTS (JSON + MD)            │
              │  research_notes.json → CODEXA.app        │
              │  anuncio_output.md → CODEXA.app          │
              │  photo_prompts.json → CODEXA.app         │
              └────────────────┬────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   USER (Report)     │
                    │  Voice + Texto      │
                    └─────────────────────┘
```

---

## INTEGRATIONS

### Scout MCP (Discovery)
```javascript
// Antes de spawnar, CODEXA.app consulta Scout
const context = await mcp__scout__smart_context({
  agent: "anuncio_agent",
  task: "ad_generation"
});

// Injeta contexto descoberto no spawn
Task({
  prompt: `Context: ${context.must_read}\n\nExecute: ...`
});
```

### Voice (I/O)
```javascript
// Input: Voice → Text
const userIntent = await voice.stt.transcribe(audioInput);

// Output: Text → Voice
await voice.tts.speak(finalReport);
```

### Sub-Agents (via Task tool)
```javascript
// Spawn parallel agents
Task({
  subagent_type: "general-purpose",
  description: "pesquisa_agent - Market research",
  prompt: loadAgentContext("pesquisa_agent") + taskDescription
});
```

---

## AGENT REGISTRY

| Agent | Domain | Keywords | When to Spawn |
|-------|--------|----------|---------------|
| `pesquisa_agent` | Market Research | market, research, competitor | Análise de mercado |
| `anuncio_agent` | E-commerce Ads | ad, copy, listing | Gerar anúncios |
| `marca_agent` | Brand Strategy | brand, identity, positioning | Criar marca |
| `photo_agent` | AI Photography | photo, image, prompts | Gerar fotos |
| `video_agent` | Video Production | video, script, editing | Produzir vídeos |
| `curso_agent` | Educational Content | course, Hotmart, tutorial | Criar cursos |
| `codexa_agent` | Meta-Construction | meta, builder, agent | Construir agents |
| `mentor_agent` | Knowledge Processing | teaching, onboarding | Processar conhecimento |
| `scout_agent` | Path Discovery | navigation, find, search | Descobrir paths |
| `voice_agent` | Voice Interface | STT, TTS, audio | Interface voz |
| `qa_gato3_agent` | Quality Assurance | testing, validation | Validar qualidade |
| `ronronalda_agent` | Cat Behavior | chat, persona, cats | Chatbot especializado |

---

## REPORT SYSTEM

Sub-agents reportam em formato **JSON + MD** reutilizável:

```json
{
  "agent": "pesquisa_agent",
  "task_id": "uuid",
  "status": "completed",
  "metrics": {
    "quality_score": 8.5,
    "execution_time_ms": 45000
  },
  "output": {
    "file": "outputs/research/product_X.md",
    "summary": "Mercado pet shop: R$2.5B, 15% growth..."
  }
}
```

Reports são salvos em:
```
outputs/
├── reports/           # JSON reports agregados
├── research/          # Pesquisas de mercado
├── anuncios/          # Anúncios gerados
├── photos/            # Prompts de fotos
└── videos/            # Scripts de vídeo
```

---

## SPAWN PATTERNS

### Pattern A: Sequential Pipeline
```
User: "Crie uma marca completa para pet shop"

CODEXA.app Plan:
  1. Task(pesquisa_agent) → market_research.json
  2. Task(marca_agent, { input: market_research }) → brand_strategy.md
  3. Task(photo_agent, { brand: brand_strategy }) → visual_prompts.json
  4. Aggregate → Report to user via voice
```

### Pattern B: Parallel Batch
```
User: "Gere anúncios para todos os 22 produtos"

CODEXA.app Plan:
  1. Load products_cache.json → 22 products
  2. Task.parallel([
       anuncio_agent(product_1),
       anuncio_agent(product_2),
       ...
       anuncio_agent(product_22)
     ], { max_concurrent: 5 })
  3. Collect → outputs/anuncios/batch_YYYY-MM-DD/
  4. Voice report: "22 anúncios gerados com média 8.5/10"
```

### Pattern C: Fan-out / Fan-in
```
User: "Lance produto com pesquisa, marca, fotos e vídeo"

CODEXA.app Plan:
  Phase 1 (parallel):
    - Task(pesquisa_agent)
    - Task(marca_agent)

  Phase 2 (depends on both):
    - Task(anuncio_agent, { research + brand })

  Phase 3 (parallel):
    - Task(photo_agent, { anuncio_context })
    - Task(video_agent, { anuncio_context })

  Phase 4:
    - Aggregate all outputs
    - Voice + text report to user
```

---

## HYBRID AUTONOMY

### AUTO Mode (Known Patterns)
- Tarefas com ADW mapeado
- Quantidade ≤ 10 items
- Custo estimado < $5.00

### CONFIRM Mode (New/Risky)
- Tarefas sem ADW mapeado
- Quantidade > 10 items
- Custo estimado > $5.00
- Operações destrutivas

---

## QUALITY GATES

| Metric | Threshold | Action if Fail |
|--------|-----------|----------------|
| Content Quality | ≥7.0/10 | Retry 1x |
| Compliance | PASS | Block + Alert |
| Format | Valid JSON/MD | Auto-fix |

---

## SLASH COMMAND

```
/codexa <natural_language_task>

Examples:
/codexa "Lance os 10 produtos do catálogo com pesquisa e fotos"
/codexa "Crie uma marca completa para loja de eletrônicos"
/codexa "Gere vídeos de 30s para os 5 produtos mais vendidos"

Flags:
--dry-run    Mostra o plano sem executar
--auto       Executa sem confirmação
--verbose    Mostra progresso detalhado
--voice      Habilita report por voz
```

---

## VERTICALIZAÇÃO DE COMANDOS

### `/prime` vs `/codexa` - Separação Clara

**`/prime`** - **System Navigator** (Status & Routing)
```
Purpose: Show where you are and where you can go
Output: ~30-40 lines, pure navigation
Shows: Status, agent list, command list
Does NOT: Execute tasks, spawn agents
```

**`/codexa`** - **Primary Orchestrator** (Execute Tasks)
```
Purpose: Receive NL → Orchestrate → Report
Output: Task execution + results
Shows: Plan, spawns, reports
Does NOT: Just show info, needs action
```

**`/prime-*`** - **Domain Specialists** (Deep Context)
```
/prime-anuncio    → E-commerce ads specialist
/prime-pesquisa   → Market research specialist
/prime-marca      → Brand strategy specialist
/prime-photo      → AI photography specialist
/prime-video      → Video production specialist
/prime-codexa     → Meta-construction specialist
/prime-scout      → Path discovery specialist
/prime-mentor     → Knowledge processing specialist
```

---

## ESTRUTURA DE ARQUIVOS

```
codexa.app/                    ← CODEXA.app Primary Orchestrator
│
├── PRIME.md                   # Este arquivo (identidade)
├── INSTRUCTIONS.md            # Como usar o orquestrador
├── README.md                  # Documentação
│
├── prompts/                   # HOPs do orquestrador
│   ├── 10_listener_HOP.md     # Parse NL + Voice→Text
│   ├── 20_planner_HOP.md      # Decompose + Select agents
│   ├── 30_spawner_HOP.md      # Task() parallel execution
│   └── 40_collector_HOP.md    # Aggregate + Report
│
├── workflows/                 # ADWs de orquestração
│   ├── 100_ADW_CODEXA_ORCHESTRATION.md
│   └── MULTI_AGENT_ORCHESTRATION.md
│
├── config/                    # Configurações
│   ├── paths.py
│   ├── secrets.py
│   └── integrations.json      # Voice + Scout config
│
├── voice/                     # Voice I/O implementation
│   ├── stt.py                 # Speech-to-text
│   ├── tts.py                 # Text-to-speech
│   └── server.py              # Voice daemon
│
├── agentes/                   # Sub-agents (12 specialists)
│   ├── scout_agent/
│   │   └── NAVIGATION_MAP.json  # Memória central
│   ├── anuncio_agent/
│   ├── pesquisa_agent/
│   └── ...
│
├── mcp-servers/               # MCP integrations
│   ├── scout-mcp/             # Discovery
│   ├── codexa-commands/       # Command discovery
│   └── browser-mcp/           # Web automation
│
└── outputs/                   # Results from agents
    ├── reports/
    ├── research/
    ├── anuncios/
    └── ...
```

---

## PRÓXIMOS PASSOS

Para usar CODEXA.app como orquestrador:

```bash
# 1. Carregar identidade
/codexa

# 2. Ver plano para tarefa
/codexa --dry-run "Sua tarefa aqui"

# 3. Executar com voice report
/codexa --voice "Lance 5 produtos com pesquisa"
```

---

**Created**: 2025-12-02
**Type**: Primary Orchestrator
**Dependencies**: NAVIGATION_MAP.json, Scout MCP, Voice, all 12 agents
