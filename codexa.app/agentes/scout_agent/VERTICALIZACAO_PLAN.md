# VERTICALIZACAO PLAN: 10 Scouts Paralelos

> **Objetivo**: Mapear todo o projeto em estrutura vertical navegável por LLMs e humanos
> **Formato**: paths/{dense_keywords} para navegação instantânea

---

## ARQUITETURA DO SPAWN

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SCOUT COMMANDER                                       │
│                    (Orquestra 10 scouts paralelos)                           │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────────────────────┐
       │                       │                                       │
       ▼                       ▼                                       ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  SCOUT-01   │   │  SCOUT-02   │   │  SCOUT-03   │   │  SCOUT-04   │
│  AGENTES    │   │  PROMPTS    │   │  WORKFLOWS  │   │  SCHEMAS    │
│  entry-pts  │   │  HOPs/layers│   │  ADWs       │   │  JSON specs │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘

┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  SCOUT-05   │   │  SCOUT-06   │   │  SCOUT-07   │   │  SCOUT-08   │
│  VECTORSTORE│   │  TEMPLATES  │   │  COMMANDS   │   │  MCP/TOOLS  │
│  knowledge  │   │  reusables  │   │  slash cmds │   │  integrations│
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘

                 ┌─────────────┐   ┌─────────────┐
                 │  SCOUT-09   │   │  SCOUT-10   │
                 │  CONTEXT    │   │  OUTPUTS    │
                 │  brand/user │   │  artifacts  │
                 └─────────────┘   └─────────────┘
```

---

## SCOUT-01: AGENTES (Entry Points)

**Missão**: Mapear todos os pontos de entrada de agentes

**Query**: `discover("agent PRIME entry point")` × 12 agentes

**Output Format**:
```
agents/{agent_name}/PRIME.md          → "entry domain capabilities"
agents/{agent_name}/INSTRUCTIONS.md   → "operations how-to"
agents/{agent_name}/README.md         → "details docs"
```

**Dense Keywords Path**:
```
agents/
├── anuncio    {copywriting produto e-commerce shopify}
├── codexa     {meta-constructor agent-builder prompts}
├── curso      {video tutoriais educacao roteiros}
├── marca      {branding identidade visual naming}
├── mentor     {coaching feedback orientacao}
├── pesquisa   {research analise mercado dados}
├── photo      {imagem produto fotografia editing}
├── qa_gato3   {quality-assurance testing}
├── ronronalda {mascote personagem copy}
├── scout      {discovery paths navigation indexing}
├── video      {edicao ffmpeg youtube shorts}
└── voice      {audio speech-to-text interaction}
```

---

## SCOUT-02: PROMPTS (HOPs & Layers)

**Missão**: Catalogar todos os Higher-Order Prompts

**Query**: `search("**/*_HOP.md")` + `search("**/layers/*.md")`

**Output Format**:
```
prompts/{agent}/
├── {XX}_HOP_{name}.md    → "task-specific prompt"
├── layers/               → "behavioral layers"
│   ├── 01_identity       → "who the agent is"
│   ├── 02_operating      → "modes of operation"
│   ├── 03_tool_usage     → "how to use tools"
│   ├── 04_communication  → "how to talk"
│   └── 05_conventions    → "code/style rules"
```

**Dense Keywords Path**:
```
prompts/
├── curso/
│   ├── roteiro_HOP       {outline structure modulos}
│   ├── visual_HOP        {thumbnail design branding}
│   └── script_HOP        {narration hooks ctas}
├── anuncio/
│   ├── produto_HOP       {bullets beneficios urgencia}
│   └── seo_HOP           {keywords meta description}
├── codexa/
│   ├── build_agent_HOP   {scaffold structure prompts}
│   ├── build_prompt_HOP  {layers sections format}
│   └── orchestrate_HOP   {phases coordination}
└── ...
```

---

## SCOUT-03: WORKFLOWS (ADWs)

**Missão**: Mapear Agentic Domain Workflows

**Query**: `search("**/*_ADW*.md")` + `search("**/workflows/**/*.md")`

**Output Format**:
```
workflows/{agent}/
├── {XXX}_ADW_{name}.md   → "multi-phase workflow"
│   ├── phases[]          → "sequential steps"
│   ├── inputs            → "what it needs"
│   ├── outputs           → "what it produces"
│   └── quality_gates     → "validation points"
```

**Dense Keywords Path**:
```
workflows/
├── anuncio/
│   └── 100_ADW_ANUNCIO   {produto→copy→shopify publish}
├── curso/
│   ├── 100_ADW_MODULO    {outline→script→video→review}
│   └── 101_ADW_PRODUCAO  {record→edit→thumbnail→upload}
├── codexa/
│   ├── 100_ADW_ORCHESTRATOR {discover→plan→execute→verify}
│   ├── 110_ADW_NEW_AGENT    {scaffold→prompts→test}
│   └── 120_ADW_CONSOLIDATION {merge→clean→validate}
├── scout/
│   └── 100_ADW_DISCOVERY {index→rank→present}
└── voice/
    └── 100_ADW_VOICE     {listen→process→respond}
