# DEMO LIVE ARCHITECTURE | CODEXA Pipeline Visualization

**Version**: 1.0.0 | **Created**: 2025-12-05
**Purpose**: Plano completo para demo ao vivo do sistema CODEXA
**Duration Target**: 5-10 minutos de demo impressionante
**Risk Level**: Alto impacto (100% ao vivo)

---

## EXECUTIVE SUMMARY

### O Que Estamos Construindo

Um **frontend de visualizacao em tempo real** que mostra a pipeline CODEXA executando:
- Publico sugere produto aleatorio
- Pipeline executa ao vivo (pesquisa → anuncio → photo → shopify)
- Frontend mostra cada fase acontecendo em tempo real
- Resultado final: produto pronto para marketplace

### Por Que Isso Impressiona

| Audiencia | Impacto |
|-----------|---------|
| Investidores | "Automatiza dias de trabalho em minutos" |
| Desenvolvedores | "Orquestracao multi-agente real, nao simulada" |
| Sellers | "Meu trabalho de semana em 5 minutos" |

---

## ARQUITETURA COMPLETA

### Diagrama de Comunicacao

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DEMO LIVE SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌───────────────┐                        ┌───────────────────────┐    │
│   │  CLAUDE CODE  │                        │   MCP DASHBOARD       │    │
│   │  (Terminal)   │                        │   (Browser)           │    │
│   │               │                        │                       │    │
│   │ ┌───────────┐ │    outputs/            │ ┌───────────────────┐ │    │
│   │ │ Pipeline  │ │    pipeline_state.json │ │   Pipeline Tab    │ │    │
│   │ │ Executor  │─┼───────────────────────▶│ │   - Phases        │ │    │
│   │ └───────────┘ │                        │ │   - Progress      │ │    │
│   │       │       │                        │ │   - Results       │ │    │
│   │       ▼       │                        │ └───────────────────┘ │    │
│   │ ┌───────────┐ │                        │          ▲           │    │
│   │ │  Agents   │ │                        │          │           │    │
│   │ │ pesquisa  │ │                        │    WebSocket         │    │
│   │ │ anuncio   │ │                        │          │           │    │
│   │ │ photo     │ │                        │ ┌────────┴────────┐  │    │
│   │ └───────────┘ │                        │ │  File Watcher   │  │    │
│   │               │                        │ │  (chokidar)     │  │    │
│   └───────────────┘                        │ └─────────────────┘  │    │
│                                            └───────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Componentes do Sistema

| Componente | Responsabilidade | Tecnologia | Status |
|------------|------------------|------------|--------|
| Claude Code | Executa pipeline, emite eventos | Claude CLI | Existente |
| Pipeline State | Arquivo JSON com estado atual | JSON file | A criar |
| File Watcher | Detecta mudancas no state | chokidar | A criar |
| WebSocket Server | Broadcast para clientes | ws (existente) | Estender |
| Pipeline Tab | Visualizacao tempo real | HTML/JS | A criar |

---

## PROTOCOLO DE COMUNICACAO

### Pipeline State Schema

```json
{
  "pipeline_id": "demo_2025-12-05_143000",
  "product_name": "Escova Dentes Cachorro Premium",
  "started_at": "2025-12-05T14:30:00Z",
  "status": "running",

  "phases": [
    {
      "id": "pesquisa",
      "name": "Market Research",
      "status": "completed",
      "progress": 100,
      "started_at": "2025-12-05T14:30:05Z",
      "completed_at": "2025-12-05T14:32:30Z",
      "quality_score": 0.85,
      "outputs": {
        "keywords_count": 47,
        "competitors_count": 5,
        "compliance": ["ANVISA"]
      }
    },
    {
      "id": "anuncio",
      "name": "Ad Copy Generation",
      "status": "running",
      "progress": 65,
      "started_at": "2025-12-05T14:32:35Z",
      "current_step": "Gerando keywords semanticos...",
      "outputs": null
    },
    {
      "id": "photo",
      "name": "Photo Prompts",
      "status": "pending",
      "progress": 0
    },
    {
      "id": "images",
      "name": "Image Generation",
      "status": "pending",
      "progress": 0
    },
    {
      "id": "shopify",
      "name": "Shopify Sync",
      "status": "pending",
      "progress": 0
    }
  ],

  "live_thoughts": [
    {
      "timestamp": "2025-12-05T14:32:40Z",
      "agent": "anuncio_agent",
      "message": "Aplicando framework AIDA para bullet points..."
    },
    {
      "timestamp": "2025-12-05T14:32:45Z",
      "agent": "anuncio_agent",
      "message": "Gerando 3 variacoes de titulo SEO..."
    }
  ],

  "current_results": {
    "title_preview": "Escova Dental Cachorro Premium - Higiene Pet Profissional",
    "keywords_preview": ["escova dente cachorro", "higiene bucal pet", "saude dental canina"],
    "image_prompts_preview": null
  }
}
```

### Eventos WebSocket

```typescript
interface PipelineEvent {
  type: 'phase_started' | 'phase_progress' | 'phase_completed' | 'thought' | 'result_preview';
  payload: {
    phase_id?: string;
    progress?: number;
    message?: string;
    data?: any;
  };
  timestamp: string;
}
```

---

## COMPONENTES DO FRONTEND

### Nova Tab: Pipeline

```html
<!-- Adicionar em index.html -->
<div class="tab" data-tab="pipeline">
  <span class="tab-icon">&#9658;</span>
  Pipeline Live
</div>

<div class="panel" id="pipeline">
  <!-- Header com input -->
  <div class="pipeline-header">
    <input type="text" id="productInput" placeholder="Nome do produto...">
    <button onclick="startPipeline()">▶ INICIAR PIPELINE</button>
  </div>

  <!-- Visualizacao das fases -->
  <div class="pipeline-phases">
    <!-- Dinamico via JS -->
  </div>

  <!-- Pensamentos ao vivo -->
  <div class="pipeline-thoughts">
    <!-- Stream de mensagens -->
  </div>

  <!-- Resultados parciais -->
  <div class="pipeline-results">
    <!-- Preview dos outputs -->
  </div>
</div>
```

### CSS Sugerido

```css
.pipeline-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.pipeline-phases {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.phase-card {
  flex: 1;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  transition: all 0.3s;
}

.phase-card.active {
  border-color: var(--accent-cyan);
  box-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
}

.phase-card.completed {
  border-color: var(--accent-green);
  background: rgba(63, 185, 80, 0.1);
}

.phase-progress {
  height: 4px;
  background: var(--bg-tertiary);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.phase-progress-bar {
  height: 100%;
  background: var(--accent-cyan);
  transition: width 0.3s;
}

.pipeline-thoughts {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  height: 150px;
  overflow-y: auto;
  padding: 1rem;
  font-family: monospace;
  font-size: 0.9rem;
}

.thought-entry {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.thought-entry .agent {
  color: var(--accent-purple);
}

.thought-entry .message {
  color: var(--text-primary);
}
```

### JavaScript

```javascript
// Pipeline state
let pipelineState = null;

// Watch for pipeline updates
function watchPipeline() {
  // WebSocket message handler
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    if (msg.type === 'pipeline_update') {
      pipelineState = msg.data;
      renderPipeline();
    }

    if (msg.type === 'thought') {
      addThought(msg.data);
    }
  };
}

function renderPipeline() {
  const container = document.getElementById('pipelinePhases');

  container.innerHTML = pipelineState.phases.map(phase => `
    <div class="phase-card ${phase.status}">
      <div class="phase-name">${phase.name}</div>
      <div class="phase-status">${phase.status}</div>
      <div class="phase-progress">
        <div class="phase-progress-bar" style="width: ${phase.progress}%"></div>
      </div>
      ${phase.quality_score ? `<div class="phase-score">${(phase.quality_score * 100).toFixed(0)}%</div>` : ''}
    </div>
  `).join('<div class="phase-arrow">→</div>');

  // Update results preview
  if (pipelineState.current_results) {
    renderResults(pipelineState.current_results);
  }
}

function addThought(thought) {
  const container = document.getElementById('pipelineThoughts');
  const entry = document.createElement('div');
  entry.className = 'thought-entry';
  entry.innerHTML = `
    <span class="agent">[${thought.agent}]</span>
    <span class="message">${thought.message}</span>
  `;
  container.appendChild(entry);
  container.scrollTop = container.scrollHeight;
}
```

---

## MODIFICACOES NO SERVER

### File Watcher (chokidar)

```javascript
// Adicionar em server.js
import chokidar from 'chokidar';

const PIPELINE_STATE_PATH = join(PROJECT_ROOT, 'outputs', 'pipeline_state.json');

// Watch pipeline state file
const watcher = chokidar.watch(PIPELINE_STATE_PATH, {
  persistent: true,
  ignoreInitial: true
});

watcher.on('change', (path) => {
  try {
    const state = JSON.parse(readFileSync(path, 'utf8'));
    broadcast({ type: 'pipeline_update', data: state });
    addLog('pipeline', 'INFO', `Pipeline updated: ${state.phases.find(p => p.status === 'running')?.name || 'complete'}`);
  } catch (err) {
    addLog('pipeline', 'ERROR', `Failed to parse pipeline state: ${err.message}`);
  }
});
```

### Nova Rota API