```

---

## SCOUT-04: SCHEMAS (JSON Specs)

**Missão**: Catalogar schemas de input/output

**Query**: `search("**/input_schema.json")` + `search("**/schemas/**/*.json")`

**Output Format**:
```
schemas/{agent}/
├── input_schema.json     → "what the agent needs"
├── output_schema.json    → "what it produces"
└── config.json           → "agent settings"
```

**Dense Keywords Path**:
```
schemas/
├── curso/
│   ├── input_schema      {titulo duracao modulos}
│   └── video_spec        {resolucao formato codec}
├── anuncio/
│   ├── input_schema      {produto preco categoria}
│   └── output_spec       {titulo descricao bullets}
└── codexa/
    ├── agent_template    {name domain prompts adws}
    └── hop_template      {sections layers format}
```

---

## SCOUT-05: VECTORSTORE (Knowledge)

**Missão**: Mapear iso_vectorstores de cada agente

**Query**: `search("**/iso_vectorstore/**/*.md")`

**Output Format**:
```
knowledge/{agent}/
├── 01_QUICK_START.md     → "5-min onboarding"
├── 02_PRIME.md           → "core identity"
├── 03_INSTRUCTIONS.md    → "operations"
├── 11_ADW_*.md           → "workflow docs"
├── 13_HOP_*.md           → "prompt docs"
└── 2X_*.md               → "advanced concepts"
```

**Dense Keywords Path**:
```
knowledge/
├── codexa/
│   ├── 01_QUICK_START    {setup first-agent 5min}
│   ├── 11_ADW_orchestrator {phases gates loop}
│   ├── 21_claude_code_meta {hooks settings mcp}
│   └── 22_agent_builder   {patterns templates best-practices}
├── curso/
│   └── video_tutorials   {passo-a-passo scripts}
└── anuncio/
    └── copywriting       {formulas gatilhos beneficios}
```

---

## SCOUT-06: TEMPLATES (Reusables)

**Missão**: Catalogar templates reutilizáveis

**Query**: `search("**/templates/**/*")`

**Output Format**:
```
templates/
├── agent/
│   ├── PRIME_TEMPLATE.md
│   ├── INSTRUCTIONS_TEMPLATE.md
│   └── HOP_TEMPLATE.md
├── docs/
│   ├── README_TEMPLATE.md
│   └── CHANGELOG_TEMPLATE.md
└── output/
    ├── REPORT_STANDARD.md
    └── DESIGN_SYSTEM.md
```

**Dense Keywords Path**:
```
templates/
├── agent/
│   ├── PRIME_TEMPLATE    {identity domain capabilities}
│   ├── INSTRUCTIONS      {operations tools outputs}
│   └── HOP_TEMPLATE      {sections format examples}
├── docs/
│   ├── fractal/ROOT_PRIME {navigation entry-point}
│   └── SETUP_TEMPLATE    {requirements install config}
└── iso/
    ├── MANIFEST_TEMPLATE {index files importance}
    └── OPTIMIZATION      {checklist validation}