```javascript
// Adicionar em server.js
app.get('/api/pipeline', (req, res) => {
  try {
    if (existsSync(PIPELINE_STATE_PATH)) {
      const state = JSON.parse(readFileSync(PIPELINE_STATE_PATH, 'utf8'));
      res.json(state);
    } else {
      res.json({ status: 'idle', phases: [] });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

---

## INTEGRACAO COM CLAUDE CODE

### Helper Function para Emitir Estado

```python
# codexa.app/agentes/codexa_agent/builders/pipeline_emitter.py

import json
from pathlib import Path
from datetime import datetime

PIPELINE_STATE_PATH = Path("outputs/pipeline_state.json")

def emit_pipeline_state(state: dict):
    """Emite estado da pipeline para o dashboard."""
    state['updated_at'] = datetime.now().isoformat()
    PIPELINE_STATE_PATH.parent.mkdir(exist_ok=True)
    PIPELINE_STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))

def emit_thought(agent: str, message: str, state: dict):
    """Adiciona pensamento ao vivo."""
    if 'live_thoughts' not in state:
        state['live_thoughts'] = []

    state['live_thoughts'].append({
        'timestamp': datetime.now().isoformat(),
        'agent': agent,
        'message': message
    })

    # Keep only last 20 thoughts
    state['live_thoughts'] = state['live_thoughts'][-20:]
    emit_pipeline_state(state)

def update_phase_progress(phase_id: str, progress: int, step: str, state: dict):
    """Atualiza progresso de uma fase."""
    for phase in state.get('phases', []):
        if phase['id'] == phase_id:
            phase['progress'] = progress
            phase['current_step'] = step
            if progress == 100:
                phase['status'] = 'completed'
                phase['completed_at'] = datetime.now().isoformat()
            break
    emit_pipeline_state(state)
```

### Uso no ADW

```markdown
## Durante execucao do 200_ADW_PRODUTO_COMPLETO

### Inicio da Fase 2 (Pesquisa)
```python
state = {
    "pipeline_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    "product_name": "$input.product_name",
    "status": "running",
    "phases": [
        {"id": "pesquisa", "name": "Market Research", "status": "running", "progress": 0},
        {"id": "anuncio", "name": "Ad Copy", "status": "pending", "progress": 0},
        {"id": "photo", "name": "Photo Prompts", "status": "pending", "progress": 0},
        {"id": "images", "name": "Image Gen", "status": "pending", "progress": 0},
        {"id": "shopify", "name": "Shopify", "status": "pending", "progress": 0}
    ]
}
emit_pipeline_state(state)
```