```

---

## SCOUT-07: COMMANDS (Slash Commands)

**Missão**: Indexar todos os slash commands

**Query**: Via codexa-commands MCP: `list_commands()`

**Output Format**:
```
commands/
├── global/
│   ├── /prime            → "navigate to PRIME.md"
│   ├── /codexa-*         → "meta-construction"
│   └── /spawn-agent      → "launch parallel agents"
└── agent/
    ├── /curso-*          → "curso agent ops"
    ├── /anuncio-*        → "anuncio agent ops"
    └── /pesquisa-*       → "research ops"
```

**Dense Keywords Path**:
```
commands/
├── global/
│   ├── prime             {entry-point navigation}
│   ├── codexa-distill    {template placeholder hydrate}
│   ├── codexa-build-agent {scaffold prompts adws}
│   └── codexa-orchestrate {multi-phase workflow}
├── curso/
│   ├── curso-outline     {modulos duracao objetivos}
│   └── curso-video       {roteiro thumbnail export}
├── anuncio/
│   ├── anuncio           {produto copy bullets}
│   └── anuncio-publish   {supabase shopify sync}
└── mentor/
    └── mentor-review     {feedback quality-score}
```

---

## SCOUT-08: MCP/TOOLS (Integrations)

**Missão**: Mapear MCP servers e tools disponíveis

**Query**: `search("**/mcp-servers/**/*.js")` + settings.json

**Output Format**:
```
tools/
├── mcp/
│   ├── scout             → "path discovery"
│   │   ├── discover()    → "find relevant files"
│   │   ├── smart_context()→ "agent context"
│   │   └── search()      → "glob patterns"
│   ├── codexa-commands   → "slash command discovery"
│   │   ├── list_commands()
│   │   ├── get_command()
│   │   └── execute_prompt()
│   ├── browser           → "web automation"
│   └── voice             → "audio processing"
└── integrations/
    ├── supabase          → "database/storage"
    ├── shopify           → "e-commerce sync"
    └── elevenlabs        → "text-to-speech"
```

**Dense Keywords Path**:
```
tools/
├── scout_mcp/
│   ├── discover          {query relevance ranking}
│   ├── smart_context     {importance tiers must-read}
│   └── agent_context     {files categories deps}
├── codexa_mcp/
│   ├── list_commands     {all filter category}
│   └── execute_prompt    {expand args context}
└── integrations/
    ├── supabase          {products storage cache}
    └── shopify           {sync publish checkout}
```

---

## SCOUT-09: CONTEXT (Brand/User)

**Missão**: Mapear contextos de marca e usuário

**Query**: `search("**/context/**/*")` + `search("**/user_docs/**/*")`

**Output Format**:
```
context/
├── brand/
│   ├── VISUAL_STYLE.md   → "cores, fontes, logo"
│   ├── TONE_VOICE.md     → "como falar"
│   └── TARGET.md         → "público-alvo"
├── user/
│   ├── products/         → "catálogo"
│   └── content/          → "conteúdo gerado"
└── project/
    ├── CLAUDE.md         → "project laws"
    └── ROADMAP.md        → "próximos passos"
```

**Dense Keywords Path**:
```
context/
├── brand/
│   ├── VISUAL_STYLE      {cores hex fontes espacamento}
│   ├── TONE_VOICE        {personalidade estilo exemplos}
│   └── TARGET_AUDIENCE   {personas dores desejos}
├── user/
│   ├── products          {catalogo precos categorias}
│   └── anuncios          {copy gerado bullets ctas}
└── project/
    ├── CLAUDE.md         {laws distill fractal}
    └── ROADMAP           {features priorities}
```

---

## SCOUT-10: OUTPUTS (Artifacts)

**Missão**: Catalogar outputs gerados

**Query**: `search("**/outputs/**/*")` + `search("**/user_anuncios/**/*")`

**Output Format**:
```
outputs/
├── anuncios/
│   ├── {produto}.md      → "copy gerado"
│   └── batch_*.json      → "lote processado"
├── cursos/
│   ├── roteiros/         → "scripts de video"
│   └── thumbnails/       → "capas geradas"
├── reports/
│   └── quality_*.json    → "relatórios de QA"
└── cache/
    ├── products.json     → "cache de produtos"
    └── publish_log.json  → "log de publicações"
```

---

## EXECUÇÃO PARALELA

### Comando de Spawn

```javascript
// spawn-agent-10-scouts.js
const scouts = [
  { id: 'SCOUT-01', query: 'agent PRIME entry point', pattern: '**/PRIME.md' },
  { id: 'SCOUT-02', query: 'HOP prompt layers', pattern: '**/*_HOP.md' },
  { id: 'SCOUT-03', query: 'ADW workflow phases', pattern: '**/*_ADW*.md' },
  { id: 'SCOUT-04', query: 'schema json spec', pattern: '**/schema*.json' },
  { id: 'SCOUT-05', query: 'vectorstore knowledge', pattern: '**/iso_vectorstore/**/*.md' },
  { id: 'SCOUT-06', query: 'template reusable', pattern: '**/templates/**/*' },
  { id: 'SCOUT-07', query: 'slash command', pattern: '**/.claude/commands/**/*.md' },
  { id: 'SCOUT-08', query: 'MCP server tool', pattern: '**/mcp-servers/**/*.js' },
  { id: 'SCOUT-09', query: 'context brand user', pattern: '**/context/**/*' },
  { id: 'SCOUT-10', query: 'output artifact', pattern: '**/outputs/**/*' },
];

// Executa em paralelo via Task tool
Promise.all(scouts.map(scout =>
  mcp_scout_discover(scout.query)
));
```

---

## OUTPUT FINAL: NAVIGATION_MAP.json

```json
{
  "version": "1.0.0",
  "generated_at": "ISO_TIMESTAMP",
  "stats": {
    "total_files": 500,
    "agents": 12,
    "commands": 46,
    "workflows": 15,
    "prompts": 30
  },
  "navigation": {
    "agents": {
      "path": "codexa.app/agentes/{name}/PRIME.md",
      "keywords": ["agent", "domain", "capabilities"],
      "importance": 100
    },
    "prompts": {
      "path": "codexa.app/agentes/{agent}/prompts/*_HOP.md",
      "keywords": ["prompt", "instructions", "format"],
      "importance": 85
    },
    "workflows": {
      "path": "codexa.app/agentes/{agent}/workflows/*_ADW*.md",
      "keywords": ["workflow", "phases", "automation"],
      "importance": 85
    },
    "commands": {
      "path": ".claude/commands/*.md",
      "keywords": ["slash", "command", "execute"],
      "importance": 70
    },
    "knowledge": {
      "path": "codexa.app/agentes/{agent}/iso_vectorstore/*.md",
      "keywords": ["knowledge", "docs", "reference"],
      "importance": 65
    }
  },
  "quick_paths": {
    "criar agente": "codexa.app/agentes/codexa_agent/prompts/91_meta_build_agent_HOP.md",
    "criar anuncio": "codexa.app/agentes/anuncio_agent/prompts/01_anuncio_HOP.md",
    "criar curso": "codexa.app/agentes/curso_agent/prompts/01_roteiro_HOP.md",
    "pesquisar mercado": "codexa.app/agentes/pesquisa_agent/PRIME.md",
    "editar video": "codexa.app/agentes/video_agent/PRIME.md"
  },
  "llm_dense_index": {
    "copywriting produto e-commerce": ["anuncio_agent", "ronronalda_agent"],
    "video educacao tutorial": ["curso_agent", "video_agent"],
    "branding identidade visual": ["marca_agent", "photo_agent"],
    "meta-construction agent builder": ["codexa_agent", "scout_agent"],
    "research analise dados": ["pesquisa_agent", "qa_gato3_agent"]
  }
}
```

---

## INTEGRAÇÃO COM DASHBOARD

### Novo Endpoint: /api/scout

```javascript
// server.js - adicionar
app.get('/api/scout/verticalize', async (req, res) => {
  // Executa os 10 scouts em paralelo
  const results = await Promise.all([
    scoutDiscover('agent PRIME entry point'),
    scoutDiscover('HOP prompt layers'),
    scoutDiscover('ADW workflow phases'),
    // ... etc
  ]);

  // Monta navigation map
  const navigationMap = buildNavigationMap(results);

  res.json(navigationMap);
});