### Durante Pesquisa
```python
emit_thought("pesquisa_agent", "Analisando 23 concorrentes no Mercado Livre...", state)
update_phase_progress("pesquisa", 30, "Competitor analysis", state)

emit_thought("pesquisa_agent", "Identificando keywords principais...", state)
update_phase_progress("pesquisa", 60, "Keyword extraction", state)

emit_thought("pesquisa_agent", "Preco medio detectado: R$89,90", state)
update_phase_progress("pesquisa", 100, "Complete", state)
```
```

---

## FLUXO DA DEMO (5 MINUTOS)

### Timeline

```
[00:00] ABERTURA
- Dashboard aberto no navegador (http://localhost:3456)
- Tab "Pipeline Live" selecionada
- Input vazio, aguardando produto

[00:15] INPUT DO PUBLICO
- Apresentador: "Qual produto voces querem criar?"
- Publico sugere: "Escova de dentes para cachorro"
- Digita no input, clica "INICIAR PIPELINE"

[00:30] FASE 1: PESQUISA (ao vivo)
- Visualizacao mostra fase PESQUISA ativa
- Pensamentos aparecem em tempo real:
  > "Buscando concorrentes no Mercado Livre..."
  > "47 listings analisados"
  > "Preco medio: R$45,90"
- Barra de progresso: 0% → 30% → 60% → 100%
- Quality score aparece: 0.85

[01:30] FASE 2: ANUNCIO (ao vivo)
- Fase PESQUISA fica verde (concluida)
- Fase ANUNCIO fica azul (ativa)
- Pensamentos:
  > "Gerando 3 variacoes de titulo..."
  > "Aplicando framework AIDA..."
  > "Criando 60 keywords semanticos..."
- Preview do titulo aparece em tempo real

[03:00] FASE 3: PHOTO (ao vivo)
- Fase ANUNCIO concluida
- Fase PHOTO ativa
- Pensamentos:
  > "Criando 9 cenas para grid..."
  > "Aplicando triggers PNL..."
- Preview dos prompts aparece

[04:00] FASE 4: GERACAO DE IMAGENS (ao vivo)
- Fase PHOTO concluida
- Fase IMAGES ativa
- Pensamentos:
  > "Chamando Imagen 4.0..."
  > "Gerando imagem 1/9: HERO_WHITE..."
- Thumbnails das imagens aparecem conforme geradas

[04:45] FASE 5: SHOPIFY SYNC
- Todas imagens geradas
- Fase SHOPIFY ativa
- Pensamentos:
  > "Criando produto no Supabase..."
  > "Sincronizando com Shopify..."
- Link do produto final aparece

[05:00] CONCLUSAO
- Todas as fases verdes
- Quality score geral: 0.92
- Link clicavel para o produto no Shopify
- Apresentador: "Pronto. De zero a produto ao vivo em 5 minutos."
```

---

## DEPENDENCIAS TECNICAS

### Packages Adicionais

```json
// package.json do mcp-dashboard
{
  "dependencies": {
    "chokidar": "^3.6.0"  // File watcher
  }
}
```

### Arquivos a Criar

| Arquivo | Descricao |
|---------|-----------|
| `mcp-dashboard/public/index.html` | Adicionar Pipeline Tab |
| `mcp-dashboard/server.js` | Adicionar watcher + rota |
| `outputs/pipeline_state.json` | Estado da pipeline (runtime) |
| `builders/pipeline_emitter.py` | Helper para emitir estado |

### Arquivos a Modificar

| Arquivo | Modificacao |
|---------|-------------|
| `200_ADW_PRODUTO_COMPLETO.md` | Adicionar emissao de eventos |
| `mcp-dashboard/package.json` | Adicionar chokidar |

---

## RISCOS E MITIGACOES

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| API Imagen falha | Media | Alto | Fallback: mostrar prompts gerados (sem imagens) |
| Latencia WebSocket | Baixa | Medio | Polling backup a cada 2s |
| Pipeline demora >5min | Media | Alto | Usar /spawn para paralelizar fases 2-4 |
| Produto muito complexo | Media | Medio | Sugerir produtos simples para demo |
| Erro de rede | Baixa | Alto | Modo offline com dados mockados |

### Fallback Plan

```
SE pipeline falhar:
  1. Mostrar erro na UI graciosamente
  2. Exibir resultados parciais (ate onde chegou)
  3. Ter screenshot/video de backup de demo anterior
  4. Explicar: "Isso e ao vivo, erros acontecem - mas o sistema se recupera"
```

---

## CHECKLIST PRE-DEMO

### 1 Dia Antes
- [ ] Testar pipeline completa 3x
- [ ] Verificar API keys (Imagen, Supabase, Shopify)
- [ ] Testar WebSocket em rede local
- [ ] Preparar 3 produtos de backup (caso publico sugira algo impossivel)

### 1 Hora Antes
- [ ] Iniciar mcp-dashboard (`npm run start`)
- [ ] Verificar conexao WebSocket (status: Connected)
- [ ] Testar uma pipeline rapida
- [ ] Limpar outputs/ de execucoes anteriores

### 5 Minutos Antes
- [ ] Abrir dashboard em fullscreen
- [ ] Tab "Pipeline Live" selecionada
- [ ] Input limpo
- [ ] Respirar fundo

---

## PROXIMO PASSO

### Ordem de Implementacao

1. **Frontend Pipeline Tab** (2-3h)
   - Adicionar tab e panel em index.html
   - CSS para visualizacao de fases
   - JavaScript para WebSocket handling

2. **Backend Watcher** (1h)
   - Instalar chokidar
   - Adicionar watcher em server.js
   - Adicionar rota /api/pipeline

3. **Pipeline Emitter** (1-2h)
   - Criar pipeline_emitter.py
   - Integrar com 200_ADW_PRODUTO_COMPLETO

4. **Teste End-to-End** (1h)
   - Executar pipeline completa
   - Verificar visualizacao no dashboard

5. **Polish e Fallbacks** (1-2h)
   - Animacoes suaves
   - Tratamento de erros
   - Modo offline/demo

**Tempo Total Estimado**: 6-9 horas de desenvolvimento

---

## RESULTADO ESPERADO

Apos implementacao, o apresentador podera:

1. Abrir `http://localhost:3456` em qualquer navegador
2. Ir para tab "Pipeline Live"
3. Digitar qualquer produto
4. Assistir ao vivo:
   - Fases executando com progresso visual
   - Pensamentos dos agentes em tempo real
   - Resultados parciais aparecendo
   - Imagens sendo geradas
   - Link final do produto

**Diferencial**: Nao e uma simulacao. E meta-construcao real, ao vivo, com sistema de producao.

---

**Version**: 1.0.0
**Author**: CODEXA Meta-Constructor
**Status**: Planning Complete - Ready for Implementation