app.get('/api/scout/search', async (req, res) => {
  const { query, agent, max } = req.query;
  const result = await scoutDiscover(query, agent, max);
  res.json(result);
});
```

### Nova UI: Scout Visualizer

```
┌───────────────────────────────────────────────────────────────────┐
│  [C] CODEXA  Dashboard    │  Commands  │  Scout ←                 │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  🔍 Search: [criar um anuncio de produto____________] [Scout!]   │
│                                                                   │
│  VERTICALIZATION MAP                                              │
│  ════════════════════                                             │
│                                                                   │
│  ┌─────────────────┐                                              │
│  │ 📁 AGENTS (12)  │ ─────────────────────────────────────────   │
│  └────────┬────────┘                                              │
│           │                                                       │
│   ┌───────┴───────┬───────────┬───────────┬───────────┐          │
│   ▼               ▼           ▼           ▼           ▼          │
│ anuncio        curso       marca      pesquisa     codexa        │
│ {copy,e-com}   {video,edu} {brand}    {research}   {meta}        │
│                                                                   │
│  ┌─────────────────┐                                              │
│  │ 📝 PROMPTS (30) │ ─────────────────────────────────────────   │
│  └────────┬────────┘                                              │
│           │                                                       │
│   ┌───────┴───────┬───────────┬───────────┐                      │
│   ▼               ▼           ▼           ▼                      │
│ anuncio_HOP   roteiro_HOP  marca_HOP  research_HOP               │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## PRÓXIMOS PASSOS

1. **Implementar endpoint `/api/scout`** no dashboard server
2. **Criar UI de visualização** do mapa de navegação
3. **Gerar NAVIGATION_MAP.json** estático para cache
4. **Testar spawn paralelo** com 10 scouts
5. **Otimizar dense keywords** baseado em uso real

---

**Status**: ✅ EXECUTED SUCCESSFULLY
**Estimated Files**: ~500
**Agents to Scan**: 12
**Parallel Scouts**: 10

---

## EXECUTION RESULTS (2025-12-02)

### Scout Summary

| Scout | Domain | Files Found | Status |
|-------|--------|-------------|--------|
| SCOUT-01 | Agents Entry Points | 12 agents | ✅ |
| SCOUT-02 | HOPs & Prompts | 30 prompts + 8 layers | ✅ |
| SCOUT-03 | Workflows ADWs | 18 workflows | ✅ |
| SCOUT-04 | JSON Schemas | 36 schemas | ✅ |
| SCOUT-05 | Vectorstore Knowledge | 243 files (13 agents) | ✅ |
| SCOUT-06 | Templates | 32 templates | ✅ |
| SCOUT-07 | Slash Commands | 23 commands | ✅ |
| SCOUT-08 | MCP Servers | 4 servers (33 tools) | ✅ |
| SCOUT-09 | Context Files | 407 files | ✅ |
| SCOUT-10 | Output Artifacts | 92 outputs | ✅ |

### Generated Artifacts

```
codexa.app/agentes/scout_agent/
├── NAVIGATION_MAP.json      ← Primary output (LLM-optimized)
├── VERTICALIZACAO_PLAN.md   ← This file (execution log)
└── iso_vectorstore/         ← Scout knowledge base
```

### Key Metrics

- **Total Files Indexed**: ~500
- **Agents Mapped**: 12 (all with PRIME/INSTRUCTIONS/README)
- **HOPs Cataloged**: 30 (TAC-7 framework)
- **ADWs Documented**: 18 (multi-phase workflows)
- **Commands Available**: 23 (8 prime-*, 6 build-*, 5 voice-*)
- **MCP Tools**: 33 across 4 servers

### Quick Navigation (Dense Keywords)

```
CRIAR AGENTE       → /codexa-build-agent + 91_meta_build_agent_HOP
CRIAR ANUNCIO      → /prime-anuncio + 100_ADW_RUN_ANUNCIO
PESQUISAR MERCADO  → /prime-pesquisa + competitor_intelligence/
CRIAR MARCA        → /prime-marca + 01_brand_identity_HOP
GERAR FOTOS AI     → /prime-photo + 10_scene_planner_HOP
PRODUZIR VIDEO     → /prime-video + video_agent/templates/
CRIAR CURSO        → /prime-curso + curso_agent/context/
USAR VOZ           → /v + voice/mcp_server.py
NAVEGAR PROJETO    → scout MCP + NAVIGATION_MAP.json
```
